import json
from randomizer.Lists.Location import LocationListOriginal
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.WrinklyHints import boss_names
from randomizer.Lists.Item import ItemList
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Types import Types
from randomizer.Enums.Items import Items
from randomizer.Enums.Levels import Levels

def genJSON():
    output = {
        "grouped": [
            "locations",
        ],
        "locations": {},
        "transitions": {},
        "levels": {},
        "bosses": {},
        "kongs": {},
        "item_list": {},
    }
    # Gen dictionaries
    location_gb_mapping = {
        Levels.JungleJapes: "Japes",
        Levels.AngryAztec: "Aztec",
        Levels.FranticFactory: "Factory",
        Levels.GloomyGalleon: "Galleon",
        Levels.FungiForest: "Forest",
        Levels.CrystalCaves: "Caves",
        Levels.CreepyCastle: "Castle",
        Levels.DKIsles: "Isles",
    }
    type_mapping = {
        Types.Fairy: "Fairies",
        Types.Key: "Bosses",
        Types.IslesMedal: "Medal Checks",
        Types.Medal: "Medal Checks",
        Types.HalfMedal: "Half-Medal Checks",
        Types.Shop: "Shops",
        Types.Blueprint: "Kasplat Checks",
        Types.BlueprintBanana: "Snide Rewards",
        Types.Enemies: "Dropsanity",
        Types.Crown: "Battle Arena Checks",
        Types.Hint: "Hint Doors",
        Types.RainbowCoin: "Dirt Patches",
        Types.CrateItem: "Melon Crates",
        Types.BoulderItem: "Holdables",
    }
    for enum_val, location in LocationListOriginal.items():
        if location.type in (Types.EnemyPhoto, Types.ProgressiveHint, Types.PreGivenMove, Types.Cranky, Types.Candy, Types.Snide, Types.Funky, Types.Climbing, Types.TrainingBarrel, Types.Constant):
            continue
        cat = "Misc"
        if location.type == Types.Banana and location.level in location_gb_mapping:
            cat = f"{location_gb_mapping[location.level]} GB Checks"
        elif location.type in type_mapping:
            cat = type_mapping[location.type]
        if cat not in output["locations"]:
            output["locations"][cat] = {}
        output["locations"][cat][enum_val.name] = location.name
    for enum_val, transition in ShufflableExits.items():
        output["transitions"][enum_val.name] = transition.name
    for enum_val, boss_name in boss_names.items():
        output["bosses"][enum_val.name] = boss_name
    for enum_val, item_data in ItemList.items():
        if item_data.type in (Types.Constant, Types.EnemyPhoto, Types.ArchipelagoItem):
            continue
        if enum_val in (Items.JunkCrystal, Items.JunkAmmo, Items.JunkFilm, Items.JunkOrange, Items.CrateMelon, Items.HalfMedal, Items.BoulderItem, Items.EnemyItem):
            continue
        if enum_val >= Items.JungleJapesDonkeyBlueprint and enum_val <= Items.DKIslesChunkyBlueprint:
            continue
        output["item_list"][enum_val.name] = item_data.name
    for member in Kongs:
        if member.name == "any":
            continue
        output["kongs"][member.name] = f"{member.name.title()} Kong"
    levels = [
        "Jungle Japes",
        "Angry Aztec",
        "Frantic Factory",
        "Gloomy Galleon",
        "Fungi Forest",
        "Crystal Caves",
        "Creepy Castle",
        "Hideout Helm",
    ]
    for level in levels:
        output["levels"][level.replace(" ", "")] = level

    # Write to file
    with open("static/presets/plandomizer/data.json", "w", encoding="utf-8") as fh:
        json.dump(output, fh, indent=4)

genJSON()