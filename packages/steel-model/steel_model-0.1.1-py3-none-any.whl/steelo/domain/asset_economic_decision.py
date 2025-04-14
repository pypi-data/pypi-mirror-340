import logging

from datetime import date

from .calculate_costs import (
    calculate_cost_of_stranded_asset,
    calculate_lost_cash_flow,
    calculate_gross_cash_flow,
    BillsOfMaterial,
)
from .models import FurnaceGroup

# Configure logging at the start of your script
# Level can be DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(
    level=logging.DEBUG,  # sets the minimum logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def stranding_asset_cost(
    opex: list[float] | list[int],
    total_debt_repayment: list[float] | list[int],
    price: int | float,
    expected_production: int | float,
    lifetime_remaining: int,
    cost_of_equity: float,
) -> float:
    """
    This is simply a wrapper function that takes agent level insights and computes the cost of stranding an asset given it's current situtation
    """
    remaining_debt = total_debt_repayment[-lifetime_remaining:]
    remaining_opex = opex[-lifetime_remaining:]

    gross_cash_flow = calculate_gross_cash_flow(remaining_opex, price, expected_production)
    lost_cf = calculate_lost_cash_flow(remaining_debt, gross_cash_flow)
    return calculate_cost_of_stranded_asset(lost_cf, cost_of_equity)


# def agent_decision(
#     # current_cost: float,
#     lifetime_remaining: int,
#     main_production_equipment: str,
#     UR: int,
#     expected_production: int,
#     cost_of_equity: float,
#     cosa: float,
#     new_asset_lifetime: int = 20,
#     high_production_threshold: float = 0.95,
#     low_production_threshold: float = 0.6,
#     tech_npv: dict = {"EAF": 1, "DRI-EAF": 1.1, "BF-BOF": 1.3},
# ) -> str:
#     """
#     Determines the cost-optimal decision for an asset agent, dynamically adjusting based on economic conditions.
#     Parameters:
#     current_cost (float): Current cost of production
#     lifetime_remaining (int): Remaining lifetime of the asset
#     main_production_equipment (str): Current production technology
#     expected_production (int): Expected production for the asset
#     r (float): Discount rate
#     price (float): Price of the product
#     OPEX (float): Operating expenses
#     remaining_capital_debt (float): the remaining debt still owed on the asset
#     new_asset_lifetime (int): Lifetime of the new asset
#     pain_point (float): Pain threshold for CoSA impact on decision
#     high_production_threshold (float): High production threshold
#     low_production_threshold (float): Low production threshold
#     """
#     # Calculate NPV for current and alternative technologies
#     # tech_npv = NPV_function(expected_production, prev_tech=main_production_equipment)
#     if UR < low_production_threshold:
#         return "close"

#     # Calculate Capital Recovery Factor (CRF)
#     crf = (cost_of_equity * (1 + cost_of_equity) ** new_asset_lifetime) / (
#         (1 + cost_of_equity) ** new_asset_lifetime - 1
#     )

#     # Determine Opportunity Cost with CoSA considered
#     opportunity_value = calculate_opportunity_cost(tech_npv, main_production_equipment, cosa, crf)
#     print(opportunity_value)
#     # Check if economic situation favors a decision before end of life
#     # Find the minimum value in the row
#     optimal_tech, init_npv = optimal_decision(opportunity_value)

#     if lifetime_remaining == 0:
#         # Conduct end-of-life decision
#         return end_of_life_decision(
#             tech_npv,
#             main_production_equipment,
#             expected_production,
#             high_production_threshold,
#             low_production_threshold,
#         )

#     else:
#         # Find the best option after accounting for CoSA

#         # Choose action based on expected production and adjusted opportunity cost
#         if main_production_equipment == optimal_tech:
#             return evaluate_high_or_medium_production(UR, high_production_threshold, low_production_threshold)
#         else:
#             decision = evaluate_high_or_medium_production(UR, high_production_threshold, low_production_threshold)
#             if decision == "expand":
#                 return f"switch to {optimal_tech} consider expansion"
#             else:
#                 return f"switch to {optimal_tech}"


def optimal_decision(cost_of_opportunity: dict[str, float]) -> dict[str, float]:
    """
    Determines the cost-optimal decision for an asset agent, dynamically adjusting based on economic conditions.
    Parameters:
    cost_of_opportunity (pd.DataFrame): Cost of opportunity for each technology
    main_production_equipment (str): Current production technology

    Returns:
    list: the optimal production equipments based on npv
    """

    return max(cost_of_opportunity.items(), key=lambda item: item[1])  # type: ignore


# def evaluate_high_or_medium_production(expected_production, high_threshold, low_threshold):
#     """
#     Evaluates expand/renovate/close based on production level
#     """
#     if expected_production >= high_threshold:
#         return "expand"
#     elif low_threshold <= expected_production < high_threshold:
#         return "renovate / do nothing"
#     else:
#         return "close"


def calculate_opportunity_cost(
    tech_npv: dict[str, float], main_production_equipment: str, cost_of_stranding_asset: float, crf: float
) -> dict[str, float]:
    """
    Calculates the opportunity cost, adding stranded asset costs to technologies other than the main one.
    """
    stranded_costs = crf * cost_of_stranding_asset
    for tech, npv in tech_npv.items():
        if tech != main_production_equipment:
            tech_npv[tech] -= stranded_costs
    return tech_npv


# FIXME: This function cannot possibly work as it is (missing plant_id)
# def decision_cycle(
#     furnace_group: FurnaceGroup, optimal_tech: str, init_npv: float, asset_lifetime_remaining: int, message_bus
# ) -> None:
#     """
#     Makes a decision based on opportunity cost at the end of asset life.
#     And adjusts the furnace group in question accordingly
#     """
#
#     if init_npv < 0:
#         logging.warning("all NPV <0! Renovating this furnace group would lead to financial ruin. We will close it.")
#         message_bus.handle(CloseFurnaceGroup(furnace_group.furnace_group_id))
#         return
#
#     cmd: Command
#     if furnace_group.technology.name == optimal_tech:
#         if asset_lifetime_remaining <= 0:
#             furnace_group.last_renovation_date = date.today()
#             logging.info(
#                 f"The asset is operating the most profitable technology {furnace_group.technology.name}. SO we renovate"
#             )
#             cmd = RenovateFurnaceGroup(furnace_group_id=furnace_group.furnace_group_id)
#             message_bus.handle(cmd)
#             return
#             # consider_expanding(furnace_group, unit_fopex=1, capacity_increment=furnace_group.capacity * 0.5, demand=300)
#         else:
#             logging.info(
#                 f"The asset is operating the most profitable technology {furnace_group.technology.name} and will therefore continue operation as is"
#             )
#             return
#
#     else:
#         logging.info(f"Switching furnace_group to optimal technology {optimal_tech}")
#         technology = Technology(
#             name=optimal_tech,
#             bill_of_materials=getattr(BillsOfMaterial, optimal_tech.replace("-", "_")),
#             product=furnace_group.technology.product,
#         )
#         cmd = ChangeFurnaceGroupTechnology(
#             furnace_group_id=furnace_group.furnace_group_id, technology_name=technology.name
#         )
#         message_bus.handle(cmd)


def asset_cosa(furnace_group: FurnaceGroup, asset_lifetime_remaining: int, cost_of_equity: float, price: int) -> float:
    remaining_opex = [int(furnace_group.opex)] * asset_lifetime_remaining
    remaining_debt = furnace_group.debt_repayment_per_year

    gross_cash_flow = calculate_gross_cash_flow(
        opex=remaining_opex, price=price, expected_production=int(furnace_group.production)
    )
    lost_cf = calculate_lost_cash_flow(remaining_debt, gross_cash_flow)
    return calculate_cost_of_stranded_asset(lost_cf, cost_of_equity)


def switch_to_optimal_technology(fg: FurnaceGroup, optimal_tech: str):
    fg.technology.name = optimal_tech
    fg.technology.bill_of_materials = getattr(BillsOfMaterial, optimal_tech.replace("-", "_"))
    fg.last_renovation_date = date.today()

    return fg


# def consider_expanding(
#     fg: FurnaceGroup,
#     unit_fopex: float,
#     capacity_increment: float,
#     demand: float,
#     environment: Environment,
#     risk_aversion_pct: float = 0.1,
# ) -> str:
#     capex = fg.technology.greenfield_capex

#     current_price = environment.extract_price_from_costcurve(demand=demand)
#     init_npv = _npv_flow_wrapper(fg, fg.technology.name, unit_fopex=unit_fopex, price=current_price, capex=capex)

#     production_cost_dict = dict(
#         production=(fg.utilization_rate - risk_aversion_pct) * fg.capacity + capacity_increment,
#         unit_cost_of_production=fg.unit_production_cost,
#     )
#     ### This bit is slightly difficult
#     # Trigger cost curve recalculation
#     new_price = environment._update_dict_and_extract_price(
#         new_entry=production_cost_dict, furnace_group_id=fg.furnace_group_id, demand=demand
#     )
#     ###

#     expand_npv = _npv_flow_wrapper(
#         fg, switch_technology=fg.technology.name, capex=capex, unit_fopex=unit_fopex, price=new_price
#     )

#     print(f"expansion impact on price: current price {current_price}, new price {new_price}")
#     print(f"expansion impact: current npv: {init_npv}, new npv if expanding {expand_npv}")
#     if expand_npv <= init_npv:
#         return "Do not expand"
#     else:
#         return "expand"


# def technology_switch(optimal_tech, product):
#     logging.info(f"Switching furnace_group to optimal technology {optimal_tech}")
#     technology = Technology(
#         name=optimal_tech,
#         bill_of_materials=getattr(BillsOfMaterial, optimal_tech.replace("-", "_")),
#         product=product,
#     )
