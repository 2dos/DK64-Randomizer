"""Compile a list of hints based on the settings."""

from __future__ import annotations

import json
import random
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Tuple, Union
from randomizer.Enums.MoveTypes import MoveTypes

import randomizer.ItemPool as ItemPool
from randomizer.Enums.Events import Events
from randomizer.Enums.HintType import HintType
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import HelmDoorItem, HelmSetting, LogicType, MicrohintsEnabled, MoveRando, ShockwaveStatus, ShuffleLoadingZones, SpoilerHints, WinCondition, WrinklyHints
from randomizer.Enums.Types import Types
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import PreGivenLocations, SharedShopLocations, TrainingBarrelLocations
from randomizer.Lists.MapsAndExits import GetMapId
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.WrinklyHints import ClearHintMessages, hints
from randomizer.Patching.UpdateHints import UpdateHint

if TYPE_CHECKING:
    from randomizer.Enums.Transitions import Transitions
    from randomizer.Lists.WrinklyHints import HintLocation
    from randomizer.LogicClasses import Region
    from randomizer.Spoiler import Spoiler


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
    ) -> None:
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


class MoveInfo:
    """Move Info for Wrinkly hint text."""

    def __init__(self, *, name="", kong="", move_type="", move_level=0, important=False) -> None:
        """Create move info object."""
        self.name = name
        self.kong = kong
        move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
        encoded_move_type = move_types.index(move_type)
        self.move_type = encoded_move_type
        self.move_level = move_level
        self.important = important
        ref_kong = kong
        if ref_kong == Kongs.any:
            ref_kong = Kongs.donkey
        self.item_key = {"move_type": move_type, "move_lvl": move_level - 1, "move_kong": ref_kong}


class StartingSpoiler:
    """Spoiler for overall seed info you need to know at the start."""

    def __init__(self, settings):
        """Create starting info spoiler with the seed settings."""
        self.krool_order = settings.krool_order.copy()
        self.helm_order = settings.kong_helm_order.copy()
        self.starting_kongs = settings.starting_kong_list.copy()
        self.starting_keys = [ItemList[key].name for key in settings.starting_key_list]
        if settings.spoiler_include_level_order:
            self.level_order = [
                settings.level_order[1],
                settings.level_order[2],
                settings.level_order[3],
                settings.level_order[4],
                settings.level_order[5],
                settings.level_order[6],
                settings.level_order[7],
            ]

    def toJSON(self):
        """Convert this object to JSON for the purposes of the spoiler log."""
        return json.dumps(self, default=lambda o: o.__dict__)


class LevelSpoiler:
    """Spoiler for a given level in spoiler-style hints."""

    def __init__(self, level_name):
        """Create level spoiler object info."""
        self.level_name = level_name
        self.vial_colors = []
        self.points = 0
        self.woth_count = 0

    def toJSON(self):
        """Convert this object to JSON for the purposes of the spoiler log."""
        return json.dumps(self, default=lambda o: o.__dict__)


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
    Hint(hint="You can find a rabbit in Fungi Forest and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a beetle in Angry Aztec and in Crystal Caves.", important=False, base=True),
    Hint(hint="You can find a vulture in Angry Aztec.", important=False, base=True),
    Hint(hint="You can find an owl in Fungi Forest.", important=False, base=True),
    Hint(hint="You can find two boulders in Jungle Japes", important=False, base=True),
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
    Hint(hint="You don't care? Just give it to me? Okay, here it is.", important=False, base=True),
    Hint(hint="Rumor has it this game was developed in a cave with only a box of scraps!", important=False, base=True),
    Hint(hint="BOINNG! BOINNG! The current time is: 8:01!", important=False, base=True),
    Hint(hint="If you backflip right before Chunky punches K. Rool, you must go into first person camera to face him before the punch.", important=False, base=True),
    Hint(hint="The barrier to \x08Hideout Helm\x08 can be cleared by obtaining \x04801 Golden Bananas\x04. It can also be cleared with fewer than that.", important=False, base=True),
    Hint(hint="It would be \x05foolish\x05 to \x04not save your spoiler logs\x04 from the dev site.", important=False, base=True),
    Hint(
        hint="\x04W\x04\x05O\x05\x06A\x06\x07H\x07\x08,\x08 \x04I\x04 \x05D\x05\x06R\x06\x07O\x07\x08P\x08\x04P\x04\x05E\x05\x06D\x06 \x07A\x07\x08L\x08\x04L\x04 \x05M\x05\x06Y\x06 \x07C\x07\x08R\x08\x04A\x04\x05Y\x05\x06O\x06\x07N\x07\x08S\x08\x04!\x04",
        important=False,
        base=True,
    ),
    Hint(hint="[[WOTB]]", important=False, base=True),
    Hint(
        hint="By using DK64Randomizer.com, users agree to release the developers from any claims, damages, bad seeds, or liabilities. Please exercise caution and randomizer responsibly.",
        important=False,
        base=True,
    ),
    Hint(hint="Bothered? I was bothered once. They put me in a barrel, a bonus barrel. A bonus barrel with beavers, and beavers make me bothered.", important=False, base=True),
    Hint(hint="Looking for useful information? Try looking at another hint.", important=False, base=True),
    Hint(hint="Can I interest you in some casino chips? They're tastefully decorated with Hunky Chunky.", important=False, base=True),
    Hint(hint="Have faith, beanlievers. Your time will come.", important=False, base=True),
    Hint(hint="I have horrible news. Your seed just got \x0510 percent worse.\x05", important=False, base=True),
    Hint(hint="Great news! Your seed just got \x0810 percent better!\x08", important=False, base=True),
    Hint(hint="This is not a joke hint.", important=False, base=True),
    Hint(hint="I'll get back to you after this colossal dump of blueprints.", important=False, base=True),
    Hint(hint="Something in the \x0dHalt! The remainder of this hint has been confiscated by the top Kop on the force.\x0d", important=False, base=True),
    Hint(hint="When I finish Pizza Tower, this hint will update.", important=False, base=True),
    Hint(
        hint="Will we see a sub hour seasonal seed? Not a chance. The movement is too optimized at this point. I expect at most 10-20 more seconds can be saved, maybe a minute with TAS.",
        important=False,
        base=True,
    ),
    Hint(hint="The dk64randomizer.com wiki has lots of helpful information about hints.", important=False, base=True),
    Hint(hint="If you're watching on YouTube, be sure to like, comment, subscribe, and smash that bell.", important=False, base=True),
]

kong_list = ["\x04Donkey\x04", "\x05Diddy\x05", "\x06Lanky\x06", "\x07Tiny\x07", "\x08Chunky\x08", "\x04Any kong\x04"]
colorless_kong_list = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
kong_colors = ["\x04", "\x05", "\x06", "\x07", "\x08", "\x0c"]

kong_cryptic = [
    ["The kong who is bigger, faster and potentially stronger too", "The kong who fires in spurts", "The kong with a tie", "The kong who slaps their instrument to the jungle beat"],
    ["The kong who can fly real high", "The kong who features in the first two Donkey Kong Country games", "The kong who wants to see red", "The kong who frees the only female playable kong"],
    [
        "The kong who inflates like a balloon, just like a balloon",
        "The kong who waddles in his overalls",
        "The kong who has a cold race with an insect",
        "The kong who lacks style, grace but not a funny face",
    ],
    ["The kong who likes jazz", "The kong who shoots K. Rool's tiny toes", "The kong who has ammo that is light as a feather", "The kong who can shrink in size"],
    ["The kong who is one hell of a guy", "The kong who can pick up boulders", "The kong who fights a blocky boss", "The kong who bows down to a dragonfly"],
    ["Members of the DK Crew", "A specific set of relatives", "A number of playable characters"],
]

all_levels = [Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon, Levels.FungiForest, Levels.CrystalCaves, Levels.CreepyCastle]
level_colors = ["\x08", "\x04", "\x0c", "\x06", "\x07", "\x0a", "\x09", "\x05", "\x0b", "\x0d"]
level_list = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
    "Hideout Helm",
    "DK Isles",
    "Cranky's Lab",
]

level_cryptic = [
    ["The level with a localized storm", "The level with a dirt mountain", "The level which has two retailers and no race"],
    ["The level with four vases", "The level with two kongs cages", "The level with a spinning totem"],
    ["The level with a toy production facility", "The level with a tower of blocks", "The level with a game from 1981", "The level where you need two quarters to play"],
    ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
    ["The level with only two retailers and two races", "The level where night can be acquired at will", "The level with a nocturnal tree dweller"],
    ["The level with two inches of water", "The level with two ice shields", "The level with an Ice Tomato"],
    ["The level with battlements", "The level with a dungeon, ballroom and a library", "The level with drawbridge and a moat"],
    ["The timed level", "The level with no boss", "The level with no small bananas"],
]
level_cryptic_isles = level_cryptic.copy()
level_cryptic_isles.remove(level_cryptic_isles[-1])
level_cryptic_isles.append(["The hub world", "The world with DK's ugly mug on it", "The world with only a Cranky's Lab and Snide's HQ in it"])

level_cryptic_helm_isles = level_cryptic.copy()
level_cryptic_helm_isles.append(level_cryptic_isles[-1])

shop_owners = ["\x04Cranky\x04", "\x04Funky\x04", "\x04Candy\x04"]
shop_cryptic = [
    ["The shop owner with a walking stick", "The shop owner who is old", "The shop owner who is persistently grumpy", "The shop owner who resides near your Treehouse"],
    ["The shop owner who has an armory", "The shop owner who has a banana on his shop", "The shop owner with sunglasses", "The shop owner who calls everyone Dude"],
    ["The shop owner who is flirtatious", "The shop owner who is not present in Fungi Forest", "The shop owner who is not present in Jungle Japes", "The shop owner with blonde hair"],
]

crankys_cryptic = ["a location out of this world", "a location 5000 points deep", "a mad scientist's laboratory"]

item_type_names = {
    Types.Blueprint: "\x06a kasplat\x06",
    Types.Fairy: "\x06a fairy\x06",
    Types.Crown: "\x06a battle arena\x06",
    Types.RainbowCoin: "\x06a dirt patch\x06",
    Types.CrateItem: "\x06a melon crate\x06",
    Types.Enemies: "\x06an enemy\x06",
}
item_type_names_cryptic = {
    Types.Blueprint: ["a minion of K. Rool", "a shockwaving foe", "a colorfully haired henchman"],
    Types.Fairy: ["an aerial ace", "a bit of flying magic", "a Queenly representative"],
    Types.Crown: ["a contest of endurance", "a crowning achievement", "the visage of K. Rool"],
    Types.RainbowCoin: ["the initials of DK", "a muddy mess", "buried treasure"],
    Types.CrateItem: ["a bouncing box", "a breakable cube", "a crate of goodies"],
    Types.Enemies: ["a minor discouragement", "an obstacle along the way", "something found in mad maze maul"],
}

moves_data = [
    # Commented out logic sections are saved if we need to revert to the old hint system
    # Donkey
    MoveInfo(name="Baboon Blast", move_level=1, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Strong Kong", move_level=2, move_type="special", kong=Kongs.donkey),
    MoveInfo(name="Gorilla Grab", move_level=3, move_type="special", kong=Kongs.donkey),
    # Diddy
    MoveInfo(name="Chimpy Charge", move_level=1, move_type="special", kong=Kongs.diddy),
    MoveInfo(name="Rocketbarrel Boost", move_level=2, move_type="special", kong=Kongs.diddy, important=True),  # (spoiler.settings.krool_diddy or spoiler.settings.helm_diddy)),
    MoveInfo(name="Simian Spring", move_level=3, move_type="special", kong=Kongs.diddy),
    # Lanky
    MoveInfo(name="Orangstand", move_level=1, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Baboon Balloon", move_level=2, move_type="special", kong=Kongs.lanky),
    MoveInfo(name="Orangstand Sprint", move_level=3, move_type="special", kong=Kongs.lanky),
    # Tiny
    MoveInfo(name="Mini Monkey", move_level=1, move_type="special", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Ponytail Twirl", move_level=2, move_type="special", kong=Kongs.tiny),
    MoveInfo(name="Monkeyport", move_level=3, move_type="special", kong=Kongs.tiny, important=True),
    # Chunky
    MoveInfo(name="Hunky Chunky", move_level=1, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Primate Punch", move_level=2, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    MoveInfo(name="Gorilla Gone", move_level=3, move_type="special", kong=Kongs.chunky, important=True),  # spoiler.settings.krool_chunky),
    # Slam
    MoveInfo(name="Slam Upgrade", move_level=1, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=2, move_type="slam", kong=Kongs.any),
    MoveInfo(name="Slam Upgrade", move_level=3, move_type="slam", kong=Kongs.any),
    # Guns
    MoveInfo(name="Coconut Shooter", move_level=1, move_type="gun", kong=Kongs.donkey, important=True),
    MoveInfo(name="Peanut Popguns", move_level=1, move_type="gun", kong=Kongs.diddy, important=True),  # spoiler.settings.krool_diddy),
    MoveInfo(name="Grape Shooter", move_level=1, move_type="gun", kong=Kongs.lanky),
    MoveInfo(name="Feather Bow", move_level=1, move_type="gun", kong=Kongs.tiny, important=True),  # spoiler.settings.krool_tiny),
    MoveInfo(name="Pineapple Launcher", move_level=1, move_type="gun", kong=Kongs.chunky),
    # Gun Upgrades
    MoveInfo(name="Homing Ammo", move_level=2, move_type="gun", kong=Kongs.any),
    MoveInfo(name="Sniper Scope", move_level=3, move_type="gun", kong=Kongs.any),
    # Ammo Belt
    MoveInfo(name="Ammo Belt Upgrade", move_level=1, move_type="ammo_belt", kong=Kongs.any),
    MoveInfo(name="Ammo Belt Upgrade", move_level=2, move_type="ammo_belt", kong=Kongs.any),
    # Instruments
    MoveInfo(name="Bongo Blast", move_level=1, move_type="instrument", kong=Kongs.donkey, important=True),  # spoiler.settings.helm_donkey),
    MoveInfo(name="Guitar Gazump", move_level=1, move_type="instrument", kong=Kongs.diddy, important=True),  # spoiler.settings.helm_diddy),
    MoveInfo(name="Trombone Tremor", move_level=1, move_type="instrument", kong=Kongs.lanky, important=True),  # (spoiler.settings.helm_lanky or spoiler.settings.krool_lanky)),
    MoveInfo(name="Saxophone Slam", move_level=1, move_type="instrument", kong=Kongs.tiny, important=True),  # spoiler.settings.helm_tiny),
    MoveInfo(name="Triangle Trample", move_level=1, move_type="instrument", kong=Kongs.chunky, important=True),  # spoiler.settings.helm_chunky),
    # Instrument Upgrades
    MoveInfo(name="Instrument Upgrade", move_level=2, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=3, move_type="instrument", kong=Kongs.any),
    MoveInfo(name="Instrument Upgrade", move_level=4, move_type="instrument", kong=Kongs.any),
]

kong_placement_levels = [{"name": "Jungle Japes", "level": 0}, {"name": "Llama Temple", "level": 1}, {"name": "Tiny Temple", "level": 1}, {"name": "Frantic Factory", "level": 2}]


# Hint distribution that will be adjusted based on settings
# These values are "if this is an option, then you must have at least X of this hint"
hint_distribution_default = {
    HintType.Joke: 1,
    HintType.KRoolOrder: 1,
    HintType.HelmOrder: 1,  # must have one on the path
    HintType.MoveLocation: 7,  # must be placed before you can buy the move
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,  # must be placed on the path and before the level they hint
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 1,  # must be placed before you find them and placed in a door of a free kong
    # HintType.MedalsRequired: 1,
    HintType.Entrance: 5,
    HintType.RequiredKongHint: -1,  # Fixed number based on the number of locked kongs
    HintType.RequiredKeyHint: -1,  # Fixed number based on the number of keys to be obtained over the seed
    HintType.RequiredWinConditionHint: 0,  # Fixed number based on what K. Rool phases you must defeat
    HintType.RequiredHelmDoorHint: 0,  # Fixed number based on how many Helm doors have random requirements
    HintType.WothLocation: 8,
    HintType.FullShopWithItems: 8,
    # HintType.FoolishMove: 0,  # Used to be 2, added to FoolishRegion when it was removed
    HintType.FoolishRegion: 4,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 0,
    HintType.RegionItemCount: 1,
    HintType.ItemRegion: 0,
    HintType.Plando: 0,
}
HINT_CAP = 35  # There are this many total slots for hints

# The racing preset has a fixed hint distribution as follows - format should include all hint types to not throw errors
race_hint_distribution = {
    HintType.Joke: 0,
    HintType.KRoolOrder: 0,
    HintType.HelmOrder: 1,
    HintType.MoveLocation: 0,
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 0,
    # HintType.MedalsRequired: 0,
    HintType.Entrance: 0,
    HintType.RequiredKongHint: 3,
    HintType.RequiredKeyHint: 0,
    HintType.RequiredWinConditionHint: 0,
    HintType.RequiredHelmDoorHint: 0,
    HintType.WothLocation: 9,
    HintType.FullShopWithItems: 0,
    # HintType.FoolishMove: 0,
    HintType.FoolishRegion: 5,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 14,
    HintType.RegionItemCount: 3,
    HintType.ItemRegion: 0,
    HintType.Plando: 0,
}

# The item-hinting distribution has a K. Rool hint, a Helm hint, and then every other hint will point to a move.
item_hint_distribution = {
    HintType.Joke: 0,
    HintType.KRoolOrder: 0,
    HintType.HelmOrder: 0,
    HintType.MoveLocation: 0,
    # HintType.DirtPatch: 0,
    HintType.BLocker: 0,
    HintType.TroffNScoff: 0,
    HintType.KongLocation: 0,
    # HintType.MedalsRequired: 0,
    HintType.Entrance: 0,
    HintType.RequiredKongHint: 0,
    HintType.RequiredKeyHint: 0,
    HintType.RequiredWinConditionHint: 0,
    HintType.RequiredHelmDoorHint: 0,
    HintType.WothLocation: 0,
    HintType.FullShopWithItems: 0,
    # HintType.FoolishMove: 0,
    HintType.FoolishRegion: 0,
    HintType.ForeseenPathless: 0,
    HintType.Multipath: 0,
    HintType.RegionItemCount: 0,
    HintType.ItemRegion: 35,
    HintType.Plando: 0,
}

hint_reroll_cap = 1  # How many times are you willing to reroll a hinted location?
hint_reroll_chance = 1.0  # What % of the time do you reroll in conditions that could trigger a reroll?
globally_hinted_location_ids = []


def compileHints(spoiler: Spoiler) -> bool:
    """Create a hint distribution, generate buff hints, and place them in locations."""
    if spoiler.settings.krusha_kong is not None:
        replaceKongNameWithKrusha(spoiler)
    ClearHintMessages()
    hint_distribution = hint_distribution_default.copy()
    plando_hints_placed = 0
    if spoiler.settings.enable_plandomizer:
        plando_hints_placed = ApplyPlandoHints(spoiler)
        hint_distribution[HintType.Plando] = plando_hints_placed
    level_order_matters = spoiler.settings.logic_type != LogicType.nologic and spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.all
    globally_hinted_location_ids = []
    # Stores the number of hints each key will get
    key_hint_dict = {
        Items.JungleJapesKey: 0,
        Items.AngryAztecKey: 0,
        Items.FranticFactoryKey: 0,
        Items.GloomyGalleonKey: 0,
        Items.FungiForestKey: 0,
        Items.CrystalCavesKey: 0,
        Items.CreepyCastleKey: 0,
        Items.HideoutHelmKey: 0,
    }
    woth_key_ids = [
        spoiler.LocationList[woth_loc].item for woth_loc in spoiler.woth_locations if ItemList[spoiler.LocationList[woth_loc].item].type == Types.Key and woth_loc in spoiler.woth_paths.keys()
    ]
    # Precalculate the locations of the Keys - this info is used by distribution generation and hint generation
    key_location_ids = {}
    for location_id, location in spoiler.LocationList.items():
        if location.item in ItemPool.Keys():
            key_location_ids[location.item] = location_id

    # Some locations are particularly useless to hint
    useless_locations = {Items.HideoutHelmKey: [], Kongs.diddy: [], Kongs.lanky: [], Kongs.tiny: [], Kongs.chunky: []}
    # Your training in Gorilla Gone, Monkeyport, and Vines are always pointless hints if Key 8 is in Helm, so let's not
    if spoiler.settings.key_8_helm and Locations.HelmKey in spoiler.woth_paths.keys():
        useless_moves = [Items.Vines]
        if not spoiler.settings.switchsanity:
            useless_moves.extend([Items.Monkeyport, Items.GorillaGone])
        useless_locations[Items.HideoutHelmKey] = [
            loc for loc in spoiler.woth_paths[Locations.HelmKey] if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in useless_moves
        ]
        useless_locations[Items.HideoutHelmKey].append(Locations.HelmKey)  # Also don't count the known location of the key itself
    # Your training in moves which you know are always needed beat K. Rool are pointless to hint
    if Kongs.diddy in spoiler.settings.krool_order and Kongs.diddy in spoiler.krool_paths.keys():
        useless_locations[Kongs.diddy] = [
            loc
            for loc in spoiler.krool_paths[Kongs.diddy]
            if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in [Items.Peanut, Items.RocketbarrelBoost]
        ]
    if Kongs.lanky in spoiler.settings.krool_order and Kongs.lanky in spoiler.krool_paths.keys():
        useless_locations[Kongs.lanky] = [
            loc for loc in spoiler.krool_paths[Kongs.lanky] if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in [Items.Barrels, Items.Trombone]
        ]
    if Kongs.tiny in spoiler.settings.krool_order and Kongs.tiny in spoiler.krool_paths.keys():
        useless_locations[Kongs.tiny] = [
            loc for loc in spoiler.krool_paths[Kongs.tiny] if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in [Items.Feather, Items.MiniMonkey]
        ]
    if Kongs.chunky in spoiler.settings.krool_order and Kongs.chunky in spoiler.krool_paths.keys():
        useless_locations[Kongs.chunky] = [
            loc
            for loc in spoiler.krool_paths[Kongs.chunky]
            if (loc in TrainingBarrelLocations or loc in PreGivenLocations) and spoiler.LocationList[loc].item in [Items.ProgressiveSlam, Items.PrimatePunch, Items.HunkyChunky, Items.GorillaGone]
        ]

    multipath_dict_hints, multipath_dict_goals = GenerateMultipathDict(spoiler, useless_locations)

    locked_hint_types = [
        HintType.RequiredKongHint,
        HintType.RequiredKeyHint,
        HintType.RequiredWinConditionHint,
        HintType.RequiredHelmDoorHint,
        HintType.Multipath,
        HintType.ItemRegion,
    ]  # Some hint types cannot have their value changed
    maxed_hint_types = []  # Some hint types cannot have additional hints placed
    minned_hint_types = []  # Some hint types cannot have all their hints removed
    # If we're using the racing hints preset, we use the predetermined distribution with no exceptions
    if spoiler.settings.wrinkly_hints == WrinklyHints.fixed_racing:
        hint_distribution = race_hint_distribution.copy()
        # Extract plando hints from foolish hints - gotta pick something and I think these are the least impactful
        if spoiler.settings.enable_plandomizer:
            hint_distribution[HintType.Plando] = plando_hints_placed
            hint_distribution[HintType.FoolishRegion] -= plando_hints_placed
        # We know how many key path hints will be placed, now we need to distribute them reasonably
        key_difficulty_score = {}
        # Every woth key is guaranteed one
        for key_id in woth_key_ids:
            key_hint_dict[key_id] = 1
            path_length = len(spoiler.woth_paths[key_location_ids[key_id]])
            if key_id == Items.HideoutHelmKey:
                path_length -= len(useless_locations[Items.HideoutHelmKey])
            key_difficulty_score[key_id] = path_length  # The length of the path serves as a "score" for how much this key needs hints
        # Determine what keys can get more hints
        keys_eligible_for_more_hints = woth_key_ids.copy()
        # In simple level order, the Japes and Aztec keys will be treated as "early" keys and get direct hints - they get no more hints
        if level_order_matters and not spoiler.settings.hard_level_progression:
            if Items.JungleJapesKey in keys_eligible_for_more_hints:
                keys_eligible_for_more_hints.remove(Items.JungleJapesKey)
            if Items.AngryAztecKey in keys_eligible_for_more_hints:
                keys_eligible_for_more_hints.remove(Items.AngryAztecKey)
        # For each key hint we have left to place, find the "most unhinted" key and give that key another hint
        for i in range(hint_distribution[HintType.RequiredKeyHint] - len(woth_key_ids)):
            key_most_needing_hint = None
            most_unhinted_key_score = 1000  # Lower = needs hint more, should never be higher than 1
            for key_id in keys_eligible_for_more_hints:
                score = key_hint_dict[key_id] / key_difficulty_score[key_id]
                # If this score beats the previous score OR it ties and (has a longer path OR is a key found later in the seed), it is the new key most in need of a hint
                if score < most_unhinted_key_score or (score == most_unhinted_key_score and key_difficulty_score[key_id] >= key_difficulty_score[key_most_needing_hint]):
                    key_most_needing_hint = key_id
                    most_unhinted_key_score = score
            key_hint_dict[key_most_needing_hint] += 1  # Bless this key with an additional hint
    # If we're doing the item-hinting system, use that distribution
    elif spoiler.settings.wrinkly_hints in (WrinklyHints.item_hinting, WrinklyHints.item_hinting_advanced):
        hint_distribution = item_hint_distribution.copy()
        hint_distribution[HintType.ItemRegion] = HINT_CAP
        if spoiler.settings.enable_plandomizer:
            hint_distribution[HintType.Plando] = plando_hints_placed
            hint_distribution[HintType.ItemRegion] -= plando_hints_placed
        valid_types = [HintType.ItemRegion, HintType.Joke]
        # Build the list of valid hint types
        # If K. Rool is live it is guaranteed a hint in this distribution
        if (spoiler.settings.krool_phase_count < 5 or spoiler.settings.krool_random) and spoiler.settings.win_condition == WinCondition.beat_krool:
            valid_types.append(HintType.KRoolOrder)
            hint_distribution[HintType.KRoolOrder] = 1
            hint_distribution[HintType.ItemRegion] -= 1
        # If Helm is live it is guaranteed a hint in this distribution
        if spoiler.settings.helm_setting != HelmSetting.skip_all and (spoiler.settings.helm_phase_count < 5 or spoiler.settings.helm_random):
            valid_types.append(HintType.HelmOrder)
            hint_distribution[HintType.HelmOrder] = 1
            hint_distribution[HintType.ItemRegion] -= 1
        # Each random Helm door is also guaranteed a hint
        if spoiler.settings.crown_door_random or spoiler.settings.coin_door_random:
            valid_types.append(HintType.RequiredHelmDoorHint)
            if spoiler.settings.crown_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
                hint_distribution[HintType.ItemRegion] -= 1
            if spoiler.settings.coin_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
                hint_distribution[HintType.ItemRegion] -= 1
        # These filler hint types should never get added if you have enough moves placed in the world.
        # These would only be relevant if you picked this hint system and also started with a ton of moves which might error anyway. (Why would you ever do this?)
        if spoiler.settings.randomize_blocker_required_amounts and spoiler.settings.blocker_max > 1:
            valid_types.append(HintType.BLocker)
        if (
            spoiler.settings.randomize_cb_required_amounts
            and len(spoiler.settings.krool_keys_required) > 0
            and spoiler.settings.krool_keys_required != [Events.HelmKeyTurnedIn]
            and spoiler.settings.troff_max > 0
        ):
            valid_types.append(HintType.TroffNScoff)
        # We have at most 35 doors, we have to prioritize what item hints go in the doors.
        # List of locations to hint IN ORDER, starting from placing index 0 first, 1 second, and so on
        item_region_locations_to_hint = []
        kongs_to_hint = [kong for kong in ItemPool.Kongs(spoiler.settings) if ItemPool.GetKongForItem(kong) not in spoiler.settings.starting_kong_list]
        if spoiler.settings.shuffle_items and Types.Key in spoiler.settings.shuffled_location_types:
            item_region_locations_to_hint.extend([key_loc for key_loc in key_location_ids.values()])  # Keys you don't start with
            if spoiler.settings.key_8_helm:  # You may know that Key 8 is in Helm and that's pointless to hint
                item_region_locations_to_hint.remove(Locations.HelmKey)
        # Determine what moves are hintable
        all_hintable_moves = ItemPool.AllKongMoves() + ItemPool.TrainingBarrelAbilities() + kongs_to_hint
        if spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            all_hintable_moves.extend(ItemPool.ShockwaveTypeItems(spoiler.settings))
        if spoiler.settings.shuffle_items and Types.Bean in spoiler.settings.shuffled_location_types:
            all_hintable_moves.append(Items.Bean)
        optional_hintable_locations = []
        slam_locations = []
        # Loop through all locations, finding the location of all of these hintable moves
        for id, location in spoiler.LocationList.items():
            # Note the location of slams - these will always be at least optionally hintable and sometimes required to be hinted
            if location.item == Items.ProgressiveSlam:
                slam_locations.append(id)
            # Never hint training moves for obvious reasons
            if location.type in (Types.TrainingBarrel, Types.PreGivenMove):
                continue
            # If it's a woth item, it must be hinted so put it in the list
            if id in spoiler.woth_locations:
                if location.item in kongs_to_hint:
                    item_region_locations_to_hint.insert(0, id)
                elif location.item in all_hintable_moves:
                    item_region_locations_to_hint.append(id)
            # To be hintable, it can't be a starting move
            elif location.item in all_hintable_moves:
                optional_hintable_locations.append(id)
        # If there's room, always hint a slam if we haven't hinted one already
        hinted_slam_locations = [loc for loc in slam_locations if loc in item_region_locations_to_hint or spoiler.LocationList[loc].type in (Types.TrainingBarrel, Types.PreGivenMove)]
        if len(item_region_locations_to_hint) < hint_distribution[HintType.ItemRegion] and len(hinted_slam_locations) < 2:
            loc_to_hint = random.choice([loc for loc in slam_locations if loc not in hinted_slam_locations])
            item_region_locations_to_hint.append(loc_to_hint)
            optional_hintable_locations.remove(loc_to_hint)
        # Fill with other random move locations as best as we can
        random.shuffle(optional_hintable_locations)
        while len(item_region_locations_to_hint) < hint_distribution[HintType.ItemRegion] and len(optional_hintable_locations) > 0:
            item_region_locations_to_hint.append(optional_hintable_locations.pop())
        # If there's so many WotH things we can't hint them all, some WotH things will go unhinted. Unlucky.
        if len(item_region_locations_to_hint) > hint_distribution[HintType.ItemRegion]:
            too_many_count = len(item_region_locations_to_hint) - hint_distribution[HintType.ItemRegion]
            # That said, whatever goes unhinted probably shouldn't be something important
            less_important_location_ids = []
            for loc_id in item_region_locations_to_hint:
                # Don't remove hints to Kongs or Keys - the rest is fair game
                if ItemList[spoiler.LocationList[loc_id].item].type not in (Types.Kong, Types.Key):
                    less_important_location_ids.append(loc_id)
            # Randomly remove some of them so we don't bias towards early/late items - if you miss it, unlucky
            random.shuffle(less_important_location_ids)
            for i in range(too_many_count):
                item_region_locations_to_hint.remove(less_important_location_ids[i])
        # If you start with a ton of moves, there may be only a handful of things to hint
        if len(item_region_locations_to_hint) < hint_distribution[HintType.ItemRegion]:
            hint_distribution[HintType.ItemRegion] = len(item_region_locations_to_hint)
        # Make sure we still have exactly 35 hints planned
        hint_count = 0
        for type in hint_distribution:
            if type in valid_types or type == HintType.Plando:
                hint_count += hint_distribution[type]
            else:
                hint_distribution[type] = 0
        # We'll never be over the cap here, but in some cases we may be under the cap - fill extra hints if we need them
        while hint_count < HINT_CAP:
            filler_type = random.choice(valid_types)
            if filler_type == HintType.Joke:
                # Make it roll joke twice to add an extra joke hint
                filler_type = random.choice(valid_types)
            if filler_type in locked_hint_types or filler_type in maxed_hint_types:
                continue  # Some hint types cannot be filled with
            hint_distribution[filler_type] += 1
            hint_count += 1
    # Otherwise we dynamically generate the hint distribution
    else:
        # In level order (or vanilla) progression, there are hints that we want to be in the player's path
        # Determine what hint types are valid for these settings
        valid_types = [HintType.Joke]
        if spoiler.settings.randomize_blocker_required_amounts and spoiler.settings.blocker_max > 1:
            valid_types.append(HintType.BLocker)
        if (
            spoiler.settings.randomize_cb_required_amounts
            and len(spoiler.settings.krool_keys_required) > 0
            and spoiler.settings.krool_keys_required != [Events.HelmKeyTurnedIn]
            and spoiler.settings.troff_max > 0
        ):
            valid_types.append(HintType.TroffNScoff)
        if spoiler.settings.kong_rando:
            if spoiler.settings.shuffle_items and Types.Kong in spoiler.settings.shuffled_location_types:
                valid_types.append(HintType.RequiredKongHint)
                hint_distribution[HintType.RequiredKongHint] = 5 - spoiler.settings.starting_kongs_count
            else:
                valid_types.append(HintType.KongLocation)
        # if spoiler.settings.coin_door_open == "need_both" or spoiler.settings.coin_door_open == "need_rw":
        #     valid_types.append(HintType.MedalsRequired)
        if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.all:
            # In entrance rando, we care more about T&S than B. Locker
            temp = hint_distribution[HintType.BLocker]
            if spoiler.settings.randomize_blocker_required_amounts and not spoiler.settings.maximize_helm_blocker:
                hint_distribution[HintType.BLocker] = max(1, hint_distribution[HintType.TroffNScoff])  # Always want a helm hint in there
            hint_distribution[HintType.TroffNScoff] = temp
            valid_types.append(HintType.Entrance)
        if (spoiler.settings.krool_phase_count < 5 or spoiler.settings.krool_random) and spoiler.settings.win_condition == WinCondition.beat_krool:
            valid_types.append(HintType.KRoolOrder)
            maxed_hint_types.append(HintType.KRoolOrder)
            # If the seed doesn't funnel you into helm, guarantee one K. Rool order hint
            if Events.HelmKeyTurnedIn not in spoiler.settings.krool_keys_required or not spoiler.settings.key_8_helm:
                minned_hint_types.append(HintType.KRoolOrder)
        if spoiler.settings.helm_setting != HelmSetting.skip_all and (spoiler.settings.helm_phase_count < 5 or spoiler.settings.helm_random):
            valid_types.append(HintType.HelmOrder)
            locked_hint_types.append(HintType.HelmOrder)
        if spoiler.settings.move_rando not in (MoveRando.off, MoveRando.item_shuffle) and Types.Shop not in spoiler.settings.shuffled_location_types:
            valid_types.append(HintType.FullShopWithItems)
            valid_types.append(HintType.MoveLocation)
        if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.shuffled_location_types:
            # With no logic WOTH isn't built correctly so we can't make any hints with it
            if spoiler.settings.logic_type != LogicType.nologic:
                # If we're in full item rando with shops in the pool, we need to replace our bad filler with good filler
                # Get rid of the bad filler
                if HintType.BLocker in valid_types:
                    valid_types.remove(HintType.BLocker)
                if HintType.TroffNScoff in valid_types:
                    valid_types.remove(HintType.TroffNScoff)
                # Add the good filler
                valid_types.append(HintType.FoolishRegion)
                # If there are more foolish region hints than regions, lower this number and prevent more from being added
                if len(spoiler.foolish_region_names) < hint_distribution[HintType.FoolishRegion]:
                    hint_distribution[HintType.FoolishRegion] = len(spoiler.foolish_region_names)
                    maxed_hint_types.append(HintType.FoolishRegion)

                # valid_types.append(HintType.ForeseenPathless)
                # # If there are more pathless move hints than pathless moves, lower this number and prevent more from being added
                # if len(spoiler.pathless_moves) < hint_distribution[HintType.ForeseenPathless]:
                #     hint_distribution[HintType.ForeseenPathless] = len(spoiler.pathless_moves)
                #     maxed_hint_types.append(HintType.ForeseenPathless)

                valid_types.append(HintType.RegionItemCount)
                # If there are more region item count hints than regions containing moves (????), lower this number and prevent more from being added
                if len(spoiler.region_hintable_count.keys()) < hint_distribution[HintType.RegionItemCount]:
                    hint_distribution[HintType.RegionItemCount] = len(spoiler.region_hintable_count.keys())
                    maxed_hint_types.append(HintType.RegionItemCount)

                valid_types.append(HintType.WothLocation)
                # K. Rool seeds could use some help finding the last pesky moves
                if spoiler.settings.win_condition == WinCondition.beat_krool:
                    valid_types.append(HintType.RequiredWinConditionHint)
                    path_length = len(spoiler.woth_paths[Locations.BananaHoard]) - 1  # Don't include the Banana Hoard itself in the path length
                    if Kongs.diddy in spoiler.settings.krool_order:
                        hint_distribution[HintType.RequiredWinConditionHint] += 1
                    if Kongs.lanky in spoiler.settings.krool_order:
                        hint_distribution[HintType.RequiredWinConditionHint] += 1
                    if Kongs.tiny in spoiler.settings.krool_order:
                        hint_distribution[HintType.RequiredWinConditionHint] += 1
                    if Kongs.chunky in spoiler.settings.krool_order:
                        hint_distribution[HintType.RequiredWinConditionHint] += 2
                    path_length -= len(useless_locations[Kongs.diddy]) + len(useless_locations[Kongs.lanky]) + len(useless_locations[Kongs.tiny]) + len(useless_locations[Kongs.chunky])
                    if hint_distribution[HintType.RequiredWinConditionHint] != 0:
                        # Guarantee you have a decent number of hints, even if you have very few, very buried moves required
                        if path_length == 0:
                            hint_distribution[HintType.RequiredWinConditionHint] = 0
                        elif path_length <= 1:  # 2 (should never be 1 here)
                            hint_distribution[HintType.RequiredWinConditionHint] = max(hint_distribution[HintType.RequiredWinConditionHint], 1)
                        elif path_length <= 3:  # 3-4
                            hint_distribution[HintType.RequiredWinConditionHint] = max(hint_distribution[HintType.RequiredWinConditionHint], 2)
                        elif path_length <= 6:  # 5-7
                            hint_distribution[HintType.RequiredWinConditionHint] = max(hint_distribution[HintType.RequiredWinConditionHint], 3)
                        elif path_length <= 9:  # 8-10
                            hint_distribution[HintType.RequiredWinConditionHint] = max(hint_distribution[HintType.RequiredWinConditionHint], 4)
                        else:  # 11+
                            hint_distribution[HintType.RequiredWinConditionHint] = max(hint_distribution[HintType.RequiredWinConditionHint], 5)
                    # Old system pointing to specific moves
                    # if Kongs.diddy in spoiler.settings.krool_order:
                    #     hint_distribution[HintType.RequiredWinConditionHint] += 1  # Dedicated Rocketbarrel hint
                    # if Kongs.tiny in spoiler.settings.krool_order:
                    #     hint_distribution[HintType.RequiredWinConditionHint] += 1  # Dedicated Mini Monkey hint
                    # if Kongs.chunky in spoiler.settings.krool_order:
                    #     hint_distribution[HintType.RequiredWinConditionHint] += 1  # Dedicated Hunky Chunky hint
                # Some win conditions need help finding the camera (if you don't start with it) - variable amount of unique hints for it
                if spoiler.settings.win_condition in (WinCondition.all_fairies, WinCondition.poke_snap) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
                    camera_location_id = None
                    for id, loc in spoiler.LocationList.items():
                        if loc.item in (Items.Camera, Items.CameraAndShockwave):
                            camera_location_id = id
                            break
                    # Don't make a Camera path hint if Camera isn't woth
                    if camera_location_id in spoiler.woth_paths.keys():
                        valid_types.append(HintType.RequiredWinConditionHint)
                        # Same rules as key path amounts
                        path_length = len(spoiler.woth_paths[camera_location_id]) - 1  # Don't include the camera itself in the path length
                        if path_length < 0:  # 0 (I'm not sure this is possible but I don't want to error)
                            hint_distribution[HintType.RequiredWinConditionHint] = 0
                        elif path_length <= 1:  # 1-2
                            hint_distribution[HintType.RequiredWinConditionHint] = 1
                        elif path_length <= 5:  # 3-6
                            hint_distribution[HintType.RequiredWinConditionHint] = 2
                        elif path_length <= 9:  # 7-10
                            hint_distribution[HintType.RequiredWinConditionHint] = 3
                        else:  # 11+
                            hint_distribution[HintType.RequiredWinConditionHint] = 4
        if spoiler.settings.crown_door_random or spoiler.settings.coin_door_random:
            valid_types.append(HintType.RequiredHelmDoorHint)
            if spoiler.settings.crown_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
            if spoiler.settings.coin_door_random:
                hint_distribution[HintType.RequiredHelmDoorHint] += 1
        # if spoiler.settings.random_patches:
        #     valid_types.append(HintType.DirtPatch)

        # There are no paths in no logic so multipath doesn't function
        if spoiler.settings.logic_type != LogicType.nologic:
            # Dynamically calculate the number of key hints that need to be placed per key. Any WotH keys should have paths that we should hint.
            if spoiler.settings.shuffle_items and len(woth_key_ids) > 0:
                valid_types.append(HintType.RequiredKeyHint)
                # Only hint keys that are in the Way of the Hoard
                for key_id in woth_key_ids:
                    # Keys you are expected to find early only get one direct hint, treat all keys as early keys because there are no paths
                    if False and key_id in (Items.JungleJapesKey, Items.AngryAztecKey) and level_order_matters and not spoiler.settings.hard_level_progression:
                        # This is no longer true with multipath hints - all keys get hints based on path length
                        key_hint_dict[key_id] = 1
                    # Late or complex keys get a number of hints based on the length of the path to them
                    else:
                        path_length = len(spoiler.woth_paths[key_location_ids[key_id]])
                        # If key 8 is in Helm, your training in several moves is utterly useless to hint
                        if key_id == Items.HideoutHelmKey and spoiler.settings.key_8_helm:
                            path_length -= len(useless_locations[Items.HideoutHelmKey])
                        if path_length <= 0:  # 0
                            key_hint_dict[key_id] = 0
                        elif path_length <= 2:  # 1-2
                            key_hint_dict[key_id] = 1
                        elif path_length <= 5:  # 3-5
                            key_hint_dict[key_id] = 2
                        elif path_length <= 9:  # 6-9
                            key_hint_dict[key_id] = 3
                        elif path_length <= 13:  # 10-13
                            key_hint_dict[key_id] = 4
                        else:  # 14+
                            key_hint_dict[key_id] = 5
                hint_distribution[HintType.RequiredKeyHint] = sum(key_hint_dict.values())
            # Convert all path hints into multipath hints, utilizing the prior calculations as a rough estimate of path length/difficulty
            estimated_path_difficulty = max(0, (hint_distribution[HintType.RequiredKeyHint] * 1) + (hint_distribution[HintType.RequiredWinConditionHint] * 0.8))
            hint_distribution[HintType.RequiredWinConditionHint] = 0
            hint_distribution[HintType.RequiredKeyHint] = 0
            if HintType.RequiredWinConditionHint in valid_types:
                valid_types.remove(HintType.RequiredWinConditionHint)
            if HintType.RequiredKeyHint in valid_types:
                valid_types.remove(HintType.RequiredKeyHint)
            # Multipath hints are generally more powerful than your average hint, so we need fewer of them (but not more hints than are possible!)
            hint_distribution[HintType.Multipath] = min(len(multipath_dict_hints.keys()), round(estimated_path_difficulty))
            if hint_distribution[HintType.Multipath] >= len(multipath_dict_hints.keys()):
                maxed_hint_types.append(HintType.Multipath)
            valid_types.append(HintType.Multipath)

        # Make sure we have exactly 35 hints placed
        hint_count = 0
        for type in hint_distribution:
            if type in valid_types or type == HintType.Plando:
                hint_count += hint_distribution[type]
            else:
                hint_distribution[type] = 0
        # Fill extra hints if we need them
        while hint_count < HINT_CAP:
            filler_type = random.choice(valid_types)
            if filler_type == HintType.Joke:
                # Make it roll joke twice to add an extra joke hint
                filler_type = random.choice(valid_types)
                if filler_type == HintType.Joke:
                    # Just kidding, make it roll joke thrice to add an extra joke hint
                    filler_type = random.choice(valid_types)
            if filler_type in locked_hint_types or filler_type in maxed_hint_types:
                continue  # Some hint types cannot be filled with
            hint_distribution[filler_type] += 1
            hint_count += 1
            # In theory, you could overload on multipath hints here, let's prevent that
            if filler_type == HintType.Multipath and hint_distribution[HintType.Multipath] >= len(multipath_dict_hints.keys()):
                maxed_hint_types.append(HintType.Multipath)
        # Remove random hints if we went over the cap
        while hint_count > HINT_CAP:
            # In many settings, you may have more required hints than you have doors
            locked_hint_count = sum([hint_distribution[typ] for typ in locked_hint_types]) + sum([hint_distribution[typ] for typ in minned_hint_types])
            # If this is the case (again, INSANELY rare) then you lose a random key hint
            if locked_hint_count > HINT_CAP:
                key_to_lose_a_hint = random.choice([key for key in key_hint_dict.keys() if key_hint_dict[key] > 0])
                key_hint_dict[key_to_lose_a_hint] -= 1
                if HintType.Multipath in valid_types:
                    hint_distribution[HintType.Multipath] -= 1
                else:
                    hint_distribution[HintType.RequiredKeyHint] -= 1
                hint_count -= 1
                continue
            # In all other cases, remove a random hint that is eligible to be removed
            removed_type = random.choice(valid_types)
            if removed_type in locked_hint_types:
                continue  # Some hint types cannot have fewer than specified by the settings
            if removed_type in minned_hint_types and hint_distribution[removed_type] == 1:
                continue  # Some hint types cannot have 0 hints if they're a possible hint type
            if hint_distribution[removed_type] > 0:
                hint_distribution[removed_type] -= 1
                hint_count -= 1

    progression_hint_locations = None
    if level_order_matters:
        # These hint locations are *much* more likely to be seen, as they'll be available as players pass through lobbies on their first visit
        progression_hint_locations = []
        for level in all_levels:
            for kong in spoiler.settings.owned_kongs_by_level[level]:
                # In hint door location rando, it's too complicated to determine if the door will be accessible on the first trip
                # Assume they'll see the hint doors for the kongs they have available
                # NOTE: this is a quick and dirty solution that can bury critical hints - better solution would be to set up accessible_hints_by_level array like moves/kongs
                if not spoiler.settings.wrinkly_location_rando:
                    # If we don't have DK + Grab then these hints are skipped basically every time so they're not on the player's path
                    if (
                        level == Levels.FranticFactory
                        and kong not in [Kongs.donkey, Kongs.chunky]
                        and (Kongs.donkey not in spoiler.settings.owned_kongs_by_level[level] or Items.GorillaGrab not in spoiler.settings.owned_moves_by_level[level])
                    ):
                        continue
                    if (
                        level == Levels.FungiForest
                        and kong is not Kongs.chunky
                        and (Kongs.donkey not in spoiler.settings.owned_kongs_by_level[level] or Items.GorillaGrab not in spoiler.settings.owned_moves_by_level[level])
                    ):
                        continue
                    # Caves Diddy needs a whole suite of moves to see this hint
                    if (
                        level == Levels.CrystalCaves
                        and kong is Kongs.diddy
                        and (
                            Kongs.chunky not in spoiler.settings.owned_kongs_by_level[level]
                            or Items.PrimatePunch not in spoiler.settings.owned_moves_by_level[level]
                            or Items.RocketbarrelBoost not in spoiler.settings.owned_moves_by_level[level]
                            or Items.Barrels not in spoiler.settings.owned_moves_by_level[level]
                        )
                    ):
                        continue
                    # Everyone else in Caves still needs Chunky + Punch + Barrels
                    if level == Levels.CrystalCaves and (
                        Kongs.chunky not in spoiler.settings.owned_kongs_by_level[level]
                        or Items.PrimatePunch not in spoiler.settings.owned_moves_by_level[level]
                        or Items.Barrels not in spoiler.settings.owned_moves_by_level[level]
                    ):
                        continue
                    # Aztec Chunky also needs Tiny + Feather + Hunky Chunky
                    if (
                        level == Levels.AngryAztec
                        and kong is Kongs.chunky
                        and (
                            Kongs.tiny not in spoiler.settings.owned_kongs_by_level[level]
                            or Items.Feather not in spoiler.settings.owned_moves_by_level[level]
                            or Items.HunkyChunky not in spoiler.settings.owned_moves_by_level[level]
                        )
                    ):
                        continue
                hint_for_location = [hint for hint in hints if hint.level == level and hint.kong == kong][0]  # Should only match one
                progression_hint_locations.append(hint_for_location)

    # Now place hints by type from most-restrictive to least restrictive. Usually anything we want on the player's path should get placed first
    # Item rando kong hints are required and highly restrictive, only hinted to free kongs before (or as) the location is available
    if hint_distribution[HintType.RequiredKongHint] > 0:
        # The length of this list should match hint_distribution[HintType.RequiredKongHint]
        kong_location_ids = [id for id, location in spoiler.LocationList.items() if location.item in (Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky)]
        for kong_location_id in kong_location_ids:
            kong_location = spoiler.LocationList[kong_location_id]
            hint_options = []
            # Attempt to find a door that will be accessible before the Kong
            if kong_location_id in spoiler.accessible_hints_for_location.keys():  # This will fail if the Kong is not WotH
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[kong_location_id])  # This will return [] if there are no hint doors available
            # Additionally, if progressive hints are on, make sure that all your kongs are hinted by the 20th hint (Galleon Chunky)
            if spoiler.settings.enable_progressive_hints:
                hint_options = [hint for hint in hint_options if hint.level in (Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon)]
            if len(hint_options) > 0:
                hint_location = random.choice(hint_options)
            # If there are no doors available early (very rare) or the Kong is not WotH (obscenely rare) then just get a random one. Tough luck.
            else:
                if spoiler.settings.enable_progressive_hints:  # In progressive hints we'll still stick the hint in the first 20 hints
                    hint_location = getRandomHintLocation(levels=[Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon])
                else:
                    hint_location = getRandomHintLocation()
            globally_hinted_location_ids.append(kong_location_id)
            freeing_kong_name = kong_list[kong_location.kong]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                if kong_location.level == Levels.Shops:  # Exactly Jetpac
                    level_name = "\x08" + random.choice(crankys_cryptic) + "\x08"
                else:
                    level_name = "\x08" + random.choice(level_cryptic_helm_isles[kong_location.level]) + "\x08"
            else:
                if kong_location.level == Levels.Shops:  # Exactly Jetpac
                    level_name = "Cranky's Lab"
                else:
                    level_name = level_colors[kong_location.level] + level_list[kong_location.level] + level_colors[kong_location.level]
            freed_kong = kong_list[ItemPool.GetKongForItem(kong_location.item)]
            message = ""
            if kong_location.type in item_type_names.keys():
                location_name = item_type_names[kong_location.type]
                if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                    location_name = "\x06" + random.choice(item_type_names_cryptic[kong_location.type]) + "\x06"
                message = f"{freed_kong} is held by {location_name} in {level_name}."
            elif kong_location.type == Types.Shop:
                message = f"{freed_kong} can be bought in {level_name}."
            elif freeing_kong_name == freed_kong:
                grammar = "himself"
                if kong_location.kong == Kongs.tiny:
                    grammar = "herself"
                message = f"{freeing_kong_name} can be found by {grammar} in {level_name}? How odd..."
            else:
                message = f"{freed_kong} can be found by {freeing_kong_name} in {level_name}."
            hint_location.related_location = kong_location_id
            hint_location.hint_type = HintType.RequiredKongHint
            UpdateHint(hint_location, message)
    # In non-item rando, Kongs should be hinted before they're available and should only be hinted to free Kongs, making them very restrictive
    hinted_kongs = []
    placed_kong_hints = 0
    while placed_kong_hints < hint_distribution[HintType.KongLocation]:
        kong_map = random.choice(kong_placement_levels)
        kong_index = spoiler.shuffled_kong_placement[kong_map["name"]]["locked"]["kong"]
        free_kong = spoiler.shuffled_kong_placement[kong_map["name"]]["puzzle"]["kong"]
        level_index = kong_map["level"]

        level_restriction = None
        # If this is the first time we're hinting this kong, attempt to put it in an earlier level (regardless of whether or not you can read it)
        # This only matters if level order matters
        if level_order_matters and kong_index not in hinted_kongs:
            level_restriction = [level for level in all_levels if spoiler.settings.EntryGBs[level] <= spoiler.settings.EntryGBs[kong_map["level"]]]
        # This list of free kongs is sometimes only a subset of the correct list. A more precise list could be calculated but it would be slow.
        free_kongs = spoiler.settings.starting_kong_list.copy()
        free_kongs.append(free_kong)
        hint_location = getRandomHintLocation(kongs=free_kongs, levels=level_restriction)
        # If this fails, it's extremely likely there's already a very useful hint in the very few spot(s) this could be
        if hint_location is None:
            if level_restriction is not None:
                # Can't make it too easy on em - put this hint in any hint door for these kongs
                hint_location = getRandomHintLocation(kongs=free_kongs)
            else:
                # In the unfathomably rare world where our freeing kong is out of hint doors, replace this hint with a joke hint
                # When I say unfathomably, I'm talking "you start with all moves and free B. Lockers but only 4 Kongs"
                hint_distribution[HintType.Joke] += 1  # Adding meme hints to meme seeds is just thematic at this point
                hint_distribution[HintType.KongLocation] -= 1
                continue

        if hint_location is not None:
            freeing_kong_name = kong_list[free_kong]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                if not kong_index == Kongs.any:
                    kong_name = "\x07" + random.choice(kong_cryptic[kong_index]) + "\x07"
                level_name = "\x08" + random.choice(level_cryptic[level_index]) + "\x08"
            else:
                if not kong_index == Kongs.any:
                    kong_name = kong_list[kong_index]
                level_name = level_colors[level_index] + level_list[level_index] + level_colors[level_index]
            unlock_verb = "frees"
            if kong_index == Kongs.any:
                unlock_verb = "accesses"
                kong_name = "an empty cage"
            message = f"{freeing_kong_name} {unlock_verb} {kong_name} in {level_name}."
            hinted_kongs.append(kong_index)
            hint_location.hint_type = HintType.KongLocation
            UpdateHint(hint_location, message)
            placed_kong_hints += 1

    # B. Locker hints need to be on the player's path to be useful
    hinted_blocker_combos = []
    for i in range(hint_distribution[HintType.BLocker]):
        # If there's a specific level order to the seed, place the hints on the player's path so these hints aren't useless
        location_restriction = None
        if level_order_matters:
            location_restriction = progression_hint_locations
        # Pick random hint locations until we get one that can hint a future level
        hintable_levels = []
        while len(hintable_levels) == 0:
            hint_location = getRandomHintLocation(location_list=location_restriction)
            if hint_location is not None:
                # Only hint levels more expensive than the current one AND we care about level order AND this hint's lobby doesn't already hint this level
                hintable_levels = [
                    level
                    for level in all_levels
                    if (not level_order_matters or spoiler.settings.EntryGBs[level] > spoiler.settings.EntryGBs[hint_location.level]) and (hint_location.level, level) not in hinted_blocker_combos
                ]
                # If Helm is random, always place at least one Helm hint - this helps non-maximized Helm seeds and slightly nerfs this category of hints otherwise.
                if not spoiler.settings.maximize_helm_blocker:
                    if i == 0:
                        hintable_levels = [Levels.HideoutHelm]
                    else:
                        hintable_levels.append(Levels.HideoutHelm)
        hinted_level = random.choice(hintable_levels)
        hinted_blocker_combos.append((hint_location.level, hinted_level))
        level_name = level_colors[hinted_level] + level_list[hinted_level] + level_colors[hinted_level]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            level_name = "\x08" + random.choice(level_cryptic[hinted_level]) + "\x08"
        message = f"The barrier to {level_name} can be cleared by obtaining \x04{spoiler.settings.EntryGBs[hinted_level]} Golden Bananas\x04."
        hint_location.hint_type = HintType.BLocker
        UpdateHint(hint_location, message)

    # Item region hints take up a ton of hint doors, and some hints have restrictions on placement
    if hint_distribution[HintType.ItemRegion] > 0:
        # This array is arranged in such a way as to place the more important items to hint (kongs, keys, woth moves) first
        for loc_id in item_region_locations_to_hint:
            hint_location = None
            # If this hint does have hint door restrictions, attempt to abide by them. Items placed earlier are more likely to have restrictions, hence the rough order of hint placement.
            if loc_id in spoiler.accessible_hints_for_location.keys():
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[loc_id])
                # Additionally, if progressive hints are on and this is a Kong hint, make sure that all your Kongs are hinted by the 20th hint (Galleon Chunky)
                if spoiler.settings.enable_progressive_hints and ItemList[spoiler.LocationList[loc_id].item].type == Types.Kong:
                    hint_options = [hint for hint in hint_options if hint.level in (Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon)]
                if len(hint_options) > 0:
                    hint_location = random.choice(hint_options)
            # If this location's goals do not restrict hint door location OR all the restricted hint door options are taken (staggeringly unlikely), get a random hint door
            if hint_location is None or len(hint_options) == 0:
                level_limit = None
                # Limit our level options to the first 4 if we're on progressive hints and this is a Kong
                if ItemList[spoiler.LocationList[loc_id].item].type == Types.Kong and spoiler.settings.enable_progressive_hints:
                    level_limit = [Levels.JungleJapes, Levels.AngryAztec, Levels.FranticFactory, Levels.GloomyGalleon]
                hint_location = getRandomHintLocation(levels=level_limit)
            location = spoiler.LocationList[loc_id]
            item = ItemList[location.item]
            item_color = kong_colors[item.kong]  # Color based on the Kong of the item
            if item.type == Types.Key:  # Except Keys are gold
                item_color = kong_colors[Kongs.donkey]
            elif item.type == Types.Kong:  # Kong items are any kong items, but these make more intuitive sense as their respective color
                item_color = kong_colors[ItemPool.GetKongForItem(location.item)]
            item_name = item.name
            # In advanced item hinting hints, hint a category of the item, not the exact item.
            if spoiler.settings.wrinkly_hints == WrinklyHints.item_hinting_advanced:
                if item.type == Types.Kong:
                    item_name = "kongs"
                    item_color = kong_colors[Kongs.donkey]  # Genericize the color to be even more vague
                elif item.type == Types.Key:
                    item_name = "keys"
                elif item.type == Types.Shockwave:
                    item_name = "fairy moves"
                    item_color = "\x06"
                elif item.type == Types.TrainingBarrel:
                    item_name = "training moves"
                elif item.type == Types.Shop:
                    if item.kong == Kongs.any:
                        item_name = "shared kong moves"
                    else:
                        # 50/50 chance for kong moves to either...
                        coin_flip = random.choice([1, 2])
                        if coin_flip == 1:
                            # Hint the kong the move belongs to
                            item_name = colorless_kong_list[item.kong] + " moves"
                        else:
                            # Hint the type of move it is
                            item_color = kong_colors[Kongs.donkey]  # Genericize the color to be even more vague
                            if item.movetype == MoveTypes.Guns:
                                item_name = "guns"
                            elif item.movetype == MoveTypes.Instruments:
                                item_name = "instruments"
                            elif location.item in (Items.GorillaGrab, Items.ChimpyCharge, Items.Orangstand, Items.PonyTailTwirl, Items.PrimatePunch):
                                item_name = "active kong moves"
                            elif location.item in (Items.StrongKong, Items.RocketbarrelBoost, Items.OrangstandSprint, Items.MiniMonkey, Items.HunkyChunky):
                                item_name = "kong barrel moves"
                            elif location.item in (Items.BaboonBlast, Items.SimianSpring, Items.BaboonBalloon, Items.Monkeyport, Items.GorillaGone):
                                item_name = "kong pad moves"
            message = f"Looking for {item_color}{item_name}{item_color}?"
            # If this hint tries to offer help finding Krusha, make sure to get his name right
            if item.type == Types.Kong and spoiler.settings.wrinkly_hints != WrinklyHints.item_hinting_advanced:
                if ItemPool.GetKongForItem(location.item) == spoiler.settings.krusha_kong:
                    message = message.replace(item.name, "Krusha")
            # Two options for hinting the location, do a coin flip
            coin_flip = random.choice([1, 2])
            if coin_flip == 1:
                # Option A: hint the region the item is in
                region = GetRegionOfLocation(spoiler, loc_id)
                if region.hint_name != "Troff 'N' Scoff":
                    hinted_location_text = level_colors[region.level] + region.hint_name + level_colors[region.level]
                else:
                    hinted_location_text = level_colors[Levels.DKIsles] + region.hint_name + level_colors[Levels.DKIsles]
                message += f" Try looking in the {hinted_location_text}."
            else:
                # Option B: hint the kong + level the item is in, using similar systems as other hints to instead hint kasplats/shops/specific types of items
                level_color = level_colors[location.level]
                if location.type in item_type_names.keys():
                    message += f" Seek {item_type_names[location.type]} in {level_color}{level_list[location.level]}{level_color}."
                elif location.type == Types.Shop:
                    message += f" Seek shops in {level_color}{level_list[location.level]}{level_color}."
                else:
                    message += f" Try looking in {level_color}{level_list[location.level]}{level_color} with {kong_list[location.kong]}."
            hint_location.related_location = loc_id
            hint_location.hint_type = HintType.ItemRegion
            UpdateHint(hint_location, message)

    # Multipath hints have some complicated restrictions on placement
    if hint_distribution[HintType.Multipath] > 0:
        hinted_path_locations = []
        # Ensure one location from each key's path is to be hinted to guarantee that goal gets a hint
        for key_id in woth_key_ids:
            # Determine if any location we're already hinting is on the path to this key
            hinted_locations_on_this_path = set(spoiler.woth_paths[key_location_ids[key_id]]) & set(hinted_path_locations)
            # If we haven't hinted anything on this path, pick something
            if not any(hinted_locations_on_this_path):
                location_options = [loc for loc in spoiler.woth_paths[key_location_ids[key_id]] if loc in multipath_dict_hints.keys()]
                # If there are no valid options, that means everything on this path is either worthless to hint or already hinted, so we're good
                if len(location_options) != 0:
                    # Otherwise pick a random location on this path - this guarantees each Key has at least one hint in its direction
                    location_to_hint = random.choice(location_options)
                    hinted_path_locations.append(location_to_hint)
        # If K. Rool is our goal, do the same with K. Rool phases
        if spoiler.settings.win_condition == WinCondition.beat_krool:
            for kong in spoiler.krool_paths.keys():
                # Determine if any location we're already hinting is on the path to this phase of K. Rool
                hinted_locations_on_this_path = set(spoiler.krool_paths[kong]) & set(hinted_path_locations)
                # If we haven't hinted anything on this path, pick something
                if not any(hinted_locations_on_this_path):
                    location_options = [loc for loc in spoiler.krool_paths[kong] if loc in multipath_dict_hints.keys()]
                    # If there are no valid options, that means everything on this path is worthless to hint/already hinted or there's nothing on the path at all (Donkey...) so we're good
                    if len(location_options) != 0:
                        # Otherwise pick a random location on this path - this guarantees each K. Rool phase has at least one hint in its direction
                        location_to_hint = random.choice(location_options)
                        hinted_path_locations.append(location_to_hint)
        # If the camera is critical to the win condition, guarantee one path hint for it
        if spoiler.settings.win_condition in (WinCondition.all_fairies, WinCondition.poke_snap) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            # Find the camera's location
            camera_location_id = None
            for location_id in multipath_dict_hints.keys():
                if spoiler.LocationList[location_id].item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = location_id
                    break
            # If we found the camera in a hintable location, ensure that we have at least one hint for it
            if camera_location_id is not None:
                # Determine if any location we're already hinting is on the path to the camera
                hinted_locations_on_this_path = set(spoiler.woth_paths[camera_location_id]) & set(hinted_path_locations)
                # If we haven't hinted anything on this path, pick something
                if not any(hinted_locations_on_this_path):
                    location_options = [loc for loc in spoiler.woth_paths[camera_location_id] if loc in multipath_dict_hints.keys()]
                    # If there are no valid options, that means everything on this path is worthless to hint (but I don't think the camera interacts with this)
                    if len(location_options) != 0:
                        # Otherwise pick a random location on this path - this guarantees the camera has at least one hint in its direction
                        location_to_hint = random.choice(location_options)
                        hinted_path_locations.append(location_to_hint)
        # pick randomly from remaining locations in the keys to the multipath dict
        while len(hinted_path_locations) < hint_distribution[HintType.Multipath]:
            location_to_hint = random.choice([loc for loc in multipath_dict_hints.keys() if loc not in hinted_path_locations])
            hinted_path_locations.append(location_to_hint)
        # When placing hints, go from start to finish by woth_locations - this *roughly* places hints in most-restricted to least-restricted order
        for loc in spoiler.woth_locations:
            if loc not in hinted_path_locations:
                continue
            # When choosing hint doors, consider ALL goals when restricting door choice
            hint_door_options = set()
            for goal_location in multipath_dict_goals[loc]:
                if len(hint_door_options) == 0:
                    hint_door_options = set(spoiler.accessible_hints_for_location[goal_location])
                else:
                    hint_door_options = hint_door_options & set(spoiler.accessible_hints_for_location[goal_location])
            hint_location = None
            # If this location's goals do restrict the hint doors, choose your hint door carefully
            if len(hint_door_options) > 0:
                hint_options = getHintLocationsForAccessibleHintItems(hint_door_options)
                if len(hint_options) > 0:
                    hint_location = random.choice(hint_options)
            # If this location's goals do not restrict hint door location OR all the restricted hint door options are taken (staggeringly unlikely), get a random hint door
            if len(hint_door_options) == 0 or hint_location is None:
                hint_location = getRandomHintLocation()

            globally_hinted_location_ids.append(loc)
            region = GetRegionOfLocation(spoiler, loc)
            if region.hint_name != "Troff 'N' Scoff":
                hinted_location_text = level_colors[region.level] + region.hint_name + level_colors[region.level]
            else:
                hinted_location_text = level_colors[Levels.DKIsles] + region.hint_name + level_colors[Levels.DKIsles]
            if loc in TrainingBarrelLocations or loc in PreGivenLocations:
                # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                hinted_item_name = ItemList[spoiler.LocationList[loc].item].name
                message = f"Your \x0btraining with {hinted_item_name}\x0b is on the path to {multipath_dict_hints[loc]}."
            else:
                message = f"Something in the {hinted_location_text} is on the path to {multipath_dict_hints[loc]}."
            hint_location.related_location = loc
            hint_location.hint_type = HintType.Multipath
            UpdateHint(hint_location, message)
            if len(message) > 123:
                # In an attempt to avoid the dreaded '...' in the pause menu, remove more of the fluff for short_hint
                hint_location.short_hint = f"{hinted_location_text}: Path to {multipath_dict_hints[loc]}"

    # Key location hints should be placed at or before the level they are for (e.g. Key 4 shows up in level 4 lobby or earlier)
    if hint_distribution[HintType.RequiredKeyHint] > 0:
        for key_id in key_hint_dict:
            if key_hint_dict[key_id] == 0:
                continue
            # For early Keys 1-2, place one hint with their required Kong and the level they're in
            if key_id in (Items.JungleJapesKey, Items.AngryAztecKey) and level_order_matters and not spoiler.settings.hard_level_progression:
                globally_hinted_location_ids.append(key_location_ids[key_id])
                location = spoiler.LocationList[key_location_ids[key_id]]
                key_item = ItemList[key_id]
                kong_index = location.kong
                # Boss locations actually have a specific kong, go look it up
                if location.kong == Kongs.any and location.type == Types.Key and location.level != Levels.HideoutHelm:
                    kong_index = spoiler.settings.boss_kongs[location.level]
                if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                    if location.level == Levels.Shops:
                        level_name = "\x08" + random.choice(crankys_cryptic) + "\x08"
                    else:
                        level_name = "\x08" + random.choice(level_cryptic_helm_isles[location.level]) + "\x08"
                    kong_name = "\x07" + random.choice(kong_cryptic[kong_index]) + "\x07"
                else:
                    level_name = level_colors[location.level] + level_list[location.level] + level_colors[location.level]
                    kong_name = kong_list[kong_index]
                # Attempt to find a door that will be accessible before the Key
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[key_location_ids[key_id]])
                if len(hint_options) > 0:
                    hint_location = random.choice(hint_options)
                # If there are no doors available (pretty unlikely) then just get a random one. Tough luck.
                else:
                    hint_location = getRandomHintLocation()
                if location.type in item_type_names.keys():
                    location_name = item_type_names[location.type]
                    if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                        location_name = "\x06" + random.choice(item_type_names_cryptic[location.type]) + "\x06"
                    message = f"\x04{key_item.name}\x04 is held by {location_name} in {level_name}."
                elif location.type == Types.Shop:
                    message = f"\x04{key_item.name}\x04 can be bought in {level_name}."
                else:
                    message = f"\x04{key_item.name}\x04 can be acquired with {kong_name} in {level_name}."
                hint_location.related_location = key_location_ids[key_id]
                hint_location.hint_type = HintType.RequiredKeyHint
                UpdateHint(hint_location, message)
            # For later or complex Keys, place hints that hint the "path" to the key
            else:
                # Prevent the same hint referring to the same location twice
                # This means if you get a duplicate path hint, each hint refers to a different item
                already_hinted_locations = []
                for i in range(key_hint_dict[key_id]):
                    path = spoiler.woth_paths[key_location_ids[key_id]]
                    key_item = ItemList[key_id]
                    # Don't hint the Helm Key in Helm when you know it's there
                    if key_id == Items.HideoutHelmKey and spoiler.settings.key_8_helm:
                        path = [loc for loc in path if loc != Locations.HelmKey]
                    # Never hint the same location for the same path twice and avoid useless locations for Key 8 (if applicable)
                    hintable_location_ids = [loc for loc in path if loc not in already_hinted_locations and not (key_id == Items.HideoutHelmKey and loc in useless_locations[Items.HideoutHelmKey])]
                    path_location_id = random.choice(hintable_location_ids)
                    # Soft reroll duplicate hints based on hint reroll parameters
                    rerolls = 0
                    while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and random.random() <= hint_reroll_chance:
                        path_location_id = random.choice(hintable_location_ids)
                        rerolls += 1
                    # After this point, the path_location_id is locked in and cannot be changed!

                    globally_hinted_location_ids.append(path_location_id)
                    already_hinted_locations.append(path_location_id)
                    region = GetRegionOfLocation(spoiler, path_location_id)
                    if region.hint_name != "Troff 'N' Scoff":
                        hinted_location_text = level_colors[region.level] + region.hint_name + level_colors[region.level]
                    else:
                        hinted_location_text = level_colors[Levels.DKIsles] + region.hint_name + level_colors[Levels.DKIsles]
                    # Attempt to find a door that will be accessible before the Key
                    hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[key_location_ids[key_id]])
                    if len(hint_options) > 0:
                        hint_location = random.choice(hint_options)
                    # If there are no doors available (very unlikely) then just get a random one. Tough luck.
                    else:
                        hint_location = getRandomHintLocation()
                    if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                        # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                        hinted_item_name = ItemList[spoiler.LocationList[path_location_id].item].name
                        message = f"Your \x0btraining with {hinted_item_name}\x0b is on the path to \x04{key_item.name}\x04."
                    else:
                        message = f"Something in the {hinted_location_text} is on the path to \x04{key_item.name}\x04."
                    hint_location.related_location = path_location_id
                    hint_location.hint_type = HintType.RequiredKeyHint
                    UpdateHint(hint_location, message)

    # Some win conditions need very specific items that we really should hint
    if hint_distribution[HintType.RequiredWinConditionHint] > 0:
        # To aid K. Rool goals create a number of path hints to help find items required specifically for K. Rool
        if spoiler.settings.win_condition == WinCondition.beat_krool:
            path = spoiler.woth_paths[Locations.BananaHoard]
            already_chosen_krool_path_locations = []
            chosen_krool_path_location_cap = hint_distribution[HintType.RequiredWinConditionHint]
            while len(already_chosen_krool_path_locations) < chosen_krool_path_location_cap:
                hintable_location_ids = [loc for loc in path if loc not in already_chosen_krool_path_locations and loc != Locations.BananaHoard]
                if len(hintable_location_ids) == 0 and spoiler.settings.wrinkly_hints == WrinklyHints.fixed_racing:
                    # This rarely happens when you're on a fixed hint distribution - some specific fills can have fewer items on the path to K. Rool than you have dedicated hints for
                    # It could also happen if you start with a ton of moves
                    hint_location = getRandomHintLocation()
                    hint_location.hint_type = HintType.RequiredWinConditionHint
                    message = "\x05Very little\x05 is on the path to \x0ddefeating K. Rool.\x0d"  # So we'll hint exactly that - there's very little on the path to K. Rool
                    UpdateHint(hint_location, message)
                    chosen_krool_path_location_cap -= 1  # This is a K. Rool hint, but isn't a location so we have to lower the cap on the loop
                    continue
                path_location_id = random.choice(hintable_location_ids)
                # Soft reroll duplicate hints based on hint reroll parameters
                rerolls = 0
                while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and random.random() <= hint_reroll_chance:
                    path_location_id = random.choice(hintable_location_ids)
                    rerolls += 1
                # After this point, the path_location_id is locked in and cannot be changed!

                # Determine what phases this item could be for
                phases_needing_this_item = [kong for kong in spoiler.krool_paths.keys() if path_location_id in spoiler.krool_paths[kong]]  # All phases this item is on the path to
                useless_kongs = [
                    kong for kong in phases_needing_this_item if path_location_id in useless_locations[kong]
                ]  # All kongs that it would be useless to hint for (e.g. Training in Peanut is path to Diddy K. Rool)
                hintable_phases = [kong for kong in phases_needing_this_item if kong not in useless_kongs]
                # If there are no valid phases to hint for this location, it's a training barrel with no useful information
                if len(hintable_phases) == 0:
                    # Therefore, we treat it as hinted and go again - this may lead to more often "very little is on the path" hints but that's fine cause it's still true
                    already_chosen_krool_path_locations.append(path_location_id)
                    chosen_krool_path_location_cap += 1  # Increment this by one so we go through the loop an extra time and don't lose a hint
                    continue
                hinted_kong = random.choice(hintable_phases)
                hinted_item_id = spoiler.LocationList[path_location_id].item
                # Every hint door is available before K. Rool so we can pick randomly...
                hint_location = getRandomHintLocation()
                # ...unless the hinted location is specifically the end of a phase path - in this case, we do not want the hint to lock itself
                if (
                    (hinted_kong == Kongs.diddy and hinted_item_id in (Items.Peanut, Items.RocketbarrelBoost))
                    or (hinted_kong == Kongs.lanky and hinted_item_id in (Items.Barrels, Items.Trombone))
                    or (hinted_kong == Kongs.tiny and hinted_item_id in (Items.Feather, Items.MiniMonkey))
                    or (hinted_kong == Kongs.chunky and hinted_item_id in (Items.ProgressiveSlam, Items.PrimatePunch, Items.HunkyChunky, Items.GorillaGone))
                ):
                    hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[path_location_id])
                    # If no hint options are available (this should be quite unlikely), it will default to the random one
                    if len(hint_options) > 0:
                        hint_location = random.choice(hint_options)
                globally_hinted_location_ids.append(path_location_id)
                already_chosen_krool_path_locations.append(path_location_id)
                # Begin to build the hint - determine the region of the location
                region = GetRegionOfLocation(spoiler, path_location_id)
                if region.hint_name != "Troff 'N' Scoff":  # Quick color-correction so that the color of "Troff 'N' Scoff" doesn't leak the level
                    hinted_location_text = level_colors[region.level] + region.hint_name + level_colors[region.level]
                else:
                    hinted_location_text = level_colors[Levels.DKIsles] + region.hint_name + level_colors[Levels.DKIsles]
                kong_color = kong_colors[hinted_kong]
                if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                    # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                    hinted_item_name = ItemList[hinted_item_id].name
                    message = f"Your \x0btraining with {hinted_item_name}\x0b is on the path to {kong_color} {colorless_kong_list[hinted_kong]}'s K. Rool fight.{kong_color}"
                else:
                    message = f"Something in the {hinted_location_text} is on the path to {kong_color} {colorless_kong_list[hinted_kong]}'s K. Rool fight.{kong_color}"
                hint_location.related_location = path_location_id
                hint_location.hint_type = HintType.RequiredWinConditionHint
                UpdateHint(hint_location, message)
        # All fairies seeds get 2 path hints for the camera
        if spoiler.settings.win_condition == WinCondition.all_fairies or spoiler.settings.win_condition == WinCondition.poke_snap:
            camera_location_id = None
            for location_id in spoiler.woth_paths.keys():
                if spoiler.LocationList[location_id].item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = location_id
                    break
            path = spoiler.woth_paths[camera_location_id]
            already_chosen_camera_path_locations = []
            for i in range(hint_distribution[HintType.RequiredWinConditionHint]):
                hintable_location_ids = [loc for loc in path if loc not in already_chosen_camera_path_locations]
                path_location_id = random.choice(hintable_location_ids)
                # Soft reroll duplicate hints based on hint reroll parameters
                rerolls = 0
                while rerolls < hint_reroll_cap and path_location_id in globally_hinted_location_ids and random.random() <= hint_reroll_chance:
                    path_location_id = random.choice(hintable_location_ids)
                    rerolls += 1
                # After this point, the path_location_id is locked in and cannot be changed!

                globally_hinted_location_ids.append(path_location_id)
                already_chosen_camera_path_locations.append(path_location_id)
                region = GetRegionOfLocation(spoiler, path_location_id)
                if region.hint_name != "Troff 'N' Scoff":
                    hinted_location_text = level_colors[region.level] + region.hint_name + level_colors[region.level]
                else:
                    hinted_location_text = level_colors[Levels.DKIsles] + region.hint_name + level_colors[Levels.DKIsles]
                # Attempt to find a door that will be accessible before the Camera
                hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[camera_location_id])
                if len(hint_options) > 0:
                    hint_location = random.choice(hint_options)
                # If there are no doors available (unlikely by now) then just get a random one. Tough luck.
                else:
                    hint_location = getRandomHintLocation()
                if path_location_id in TrainingBarrelLocations or path_location_id in PreGivenLocations:
                    # Starting moves could be a lot of things - instead of being super vague we'll hint the specific item directly.
                    hinted_item_name = ItemList[spoiler.LocationList[path_location_id].item].name
                    message = f"Your \x0btraining with {hinted_item_name}\x0b is on the path to \x07taking photos\x07."
                else:
                    message = f"Something in the {hinted_location_text} is on the path to \x07taking photos\x07."
                hint_location.related_location = path_location_id
                hint_location.hint_type = HintType.RequiredWinConditionHint
                UpdateHint(hint_location, message)

    # Moves should be hinted before they're available
    moves_hinted_and_lobbies = {}  # Avoid putting a hint for the same move in the same lobby twice
    locationless_move_keys = []  # Keep track of moves we know have run out of locations to hint
    placed_move_hints = 0
    while placed_move_hints < hint_distribution[HintType.MoveLocation]:
        # First pick a random item from the WOTH - valid items are moves (not kongs) and must not be one of our known impossible-to-place items
        woth_item = None
        valid_woth_item_locations = [loc for loc in spoiler.woth_locations if loc not in locationless_move_keys and spoiler.LocationList[loc].type == Types.Shop]
        if len(valid_woth_item_locations) == 0:
            # In the OBSCENELY rare case that we can't hint any more moves, then we'll settle for joke hints
            # This would only happen in the case where all moves are in early worlds, coins are plentiful, and the distribution here is insanely high
            # Your punishment for these extreme settings is more joke hints
            hint_diff = hint_distribution[HintType.MoveLocation] - placed_move_hints
            hint_distribution[HintType.Joke] += hint_diff
            hint_distribution[HintType.MoveLocation] -= hint_diff
            break
        woth_item_location = random.choice(valid_woth_item_locations)
        index_of_level_with_location = spoiler.LocationList[woth_item_location].level
        # Now we need to find the Item object associated with this name
        woth_item = spoiler.LocationList[woth_item_location].item
        # Don't hint slams with these hints - it's slightly misleading and saves some headache to not do this
        if woth_item == Items.ProgressiveSlam:
            continue
        # Determine what levels are before this level
        hintable_levels = all_levels.copy()
        # Only if we care about the level order do we restrict these hints' locations
        # We lack the tools (or creativity) to figure out proper locations for hints in hard level progression (for now?)
        if level_order_matters and not spoiler.settings.hard_level_progression:
            # Determine a sorted order of levels by B. Lockers - this may not be the actual "progression" but it'll do for now
            levels_in_order = all_levels.copy()
            levels_in_order.sort(key=lambda l: spoiler.settings.EntryGBs[l])

            hintable_levels = []
            cheapest_levels_with_item = []
            # Go through our levels in progression order
            for level in levels_in_order:
                # If the level doesn't have access to the move, we can hint it in the lobby
                if woth_item not in spoiler.settings.owned_moves_by_level[level]:
                    hintable_levels.append(level)
                # We hit our first level that has logical access to the move, time to get to work
                else:
                    # Find all levels with B. Lockers of the same price as this one
                    cheapest_levels_candidates = [
                        candidate for candidate in all_levels if spoiler.settings.EntryGBs[candidate] == spoiler.settings.EntryGBs[level] and candidate not in hintable_levels
                    ]
                    # If there's only one candidate then this is the level that gives logical access to the move, so we're done
                    # If it's an Isles shop we're hinting we don't need to pare down the lobby options, so we're done
                    if len(cheapest_levels_candidates) == 1 or index_of_level_with_location >= 7:
                        cheapest_levels_with_item = cheapest_levels_candidates
                    # In normal level progression, we need to remove levels that are beyond the shop's level
                    else:
                        # Determine the level order of the shop
                        level_order_of_shop_location = -1
                        for order in spoiler.settings.level_order:
                            if index_of_level_with_location == spoiler.settings.level_order[order]:
                                level_order_of_shop_location = order
                                break
                        # For each of our cheap levels
                        for cheap_level in cheapest_levels_candidates:
                            # Get the level order of this cheap level (will only match one)
                            cheap_level_order = [o for o in spoiler.settings.level_order if cheap_level == spoiler.settings.level_order[o]][0]
                            # If this level is before our shop's level in the order, it can have the hint
                            if cheap_level_order <= level_order_of_shop_location:
                                cheapest_levels_with_item.append(cheap_level)
                    break
            # We can also hint the cheapest levels that have access to this item
            # This manifests in the form of finding a hint in Japes lobby for Pineapple in an earlier level if Chunky is unlocked in Japes
            hintable_levels.extend(cheapest_levels_with_item)
        # Don't place the same hint in the same lobby
        if woth_item in moves_hinted_and_lobbies.keys():
            for lobby_with_this_hint in moves_hinted_and_lobbies[woth_item]:
                if lobby_with_this_hint in hintable_levels:
                    hintable_levels.remove(lobby_with_this_hint)
        else:
            moves_hinted_and_lobbies[woth_item] = []

        hint_location = getRandomHintLocation(levels=hintable_levels, move_name=ItemList[woth_item].name)
        # If we've been too restrictive and ran out of spots for this move to be hinted in, don't bother trying to fix it. Just pick another move
        if hint_location is None:
            locationless_move_keys.append(woth_item_location)
            continue

        shop_level = level_colors[index_of_level_with_location] + level_list[index_of_level_with_location] + level_colors[index_of_level_with_location]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            shop_level = "\x08" + random.choice(level_cryptic_helm_isles[index_of_level_with_location]) + "\x08"
        shop_name = shop_owners[spoiler.LocationList[woth_item_location].vendor]
        message = f"On the Way of the Hoard, \x05{ItemList[woth_item].name}\x05 is bought from {shop_name} in {shop_level}."
        moves_hinted_and_lobbies[woth_item].append(hint_location.level)
        hint_location.related_location = woth_item_location
        hint_location.hint_type = HintType.MoveLocation
        UpdateHint(hint_location, message)
        placed_move_hints += 1

    # For T&S hints, we want to hint levels after the hint location and only levels that we don't start with keys for
    if hint_distribution[HintType.TroffNScoff] > 0:
        # Determine what levels have incomplete T&S
        levels_with_tns = []
        for keyEvent in spoiler.settings.krool_keys_required:
            if keyEvent == Events.JapesKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[1])
            if keyEvent == Events.AztecKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[2])
            if keyEvent == Events.FactoryKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[3])
            if keyEvent == Events.GalleonKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[4])
            if keyEvent == Events.ForestKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[5])
            if keyEvent == Events.CavesKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[6])
            if keyEvent == Events.CastleKeyTurnedIn:
                levels_with_tns.append(spoiler.settings.level_order[7])
        placed_tns_hints = 0
        while placed_tns_hints < hint_distribution[HintType.TroffNScoff]:
            attempts = 0
            # Make sure the location we randomly pick either is a level or is before a level that has a T&S
            future_tns_levels = []
            while not any(future_tns_levels):
                # If you can't find a location that can fit a T&S hint in 15 tries, it's either impossible or very likely redundant
                attempts += 1
                if attempts > 15:
                    break
                hint_location = getRandomHintLocation()
                future_tns_levels = [
                    level for level in all_levels if level in levels_with_tns and (not level_order_matters or spoiler.settings.EntryGBs[level] >= spoiler.settings.EntryGBs[hint_location.level])
                ]
            # If we failed to find it in 15 attempts, convert remaining T&S hints to joke hints
            # This is a disgustingly rare scenario, likely involving very few and early keys required
            if attempts > 15:
                hint_diff = hint_distribution[HintType.TroffNScoff] - placed_tns_hints
                hint_distribution[HintType.Joke] += hint_diff
                hint_distribution[HintType.TroffNScoff] -= hint_diff
                break
            hinted_level = random.choice(future_tns_levels)
            level_name = level_colors[hinted_level] + level_list[hinted_level] + level_colors[hinted_level]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                level_name = "\x08" + random.choice(level_cryptic[hinted_level]) + "\x08"
            count = spoiler.settings.BossBananas[hinted_level]
            cb_name = "Small Bananas"
            if count == 1:
                cb_name = "Small Banana"
            message = f"The barrier to the boss in {level_name} can be cleared by obtaining \x04{count} {cb_name}\x04."
            hint_location.hint_type = HintType.TroffNScoff
            UpdateHint(hint_location, message)
            placed_tns_hints += 1

    # WotH Location hints list a location that is Way of the Hoard. Most applicable in item rando.
    if hint_distribution[HintType.WothLocation] > 0:
        hintable_location_ids = []
        for location_id in spoiler.woth_locations:
            location = spoiler.LocationList[location_id]
            # Only hint things that are in shuffled locations - don't hint starting moves because you can't know which move it refers to and don't hint the Helm Key if you know key 8 is there
            if (
                location.type in spoiler.settings.shuffled_location_types
                and location.type not in (Types.TrainingBarrel, Types.PreGivenMove)
                and not (spoiler.settings.key_8_helm and location_id == Locations.HelmKey)
            ):
                hintable_location_ids.append(location_id)
        random.shuffle(hintable_location_ids)
        placed_woth_hints = 0
        while placed_woth_hints < hint_distribution[HintType.WothLocation]:
            # If you run out of hintable woth locations, throw in a foolish for their troubles - this should only happen if there's very few late woth locations.
            # In (increasingly) obscenely rare circumstances, this might affect the Fixed distribution. I think this is too subtle to actually matter.
            if len(hintable_location_ids) == 0:
                hint_distribution[HintType.WothLocation] -= 1
                hint_distribution[HintType.FoolishRegion] += 1
                continue
            hinted_loc_id = random.choice(hintable_location_ids)
            # Soft reroll duplicate hints based on hint reroll parameters
            rerolls = 0
            while rerolls < hint_reroll_cap and hinted_loc_id in globally_hinted_location_ids and random.random() <= hint_reroll_chance:
                hinted_loc_id = random.choice(hintable_location_ids)
                rerolls += 1
            # After this point, the path_location_id is locked in and cannot be changed!

            globally_hinted_location_ids.append(hinted_loc_id)
            hintable_location_ids.remove(hinted_loc_id)
            # Attempt to find a door that will be accessible before the location is
            hint_options = getHintLocationsForAccessibleHintItems(spoiler.accessible_hints_for_location[hinted_loc_id])
            if len(hint_options) > 0:
                hint_location = random.choice(hint_options)
            # If there are no doors available, it's likely a very early woth location. Go find a better location to hint.
            else:
                continue
            hint_color = level_colors[spoiler.LocationList[hinted_loc_id].level]
            message = f"{hint_color}{spoiler.LocationList[hinted_loc_id].name}{hint_color} is on the \x04Way of the Hoard\x04."
            hint_location.related_location = hinted_loc_id
            hint_location.hint_type = HintType.WothLocation
            UpdateHint(hint_location, message)
            placed_woth_hints += 1

    # Foolish Region hints state that a hint region is foolish. Useful in item rando.
    # Foolish regions contain no major items that would block any amount of progression, even non-required progression
    if hint_distribution[HintType.FoolishRegion] > 0:
        # Determine how many locations are contained in the foolish regions
        total_foolish_location_score = 0
        foolish_region_location_score = {}
        for foolish_name in spoiler.foolish_region_names:
            foolish_location_score = 0
            shops_in_region = 0
            regions_in_region = [region for region in spoiler.RegionList.values() if region.hint_name == foolish_name]
            for region in regions_in_region:
                foolish_location_score += len(
                    [loc for loc in region.locations if not spoiler.LocationList[loc.id].inaccessible and spoiler.LocationList[loc.id].type in spoiler.settings.shuffled_location_types]
                )
                if region.level == Levels.Shops and region.hint_name != "Jetpac Game":  # Jetpac isn't a "real" shop, it's in the Shops level for convenience
                    shops_in_region += 1
            if "Medal Rewards" in foolish_name:  # "Medal Rewards" regions are cb foolish hints, which are just generally more valuable to hint foolish
                foolish_location_score += 3
            elif shops_in_region > 0:  # Shops are generally overvalued (4/6 locations per shop) with this method due to having mutually exclusive locations
                foolish_location_score -= 1 * shops_in_region  # With smaller shops, this reduces the location count to 3 locations per shop
                if foolish_location_score < 0:  # Prevent negative scores
                    foolish_location_score = 0
            foolish_location_score = foolish_location_score**1.25  # Exponentiation of this score puts additional emphasis (but not too much) on larger regions
            total_foolish_location_score += foolish_location_score
            foolish_region_location_score[foolish_name] = foolish_location_score
        random.shuffle(spoiler.foolish_region_names)
        for i in range(hint_distribution[HintType.FoolishRegion]):
            # If you run out of foolish regions (maybe in an all medals run?) - this *should* be covered by the distribution earlier but this is a good failsafe
            if len(spoiler.foolish_region_names) == 0 or sum(foolish_region_location_score.values()) == 0:  # You can either expend the whole list or run out of eligible regions
                # Replace remaining move hints with region item count hints, because it sounds like you need em
                hint_distribution[HintType.FoolishRegion] -= 1
                hint_distribution[HintType.RegionItemCount] += 1
                continue
            hinted_region_name = random.choices(list(foolish_region_location_score.keys()), foolish_region_location_score.values())[0]  # Weighted random choice from list of foolish region names
            spoiler.foolish_region_names.remove(hinted_region_name)
            del foolish_region_location_score[hinted_region_name]
            hint_location = getRandomHintLocation()
            level_color = "\x05"
            for region_id in Regions:
                if spoiler.RegionList[region_id].hint_name == hinted_region_name:
                    level_color = level_colors[spoiler.RegionList[region_id].level]
                    break
            if "Medal Rewards" in hinted_region_name:
                cutoff = hinted_region_name.index(" Medal Rewards")
                message = f"It would be \x05foolish\x05 to collect {level_color}colored bananas in {hinted_region_name[0:cutoff]}{level_color}."
            else:
                message = f"It would be \x05foolish\x05 to explore the {level_color}{hinted_region_name}{level_color}."
            hint_location.hint_type = HintType.FoolishRegion
            UpdateHint(hint_location, message)

    # TEMPORARILY SHELVED - may revisit in the future with either more processing power or a more clever approach
    # Pathless hints are the evolution of foolish moves - it hints a move that is not on the path to anything else.
    # You may use a pathless move as a part of an either/or, but it will not be strictly required for anything.
    # Slams are banned from being hinted this way cause I do not want to deal with that *at all*
    # Hints are weighted towards more impactful things: guns, instruments, and good training moves.
    if hint_distribution[HintType.ForeseenPathless] > 0:
        pathless_move_score = {}
        for move in spoiler.pathless_moves:
            # Some moves are just better than others - these are less likely to not be on paths, and it's really good to know that.
            if move in [
                Items.Coconut,  # All the guns
                Items.Peanut,
                Items.Grape,
                Items.Feather,
                Items.Pineapple,
                Items.Bongos,  # All the instruments
                Items.Guitar,
                Items.Trombone,
                Items.Saxophone,
                Items.Triangle,
                Items.Barrels,  # All the good training moves
                Items.Vines,
                Items.Swim,
                Items.Camera,  # Camera and Shockwave
                Items.Shockwave,
                Items.CameraAndShockwave,
                Items.RocketbarrelBoost,  # A few extra moves that are particularly useful
                Items.MiniMonkey,
                Items.PrimatePunch,
            ]:
                pathless_move_score[move] = 4  # These moves are four times as likely as any other move to get picked now
            else:
                pathless_move_score[move] = 1
        for i in range(hint_distribution[HintType.ForeseenPathless]):
            # If somehow you end up with more hints than there are pathless moves...
            if len(pathless_move_score.keys()) <= 0:
                # Convert to region item count hints because it sounds like you need em
                hint_distribution[HintType.ForeseenPathless] -= 1
                hint_distribution[HintType.RegionItemCount] += 1
                continue
            pathless_item = random.choices(list(pathless_move_score.keys()), pathless_move_score.values())[0]
            del pathless_move_score[pathless_item]
            hint_location = getRandomHintLocation()
            message = f"I have foreseen that there are \x0bno paths to the Hoard\x0b which contain \x04{ItemList[pathless_item].name}\x04."
            hint_location.hint_type = HintType.ForeseenPathless
            UpdateHint(hint_location, message)

    # Region Item Count hints tell you how many potions are in contained in the entirety of a hint region.
    # Currently it randomly picks a region that has a non-zero amount of potions in it, but it cannot hint shop regions.
    if hint_distribution[HintType.RegionItemCount] > 0:
        hintable_region_names = list(spoiler.region_hintable_count.keys())
        random.shuffle(hintable_region_names)
        for i in range(hint_distribution[HintType.RegionItemCount]):
            # If somehow you end up with more hints than there are regions with moves in them...
            if len(hintable_region_names) <= 0:
                # You made some meme of a seed so have some meme hints
                hint_distribution[HintType.RegionItemCount] -= 1
                hint_distribution[HintType.Joke] += 1
                continue
            region_name_to_hint = hintable_region_names.pop()
            hint_location = getRandomHintLocation()
            level_color = "\x05"
            for region_id in Regions:
                if spoiler.RegionList[region_id].hint_name == region_name_to_hint:
                    level_color = level_colors[spoiler.RegionList[region_id].level]
                    break
            plural = ""
            if spoiler.region_hintable_count[region_name_to_hint] > 1:
                plural = "s"
            message = f"Scouring the {level_color}{region_name_to_hint}{level_color} will yield you \x0d{spoiler.region_hintable_count[region_name_to_hint]} potion{plural}\x0d."
            hint_location.hint_type = HintType.RegionItemCount
            UpdateHint(hint_location, message)

    # Entrance hints are tricky, there's some requirements we must hit:
    # We must hint each of Japes, Aztec, and Factory at least once
    # The rest of the hints are tied to a variety of important locations
    if hint_distribution[HintType.Entrance] > 0:
        criticalJapesRegions = [Regions.JungleJapesStart, Regions.JungleJapesMain, Regions.JapesBeyondFeatherGate, Regions.TinyHive, Regions.JapesLankyCave, Regions.Mine]
        criticalAztecRegions = [
            Regions.AngryAztecStart,
            Regions.AngryAztecOasis,
            Regions.AngryAztecMain,
            Regions.DonkeyTemple,
            Regions.DiddyTemple,
            Regions.LankyTemple,
            Regions.TinyTemple,
            Regions.ChunkyTemple,
        ]
        criticalFactoryRegions = [Regions.FranticFactoryStart, Regions.ChunkyRoomPlatform, Regions.PowerHut, Regions.BeyondHatch, Regions.LowerCore, Regions.InsideCore]
        usefulRegions = [
            criticalJapesRegions,
            criticalAztecRegions,
            criticalFactoryRegions,
            [Regions.BananaFairyRoom],
            [Regions.TrainingGrounds],
            [Regions.GloomyGalleonStart, Regions.LighthousePlatform, Regions.LighthouseUnderwater, Regions.ShipyardUnderwater, Regions.Shipyard],
            [Regions.FungiForestStart, Regions.GiantMushroomArea, Regions.MushroomLowerExterior, Regions.MushroomNightExterior, Regions.MushroomUpperExterior, Regions.MillArea, Regions.ThornvineArea],
            [Regions.CrystalCavesMain, Regions.IglooArea, Regions.CabinArea],
            [Regions.CreepyCastleMain, Regions.CastleWaterfall],
            [Regions.LowerCave],
            [Regions.UpperCave],
        ]
        placed_entrance_hints = 0
        while placed_entrance_hints < hint_distribution[HintType.Entrance]:
            message = ""
            # Always put in at least one Japes hint
            if placed_entrance_hints == 0:
                japesHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalJapesRegions]
                random.shuffle(japesHintEntrances)
                japesHintPlaced = False
                while len(japesHintEntrances) > 0:
                    japesHinted = japesHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, japesHinted, criticalJapesRegions)
                    if message != "":
                        japesHintPlaced = True
                        break
                if not japesHintPlaced:
                    print("Japes LZR hint unable to be placed!")
            # Always put in at least one Aztec hint
            elif placed_entrance_hints == 1:
                aztecHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalAztecRegions]
                random.shuffle(aztecHintEntrances)
                aztecHintPlaced = False
                while len(aztecHintEntrances) > 0:
                    aztecHinted = aztecHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, aztecHinted, criticalAztecRegions)
                    if message != "":
                        aztecHintPlaced = True
                        break
                if not aztecHintPlaced:
                    print("Aztec LZR hint unable to be placed!")
            # Always put in at least one Factory hint
            elif placed_entrance_hints == 2:
                factoryHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalFactoryRegions]
                random.shuffle(factoryHintEntrances)
                factoryHintPlaced = False
                while len(factoryHintEntrances) > 0:
                    factoryHinted = factoryHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, factoryHinted, criticalFactoryRegions)
                    if message != "":
                        factoryHintPlaced = True
                        break
                if not factoryHintPlaced:
                    print("Factory LZR hint unable to be placed!")
            else:
                region_to_hint = random.choice(usefulRegions)
                usefulHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in region_to_hint]
                random.shuffle(usefulHintEntrances)
                usefulHintPlaced = False
                while len(usefulHintEntrances) > 0:
                    usefulHinted = usefulHintEntrances.pop()
                    message = TryCreatingLoadingZoneHint(spoiler, usefulHinted, region_to_hint)
                    if message != "":
                        usefulHintPlaced = True
                        break
                if not usefulHintPlaced:
                    print(f"Useful LZR hint to {usefulHinted.name} unable to be placed!")
            if message == "":
                # Then we somehow managed to fail to create a hint. This is real bad but we'll just laugh it off with a joke hint. Hahaha!
                hint_distribution[HintType.Entrance] -= 1
                hint_distribution[HintType.Joke] += 1
                continue
            hint_location = getRandomHintLocation()
            hint_location.hint_type = HintType.Entrance
            UpdateHint(hint_location, message)
            placed_entrance_hints += 1

    # If any Helm doors are random, place a hint for each random door somewhere
    if hint_distribution[HintType.RequiredHelmDoorHint] > 0:
        helmdoor_vars = {
            HelmDoorItem.req_gb: "Golden Banana",
            HelmDoorItem.req_bp: "Blueprint",
            HelmDoorItem.req_companycoins: "Special Coin",
            HelmDoorItem.req_key: "Key",
            HelmDoorItem.req_medal: "Medal",
            HelmDoorItem.req_crown: "Crown",
            HelmDoorItem.req_fairy: "Fairy",
            HelmDoorItem.req_rainbowcoin: "Rainbow Coin",
            HelmDoorItem.req_bean: "Bean",
            HelmDoorItem.req_pearl: "Pearl",
        }
        if spoiler.settings.crown_door_random:
            item_name = helmdoor_vars[spoiler.settings.crown_door_item]
            if spoiler.settings.crown_door_item_count > 1:
                if spoiler.settings.crown_door_item == HelmDoorItem.req_fairy:
                    item_name = "Fairies"  # English is so rude sometimes
                else:
                    item_name = item_name + "s"
            hint_location = getRandomHintLocation()
            message = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{spoiler.settings.crown_door_item_count} {item_name}\x04."
            hint_location.hint_type = HintType.RequiredHelmDoorHint
            UpdateHint(hint_location, message)
        if spoiler.settings.coin_door_random:
            item_name = helmdoor_vars[spoiler.settings.coin_door_item]
            if spoiler.settings.coin_door_item_count > 1:
                if spoiler.settings.coin_door_item == HelmDoorItem.req_fairy:
                    item_name = "Fairies"  # Plurals? Consistency? A pipe dream
                else:
                    item_name = item_name + "s"
            hint_location = getRandomHintLocation()
            message = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{spoiler.settings.coin_door_item_count} {item_name}\x04."
            hint_location.hint_type = HintType.RequiredHelmDoorHint
            UpdateHint(hint_location, message)

    # Full Shop With Items hints are essentially a rework of shop dump hints but with the ability to list any item instead of just moves.
    chosen_shops = []
    for i in range(hint_distribution[HintType.FullShopWithItems]):
        # Shared shop lists are a convenient list of all individual shops in the game, regardless of if something is there
        shared_shop_location = random.choice([shop for shop in SharedShopLocations if shop not in chosen_shops])
        # Ensure we always hint unique shops
        chosen_shops.append(shared_shop_location)
        # Get the level and vendor type from that location
        shop_info = spoiler.LocationList[shared_shop_location]
        # Find all locations for this shop
        kongLocationsAtThisShop = [
            location
            for id, location in spoiler.LocationList.items()
            if location.type == Types.Shop and location.level == shop_info.level and location.vendor == shop_info.vendor and location.kong != Kongs.any
        ]
        # If this is a shared shop dump...
        if shop_info.item is not None and shop_info.item != Items.NoItem:
            shop_vendor = shop_owners[shop_info.vendor]
            level_name = level_colors[shop_info.level] + level_list[shop_info.level] + level_colors[shop_info.level]
            if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
                level_name = "\x08" + random.choice(level_cryptic_helm_isles[shop_info.level]) + "\x08"
            move_series = ItemList[shop_info.item].name
        # Else this is a series of Kong-specific purchases
        else:
            random.shuffle(kongLocationsAtThisShop)  # Shuffle this list so you don't know who buys what
            item_names = [ItemList[location.item].name for location in kongLocationsAtThisShop if location.item is not None and location.item != Items.NoItem]
            if len(item_names) == 0:
                move_series = "nothing"
            else:
                move_series = item_names[0]
                if len(item_names) > 1:
                    move_series = f"{', '.join(item_names[:-1])}, and {item_names[-1]}"
        shop_vendor = shop_owners[shop_info.vendor]
        level_name = level_colors[shop_info.level] + level_list[shop_info.level] + level_colors[shop_info.level]
        if spoiler.settings.wrinkly_hints == WrinklyHints.cryptic:
            level_name = "\x08" + random.choice(level_cryptic_helm_isles[shop_info.level]) + "\x08"
        hint_location = getRandomHintLocation()
        message = f"{shop_vendor}'s in {level_name} contains {move_series}."
        hint_location.hint_type = HintType.FullShopWithItems
        UpdateHint(hint_location, message)

    # At least one Helm Order hint should be placed, but they can be placed randomly. If the player needs the info, they can seek it out.
    for i in range(hint_distribution[HintType.HelmOrder]):
        hint_location = getRandomHintLocation()
        default_order = [Kongs.donkey, Kongs.chunky, Kongs.tiny, Kongs.lanky, Kongs.diddy]
        helm_order = [default_order[room] for room in spoiler.settings.helm_order]
        kong_helm_order = [kong_list[x] for x in helm_order]
        kong_helm_text = ", then ".join(kong_helm_order)
        associated_hint = f"The \x05Blast-O-Matic\x05 can be disabled by using {kong_helm_text}."
        hint_location.hint_type = HintType.HelmOrder
        UpdateHint(hint_location, associated_hint)

    # No need to do anything fancy here - there's often already a K. Rool hint on the player's path (the wall in Helm)
    for i in range(hint_distribution[HintType.KRoolOrder]):
        hint_location = getRandomHintLocation()
        kong_krool_order = [kong_list[kong] for kong in spoiler.settings.krool_order]
        kong_krool_text = ", then ".join(kong_krool_order)
        associated_hint = f"\x08King K. Rool\x08 will face off in the ring against {kong_krool_text}."
        hint_location.hint_type = HintType.KRoolOrder
        UpdateHint(hint_location, associated_hint)

    # Dirt patch hints are already garbage anyway - no restrictions here
    # for i in range(hint_distribution[HintType.DirtPatch]):
    #     dirt_patch_name = random.choice(spoiler.dirt_patch_placement)
    #     hint_location = getRandomHintLocation()
    #     message = f"There is a dirt patch located at {dirt_patch_name}"
    #     hint_location.hint_type = HintType.DirtPatch
    #     UpdateHint(hint_location, message)

    # Very useless hint, can be found at Cranky's anyway
    # for i in range(hint_distribution[HintType.MedalsRequired]):
    #     hint_location = getRandomHintLocation()
    #     message = f"{spoiler.settings.medal_requirement} medals are required to access Jetpac."
    #     hint_location.hint_type = HintType.MedalsRequired
    #     UpdateHint(hint_location, message)

    # Finally, place our joke hints
    for i in range(hint_distribution[HintType.Joke]):
        hint_location = getRandomHintLocation()
        if i > 4:
            message = "What do you think I am, a comedian? Try again in another seed."
        else:
            joke_hint_list = hint_list.copy()
            random.shuffle(joke_hint_list)
            message = joke_hint_list.pop().hint
        # Way of the Bean joke hint - yes, this IS worth it
        if message == "[[WOTB]]":
            bean_location_id = None
            for id, location in spoiler.LocationList.items():
                if location.item == Items.Bean:
                    bean_location_id = id
            # If we didn't find the bean, just get another joke hint :(
            if bean_location_id is None:
                message = joke_hint_list.pop()
            else:
                bean_region = GetRegionOfLocation(spoiler, bean_location_id)
                hinted_location_text = bean_region.hint_name
                be_verb = "is"
                if hinted_location_text[-1] == "s":
                    be_verb = "are"
                message = f"The {hinted_location_text} {be_verb} on the Way of the Bean."
                hint_location.related_location = bean_location_id
        hint_location.hint_type = HintType.Joke
        UpdateHint(hint_location, message)

    UpdateSpoilerHintList(spoiler)
    spoiler.hint_distribution = hint_distribution

    # Dim hints - these are only useful (and doable) if item rando is on
    if spoiler.settings.dim_solved_hints and spoiler.settings.shuffle_items:
        AssociateHintsWithFlags(spoiler)

    # # DEBUG CODE to alert when a hint is empty
    # for hint in hints:
    #     if hint.hint == "":
    #         print("RED ALERT")

    return True


def getRandomHintLocation(location_list=None, kongs=None, levels=None, move_name=None) -> HintLocation:
    """Return an unoccupied hint location. The parameters can be used to specify location requirements."""
    valid_unoccupied_hint_locations = [
        hint
        for hint in hints
        if hint.hint == ""
        and (location_list is None or hint in location_list)
        and (kongs is None or hint.kong in kongs)
        and (levels is None or hint.level in levels)
        and move_name not in hint.banned_keywords
    ]
    # If it's too specific, we may not be able to find any
    if len(valid_unoccupied_hint_locations) == 0:
        return None
    hint_location = random.choice(valid_unoccupied_hint_locations)
    # Update the reference so we're updating the main list instead of a copy of it
    for hint in hints:
        if hint.name == hint_location.name:
            return hint
    return None


def getHintLocationsForAccessibleHintItems(hint_item_ids: Union[Set[Items], List[Items]]) -> List[Union[HintLocation, Any]]:
    """Given a list of hint item ids, return unoccupied HintLocation objects they correspond to, possibly returning an empty list."""
    accessible_hints = []
    for item_id in hint_item_ids:
        item = ItemList[item_id]
        matching_hint = [hint for hint in hints if hint.level == item.level and hint.kong == item.kong][0]  # Should only match one
        accessible_hints.append(matching_hint)
    return [hint for hint in accessible_hints if hint.hint == ""]  # Filter out the occupied ones


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


def getHelmProgItems(spoiler: Spoiler) -> list:
    """Get the items needed to progress to helm."""
    base_list = [Items.Monkeyport, Items.GorillaGone]
    if spoiler.settings.switchsanity:
        switch_item_data = {
            SwitchType.PadMove: [Items.BaboonBlast, Items.SimianSpring, Items.BaboonBalloon, Items.Monkeyport, Items.GorillaGone],
            SwitchType.InstrumentPad: [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle],
            SwitchType.MiscActivator: [Items.GorillaGrab, Items.ChimpyCharge],
        }
        switches = [Switches.IslesMonkeyport, Switches.IslesHelmLobbyGone]
        for switch_index, switch in enumerate(switches):
            data = spoiler.settings.switchsanity_data[switch]
            base_list[switch_index] = switch_item_data[data.switch_type][data.kong]
    return base_list


def compileMicrohints(spoiler: Spoiler) -> None:
    """Create guaranteed level + kong hints for various items."""
    spoiler.microhints = {}
    if spoiler.settings.microhints_enabled != MicrohintsEnabled.off:
        slam_levels = []
        helm_prog_items = getHelmProgItems(spoiler)
        microhint_categories = {
            MicrohintsEnabled.base: helm_prog_items.copy() + [Items.ProgressiveSlam],
            MicrohintsEnabled.all: helm_prog_items.copy() + [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle, Items.ProgressiveSlam],
        }
        items_needing_microhints = microhint_categories[spoiler.settings.microhints_enabled].copy()
        # Loop through locations looking for the items that need a microhint
        for id, location in spoiler.LocationList.items():
            if location.item in items_needing_microhints:
                item = ItemList[location.item]
                level_color = level_colors[location.level]
                if location.item == Items.ProgressiveSlam:
                    # Chunky Phase slam hint
                    if id not in PreGivenLocations and id not in TrainingBarrelLocations:  # Ignore anything pre-given
                        if location.level not in slam_levels:
                            slam_levels.append(location.level)
                else:
                    if location.type in item_type_names.keys():
                        hint_text = f"You would be better off looking for {item_type_names[location.type]} in {level_color}{level_list[location.level]}{level_color} for this.".upper()
                    elif location.type == Types.Shop:
                        hint_text = f"You would be better off looking for shops in {level_color}{level_list[location.level]}{level_color} for this.".upper()
                    else:
                        hint_text = f"You would be better off looking in {level_color}{level_list[location.level]}{level_color} with {kong_list[location.kong]} for this.".upper()
                    if spoiler.settings.krusha_kong == location.kong:
                        hint_text = hint_text.replace(colorless_kong_list[location.kong].upper(), "KRUSHA")
                    spoiler.microhints[item.name] = hint_text
        if len(slam_levels) > 0:
            slam_text_entries = [f"{level_colors[x]}{level_list[x]}{level_colors[x]}" for x in slam_levels]
            slam_text = " or ".join(slam_text_entries)
            spoiler.microhints[ItemList[Items.ProgressiveSlam].name] = (
                f"Ladies and Gentlemen! It appears that one fighter has come unequipped to properly handle this reptilian beast. Perhaps they should have looked in {slam_text} for the elusive slam.".upper()
            )


def compileSpoilerHints(spoiler):
    """Assemble the specified spoiler-style hints. See SpoilerHints enum for a list of all options."""
    spoiler.level_spoiler = {
        Levels.JungleJapes: LevelSpoiler(level_list[Levels.JungleJapes]),
        Levels.AngryAztec: LevelSpoiler(level_list[Levels.AngryAztec]),
        Levels.FranticFactory: LevelSpoiler(level_list[Levels.FranticFactory]),
        Levels.GloomyGalleon: LevelSpoiler(level_list[Levels.GloomyGalleon]),
        Levels.FungiForest: LevelSpoiler(level_list[Levels.FungiForest]),
        Levels.CrystalCaves: LevelSpoiler(level_list[Levels.CrystalCaves]),
        Levels.CreepyCastle: LevelSpoiler(level_list[Levels.CreepyCastle]),
        Levels.HideoutHelm: LevelSpoiler(level_list[Levels.HideoutHelm]),
        Levels.DKIsles: LevelSpoiler(level_list[Levels.DKIsles]),
        Levels.Shops: LevelSpoiler(level_list[Levels.Shops]),
    }
    # Sort the items by level they're found in
    important_items = ItemPool.Keys() + ItemPool.Kongs(spoiler.settings) + ItemPool.AllKongMoves() + ItemPool.ShockwaveTypeItems(spoiler.settings) + ItemPool.TrainingBarrelAbilities() + [Items.Bean]
    for location_id in spoiler.LocationList.keys():
        location = spoiler.LocationList[location_id]
        if location.item in important_items:
            spoiler.level_spoiler[location.level].vial_colors.append(CategorizeItem(ItemList[location.item]))
            spoiler.level_spoiler[location.level].points += PointValueOfItem(spoiler.settings, location.item)
            if location_id in spoiler.woth_locations:
                spoiler.level_spoiler[location.level].woth_count += 1
    # Convert those spoiler hints to readable text
    spoiler.level_spoiler_human_readable = {
        level_list[Levels.DKIsles]: "",
        level_list[Levels.JungleJapes]: "",
        level_list[Levels.AngryAztec]: "",
        level_list[Levels.FranticFactory]: "",
        level_list[Levels.GloomyGalleon]: "",
        level_list[Levels.FungiForest]: "",
        level_list[Levels.CrystalCaves]: "",
        level_list[Levels.CreepyCastle]: "",
        level_list[Levels.HideoutHelm]: "",
        level_list[Levels.Shops]: "",
    }
    for level in spoiler.level_spoiler.keys():
        # Clear out variables if they're unused or undesired
        if not spoiler.settings.spoiler_include_woth_count:
            spoiler.level_spoiler[level].woth_count = -1
        if spoiler.settings.spoiler_hints != SpoilerHints.vial_colors:
            spoiler.level_spoiler[level].vial_colors = []
        if spoiler.settings.spoiler_hints != SpoilerHints.points:
            spoiler.level_spoiler[level].points = -1
        # Create the text that will be human-readable on the site
        if spoiler.settings.spoiler_hints == SpoilerHints.vial_colors:
            # Sort the kongs/keys/vials in each level for readability
            spoiler.level_spoiler[level].vial_colors.sort()
            spoiler.level_spoiler_human_readable[level_list[level]] = "Items: " + ", ".join(spoiler.level_spoiler[level].vial_colors)
        if spoiler.settings.spoiler_hints == SpoilerHints.points:
            spoiler.level_spoiler_human_readable[level_list[level]] = "Points: " + str(spoiler.level_spoiler[level].points)
        if spoiler.settings.spoiler_include_woth_count:
            spoiler.level_spoiler_human_readable[level_list[level]] += " | WotH Items: " + str(spoiler.level_spoiler[level].woth_count)
    starting_info = StartingSpoiler(spoiler.settings)
    spoiler.level_spoiler["starting_info"] = starting_info
    spoiler.level_spoiler_human_readable["Starting Info"] = "Starting Kongs: " + ", ".join([colorless_kong_list[kong] for kong in starting_info.starting_kongs])
    spoiler.level_spoiler_human_readable["Starting Info"] += " | Starting Keys: " + ", ".join(starting_info.starting_keys)
    spoiler.level_spoiler_human_readable["Starting Info"] += " | Helm Order: " + ", ".join([colorless_kong_list[kong] for kong in starting_info.helm_order])
    spoiler.level_spoiler_human_readable["Starting Info"] += " | K. Rool Order: " + ", ".join([colorless_kong_list[kong] for kong in starting_info.krool_order])
    if spoiler.settings.spoiler_include_level_order:
        spoiler.level_spoiler_human_readable["Starting Info"] += " | Level Order: " + ", ".join([level_list[level] for level in starting_info.level_order])
    if spoiler.settings.spoiler_hints == SpoilerHints.points:
        spoiler.level_spoiler["point_spread"] = {
            "kongs": spoiler.settings.points_list_kongs,
            "keys": spoiler.settings.points_list_keys,
            "guns": spoiler.settings.points_list_guns,
            "instruments": spoiler.settings.points_list_instruments,
            "active_moves": spoiler.settings.points_list_active_moves,
            "pad_moves": spoiler.settings.points_list_pad_moves,
            "barrel_moves": spoiler.settings.points_list_barrel_moves,
            "training_moves": spoiler.settings.points_list_training_moves,
            "important_shared_moves": spoiler.settings.points_list_important_shared,
            "bean": spoiler.settings.points_list_bean,
        }
        spoiler.level_spoiler_human_readable["Point Spread"] = (
            "Kongs: "
            + str(spoiler.settings.points_list_kongs)
            + " | Keys: "
            + str(spoiler.settings.points_list_keys)
            + " | Guns: "
            + str(spoiler.settings.points_list_guns)
            + " | Instruments: "
            + str(spoiler.settings.points_list_instruments)
            + " | Active Moves: "
            + str(spoiler.settings.points_list_active_moves)
            + " | Pad Moves: "
            + str(spoiler.settings.points_list_pad_moves)
            + " | Barrel Moves: "
            + str(spoiler.settings.points_list_barrel_moves)
            + " | Training Moves: "
            + str(spoiler.settings.points_list_training_moves)
            + " | Shared Moves: "
            + str(spoiler.settings.points_list_important_shared)
            + " | Bean: "
            + str(spoiler.settings.points_list_bean)
        )


def CategorizeItem(item):
    """Identify the hint string for the given item."""
    if item.type == Types.Kong:
        return "Kong"
    elif item.type == Types.Key:
        return "Key"
    elif item.type == Types.Bean:
        return "Bean"
    elif item.kong == Kongs.donkey:
        return "Yellow Vial"
    elif item.kong == Kongs.diddy:
        return "Red Vial"
    elif item.kong == Kongs.lanky:
        return "Blue Vial"
    elif item.kong == Kongs.tiny:
        return "Purple Vial"
    elif item.kong == Kongs.chunky:
        return "Green Vial"
    elif item.kong == Kongs.any:
        return "Clear Vial"


def PointValueOfItem(settings, item_id):
    """Determine the point value of this item."""
    if item_id in [Items.Donkey, Items.Diddy, Items.Lanky, Items.Tiny, Items.Chunky]:
        return settings.points_list_kongs
    elif item_id in ItemPool.Keys():
        return settings.points_list_keys
    elif item_id in [Items.Coconut, Items.Peanut, Items.Grape, Items.Feather, Items.Pineapple]:
        return settings.points_list_guns
    elif item_id in [Items.Bongos, Items.Guitar, Items.Trombone, Items.Saxophone, Items.Triangle]:
        return settings.points_list_instruments
    elif item_id in [Items.GorillaGrab, Items.ChimpyCharge, Items.Orangstand, Items.PonyTailTwirl, Items.PrimatePunch]:
        return settings.points_list_active_moves
    elif item_id in [Items.BaboonBlast, Items.SimianSpring, Items.BaboonBalloon, Items.Monkeyport, Items.GorillaGone]:
        return settings.points_list_pad_moves
    elif item_id in [Items.StrongKong, Items.RocketbarrelBoost, Items.OrangstandSprint, Items.MiniMonkey, Items.HunkyChunky]:
        return settings.points_list_barrel_moves
    elif item_id in ItemPool.TrainingBarrelAbilities():
        return settings.points_list_training_moves
    elif item_id in ItemPool.ImportantSharedMoves:
        return settings.points_list_important_shared
    elif item_id == Items.Bean:
        return settings.points_list_bean
    return 0


def TryCreatingLoadingZoneHint(spoiler: Spoiler, transition: Transitions, disallowedRegions: Optional[List[Regions]] = None) -> str:
    """Try to create a hint message for the given transition. If this hint is determined to be bad, it will return false and not place the hint."""
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
        return ""
    # Validate the region of the hinted entrance is not in disallowedRegions
    if ShufflableExits[pathToHint].region in disallowedRegions:
        return ""
    # Validate the hinted destination is not the same as the hinted origin
    entranceMap = GetMapId(ShufflableExits[pathToHint].region)
    destinationMap = GetMapId(spoiler.shuffled_exit_data[transition].regionId)
    if entranceMap == destinationMap:
        return ""
    entranceName = ShufflableExits[pathToHint].name
    destinationName: str = spoiler.shuffled_exit_data[transition].spoilerName
    fromExitName = destinationName.find(" from ")
    if fromExitName != -1:
        # Remove exit name from destination
        destinationName = destinationName[:fromExitName]
    return f"If you're looking for \x04{destinationName}\x04, follow the path \x08from {entranceName}\x08."


def UpdateSpoilerHintList(spoiler: Spoiler) -> None:
    """Write hints to spoiler object."""
    for hint in hints:
        spoiler.hint_list[hint.name] = hint.hint
        spoiler.short_hint_list[hint.name] = hint.short_hint if hint.short_hint is not None else hint.hint


def GetRegionOfLocation(spoiler: Spoiler, location_id: Locations) -> Region:
    """Given the id of a Location, return the Region it belongs to."""
    location = spoiler.LocationList[location_id]
    # Shop locations are tied to the level, not the shop regions
    if location.type == Types.Shop:
        for region in [reg for id, reg in spoiler.RegionList.items() if reg.level == Levels.Shops]:
            if location_id in [location_logic.id for location_logic in region.locations if not location_logic.isAuxiliaryLocation]:
                return region
    for region_id in Regions:
        region = spoiler.RegionList[region_id]
        if region.level == location.level:
            if location_id in [location_logic.id for location_logic in region.locations if not location_logic.isAuxiliaryLocation]:
                return region
    raise Exception("Unable to find Region for Location")  # This should never trigger!


def GenerateMultipathDict(
    spoiler: Spoiler, useless_locations: Dict[Union[Items, Kongs], List[Any]]
) -> Tuple[Dict[Union[Locations, int], str], Dict[Union[Locations, int], List[Union[Locations, int]]]]:
    """Create multipath hint text and identify relevant goal locations for each eligible woth location.

    Returns two dicts.
    The hints dict will contain the hint texted needed for a multipath hint of the key's location.
    The goals dict will contain relevant locations for the purposes of identifying valid hint doors when placing multipath hints.
    """
    multipath_dict_hints = {}
    multipath_dict_goals = {}
    for location in spoiler.woth_locations:
        path_to_keys = []
        path_to_krool_phases = []
        path_to_camera = []
        relevant_goal_locations = []
        # Determine which keys this location is on the path to
        for woth_loc in spoiler.woth_paths.keys():
            if location in spoiler.woth_paths[woth_loc]:
                endpoint_item = ItemList[spoiler.LocationList[woth_loc].item]
                if endpoint_item.type == Types.Key:
                    path_to_keys.append(str(endpoint_item.index))
                    relevant_goal_locations.append(woth_loc)
        # Determine which K. Rool phases this is on the path to (if relevant)
        if spoiler.settings.win_condition == WinCondition.beat_krool:
            for kong in spoiler.krool_paths.keys():
                if location in spoiler.krool_paths[kong]:
                    path_to_krool_phases.append(kong_list[kong])
        # Determine if this location is on the path to taking photos for certain win conditions
        if spoiler.settings.win_condition in (WinCondition.all_fairies, WinCondition.poke_snap) and spoiler.settings.shockwave_status != ShockwaveStatus.start_with:
            camera_location_id = None
            for id, loc in spoiler.LocationList.items():
                if loc.item in (Items.Camera, Items.CameraAndShockwave):
                    camera_location_id = id
                    break
            if camera_location_id in spoiler.woth_paths.keys() and location in spoiler.woth_paths[camera_location_id]:
                path_to_camera.append("taking photos")
                relevant_goal_locations.append(camera_location_id)
        # Some locations are useless to hint on the path to some goals - every hint we construct should be useful
        if location in TrainingBarrelLocations or location in PreGivenLocations or location == Locations.HelmKey:
            # This is the assumed number of useful paths there are to hint for this location
            useful_path_count = len(path_to_keys) + len(path_to_krool_phases)
            for goal in useless_locations.keys():
                # If a goal contains this location as a useless path, it no longer counts as a useful path to hint
                if location in useless_locations[goal]:
                    useful_path_count -= 1
            # If at the end this location is not useful to hint on any paths, then it is not eligible for a multipath hint
            if useful_path_count <= 0:
                continue
        # Join the Key and K. Rool text together into what will be the core of the hint text
        hint_text_components = []
        if len(path_to_keys) > 0:
            path_to_keys.sort()
            key_text = "\x04Keys "
            if len(path_to_keys) == 1:
                key_text = "\x04Key "
            hint_text_components.append(key_text + join_words(path_to_keys) + "\x04")
        if len(path_to_krool_phases) > 0:
            hint_text_components.append("\x0dK. Rool vs.\x0d " + join_words(path_to_krool_phases))
        if len(path_to_camera) > 0:
            hint_text_components.append(path_to_camera[0])
        if len(path_to_keys) + len(path_to_krool_phases) + len(path_to_camera) > 0:
            multipath_dict_hints[location] = join_words(hint_text_components)
            multipath_dict_goals[location] = relevant_goal_locations
    return multipath_dict_hints, multipath_dict_goals


def join_words(words: List[str]) -> str:
    """Join a list of words with an 'and' for grammatical perfection."""
    if len(words) > 2:
        return "%s, and %s" % (", ".join(words[:-1]), words[-1])
    else:
        return " and ".join(words)


def AssociateHintsWithFlags(spoiler):
    """Associate hints with the related flag at their related location as applicable."""
    for hint in hints:
        if hint.related_location is not None:
            for location_selection in spoiler.item_assignment:
                if location_selection.location == hint.related_location:
                    hint.related_flag = location_selection.new_flag
                    break
        if hint.name != "First Time Talk":
            spoiler.tied_hint_flags[hint.name] = hint.related_flag if hint.related_flag is not None else 0xFFFF


def ApplyColorToPlandoHint(hint):
    """Replace plandomizer color tags with the appropriate characters."""
    new_hint = hint
    color_replace_dict = {
        "[orange]": "\x04",
        "[/orange]": "\x04",
        "[red]": "\x05",
        "[/red]": "\x05",
        "[blue]": "\x06",
        "[/blue]": "\x06",
        "[purple]": "\x07",
        "[/purple]": "\x07",
        "[lightgreen]": "\x08",
        "[/lightgreen]": "\x08",
        "[magenta]": "\x09",
        "[/magenta]": "\x09",
        "[cyan]": "\x0a",
        "[/cyan]": "\x0a",
        "[rust]": "\x0b",
        "[/rust]": "\x0b",
        "[paleblue]": "\x0c",
        "[/paleblue]": "\x0c",
        "[green]": "\x0d",
        "[/green]": "\x0d",
    }
    for color_tag, color_character in color_replace_dict.items():
        new_hint = new_hint.replace(color_tag, color_character)
    return new_hint


def ApplyPlandoHints(spoiler):
    """Apply plandomizer hint messages, returning the number of hints placed."""
    plando_hints_placed = 0
    for loc_id, message in spoiler.settings.plandomizer_dict["hints"].items():
        if message != "":
            final_message = ApplyColorToPlandoHint(message)
            location = spoiler.LocationList[int(loc_id)]
            hint_location = [hint_loc for hint_loc in hints if hint_loc.level == location.level and hint_loc.kong == location.kong][0]  # Matches exactly one hint
            UpdateHint(hint_location, final_message)
            hint_location.hint_type = HintType.Plando
            plando_hints_placed += 1
    return plando_hints_placed


def replaceKongNameWithKrusha(spoiler):
    """Replace Krusha's kong name."""
    krusha = spoiler.settings.krusha_kong
    kong_list[krusha] = f"{kong_colors[krusha]}Krusha{kong_colors[krusha]}"
    colorless_kong_list[krusha] = "Krusha"
    kong_cryptic[krusha] = [
        "The kong that has... scales ?",
        "The kong that is normally only available in multiplayer",
        "The kong that is not a monkey",
        "The Kong that is not in the DK Rap",
        "The Kong that Rivals Chunky in Strength",
        "The Kong that replaces another Kong",
        "The Kong that wears Camo",
        "The Kong that was K. Rool's Bodyguard",
    ]
