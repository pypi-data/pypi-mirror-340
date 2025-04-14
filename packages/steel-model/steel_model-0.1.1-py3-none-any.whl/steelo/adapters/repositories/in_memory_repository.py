from pathlib import Path
from typing import Iterable
import json
from datetime import date
from steelo.domain.models import TimeFrame

from .interface import PlantRepository, FurnaceGroupRepository, DemandCenterRepository
from ...domain import Plant, Volumes, Year, Location, Technology, FurnaceGroup, PointInTime, DemandCenter


class PlantInMemoryRepository:
    def __init__(self) -> None:
        self.data: dict[str, Plant] = {}
        self.furnace_id_to_plant_id: dict[str, str] = {}
        self.seen: set[Plant] = set()

    def add(self, plant: Plant) -> None:
        self.data[plant.plant_id] = plant
        for furnace_group in plant.furnace_groups:
            self.furnace_id_to_plant_id[furnace_group.furnace_group_id] = plant.plant_id
        self.seen.add(plant)

    def add_list(self, plants: Iterable[Plant]) -> None:
        for plant in plants:
            self.add(plant)

    def get(self, plant_id) -> Plant:
        return self.data[plant_id]

    def list(self) -> list[Plant]:
        return list(self.data.values())

    def get_by_furnace_group_id(self, furnace_group_id: str) -> Plant:
        plant_id = self.furnace_id_to_plant_id[furnace_group_id]
        return self.data[plant_id]


class FurnaceGroupInMemoryRepository:
    def __init__(self) -> None:
        self.data: dict[str, FurnaceGroup] = {}

    def add(self, furnace_group: FurnaceGroup) -> None:
        self.data[furnace_group.furnace_group_id] = furnace_group

    def add_list(self, furnace_groups: Iterable[FurnaceGroup]) -> None:
        for furnace_group in furnace_groups:
            self.add(furnace_group)

    def get(self, furnace_group_id) -> FurnaceGroup:
        return self.data[furnace_group_id]

    def list(self) -> list[FurnaceGroup]:
        return list(self.data.values())


class DemandCenterInMemoryRepository:
    def __init__(self) -> None:
        self.data: dict[str, DemandCenter] = {}

    def add(self, demand_center: DemandCenter) -> None:
        self.data[demand_center.demand_center_id] = demand_center

    def add_list(self, demand_centers: Iterable[DemandCenter]) -> None:
        for demand_center in demand_centers:
            self.add(demand_center)

    def get(self, demand_center_id) -> DemandCenter:
        return self.data[demand_center_id]

    def list(self) -> list[DemandCenter]:
        return list(self.data.values())


class InMemoryRepository:
    plants: PlantRepository
    furnace_groups: FurnaceGroupRepository
    demand_centers: DemandCenterRepository

    def __init__(self) -> None:
        self.plants = PlantInMemoryRepository()
        self.furnace_groups = FurnaceGroupInMemoryRepository()
        self.demand_centers = DemandCenterInMemoryRepository()


def import_plants_from_json(json_path: Path, mvp_filter_furnaces: bool = True) -> InMemoryRepository:
    """
    Import plants data from a JSON file and add it to an in-memory repository.
    """
    with json_path.open("r", encoding="utf-8") as f:
        plants_data = json.load(f)

    def convert_to_domain(plant_dict):
        # Convert the raw dictionary to a domain Plant object
        location = Location(**plant_dict["location"])
        furnace_groups = []
        for fg_dict in plant_dict["furnace_groups"]:
            technology = Technology(**fg_dict["technology"])
            time_frame = TimeFrame(**fg_dict["lifetime"]["time_frame"])
            lifetime = PointInTime(current=Year(fg_dict["lifetime"]["current"]), time_frame=time_frame)
            furnace_group = FurnaceGroup(
                furnace_group_id=fg_dict["furnace_group_id"],
                capacity=Volumes(fg_dict["capacity"]),
                status=fg_dict["status"],
                lifetime=lifetime,
                last_renovation_date=date.fromisoformat(fg_dict["last_renovation_date"]),
                technology=technology,
                historical_production={Year(k): Volumes(v) for k, v in fg_dict["historical_production"].items()},
                utilization_rate=fg_dict["utilization_rate"],
            )
            furnace_groups.append(furnace_group)
        return Plant(
            plant_id=plant_dict["plant_id"],
            location=location,
            furnace_groups=(
                [fg for fg in furnace_groups if fg.technology.name in ["EAF", "BOF"]]
                if mvp_filter_furnaces
                else furnace_groups
            ),
            power_source=plant_dict["power_source"],
            soe_status=plant_dict["soe_status"],
            parent_gem_id=plant_dict["parent_gem_id"],
            workforce_size=plant_dict["workforce_size"],
            certified=plant_dict["certified"],
            category_steel_product=set(plant_dict["category_steel_product"]),
        )

    plants = [convert_to_domain(plant_dict) for plant_dict in plants_data["root"]]

    print({fg.technology.name for plant in plants for fg in plant.furnace_groups})

    repository_in_memory = InMemoryRepository()

    repository_in_memory.plants.add_list(plants)
    return repository_in_memory
