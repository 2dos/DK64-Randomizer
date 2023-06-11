"""Randomize Move Locations."""
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Settings import MicrohintsEnabled, MoveRando
from randomizer.Enums.Types import Types
from randomizer.Lists.Item import ItemList
from randomizer.Lists.Location import LocationList
from randomizer.Patching.Patcher import ROM, LocalROM

# /* 0x0A7 */ char move_rando_on; // O = No Move Randomization. 1 = On.
# /* 0x0A8 */ unsigned char dk_crankymoves[7]; // First 4 bits indicates the moves type, 0 = Moves, 1 = Slam, 2 = Guns, 3 = Ammo Belt, 4 = Instrument, 0xF = No Upgrade. Last 4 bits indicate move level (eg. 1 = Baboon Blast, 2 = Strong Kong, 3 = Gorilla Grab). Each item in the array indicates the level it is given (eg. 1st slot is purchased in Japes, 2nd for Aztec etc.)
# /* 0x0AF */ unsigned char diddy_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0B6 */ unsigned char lanky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0BD */ unsigned char tiny_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0C4 */ unsigned char chunky_crankymoves[7]; // See "dk_crankymoves"
# /* 0x0CB */ unsigned char dk_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D2 */ unsigned char diddy_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0D9 */ unsigned char lanky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E0 */ unsigned char tiny_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0E7 */ unsigned char chunky_funkymoves[7]; // See "dk_crankymoves"
# /* 0x0EE */ unsigned char dk_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0F5 */ unsigned char diddy_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x0FC */ unsigned char lanky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x103 */ unsigned char tiny_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi
# /* 0x10A */ unsigned char chunky_candymoves[7]; // See "dk_crankymoves". Note: Do not assign anything to item 0 or 4 as there's no Candy's in Japes or Fungi

moveRandoOffset = 0x0A7

dk_crankymoves = []
diddy_crankymoves = []
lanky_crankymoves = []
tiny_crankymoves = []
chunky_crankymoves = []
dk_funkymoves = []
diddy_funkymoves = []
lanky_funkymoves = []
tiny_funkymoves = []
chunky_funkymoves = []
dk_candymoves = []
diddy_candymoves = []
lanky_candymoves = []
tiny_candymoves = []
chunky_candymoves = []

level_names = [
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
    "DK Isles",
]

kong_names = {Kongs.donkey: "Donkey Kong", Kongs.diddy: "Diddy", Kongs.lanky: "Lanky", Kongs.tiny: "Tiny", Kongs.chunky: "Chunky", Kongs.any: "Any Kong"}


def pushItemMicrohints(spoiler, move_dict: dict, level: int, kong: int, slot: int):
    """Push hint for the micro-hints system."""
    if spoiler.settings.microhints_enabled != MicrohintsEnabled.off:
        if kong != Kongs.any or slot == 0:
            move = None  # Using no item for the purpose of a default
            hinted_items = {
                # Key = Item, Value = Textbox index in text file 19
                Items.Monkeyport: [("special", 2, Kongs.tiny), 26, [MicrohintsEnabled.base, MicrohintsEnabled.all]],
                Items.GorillaGone: [("special", 2, Kongs.chunky), 25, [MicrohintsEnabled.base, MicrohintsEnabled.all]],
                Items.Bongos: [("instrument", 0, Kongs.donkey), 27, [MicrohintsEnabled.all]],
                Items.Triangle: [("instrument", 0, Kongs.chunky), 28, [MicrohintsEnabled.all]],
                Items.Saxophone: [("instrument", 0, Kongs.tiny), 29, [MicrohintsEnabled.all]],
                Items.Trombone: [("instrument", 0, Kongs.lanky), 30, [MicrohintsEnabled.all]],
                Items.Guitar: [("instrument", 0, Kongs.diddy), 31, [MicrohintsEnabled.all]],
            }
            for item_hint in hinted_items:
                move_data = hinted_items[item_hint][0]
                if move_dict["move_type"] == move_data[0] and move_dict["move_lvl"] == move_data[1] and move_dict["move_kong"] == move_data[2]:
                    if spoiler.settings.microhints_enabled in list(hinted_items[item_hint][2]):
                        move = item_hint
            if move is not None:
                data = {"textbox_index": hinted_items[move][1], "mode": "replace_whole", "target": spoiler.microhints[ItemList[move].name]}
                if 19 in spoiler.text_changes:
                    spoiler.text_changes[19].append(data)
                else:
                    spoiler.text_changes[19] = [data]


def writeMoveDataToROM(arr: list, enable_hints: bool, spoiler, kong_slot: int, kongs: list, level_override=None):
    """Write move data to ROM."""
    for xi, x in enumerate(arr):
        if x["move_type"] == "flag":
            flag_dict = {"dive": 0x182, "orange": 0x184, "barrel": 0x185, "vine": 0x183, "camera": 0x2FD, "shockwave": 0x179, "camera_shockwave": 0xFFFE}
            flag_index = 0xFFFF
            if x["flag"] in flag_dict:
                flag_index = flag_dict[x["flag"]]
            LocalROM().writeMultipleBytes(5 << 5, 1)
            LocalROM().writeMultipleBytes(x["price"], 1)
            LocalROM().writeMultipleBytes(flag_index, 2)
        elif x["move_type"] is None:
            LocalROM().writeMultipleBytes(7 << 5, 1)
            LocalROM().writeMultipleBytes(0, 1)
            LocalROM().writeMultipleBytes(0xFFFF, 2)
        else:
            move_types = ["special", "slam", "gun", "ammo_belt", "instrument"]
            data = move_types.index(x["move_type"]) << 5 | (x["move_lvl"] << 3) | x["move_kong"]
            LocalROM().writeMultipleBytes(data, 1)
            LocalROM().writeMultipleBytes(x["price"], 1)
            LocalROM().writeMultipleBytes(0xFFFF, 2)
        if enable_hints:
            if level_override is not None:
                pushItemMicrohints(spoiler, x, level_override, kongs[xi], kong_slot)
            else:
                pushItemMicrohints(spoiler, x, xi, kongs[xi], kong_slot)


def dictEqual(dict1: dict, dict2: dict) -> bool:
    """Determine if two dictionaries are equal."""
    if len(dict1) != len(dict2):
        return False
    else:
        for i in dict1:
            if dict1.get(i) != dict2.get(i):
                return False
    return True


def randomize_moves(spoiler):
    """Randomize Move locations based on move_data from spoiler."""
    varspaceOffset = spoiler.settings.rom_data
    movespaceOffset = spoiler.settings.move_location_data
    hint_enabled = True
    if spoiler.settings.shuffle_items and Types.Shop in spoiler.settings.valid_locations:
        hint_enabled = False
    if spoiler.settings.move_rando != MoveRando.off and spoiler.move_data is not None:
        # Take a copy of move_data before modifying
        move_arrays = spoiler.move_data.copy()

        dk_crankymoves = move_arrays[0][0][0]
        diddy_crankymoves = move_arrays[0][0][1]
        lanky_crankymoves = move_arrays[0][0][2]
        tiny_crankymoves = move_arrays[0][0][3]
        chunky_crankymoves = move_arrays[0][0][4]
        dk_funkymoves = move_arrays[0][1][0]
        diddy_funkymoves = move_arrays[0][1][1]
        lanky_funkymoves = move_arrays[0][1][2]
        tiny_funkymoves = move_arrays[0][1][3]
        chunky_funkymoves = move_arrays[0][1][4]
        dk_candymoves = move_arrays[0][2][0]
        diddy_candymoves = move_arrays[0][2][1]
        lanky_candymoves = move_arrays[0][2][2]
        tiny_candymoves = move_arrays[0][2][3]
        chunky_candymoves = move_arrays[0][2][4]

        training_moves = move_arrays[1]
        bfi_move = move_arrays[2]

        kong_lists = []
        for shop in range(3):
            shop_lst = []
            for kong in range(5):
                kong_lst = []
                for level in range(8):
                    kong_lst.append([])
                shop_lst.append(kong_lst)
            kong_lists.append(shop_lst)
        for shop in range(3):
            for level in range(8):
                is_shared = True
                default = 0
                for kong in range(5):
                    if kong == 0:
                        default = move_arrays[0][shop][kong][level]
                    if not dictEqual(default, move_arrays[0][shop][kong][level]):
                        is_shared = False
                for kong in range(5):
                    applied_kong = kong
                    if is_shared:
                        applied_kong = Kongs.any
                    kong_lists[shop][kong][level] = applied_kong

        LocalROM().seek(varspaceOffset + moveRandoOffset)
        LocalROM().write(0x1)
        LocalROM().seek(movespaceOffset)
        writeMoveDataToROM(dk_crankymoves, hint_enabled, spoiler, 0, kong_lists[0][0])
        writeMoveDataToROM(diddy_crankymoves, hint_enabled, spoiler, 1, kong_lists[0][1])
        writeMoveDataToROM(lanky_crankymoves, hint_enabled, spoiler, 2, kong_lists[0][2])
        writeMoveDataToROM(tiny_crankymoves, hint_enabled, spoiler, 3, kong_lists[0][3])
        writeMoveDataToROM(chunky_crankymoves, hint_enabled, spoiler, 4, kong_lists[0][4])
        writeMoveDataToROM(dk_funkymoves, hint_enabled, spoiler, 0, kong_lists[1][0])
        writeMoveDataToROM(diddy_funkymoves, hint_enabled, spoiler, 1, kong_lists[1][1])
        writeMoveDataToROM(lanky_funkymoves, hint_enabled, spoiler, 2, kong_lists[1][2])
        writeMoveDataToROM(tiny_funkymoves, hint_enabled, spoiler, 3, kong_lists[1][3])
        writeMoveDataToROM(chunky_funkymoves, hint_enabled, spoiler, 4, kong_lists[1][4])
        writeMoveDataToROM(dk_candymoves, hint_enabled, spoiler, 0, kong_lists[2][0])
        writeMoveDataToROM(diddy_candymoves, hint_enabled, spoiler, 1, kong_lists[2][1])
        writeMoveDataToROM(lanky_candymoves, hint_enabled, spoiler, 2, kong_lists[2][2])
        writeMoveDataToROM(tiny_candymoves, hint_enabled, spoiler, 3, kong_lists[2][3])
        writeMoveDataToROM(chunky_candymoves, hint_enabled, spoiler, 4, kong_lists[2][4])
        writeMoveDataToROM(training_moves, hint_enabled, spoiler, 0, [Kongs.any, Kongs.any, Kongs.any, Kongs.any], 7)
        writeMoveDataToROM(bfi_move, hint_enabled, spoiler, 0, [Kongs.tiny], 7)


def getNextSlot(spoiler, item: Items) -> int:
    """Get slot for progressive item with pre-given moves."""
    slots = []
    if item == Items.ProgressiveAmmoBelt:
        slots = [0x1C, 0x1D]
    elif item == Items.ProgressiveInstrumentUpgrade:
        slots = [0x20, 0x21, 0x22]
    elif item == Items.ProgressiveSlam:
        slots = [0x10, 0x11]  # 0xF excluded as slam 1 is pre-given
    if len(slots) == 0:
        return None
    for slot in slots:
        offset = int(slot >> 3)
        check = int(slot % 8)
        LocalROM().seek(spoiler.settings.rom_data + 0xD5 + offset)
        val = int.from_bytes(LocalROM().readBytes(1), "big")
        if (val & (0x80 >> check)) == 0:
            return slot
    return None


def place_pregiven_moves(spoiler):
    """Place pre-given moves."""
    item_order = [
        Items.BaboonBlast,
        Items.StrongKong,
        Items.GorillaGrab,
        Items.ChimpyCharge,
        Items.RocketbarrelBoost,
        Items.SimianSpring,
        Items.Orangstand,
        Items.BaboonBalloon,
        Items.OrangstandSprint,
        Items.MiniMonkey,
        Items.PonyTailTwirl,
        Items.Monkeyport,
        Items.HunkyChunky,
        Items.PrimatePunch,
        Items.GorillaGone,
        Items.ProgressiveSlam,
        Items.ProgressiveSlam,
        Items.ProgressiveSlam,
        Items.Coconut,
        Items.Peanut,
        Items.Grape,
        Items.Feather,
        Items.Pineapple,
        Items.Bongos,
        Items.Guitar,
        Items.Trombone,
        Items.Saxophone,
        Items.Triangle,
        Items.ProgressiveAmmoBelt,
        Items.ProgressiveAmmoBelt,
        Items.HomingAmmo,
        Items.SniperSight,
        Items.ProgressiveInstrumentUpgrade,
        Items.ProgressiveInstrumentUpgrade,
        Items.ProgressiveInstrumentUpgrade,
        Items.Swim,
        Items.Oranges,
        Items.Barrels,
        Items.Vines,
        Items.Camera,
        Items.Shockwave,
    ]
    for item in spoiler.pregiven_items:
        # print(item)
        if item is not None and item != Items.NoItem:
            new_slot = None
            if item in (Items.ProgressiveAmmoBelt, Items.ProgressiveInstrumentUpgrade, Items.ProgressiveSlam):
                new_slot = getNextSlot(spoiler, item)
            elif item in item_order:
                new_slot = item_order.index(item)
            elif item == Items.CameraAndShockwave:
                new_slot = None  # Setting is handled by the code below
                for index in [item_order.index(Items.Camera), item_order.index(Items.Shockwave)]:
                    offset = int(index >> 3)
                    check = int(index % 8)
                    LocalROM().seek(spoiler.settings.rom_data + 0xD5 + offset)
                    val = int.from_bytes(LocalROM().readBytes(1), "big")
                    val |= 0x80 >> check
                    LocalROM().seek(spoiler.settings.rom_data + 0xD5 + offset)
                    LocalROM().writeMultipleBytes(val, 1)
            if new_slot is not None:
                offset = int(new_slot >> 3)
                check = int(new_slot % 8)
                LocalROM().seek(spoiler.settings.rom_data + 0xD5 + offset)
                val = int.from_bytes(LocalROM().readBytes(1), "big")
                val |= 0x80 >> check
                LocalROM().seek(spoiler.settings.rom_data + 0xD5 + offset)
                LocalROM().writeMultipleBytes(val, 1)
