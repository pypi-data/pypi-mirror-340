from .models import Plant, Environment
from steelo.utilities.global_variables import ACTIVE_STATUSES


class DataCollector:
    def __init__(self, world_plants: list[Plant], env: Environment, custom_function=None) -> None:
        self.plants = world_plants
        self.env = env
        self.cost_breakdown: dict[str, dict] = {}
        self.trace_capacity: dict[int, dict[str, float]] = {}
        self.trace_price: dict[int, float] = {}
        # self.trace_cost_curve = {}
        self.trace_production: dict[int, float] = {}
        self.step = 0
        self.emissions: dict[int, float] = {}
        self.trace_utilisation_rate: dict[int, dict[str, float]] = {}
        self.capacity_by_technology_and_PAM_status: dict[int, dict[str, dict[bool, float]]] = {}
        self.capacity_deltas: dict[int, dict[str, float]] = {}

        if custom_function is not None:
            pass

    def collect_cost_breakdrown(self):
        """
        This function will return a cost breakdown of the plant, in terms of principal debt, interest, bill of materials, o&m and other opex
        """
        breakdown = {}
        for plant in self.plants:
            breakdown[plant.plant_id] = plant.report_cost_breakdown()
        return breakdown

    def collect_capacity(self):
        """
        This collect the capacity stored in the system environment
        """
        self.env.update_regional_capacity(self.plants)
        return {"Iron": self.env.regional_iron_capacity, "Steel": self.env.regional_steel_capacity}

    def collect_market_iron_steel_price(self, demand: int = 300):
        """
        This function will return the market price of iron and steel
        """
        return {
            "Iron": self.env.extract_price_from_costcurve(demand),
            "Steel": self.env.extract_price_from_costcurve(demand),
        }

    # def collect_params4steel_cost_curve(self):
    #     """
    #     This function will return the steel cost curve and the current demand.
    #     """
    #     return {
    #         "steel_cost_curve": self.env.steel_cost_curve,
    #         "current_demand": self.env.current_demand,
    #         "plants": self.plants,
    #     }

    def collect_emissions_by_plants(self):
        """
        This function will collect the emissions by plants
        """
        emissions = {}
        for plant in self.plants:
            emissions[plant.plant_id] = plant.aggregate_emissions()
        return emissions

    def collect_utilisation_rates(self):
        """collecting furnace_group utilisisation_rates"""
        return {
            fg.furnace_group_id: fg.utilization_rate
            for plant in self.plants
            for fg in plant.furnace_groups
            if fg.status.lower() in ACTIVE_STATUSES
        }

    def collect_capacity_deltas(self):
        delta_added = [plant.added_capacity for plant in self.plants]
        delta_removed = [plant.removed_capacity for plant in self.plants]
        return {"added": sum(delta_added), "removed": sum(delta_removed)}

    def collect_global_steel_production(self):
        """
        This function will collect the production by each operating steel furnace group and return the global total.
        """
        total_production = {}
        for tech in [
            "EAF",
            "BOF",
        ]:  # TODO: Replace with a reference to _allowed_technologies in the technology class post MVP
            total_production[tech] = 0
            for plant in self.plants:
                for fg in plant.furnace_groups:
                    if (
                        (fg.status.lower() in ACTIVE_STATUSES)
                        and (fg.technology.product.lower() == "steel")
                        and (fg.technology.name == tech)
                    ):
                        total_production[tech] += fg.production
        return total_production

    def collect_capacity_by_technology_and_PAM_status(self):
        """
        This function will collect the capacity by technology and PAM status
        """
        capacity = {}
        for tech in [
            "EAF",
            "BOF",
        ]:
            cap_tech_pre_existing = [
                fg.capacity
                for plant in self.plants
                for fg in plant.furnace_groups
                if fg.technology.name == tech and fg.status.lower() in ACTIVE_STATUSES and not fg.created_by_PAM
            ]
            cap_tech_created = [
                fg.capacity
                for plant in self.plants
                for fg in plant.furnace_groups
                if fg.technology.name == tech and fg.status.lower() in ACTIVE_STATUSES and fg.created_by_PAM
            ]
            capacity[tech] = {"pre_existing": sum(cap_tech_pre_existing), "created": sum(cap_tech_created)}
        return capacity

    def production_trade(self):
        pass

    def collect(self):
        self.cost_breakdown[self.step] = self.collect_cost_breakdrown()
        self.trace_capacity[self.step] = self.collect_capacity()
        self.trace_price[self.step] = self.collect_market_iron_steel_price(self.env.current_demand)
        # self.trace_cost_curve[self.step] = self.collect_params4steel_cost_curve()
        self.trace_production[self.step] = self.collect_global_steel_production()
        self.trace_utilisation_rate[self.step] = self.collect_utilisation_rates()
        self.capacity_by_technology_and_PAM_status[self.step] = self.collect_capacity_by_technology_and_PAM_status()
        self.capacity_deltas[self.step] = self.collect_capacity_deltas()
        self.production_trade()
        # self.emissions[self.step] = self.collect_emissions_by_plants().copy() # TODO: fix error and uncomment

        self.step += 1
