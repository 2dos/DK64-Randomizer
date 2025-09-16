"""Hint location data for Wrinkly hints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Union, Set

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import Types

from randomizer.Enums.WrinklyKong import WrinklyLocation
from randomizer.Lists.Item import ItemList


class HintLocation:
    """Hint object for Wrinkly hint data locations."""

    def __init__(
        self,
        name: str,
        kong: Kongs,
        location: WrinklyLocation,
        hint: str,
        level: Levels,
        banned_keywords: List[Union[Any, str]] = [],
    ) -> None:
        """Create wrinkly hint object.

        Args:
            name (str): Location/String name of wrinkly.
            kong (Kongs): What kong the hint is for.
            location (WrinklyLocation): What lobby the hint is in.
            hint (str): Hint to be written to ROM
        """
        self.name = name
        self.kong = kong
        self.location = location
        self.hint = hint
        self.short_hint = None
        self.hint_type = -1
        self.banned_keywords = banned_keywords.copy()
        self.level = level
        self.related_location = None
        self.related_location_name = None
        self.related_location_item_name = None
        self.related_flag = None


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


def getDefaultHintList() -> List[HintLocation]:
    """Return the default set of hints."""
    return [
        HintLocation(
            "First Time Talk",
            Kongs.any,
            WrinklyLocation.ftt,
            "WELCOME TO THE DONKEY KONG 64 RANDOMIZER. MADE BY 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, CFOX, BISMUTH & ZNERNICUS",
            Levels.DKIsles,
        ),
        HintLocation("Japes DK", Kongs.donkey, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Diddy", Kongs.diddy, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Lanky", Kongs.lanky, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Tiny", Kongs.tiny, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Japes Chunky", Kongs.chunky, WrinklyLocation.japes, "", Levels.JungleJapes),
        HintLocation("Aztec DK", Kongs.donkey, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Diddy", Kongs.diddy, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Lanky", Kongs.lanky, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation("Aztec Tiny", Kongs.tiny, WrinklyLocation.aztec, "", Levels.AngryAztec),
        HintLocation(
            "Aztec Chunky",
            Kongs.chunky,
            WrinklyLocation.aztec,
            "",
            Levels.AngryAztec,
            banned_keywords=["Hunky Chunky", "Feather Bow"],
        ),
        HintLocation("Factory DK", Kongs.donkey, WrinklyLocation.factory, "", Levels.FranticFactory),
        HintLocation(
            "Factory Diddy",
            Kongs.diddy,
            WrinklyLocation.factory,
            "",
            Levels.FranticFactory,
            banned_keywords=["Gorilla Grab"],
        ),
        HintLocation(
            "Factory Lanky",
            Kongs.lanky,
            WrinklyLocation.factory,
            "",
            Levels.FranticFactory,
            banned_keywords=["Gorilla Grab"],
        ),
        HintLocation("Factory Tiny", Kongs.tiny, WrinklyLocation.factory, "", Levels.FranticFactory, banned_keywords=["Gorilla Grab"]),
        HintLocation("Factory Chunky", Kongs.chunky, WrinklyLocation.factory, "", Levels.FranticFactory),
        HintLocation("Galleon DK", Kongs.donkey, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Diddy", Kongs.diddy, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Lanky", Kongs.lanky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Tiny", Kongs.tiny, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Galleon Chunky", Kongs.chunky, WrinklyLocation.galleon, "", Levels.GloomyGalleon),
        HintLocation("Fungi DK", Kongs.donkey, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Diddy", Kongs.diddy, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Lanky", Kongs.lanky, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Tiny", Kongs.tiny, WrinklyLocation.fungi, "", Levels.FungiForest, banned_keywords=["Gorilla Grab"]),
        HintLocation("Fungi Chunky", Kongs.chunky, WrinklyLocation.fungi, "", Levels.FungiForest),
        HintLocation("Caves DK", Kongs.donkey, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation(
            "Caves Diddy",
            Kongs.diddy,
            WrinklyLocation.caves,
            "",
            Levels.CrystalCaves,
            banned_keywords=["Primate Punch", "Rocketbarrel Boost"],
        ),
        HintLocation("Caves Lanky", Kongs.lanky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Caves Tiny", Kongs.tiny, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Caves Chunky", Kongs.chunky, WrinklyLocation.caves, "", Levels.CrystalCaves, banned_keywords=["Primate Punch"]),
        HintLocation("Castle DK", Kongs.donkey, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Diddy", Kongs.diddy, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Lanky", Kongs.lanky, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Tiny", Kongs.tiny, WrinklyLocation.castle, "", Levels.CreepyCastle),
        HintLocation("Castle Chunky", Kongs.chunky, WrinklyLocation.castle, "", Levels.CreepyCastle),
    ]


class HintSet:
    """A set of hints and all pertinent information about them."""

    def __init__(self, hint_cap=35):
        """Create a hint set object."""
        self.hints: List[HintLocation] = getDefaultHintList()
        self.hint_cap = hint_cap
        self.expectedDistribution = {}
        self.currentDistribution = {}

    def ClearHintMessages(self) -> None:
        """Reset the hint message for all hints."""
        self.hints = getDefaultHintList()

    def getRandomHintLocation(self, random, location_list=None, kongs=None, levels=None, move_name=None) -> HintLocation:
        """Return an unoccupied hint location. The parameters can be used to specify location requirements."""
        valid_unoccupied_hint_locations = [
            hint
            for hint in self.hints
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
        for hint in self.hints:
            if hint.name == hint_location.name:
                return hint
        return None

    def getHintLocationsForAccessibleHintItems(self, hint_item_ids: Union[Set[Items], List[Items]], include_occupied=False) -> List[Union[HintLocation, Any]]:
        """Given a list of hint item ids, return unoccupied HintLocation objects they correspond to, possibly returning an empty list."""
        accessible_hints = []
        for item_id in hint_item_ids:
            item = ItemList[item_id]
            matching_hint = [hint for hint in self.hints if hint.level == item.level and hint.kong == item.kong][0]  # Should only match one
            accessible_hints.append(matching_hint)
        if include_occupied:
            return accessible_hints
        return [hint for hint in accessible_hints if hint.hint == ""]  # Filter out the occupied ones

    def RemoveFTT(self) -> None:
        """Remove the FTT hint from the hintset."""
        self.hints = [hint for hint in self.hints if hint.name != "First Time Talk"]


def UpdateHint(WrinklyHint: HintLocation, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    if len(message) <= 914:
        # We're safely below the character limit
        WrinklyHint.hint = message
        return True
    else:
        raise Exception("Hint message is longer than allowed.")
    return False


joke_hint_list = [
    "Did you know - Donkey Kong officially features in Donkey Kong 64.",
    "Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie.",
    "Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick.",
    "Tiny Kong is the youngest sister of Dixie Kong.",
    "Mornin.",
    "Lanky Kong is the only kong with no canonical relation to the main Kong family tree.",
    "Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64.",
    "Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64.",
    "If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight.",
    "Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021.",
    "The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes.",
    "Chunky Kong is the brother of Kiddy Kong.",
    "Fungi Forest contains mushrooms.",
    "Igloos can be found in Crystal Caves.",
    "Frantic Factory has multiple floors where things can be found.",
    "Angry Aztec has so much sand, it's even in the wind.",
    "You can find a rabbit in Fungi Forest and in Crystal Caves.",
    "You can find a beetle in Angry Aztec and in Crystal Caves.",
    "You can find a vulture in Angry Aztec.",
    "You can find an owl in Fungi Forest.",
    "You can find two boulders in Jungle Japes",
    "To buy moves, you will need coins.",
    "You can change the music and sound effects volume in the sound settings on the main menu.",
    "Coin Hoard is a Monkey Smash game mode where players compete to collect the most coins.",
    "Capture Pad is a Monkey Smash game mode where players attempt to capture pads in different corners of the arena.",
    "I have nothing to say to you.",
    "I had something to tell you, but I forgot what it is.",
    "I don't know anything.",
    "I'm as lost as you are. Good luck!",
    "Wrinkly? Never heard of him.",
    "This is it. The peak of all randomizers. No other randomizer exists besides DK64 Randomizer where you can listen to the dk rap in its natural habitat while freeing Chunky Kong in Jungle Japes.",
    "Why do they call it oven when you of in the cold food of out hot eat the food?",
    "Wanna become famous? Buy followers, coconuts and donks at DK64Randomizer (DK64Randomizer . com)!",
    "What you gonna do, SpikeVegeta?",
    "You don't care? Just give it to me? Okay, here it is.",
    "Rumor has it this game was developed in a cave with only a box of scraps!",
    "BOINNG! BOINNG! The current time is: 8:01!",
    "If you backflip right before Chunky punches K. Rool, you must go into first person camera to face him before the punch.",
    "The barrier to \x08Hideout Helm\x08 can be cleared by obtaining \x04801 Golden Bananas\x04. It can also be cleared with fewer than that.",
    "It would be \x05foolish\x05 to \x04not save your spoiler logs\x04 from the dev site.",
    "\x04W\x04\x05O\x05\x06A\x06\x07H\x07\x08,\x08 \x04I\x04 \x05D\x05\x06R\x06\x07O\x07\x08P\x08\x04P\x04\x05E\x05\x06D\x06 \x07A\x07\x08L\x08\x04L\x04 \x05M\x05\x06Y\x06 \x07C\x07\x08R\x08\x04A\x04\x05Y\x05\x06O\x06\x07N\x07\x08S\x08\x04!\x04",
    "[[WOTB]]",
    "By using DK64Randomizer.com, users agree to release the developers from any claims, damages, bad seeds, or liabilities. Please exercise caution and randomizer responsibly.",
    "Bothered? I was bothered once. They put me in a barrel, a bonus barrel. A bonus barrel with beavers, and beavers make me bothered.",
    "Looking for useful information? Try looking at another hint.",
    "Can I interest you in some casino chips? They're tastefully decorated with Hunky Chunky.",
    "Have faith, beanlievers. Your time will come.",
    "I have horrible news. Your seed just got \x0510 percent worse.\x05",
    "Great news! Your seed just got \x0810 percent better!\x08",
    "This is not a joke hint.",
    "I'll get back to you after this colossal dump of blueprints.",
    "Something in the \x0dHalt! The remainder of this hint has been confiscated by the top Kop on the force.\x0d",
    "When I finish Pizza Tower, this hint will update.",
    "Will we see a sub hour seasonal seed? Not a chance. The movement is too optimized at this point. I expect at most 10-20 more seconds can be saved, maybe a minute with TAS.",
    "I could put something useful here, but the \x04dk64randomizer.com\x04 wiki has lots of helpful information about hints already.",
    "If you're watching on YouTube, be sure to like, comment, subscribe, and smash that bell.",
    "I could really go for a hot dog right now.",
    "You can find statues of dinosnakes in Angry Aztec.",
    "If this seed was a channel point redemption, you have my condolences. If it wasn't, you have many options for victims.",
    "You wouldn't steal a coin. You wouldn't steal a banana. You wouldn't fail to report a bug to the devs.",
    "It's time to get your counting practice in: 1, 2, 3, 4, 5, 6, 9...",
    "I asked AI to help you and it said: 'The best way to get better at this game is to play it.'",
    "The hint you're looking for is on the next page, keep scrolling.",
    "Banandium? Void Kong? Pauline? DK, what are you talking about? It's 1999! Go get Cranky to knock some sense into your head.",
]

kong_list = ["\x04Donkey\x04", "\x05Diddy\x05", "\x06Lanky\x06", "\x07Tiny\x07", "\x08Chunky\x08", "\x04Any kong\x04"]
colorless_kong_list = ["Donkey", "Diddy", "Lanky", "Tiny", "Chunky"]
kong_colors = ["\x04", "\x05", "\x06", "\x07", "\x08", "\x0c"]

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
    [
        "The kong who likes jazz",
        "The kong who shoots K. Rool's tiny toes",
        "The kong who has ammo that is light as a feather",
        "The kong who can shrink in size",
    ],
    [
        "The kong who is one hell of a guy",
        "The kong who can pick up boulders",
        "The kong who fights a blocky boss",
        "The kong who bows down to a dragonfly",
    ],
    ["Members of the DK Crew", "A specific set of relatives", "A number of playable characters"],
]

all_levels = [
    Levels.JungleJapes,
    Levels.AngryAztec,
    Levels.FranticFactory,
    Levels.GloomyGalleon,
    Levels.FungiForest,
    Levels.CrystalCaves,
    Levels.CreepyCastle,
]
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
short_level_list = [
    "Japes",
    "Aztec",
    "Factory",
    "Galleon",
    "Forest",
    "Caves",
    "Castle",
    "Helm",
    "Isles",
    "Cranky's Lab",
]
vacation_levels_properties = [
    "Glorious Hills",
    "Arid Sands",
    "OSHA Violation Hotspot",
    "Murky Depths",
    "Blissful Greens",
    "Miners Paradise",
    "Haunted Architecture",
    "Timeless Corridors",
    "Undeniable Serenity",
    "Arcade Dwellers Paradise",
]

level_cryptic = [
    [
        "The level with a localized storm",
        "The level with a dirt mountain",
        "The level which has two retailers and no race",
    ],
    ["The level with four vases", "The level with two kongs cages", "The level with a spinning totem"],
    [
        "The level with a toy production facility",
        "The level with a tower of blocks",
        "The level with a game from 1981",
        "The level where you need two quarters to play",
    ],
    ["The level with the most water", "The level where you free a water dweller", "The level with stacks of gold"],
    [
        "The level with only two retailers and two races",
        "The level where night can be acquired at will",
        "The level with a nocturnal tree dweller",
    ],
    ["The level with two inches of water", "The level with two ice shields", "The level with an Ice Tomato"],
    [
        "The level with battlements",
        "The level with a dungeon, ballroom and a library",
        "The level with drawbridge and a moat",
    ],
    ["The timed level", "The level with no boss", "The level with no small bananas"],
]
level_cryptic_isles = level_cryptic.copy()
level_cryptic_isles.remove(level_cryptic_isles[-1])
level_cryptic_isles.append(["The hub world", "The world with DK's ugly mug on it", "The world with only a Cranky's Lab and Snide's HQ in it"])

level_cryptic_helm_isles = level_cryptic.copy()
level_cryptic_helm_isles.append(level_cryptic_isles[-1])

shop_owners = ["\x04Cranky\x04", "\x04Funky\x04", "\x04Candy\x04"]
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
    [
        "The shop owner who is flirtatious",
        "The shop owner who is not present in Fungi Forest",
        "The shop owner who is not present in Jungle Japes",
        "The shop owner with blonde hair",
    ],
]

crankys_cryptic = ["a location out of this world", "a location 5000 points deep", "a mad scientist's laboratory"]

item_type_names = {
    Types.Blueprint: "\x06a kasplat\x06",
    Types.Fairy: "\x06a fairy\x06",
    Types.Crown: "\x06a battle arena\x06",
    Types.RainbowCoin: "\x06a dirt patch\x06",
    Types.CrateItem: "\x06a melon crate\x06",
    Types.Enemies: "\x06an enemy\x06",
    Types.Hint: "\x06a hint door\x06",
    Types.BoulderItem: "\x06a holdable object\x06",
}
item_type_names_cryptic = {
    Types.Blueprint: ["a minion of K. Rool", "a shockwaving foe", "a colorfully haired henchman"],
    Types.Fairy: ["an aerial ace", "a bit of flying magic", "a Queenly representative"],
    Types.Crown: ["a contest of endurance", "a crowning achievement", "the visage of K. Rool"],
    Types.RainbowCoin: ["the initials of DK", "a muddy mess", "buried treasure"],
    Types.CrateItem: ["a bouncing box", "a breakable cube", "a crate of goodies"],
    Types.Enemies: ["a minor discouragement", "an obstacle along the way", "something found in mad maze maul"],
    Types.Hint: ["a source of a riddle", "the old granny house", "a door to the granny"],
    Types.BoulderItem: ["an object of relative ease", "something as solid as a rock"],
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

kong_placement_levels = [
    {"name": "Jungle Japes", "level": 0},
    {"name": "Llama Temple", "level": 1},
    {"name": "Tiny Temple", "level": 1},
    {"name": "Frantic Factory", "level": 2},
]

boss_names = {
    Maps.JapesBoss: "Army Dillo 1",
    Maps.AztecBoss: "Dogadon 1",
    Maps.FactoryBoss: "Mad Jack",
    Maps.GalleonBoss: "Pufftoss",
    Maps.FungiBoss: "Dogadon 2",
    Maps.CavesBoss: "Army Dillo 2",
    Maps.CastleBoss: "King Kut Out",
    Maps.KroolDonkeyPhase: "DK Phase",
    Maps.KroolDiddyPhase: "Diddy Phase",
    Maps.KroolLankyPhase: "Lanky Phase",
    Maps.KroolTinyPhase: "Tiny Phase",
    Maps.KroolChunkyPhase: "Chunky Phase",
}
boss_colors = {
    Maps.JapesBoss: "\x08",
    Maps.AztecBoss: "\x04",
    Maps.FactoryBoss: "\x0c",
    Maps.GalleonBoss: "\x06",
    Maps.FungiBoss: "\x07",
    Maps.CavesBoss: "\x0a",
    Maps.CastleBoss: "\x09",
    Maps.KroolDonkeyPhase: "\x04",
    Maps.KroolDiddyPhase: "\x05",
    Maps.KroolLankyPhase: "\x06",
    Maps.KroolTinyPhase: "\x07",
    Maps.KroolChunkyPhase: "\x08",
}

PointSpreadSelector = []
PointSpreadBase = [
    ("Kongs", 11),
    ("Keys", 11),
    ("Guns", 9),
    ("Instruments", 9),
    ("Training Moves", 7),
    ("Fairy Moves", 7),
    ("Important Shared", 5),
    ("Pad Moves", 3),
    ("Barrel Moves", 7),
    ("Active Moves", 5),
    ("Bean", 3),
    ("Shopkeepers", 11),
]
for item in PointSpreadBase:
    PointSpreadSelector.append({"name": item[0], "value": item[0].lower().replace(" ", "_"), "tooltip": "", "default": item[1]})
