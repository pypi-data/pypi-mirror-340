from dataclasses import dataclass
from typing import Any


class Command:
    """Base class for all commands."""


@dataclass
class CloseFurnaceGroup(Command):
    """Close a furnace group."""

    plant_id: str
    furnace_group_id: str


@dataclass
class RenovateFurnaceGroup(Command):
    """Renovate a furnace group."""

    plant_id: str
    furnace_group_id: str


@dataclass
class ChangeFurnaceGroupTechnology(Command):
    """Change the technology of a furnace group."""

    plant_id: str
    furnace_group_id: str
    technology_name: str


@dataclass
class AddFurnaceGroup(Command):
    """Add a furnace group to a plant."""

    plant_id: str
    furnace_group_id: str
    new_furnace: Any
