"""Compile a list of hints based on the settings."""
import random

from randomizer.Spoiler import Spoiler
from randomizer.UpdateHints import updateRandomHint


def compileHints(spoiler: Spoiler):
    """Push hints to hint list based on settings."""
    # K Rool Order
    kong_names = ["DK", "Diddy", "Lanky", "Tiny", "Chunky"]
    if spoiler.settings.k_rool_phase_order:
        associated_hint = f"K. Rool order is {kong_names[spoiler.settings.krool_order[0]]}"
        for x in range(len(spoiler.settings.krool_order)):
            if x != 0:
                associated_hint += f" then {kong_names[spoiler.settings.krool_order[x]]}"
        updateRandomHint(associated_hint)
    # K. Rool Moves
    if spoiler.settings.shuffle_items == "moves" and spoiler.move_data is not None:
        krool_move_requirements = [0, 2, 1, 1, 4]
        total_moves_for_krool = 0
        for x in spoiler.settings.krool_order:
            total_moves_for_krool += krool_move_requirements[x]
        moves_of_importance = [
            {
                "name": "Monkeyport",
                "name_cryptic": "Their third special move",
                "key": 0x03,
                "kong": 3,
                "level": 0,
                "shop": 0,
            },
            {"name": "Mini Monkey", "name_cryptic": "Their first special move", "key": 0x01, "kong": 3, "level": 0, "shop": 0},
            {
                "name": "Coconut Gun",
                "name_cryptic": "Their gun",
                "key": 0x21,
                "kong": 0,
                "level": 0,
                "shop": 0,
            },
            {"name": "Chimpy Charge", "name_cryptic": "Their first special move", "key": 0x01, "kong": 1, "level": 0, "shop": 0},
            {
                "name": "Gorilla Gone",
                "name_cryptic": "Their third special move",
                "key": 0x03,
                "kong": 4,
                "level": 0,
                "shop": 0,
            },
        ]
        kong_cryptic = [
            [
                "The kong who is bigger, faster and potentially stronger too",
                "The kong who fires in spurts",
                "The kong with a tie",
                "The kong who slaps their instrument to the jungle beat",
            ],
            [
                "The kong who can fly real high",
                "The kong who features in the first two Donkey Kong Country games",
                "The kong who wants to see red",
                "The kong who frees the only female playable kong",
            ],
            [
                "The kong who inflates like a balloon, just like a balloon",
                "The kong who waddles in his dungarees",
                "The kong who has a cold race with an insect",
                "The kong who shares a home with a thirsty dweller",
            ],
            ["The kong who likes jazz", "The kong who shoots K. Rool's tiny toes", "The kong who has ammo that is light as a feather", "The kong who can shrink in size"],
            [
                "The kong who is one hell of a guy",
                "The kong who can pick up boulders",
                "The kong who fights a blocky boss",
                "The kong who bows down to a dragonfly",
            ],
        ]
        level_cryptic = [
            [
                "The level with a localized storm",
                "The level with a dirt mountain",
                "The level which has two retailers and no race",
            ],
            ["The level with sporadic gusts of sand", "The level with two kongs to free", "The level who is home to a humped animal"],
            [
                "The level with a toy production facility",
                "The level with a tower of blocks",
                "The level with Cranky and Candy adjacent to each other",
            ],
            ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
            ["The level with only two retailers and two races", "The level where night can be acquired at will", "The level with a nocturnal tree dweller"],
            [
                "The level where it rains rocks",
                "The level with two ice shields",
                "The level with a tile-flipping minigame",
            ],
            ["The level with constant rain", "The level with a dungeon, ballroom and a library", "The level with drawbridge and a moat"],
        ]
        shop_cryptic = [
            [
                "The shop owner with a walking stick",
                "The shop owner who is old",
                "The shop owner who is persistently grumpy",
                "The shop owner who resides near your Treehouse",
            ],
            [
                "The shop owner who has an armory",
                "The shop owner who has a banana on his shop",
                "The shop owner with sunglasses",
                "The shop owner who calls everyone Dude",
            ],
            ["The shop owner who is flirtatious", "The shop owner who is not present in Fungi Forest", "The shop owner who is not present in Jungle Japes", "The shop owner with blonde hair"],
        ]
        for shop in range(3):
            for kong in range(5):
                for level in range(7):
                    for move in moves_of_importance:
                        if spoiler.move_data[shop][kong][level] == move["key"] and kong == move["kong"]:
                            move["level"] = level
                            move["shop"] = shop
        for move in moves_of_importance:
            kong_name = random.choice(kong_cryptic[move["kong"]])
            move_name = move["name_cryptic"]
            level_name = random.choice(level_cryptic[move["level"]])
            shop_name = random.choice(shop_cryptic[move["shop"]])
            updateRandomHint(f"{kong_name} can purchase {move_name} in {level_name} from {shop_name}")

    # How to reach Japes, Factory, Banana Fairy (Rare)
