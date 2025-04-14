from pathlib import Path
from datetime import date
from typing import Self, List, Iterable
from pydantic import BaseModel

from .interface import PlantRepository, FurnaceGroupRepository, DemandCenterRepository
from ...domain import Plant, Volumes, Year, Location, Technology, FurnaceGroup, PointInTime, TimeFrame, DemandCenter


class LocationInDb(BaseModel):
    iso3: str | None
    country: str
    region: str
    lat: float
    lon: float


class TechnologyInDb(BaseModel):
    name: str
    product: str
    technology_readiness_level: int | None
    process_emissions: float | None = None
    emissions_factor: float | None
    energy_consumption: float | None
    bill_of_materials: dict[str, dict[str, dict[str, float]]] | None = None


class TimeFrameInDb(BaseModel):
    start: int
    end: int


class PointInTimeInDb(BaseModel):
    current: int
    time_frame: TimeFrameInDb


class FurnaceGroupInDb(BaseModel):
    furnace_group_id: str
    capacity: Volumes
    status: str
    lifetime: PointInTimeInDb
    last_renovation_date: date
    technology: TechnologyInDb
    historical_production: dict[Year, Volumes]
    utilization_rate: float

    @property
    def to_domain(self) -> FurnaceGroup:
        return FurnaceGroup(
            furnace_group_id=self.furnace_group_id,
            capacity=self.capacity,
            status=self.status,
            lifetime=PointInTime(
                current=Year(self.lifetime.current),
                time_frame=TimeFrame(
                    start=Year(self.lifetime.time_frame.start), end=Year(self.lifetime.time_frame.end)
                ),
            ),
            last_renovation_date=self.last_renovation_date,
            technology=Technology(
                name=self.technology.name,
                product=self.technology.product,
                technology_readiness_level=self.technology.technology_readiness_level,
                process_emissions=self.technology.process_emissions,
                emissions_factor=self.technology.emissions_factor,
                energy_consumption=self.technology.energy_consumption,
                bill_of_materials={}
                if self.technology.bill_of_materials is None
                else self.technology.bill_of_materials,
            ),
            historical_production=self.historical_production,
            utilization_rate=self.utilization_rate,
        )

    @classmethod
    def from_domain(cls, furnace_group: FurnaceGroup) -> Self:
        technology_data = furnace_group.technology.__dict__.copy()
        if technology_data["bill_of_materials"] is not None:
            technology_data["bill_of_materials"] = dict(technology_data["bill_of_materials"])
        return cls(
            furnace_group_id=furnace_group.furnace_group_id,
            capacity=furnace_group.capacity,
            status=furnace_group.status,
            lifetime=PointInTimeInDb(
                current=furnace_group.lifetime.current,
                time_frame=TimeFrameInDb(
                    start=furnace_group.lifetime.start,
                    end=furnace_group.lifetime.end,
                ),
            ),
            last_renovation_date=furnace_group.last_renovation_date,
            technology=TechnologyInDb(**technology_data),
            historical_production=furnace_group.historical_production,
            utilization_rate=furnace_group.utilization_rate,
        )


class PlantInDb(BaseModel):
    plant_id: str
    location: LocationInDb
    furnace_groups: list[FurnaceGroupInDb]
    power_source: str
    soe_status: str
    parent_gem_id: str
    workforce_size: int
    certified: bool
    category_steel_product: set[str]

    def __lt__(self, other: Self) -> bool:
        """
        Make PlantInDb sortable by id. This is useful to keep the order of plants in the json file.
        Which is useful for diffing the file when the list of plants is updated.
        """
        return self.plant_id < other.plant_id

    @property
    def to_domain(self) -> Plant:
        location = Location(**self.location.model_dump())
        furnace_groups = []
        for fg in self.furnace_groups:
            fg_data = fg.model_dump()
            fg_data["technology"] = Technology(**fg_data["technology"])
            fg_data["lifetime"] = PointInTime(**fg.lifetime.model_dump())
            furnace_groups.append(FurnaceGroup(**fg_data))
        plant_data = self.model_dump()
        plant_data["location"] = location
        plant_data["furnace_groups"] = furnace_groups
        return Plant(**plant_data)

    @classmethod
    def from_domain(cls, plant: Plant) -> Self:
        plant_data = plant.__dict__
        plant_data["location"] = LocationInDb(**plant_data["location"].__dict__)
        furnace_groups_in_db = []
        for fg in plant_data["furnace_groups"]:
            fg_data = fg.__dict__
            technology_data = fg_data["technology"].__dict__.copy()
            if not technology_data["bill_of_materials"]:
                print(type(technology_data["bill_of_materials"]))
                technology_data["bill_of_materials"] = dict()
            fg_data["technology"] = TechnologyInDb(**technology_data)
            lifetime = fg_data["lifetime"]
            time_frame_in_db = TimeFrameInDb(start=lifetime.start, end=lifetime.end)
            fg_data["lifetime"] = PointInTimeInDb(current=lifetime.current, time_frame=time_frame_in_db)
            furnace_groups_in_db.append(FurnaceGroupInDb(**fg_data))
        plant_data["furnace_groups"] = furnace_groups_in_db
        return cls(**plant_data)


class PlantListInDb(BaseModel):
    """
    Used to make a list of plants serializable to json.
    """

    root: list[PlantInDb]


class PlantJsonRepository:
    """
    Repository for storing plants in a json file. Uses pydantic models for serialization / deserialization.
    All input and output is done using domain models. Domain models are converted to / from db models
    and then validated and dumped to json.
    """

    _all = None

    def __init__(self, path: Path) -> None:
        self.path = path
        self.seen: set[Plant] = set()

    def _fetch_all(self) -> dict[str, PlantInDb]:
        try:
            if not self.path.exists():
                return {}
            with self.path.open("r", encoding="utf-8") as f:
                plants_in_db = PlantListInDb.model_validate_json(f.read())
            return {plant.plant_id: plant for plant in plants_in_db.root}
        except FileNotFoundError:
            return {}

    @property
    def all(self) -> dict[str, PlantInDb]:
        """
        Cache fetching all models from file.
        """
        if self._all is None:
            self._all = self._fetch_all()
        return self._all

    def get(self, plant_id) -> Plant:
        return self.all[plant_id].to_domain

    def get_by_furnace_group_id(self, furnace_group_id: str) -> Plant:
        for plant_in_db in self.all.values():
            for fg in plant_in_db.furnace_groups:
                if fg.furnace_group_id == furnace_group_id:
                    return plant_in_db.to_domain
        raise KeyError(f"No plant with furnace group id {furnace_group_id}")

    def list(self) -> list[Plant]:
        return [plant_in_db.to_domain for plant_in_db in self.all.values()]

    def _write_models(self, locked: List[PlantInDb]) -> None:  # use List because of list method
        self.path.parent.mkdir(exist_ok=True)
        locked.sort()  # sort by id to keep the order of plants in the file for easier diffing
        plants_in_db = PlantListInDb(root=locked)
        with self.path.open("w", encoding="utf-8") as f:
            f.write(plants_in_db.model_dump_json(indent=2))

    def add(self, plant: Plant) -> None:
        """Add a single plant to the repository."""
        plant_in_db = PlantInDb.from_domain(plant)
        locked = self._fetch_all()
        locked[plant_in_db.plant_id] = plant_in_db
        self._write_models(list(locked.values()))
        self.seen.add(plant)

    def add_list(self, plants: Iterable[Plant]) -> None:
        """Add a list of plant to the repository."""
        plants_in_db = [PlantInDb.from_domain(plant) for plant in plants]
        locked = self._fetch_all()
        for plant_in_db in plants_in_db:
            locked[plant_in_db.plant_id] = plant_in_db
        self._write_models(list(locked.values()))


class FurnaceGroupJsonRepository:
    """
    Repository for storing furnace groups in a json file. Uses pydantic models for serialization / deserialization.
    All input and output is done using domain models. Domain models are converted to / from db models
    and then validated and dumped to json.
    """

    _all = None

    def __init__(self, path: Path) -> None:
        self.path = path
        self.seen: set[FurnaceGroup] = set()

    def _fetch_all(self) -> dict[str, FurnaceGroupInDb]:
        try:
            if not self.path.exists():
                return {}
            with self.path.open("r", encoding="utf-8") as f:
                furnace_groups_in_db = [FurnaceGroupInDb.model_validate_json(line) for line in f]
            return {fg.furnace_group_id: fg for fg in furnace_groups_in_db}
        except FileNotFoundError:
            return {}

    @property
    def all(self) -> dict[str, FurnaceGroupInDb]:
        """
        Cache fetching all models from file.
        """
        if self._all is None:
            self._all = self._fetch_all()
        return self._all

    def get(self, furnace_group_id) -> FurnaceGroup:
        return self.all[furnace_group_id].to_domain

    def list(self) -> list[FurnaceGroup]:
        return [fg.to_domain for fg in self.all.values()]

    def _write_models(self, locked: List[FurnaceGroupInDb]) -> None:
        self.path.parent.mkdir(exist_ok=True)
        locked.sort(
            key=lambda fg: fg.furnace_group_id
        )  # sort by id to keep the order of furnace groups in the file for easier diffing
        with self.path.open("w", encoding="utf-8") as f:
            for fg in locked:
                f.write(fg.model_dump_json(indent=2) + "\n")

    def add(self, furnace_group: FurnaceGroup) -> None:
        """Add a single furnace group to the repository."""
        fg_in_db = FurnaceGroupInDb.from_domain(furnace_group)
        locked = self._fetch_all()
        locked[fg_in_db.furnace_group_id] = fg_in_db
        self._write_models(list(locked.values()))
        self.seen.add(furnace_group)

    def add_list(self, furnace_groups: Iterable[FurnaceGroup]) -> None:
        """Add a list of furnace groups to the repository."""
        fgs_in_db = [FurnaceGroupInDb.from_domain(fg) for fg in furnace_groups]
        locked = self._fetch_all()
        for fg_in_db in fgs_in_db:
            locked[fg_in_db.furnace_group_id] = fg_in_db
        self._write_models(list(locked.values()))

    def to_json(self) -> str:
        """
        Return the JSON content of the furnace groups.
        """
        furnace_groups_in_db = list(self.all.values())
        return "[\n" + ",\n".join(fg.model_dump_json(indent=2) for fg in furnace_groups_in_db) + "\n]"


class DemandCenterInDb(BaseModel):
    demand_center_id: str
    center_of_gravity: LocationInDb
    demand_by_year: dict[Year, Volumes]

    @property
    def to_domain(self) -> DemandCenter:
        location = Location(**self.center_of_gravity.model_dump())
        return DemandCenter(
            demand_center_id=self.demand_center_id,
            center_of_gravity=location,
            demand_by_year=self.demand_by_year,
        )

    @classmethod
    def from_domain(cls, demand_center: DemandCenter) -> Self:
        location_in_db = LocationInDb(**demand_center.center_of_gravity.__dict__)
        return cls(
            demand_center_id=demand_center.demand_center_id,
            center_of_gravity=location_in_db,
            demand_by_year=demand_center.demand_by_year,
        )


class DemandCenterJsonRepository:
    """
    Repository for storing demand centers in a json file. Uses pydantic models for serialization / deserialization.
    All input and output is done using domain models. Domain models are converted to / from db models
    and then validated and dumped to json.
    """

    _all = None

    def __init__(self, path: Path) -> None:
        self.path = path
        self.seen: set[DemandCenter] = set()

    def _fetch_all(self) -> dict[str, DemandCenterInDb]:
        try:
            if not self.path.exists():
                return {}
            with self.path.open("r", encoding="utf-8") as f:
                demand_centers_in_db = [DemandCenterInDb.model_validate_json(line) for line in f]
            return {dc.demand_center_id: dc for dc in demand_centers_in_db}
        except FileNotFoundError:
            return {}

    @property
    def all(self) -> dict[str, DemandCenterInDb]:
        """
        Cache fetching all models from file.
        """
        if self._all is None:
            self._all = self._fetch_all()
        return self._all

    def get(self, demand_center_id) -> DemandCenter:
        return self.all[demand_center_id].to_domain

    def list(self) -> list[DemandCenter]:
        return [dc.to_domain for dc in self.all.values()]

    def _write_models(self, locked: List[DemandCenterInDb]) -> None:
        self.path.parent.mkdir(exist_ok=True)
        locked.sort(
            key=lambda dc: dc.demand_center_id
        )  # sort by id to keep the order of demand centers in the file for easier diffing
        with self.path.open("w", encoding="utf-8") as f:
            for dc in locked:
                f.write(dc.model_dump_json(indent=2) + "\n")

    def add(self, demand_center: DemandCenter) -> None:
        """Add a single demand center to the repository."""
        dc_in_db = DemandCenterInDb.from_domain(demand_center)
        locked = self._fetch_all()
        locked[dc_in_db.demand_center_id] = dc_in_db
        self._write_models(list(locked.values()))
        self.seen.add(demand_center)

    def add_list(self, demand_centers: Iterable[DemandCenter]) -> None:
        """Add a list of demand centers to the repository."""
        dcs_in_db = [DemandCenterInDb.from_domain(dc) for dc in demand_centers]
        locked = self._fetch_all()
        for dc_in_db in dcs_in_db:
            locked[dc_in_db.demand_center_id] = dc_in_db
        self._write_models(list(locked.values()))

    def to_json(self) -> str:
        """
        Return the JSON content of the demand centers.
        """
        demand_centers_in_db = list(self.all.values())
        return "[\n" + ",\n".join(dc.model_dump_json(indent=2) for dc in demand_centers_in_db) + "\n]"


class JsonRepository:
    plants: PlantRepository
    furnace_groups: FurnaceGroupRepository
    demand_centers: DemandCenterRepository

    def __init__(self, path: Path) -> None:
        self.plants = PlantJsonRepository(path)
        self.furnace_groups = FurnaceGroupJsonRepository(path)
        self.demand_centers = DemandCenterJsonRepository(path)
