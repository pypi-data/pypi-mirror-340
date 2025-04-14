import logging
from typing import TypedDict

from .dbom import derive_unnested_feedstock_bom, extract_steel, BusinessCaseArchitypes

from .constants import Auto


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

positive_infinity = float("inf")


def get_mvp_bom(technology: str):
    """
    Extract the bill of materials for the given business case archetype (no allocation data).

    Parameters:
        technology: The technology identifier used to look up the business case archetype.

    Returns:
        The extracted steel portion of the bill of materials.
    """
    business_case = BusinessCaseArchitypes.get_architype(technology)
    bom = derive_unnested_feedstock_bom(business_case)
    return extract_steel(bom)


class BillsOfMaterial:
    """
    Container for bills of materials for different technologies (cold-start mode without allocation data).

    NOTE: This class will become obsolete once trade allocation is used to distribute the feedstock
    among the different products.
    """

    BF_BOF = get_mvp_bom("BF-BOF")
    DRI_EAF = get_mvp_bom("DRI-EAF")
    EAF = get_mvp_bom("EAF")
    BF = get_mvp_bom("BF-BOF")  # TODO: update to BF-specific BOM
    BOF = get_mvp_bom("BF-BOF")  # TODO: update to BOF-specific BOM
    DRI = get_mvp_bom("DRI-EAF")  # TODO: update to DRI-specific BOM
    other = get_mvp_bom("BF-BOF")  # TODO: update to correct BOM for 'other'
    unknown = get_mvp_bom("BF-BOF")  # TODO: update to correct BOM for 'unknown'
    OHF = get_mvp_bom("BF-BOF")  # TODO: update to OHF-specific BOM


def calculate_variable_opex(materials_cost_data: dict, energy_cost_data: dict) -> int:
    """
    Calculate the total variable operating expenditure (OPEX).

    Parameters:
        materials_cost_data: Dictionary of material cost data with keys 'demand' and 'unit_cost' (with subkey "Value").
        energy_cost_data: Dictionary of energy cost data with keys 'demand' and 'unit_cost' (with subkey "Value").

    Returns:
        The total variable OPEX.
    """
    if not materials_cost_data:
        raise ValueError("materials_cost_data is empty.")

    material_cost = sum(data["demand"] * data["unit_cost"]["Value"] for data in materials_cost_data.values())
    energy_cost = sum(data["demand"] * data["unit_cost"]["Value"] for data in energy_cost_data.values())

    return material_cost + energy_cost


def calculate_fixed_opex(greenfield_capex: float, opex_capex_ratio: float = 0.1) -> float:
    """
    Calculate the fixed operating expenditure (O&M) as a fraction of the greenfield CAPEX.

    Parameters:
        greenfield_capex: The CAPEX related to building a new plant.
        opex_capex_ratio: The ratio of CAPEX allocated to fixed OPEX. Defaults to 0.1.

    Returns:
        The fixed OPEX.
    """
    return greenfield_capex * opex_capex_ratio


class CostData(TypedDict):
    demand: float
    unit_cost: dict[str, float]  # or a more specific TypedDict if you know more


BillOfMaterialsDict = dict[str, dict[str, CostData]]


def calculate_opex(bill_of_materials: BillOfMaterialsDict, fixed_opex: float, production: float) -> float:
    """
    Calculate the total operating expenditure (OPEX) per unit produced.

    Parameters:
        bill_of_materials: The bill of materials for producing one unit.
            Expected to have keys "materials" and "energy" with associated cost data.
        fixed_opex: The fixed operational expenditure.
        production: The production volume.

    Returns:
        The per-unit OPEX (fixed OPEX per unit plus variable OPEX per unit).
    """
    materials_cost = bill_of_materials["materials"]
    material_cost = sum(data["demand"] * data["unit_cost"]["Value"] for data in materials_cost.values())
    energy_cost_data = bill_of_materials["energy"]
    energy_cost = sum(data["demand"] * data["unit_cost"]["Value"] for data in energy_cost_data.values())
    variable_opex = material_cost + energy_cost
    return fixed_opex / production + variable_opex if production > 0 else positive_infinity  # to avoid division by zero


def calculate_debt_repayment(
    total_investment: float,
    equity_share: float,
    lifetime: int,
    cost_of_debt: float,
    lifetime_remaining: int | None = None,
) -> list[float]:
    """
    Calculate the yearly debt repayment schedule based on the investment parameters.

    Parameters:
        total_investment: The total investment cost.
        equity_share: The fraction of the investment financed by equity.
        lifetime: The full repayment lifetime in years.
        cost_of_debt: The annual interest rate on debt.
        lifetime_remaining: The remaining years for debt repayment. Defaults to lifetime.

    Returns:
        A list of yearly repayment amounts.
    """
    if lifetime_remaining is None:
        lifetime_remaining = lifetime

    debt = total_investment * (1 - equity_share)

    if debt == 0:
        total_repayment_list = [0.0] * lifetime
    else:
        capital_repayment_list = [debt / lifetime] * lifetime_remaining
        total_repayment_list = []
        for capital_repayment in capital_repayment_list:
            remaining_debt = debt - capital_repayment
            interest_repayment = ((debt + remaining_debt) / 2) * cost_of_debt
            total_repayment_list.append(interest_repayment + capital_repayment)
            debt = remaining_debt

    return total_repayment_list[-lifetime_remaining:]


def calculate_current_debt_repayment(
    total_investment: float,
    lifetime_expired: bool,
    lifetime_years: int,
    years_elapsed: int,
    cost_of_debt: float,
    equity_share: float,
) -> float:
    """
    Calculate the total debt repayment (principal plus interest) for the current year.

    Parameters:
        total_investment: The total investment cost.
        lifetime_expired: Flag indicating if the repayment period is over.
        lifetime_years: The total repayment lifetime in years.
        years_elapsed: The number of years elapsed since operation start.
        cost_of_debt: The annual interest rate on debt.
        equity_share: The fraction of the investment financed by equity.

    Returns:
        float: The debt repayment amount for the current year.
    """
    debt = total_investment * (1 - equity_share)

    if debt == 0 or lifetime_expired:
        return 0.0

    yearly_principal = debt / lifetime_years
    remaining_debt = debt - (yearly_principal * (years_elapsed - 1))
    avg_debt = (remaining_debt + (remaining_debt - yearly_principal)) / 2

    return yearly_principal + (avg_debt * cost_of_debt)


def calculate_unit_production_cost(opex: float, current_debt_repayment: float, production: float) -> float:
    """
    Calculate the unit production cost by adding OPEX and debt repayment costs per unit.

    Parameters:
        opex: The operating expenditure.
        current_debt_repayment: The debt repayment cost for the current period.
        production: The production volume.

    Returns:
        float: The cost per unit of production.
    """
    return opex + current_debt_repayment / production if production > 0 else positive_infinity


def calculate_gross_cash_flow_per_step(price: float, opex: float, expected_production: float) -> float:
    """
    Calculate the gross cash flow for a single time step.

    Parameters:
        price: The price per unit.
        opex: The operating expenditure per unit.
        expected_production: The production volume for the time step.

    Returns:
        float: The gross cash flow for the step.
    """
    return (price - opex) * expected_production


def calculate_gross_cash_flow(
    opex: list[float] | list[int], price: float | int, expected_production: float | int
) -> list[float]:
    """
    Calculate the gross cash flow over multiple time steps.

    Parameters:
        opex: List of operating expenditures per period.
        price: The price per unit.
        expected_production: The production volume per period.

    Returns:
        list[float]: A list of gross cash flows for each period.
    """
    return [calculate_gross_cash_flow_per_step(price, opex_year, expected_production) for opex_year in opex]


def calculate_net_cash_flow(total_debt_repayment: list[float], gross_cash_flow: list[float]) -> list[float]:
    """
    Calculate the net cash flow by subtracting debt repayment from gross cash flow for each period.

    Parameters:
        total_debt_repayment: List of debt repayment amounts per period.
        gross_cash_flow: List of gross cash flows per period.

    Returns:
        list[float]: A list of net cash flow values.
    """
    if len(total_debt_repayment) != len(gross_cash_flow):
        raise ValueError("The lengths of total_debt_repayment and gross_cash_flow must be the same.")

    return [gross - debt for gross, debt in zip(gross_cash_flow, total_debt_repayment)]


def calculate_lost_cash_flow(
    total_debt_repayment: list[float] | list[int], gross_cash_flow: list[float] | list[int]
) -> list[float]:
    """
    Calculate the lost cash flow by adding debt repayment to gross cash flow for each period.

    Parameters:
        total_debt_repayment: List of debt repayment amounts per period.
        gross_cash_flow: List of gross cash flows per period.

    Returns:
        list[float]: A list of lost cash flow values.
    """
    if len(total_debt_repayment) != len(gross_cash_flow):
        raise ValueError("The lengths of total_debt_repayment and gross_cash_flow must be the same.")

    return [gross + debt for gross, debt in zip(gross_cash_flow, total_debt_repayment)]


def calculate_cost_of_stranded_asset(lost_cash_flow: list[float], cost_of_debt: float) -> float:
    """
    Calculate the net present value (NPV) of losses due to stranding an asset.

    Parameters:
        lost_cash_flow: Future lost cash flows per period.
        cost_of_debt: The discount rate (cost of debt).

    Returns:
        float: The NPV of the stranded asset cost.
    """
    npv_loss = 0.0
    for t, cash in enumerate(lost_cash_flow, start=1):
        discount_factor = (1 + cost_of_debt) ** t
        npv_loss += cash / discount_factor
    return npv_loss


def calculate_npv_costs(
    net_cash_flow: list[float],
    cost_of_debt: float,
    equity_share: float,
    fixed_opex: float,
    total_investment: float = 0,
) -> float:
    """
    Calculate the net present value (NPV) of a series of cash flows.

    Parameters:
        net_cash_flow: List of future net cash flows per period.
        cost_of_debt: The discount rate (cost of debt).
        equity_share: The fraction of the investment financed by equity.
        fixed_opex: The fixed operating expenditure.
        total_investment: The total investment cost. Defaults to 0.

    Returns:
        float: The calculated NPV.
    """
    npv = -(total_investment * equity_share + fixed_opex)
    for t, cash in enumerate(net_cash_flow, start=1):
        npv += cash / ((1 + cost_of_debt) ** t)
    return npv


def calculate_levelised_cost(
    expected_production: list[float],
    opex: list[float],
    cost_of_debt: float,
    total_investment: float,
    total_repayment: list[float],
    equity_share: float,
    fixed_opex: float,
) -> float:
    """
    Calculate the levelised cost of steel or iron.
    The levelised cost of x is determined by discounting all costs and dividing by the production.

    Parameters:
        expected_production: Expected production per period.
        opex: Operating expenditures per period.
        cost_of_debt: Discount rate (cost of debt).
        total_investment: Total upfront investment cost.
        total_repayment: Debt repayments per period.
        equity_share: Fraction of the investment financed by equity.
        fixed_opex: Fixed operating expenditure at time zero.

    Raises:
        ValueError: If input lists have mismatched lengths or if discounted production is zero.
    """
    if not (len(expected_production) == len(opex) == len(total_repayment)):
        raise ValueError("Input lists 'expected_production', 'opex', and 'total_repayment' must have the same length.")

    initial_investment = total_investment * equity_share + fixed_opex
    discounted_cost = -initial_investment

    for t, (opex_year, repayment) in enumerate(zip(opex, total_repayment), start=1):
        discounted_cost -= (opex_year + repayment) / ((1 + cost_of_debt) ** t)

    discounted_production = sum(prod / ((1 + cost_of_debt) ** t) for t, prod in enumerate(expected_production, start=1))

    if discounted_production == 0:
        raise ValueError("Discounted production is zero, cannot compute levelised cost.")

    levelised_cost = discounted_cost / discounted_production
    return -levelised_cost


def calculate_npv_full(
    technology: str,
    capex: float,
    capacity: float,
    fixed_opex: float,
    expected_utilisation_rate: float,
    price: float,
    lifetime: float = 20,
    cost_of_debt: float = 0.05,
    equity_share: float = 0.2,
    bill_of_materials: dict[str, dict[str, dict[str, float]]] = Auto,
) -> float:
    """
    Calculate the net present value (NPV) for a technology.

    Parameters:
        technology: The technology identifier.
        capex: The capital expenditure per unit capacity.
        capacity: The capacity of the furnace group.
        fixed_opex: Fixed operating expenditure.
        expected_utilisation_rate: Expected utilisation rate.
        price: The market price per unit product.
        lifetime: The project lifetime in years. Defaults to 20.
        cost_of_debt: The cost of debt (interest rate). Defaults to 0.05.
        equity_share: The fraction of the investment financed by equity. Defaults to 0.2.
        bill_of_materials: Bill of materials data. If not provided, it is derived from BillsOfMaterial.

    Returns:
        The NPV for the technology.
    """
    if not bill_of_materials:
        bill_of_materials = getattr(BillsOfMaterial, technology.replace("-", "_"))

    variable_opex = calculate_variable_opex(
        bill_of_materials["materials"],
        bill_of_materials["energy"],
    )
    total_opex = fixed_opex + variable_opex
    total_investment = capacity * capex

    debt_repayment = calculate_debt_repayment(
        total_investment=total_investment, equity_share=equity_share, lifetime=int(lifetime), cost_of_debt=cost_of_debt
    )

    opex_list = [total_opex] * len(debt_repayment)
    production = expected_utilisation_rate * capacity
    gross_cash_flow = calculate_gross_cash_flow(opex=opex_list, price=price, expected_production=float(production))
    net_cash_flow = calculate_net_cash_flow(total_debt_repayment=debt_repayment, gross_cash_flow=gross_cash_flow)

    return calculate_npv_costs(
        net_cash_flow=net_cash_flow,
        cost_of_debt=cost_of_debt,
        equity_share=equity_share,
        fixed_opex=fixed_opex,
        total_investment=total_investment,
    )


def stranding_asset_cost(
    debt_repayment_per_year: list[float],
    opex: list[float],
    remaining_time: int,
    price: float,
    expected_production: float,
    cost_of_debt: float,
) -> float:
    """
    Calculate the cost associated with stranding an asset.

    Parameters:
        debt_repayment_per_year: Yearly debt repayment amounts.
        opex: Yearly operating expenditures.
        remaining_time: Remaining time (in years) for the asset.
        price: Price per unit product.
        expected_production: Production volume per period.
        cost_of_debt: Annual cost of debt (interest rate).

    Returns:
        The net present value of losses due to the stranded asset.
    """
    remaining_debt = debt_repayment_per_year[-remaining_time:]
    remaining_opex = opex[-remaining_time:]
    gross_cash_flow = calculate_gross_cash_flow(remaining_opex, price, expected_production)
    lost_cash_flow = calculate_lost_cash_flow(remaining_debt, gross_cash_flow)
    return calculate_cost_of_stranded_asset(lost_cash_flow, cost_of_debt)


def calculate_technogy_npv(
    capex_dict: dict[str, float],
    capacity: float,
    fixed_opex: float,
    expected_utilisation_rate: float,
    price: float,
    lifetime: int = 20,
    cost_of_debt: float = 0.05,
    equity_share: float = 0.2,
) -> dict[str, float]:
    """
    Calculate the net present value (NPV) for multiple technologies based on their CAPEX and other parameters.

    Parameters:
        capex_dict: Mapping of technology identifiers to CAPEX values.
        capacity: The capacity of the furnace group.
        fixed_opex: Fixed operating expenditure.
        expected_utilisation_rate: Expected utilisation rate.
        price: Market price per unit.
        lifetime: Lifetime in years. Defaults to 20.
        cost_of_debt: Cost of debt (interest rate). Defaults to 0.05.
        equity_share: Fraction of the investment financed by equity. Defaults to 0.2.

    Returns:
        A dictionary mapping technology identifiers to their NPV.
    """
    return {
        technology: calculate_npv_full(
            technology,
            capex,
            capacity,
            fixed_opex,
            expected_utilisation_rate,
            price,
            lifetime,
            cost_of_debt,
            equity_share,
        )
        for technology, capex in capex_dict.items()
    }.copy()


def derive_best_technology_switch(
    current_technology: str,
    cost_of_debt: float = 0.05,
    equity_share: float = 0.2,
    lifetime: int = 20,
    expected_utilisation_rate: float = 0.7,
    capacity: float = 1000,
    price: float = 100,
    mvp: bool = True,
    bill_of_materials: dict[str, dict[str, dict[str, float]]] = Auto,
    cosa=None,
) -> tuple[float, str]:
    """
    Calculate the net present value (NPV) for switching or renovating technologies and determine the best alternative.

    Parameters:
        current_technology: The current technology identifier.
        cost_of_debt: The cost of debt (interest rate). Defaults to 0.05.
        equity_share: The equity share. Defaults to 0.2.
        lifetime: The technology lifetime in years. Defaults to 20.
        expected_utilisation_rate: Expected utilisation rate. Defaults to 0.7.
        capacity: Capacity of the furnace group. Defaults to 1000.
        price: Market price per unit. Defaults to 100.
        mvp: Flag for MVP mode. Defaults to True.
        bill_of_materials: Bill of materials data. Defaults to Auto.
        cosa: Cost of stranding the current to subtract from non-current technologies.

    Returns:
        A tuple containing the best NPV and its corresponding technology identifier.
    """
    from steelo.domain.Capex import TECH_SWITCH_CAPEX, FULL_GREENFIELD_CAPEX

    npv_dict = {}
    if mvp:
        for tech, capex in TECH_SWITCH_CAPEX[current_technology].items():
            if tech in ["BOF", "DRI-EAF", "EAF"]:
                npv_dict[tech] = calculate_npv_full(
                    technology=tech,
                    capex=capex,
                    capacity=capacity,
                    fixed_opex=calculate_fixed_opex(FULL_GREENFIELD_CAPEX[tech]),
                    expected_utilisation_rate=expected_utilisation_rate,
                    price=price,
                    lifetime=lifetime,
                    cost_of_debt=cost_of_debt,
                    equity_share=equity_share,
                )
                if tech != current_technology and cosa is not None:
                    npv_dict[tech] -= cosa
    else:
        for tech, capex in TECH_SWITCH_CAPEX[current_technology].items():
            npv_dict[tech] = calculate_npv_full(
                technology=tech,
                capex=capex,
                capacity=capacity,
                fixed_opex=calculate_fixed_opex(FULL_GREENFIELD_CAPEX[tech]),
                expected_utilisation_rate=expected_utilisation_rate,
                price=price,
                lifetime=lifetime,
                cost_of_debt=cost_of_debt,
                equity_share=equity_share,
                bill_of_materials=bill_of_materials,
            )
            if tech != current_technology and cosa is not None:
                npv_dict[tech] -= cosa

    # Find tech with maximum NPV value
    best_tech = max(npv_dict, key=lambda k: npv_dict[k] if npv_dict[k] is not None else float("-inf"))
    best_value = npv_dict[best_tech]
    return best_value, best_tech


def calculate_capex_reduction_rate(
    capacity_zero: float,
    capacity_current: float,
    learning_coeff: float = -0.043943347587597055,
) -> float:
    """
    Calculate the CAPEX reduction rate based on learning effects.

    Parameters:
        capacity_zero: The initial capacity.
        capacity_current: The current capacity.
        learning_coeff: The learning coefficient. Defaults to -0.043943347587597055.

    Returns:
        The CAPEX reduction rate.
    """
    return (capacity_current / capacity_zero) ** learning_coeff


def calculate_debt_report(
    total_investment: float,
    lifetime_expired: bool,
    lifetime_years: int,
    years_elapsed: int,
    cost_of_debt: float,
    equity_share: float,
) -> tuple[float, float]:
    """
    Calculate the debt components (yearly principal and interest) for reporting purposes.

    Parameters:
        total_investment (float): The total investment cost.
        lifetime_expired (bool): Flag indicating if the debt repayment lifetime has expired.
        lifetime_years (int): The total number of repayment years.
        years_elapsed (int): The number of years that have elapsed.
        cost_of_debt (float): The annual interest rate on debt.
        equity_share (float): The fraction of the investment financed by equity.

    Returns:
        A tuple of (yearly_principal, interest_repayment) for the current year.
    """
    debt = total_investment * (1 - equity_share)

    if debt == 0 or lifetime_expired:
        return 0.0, 0.0

    yearly_principal = debt / lifetime_years
    remaining_debt = debt - (yearly_principal * (years_elapsed - 1))
    avg_debt = (remaining_debt + (remaining_debt - yearly_principal)) / 2

    return yearly_principal, (avg_debt * cost_of_debt)
