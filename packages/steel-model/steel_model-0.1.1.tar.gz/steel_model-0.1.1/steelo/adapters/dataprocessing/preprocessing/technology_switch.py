import pandas as pd
from typing import Hashable


def read_and_prep_capex_data(path) -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """
    Reads the capex data and prepares it for further processing
    """
    # TODO: Might need updating at any point when new data comes in.
    process_design_matrix = pd.read_excel(path, sheet_name="Process step combinations", skiprows=1, index_col=0)
    process_design_matrix.replace("x", 1, inplace=True)
    process_design_matrix.set_index("Process step", inplace=True)
    process_design_matrix.loc["Casting"] = (
        process_design_matrix.loc[pd.Index(["BOF + Casting", "EAF + Casting"])].sum() > 0
    ).astype(int)
    process_design_matrix.index = process_design_matrix.index.str.replace(" + Casting", "")
    capex = pd.read_excel("~/Downloads/Data_collection_ultimate_steel.xlsx", sheet_name="CAPEX", skiprows=2, nrows=20)

    ncapex = capex.set_index("Process step")["Reference unit Capex for 1 Mt plant.1"].dropna()
    # Define the index as a list of strings
    index_values = [
        "Coke production",
        "Sinter production",
        "Pellets production",
        "Shaft Furnace",
        "EAF",
        "Electrolyzer",
        "ESF",
        "BOF",
        "BOF (Relining)",
        "BF",
        "BF (Relining)",
        "Smelting Furnace",
        "Casting",
        "Hot Strip Mill",
        "Oxygen generation",
        "Limestone use",
        "Electricity generation",
        "Steam generation",
        "Other equipment",
    ]
    # Assign the list to the index
    ncapex.index = pd.Index(index_values)
    return process_design_matrix, ncapex, ncapex / 2


def derive_capex_switch(
    process_design_matrix: pd.DataFrame, bf_capex: pd.Series, gf_capex: pd.Series
) -> dict[str | Hashable, dict[str, float]]:
    """
    Takes in dataframes of production process and capex of 1mt installation related to machinery and derives renovation and technology switch capex

    returns a dict that encodes the cost of switch from the technolgy: key to the considered technologies: value
    """
    capex_switch = {}
    for column in process_design_matrix:
        tech_stack = process_design_matrix[column]

        # Use axis parameter instead of "index" string
        # Convert tech_stack.values to Series for sub operation
        difference = process_design_matrix.sub(
            pd.Series(tech_stack.values, index=process_design_matrix.index), fill_value=0
        )
        result = ((difference == 0).mul(bf_capex, axis=0) + (difference == 1).mul(gf_capex, axis=0)).sum().copy()
        # Replace the string safely
        col_name = column
        if isinstance(col_name, str):
            col_name = col_name.replace("Avg ", "")
        capex_switch[col_name] = result.astype(float).round(2).to_dict()
    return capex_switch


def prepare_steel_iron_capex(process_design_matrix: pd.DataFrame, gf_capex: pd.Series) -> dict[str, float]:
    """
    Prepares the full greenfield cost of new furnace
    """

    gf = process_design_matrix.multiply(gf_capex, axis="index").sum()
    gf.index = gf.index.str.replace("Avg ", "")
    return gf.astype(float).round(2).to_dict()


def read_prep_capex_data(path):
    process, ncapex, bf_capex = read_and_prep_capex_data(path)
    full_greenfield = prepare_steel_iron_capex(process, ncapex)
    technology_switch_capex = derive_capex_switch(process, bf_capex, ncapex)
    return full_greenfield, technology_switch_capex


def main(capex_module_path, data_in_path):
    gf_data, switch_data = read_prep_capex_data(data_in_path)

    content = f"""
# Capex swith and full greenfield capex
TECH_SWITCH_CAPEX = {switch_data}
FULL_GREENFIELD_CAPEX = {gf_data}
    """
    with open(capex_module_path, "w") as file:
        file.write(content)


if __name__ == "__main__":
    main("src/steelo/domain/Capex.py", "~/Downloads/Data_collection_ultimate_steel.xlsx")
