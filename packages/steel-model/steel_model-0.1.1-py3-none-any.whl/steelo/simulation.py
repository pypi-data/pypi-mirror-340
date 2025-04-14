from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import json
import os

from .service_layer.message_bus import MessageBus
from .service_layer.unit_of_work import UnitOfWork
from .economic_models import EconomicModel, PlantAgentsModel, AllocationModel
from .domain.models import Environment
from .domain.events import IterationOver
from .domain.datacollector import DataCollector
from .domain.calculate_costs import BillsOfMaterial
from .bootstrap import bootstrap
from .config import settings
from .adapters.repositories.in_memory_repository import import_plants_from_json
from .adapters.dataprocessing.preprocessing.raw_plant_data_processing import read_technology_lcop_data
from .adapters.dataprocessing.excel_reader import read_demand_centers_into_repository
from .utilities.global_variables import ACTIVE_STATUSES


class Simulation:
    """
    A class to run a simulation using an economic model. The simulation
    uses a MessageBus to handle events and commands and uses the strategy
    pattern to run the economic model.
    """

    def __init__(self, *, bus: MessageBus, economic_model: EconomicModel) -> None:
        self.bus = bus
        self.economic_model = economic_model

    def run_simulation(self) -> None:
        self.economic_model.run(self.bus)


@dataclass
class SimulationConfig:
    """Configuration for running a complete simulation."""

    plants_json_path: Path = settings.sample_plants_json_path
    technology_lcop_csv: Path = settings.technology_lcop_csv
    gravity_distances_csv: Path = settings.gravity_distances_csv
    start_year: int = 2025
    end_year: int = 2027
    output_file: Path = settings.intermediate_outputs_simulation_run
    demand_center_xlsx: Path = settings.demand_center_xlsx
    demand_sheet_name: str = "Steel_Demand_Chris Bataille"
    location_csv: Path = settings.location_csv
    log_level: int = logging.WARNING
    cost_of_x_csv: Path = settings.cost_of_x_csv

    def __repr__(self):
        return json.dumps(self.__dict__, indent=4, default=str)


class SimulationRunner:
    """
    A class that orchestrates the full simulation process.
    This can be used from both CLI and Django interfaces.
    """

    def __init__(self, config: SimulationConfig, do_setup: bool = True):
        self.config = config
        logging.getLogger().setLevel(config.log_level)

        # Results that will be populated after setup
        self.data_collector: Optional[DataCollector] = None
        self.bus: Optional[MessageBus] = None

        # Run setup during initialization to populate required attributes
        if do_setup:
            # FIXME: this should be handled in a better way
            self.setup()

    def setup(self):
        """Set up all necessary components for the simulation."""
        # Load plant data from JSON
        repository_json = import_plants_from_json(json_path=self.config.plants_json_path)
        technology_lcops = read_technology_lcop_data(self.config.technology_lcop_csv)

        # Set technology LCOP data for each plant
        for plant in repository_json.plants.list():
            plant.set_technology_lcops(technology_lcops)
            plant.calculate_average_steel_cost_and_capacity()

        # Read demand centers
        repository = read_demand_centers_into_repository(
            demand_excel_path=self.config.demand_center_xlsx,
            demand_sheet_name=self.config.demand_sheet_name,
            location_csv=self.config.location_csv,
            repository=repository_json,
            gravity_distances_csv=self.config.gravity_distances_csv,
        )

        # Set bill of materials for each furnace group
        for plant in repository_json.plants.list():
            for fg in plant.furnace_groups:
                fg.technology.bill_of_materials = getattr(BillsOfMaterial, fg.technology.name.replace("-", "_"))

        # Create environment and message bus
        env = Environment(cost_of_x_csv=self.config.cost_of_x_csv)
        uow = UnitOfWork(repository=repository)
        bus = bootstrap(uow=uow, env=env)

        # Initialize environment
        steel_furnaces = [
            fg
            for plant in bus.uow.plants.list()
            for fg in plant.furnace_groups
            if fg.technology.product in ["steel", "Steel"]
        ]
        bus.env.initiate_demand_dicts(repository.demand_centers.list())
        bus.env.calculate_demand()
        bus.env.generate_cost_curve(steel_furnaces)
        bus.env.update_regional_capacity(bus.uow.plants.list())

        # Create data collector
        data_collector = DataCollector(world_plants=bus.uow.plants.list(), env=bus.env)

        self.bus = bus
        self.data_collector = data_collector

    def print_capacity_stats(self):
        """Print statistics about plant capacities."""
        if not self.bus:
            raise RuntimeError("Bus is not initialized. Run setup() first.")

        capacities_operated = 0
        capacities_non_operated = 0

        for plant in self.bus.uow.plants.list():
            for fg in plant.furnace_groups:
                if fg.status.lower() in ACTIVE_STATUSES and fg.technology.product in ["steel", "Steel"]:
                    capacities_operated += fg.capacity
                elif fg.technology.product in ["steel", "Steel"]:
                    capacities_non_operated += fg.capacity

        print("Total Capacity of Operating Furnaces: ", capacities_operated)
        print("Total Capacity of Non-Operating Furnaces: ", capacities_non_operated)
        print("Steel Price:", self.bus.env.extract_price_from_costcurve(demand=self.bus.env.current_demand))

    def run(self) -> Dict[str, Any]:
        """Run the full simulation process and return results."""
        if not self.bus or not self.data_collector:
            raise RuntimeError("Bus or DataCollector is not initialized. Run setup() first.")

        # Initial statistics
        self.print_capacity_stats()

        # Run simulation for each year in the range
        for year in range(self.config.start_year, self.config.end_year):
            self.bus.env.calculate_demand()
            print("Demand: ", self.bus.env.current_demand)

            # Run the allocation and plant agent models
            Simulation(bus=self.bus, economic_model=AllocationModel()).run_simulation()
            Simulation(bus=self.bus, economic_model=PlantAgentsModel()).run_simulation()

            print("Year: ", year)

            # Collect data for this time step
            self.data_collector.collect()

            # Print statistics for this year
            self.print_capacity_stats()

            # Advance time step
            if (event := IterationOver) is not None:
                print("Event received: ", event)
                self.bus.handle(event(time_step_increment=1))

        # Prepare results dictionary
        results = {
            "price": self.data_collector.trace_price,
            "cost": self.data_collector.cost_breakdown,
            "capacity": self.data_collector.trace_capacity,
            "production": self.data_collector.trace_production,
        }

        # Save results to file if output_file is specified
        if self.config.output_file:
            output_file = self.config.output_file
            if os.path.exists(output_file):
                os.remove(output_file)
            with open(output_file, "w") as f:
                json.dump(results, f, indent=4)

        return results
