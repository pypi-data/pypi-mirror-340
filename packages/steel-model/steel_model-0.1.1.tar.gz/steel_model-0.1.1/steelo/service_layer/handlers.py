from typing import Callable

from ..domain import events, commands, Year
from .unit_of_work import UnitOfWork
from ..domain.models import Environment
from steelo.utilities.global_variables import ANNOUNCED_STATUSES
from datetime import datetime


import logging

logger = logging.getLogger(__name__)


def close_furnace_group(cmd: commands.CloseFurnaceGroup, uow: UnitOfWork):
    with uow:
        plant = uow.plants.get(cmd.plant_id)
        plant.close_furnace_group(cmd.furnace_group_id)
        uow.commit()


def renovate_furnace_group(cmd: commands.RenovateFurnaceGroup, uow: UnitOfWork):
    with uow:
        plant = uow.plants.get(cmd.plant_id)
        plant.renovate_furnace_group(cmd.furnace_group_id)
        uow.commit()


def change_furnace_group_technology(cmd: commands.ChangeFurnaceGroupTechnology, uow: UnitOfWork):
    with uow:
        plant = uow.plants.get(cmd.plant_id)
        plant.change_furnace_group_technology(cmd.furnace_group_id, cmd.technology_name)
        uow.commit()


def add_furnace_group(cmd: commands.AddFurnaceGroup, uow: UnitOfWork):
    with uow:
        plant = uow.plants.get(cmd.plant_id)
        plant.add_furnace_group(cmd.new_furnace)
        plant.added_capacity += cmd.new_furnace.capacity
        plant.furnace_group_added(cmd.furnace_group_id, cmd.plant_id)
        uow.commit()


def update_cost_curve(_event: events.Event, uow: UnitOfWork, env: Environment):
    with uow:
        env.update_cost_curve(world_furnace_groups=[fg for plant in uow.plants.list() for fg in plant.furnace_groups])
        uow.commit()


def update_furnace_utilization_rates(event: events.SteelAllocationsCalculated, uow: UnitOfWork):
    allocation = event.allocations.allocations
    with uow:
        for plant in uow.plants.list():
            for fg in plant.furnace_groups:
                fg.utilization_rate = 0.0
        # furnace_groups = {fg.furnace_group_id: fg for plant in uow.plants.list() for fg in plant.furnace_groups}
        for (plant_obj, furnace_group, _), production in allocation.items():
            furnace_group.utilization_rate = production / furnace_group.capacity
        for plant in uow.plants.list():
            for fg in plant.furnace_groups:
                if fg.utilization_rate == 0.0:
                    uow.plants.get(plant.plant_id).close_furnace_group(fg.furnace_group_id)
        uow.commit()


def finalise_iteration(event: events.IterationOver, env: Environment, uow: UnitOfWork):
    env.year = Year(env.year + event.time_step_increment)
    with uow:
        for plant in uow.plants.list():
            plant.reset_capacity_changes()
            for fg in plant.furnace_groups:
                fg.lifetime.current = env.year
                if fg.lifetime.current >= fg.lifetime.time_frame.start and fg.status.lower() in ANNOUNCED_STATUSES:
                    fg.status = "Operating"
        uow.commit()
    logger.debug(f"finalising iteration. time: {datetime.now()}")


EVENT_HANDLERS: dict[type[events.Event], list[Callable]] = {
    events.FurnaceGroupClosed: [update_cost_curve],
    events.FurnaceGroupTechChanged: [update_cost_curve],
    events.FurnaceGroupRenovated: [update_cost_curve],
    events.FurnaceGroupAdded: [update_cost_curve],
    events.SteelAllocationsCalculated: [update_furnace_utilization_rates, update_cost_curve],
    events.IterationOver: [finalise_iteration],
}

COMMAND_HANDLERS: dict[type[commands.Command], Callable] = {
    commands.CloseFurnaceGroup: close_furnace_group,
    commands.RenovateFurnaceGroup: renovate_furnace_group,
    commands.ChangeFurnaceGroupTechnology: change_furnace_group_technology,
    commands.AddFurnaceGroup: add_furnace_group,
}
