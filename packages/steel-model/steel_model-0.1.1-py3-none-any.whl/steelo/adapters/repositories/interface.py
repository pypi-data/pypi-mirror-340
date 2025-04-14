from typing import Protocol, runtime_checkable, Iterable

from ...domain import Plant, FurnaceGroup, DemandCenter


@runtime_checkable
class PlantRepository(Protocol):
    seen: set[Plant]

    def add(self, plant: Plant) -> None:
        """Add a steel plant to the repository."""
        ...

    def add_list(self, plants: Iterable[Plant]) -> None:
        """Add an iterable of steel plants to the repository."""
        ...

    def get(self, plant_id) -> Plant:
        """Get a steel plant from the repository by ID."""
        ...

    def list(self) -> list[Plant]:
        """Get a list of all steel plants."""
        ...

    def get_by_furnace_group_id(self, furnace_group_id: str) -> Plant:
        """Get a steel plant from the repository by furnace group ID."""
        ...


@runtime_checkable
class FurnaceGroupRepository(Protocol):
    def add(self, furnace_group: FurnaceGroup) -> None:
        """Add a furnace group to the repository."""
        ...

    def add_list(self, plants: Iterable[FurnaceGroup]) -> None:
        """Add an iterable of furnace groups to the repository."""
        ...

    def get(self, furnace_group) -> FurnaceGroup:
        """Get a furnace group from the repository by ID."""
        ...

    def list(self) -> list[FurnaceGroup]:
        """Get a list of all furnace groups."""
        ...


@runtime_checkable
class DemandCenterRepository(Protocol):
    def add(self, demand_center: DemandCenter) -> None:
        """Add a demand center to the repository."""
        ...

    def add_list(self, demand_center: Iterable[DemandCenter]) -> None:
        """Add an iterable of demand center to the repository."""
        ...

    def get(self, demand_center) -> DemandCenter:
        """Get a demand center from the repository by ID."""
        ...

    def list(self) -> list[DemandCenter]:
        """Get a list of all demand center."""
        ...


@runtime_checkable
class Repository(Protocol):
    plants: PlantRepository
    furnace_groups: FurnaceGroupRepository
    demand_centers: DemandCenterRepository
