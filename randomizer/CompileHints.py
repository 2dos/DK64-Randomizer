"""Compile a list of hints based on the settings."""
import random

from randomizer.Lists.Item import NameFromKong
from randomizer.Spoiler import Spoiler
from randomizer.UpdateHints import updateRandomHint


def compileHints(spoiler: Spoiler):
    """Push hints to hint list based on settings."""
    # K Rool Order
    if spoiler.settings.k_rool_phase_order:
        associated_hint = f"K. Rool order is {NameFromKong(spoiler.settings.krool_order[0])}"
        for x in range(len(spoiler.settings.krool_order)):
            if x != 0:
                associated_hint += f" then {NameFromKong(spoiler.settings.krool_order[x])}"
        updateRandomHint(associated_hint)
    padded_hints = [
        "Did you know - Donkey Kong officially features in Donkey Kong 64",
        "Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie",
        "Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick",
        "Tiny Kong is the youngest sister of Dixie Kong",
        "Mornin",
        "Lanky Kong is the only kong with no canonical relation to the main Kong family tree",
        "Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64",
        "Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64",
        "Candy Kong does not appear in Jungle Japes or Fungi Forest",
        "If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight",
        "Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021",
        "The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes",
        "Chunky Kong is the brother of Kiddy Kong",
        "Fungi Forest contains mushrooms.",
        "Igloos can be found in Crystal Caves.",
        "Frantic Factory has multiple floors where things can be found.",
        "Angry Aztec has so much sand, it's even in the wind.",
        "DK Isles does not have a key.",
        "You can find a rabbit in Fungi Forest and in Crystal Caves.",
        "You can find a beetle in Angry Aztec and in Crystal Caves.",
        "You can find a vulture in Angry Aztec.",
        "You can find an owl in Fungi Forest.",
        "To buy moves, you will need coins.",
        "You can change the music and sound effects volume in the sound settings on the main menu.",
        "Coin Hoard is a Monkey Smash game mode where players compete to collect the most coins.",
        "Capture Pad is a Monkey Smash game mode where players attempt to capture pads in different corners of the arena.",
        "I have nothing to say to you.",
        "I had something to tell you, but I forgot what it is.",
        "I don't know anything.",
        "I'm as lost as you are. Good luck!",
        "Wrinkly? Never heard of him.",
    ]
    # K. Rool Moves
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
        ["The timed level", "The level with no boss", "The level with no small bananas"],
    ]
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
                "important": True,
            },
            {"name": "Mini Monkey", "name_cryptic": "Their first special move", "key": 0x01, "kong": 3, "level": 0, "shop": 0, "important": True},
            {
                "name": "Coconut Gun",
                "name_cryptic": "Their gun",
                "key": 0x21,
                "kong": 0,
                "level": 0,
                "shop": 0,
                "important": True,
            },
            {"name": "Chimpy Charge", "name_cryptic": "Their first special move", "key": 0x01, "kong": 1, "level": 0, "shop": 0, "important": True},
            {
                "name": "Gorilla Gone",
                "name_cryptic": "Their third special move",
                "key": 0x03,
                "kong": 4,
                "level": 0,
                "shop": 0,
                "important": True,
            },
            {
                "name": "Ponytail Twirl",
                "key": 0x02,
                "kong": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Baboon Blast",
                "key": 0x01,
                "kong": 0,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Strong Kong",
                "key": 0x02,
                "kong": 0,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Gorilla Gone",
                "key": 0x03,
                "kong": 0,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Rocketbarrel Boost",
                "key": 0x02,
                "kong": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Simian Spring",
                "key": 0x03,
                "kong": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Orangstand",
                "key": 0x01,
                "kong": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Baboon Balloon",
                "key": 0x02,
                "kong": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Orangstand Sprint",
                "key": 0x03,
                "kong": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Hunky Chunky",
                "key": 0x01,
                "kong": 4,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Primate Punch",
                "key": 0x02,
                "kong": 4,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Peanut Popguns",
                "key": 0x21,
                "kong": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Grape Shooter",
                "key": 0x21,
                "kong": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Feather Bow",
                "key": 0x21,
                "kong": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Pineapple Launcher",
                "key": 0x21,
                "kong": 4,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Bongo Blast",
                "key": 0x41,
                "kong": 0,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Guitar Gazump",
                "key": 0x41,
                "kong": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Trombone Tremor",
                "key": 0x41,
                "kong": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Saxapone Slam",
                "key": 0x41,
                "kong": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Triangle Trample",
                "key": 0x41,
                "kong": 4,
                "level": 0,
                "shop": 0,
                "important": False,
            },
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
            move_name = move["name"]
            level_name = random.choice(level_cryptic[move["level"]])
            shop_name = random.choice(shop_cryptic[move["shop"]])
            text = f"{move_name} can be purchased in {level_name} from {shop_name}"
            if move["important"]:
                updateRandomHint(text)
            else:
                padded_hints.append(text)
    if spoiler.settings.kong_rando:
        kong_json = spoiler.shuffled_kong_placement
        placement_levels = [
            {
                "name": "Jungle Japes",
                "level": 0,
            },
            {
                "name": "Llama Temple",
                "level": 1,
            },
            {
                "name": "Tiny Temple",
                "level": 1,
            },
            {
                "name": "Frantic Factory",
                "level": 2,
            },
        ]
        for kong_map in placement_levels:
            kong_index = kong_json[kong_map["name"]]["locked"]["kong"]
            level_index = kong_map["level"]
            kong_name = random.choice(kong_cryptic[kong_index])
            level_name = random.choice(level_cryptic[level_index])
            updateRandomHint(f"{kong_name} can be found in {level_name}")
    if spoiler.settings.BananaMedalsRequired:
        updateRandomHint(f"{spoiler.settings.BananaMedalsRequired} medals are required to access Jetpac")
    if spoiler.settings.perma_death:
        updateRandomHint("The curse can only be removed upon disabling K. Rools machine")
    updateRandomHint(f"{spoiler.settings.krool_key_count} Keys are required to turn in K. Rool")
    if spoiler.settings.level_randomization != "level_order":
        for x in spoiler.settings.krool_keys_required:
            key_index = x - 4
            level_name = random.choice(level_cryptic[key_index])
            updateRandomHint(f"You will need to obtain the key from {level_name} to fight your greatest foe")
    for x in range(7):
        boss_map = spoiler.settings.boss_maps[x]
        level_name = random.choice(level_cryptic[x])
        if boss_map == 0xC7:
            updateRandomHint(f"The cardboard boss can be found in {level_name}")

    # PADDED HINTS
    level_list = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle"]
    cb_list = [
        {"kong": "Donkey", "color": "Yellow"},
        {"kong": "Diddy", "color": "Red"},
        {"kong": "Lanky", "color": "Blue"},
        {"kong": "Tiny", "color": "Purple"},
        {"kong": "Chunky", "color": "Green"},
    ]
    # padded_hints.append(f"Your seed is {spoiler.settings.seed}")
    padded_hints.append(f"You can find bananas in {random.choice(level_list)}, but also in other levels.")
    cb_hint = random.choice(cb_list)
    padded_hints.append(f"{cb_hint['kong']} can find {cb_hint['color']} bananas in {random.choice(level_list)}.")
    for x in range(8):
        count = spoiler.settings.EntryGBs[x]
        gb_name = "Golden Bananas"
        if count == 1:
            gb_name = "Golden Banana"
        level_name = random.choice(level_cryptic[x])
        padded_hints.append(f"The barrier to {level_name} can be cleared by obtaining {count} {gb_name}")
    for x in range(7):
        count = spoiler.settings.BossBananas[x]
        cb_name = "Small Bananas"
        if count == 1:
            cb_name = "Small Banana"
        level_name = random.choice(level_cryptic[x])
        padded_hints.append(f"The barrier to the boss in {level_name} can be cleared by obtaining {count} {cb_name}")
    padded_count = 35
    if len(padded_hints) < 35:
        padded_count = len(padded_hints)
    random.shuffle(padded_hints)
    for x in range(padded_count):
        updateRandomHint(padded_hints[x])

    # How to reach Japes, Factory, Banana Fairy (Rare)
