"""Compile a list of hints based on the settings."""
import random
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions

from randomizer.Lists.Item import NameFromKong
from randomizer.Lists.MapsAndExits import GetMapId
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Spoiler import Spoiler
from randomizer.Patching.UpdateHints import updateRandomHint


def compileHints(spoiler: Spoiler):
    """Push hints to hint list based on settings."""
    # K Rool Order
    if spoiler.settings.krool_phase_order_rando:
        associated_hint = f"K. Rool order is {NameFromKong(spoiler.settings.krool_order[0])}"
        for x in range(len(spoiler.settings.krool_order)):
            if x != 0:
                associated_hint += f" then {NameFromKong(spoiler.settings.krool_order[x])}"
        updateRandomHint(associated_hint)
    padded_hints = [
        "Did you know - Donkey Kong officially features in Donkey Kong 64.",
        "Fungi Forest was originally intended to be in the other N64 Rareware title, Banjo Kazooie.",
        "Holding up-left when trapped inside of a trap bubble will break you out of it without spinning your stick.",
        "Tiny Kong is the youngest sister of Dixie Kong.",
        "Mornin.",
        "Lanky Kong is the only kong with no canonical relation to the main Kong family tree.",
        "Despite the line in the DK Rap stating otherwise, Chunky is the kong who can jump highest in DK64.",
        "Despite the line in the DK Rap stating otherwise, Tiny is one of the two slowest kongs in DK64.",
        "Candy Kong does not appear in Jungle Japes or Fungi Forest.",
        "If you fail the twelfth round of K. Rool, the game will dictate that K. Rool is victorious and end the fight.",
        "Donkey Kong 64 Randomizer started as a LUA Script in early 2019, evolving into a ROM Hack in 2021.",
        "The maximum in-game time that the vanilla file screen time can display is 1165 hours and 5 minutes.",
        "Chunky Kong is the brother of Kiddy Kong.",
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
        "This is it. The peak of all randomizers. No other randomizer exists besides DK64 Randomizer where you can listen to the dk rap in its natural habitat while freeing Chunky Kong in Jungle Japes.",
        "Why do they call it oven when you of in the cold food of out hot eat the food?",
    ]
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
    level_cryptic = [
        [
            "The level with a localized storm",
            "The level with a dirt mountain",
            "The level which has two retailers and no race",
        ],
        ["The level with sporadic gusts of sand", "The level with two kongs to free", "The level with a spinning totem"],
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
            "The level with an Ice Tomato",
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
                "name": "Gorilla Grab",
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
                "name": "Saxophone Slam",
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
        for shop in range(3):
            for kong in range(5):
                for level in range(7):
                    for move in moves_of_importance:
                        if spoiler.move_data[shop][kong][level] == move["key"] and kong == move["kong"]:
                            move["level"] = level
                            move["shop"] = shop
        for move in moves_of_importance:
            if spoiler.settings.wrinkly_hints == "cryptic":
                kong_name = random.choice(kong_cryptic[move["kong"]])
                level_name = random.choice(level_cryptic[move["level"]])
            else:
                kong_name = kong_list[move["kong"]]
                level_name = level_list[move["level"]]
            move_name = move["name"]

            shop_name = shop_owners[move["shop"]]
            text = f"{move_name} can be purchased from {shop_name} in {level_name}."
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
            if spoiler.settings.wrinkly_hints == "cryptic":
                if not kong_index == Kongs.any:
                    kong_name = random.choice(kong_cryptic[kong_index])
                level_name = random.choice(level_cryptic[level_index])
            else:
                if not kong_index == Kongs.any:
                    kong_name = kong_list[kong_index]
                level_name = level_list[level_index]
            if kong_index == Kongs.any:
                kong_name = "An empty cage"
            updateRandomHint(f"{kong_name} can be found in {level_name}.")
    if spoiler.settings.shuffle_loading_zones == "all":
        AddLoadingZoneHints(spoiler)
    if spoiler.settings.BananaMedalsRequired:
        updateRandomHint(f"{spoiler.settings.BananaMedalsRequired} medals are required to access Jetpac.")
    if spoiler.settings.perma_death:
        updateRandomHint("The curse can only be removed upon disabling K. Rools machine.")
    updateRandomHint(f"{spoiler.settings.krool_key_count} Keys are required to turn in K. Rool.")
    if spoiler.settings.level_randomization != "level_order":
        for x in spoiler.settings.krool_keys_required:
            key_index = x - 4
            if spoiler.settings.wrinkly_hints == "cryptic":
                level_name = random.choice(level_cryptic[key_index])
            else:
                level_name = level_list[key_index]
            updateRandomHint(f"You will need to obtain the key from {level_name} to fight your greatest foe.")
    for x in range(7):
        boss_map = spoiler.settings.boss_maps[x]
        if spoiler.settings.wrinkly_hints == "cryptic":
            level_name = random.choice(level_cryptic[x])
        else:
            level_name = level_list[x]
        if boss_map == 0xC7:
            updateRandomHint(f"The cardboard boss can be found in {level_name}.")
    # Way of the Hoard hints
    shopNames = ["Candy", "Funky", "Cranky"]
    moveSpecificSuffixes = [" Donkey", " Diddy", " Lanky", " Tiny", " Chunky", " Shared"]
    wothLocations = [key for key in spoiler.woth.keys() if any(shopName in key for shopName in shopNames)]
    selectedWothLocations = random.sample(wothLocations, min(5, len(wothLocations)))
    for wothLocation in selectedWothLocations:
        suffix = [specificSuffix for specificSuffix in moveSpecificSuffixes if specificSuffix in wothLocation]
        if len(suffix) > 0:
            wothHint = str(wothLocation).removesuffix(suffix[0])
        updateRandomHint(f"{wothHint} is on the Way of the Hoard.")

    # PADDED HINTS
    cb_list = [
        {"kong": "Donkey", "color": "Yellow"},
        {"kong": "Diddy", "color": "Red"},
        {"kong": "Lanky", "color": "Blue"},
        {"kong": "Tiny", "color": "Purple"},
        {"kong": "Chunky", "color": "Green"},
    ]
    # padded_hints.append(f"Your seed is {spoiler.settings.seed}")
    padded_hints.append(f"You can find bananas in {level_list[random.randint(0,6)]}, but also in other levels.")
    cb_hint = random.choice(cb_list)
    padded_hints.append(f"{cb_hint['kong']} can find {cb_hint['color']} bananas in {random.choice(level_list)}.")
    for x in range(8):
        count = spoiler.settings.EntryGBs[x]
        gb_name = "Golden Bananas"
        if count == 1:
            gb_name = "Golden Banana"
        if spoiler.settings.wrinkly_hints == "cryptic":
            level_name = random.choice(level_cryptic[x])
        else:
            level_name = level_list[x]
        padded_hints.append(f"The barrier to {level_name} can be cleared by obtaining {count} {gb_name}.")
    for x in range(7):
        count = spoiler.settings.BossBananas[x]
        cb_name = "Small Bananas"
        if count == 1:
            cb_name = "Small Banana"
        if spoiler.settings.wrinkly_hints == "cryptic":
            level_name = random.choice(level_cryptic[x])
        else:
            level_name = level_list[x]
        padded_hints.append(f"The barrier to the boss in {level_name} can be cleared by obtaining {count} {cb_name}.")
    padded_count = 35
    if len(padded_hints) < 35:
        padded_count = len(padded_hints)
    random.shuffle(padded_hints)
    for x in range(padded_count):
        updateRandomHint(padded_hints[x])


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
        if TryAddingLoadingZoneHint(spoiler, japesHinted, criticalJapesRegions):
            japesHintPlaced = True
            break
    if not japesHintPlaced:
        print("Japes LZR hint unable to be placed!")

    aztecHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalAztecRegions]
    random.shuffle(aztecHintEntrances)
    aztecHintPlaced = False
    while len(aztecHintEntrances) > 0:
        aztecHinted = aztecHintEntrances.pop()
        if TryAddingLoadingZoneHint(spoiler, aztecHinted, criticalAztecRegions):
            aztecHintPlaced = True
            break
    if not aztecHintPlaced:
        print("Aztec LZR hint unable to be placed!")

    factoryHintEntrances = [entrance for entrance, back in spoiler.shuffled_exit_data.items() if back.regionId in criticalFactoryRegions]
    random.shuffle(factoryHintEntrances)
    factoryHintPlaced = False
    while len(factoryHintEntrances) > 0:
        factoryHinted = factoryHintEntrances.pop()
        if TryAddingLoadingZoneHint(spoiler, factoryHinted, criticalFactoryRegions):
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
            if TryAddingLoadingZoneHint(spoiler, usefulHinted, regions):
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
        elif TryAddingLoadingZoneHint(spoiler, transition):
            remainingHintCount -= 1
    if remainingHintCount > 0:
        print("Unable to place remaining LZR hints!")


def TryAddingLoadingZoneHint(spoiler: Spoiler, transition, disallowedRegions: list = None):
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
    updateRandomHint(f"If you're looking for {destinationName}, follow the path from {entranceName}.")
    return True
