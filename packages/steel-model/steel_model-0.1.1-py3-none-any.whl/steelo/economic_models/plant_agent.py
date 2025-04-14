import logging

from ..service_layer.message_bus import MessageBus
from ..domain.trade_modelling.hitchcock_modelling import steel_trade_HP
from ..domain.events import SteelAllocationsCalculated

logger = logging.getLogger(__name__)


class AllocationModel:
    """Model to allocate resource to demand center from supply center"""

    @staticmethod
    def run(bus: MessageBus) -> None:
        """
        Run the trade model

        Args

        """
        allocations = steel_trade_HP(bus.uow.repository, bus.env.year)
        if (event := SteelAllocationsCalculated(allocations=allocations)) is not None:
            bus.handle(event)


class PlantAgentsModel:
    """Simplest possible economic model for a plant agent."""

    @staticmethod
    def run(bus: MessageBus) -> None:
        """
        Run the plant agent model.

        Args:
            bus (MessageBus): The message bus to send the event to
        """

        plants = bus.uow.plants.list()
        for plant in plants:
            for fg in plant.furnace_groups:
                if (
                    cmd := plant.evaluate_furnace_group_strategy(
                        fg.furnace_group_id, price=bus.env.extract_price_from_costcurve(demand=bus.env.current_demand)
                    )
                ) is not None:
                    bus.handle(cmd)

            # Maybe not the prettiest but it works?
            try:  # TODO: @Marcus - This will be updated as part of ticket on new expansion strategy
                assert isinstance(plant.location.iso3, str)
                new_furnace = plant.generate_new_furnace(
                    technology_name=bus.env.new_furnace_npv()[1],
                    current_year=bus.env.year,
                    product="steel",
                    # FIXME: workaround iso3 key error
                    cost_of_debt=bus.env.cost_of_capital.get(plant.location.iso3, 0.05),
                )  # TODO: cost of debt should come from plant level since location specific
                if (cmd := plant.evaluate_expansion(bus.env, new_furnace=new_furnace)) is not None:
                    bus.handle(cmd)
            except ValueError as e:
                if "Cost curve is empty" in str(e):
                    logger.warning("Cannot evaluate expansion: Cost curve is empty")
                else:
                    # Re-raise other ValueErrors
                    raise
