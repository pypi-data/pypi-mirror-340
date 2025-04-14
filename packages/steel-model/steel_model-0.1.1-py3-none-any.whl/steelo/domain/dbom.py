from ..utilities.utils import merge_dicts_bom


class Bill:
    """Base costs/bills related to non-dynamic input variables"""

    IO_mid = {"Value": 124.0, "Unit": "USD/t"}
    IO_high = {"Value": 130.2, "Unit": "USD/t"}
    Met_coal = {"Value": 328.3, "Unit": "USD/GJ"}
    Natural_gas = {"Value": 13.8, "Unit": "USD/GJ"}
    Scrap = {"Value": 344.5, "Unit": "USD/t"}
    Coal = {"Value": 130.0, "Unit": "USD/t"}
    Coking_coal = {"Value": 130.0, "Unit": "USD/t"}
    PCI = {"Value": 130.0, "Unit": "USD/t"}

    Burnt_lime = {"Value": 50.0, "Unit": "USD/t"}
    Burnt_dolomite = {"Value": 50.0, "Unit": "USD/t"}
    Slag = {"Value": 0.0, "Unit": "USD/t"}

    Electricity = {"Value": 0.235, "Unit": "USD/kWh"}
    Natural_gas = {"Value": 13.8, "Unit": "USD/GJ"}
    Hydrogen = {"Value": 35.211, "Unit": "USD/GJ"}

    @classmethod
    def add_additional_bill(cls, new_variable, variable_name):
        setattr(cls, variable_name, new_variable)

    @classmethod
    def to_dict(cls):
        return {key: value for key, value in cls.__dict__.items() if not key.startswith("__") and not callable(key)}


class DBOM:
    """Class for handling bill of materials generation from the dynamic business cases"""

    from steelo.domain.BOM import bom_data

    data = bom_data.copy()

    @classmethod
    def extract_input_values(cls, business_case, metallic_charge=None, reductant=None, share=1):
        # Convert None to slice(None) for wildcard matching
        query = tuple(
            param if param is not None else slice(None) for param in [business_case, metallic_charge, reductant]
        )

        def matches(key_tuple, query_tuple):
            return all((q == slice(None)) or (k == q) for k, q in zip(key_tuple, query_tuple))

        matched_row = {k[3:5]: v for k, v in cls.data.items() if matches(k, query) and k[3] in ["Materials", "Energy"]}

        return matched_row


def translate_input_variables_to_bom(materials, energy, additional_bills, bill=Bill):
    bill_of_materials = {}
    bill_of_energy = {}
    for key, value in materials.items():
        # print(key, value['Value'])
        if value["Value"] > 0:
            try:
                unit_cost = getattr(bill, key.replace(" ", "_"))
            except AttributeError:
                unit_cost = additional_bills[key.replace(" ", "_")]

            bill_of_materials[key] = {
                "demand": value["Value"],
                "unit_cost": unit_cost,
            }
    for key, value in energy.items():
        if key == "Flexible":
            key = "Natural gas"  # let all flexible energy for now be natural gas... for now
        if value["Value"] > 0:
            try:
                unit_cost = getattr(bill, key.replace(" ", "_"))
            except AttributeError:
                unit_cost = additional_bills[key.replace(" ", "_")]

            bill_of_energy[key] = {
                "demand": value["Value"],
                "unit_cost": unit_cost,
            }
    return {"materials": bill_of_materials, "energy": bill_of_energy}


def derive_single_cost(bom, bill=Bill):
    cost = 0
    for key, entry in bom.items():
        for mat, values in entry.items():
            cost += values["demand"] * values["unit_cost"]["Value"]
    return cost


def derive_unnested_feedstock_bom(architype, dbom=DBOM):  # TODO: fix the share thing
    _ = {}  # This is purely meant act as a placeholder to store the bom/unit

    for metallic_charge, items in architype.items():
        # cost for a given metallic charge respective to the current business case
        _input = dbom.extract_input_values(**items)
        materials = {k[1]: v for k, v in _input.items() if k[0] == "Materials"}
        energy = {k[1]: v for k, v in _input.items() if k[0] == "Energy"}

        bom = translate_input_variables_to_bom(materials, energy, _)
        _[f"{metallic_charge.replace(' ', '_')}_bom"] = bom
        # bill.add_additional_bill(bom, f"{metallic_charge.replace(' ', '_')}_{business_case}_bom")
        c = derive_single_cost(
            bom,
        )
        _[f"{metallic_charge.replace(' ', '_')}"] = {"Value": c, "Unit": "USD/t"}
        # bill.add_additional_bill({"Value": c, "Unit": "USD/t"}, f'{metallic_charge.replace(' ', '_')}_{business_case}')
    return _


def extract_steel(bom):
    bill_of = [v for k, v in bom.items() if k in ["Steel_bom", "Scrap_bom"]]
    # print(bill_of)
    if len(bill_of) > 1:
        bill_of_materials = merge_dicts_bom(bill_of)
        return bill_of_materials
    else:
        return bill_of[0]


class BusinessCaseArchitypes:
    """MVP Business case architypes"""

    steel_bof = {
        "Coke": dict(business_case="prep_coke"),
        "Pellets_mid": dict(business_case="prep_pellet", metallic_charge="IO_mid"),
        "Hot metal": dict(business_case="iron_bf", metallic_charge="Pellets_mid", reductant="Coke+PCI"),
        "Steel": dict(business_case="steel_bof", metallic_charge="Hot metal"),
    }

    steel_eaf = {
        "Scrap": dict(business_case="steel_eaf", metallic_charge="Scrap"),
    }
    dri_eaf = {
        "Pellets_high": dict(business_case="prep_pellet", metallic_charge="IO_high"),
        "DRI_high": dict(business_case="iron_dri", metallic_charge="Pellets_high", reductant="Natural gas"),
        "Steel": dict(business_case="steel_eaf", metallic_charge="DRI_high"),
    }

    # h2_dri_eaf_architype = {
    #     "Pellets_high": dict(business_case="prep_pellet", metallic_charge="IO_high"),
    #     "DRI_high": dict(business_case="iron_dri", metallic_charge="Pellets_high", reductant="Hydrogen"),
    #     "Steel": dict(business_case="steel_eaf", metallic_charge="DRI_high"),
    # }

    @classmethod
    def get_all(cls):
        return {
            "BF-BOF": cls.steel_bof_architype,
            "EAF": cls.steel_eaf_architype,
            "DRI-EAF": cls.ng_dri_eaf_architype,
        }

    @classmethod
    def get_architype(cls, key):
        if key == "BF-BOF":
            return cls.steel_bof
        elif key == "EAF":
            return cls.steel_eaf
        elif key == "DRI-EAF":
            return cls.dri_eaf
        else:
            return None
