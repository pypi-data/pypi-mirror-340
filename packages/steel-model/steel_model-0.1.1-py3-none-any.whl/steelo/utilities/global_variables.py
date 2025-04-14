import pandas as pd

# GEM data years
STEEL_PLANT_GEM_DATA_YEAR = 2024
PRODUCTION_GEM_DATA_YEARS = range(2019, 2023)

# Learning rates for solar and wind energy
# Based on previous Systemiq project
LEARNING_RATES = pd.DataFrame(
    {
        "solar": [0.334, 0.234, 0.134],
        "wind": [0.226, 0.146, 0.066],
    },
    index=["low cost", "average cost", "high cost"],
)

# Lifetime of solar PV and on-shore wind turbines
LIFETIME = {
    "solar": 30,  # IRENA https://energycentral.com/system/files/ece/nodes/451407/irena_end_of_life_management_solar_pv.pdf p. 11; other sources say 25 years
    "wind": 25,  # IRENA https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2017/Jun/IRENA_Leveraging_for_Onshore_Wind_Executive_Summary_2017.pdf p.20; other sources say 25 years
    "steel": 20,
}

# Deterioration rate the energy systems over their lifetime
# TODO: Look for better sources; currently using a rough estimate by Rafal
YEARLY_DETERIORATION_RATE = {
    "solar": 0.005,  # 0.5% per year
    "wind": 0.01,  # 1% per year
}


ENERGY_EMISSION_FACTORS = {
    "Thermal coal": 95 * 36,  # 95 kgCO2/GJ -> conversion to kgCO2/MWh
    "BF gas": 260 * 36,  # 260 kgCO2/GJ -> conversion to kgCO2/MWh
    "COG": 44 * 36,  # 44 kgCO2/GJ -> conversion to kgCO2/MWh
    "BOF gas": 192 * 36,  # 192 kgCO2/GJ -> conversion to kgCO2/MWh
    "Natural gas": 55 * 36,  # 55 kgCO2/GJ -> conversion to kgCO2/MWh
    "Plastic waste": 111 * 36,  # 111 kgCO2/GJ -> conversion to kgCO2/MWh
    "Electricity": 375,  # 375 gCO2/kWh
}

ACTIVE_STATUSES = ["operating", "operating pre-retirement"]
ANNOUNCED_STATUSES = ["announced", "construction"]

CAPACITY_LIMIT = 0.95

SIMULATION_START_YEAR = 2025
