"""Compile a list of hints based on the settings."""
import random
from re import U
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions

from randomizer.Lists.Item import NameFromKong
from randomizer.Lists.MapsAndExits import GetMapId
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.WrinklyHints import hints
from randomizer.Spoiler import Spoiler
from randomizer.Patching.UpdateHints import updateRandomHint
from randomizer.Lists.WrinklyHints import HintLocation, hints
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Transitions import Transitions


class Hint:
    """Hint object for Wrinkly hint text."""

    def __init__(
        self,
        *,
        hint="",
        important=True,
        priority=1,
        kongs=[Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky],
        repeats=1,
        base=False,
        keywords=[],
        permitted_levels=[Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon, Levels.FungiForest, Levels.CrystalCaves, Levels.CreepyCastle],
        subtype="joke",
        joke=False,
        joke_defined=False,
    ):
        """Create wrinkly hint text object."""
        self.kongs = kongs.copy()
        self.hint = hint
        self.important = important
        self.priority = priority
        self.repeats = repeats
        self.base = base
        self.used = False
        self.was_important = important
        self.original_repeats = repeats
        self.original_priority = priority
        self.keywords = keywords.copy()
        self.permitted_levels = permitted_levels.copy()
        self.subtype = subtype
        self.joke = base
        if joke_defined:
            self.joke = joke

    def use_hint(self):
        """Set hint as used."""
        if self.repeats == 1:
            self.used = True
            self.repeats = 0
        else:
            self.repeats -= 1
            self.priority += 1

    def downgrade(self):
        """Downgrade hint status."""
        self.important = False


hint_list = [
    Hint(hint="Did you know - Donkey Kong officially features in Donkey Kong 64.", important=False, base=True),
    Hint(hint="Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie.", important=False, base=True),
    Hint(hint="Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick.", important=False, base=True),
    Hint(hint="Tiny Kong is the youngest sister of Dixie Kong.", important=False, base=True),
    Hint(hint="Mornin.", important=False, base=True),
    Hint(hint="Lanky Kong is the only kong with no canonical relation to the main Kong family tree.", important=False, base=True),
    Hint(hint="Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64.", important=False, base=True),
    Hint(hint="Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64.", important=False, base=True),
    Hint(hint="Candy Kong does not appear in Jungle Japes or Fungi Forest.", important=False, base=True),
    Hint(hint="If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight.", important=False, base=True),
    Hint(hint="Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021.", important=False, base=True),
    Hint(hint="The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes.", important=False, base=True),
    Hint(hint="Chunky Kong is the brother of Kiddy Kong.", important=False, base=True),
    Hint(hint="Fungi Forest contains mushrooms.", important=False, base=True),
    Hint(hint="Igloos can be found in Crystal Caves.", important=False, base=True),
    Hint(hint="Frantic Factory has multiple floors where things can be found.", important=False, base=True),
    Hint(hint="Angry Aztec has so much sand, it's even in the wind.", important=False, base=True),
    Hint(hint="DK Isles does not have a key.", important=False, base=True),
    Hint(hint="You can find a rabbit in Fungi Forest and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a beetle in Angry Aztec and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a vulture in Angry Aztec.", important=False, base=True),
    Hint(hint="You can find an owl in Fungi Forest.", important=False, base=True),
    Hint(hint="To buy moves, you will need coins.", important=False, base=True),
    Hint(hint="You can change the music and sound effects volume in the sound settings on the main menu.", important=False, base=True),
    Hint(hint="Coin Hoard is a Monkey Smash game mode where players compete to collect the most coins.", important=False, base=True),
    Hint(hint="Capture Pad is a Monkey Smash game mode where players attempt to capture pads in different corners of the arena.", important=False, base=True),
    Hint(hint="I have nothing to say to you.", important=False, base=True),
    Hint(hint="I had something to tell you, but I forgot what it is.", important=False, base=True),
    Hint(hint="I don't know anything.", important=False, base=True),
    Hint(hint="I'm as lost as you are. Good luck!", important=False, base=True),
    Hint(hint="Wrinkly? Never heard of him.", important=False, base=True),
    Hint(
        hint="This is it. The peak of all randomizers. No other randomizer exists besides DK64 Randomizer where you can listen to the dk rap in its natural habitat while freeing Chunky Kong in Jungle Japes.",
        important=False,
        base=True,
    ),
    Hint(hint="Why do they call it oven when you of in the cold food of out hot eat the food?", important=False, base=True),
    Hint(hint="Wanna become famous? Buy followers, coconuts and donks at DK64Randomizer (DK64Randomizer . com)!", important=False, base=True),
    Hint(hint="What you gonna do, SpikeVegeta?", important=False, base=True),
]


def pushHintToList(hint: Hint):
    """Push hint to hint list."""
    hint_list.append(hint)


def resetHintList():
    """Reset hint list to default state."""
    for hint in hint_list:
        if not hint.base:
            hint_list.remove(hint)
        else:
            hint.used = False
            hint.important = hint.was_important
            hint.repeats = hint.original_repeats
            hint.priority = hint.original_priority


def compileHints(spoiler: Spoiler):
    """Push hints to hint list based on settings."""
    resetHintList()
    all_levels = [Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon, Levels.FungiForest, Levels.CrystalCaves, Levels.CreepyCastle]
    # K Rool Order
    if spoiler.settings.krool_phase_order_rando and len(spoiler.settings.krool_order) > 1:
        associated_hint = f"K. Rool order is {NameFromKong(spoiler.settings.krool_order[0])}"
        for x in range(len(spoiler.settings.krool_order)):
            if x != 0:
                associated_hint += f" then {NameFromKong(spoiler.settings.krool_order[x])}"
        hint_list.append(Hint(hint=associated_hint, repeats=2, kongs=spoiler.settings.krool_order.copy(), subtype="k_rool"))
    # K. Rool Moves
    kong_list = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
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
            "The kong who waddles in his overalls",
            "The kong who has a cold race with an insect",
            "The kong who lacks style, grace but not a funny face",
        ],
        ["The kong who likes jazz", "The kong who shoots K. Rool's tiny toes", "The kong who has ammo that is light as a feather", "The kong who can shrink in size"],
        [
            "The kong who is one hell of a guy",
            "The kong who can pick up boulders",
            "The kong who fights a blocky boss",
            "The kong who bows down to a dragonfly",
        ],
    ]
    level_list = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle", "Hideout Helm"]
    level_list_isles = ["Jungle Japes", "Angry Aztec", "Frantic Factory", "Gloomy Galleon", "Fungi Forest", "Crystal Caves", "Creepy Castle", "DK Isles"]
    level_cryptic = [
        [
            "The level with a localized storm",
            "The level with a dirt mountain",
            "The level which has two retailers and no race",
        ],
        ["The level with four vases", "The level with two kongs cages", "The level with a spinning totem"],
        ["The level with a toy production facility", "The level with a tower of blocks", "The level with a game from 1981", "The level where you need two quarters to play"],
        ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
        ["The level with only two retailers and two races", "The level where night can be acquired at will", "The level with a nocturnal tree dweller"],
        [
            "The level with two inches of water",
            "The level with two ice shields",
            "The level with an Ice Tomato",
        ],
        ["The level with battlements", "The level with a dungeon, ballroom and a library", "The level with drawbridge and a moat"],
        ["The timed level", "The level with no boss", "The level with no small bananas"],
    ]
    # Make Isles Versions
    level_cryptic_isles = level_cryptic.copy()
    level_cryptic_isles.remove(level_cryptic_isles[-1])
    level_cryptic_isles.append(["The hub world", "The world with DK's ugly mug on it", "The world with only a Cranky's Lab and Snide's HQ in it"])

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
                "move_type": 0,
                "move_index": 3,
                "level": 0,
                "shop": 0,
                "important": True,
            },
            {"name": "Mini Monkey", "name_cryptic": "Their first special move", "key": 0x01, "kong": 3, "move_type": 0, "move_index": 1, "level": 0, "shop": 0, "important": True},
            {
                "name": "Coconut Gun",
                "name_cryptic": "Their gun",
                "key": 0x21,
                "kong": 0,
                "move_type": 2,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": True,
            },
            {"name": "Chimpy Charge", "name_cryptic": "Their first special move", "key": 0x01, "kong": 1, "move_type": 0, "move_index": 1, "level": 0, "shop": 0, "important": True},
            {
                "name": "Gorilla Gone",
                "name_cryptic": "Their third special move",
                "key": 0x03,
                "kong": 4,
                "move_type": 0,
                "move_index": 3,
                "level": 0,
                "shop": 0,
                "important": True,
            },
            {
                "name": "Ponytail Twirl",
                "key": 0x02,
                "kong": 3,
                "move_type": 0,
                "move_index": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Baboon Blast",
                "key": 0x01,
                "kong": 0,
                "move_type": 0,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Strong Kong",
                "key": 0x02,
                "kong": 0,
                "move_type": 0,
                "move_index": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Gorilla Grab",
                "key": 0x03,
                "kong": 0,
                "move_type": 0,
                "move_index": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Rocketbarrel Boost",
                "key": 0x02,
                "kong": 1,
                "move_type": 0,
                "move_index": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Simian Spring",
                "key": 0x03,
                "kong": 1,
                "move_type": 0,
                "move_index": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Orangstand",
                "key": 0x01,
                "kong": 2,
                "move_type": 0,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Baboon Balloon",
                "key": 0x02,
                "kong": 2,
                "move_type": 0,
                "move_index": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Orangstand Sprint",
                "key": 0x03,
                "kong": 2,
                "move_type": 0,
                "move_index": 3,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Hunky Chunky",
                "key": 0x01,
                "kong": 4,
                "move_type": 0,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Primate Punch",
                "key": 0x02,
                "kong": 4,
                "move_type": 0,
                "move_index": 2,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Peanut Popguns",
                "key": 0x21,
                "kong": 1,
                "move_type": 2,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Grape Shooter",
                "key": 0x21,
                "kong": 2,
                "move_type": 2,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Feather Bow",
                "key": 0x21,
                "kong": 3,
                "move_type": 2,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Pineapple Launcher",
                "key": 0x21,
                "kong": 4,
                "level": 0,
                "move_type": 2,
                "move_index": 1,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Bongo Blast",
                "key": 0x41,
                "kong": 0,
                "move_type": 4,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Guitar Gazump",
                "key": 0x41,
                "kong": 1,
                "move_type": 4,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Trombone Tremor",
                "key": 0x41,
                "kong": 2,
                "move_type": 4,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Saxophone Slam",
                "key": 0x41,
                "kong": 3,
                "move_type": 4,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {
                "name": "Triangle Trample",
                "key": 0x41,
                "kong": 4,
                "move_type": 4,
                "move_index": 1,
                "level": 0,
                "shop": 0,
                "important": False,
            },
            {"name": "Slam Upgrade", "key": 0x12, "kong": 0, "move_type": 1, "move_index": 2, "level": 0, "shop": 0, "important": False, "shared": True},
            {"name": "Homing Ammo", "key": 0x22, "kong": 0, "move_type": 2, "move_index": 2, "level": 0, "shop": 0, "important": False, "shared": True},
            {"name": "Sniper Scope", "key": 0x23, "kong": 0, "move_type": 2, "move_index": 3, "level": 0, "shop": 0, "important": False, "shared": True},
            {"name": "Ammo Belt Upgrade", "key": 0x32, "kong": 0, "move_type": 3, "move_index": 2, "level": 0, "shop": 0, "important": False, "shared": True},
            {"name": "Instrument Upgrade", "key": 0x42, "kong": 0, "move_type": 4, "move_index": 2, "level": 0, "shop": 0, "important": False, "shared": True},
        ]
        shop_owners = ["Cranky", "Funky", "Candy"]
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
        for move in moves_of_importance:
            move["key"] = ((move["move_type"] & 7) << 5) + (((move["move_index"] - 1) & 3) << 3) + (move["kong"] & 7)
            move["purchase_kong"] = -1
            move["level"] = -1
            move["shop"] = -1
        shop_contains = {}
        for shop in range(3):
            for kong in range(5):
                for level in range(8):
                    for move in moves_of_importance:
                        if spoiler.move_data[shop][kong][level] == move["key"]:
                            move["level"] = level
                            move["shop"] = shop
                            move["purchase_kong"] = kong
                            if spoiler.settings.wrinkly_hints == "cryptic":
                                shop_level_name = f"{shop_owners[shop]}'s in {level}"
                            else:
                                shop_level_name = f"{level_list_isles[level]} {shop_owners[shop]}"
                            is_shared = False
                            if "shared" in move:
                                is_shared = move["shared"]
                            if shop_level_name in shop_contains:
                                if not is_shared:
                                    shop_contains[shop_level_name]["moves"].append(move["name"])
                                    shop_contains[shop_level_name]["kongs"].append(kong)
                            else:
                                kong_lst = [kong]
                                if is_shared:
                                    kong_lst = [Kongs.donkey, Kongs.diddy, Kongs.lanky, Kongs.tiny, Kongs.chunky]
                                shop_contains[shop_level_name] = {"moves": [move["name"]], "kongs": kong_lst.copy()}
        # All moves in a shop
        shop_contain_keys = list(shop_contains.keys())
        random.shuffle(shop_contain_keys)
        priority_barriers = [3, 6, 10]
        shop_priority = 1
        shop_importance = True
        for shop_index, shop in enumerate(shop_contain_keys):
            shop_name = shop
            if "'s in " in shop_name:
                level_index = int(shop_name.split("'s in ")[1].strip())
                shop_name = random.choice(level_cryptic_isles[level_index])
            if len(shop_contains[shop]["moves"]) > 2:
                item_names = ", ".join(shop_contains[shop]["moves"][:-1])
                item_names = f"{item_names} and {shop_contains[shop]['moves'][-1]}"
            elif len(shop_contains[shop]["moves"]) == 2:
                item_names = " and ".join(shop_contains[shop]["moves"])
            else:
                item_names = shop_contains[shop]["moves"][0]
            hint_list.append(
                Hint(
                    hint=f"{shop_name} contains {item_names}",
                    priority=shop_priority,
                    important=shop_importance,
                    kongs=shop_contains[shop]["kongs"],
                    keywords=shop_contains[shop]["moves"],
                    subtype="shop_dump",
                )
            )
            if shop_importance:
                hint_list.append(Hint(hint=f"{shop_name} contains {item_names}", important=False, kongs=shop_contains[shop]["kongs"], keywords=shop_contains[shop]["moves"], subtype="shop_dump"))
            if shop_priority <= len(priority_barriers):
                if (shop_index + 1) >= priority_barriers[shop_priority - 1]:
                    if shop_priority == len(priority_barriers):
                        shop_importance = False
                    else:
                        shop_priority += 1

        for move in moves_of_importance:
            if move["level"] > -1 and move["shop"] > -1 and move["purchase_kong"] > -1:
                if spoiler.settings.wrinkly_hints == "cryptic":
                    kong_name = random.choice(kong_cryptic[move["purchase_kong"]])
                    level_name = random.choice(level_cryptic[move["level"]])
                else:
                    kong_name = kong_list[move["purchase_kong"]]
                    level_name = level_list[move["level"]]
                move_name = move["name"]

                shop_name = shop_owners[move["shop"]]
                text = f"{move_name} can be purchased from {shop_name} in {level_name}."
                hint_list.append(Hint(hint=text, priority=2, kongs=[move["purchase_kong"]], important=move["important"], keywords=[move["name"]], subtype="move_location"))
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
            free_kong = kong_json[kong_map["name"]]["puzzle"]["kong"]
            level_index = kong_map["level"]
            if spoiler.settings.wrinkly_hints == "cryptic":
                if not kong_index == Kongs.any:
                    kong_name = random.choice(kong_cryptic[kong_index])
                level_name = random.choice(level_cryptic[level_index])
            else:
                if not kong_index == Kongs.any:
                    kong_name = kong_list[kong_index]
                level_name = level_list[level_index]
            hint_priority = 2
            if kong_index == Kongs.any:
                kong_name = "An empty cage"
                hint_priority = 3
            hint_list.append(Hint(hint=f"{kong_name} can be found in {level_name}.", kongs=[free_kong], priority=hint_priority, subtype="kong_location"))
    if spoiler.settings.random_patches:
        level_patches = {
            "DK Isles": 0,
            "Jungle Japes": 0,
            "Angry Aztec": 0,
            "Frantic Factory": 0,
            "Gloomy Galleon": 0,
            "Fungi Forest": 0,
            "Crystal Caves": 0,
            "Creepy Castle": 0,
        }
        for patch in spoiler.dirt_patch_placement:
            for level in level_patches:
                if level in patch:
                    level_patches[level] += 1
        level_ordering = list(level_patches.keys())
        random.shuffle(level_ordering)
        for importance in range(2):
            for index in range(4):
                level_name = level_ordering[index + (4 * importance)]
                patch_count = level_patches[level_name]
                if patch_count > 0:
                    patch_mult = "patches"
                    patch_pre = "are"
                    if patch_count == 1:
                        patch_mult = "patch"
                        patch_pre = "is"
                    patch_text = f"There {patch_pre} {patch_count} {patch_mult} in {level_name}"
                    hint_list.append(Hint(hint=patch_text, priority=index + 3, important=False, subtype="level_patch_count"))
        patch_list = spoiler.dirt_patch_placement.copy()
        random.shuffle(patch_list)
        for importance in range(2):
            for index in range(4):
                patch_name = patch_list[index + (importance * 4)]
                patch_text = f"There is a dirt patch located at {patch_name}"
                hint_list.append(Hint(hint=patch_text, priority=index + 4, important=importance == 0, subtype="patch_location"))
    if spoiler.settings.shuffle_loading_zones == "all":
        AddLoadingZoneHints(spoiler)
    if spoiler.settings.coin_door_open == "need_both" or spoiler.settings.coin_door_open == "need_rw":
        hint_list.append(Hint(hint=f"{spoiler.settings.medal_requirement} medals are required to access Jetpac.", priority=4, subtype="medal"))
    if spoiler.settings.perma_death:
        hint_list.append(Hint(hint="The curse can only be removed upon disabling K. Rools machine.", subtype="permadeath"))
    if spoiler.settings.level_randomization != "level_order":
        for x in spoiler.settings.krool_keys_required:
            key_index = x - 4
            if spoiler.settings.wrinkly_hints == "cryptic":
                level_name = random.choice(level_cryptic[key_index])
            else:
                level_name = level_list[key_index]
            hint_list.append(Hint(hint=f"You will need to obtain the key from {level_name} to fight your greatest foe.", important=False, subtype="key_is_required"))
    # Way of the Hoard hints
    shopNames = ["Candy", "Funky", "Cranky"]
    moveSpecificSuffixes = [" Donkey", " Diddy", " Lanky", " Tiny", " Chunky", " Shared"]
    wothLocations = [key for key in spoiler.woth.keys() if any(shopName in key for shopName in shopNames)]
    selectedWothLocations = random.sample(wothLocations, min(5, len(wothLocations)))
    wothPriority = random.randint(1, 4)
    for wothLocation in selectedWothLocations:
        suffix = [specificSuffix for specificSuffix in moveSpecificSuffixes if specificSuffix in wothLocation]
        if len(suffix) > 0:
            wothHint = str(wothLocation).removesuffix(suffix[0])
        hint_list.append(Hint(hint=f"{wothHint} is on the Way of the Hoard.", important=random.choice([True, True, False]), priority=wothPriority, subtype="way_of_the_hoard"))
        wothPriority += random.randint(1, 2)

    # PADDED HINTS
    cb_list = [
        {"kong": "Donkey", "color": "Yellow"},
        {"kong": "Diddy", "color": "Red"},
        {"kong": "Lanky", "color": "Blue"},
        {"kong": "Tiny", "color": "Purple"},
        {"kong": "Chunky", "color": "Green"},
    ]
    # hint_list.append(Hint(hint=f"Your seed is {spoiler.settings.seed}")
    hint_list.append(Hint(hint=f"You can find bananas in {level_list[random.randint(0,6)]}, but also in other levels.", important=False, subtype="joke", joke=True, joke_defined=True))
    cb_hint = random.choice(cb_list)
    hint_list.append(Hint(hint=f"{cb_hint['kong']} can find {cb_hint['color']} bananas in {random.choice(level_list)}.", important=False, subtype="joke", joke=True, joke_defined=True))
    hint_list.append(Hint(hint=f"{spoiler.settings.krool_key_count} Keys are required to reach K. Rool.", important=False, subtype="key_count_required"))

    if spoiler.settings.shuffle_loading_zones == "levels":

        lobby_entrance_order = {
            Transitions.IslesMainToJapesLobby: Levels.JungleJapes,
            Transitions.IslesMainToAztecLobby: Levels.AngryAztec,
            Transitions.IslesMainToFactoryLobby: Levels.FranticFactory,
            Transitions.IslesMainToGalleonLobby: Levels.GloomyGalleon,
            Transitions.IslesMainToForestLobby: Levels.FungiForest,
            Transitions.IslesMainToCavesLobby: Levels.CrystalCaves,
            Transitions.IslesMainToCastleLobby: Levels.CreepyCastle,
        }
        lobby_exit_order = {
            Transitions.IslesJapesLobbyToMain: Levels.JungleJapes,
            Transitions.IslesAztecLobbyToMain: Levels.AngryAztec,
            Transitions.IslesFactoryLobbyToMain: Levels.FranticFactory,
            Transitions.IslesGalleonLobbyToMain: Levels.GloomyGalleon,
            Transitions.IslesForestLobbyToMain: Levels.FungiForest,
            Transitions.IslesCavesLobbyToMain: Levels.CrystalCaves,
            Transitions.IslesCastleLobbyToMain: Levels.CreepyCastle,
        }
        level_positions = {}
        level_order = {}
        shuffled_level_list = []
        for transition, vanilla_level in lobby_entrance_order.items():
            shuffled_level = lobby_exit_order[spoiler.shuffled_exit_data[transition].reverse]
            level_positions[shuffled_level] = vanilla_level
            level_order[vanilla_level] = shuffled_level
    if spoiler.settings.randomize_blocker_required_amounts is True and spoiler.settings.shuffle_loading_zones == "levels":
        for i in list(level_order.values()):
            shuffled_level_list.append(i.name)
        for x in range(8):
            count = spoiler.settings.EntryGBs[x]
            gb_name = "Golden Bananas"
            if count == 1:
                gb_name = "Golden Banana"
            level_name = level_list[x]
            # current_level_position = level_positions.index(level_name)
            gb_importance = False
            permitted_levels = all_levels.copy()
            priority_level = x + 1
            if spoiler.settings.shuffle_loading_zones == "levels":
                if x != 7:
                    current_level_order = level_positions[x]
                    permitted_levels = []
                    for y in range(7):
                        if y < current_level_order:
                            permitted_levels.append(level_order[y])
                    if level_name.replace(" ", "") in shuffled_level_list[4:7]:
                        priority_level = 4
                        gb_importance = True
                if spoiler.settings.maximize_helm_blocker is False and x == 7:
                    priority_level = 1
                    gb_importance = True
            if spoiler.settings.wrinkly_hints == "cryptic":
                level_name = random.choice(level_cryptic[x])

            hint_list.append(
                Hint(
                    hint=f"The barrier to {level_name} can be cleared by obtaining {count} {gb_name}.",
                    important=gb_importance,
                    priority=priority_level,
                    permitted_levels=permitted_levels.copy(),
                    subtype="gb_amount",
                )
            )
    for x in range(7):
        count = spoiler.settings.BossBananas[x]
        cb_name = "Small Bananas"
        if count == 1:
            cb_name = "Small Banana"
        if spoiler.settings.wrinkly_hints == "cryptic":
            level_name = random.choice(level_cryptic[x])
        else:
            level_name = level_list[x]
        permitted_levels = all_levels.copy()
        if spoiler.settings.shuffle_loading_zones == "levels":
            current_level_order = level_positions[x]
            permitted_levels = []
            for y in range(7):
                if y <= current_level_order:
                    permitted_levels.append(level_order[y])
        hint_list.append(
            Hint(hint=f"The barrier to the boss in {level_name} can be cleared by obtaining {count} {cb_name}.", important=False, permitted_levels=permitted_levels.copy(), subtype="cb_amount")
        )
    # Write Hints
    hint_distro = {}
    # 1 Joke Hint
    joke_hints = []
    for hint in hint_list:
        if not hint.important and not hint.used and hint.joke:
            joke_hints.append(hint)
    random_joke_hint = random.choice(joke_hints)
    placed = False
    joke_hint_count = 0
    while not placed:
        placed = updateRandomHint(random_joke_hint.hint, random_joke_hint.kongs.copy(), random_joke_hint.keywords.copy(), random_joke_hint.permitted_levels.copy())
        if placed:
            random_joke_hint.use_hint()
            joke_hint_count += 1
            subtype = random_joke_hint.subtype
            if subtype in hint_distro:
                hint_distro[subtype] += 1
            else:
                hint_distro[subtype] = 1
            break
    # Important
    random.shuffle(hint_list)
    priority_level = 1
    no_important_hints = False
    important_hint_count = 0
    while not no_important_hints:
        found_important = False
        for hint in hint_list:
            if hint.important and hint.priority == priority_level and not hint.used and not hint.joke:
                found_important = True
                placed = updateRandomHint(hint.hint, hint.kongs.copy(), hint.keywords.copy(), hint.permitted_levels.copy())
                if placed:
                    hint.use_hint()
                    important_hint_count += 1
                    subtype = hint.subtype
                    if subtype in hint_distro:
                        hint_distro[subtype] += 1
                    else:
                        hint_distro[subtype] = 1
                else:
                    hint.downgrade()
        if not found_important:
            no_important_hints = True
        priority_level += 1
    # Unimportant
    joke_hints = []
    vacant_slots = 0
    for hint in hint_list:
        if not hint.important and not hint.used and not hint.joke:
            joke_hints.append(hint)
    for hint in hints:
        if hint.hint == "":
            vacant_slots += 1
    random.shuffle(joke_hints)
    unimportant_hint_count = 0
    error_hint_count = 0
    if vacant_slots > 0:
        slot = 0
        tries = 100
        usage_slot = 0
        while slot < vacant_slots:
            placed = False
            if not joke_hints[usage_slot].used:
                placed = updateRandomHint(joke_hints[usage_slot].hint, joke_hints[usage_slot].kongs, joke_hints[usage_slot].keywords.copy(), joke_hints[usage_slot].permitted_levels.copy())
            if placed:
                joke_hints[usage_slot].use_hint()
                unimportant_hint_count += 1
                subtype = joke_hints[usage_slot].subtype
                if subtype in hint_distro:
                    hint_distro[subtype] += 1
                else:
                    hint_distro[subtype] = 1
                slot += 1
            else:
                tries -= 1
            usage_slot += 1
            if usage_slot >= len(joke_hints):
                usage_slot = 0
            if tries == 0:
                for hint in hints:
                    if hint.hint == "":
                        hint.hint = "I have so little to tell you that this hint got placed here. If you see this, please report with your spoiler log in the bug reports channel in the DK64 Randomizer discord."
                        subtype = "error"
                        if subtype in hint_distro:
                            hint_distro[subtype] += 1
                        else:
                            hint_distro[subtype] = 1
                        error_hint_count += 1
                slot = vacant_slots
    UpdateSpoilerHintList(spoiler)
    return True


def AddLoadingZoneHints(spoiler: Spoiler):
    """Add hints for loading zone transitions and their destinations."""
    # One hint for each of the critical areas: Japes, Aztec, Factory
    criticalJapesRegions = [
        Regions.JungleJapesMain,
        Regions.JapesBeyondFeatherGate,
        Regions.TinyHive,
        Regions.JapesLankyCave,
        Regions.Mine,
    ]
    criticalAztecRegions = [
        Regions.AngryAztecStart,
        Regions.AngryAztecMain,
    ]
    criticalFactoryRegions = [
        Regions.FranticFactoryStart,
        Regions.ChunkyRoomPlatform,
        Regions.PowerHut,
        Regions.BeyondHatch,
        Regions.InsideCore,
    ]
    japesHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalJapesRegions]
    random.shuffle(japesHintEntrances)
    japesHintPlaced = False
    while len(japesHintEntrances) > 0:
        japesHinted = japesHintEntrances.pop()
        if TryAddingLoadingZoneHint(spoiler, japesHinted, 1, criticalJapesRegions):
            japesHintPlaced = True
            break
    if not japesHintPlaced:
        print("Japes LZR hint unable to be placed!")

    aztecHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalAztecRegions]
    random.shuffle(aztecHintEntrances)
    aztecHintPlaced = False
    while len(aztecHintEntrances) > 0:
        aztecHinted = aztecHintEntrances.pop()
        if TryAddingLoadingZoneHint(spoiler, aztecHinted, 1, criticalAztecRegions):
            aztecHintPlaced = True
            break
    if not aztecHintPlaced:
        print("Aztec LZR hint unable to be placed!")

    factoryHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalFactoryRegions]
    random.shuffle(factoryHintEntrances)
    factoryHintPlaced = False
    while len(factoryHintEntrances) > 0:
        factoryHinted = factoryHintEntrances.pop()
        if TryAddingLoadingZoneHint(spoiler, factoryHinted, 1, criticalFactoryRegions):
            factoryHintPlaced = True
            break
    if not factoryHintPlaced:
        print("Factory LZR hint unable to be placed!")

    # Three hints for any of these useful areas: Banana Fairy, Galleon, Fungi, Caves, Castle, Crypt, Tunnel
    usefulRegions = [
        [Regions.BananaFairyRoom],
        [
            Regions.GloomyGalleonStart,
            Regions.LighthouseArea,
            Regions.Shipyard,
        ],
        [
            Regions.FungiForestStart,
            Regions.GiantMushroomArea,
            Regions.MushroomLowerExterior,
            Regions.MushroomNightExterior,
            Regions.MushroomUpperExterior,
            Regions.MillArea,
        ],
        [
            Regions.CrystalCavesMain,
            Regions.IglooArea,
            Regions.CabinArea,
        ],
        [
            Regions.CreepyCastleMain,
            Regions.CastleWaterfall,
        ],
        [Regions.LowerCave],
        [Regions.UpperCave],
    ]
    hintedUsefulAreas = random.sample(usefulRegions, 3)
    for regions in hintedUsefulAreas:
        usefulHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in regions]
        random.shuffle(usefulHintEntrances)
        usefulHintPlaced = False
        while len(usefulHintEntrances) > 0:
            usefulHinted = usefulHintEntrances.pop()
            if TryAddingLoadingZoneHint(spoiler, usefulHinted, 3, regions):
                usefulHintPlaced = True
                break
        if not usefulHintPlaced:
            print(f"Useful LZR hint to {usefulHinted.name} unable to be placed!")

    # Remaining hints for any shuffled exits in the game
    # Restrict DK isles main areas from being hinted
    uselessDkIslesRegions = [
        Regions.IslesMain,
        Regions.IslesMainUpper,
    ]
    remainingTransitions = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId not in uselessDkIslesRegions]
    random.shuffle(remainingTransitions)
    remainingHintCount = 4
    for transition in remainingTransitions:
        if remainingHintCount == 0:
            break
        elif TryAddingLoadingZoneHint(spoiler, transition, 5):
            remainingHintCount -= 1
    if remainingHintCount > 0:
        print("Unable to place remaining LZR hints!")


def TryAddingLoadingZoneHint(spoiler: Spoiler, transition, useful_rating, disallowedRegions: list = None):
    """Try to write a hint for the given transition. If this hint is determined to be bad, it will return false and not place the hint."""
    if disallowedRegions is None:
        disallowedRegions = []
    pathToHint = transition
    # Don't hint entrances from dead-end rooms, follow the reverse pathway back until finding a place with multiple entrances
    if spoiler.settings.decoupled_loading_zones:
        while ShufflableExits[pathToHint].category is None:
            originPaths = [x for x, back in spoiler.shuffled_exit_data.items() if back.reverse == pathToHint]
            # In a few cases, there is no reverse loading zone. In this case we must keep the original path to hint
            if len(originPaths) == 0:
                break
            pathToHint = originPaths[0]
    # With coupled loading zones, never hint from a dead-end room, since it is forced to be coming from the same destination
    elif ShufflableExits[pathToHint].category is None:
        return False
    # Validate the region of the hinted entrance is not in disallowedRegions
    if ShufflableExits[pathToHint].region in disallowedRegions:
        return False
    # Validate the hinted destination is not the same as the hinted origin
    entranceMap = GetMapId(ShufflableExits[pathToHint].region)
    destinationMap = GetMapId(spoiler.shuffled_exit_data[transition].regionId)
    if entranceMap == destinationMap:
        return False
    entranceName = ShufflableExits[pathToHint].name
    destinationName: str = spoiler.shuffled_exit_data[transition].spoilerName
    fromExitName = destinationName.find(" from ")
    if fromExitName != -1:
        # Remove exit name from destination
        destinationName = destinationName[:fromExitName]
    pushHintToList(Hint(hint=f"If you're looking for {destinationName}, follow the path from {entranceName}.", priority=useful_rating, subtype="lzr"))
    return True


def UpdateSpoilerHintList(spoiler: Spoiler):
    """Write hints to spoiler object."""
    for hint in hints:
        if hint.kong != Kongs.any:
            spoiler.hint_list[hint.name] = hint.hint
