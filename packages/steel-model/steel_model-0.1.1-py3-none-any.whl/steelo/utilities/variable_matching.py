from typing import Dict

# TECHNOLOGY GROUPINGS

MYPY_DICT_STR_LIST = Dict[str, list]

FURNACE_GROUP_DICT: MYPY_DICT_STR_LIST = {
    "blast_furnace": [
        "Avg BF-BOF",
        "BAT BF-BOF",
        "BAT BF-BOF_bio PCI",
        "BAT BF-BOF_H2 PCI",
        "BAT BF-BOF+CCUS",
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCU",
    ],
    "dri-bof": ["DRI-Melt-BOF", "DRI-Melt-BOF_100% zero-C H2", "DRI-Melt-BOF+CCUS"],
    "dri-eaf": [
        "DRI-EAF",
        "DRI-EAF_50% bio-CH4",
        "DRI-EAF_50% green H2",
        "DRI-EAF+CCUS",
        "DRI-EAF_100% green H2",
    ],
    "smelting_reduction": ["Smelting Reduction", "Smelting Reduction+CCUS"],
    "eaf-basic": ["EAF"],
    "eaf-advanced": ["Electrolyzer-EAF", "Electrowinning-EAF"],
    "ccs": [
        "BAT BF-BOF+BECCUS",
        "BAT BF-BOF+CCUS",
        "DRI-Melt-BOF+CCUS",
        "DRI-EAF+CCUS",
        "Smelting Reduction+CCUS",
    ],
    "ccu": ["BAT BF-BOF+CCU"],
}
FURNACE_GROUP_DICT["dri"] = FURNACE_GROUP_DICT["dri-bof"] + FURNACE_GROUP_DICT["dri-eaf"]
FURNACE_GROUP_DICT["eaf-all"] = FURNACE_GROUP_DICT["eaf-basic"] + FURNACE_GROUP_DICT["eaf-advanced"]
