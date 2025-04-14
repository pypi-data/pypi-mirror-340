from dataclasses import dataclass

from typing import TYPE_CHECKING

# from steelo.domain.datacollector import DataCollector

if TYPE_CHECKING:
    from .models import SteelAllocations


class Event:
    """Base class for all events."""


@dataclass
class FurnaceGroupClosed(Event):
    """Furnace group closed."""

    furnace_group_id: str


@dataclass
class FurnaceGroupTechChanged(Event):
    """Furnace group technology was changed."""

    furnace_group_id: str


@dataclass
class FurnaceGroupRenovated(Event):
    """Furnace group renovated."""

    furnace_group_id: str


@dataclass
class FurnaceGroupAdded(Event):
    """Furnace group renovated."""

    plant_id: str
    furnace_group_id: str


@dataclass
class SteelAllocationsCalculated(Event):
    """Steel allocations calculated."""

    allocations: "SteelAllocations"


@dataclass
class IterationOver(Event):
    """This timestep is finalised."""

    time_step_increment: int
    # dc: DataCollector
