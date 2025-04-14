from dataclasses import dataclass
from datetime import date
from pathlib import Path

from geopy.distance import geodesic  # type: ignore
from typing import TypeVar, ClassVar, FrozenSet, Any
from collections import defaultdict

from .constants import Auto, Volumes, Year
from . import events, commands
from steelo.utilities.global_variables import ENERGY_EMISSION_FACTORS, ACTIVE_STATUSES, SIMULATION_START_YEAR
import steelo.utilities.global_variables as gv
from ..utilities.utils import merge_two_dictionaries
import json

import logging

logger = logging.getLogger(__name__)


BoundedStringT = TypeVar("BoundedStringT", bound="BoundedString")


class BoundedString(str):
    _valid_values: ClassVar[FrozenSet[str]] = frozenset()  # Make it immutable

    def __new__(cls: type[BoundedStringT], value: str) -> BoundedStringT:
        if value not in cls._valid_values:
            raise ValueError(f"Invalid value for {cls.__name__}: {value}. Valid values are: {cls._valid_values}")
        return str.__new__(cls, value)

    @classmethod
    def is_valid(cls, value: str) -> bool:
        return value in cls._valid_values

    @classmethod
    def all_values(cls) -> FrozenSet[str]:
        return cls._valid_values


class ProductCategory(BoundedString):
    _valid_values = frozenset({"Flat", "Long", "Tubes", "Semi-finished"})


class TimeFrame:
    """
    Holds the start and end year for the model calculations.
    """

    def __init__(self, *, start: Year = Year(2025), end: Year = Year(2050)) -> None:
        self.start = start
        self.end = end

    @property
    def years(self) -> tuple[Year, ...]:
        return tuple(Year(y) for y in range(self.start, self.end + 1))


class PointInTime:
    """
    Holds the current year and the time frame for the model calculations.

    For example, the lifetime of a furnace group is a point in time. It
    started in a specific year and will end in a specific year and how
    much lifetime is left can be calculated based on the current year.
    """

    def __init__(self, *, current: Year = Auto, time_frame: TimeFrame = Auto) -> None:
        if not time_frame:
            time_frame = TimeFrame()
        if not current:
            current = time_frame.start
        self.current = current
        self.time_frame = time_frame

    @property
    def start(self) -> Year:
        return self.time_frame.start

    @property
    def end(self) -> Year:
        return self.time_frame.end

    @property
    def number_of_years(self) -> int:
        return self.end - self.start

    @property
    def remaining_number_of_years(self) -> int:
        return self.end - self.current

    @property
    def elapsed_number_of_years(self) -> int:
        return self.current - self.start

    @property
    def expired(self) -> bool:
        return self.current >= self.end


@dataclass
class Location:
    lat: float
    lon: float
    country: str
    region: str
    iso3: str | None = None
    distance_to_other_iso3: dict[str, float] | None = None


class PrimaryFeedstock:
    def __init__(self, metallic_charge: str, technology: str):
        self.name = f"{technology}_{metallic_charge}"
        self.metallic_charge = None
        self.technology = technology
        self.required_quantity_per_ton_of_product = None
        self.secondary_feedstock: dict[str, float] = {}
        self.energy_requirements: dict[str, float] = {}

    def __repr__(self) -> str:
        return self.name

    def add_secondary_feedstock(self, name: str, share: float) -> None:
        self.secondary_feedstock[name] = share

    def add_maximum_share_in_product(self, limit: float) -> None:
        self.maximum_share_in_product = limit

    def add_minimum_share_in_product(self, limit: float) -> None:
        self.minimum_share_in_product = limit

    def add_energy_requirement(self, vector_name: str, amount: float) -> None:
        self.energy_requirements[vector_name] = amount

    def add_share_constraint(self, constraint_type: str, value: float) -> None:
        assert constraint_type in ["Maximum", "Minimum", "Minium"], f"Invalid constraint type {constraint_type}"
        if constraint_type == "Maximum":
            self.add_maximum_share_in_product(value)
        else:
            self.add_minimum_share_in_product(value)


@dataclass
class Technology:
    name: str
    product: str
    technology_readiness_level: int | None = None
    process_emissions: float | None = None
    dynamic_business_case: list[PrimaryFeedstock] = Auto
    # TODO: all below are dynamic, based on feedstock:
    emissions_factor: float | None = None
    energy_consumption: float | None = None
    bill_of_materials: dict[str, dict[str, dict[str, Any]]] = Auto  # FIXME, dunno how this should look like
    lcop: float | None = None
    capex_type: str | None = None

    _allowed_names = {"EAF", "DRI", "DRI-EAF", "BF", "BOF", "BF-BOF", "OHF", "other", "unknown"}

    def __post_init__(self):
        # Check if the technology name is valid
        if self.name not in self._allowed_names:
            raise ValueError(f"Invalid name: {self.name}")
        if self.capex_type is None:
            self.capex_type = "greenfield"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        # Technologies are equal if they have the same name
        return self.name == other.name

    def __repr__(self) -> str:
        return f"Technology: <{self.name}>"

    def emissions_per_unit(self) -> float:
        emissions_per_unit: float = 0.0
        for feedstock in self.dynamic_business_case:
            if feedstock.required_quantity_per_ton_of_product is None:
                continue

            for sec_fs in feedstock.secondary_feedstock:
                if sec_fs in ENERGY_EMISSION_FACTORS:
                    emissions_per_unit += (
                        feedstock.required_quantity_per_ton_of_product
                        * feedstock.secondary_feedstock[sec_fs]
                        * ENERGY_EMISSION_FACTORS[sec_fs]
                    )
            for en_req in feedstock.energy_requirements:
                # Todo: this is probably wrong though:
                if en_req == "Flexible":
                    emissions_per_unit += (
                        feedstock.required_quantity_per_ton_of_product
                        * feedstock.energy_requirements[en_req]
                        * ENERGY_EMISSION_FACTORS["Natural gas"]
                    )
                if en_req in ENERGY_EMISSION_FACTORS:
                    emissions_per_unit += (
                        feedstock.required_quantity_per_ton_of_product
                        * feedstock.energy_requirements[en_req]
                        * ENERGY_EMISSION_FACTORS[en_req]
                    )
        return emissions_per_unit

    @property
    def technology_capex(self) -> float:
        from .Capex import FULL_GREENFIELD_CAPEX

        name_to_capex = {
            "greenfield": FULL_GREENFIELD_CAPEX,
            "brownfield": {k: v / 2 for k, v in FULL_GREENFIELD_CAPEX.items()},
        }
        if self.capex_type is None:
            raise ValueError("Capex type must not be None")
        capex_dict = name_to_capex.get(self.capex_type)
        if capex_dict is None:
            raise ValueError(f"Unknown capex_type: {self.capex_type}")
        return capex_dict.get(self.name, 0.0)

    def add_feedstock_to_dynamic_business_case(self, primary_feedstock: PrimaryFeedstock) -> None:
        self.dynamic_business_case.append(primary_feedstock)


@dataclass
class ProductionThreshold:
    """Production thresholds for the utilization rate of a furnace group."""

    low: float = 0.1
    high: float = 0.95


class FurnaceGroup:
    def __init__(
        self,
        *,
        furnace_group_id: str,
        capacity: Volumes,
        status: str,
        last_renovation_date: date,
        technology: Technology,
        historical_production: dict[Year, Volumes],
        utilization_rate: float,
        lifetime: PointInTime,
        production_threshold: ProductionThreshold = ProductionThreshold(),
        equity_share: float = 0.2,
        cost_of_debt: float = 0.05,
    ) -> None:
        self.furnace_group_id = furnace_group_id
        self.capacity = capacity
        self.status = status
        self.last_renovation_date = last_renovation_date
        self.technology = technology
        self.historical_production = historical_production
        self.utilization_rate = utilization_rate
        self.lifetime = lifetime
        self.production_threshold = production_threshold
        self.created_by_PAM = False

        # Economic variables
        self.equity_share = equity_share
        self.cost_of_debt = cost_of_debt

    def __repr__(self) -> str:
        return f"FurnaceGroup: <{self.furnace_group_id}>"

    def __eq__(self, other) -> bool:
        return self.furnace_group_id == other.furnace_group_id

    def __hash__(self):
        return hash(self.furnace_group_id)

    def set_technology(self, new_technology: Technology) -> None:
        self.technology = new_technology

    def update_renovation_date(self, new_renovation_date: date) -> None:
        self.last_renovation_date = new_renovation_date

    def renovation_needed(self, current_date: date, average_renovation_frequency: int = 20) -> bool:
        return (current_date.year - self.last_renovation_date.year) > average_renovation_frequency

    def update_utilization_rate(self, utilization_rate: Volumes) -> None:
        self.utilization_rate = utilization_rate

    def report_bill_of_materials(self):
        return {
            item_name: item_dict["demand"] * item_dict["unit_cost"]["Value"] * self.production
            for bom_group, items in self.technology.bill_of_materials.items()
            for item_name, item_dict in items.items()
        }

    @property
    def emissions(self):
        return self.production * self.technology.emissions_per_unit() / (1e6)  # Convert from gram to ton

    @property
    def fixed_opex(self) -> float:
        from .calculate_costs import calculate_fixed_opex

        return calculate_fixed_opex(self.technology.technology_capex)

    @property
    def opex(self) -> float:
        from .calculate_costs import calculate_opex, BillsOfMaterial

        return calculate_opex(
            bill_of_materials=getattr(BillsOfMaterial, self.technology.name.replace("-", "_")),
            fixed_opex=self.fixed_opex * self.capacity,
            production=self.production,
        )

    @property
    def total_investment(self) -> float:
        return self.capacity * self.technology.technology_capex

    @property
    def debt_repayment_per_year(self) -> list[float]:
        from .calculate_costs import calculate_debt_repayment

        """Returns the debt repayment amount for each year of the remaining lifetime."""
        return calculate_debt_repayment(
            total_investment=self.total_investment,
            equity_share=self.equity_share,
            lifetime=self.lifetime.number_of_years,
            cost_of_debt=self.cost_of_debt,
            lifetime_remaining=self.lifetime.remaining_number_of_years,
        )

    @property
    def debt_repayment_for_current_year(self) -> float:
        from .calculate_costs import calculate_current_debt_repayment

        """Returns the debt repayment amount for the current year."""
        if self.cost_of_debt is None:
            # FIXME how do we even end up here?
            self.cost_of_debt = 0.05
        return calculate_current_debt_repayment(
            total_investment=self.total_investment,
            lifetime_expired=self.lifetime.expired,
            lifetime_years=self.lifetime.number_of_years,
            years_elapsed=self.lifetime.elapsed_number_of_years,
            cost_of_debt=self.cost_of_debt,
            equity_share=self.equity_share,
        )

    @property
    def production(self) -> float:
        return self.utilization_rate * self.capacity

    @property
    def unit_production_cost(self) -> float:
        from .calculate_costs import calculate_unit_production_cost

        """Maybe divide by production to normalize to unit?"""
        return calculate_unit_production_cost(
            opex=self.opex, current_debt_repayment=self.debt_repayment_for_current_year, production=self.production
        )

    @property
    def is_underutilized(self) -> bool:
        return self.utilization_rate < self.production_threshold.low

    def optimal_technology_name(self, price) -> tuple[str, float]:  # TODO: @Marcus update implimentation
        from .calculate_costs import derive_best_technology_switch, stranding_asset_cost

        cosa = stranding_asset_cost(
            self.debt_repayment_per_year,
            [self.opex] * len(self.debt_repayment_per_year),
            self.lifetime.remaining_number_of_years,
            price,
            self.production,
            self.cost_of_debt,
        )

        # optimal_tech_name, _ = max(self.technology_switch_npv.items(), key=lambda item: item[1]
        npv, optimal_tech_name = derive_best_technology_switch(
            current_technology=self.technology.name,
            cost_of_debt=self.cost_of_debt,
            equity_share=self.equity_share,
            lifetime=gv.LIFETIME["steel"],
            expected_utilisation_rate=0.7,
            capacity=1000,
            price=price,
            mvp=True,
            cosa=cosa,
        )

        return optimal_tech_name, npv

    # def no_profitable_technology(self, price) -> bool:  # TODO @Marcus update this implimentatio
    #     """
    #     Assesses if there is no profitable technology to switch to
    #     """
    #     from .calculate_costs import derive_best_technology_switch

    #     derive_best_technology_switch(
    #         current_technology=self.technology.name,
    #         cost_of_debt=self.cost_of_debt,
    #         equity_share=self.equity_share,
    #         lifetime=gv.LIFETIME["steel"],
    #         expected_utilisation_rate=0.7,
    #         capacity=1000,
    #         price=price,
    #         mvp=True,
    #         cosa=cosa,
    #     )

    #     optimal_npv, optimal_tech = max(self.technology_switch_npv.items(), key=lambda item: item[1])
    #     threshold = 100
    #     return optimal_npv < threshold


class Plant:
    def __init__(
        self,
        *,
        plant_id: str,
        location: Location,
        furnace_groups: list[FurnaceGroup],
        power_source: str,
        soe_status: str,
        parent_gem_id: str,
        workforce_size: int,
        certified: bool,
        category_steel_product: set[ProductCategory],
    ) -> None:
        # ID:
        self.plant_id = plant_id

        # Location
        self.location = location

        # Plant operations
        self.furnace_groups = furnace_groups
        self.power_source = power_source

        # Company management info
        self.soe_status = soe_status  # State-owned plants expected to make different decisions than private companies (e.g., no country shift)
        self.parent_gem_id = parent_gem_id
        self.workforce_size = workforce_size  # Keep for OPEX calc and impacts

        # Product quality
        self.certified = certified  # Merge 'ISO 14001', 'ISO 50001', and 'ResponsibleSteel Certification' into one single col, True (one enough) / False
        self.category_steel_product = (
            category_steel_product  # Discuss with Hannah if demand is dependent on steel quality
        )

        # collect domain events
        self.events: list[events.Event] = []
        self.added_capacity = Volumes(0)
        self.removed_capacity = Volumes(0)

    def add_furnace_group(self, new_furnace_group: FurnaceGroup) -> None:
        self.furnace_groups.append(new_furnace_group)

    def get_consumption_values(self) -> None:
        """
        This will fetch the consumption values per production unit for the given tech stack
        We assume that the tech stack lives somewhere accessible to the plant agent.
        """

    def has_DRI_furnace(self) -> bool:
        """
        Check if the plant has a DRI furnace
        """
        for furnace_group in self.furnace_groups:
            if furnace_group.technology.name == "DRI":
                return True
        return False

    def set_technology_lcops(self, technology_lops: dict[str, float]) -> None:
        """
        sets levelised cost of production to the technologies in the plant
        """
        has_DRI = self.has_DRI_furnace()
        for furnace_group in self.furnace_groups:
            if furnace_group.technology.name == "EAF":
                if has_DRI:
                    furnace_group.technology.lcop = technology_lops["DRI-EAF"]
                else:
                    furnace_group.technology.lcop = technology_lops["EAF"]
            elif furnace_group.technology.name == "BOF":
                furnace_group.technology.lcop = technology_lops["Avg BF-BOF"]
            furnace_group.technology.lcop

    def calculate_average_steel_cost_and_capacity(self):
        """
        Calculates average steel cost and capacity for the plant for active steel furnaces
        """
        total_cost = 0
        total_capacity = 0
        for furnace_group in self.furnace_groups:
            if (
                furnace_group.status in ACTIVE_STATUSES
                and furnace_group.technology.product == "Steel"
                and furnace_group.technology.lcop is not None
            ):
                total_cost += furnace_group.technology.lcop * furnace_group.capacity
                total_capacity += furnace_group.capacity
        if total_capacity == 0:
            return
        self.average_steel_cost = total_cost / total_capacity
        self.steel_capacity = total_capacity

    def distance_to(self, location: Location) -> float:
        if self.location.distance_to_other_iso3 is not None and location.iso3 is not None:
            return self.location.distance_to_other_iso3[location.iso3]
        else:
            return geodesic((self.location.lat, self.location.lon), (location.lat, location.lon)).kilometers

    def __eq__(self, other) -> bool:
        return self.plant_id == other.plant_id

    def __hash__(self):
        return hash(self.plant_id)

    def __repr__(self) -> str:
        return f"Plant: <{self.plant_id}>"

    def get_furnace_group(self, furnace_group_id: str) -> FurnaceGroup:
        try:
            return next(fg for fg in self.furnace_groups if fg.furnace_group_id == furnace_group_id)
        except StopIteration:
            raise ValueError(f"Furnace group {furnace_group_id} not found in plant {self.plant_id}")

    def reset_capacity_changes(self):
        self.added_capacity = Volumes(0)
        self.removed_capacity = Volumes(0)

    def close_furnace_group(self, furnace_group_id: str) -> None:
        """
        Close a furnace group by mothballing it.

        Retrieves the furnace group with id==furnace_group_id, adds its capacity to the removed capacity,
        sets its capacity to zero, updates its status to "Mothballed", and logs a FurnaceGroupClosed event.
        """
        furnace_group = self.get_furnace_group(furnace_group_id)
        self.removed_capacity = Volumes(self.removed_capacity + furnace_group.capacity)
        furnace_group.capacity = Volumes(0)
        furnace_group.status = "Mothballed"
        self.events.append(events.FurnaceGroupClosed(furnace_group_id=furnace_group_id))

    def renovate_furnace_group(self, furnace_group_id: str) -> None:
        """
        Renovate a furnace group.

        Resets furnace group lifetime to a new 20-year period, changes technology CAPEX type to "brownfield", and sets last_renovation date.
        An event is logged to indicate that the furnace group has been renovated.
        """
        furnace_group = self.get_furnace_group(furnace_group_id)
        current_year = furnace_group.lifetime.current
        furnace_group.last_renovation_date = date(current_year, 1, 1)
        furnace_group.lifetime = PointInTime(
            current=current_year,
            time_frame=TimeFrame(start=current_year, end=Year(current_year + gv.LIFETIME["steel"])),
        )
        furnace_group.technology.capex_type = "brownfield"
        self.events.append(events.FurnaceGroupRenovated(furnace_group_id=furnace_group_id))

    def change_furnace_group_technology(self, furnace_group_id: str, technology_name: str) -> None:
        """
        Change the technology of a specified furnace group.

        Updates the technology of the furnace group with id==`furnace_group_id` to a new technology
        specified by `technology_name`. The method retrieves the corresponding bill of materials, updates
        the product and capex type, resets the furnace group's lifetime to a new 20-year period based on
        the current year, and appends a technology change event.

        TODO:
            - Ensure that the cost of debt is inherited based on location.
            Marcus? if we only change the technology, we should not change the cost of debt?
        """
        from .calculate_costs import BillsOfMaterial

        furnace_group = self.get_furnace_group(furnace_group_id)
        technology = Technology(
            name=technology_name,
            bill_of_materials=getattr(BillsOfMaterial, technology_name.replace("-", "_")),
            product=furnace_group.technology.product,
            capex_type="greenfield",
        )

        furnace_group.technology = technology
        current_year = furnace_group.lifetime.current
        furnace_group.lifetime = PointInTime(
            current=current_year,
            time_frame=TimeFrame(start=current_year, end=Year(current_year + gv.LIFETIME["steel"])),
        )
        self.events.append(events.FurnaceGroupTechChanged(furnace_group_id=furnace_group_id))

        # TODO: @Marcus - make sure that cost of debt is inherited based on location!

    def evaluate_furnace_group_strategy(self, furnace_group_id: str, price: float) -> commands.Command | None:
        """
        This function will evaluate the strategy for the given furnace group
        """
        furnace_group = self.get_furnace_group(furnace_group_id)
        if furnace_group.is_underutilized:  # or furnace_group.no_profitable_technology:
            return commands.CloseFurnaceGroup(plant_id=self.plant_id, furnace_group_id=furnace_group.furnace_group_id)

        optimal_tech_name, tech_npv = furnace_group.optimal_technology_name(price)
        if tech_npv < 0:
            logger.debug(
                f"Optimal tech is {optimal_tech_name} with npv of {tech_npv}, but also capacity of {furnace_group.capacity}"
            )
            return None
        technology_already_optimal = furnace_group.technology.name == optimal_tech_name

        # Check whether the asset should be renovated
        if furnace_group.lifetime.expired and technology_already_optimal:
            return commands.RenovateFurnaceGroup(
                plant_id=self.plant_id, furnace_group_id=furnace_group.furnace_group_id
            )
        # Check whether the asset should switch to a more profitable technology
        technology_not_optimal = not technology_already_optimal
        if technology_not_optimal:
            return commands.ChangeFurnaceGroupTechnology(
                plant_id=self.plant_id,
                furnace_group_id=furnace_group.furnace_group_id,
                technology_name=optimal_tech_name,
            )

        # If none of the above conditions are met, continue operations without changing strategy
        return None

    def generate_new_furnace(
        self,
        technology_name: str,
        product: str,
        current_year: int,
        cost_of_debt: float = 0.02,
        expected_util_rate: float = 0.07,
        capacity: int = 1000,
    ) -> FurnaceGroup:
        """
        Generate a new furnace group for the specified technology.

        This is a placeholder implementation that creates a FurnaceGroup object using the given
        technology name and current year. The technology's bill of materials is retrieved from
        the BillsOfMaterial container. The furnace group is initialized with default values for
        capacity, status, utilization, and lifetime.

        Parameters:
            technology_name (str): The name of the technology.
            current_year (int): The current year used to set the furnace group's timeline.

        Returns:
            FurnaceGroup: The newly created furnace group.
        """
        from .calculate_costs import BillsOfMaterial

        technology = Technology(
            name=technology_name,
            bill_of_materials=getattr(BillsOfMaterial, technology_name.replace("-", "_")),
            product=product,
        )

        new_furnace_id = self.get_new_furnance_id_number()
        active_year = current_year + 3  # TODO: update with years to add given technology being built

        furnace_group = FurnaceGroup(
            furnace_group_id=new_furnace_id,
            capacity=Volumes(capacity),
            status="announced",
            last_renovation_date=date(current_year, 1, 1),
            technology=technology,
            historical_production={},
            utilization_rate=expected_util_rate,
            cost_of_debt=cost_of_debt,
            lifetime=PointInTime(
                current=Year(current_year),
                time_frame=TimeFrame(start=Year(active_year), end=Year(active_year + gv.LIFETIME["steel"])),
            ),
        )
        furnace_group.created_by_PAM = True

        return furnace_group

    def evaluate_expansion(self, environment, new_furnace: FurnaceGroup) -> commands.Command | None:
        """
        Evaluate whether a new furnace group should be added to the plant.

        Compares the predicted market price with 150% of the new furnace group's unit production cost.
        If the predicted price exceeds this threshold, returns an AddFurnaceGroup command; otherwise, returns None.

        Parameters:
            environment: An object that provides market information and demand, including a method
                        to predict new market prices.
            new_furnace (FurnaceGroup): The furnace group under evaluation for expansion.

        Returns:
            commands.Command | None: The command to add the furnace group if expansion is justified, otherwise None.
        """
        predicted_price = environment._predict_new_market_price(
            demand=environment.current_demand,
            new_furnace_group=new_furnace,
        )

        if predicted_price > new_furnace.unit_production_cost * 1.5:  # 50% margin TODO: improve expansion logic
            return commands.AddFurnaceGroup(
                plant_id=self.plant_id, furnace_group_id=new_furnace.furnace_group_id, new_furnace=new_furnace
            )
        return None

    def furnace_group_added(self, furnace_group_id: str, plant_id: str) -> None:
        self.events.append(events.FurnaceGroupAdded(furnace_group_id=furnace_group_id, plant_id=plant_id))

    def report_cost_breakdown(self):
        """
        Generate a cost breakdown report for each technology.

        Iterates over furnace groups, calculates cost components (debt, interest, O&M, production),
        and merges the bill of materials for each technology. Returns a dictionary mapping technology
        names to their cost breakdown details.

        Returns:
            dict: A dictionary with cost breakdown for each technology.
        """
        from .calculate_costs import calculate_debt_report

        cost_breakdown_by_tech = defaultdict(lambda: defaultdict(float))
        bom_breakdown_by_tech = defaultdict(lambda: defaultdict(float))
        final_breakdown = {}

        # Iterate over each furnace group to update the cost breakdown
        for fg in self.furnace_groups:
            if fg.capacity == 0:
                continue
            tech = fg.technology.name
            # Calculate cost components
            principal_debt, interest = calculate_debt_report(
                total_investment=fg.total_investment,
                lifetime_expired=fg.lifetime.expired,
                equity_share=fg.equity_share,
                lifetime_years=fg.lifetime.number_of_years,
                years_elapsed=fg.lifetime.elapsed_number_of_years,
                cost_of_debt=fg.cost_of_debt,
            )
            cost_breakdown_by_tech[tech]["Principal_debt"] += principal_debt
            cost_breakdown_by_tech[tech]["Interest"] += interest
            cost_breakdown_by_tech[tech]["O&M"] += fg.fixed_opex * fg.production
            cost_breakdown_by_tech[tech]["Production"] += fg.production

            # Merge Bill of Materials for this technology
            bill_of_materials = fg.report_bill_of_materials()  # This should be a dict
            if bill_of_materials:
                merge_two_dictionaries(bom_breakdown_by_tech[tech], bill_of_materials)

            # Integrate each technology's merged Bill of Materials into its cost breakdown
            for tech, cost_data in cost_breakdown_by_tech.items():
                cost_data["Bill of Materials"] = dict(bom_breakdown_by_tech[tech])
                final_breakdown[tech] = dict(cost_data)

        return final_breakdown

    def aggregate_emissions(self):
        """
        Report the total emissions for the plant.
        """
        emissions = 0
        for fg in self.furnace_groups:
            emissions += fg.emissions
        return emissions

    def get_new_furnance_id_number(self) -> str:
        """
        Get a furnace group id for a potential new furnace group.
        Adds 1 to the number of the last furnace group id belonging to the plant.
        """
        try:
            newest_furnace = self.furnace_groups[-1].furnace_group_id
        except IndexError:
            # No furnace groups exist yet, so we create a new one
            return f"{self.plant_id}_1"

        # This is completely nuts - FIXME please!
        # Handle different ID formats (fg_group_N or plant_id_N)
        parts = newest_furnace.split("_")
        if len(parts) >= 2 and parts[0] == "fg":
            # Format: fg_group_N
            try:
                if parts[1] == "group":
                    new_number = int(parts[2]) + 1
                    return f"fg_group_{new_number}"
                else:
                    # Try to get the number from the last part
                    new_number = int(parts[-1]) + 1
                    return f"{parts[0]}_{parts[1]}_{new_number}"
            except (IndexError, ValueError):
                # Fallback if we can't parse the ID format
                return f"fg_group_{len(self.furnace_groups) + 1}"
        else:
            # Format: plant_id_N
            try:
                new_number = int(parts[-1]) + 1
                return f"{self.plant_id}_{new_number}"
            except (IndexError, ValueError):
                # Fallback if we can't parse the ID format
                return f"{self.plant_id}_{len(self.furnace_groups) + 1}"


class PlantGroup:
    def __init__(self, *, plant_group_id: str, plants: list[Plant]) -> None:
        self.plant_group_id = plant_group_id
        self.plants = plants

    # TODO: What else goes in here?
    # Maybe this is in reality where the consideration of adding a furnace comes into play.
    # According to Artem it will be the parent group that assess the need an opportunity for a new furnace.


class DemandCenter:
    def __init__(self, demand_center_id: str, center_of_gravity: Location, demand_by_year: dict[Year, Volumes]) -> None:
        self.demand_center_id = demand_center_id
        self.center_of_gravity = center_of_gravity
        self.demand_by_year = demand_by_year

    def __repr__(self) -> str:
        return f"DemandCenter: <{self.demand_center_id}>"

    def __hash__(self):
        return hash(self.demand_center_id)

    def __eq__(self, other) -> bool:
        return self.demand_center_id == other.demand_center_id


class SteelAllocations:
    def __init__(self, allocations: dict[tuple[Plant, FurnaceGroup, DemandCenter], Volumes]) -> None:
        self.allocations = allocations

    def __repr__(self) -> str:
        return f"{len(self.allocations)} SteelAllocations"

    def get_total(self) -> Volumes:
        return sum(self.allocations.values(), Volumes(0))


class Environment:
    """
    Class to track system environment, e.g. the collective macro-scale of the system
    such as total capacity of technologies to produce commodity X, cost curve of steel and
    iron per unit of production, prediction of market prices, emissions, capex, and optimal plant technology
    contains yearly demand dicts and the iteration year
    """

    def __init__(self, cost_of_x_csv: Path = Auto):
        """
        Initialise the environment with the capex values and switching capex
        (i.e. the capex needed switching from tech A --> B)
        """
        from .Capex import FULL_GREENFIELD_CAPEX, TECH_SWITCH_CAPEX

        self.year = Year(SIMULATION_START_YEAR)

        self.name_to_capex = {
            "greenfield": FULL_GREENFIELD_CAPEX.copy(),
            "brownfield": {k: v / 2 for k, v in FULL_GREENFIELD_CAPEX.items()},
        }
        # Initialize these as defaultdict instead of None
        self.steel_init_capacity: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.iron_init_capacity: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.technology_switch_capex = TECH_SWITCH_CAPEX.copy()

        self.cost_of_capital = self.initiate_industrial_asset_cost_of_capital(cost_of_x_csv=cost_of_x_csv)

    def initiate_industrial_asset_cost_of_capital(self, cost_of_x_csv: Path = Auto) -> dict[str, float]:
        """
        Load the cost of capital for industrial assets from cost_of_x file
        Returns: a dictionary with the cost of capital for each country
        """
        if not cost_of_x_csv:
            from ..config import settings

            cost_of_x_csv = settings.cost_of_x_csv

        with open(cost_of_x_csv, "r") as file:
            data = json.load(file)
        return dict(zip(data["Country code"].values(), data["Cost of equity - industrial assets"].values()))

    def _generate_cost_dict(self, world_furnace_groups: list[FurnaceGroup]) -> dict[str, dict[str, float]]:
        """
        Generate a dict representation of the costs for all furnace_groups
        """
        assets = {}
        for fg in world_furnace_groups:
            if fg.status.lower() not in ACTIVE_STATUSES or fg.capacity == 0:
                continue
            unit_cost = fg.unit_production_cost

            # Use furnace group ID as key
            assets[fg.furnace_group_id] = {"capacity": fg.capacity, "unit_cost_of_production": unit_cost}

        # Sort by unit cost of production
        self.cost_dict = assets
        return assets

    def generate_cost_curve(self, world_furnace_groups: list[FurnaceGroup]) -> list[dict]:
        """
        Generate a cost curve based on the unit cost of production for furnace groups.

        1) Generates and sorts the internal cost dictionary by the unit cost of production,
        2) Computes a cumulative production capacity and associates it with the corresponding production cost.


        Returns:
            list[dict]: A list of dictionaries representing the cost curve. Each dictionary has keys:
                - "cumulative_capacity" (float): The cumulative production capacity.
                - "production_cost" (float): The unit cost of production at that cumulative capacity.

        TODO: Add separation of steel and iron price.
        """
        self._generate_cost_dict(world_furnace_groups)
        sorted_assets = dict(sorted(self.cost_dict.items(), key=lambda item: item[1]["unit_cost_of_production"]))

        # Sort by unit cost of production
        # Generate cost curve
        cumulative_production: float = 0
        curve = []
        for fg_id, values in sorted_assets.items():
            cap = values["capacity"]
            cost = values["unit_cost_of_production"]

            cumulative_production += cap

            curve.append({"cumulative_capacity": cumulative_production, "production_cost": cost})
        self.steel_cost_curve = curve
        return curve

    def update_cost_curve(self, world_furnace_groups: list[FurnaceGroup], product_type="steel") -> list[dict]:
        """
        Update the cost curve for a given product type.
        Filters the furnace groups by product type and generates the cost curve.

        Parameters:
            world_furnace_groups (list[FurnaceGroup]): List of furnace groups.
            product_type (str, optional): Product type to filter by (default "steel").

        """
        return self.generate_cost_curve(
            [fg for fg in world_furnace_groups if fg.technology.product.lower() == product_type]
        )

    def extract_price_from_costcurve(self, demand: float) -> float:
        """
        Return the production cost for the first cumulative capacity that meets or exceeds the demand.

        Raises:
            ValueError: If the cost curve is empty or if demand exceeds maximum cumulative production.
        """
        # Handle empty cost curve
        if not self.steel_cost_curve:
            raise ValueError("Cost curve is empty")

        # Get the last entry (highest capacity)
        last_entry = self.steel_cost_curve[-1]

        # If demand exceeds available capacity, raise an error
        if demand > last_entry["cumulative_capacity"]:
            raise ValueError(f"Demand of {demand} exceeds maximum cumulative production")

        # Normal case - find first entry that meets or exceeds demand
        for entry in self.steel_cost_curve:
            if entry["cumulative_capacity"] >= demand:
                return entry["production_cost"]

        raise ValueError("capacity should always be greater than demand")  # This should never happen

    def _predict_new_market_price(self, new_furnace_group: FurnaceGroup, demand: float) -> float:
        """
        Takes in a list of furnace groups and predicts the new market price based on the cost curve, but doesn't store it.
        Returns:  The production cost at or above the demand level.
        """
        extended_list_of_furnace_groups = self.cost_dict.copy()
        extended_list_of_furnace_groups[new_furnace_group.furnace_group_id] = {
            "capacity": new_furnace_group.capacity,
            "unit_cost_of_production": new_furnace_group.unit_production_cost,
        }
        sorted_assets = dict(
            sorted(extended_list_of_furnace_groups.items(), key=lambda item: item[1]["unit_cost_of_production"])
        )

        # Sort by unit cost of production

        # Generate cost curve
        cumulative_capacity: float = 0
        for fg_id, values in sorted_assets.items():
            cap = values["capacity"]
            cost = values["unit_cost_of_production"]

            cumulative_capacity += cap

            if cumulative_capacity >= demand:
                return cost
        raise ValueError(f"Demand of {demand} exceeds maximum cumulative capacity of {cumulative_capacity}")

    def new_furnace_npv(
        self,
        cost_of_debt=0.05,
        equity_share=0.2,
        lifetime=20,
        expected_utilisation_rate=0.7,
        mvp: bool = True,
        demand: int = Auto,
    ):
        """
        Derives the most benefitial technology and its NPV for a new furnace

        Uses the calculate_npv_full function to calculate the NPV for each technology, and returns the highest NPV and the associated technology.
        """
        from steelo.domain import calculate_costs as cc
        from steelo.domain.Capex import FULL_GREENFIELD_CAPEX as greenfield_capex

        if not demand or demand is None:  # Auto or None? - this is probably wrong FIXME - jochen
            demand = int(self.current_demand)

        NPV = {}
        if mvp:
            for tech, capex in greenfield_capex.items():
                if tech in ["BOF", "DRI-EAF", "EAF"]:
                    NPV[tech] = cc.calculate_npv_full(
                        technology=tech,
                        capex=capex,
                        cost_of_debt=cost_of_debt,
                        equity_share=equity_share,
                        lifetime=lifetime,
                        fixed_opex=capex * 0.1,
                        expected_utilisation_rate=expected_utilisation_rate,
                        capacity=Volumes(1000),
                        price=self.extract_price_from_costcurve(demand),
                    )

        else:  # for now this is how we hack the mvp
            for tech, capex in greenfield_capex.items():
                NPV[tech] = cc.calculate_npv_full(
                    technology=tech,
                    capex=capex,
                    cost_of_debt=cost_of_debt,
                    equity_share=equity_share,
                    lifetime=lifetime,
                    fixed_opex=capex * 0.1,
                    expected_utilisation_rate=expected_utilisation_rate,
                    capacity=Volumes(1000),
                    price=self.extract_price_from_costcurve(demand),
                )
        # Find technology with maximum NPV value
        best = max(NPV, key=lambda k: NPV[k] if NPV[k] is not None else float("-inf"))
        best_value = NPV[best]
        return best_value, best

    def update_regional_capacity(self, world_plants: list[Plant]) -> None:
        """
        Extracts the regional capacity of the world's furnace groups depending on technology.
        """

        self.regional_steel_capacity: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.regional_iron_capacity: defaultdict[str, defaultdict[str, int]] = defaultdict(lambda: defaultdict(int))

        for pa in world_plants:
            for fg in pa.furnace_groups:
                if fg.status.lower() not in ACTIVE_STATUSES:
                    continue

                target_capacity = (
                    self.regional_steel_capacity
                    if fg.technology.product == "Steel"
                    else self.regional_iron_capacity
                    if fg.technology.product == "Iron"
                    else None
                )

                if target_capacity is not None and pa.location.iso3 is not None:
                    target_capacity[pa.location.iso3][fg.technology.name] += fg.capacity

        if not self.steel_init_capacity:
            self.steel_init_capacity = self.regional_steel_capacity.copy()

        if not self.iron_init_capacity:
            self.iron_init_capacity = self.regional_iron_capacity.copy()

        # TODO: fix division by zero error and uncomment
        # # Update capex reduction ratios if regional capacities have changed.
        # if self.steel_C0 != self.regional_steel_capacity:
        #     self.update_steel_capex_reduction_ratio()
        # if self.iron_C0 != self.regional_iron_capacity:
        #     self.update_iron_capex_reduction_ratio()

    def update_steel_capex_reduction_ratio(self) -> None:
        """
        Will calculate the ratio to reduce the capex of iron technologies with
        """
        from .calculate_costs import calculate_capex_reduction_rate

        self.steel_capex_reduction_ratio: dict[str, dict[str, float]] = {}
        for region, capacity in self.regional_steel_capacity.items():
            self.steel_capex_reduction_ratio[region] = {}
            for tech, cap in capacity.items():
                self.steel_capex_reduction_ratio[region][tech] = calculate_capex_reduction_rate(
                    self.steel_init_capacity[region][tech], cap
                )

    def update_iron_capex_reduction_ratio(self) -> None:
        """
        Will calculate the ratio to reduce the capex of iron technologies with
        """
        from .calculate_costs import calculate_capex_reduction_rate

        self.iron_capex_reduction_ratio: dict[str, dict[str, float]] = {}
        for region, capacity in self.regional_iron_capacity.items():
            self.iron_capex_reduction_ratio[region] = {}

            for tech, cap in capacity.items():
                self.iron_capex_reduction_ratio[region][tech] = calculate_capex_reduction_rate(
                    capacity_current=cap, capacity_zero=self.iron_init_capacity[region][tech]
                )
        return None

    def initiate_demand_dicts(self, world_demand_centres: list[DemandCenter]) -> None:
        """
        Initiates the demand dictionary in the environment

        This allows us to have a proxy for the demand centres, as values, but not locations, change in time
        """
        self.demand_dict: dict[str, dict[Year, Volumes]] = defaultdict(lambda: defaultdict(lambda: Volumes(0)))
        for dc in world_demand_centres:
            self.demand_dict[dc.demand_center_id] = dc.demand_by_year

    def calculate_demand(self) -> None:
        """
        Calaculates the total demand for the current year
        """
        self.current_demand = sum(entry.get(self.year, 0) for entry in self.demand_dict.values())
