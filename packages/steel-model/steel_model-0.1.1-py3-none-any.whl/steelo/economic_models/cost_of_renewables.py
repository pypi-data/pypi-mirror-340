from typing import cast

import pandas as pd
import numpy as np
import logging

from ..domain.mappings import (
    COUNTRY_TO_IRENA_MAP,
    COUNTRY_TO_REGION_MAP,
    COUNTRY_TO_CODE_MAP,
    COUNTRY_TO_SSP_REGION_MAP,
)

from steelo.utilities.global_variables import LEARNING_RATES, LIFETIME, YEARLY_DETERIORATION_RATE
from steelo.config import settings

# ----------------------------------------------------- FUNCTION DEF -----------------------------------------------------


def load_capacity_data(base_yr: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads the capacity factor and capacity projections data for solar PV and onshore wind.

        - Capacity factors: daily variable capacity factors (i.e., ratio between the actual and the theoretical maximum
        output when running always at full capacity; normal CF * 24) and size of bare land areas (i.e., number of km^2
        available to build on). Temporal res.: yearly. Spatial resolution: country level. Units: MW/km^2. Assumptions:
        capacity factors derived under the constraint of only using bare land areas. Source: Systemiq internal.

        - Historical capacity: historically installed capacity data for solar PV and onshore wind. Temporal res.: yearly.
        Time: 2023. Spatial res.: country and regional (244 countries). Units: MW.
        Source: IRENA (https://pxweb.irena.org/pxweb/en/IRENASTAT/IRENASTAT__Power%20Capacity%20and%20Generation/Country_ELECSTAT_2024_H2.px/).

        - Capacity projections (SSP-RCP): capacity buildout projections from 2005 to 2100. Temporal res.: decadal.
        Spatial res.: regional (5 regions). Units: GW. Source: IIASA (https://tntcat.iiasa.ac.at/SspDb/dsd?Action=htmlpage&page=welcome).
        Scenario selection:
            - SSP1-2.6: Sustainability; low emissions in line with 2°C target; low adaptation and mitigation challenges
            - SSP2-4.5: Middle of the Road; moderate emissions; medium adaptation and mitigation challenges
            - SSP3-baseline: Regional Rivalry; high emissions from no global climate policy (BAU); high adaptation and mitigation challenges
    """
    logging.info("Loading capacity data")
    # Load capacity factors data
    capacity_fact_file_path = settings.project_root / "data" / "capacity_factors.csv"
    capacity_factors_data = pd.read_csv(capacity_fact_file_path, index_col=0)

    # Load historical capacity data
    historical_capacity_file_path = settings.project_root / "data" / f"installed_renewables_capacity_{str(base_yr)}.csv"
    historical_capacity_data = pd.read_csv(historical_capacity_file_path, header=0)

    # Load capacity projections data
    solar_capacity_proj_file_path = settings.project_root / "data" / "ssp_rcp_solar_capacity_projections.xlsx"
    wind_capacity_proj_file_path = settings.project_root / "data" / "ssp_rcp_onshore_wind_capacity_projections.xlsx"
    solar_capacity_proj_data = pd.read_excel(solar_capacity_proj_file_path, usecols="A:P", header=0, skipfooter=2)
    wind_capacity_proj_data = pd.read_excel(wind_capacity_proj_file_path, usecols="A:P", header=0, skipfooter=2)

    return capacity_factors_data, historical_capacity_data, solar_capacity_proj_data, wind_capacity_proj_data


def load_cost_data(base_yr: int) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Loads the CAPEX data for solar and onshore wind, and other cost data.
        - CAPEX: Total cost, cost of hardware, and cost of non-hardware. Spatial resolution: regional level (16 regions
        worldwide). Year: 2022. Units: USD/kW. Source: Systemiq internal.
        - Other costs: Output from economic model. Loaded for cost of capital.
    """
    logging.info("Loading cost data")
    # Load solar CAPEX data
    solar_capex_file_path = settings.project_root / "data" / f"capex_solar_{str(base_yr)}.csv"
    solar_capex_data = pd.read_csv(solar_capex_file_path, index_col=0)

    # Load onshore wind CAPEX data
    wind_capex_file_path = settings.project_root / "data" / f"capex_onshore_wind_{str(base_yr)}.csv"
    wind_capex_data = pd.read_csv(wind_capex_file_path, index_col=0)

    # Load other costs data
    cost_of_x_path = settings.project_root / "data" / "cost_of_x.json"
    cost_data = pd.read_json(cost_of_x_path)

    return solar_capex_data, wind_capex_data, cost_data


def prepare_capex_data_per_tech(raw_capex_data: pd.DataFrame, tech_name: str) -> pd.DataFrame:
    """
    Renames the columns to include the technology name, resets the index, and drops irrelevant columns.
    """

    clean_capex_data = raw_capex_data.copy()
    clean_capex_data = clean_capex_data.reset_index().rename(
        columns={
            "Total capex (USD/kW)": f"Total capex {tech_name} (USD/kW)",
            "Hardware capex (USD/kW)": f"Hardware capex {tech_name} (USD/kW)",
            "Non-hardware capex (USD/kW)": f"Non-hardware capex {tech_name} (USD/kW)",
            "Opex (%)": f"Opex {tech_name} (%)",
        }
    )
    clean_capex_data.drop(columns=["Source"], inplace=True)

    return clean_capex_data


def preprocess_cost_data(
    solar_capex: pd.DataFrame,
    wind_capex: pd.DataFrame,
    cost_data: pd.DataFrame,
    countries_df: pd.DataFrame,
    country_to_region_map: dict,
    country_to_code_map: dict,
) -> pd.DataFrame:
    """
    Preprocesses the CAPEX and cost of capital data for solar and wind technologies. Maps the regional CAPEX data to countries,
    fills missing cost of capital values (about 20%) with the global average, and merges all data into a single df.
    """
    logging.info("Preprocessing cost data")
    # CAPEX
    solar_capex_pp = prepare_capex_data_per_tech(solar_capex, "solar")
    wind_capex_pp = prepare_capex_data_per_tech(wind_capex, "wind")
    renewable_capex = pd.merge(solar_capex_pp, wind_capex_pp, on="Region", how="outer")
    countries_ = countries_df.copy()
    countries_["Region"] = countries_["Country"].map(country_to_region_map)
    renewable_capex_per_country = pd.merge(countries_, renewable_capex, on="Region", how="left")

    # Cost of capital
    cost_of_capital = cost_data.copy()[["Country code", "Cost of capital - renewables"]].rename(
        columns={"Cost of capital - renewables": "Cost of capital (%)"}
    )
    country_to_code_map_r = {v: k for k, v in country_to_code_map.items()}
    cost_of_capital["Country"] = cost_of_capital["Country code"].map(country_to_code_map_r)
    cost_of_capital.drop(columns=["Country code"], inplace=True)

    # All costs
    cost_per_country = (
        pd.merge(renewable_capex_per_country, cost_of_capital, on="Country", how="left")
        .set_index("Country")
        .sort_index()
    )
    cost_per_country.drop(columns=["Region"], inplace=True)
    cost_per_country.fillna(cost_per_country.select_dtypes(include=[np.number]).mean(), inplace=True)

    return cost_per_country


def preprocess_capacity_factors(cap_fact: pd.DataFrame) -> pd.DataFrame:
    """
    Restructures the data, divides all data by 24 to get hourly capacity factors instead of daily ones, and
    fills missing values with the global average.
    """
    logging.info("Preprocessing capacity factors data")
    cap_fact_ = (
        cap_fact.transpose()
        .reset_index()
        .rename(
            columns={
                "index": "Country",
                "pvDaily_total": "Capacity factor solar (%)",
                "windDaily_total": "Capacity factor wind (%)",
            }
        )
    )
    for tech in ["solar", "wind"]:
        cap_fact_[f"Capacity factor {tech} (%)"] = cap_fact_[f"Capacity factor {tech} (%)"] / 24
    cap_fact_.drop(columns=["solar_area", "onshore_wind_area"], inplace=True)
    cap_fact_.fillna(cap_fact_.select_dtypes(include=[np.number]).mean(), inplace=True)
    cap_fact_ = cap_fact_.set_index("Country")

    return cap_fact_


def preprocess_historical_renewable_capacity(
    hist_cap: pd.DataFrame, countries: pd.DataFrame, country_to_irena_map: dict
) -> tuple[pd.Series, pd.Series]:
    """
    Maps country names from different data sources, fills missing values with the global average, and splits the data into solar and wind.
    """
    logging.info("Preprocessing historical capacity data")
    hist_cap_ = hist_cap.copy().rename(columns={"Country": "IRENA Country"})
    countries_ = countries.copy()
    countries_["IRENA Country"] = countries_["Country"].map(country_to_irena_map)
    cap_now = (
        pd.merge(countries_, hist_cap_, on="IRENA Country", how="left")
        .set_index("Country")
        .sort_index()
        .drop(columns=["IRENA Country"])
    )
    for tech in ["solar", "wind"]:
        cap_now[f"Capacity {tech} (MW)"] = pd.to_numeric(cap_now[f"Capacity {tech} (MW)"], errors="coerce")
        cap_now[f"Capacity {tech} (MW)"] = cap_now[f"Capacity {tech} (MW)"].fillna(
            cap_now[f"Capacity {tech} (MW)"].mean()
        )
    solar_cap_now = cap_now["Capacity solar (MW)"]
    wind_cap_now = cap_now["Capacity wind (MW)"]

    return solar_cap_now, wind_cap_now


def correct_ssp_projections_with_current_capacity(
    current_capacity: pd.Series | pd.DataFrame,
    raw_capacity_data: pd.DataFrame,
    countries_df: pd.DataFrame,
    country_to_ssp_region_map: dict,
    base_yr: int,
    tech: str,
) -> pd.DataFrame:
    """
    Corrects the magnitude of the SSP projections with the current capacity data. Only the gradient of the SSP projections is used to project
    these current data until 2100. Expands the decadal SSP projections to yearly resolution via linear interpolation.
    """
    logging.info(f"Correcting SSP projections with current capacity data for {tech}")
    countries_ = countries_df.copy()
    countries_["Region"] = countries_["Country"].map(country_to_ssp_region_map)
    capacity_per_country = pd.merge(raw_capacity_data, countries_, on="Region", how="left")

    # Fill missing values with global average
    capacity_per_country.fillna(capacity_per_country.select_dtypes(include=[np.number]).mean(), inplace=True)

    # Set index and drop irrelevant columns
    capacity_per_country = capacity_per_country.set_index(["Country", "Scenario"])
    capacity_per_country.drop(columns=["Model", "Variable", "Region", "Unit", 2005, 2010], inplace=True)
    year_cols = cast(
        list[int], [col for col in capacity_per_country.columns if isinstance(col, int) and 1900 <= int(col) <= 3000]
    )  # Select only years
    capacity_per_country = capacity_per_country.loc[:, year_cols]

    # Expand decadal data to yearly and interpolate linearly
    capacity_per_country_interp = capacity_per_country.copy()
    min_year = min(year_cols)
    max_year = max(year_cols)
    for year in range(min_year, max_year + 1, 1):
        if year not in capacity_per_country_interp.columns:
            capacity_per_country_interp.loc[:, int(year)] = np.nan
    capacity_per_country_interp = capacity_per_country_interp.sort_index(axis=1).interpolate(axis=1)

    # Calculate the gradient (ratio of growth between consecutive years) and drop irrelevant years
    interp_year_cols = [
        col for col in capacity_per_country_interp.columns if isinstance(col, int) and 1900 <= int(col) <= 3000
    ]  # Select only years
    year_cols_to_drop = [col for col in interp_year_cols if isinstance(col, int) and col <= base_yr]
    # TODO: Check div by zero
    capacity_gradient = capacity_per_country_interp.pct_change(axis=1).drop(columns=year_cols_to_drop)

    # Use the gradient to project the capacity from the base year onto [base_year +1, 2100]
    capacity_projection = (
        pd.merge(current_capacity, capacity_gradient.reset_index(), on="Country", how="left")
        .rename(columns={f"Capacity {tech} (MW)": base_yr})
        .set_index(["Country", "Scenario"])
    )
    projection_years = cast(list[int], sorted([col for col in capacity_projection.columns if isinstance(col, int)]))
    for i in range(1, len(projection_years)):
        year = projection_years[i]
        prev_year = projection_years[i - 1]
        capacity_projection[year] = capacity_projection[prev_year] * (1 + capacity_projection[year])

    return capacity_projection


def update_capex_using_learning_curve(capacity_0: float, capacity_t: float, capex_0: float, lr: float) -> float:
    """
    Update the capex based on the capacity change.
    Note: Capacity units are irrelevant, since they cancel out.
    Cases with capacity_0 == 0 are replaced by small epsilon to avoid division by 0.
    """
    b = np.log(1 - lr) / np.log(2)
    # TODO: Move epsilon to global vars
    epsilon = 1e-3
    capacity_0 = max(capacity_0, epsilon)
    capex_t = capex_0 * (capacity_t / capacity_0) ** b

    return capex_t


def project_capex_across_all_dims(
    capacity_projections: pd.DataFrame,
    costs: pd.DataFrame,
    learning_rates: pd.DataFrame,
    base_yr: int,
    tech: str,
) -> pd.DataFrame:
    """
    Projects the CAPEX for a given technology across all dimensions (countries, scenarios, learning rates, and years) using the learning curve.
    """
    logging.info(f"Projecting CAPEX for {tech}")
    # Initialize an empty dataframe
    countries = capacity_projections.index.get_level_values("Country").unique()
    ssp_scenarios = capacity_projections.index.get_level_values("Scenario").unique().sort_values()
    index = pd.MultiIndex.from_product(
        [countries, ssp_scenarios, learning_rates.index], names=["Country", "Scenario", "LR Scenario"]
    )
    years = capacity_projections.columns
    capex_projection = pd.DataFrame(index=index, columns=years)

    # Store the base year CAPEX data in the empty dataframe
    # TODO: Add split up between hardware and non-hardware capex if needed, currently using totals
    initial_capex = (
        costs[f"Total capex {tech} (USD/kW)"].to_frame().rename(columns={f"Total capex {tech} (USD/kW)": base_yr})
    )
    initial_capex = initial_capex.reindex(capex_projection.index, level="Country")
    capex_projection.loc[:, base_yr] = initial_capex.values

    # Project CAPEX using the learning curve
    for scenario in ssp_scenarios:
        for lr_scen in learning_rates.index:
            for country in countries:
                for i in range(1, len(years)):
                    year = years[i]
                    prev_year = years[i - 1]
                    capex_0_ = capex_projection.loc[pd.IndexSlice[country, scenario, lr_scen], prev_year]
                    capacity_0_ = capacity_projections.loc[(country, scenario), prev_year]
                    capacity_t_ = capacity_projections.loc[(country, scenario), year]
                    capex_t = update_capex_using_learning_curve(
                        capacity_0_, capacity_t_, capex_0_, LEARNING_RATES.loc[lr_scen][tech]
                    )
                    capex_projection.loc[pd.IndexSlice[country, scenario, lr_scen], year] = capex_t

    return capex_projection


def calculate_yearly_generated_electricity_in_lifetime(
    capacity_factor: float, lifetime: int, deterioration_rate: float
) -> list[float]:
    """
    Calculate the yearly generated electricity in MWh by 1 MW os installed capacity over its lifetime, taking into account its
    deterioration; 8760 = hours in a year (24 h/day x 365 days/year).
    Inputs:
        capacity_factor: ratio between total generated electricity and total electricity we could potentially generate
        if all installed capacity was running at its fullest (%).
        years: list of years in the lifetime of the technology.
        deterioration_rate: rate at which the capacity deteriorates with each year that passes by (%).
    """
    generated_electricity: list[float] = []
    # Initialize full capacity and actual capacity arrays
    full_capacity = [1.0] * lifetime
    actual_capacity = full_capacity.copy()

    # Calculate actual capacity with deterioration
    for i in range(1, lifetime):  # No deterioration in the first year
        actual_capacity[i] = actual_capacity[i - 1] * (1 - deterioration_rate)

    # Calculate generated electricity for each year
    for year in range(lifetime):
        # TODO: Move 8760 to global vars
        generated_electricity.append(actual_capacity[year] * capacity_factor * 8760)

    return generated_electricity


def calculate_lcoe(
    generated_electricity: list[float],
    fixed_opex_percentage: float,
    cost_of_capital: float,
    capex_0: float,
    capex_t: list[float] | None = None,
    curtailment: list[float] | None = None,
) -> float:
    """
    Calculate the Levelized Cost of Electricity (LCOE) in USD/MWh.
    lcoe = (capex_0 + sum_t(fixed_opex_percentage * capex_t / (1 + cost_of_capital)^t)) /
            sum_t((generated_electricity_t * (1 - curtailment_t)) / (1 + cost_of_capital)^t))
    Notes:
        1. sum_t from t = 1 to T, where T is the number of years in the lifetime of the technology. t=0 (investment time)
        corresponds to CAPEX_0 and generated electricity = 0.
        2. Can be calculated without absolute capacity values, since it cancels out anyways (set capacity to 1 MW and use
        CAPEX per MW).

    Inputs:
        generated_electricity: Electricity generated per timestep in MW.
        capex_0: Initial capital expenditure (CAPEX) in USD/MW.
        fixed_opex_percentage: Fixed OPEX as a percentage of CAPEX in %.
        cost_of_capital: Discount rate (r) in % (risk aversion, discount gets higher with time as uncertainty increases).
        curtailment: Curtailment rate per timestep in %.

    Output:
        lcoe: Levelized Cost of Electricity (LCOE) in USD/MWh.
    """
    # Simplification depending on cases
    if not capex_t:
        capex_t = [capex_0] * len(generated_electricity)
    if not curtailment:
        curtailment = [0] * len(generated_electricity)
    years = range(len(generated_electricity))
    discount_factors = [
        (1 + cost_of_capital) ** (t + 1) for t in years
    ]  # (t + 1) since the index starts at 0 and t starts at 1
    # Numerator
    x = [capex_t[t] / discount_factors[t] for t in years]
    opex_proxy = fixed_opex_percentage * sum(x)
    numerator = capex_0 + opex_proxy
    # Denominator
    sold_electricity = [generated_electricity[t] * (1 - curtailment[t]) for t in years]
    discounted_electricity = [sold_electricity[t] / discount_factors[t] for t in years]
    denominator = sum(discounted_electricity)
    if denominator == 0:
        raise ZeroDivisionError("Denominator (discounted electricity) is 0, cannot divide by 0.")

    return numerator / denominator


def get_lcoe_across_all_dims(
    capacity_fact: pd.Series | pd.DataFrame,
    capex_projection: pd.DataFrame,
    cost: pd.DataFrame,
    learning_rates: pd.DataFrame,
    lifetime: int,
    deterioration: float,
    tech: str,
) -> pd.DataFrame:
    """
    Calculate the LCOE for all combinations of countries, scenarios, and learning rates and store it in a dataframe with a
    multiindex for those dimensions.
    """
    logging.info(f"Calculating LCOE for {tech}")
    # Correct units
    capex_projection_usdmw = capex_projection * 1000  # from USD/kW to USD/MW
    capex_columns = cost.columns[cost.columns.str.contains("capex")]
    cost_usdmw = cost.copy()
    cost_usdmw[capex_columns] = cost[capex_columns] * 1000  # from USD/kW to USD/MW
    cost_usdmw = cost_usdmw.rename(columns={col: str(col)[:-8] + "(USD/MW)" for col in capex_columns})

    # Initialize an empty dataframe to store the LCOE results
    countries = capex_projection.index.get_level_values("Country").unique()
    ssp_scenarios = capex_projection.index.get_level_values("Scenario").unique().sort_values()
    investment_years = list(
        capex_projection.columns[:-lifetime]
    )  # Select only years for which the whole lifetime can be calculated
    index = pd.MultiIndex.from_product(
        [countries, ssp_scenarios, learning_rates.index], names=["Country", "Scenario", "LR Scenario"]
    )
    lcoe = pd.DataFrame(index=index, columns=[investment_years])

    # Calculate the LCOE for all combinations of countries, scenarios, and learning rates
    # TODO: Speed up by reducing times stuff gets calculated (e.g., discount factors for each year, calculte only once for all 70 years, read from there). Lambda fct instead of for loop?
    for scenario in ssp_scenarios:
        for lr_scen in learning_rates.index:
            for country in countries:
                for investment_year in investment_years:
                    # Select the time horizon for LCOE calculation (years). The investment year (t=0) corresponds to CAPEX_0
                    # and generated electricity = 0, which is why it is excluded from the time steps.
                    years = range(int(investment_year) + 1, int(investment_year) + lifetime + 1)
                    generated_electricity = calculate_yearly_generated_electricity_in_lifetime(
                        capacity_fact.loc[country],
                        lifetime,
                        deterioration,
                    )
                    lcoe_value = calculate_lcoe(
                        generated_electricity,
                        cost_usdmw.loc[country, f"Opex {tech} (%)"],
                        cost_usdmw.loc[country, "Cost of capital (%)"],
                        capex_projection_usdmw.loc[(country, scenario, lr_scen), investment_year],
                        [capex_projection_usdmw.loc[(country, scenario, lr_scen), year] for year in years],
                    )
                    lcoe.loc[(country, scenario, lr_scen), investment_year] = lcoe_value
    return lcoe


# ----------------------------------------------------- MAIN -----------------------------------------------------
def execute_calculate_cost_of_renewables(
    country_region: dict, country_code: dict, country_irena: dict, lr: pd.DataFrame, life: dict, det_rate: dict
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Main function to project the LCOE of renewables (solar PV and onshore wind) at country level until 2100 minus their lifetime.
    """

    # Select base year - year of the "current" CAPEX and capacity data
    base_year = 2022

    # Load data
    raw_solar_capex, raw_wind_capex, raw_cost_data = load_cost_data(base_yr=base_year)
    raw_capacity_factors, raw_hist_capacity, raw_solar_capacity_ssp, raw_wind_capacity_ssp = load_capacity_data(
        base_yr=base_year
    )

    # Preprocess data
    countries = pd.DataFrame(list(country_region.keys()), columns=["Country"])
    cost_per_country = preprocess_cost_data(
        raw_solar_capex, raw_wind_capex, raw_cost_data, countries, country_region, country_code
    )
    capacity_factors = preprocess_capacity_factors(raw_capacity_factors)
    solar_capacity_now, wind_capacity_now = preprocess_historical_renewable_capacity(
        raw_hist_capacity, countries, country_irena
    )
    solar_capacity = correct_ssp_projections_with_current_capacity(
        solar_capacity_now, raw_solar_capacity_ssp, countries, COUNTRY_TO_SSP_REGION_MAP, base_year, "solar"
    )
    wind_capacity = correct_ssp_projections_with_current_capacity(
        wind_capacity_now, raw_wind_capacity_ssp, countries, COUNTRY_TO_SSP_REGION_MAP, base_year, "wind"
    )

    # Project CAPEX based on the learning curve
    solar_capex_projection = project_capex_across_all_dims(solar_capacity, cost_per_country, lr, base_year, "solar")
    wind_capex_projection = project_capex_across_all_dims(wind_capacity, cost_per_country, lr, base_year, "wind")

    # Calculate LCOE for solar and wind
    solar_lcoe = get_lcoe_across_all_dims(
        capacity_factors["Capacity factor solar (%)"],
        solar_capex_projection,
        cost_per_country,
        lr,
        life["solar"],
        det_rate["solar"],
        "solar",
    )
    solar_lcoe.replace([np.inf, -np.inf], np.nan, inplace=True)

    wind_lcoe = get_lcoe_across_all_dims(
        capacity_factors["Capacity factor wind (%)"],
        wind_capex_projection,
        cost_per_country,
        lr,
        life["wind"],
        det_rate["wind"],
        "wind",
    )
    wind_lcoe.replace([np.inf, -np.inf], np.nan, inplace=True)

    return solar_lcoe, wind_lcoe


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    solar_lcoe_, wind_lcoe_ = execute_calculate_cost_of_renewables(
        COUNTRY_TO_REGION_MAP,
        COUNTRY_TO_CODE_MAP,
        COUNTRY_TO_IRENA_MAP,
        LEARNING_RATES,
        LIFETIME,
        YEARLY_DETERIORATION_RATE,
    )
    logging.info(f"Solar LCOE: \n{solar_lcoe_}")
    logging.info(f"Wind LCOE: \n{wind_lcoe_}")
