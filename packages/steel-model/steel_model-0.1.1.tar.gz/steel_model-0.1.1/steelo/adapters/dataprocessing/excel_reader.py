import math
from pathlib import Path

import pandas as pd
from ...domain import (
    Location,
    Technology,
    FurnaceGroup,
    Plant,
    Volumes,
    ProductCategory,
    PointInTime,
    Year,
    TimeFrame,
    DemandCenter,
    PrimaryFeedstock,
    Auto,
)
from ..repositories import InMemoryRepository
from ..dataprocessing.preprocessing.raw_plant_data_processing import execute_preprocessing
from ..dataprocessing.preprocessing.iso3_finder import derive_iso3
from ...config import settings
from ...utilities import global_variables as gv

translate_country_names = {
    "Dem. Rep. of the Congo": "Congo DRC",
    "Hong Kong, China": "Hong Kong",
    "Ivory Coast": "Côte d'Ivoire",
    "Korea, North": "North Korea",
    "Korea, Republic of": "South Korea",
    "Macedonia": "North Macedonia",
    "Russia": "Russian Federation",
}

translate_technology_names = {
    "steel_eaf": "EAF",
    "steel_bof": "BOF",
    "iron_bf": "BF",
    "iron_dri": "DRI",
    "prep_pellet": "Prep Pellet",
    "prep_coke": "Prep Coke",
}


def read_location_from_row(row: dict) -> Location:
    """
    Create a Location object from a dictionary representing a data row.
    """
    return Location(
        lat=row["Latitude"],
        lon=row["Longitude"],
        country=row["Country"],
        region=row["Region"],
        iso3=derive_iso3(lat=row["Latitude"], lon=row["Longitude"]),
        # iso3="DEU",
    )


def read_technology_from_row(row: dict) -> Technology:
    """
    Create a Technology object from a dictionary representing a data row.
    Assigning the product based on the technology name:
      - "EAF" and "BOF" are associated with "Steel".
      - Other technologies are associated with "Iron".
    """
    tech = row["Technology"]
    if tech in ["EAF", "BOF"]:
        product = "Steel"
    else:
        product = "Iron"
    return Technology(
        name=row["Technology"],
        product=product,
    )


def read_pointintime_from_row(row: dict) -> PointInTime:
    """
    Create a PointInTime object from a row dict.

    Uses 'Last renovation year' if available, otherwise falls back to 'Start year'.
    The time frame spans from the base year to base year + 20.

    returns PointInTime object to the furnace group
    """
    if not pd.isna(row.get("Start year")):
        try:
            base_year = int(row["Last renovation year"])
        except (ValueError, TypeError):
            base_year = int(row["Start year"])
        return PointInTime(
            current=Year(gv.SIMULATION_START_YEAR),
            time_frame=TimeFrame(start=Year(base_year), end=Year(base_year + 20)),
        )
    else:
        return PointInTime(
            current=Year(gv.SIMULATION_START_YEAR),
            time_frame=TimeFrame(start=Year(0), end=Year(0)),
        )


def read_furnace_group_from_row(row: dict, iterator: int) -> FurnaceGroup:
    """
    Generate a FurnaceGroup object from a dictionary representing a data row from the GEM data
    This function reads the technology, capacity, and other relevant fields to construct a FurnaceGroup.
    The capacity column is determined based on the product type:
      - "Nominal steel capacity (ttpa)" for steel-based technologies.
      - "Nominal iron capacity (ttpa)" for iron-based technologies.
    """

    technology = read_technology_from_row(row)
    if technology.product == "Steel":
        cap_col = "Nominal steel capacity (ttpa)"
    else:
        cap_col = "Nominal iron capacity (ttpa)"

    try:
        capacity = Volumes(int(row[cap_col]))
    except ValueError:
        capacity = Volumes(0)

    lifetime = read_pointintime_from_row(row)

    return FurnaceGroup(
        furnace_group_id=f"{row['Plant ID']}_{iterator}",
        capacity=capacity,
        status=row["Capacity operating status"],
        lifetime=lifetime,
        last_renovation_date=pd.to_datetime(row["Last renovation year"]),
        technology=technology,
        historical_production={},
        utilization_rate=0.7,
    )


def has_location(row: dict) -> bool:
    """
    Check whether a data row contains valid location information.
    This function verifies that the row dictionary has both "Latitude" and "Longitude" keys with valid

    """
    lat, lon = row.get("Latitude"), row.get("Longitude")
    has_float_latitude = isinstance(lat, float) and not math.isnan(lat)
    has_float_longitude = isinstance(lon, float) and not math.isnan(lon)
    return has_float_latitude and has_float_longitude


def preprocessed_rows_to_domain_objects(
    preprocessed_rows: list[dict], gravity_distances_csv: Path = Auto
) -> dict[str, Plant]:
    """
    Convert a list of preprocessed data rows into domain Plant objects.

    Processes each row to create associated Location, FurnaceGroup, and Plant objects.
    Rows without valid location data are skipped. Additionally, gravity distance data is integrated into each location.
    """
    plants: dict[str, Plant] = {}
    if not gravity_distances_csv:
        gravity_distances_csv = settings.gravity_distances_csv
    gravity_df = pd.read_csv(gravity_distances_csv)
    for num, row in enumerate(preprocessed_rows):
        if not has_location(row):
            # If there's no location -> skip  FIXME maybe do something more sophisticated?
            continue
        location = read_location_from_row(row)
        read_gravity_distances_into_locations([location], gravity_df)

        furnace_group = read_furnace_group_from_row(row, num)
        # repository.furnace_groups.add(furnace_group)
        if (plant := plants.get(row["Plant ID"])) is not None:
            # plant already exists -> just add the furnace group and move on
            plant.furnace_groups.append(furnace_group)
            continue
        else:
            try:
                workforce_size = int(str(row["Workforce size"]))
            except ValueError:
                workforce_size = -1
            try:
                product_categories = {ProductCategory(str(row["Category steel product"]))}
            except ValueError:
                product_categories = set()
            plant = Plant(
                plant_id=str(row["Plant ID"]),
                location=location,
                furnace_groups=[furnace_group],
                power_source=str(row["Power source"]),
                soe_status=str(row["SOE Status"]),
                parent_gem_id=str(row["Parent GEM ID"]),
                workforce_size=workforce_size,
                certified=False,  # TODO @Beth
                category_steel_product=product_categories,
            )
            plants[plant.plant_id] = plant
    return plants


def read_gravity_distances_into_locations(locations: list[Location], gravity_df: pd.DataFrame):
    """
    Update a list of Location objects with gravity distance data.

    For each location, the function extracts gravity distance values from the provided DataFrame and assigns
    these distances to the location's 'distance_to_other_iso3' attribute.

    """
    for location in locations:
        gravity_this_location = gravity_df[gravity_df["iso3_o"] == location.iso3]
        gravity_dict = gravity_this_location.set_index("iso3_d")["dist"].to_dict()
        assert gravity_dict is not None
        location.distance_to_other_iso3 = gravity_dict


def read_plants_into_repository(gravity_distances_csv: Path = Auto) -> InMemoryRepository:
    """
    Load plant and furnace group data into in-memory repository.

    Processes preprocessed plant data to create Plant objects and their associated FurnaceGroup objects,
    and adds them to an InMemoryRepository.
    """
    repository = InMemoryRepository()

    # add plants
    _plant_df, furnace_group_df = execute_preprocessing()
    plants = preprocessed_rows_to_domain_objects(
        furnace_group_df.to_dict(orient="records"), gravity_distances_csv=gravity_distances_csv
    )
    repository.plants.add_list(plants.values())

    # add furnace groups
    furnace_groups = [fg for plant in plants.values() for fg in plant.furnace_groups]
    repository.furnace_groups.add_list(furnace_groups)
    return repository


def read_dynamic_business_cases_into_repository(
    dynamic_business_cases_excel_path: str, excel_sheet: str, repository: InMemoryRepository
):
    """
    Read dynamic business case data from an Excel file and organize it into a dictionary.

    Processes the specified Excel sheet to create PrimaryFeedstock objects based on business case information,
    constraints, material requirements, and energy requirements. Feedstocks are grouped by their technology.

    """
    dynamic_business_cases_df = pd.read_excel(dynamic_business_cases_excel_path, sheet_name=excel_sheet)
    read_feedstocks: dict[str, PrimaryFeedstock] = {}
    for _, row in dynamic_business_cases_df.iterrows():
        side = row["Side"]
        # only reading in inputs for now - as of now no motive for outputs
        if side == "Output":
            continue
        technology = translate_technology_names[row["Business case"]]
        metallic_charge = row["Metallic charge"]
        primary_feedstock_name = f"{technology}_{metallic_charge}"
        if primary_feedstock_name in read_feedstocks:
            primary_feedstock = read_feedstocks[primary_feedstock_name]
        else:
            primary_feedstock = PrimaryFeedstock(metallic_charge=metallic_charge, technology=technology)
        primary_feedstock.metallic_charge = metallic_charge
        primary_feedstock.technology = technology
        row_type = row["Metric type"]
        if row_type == "Constraint":
            constraint_type = row["Type"]
            assert isinstance(constraint_type, str), f"Expected str, got {type(constraint_type)}"
            value = row["Value"]
            primary_feedstock.add_share_constraint(constraint_type, value)
        if row_type == "Materials":
            material = row["Vector"]
            value = row["Value"]
            unit = row["Unit"]
            if material == metallic_charge:
                assert unit in [
                    "t/t product",
                    "t/t pellet",
                ], f"Unit '{unit}' not supported for primary material requirement."
                primary_feedstock.required_quantity_per_ton_of_product = value
            else:
                if unit in ["t/t product", "t/t pellet", "t/t coke"]:
                    converted_value = value
                elif unit == "kg/t product":
                    converted_value = value / 1000
                else:
                    raise ValueError(f"Unit '{unit}' not supported for secondary material requirement.")
                primary_feedstock.add_secondary_feedstock(material, converted_value)
        if row_type == "Energy":
            vector = row["Vector"]
            value = row["Value"]
            unit = row["Unit"]
            if unit.startswith("kWh/t"):
                converted_value = value
            elif unit.startswith("GJ/t"):
                converted_value = value * 0.0036
            elif unit == "kg/t product":
                # ugh, I don't know...
                converted_value = value
            else:
                print(f"Unit '{unit}' not supported for energy requirement.")
            primary_feedstock.add_energy_requirement(vector, converted_value)
        read_feedstocks[primary_feedstock_name] = primary_feedstock

    technology_feedstocks: dict[str, list[PrimaryFeedstock]] = {}
    for primary_feedstock in read_feedstocks.values():
        if primary_feedstock.technology not in technology_feedstocks:
            technology_feedstocks[primary_feedstock.technology] = []
        technology_feedstocks[primary_feedstock.technology].append(primary_feedstock)

    return technology_feedstocks


def read_demand_centers_into_repository(
    demand_excel_path: str,
    demand_sheet_name: str,
    location_csv: str,
    repository: InMemoryRepository = Auto,
    gravity_distances_csv: Path = Auto,
) -> InMemoryRepository:
    """
    Read demand center data from Excel and CSV files and add them into an in-memory repository.

    Performs the following steps:
      1. Reads gravity distance data from a CSV file.
      2. Loads and filters demand data from the specified Excel sheet.
      3. Translates country names using a predefined mapping.
      4. Reads location data from a CSV file and updates each Location with gravity distances.
      5. Constructs DemandCenter objects by matching demand data with locations.
      6. Adds the DemandCenter objects to the repository.
    """
    if not gravity_distances_csv:
        gravity_distances_csv = settings.gravity_distances_csv
    gravity_df = pd.read_csv(gravity_distances_csv)
    demand_df = pd.read_excel(demand_excel_path, sheet_name=demand_sheet_name)

    # TODO: What to do with demand from "other" areas -> might be fixed once we get actual demand data
    demand_df = demand_df[~demand_df["Country"].str.startswith("Other")]
    demand_df = demand_df[~demand_df["Country"].str.startswith("TOTAL")]
    demand_df["Country"] = demand_df["Country"].apply(lambda x: translate_country_names.get(x, x))
    location_df = pd.read_csv(location_csv)
    locations = []
    for _, row in location_df.iterrows():
        location = Location(
            lat=row["latitude"],
            lon=row["longitude"],
            country=row["COUNTRY"],
            region="Unknown",
            # FIXME 5000 km is a bit much, no?
            iso3=derive_iso3(lat=float(row["latitude"]), lon=float(row["longitude"]), max_distance_km=5000),
        )
        locations.append(location)

    # locations = [location for location in locations if location.iso3 in list(gravity_df.iso3_o.unique())]
    read_gravity_distances_into_locations(locations, gravity_df)

    demand_centers = []
    for _, row in demand_df.iterrows():
        try:
            demand_location = next(loc for loc in locations if loc.country == row["Country"])
        except StopIteration:
            raise ValueError(f"Location not found for country: {row['Country']}")
        demand_location.region = row["Region"]
        demand_by_year = {}
        for col in demand_df.columns:
            try:
                year = Year(int(col))
                demand_by_year[year] = Volumes(int(row[col]))
            except ValueError:
                continue
        demand_center = DemandCenter(
            demand_center_id=demand_location.country,
            center_of_gravity=demand_location,
            demand_by_year=demand_by_year,
        )
        demand_centers.append(demand_center)
    if not repository:
        repository = InMemoryRepository()
    repository.demand_centers.add_list(demand_centers)
    return repository
