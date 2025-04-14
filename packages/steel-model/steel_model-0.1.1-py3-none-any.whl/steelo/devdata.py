from datetime import date

from .domain import Auto, Plant, Location, Technology, FurnaceGroup, ProductCategory, Volumes, Year, DemandCenter
from .domain.models import PointInTime, TimeFrame

technology_consumption_dict = {
    "BF-BOF": {
        "materials": {
            "Iron Ore": {"demand": 2, "unit_cost": {"Value": 1.5}},
            "Scrap": {"demand": 0.2, "unit_cost": {"Value": 3.0}},
        },
        "energy": {
            "Electricity": {"demand": -1.0, "unit_cost": {"Value": 0.75}},
            "Hydrogen": {"demand": 0.0, "unit_cost": {"Value": 2.5}},  # 5 times electricity
            "Coal": {"demand": 10.0, "unit_cost": {"Value": 0.5}},
            "Gas": {"demand": 5.0, "unit_cost": {"Value": 0.5}},
        },
    },
    "DRI-EAF": {
        "materials": {
            "Iron Ore": {"demand": 2, "unit_cost": {"Value": 1.5}},
            "Scrap": {"demand": 0.2, "unit_cost": {"Value": 3.0}},
        },
        "energy": {
            "Electricity": {"demand": 6.0, "unit_cost": {"Value": 0.75}},
            "Hydrogen": {"demand": 5.0, "unit_cost": {"Value": 2.5}},
            "Coal": {"demand": 0.0, "unit_cost": {"Value": 0.5}},
        },
    },
    "EAF": {
        "materials": {
            "Iron": {"demand": 0.2, "unit_cost": {"Value": 2.5}},
            "Scrap": {"demand": 1.2, "unit_cost": {"Value": 3.0}},
        },
        "energy": {
            "Electricity": {"demand": 6.0, "unit_cost": {"Value": 0.75}},
            "Hydrogen": {"demand": 0.0, "unit_cost": {"Value": 2.5}},
            "Coal": {"demand": 0.0, "unit_cost": {"Value": 0.5}},
        },
    },
}


capex_switch_dict = {
    "BF-BOF": {"EAF": 10, "DRI-EAF": 13, "BF-BOF": 4},
    "DRI-EAF": {"EAF": 5, "DRI-EAF": 5.5, "BF-BOF": 8},
    "EAF": {"EAF": 5, "DRI-EAF": 8, "BF-BOF": 8},
}


def get_furnace_group(
    *,
    fg_id: str = "fg_group_1",
    tech_name: str = "EAF",
    production: float = 45.0,
    utilization_rate: float = 0.7,
    lifetime: PointInTime = Auto,
    capacity: Volumes = Auto,
) -> FurnaceGroup:
    technology = Technology(
        name=tech_name,
        bill_of_materials=technology_consumption_dict[tech_name],
        product="Steel",
    )
    if not lifetime:
        lifetime = PointInTime(current=Year(2025), time_frame=TimeFrame(start=Year(2015), end=Year(2035)))
    if not capacity:
        capacity = Volumes(int(production / utilization_rate))
    furnace_group = FurnaceGroup(
        furnace_group_id=fg_id,
        capacity=capacity,
        status="Operating",
        last_renovation_date=date(2015, 5, 4),  # TODO @Beth
        technology=technology,
        historical_production={},
        utilization_rate=utilization_rate,
        lifetime=lifetime,
    )
    return furnace_group


def get_plant(
    *,
    plant_id: str = "plant_1",
    tech_name: str = "EAF",
    unit_production_cost: float = 70.0,
    production: float = 45.0,
    location: Location = Auto,
    furnace_groups: list[FurnaceGroup] = Auto,
) -> Plant:
    if not location:
        location = Location(iso3="DEU", country="Germany", region="Europe", lat=49.40768, lon=8.69079)
    if not furnace_groups:
        furnace_groups = [
            get_furnace_group(
                fg_id=f"{plant_id}_fg",
                tech_name=tech_name,
                production=production,
            )
        ]
    return Plant(
        plant_id=plant_id,
        location=location,
        furnace_groups=furnace_groups,
        power_source="unknown",
        soe_status="unknown",
        parent_gem_id="gem_id",
        workforce_size=10,
        certified=False,  # TODO @Beth
        category_steel_product={ProductCategory("Flat")},
    )


def get_demand_center(
    *,
    centre_id: str = "demand_center_1",
    gravity: Location = Auto,
    demand: dict[Year, Volumes] = Auto,
) -> DemandCenter:
    if not demand:
        demand = {Year(2025): Volumes(10), Year(2026): Volumes(20)}
    return DemandCenter(
        demand_center_id=centre_id,
        center_of_gravity=gravity,
        demand_by_year=demand,
    )


furnace_announcement_dates = [
    ("announced", 2028),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2030),
    ("Operating", 2024),
    ("announced", 2031),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2035),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2030),
    ("Operating", 2024),
    ("announced", 2032),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2031),
    ("construction", 2034),
    ("announced", 2032),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2030),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2031),
    ("Operating", 2024),
    ("Operating", 2024),
    ("announced", 2032),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
    ("Operating", 2024),
]
