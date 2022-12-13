"""Apply item rando changes."""
import js
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Enums.Types import Types
from randomizer.Enums.Locations import Locations
from randomizer.Patching.Lib import intf_to_float, float_to_hex

model_two_indexes = {
    Types.Banana: 0x74,
    Types.Blueprint: [0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
    Types.Coin: [0x48, 0x28F],  # Nintendo, Rareware
    Types.Key: 0x13C,
    Types.Crown: 0x18D,
    Types.Medal: 0x90,
    Types.Shop: [0x5B, 0x1F2, 0x59, 0x1F3, 0x1F5, 0x1F6],
    Types.TrainingBarrel: 0x1F6,
    Types.Shockwave: 0x1F6,
    Types.NoItem: 0,  # No Item
    Types.Kong: [0x257, 0x258, 0x259, 0x25A, 0x25B],
    Types.Bean: 0x198,
    Types.Pearl: 0x1B4,
}

model_two_scales = {
    Types.Banana: 0.25,
    Types.Blueprint: 2,
    Types.Coin: 0.4,
    Types.Key: 0.17,
    Types.Crown: 0.25,
    Types.Medal: 0.22,
    Types.Shop: 0.25,
    Types.TrainingBarrel: 0.25,
    Types.Shockwave: 0.25,
    Types.NoItem: 0.25,  # No Item
    Types.Kong: 0.25,
    Types.Bean: 0.25,
    Types.Pearl: 0.25,
}

actor_indexes = {
    Types.Banana: 45,
    Types.Blueprint: [78, 75, 77, 79, 76],
    Types.Key: 72,
    Types.Crown: 86,
    Types.Coin: [151, 152],
    Types.Shop: [157, 158, 159, 160, 161, 162],
    Types.TrainingBarrel: 162,
    Types.Shockwave: 162,
    Types.NoItem: 153,
    Types.Medal: 154,
    Types.Kong: [141, 142, 143, 144, 155],
    Types.Bean: 172,
    Types.Pearl: 174,
}
kong_flags = (385, 6, 70, 66, 117)


class TextboxChange:
    """Class to store information which pertains to a change of textbox information."""

    def __init__(self, file_index, textbox_index, text_replace, replacement_text="|", force_pipe=False):
        """Initialize with given paremeters."""
        self.file_index = file_index
        self.textbox_index = textbox_index
        self.text_replace = text_replace  # Text which is going to be replaced with replacement_text
        self.replacement_text = replacement_text
        self.force_pipe = force_pipe  # If True, don't replace with item name upon checking later. Instead, will be replaced in RDRAM dynamically


textboxes = {
    Locations.AztecTinyBeetleRace: TextboxChange(14, 0, "GOLDEN BANANA", "|", True),
    Locations.CavesLankyBeetleRace: TextboxChange(14, 0, "GOLDEN BANANA", "|", True),
    Locations.JapesDiddyMinecarts: TextboxChange(16, 2, "GOLDEN BANANA"),
    Locations.JapesDiddyMinecarts: TextboxChange(16, 3, "BANANA"),
    Locations.JapesDiddyMinecarts: TextboxChange(16, 4, "BANANA"),
    Locations.ForestChunkyMinecarts: TextboxChange(16, 5, "GOLDEN BANANA"),
    Locations.ForestChunkyMinecarts: TextboxChange(16, 7, "BANANA"),
    Locations.CastleDonkeyMinecarts: TextboxChange(16, 8, "BE A WINNER", "WIN A |"),
    Locations.CastleDonkeyMinecarts: TextboxChange(16, 9, "BANANA"),
    Locations.IslesDonkeyInstrumentPad: TextboxChange(16, 18, "ANOTHER BANANA", "SOMETHING"),
    Locations.IslesDiddyInstrumentPad: TextboxChange(16, 18, "ANOTHER BANANA", "SOMETHING"),
    Locations.IslesLankyInstrumentPad: TextboxChange(16, 18, "ANOTHER BANANA", "SOMETHING"),
    Locations.IslesTinyInstrumentPad: TextboxChange(16, 18, "ANOTHER BANANA", "SOMETHING"),
    Locations.IslesChunkyInstrumentPad: TextboxChange(16, 18, "ANOTHER BANANA", "SOMETHING"),
    Locations.FactoryTinyCarRace: TextboxChange(17, 4, "GOLDEN BANANA"),
    Locations.GalleonTinyPearls: TextboxChange(23, 0, "PLEASE TRY AND GET THEM BACK", "IF YOU HELP ME FIND THEM, I WILL REWARD YOU WITH A |"),
    Locations.GalleonTinyPearls: TextboxChange(23, 1, "GOLDEN BANANA"),
    Locations.AztecDiddyVultureRace: TextboxChange(15, 0, "TEST OF YOUR FLYING SKILL"),
    Locations.AztecDonkeyFreeLlama: TextboxChange(10, 1, "ALL THIS SAND", "THIS |"),
    Locations.AztecDonkeyFreeLlama: TextboxChange(10, 2, "BANANA"),
    Locations.RarewareCoin: TextboxChange(8, 2, "RAREWARE COIN"),
    Locations.RarewareCoin: TextboxChange(8, 34, "RAREWARE COIN"),
    Locations.ForestLankyRabbitRace: TextboxChange(20, 1, "TROPHY", "| TROPHY"),
    Locations.ForestLankyRabbitRace: TextboxChange(20, 2, "TROPHY", "| TROPHY"),
    Locations.ForestLankyRabbitRace: TextboxChange(20, 3, "TROPHY", "| TROPHY"),
    Locations.ForestChunkyApple: TextboxChange(22, 0, "BANANA"),
    Locations.ForestChunkyApple: TextboxChange(22, 1, "BANANA"),
    Locations.ForestChunkyApple: TextboxChange(22, 4, "BANANA"),
    Locations.GalleonDonkeySealRace: TextboxChange(28, 2, "CHEST O' GOLD"),
    Locations.RarewareBanana: TextboxChange(30, 0, "REWARD ANYONE", "REWARD ANYONE WITH A |"),
    Locations.CavesLankyCastle: TextboxChange(33, 0, "HOW ABOUT IT", "HOW ABOUT A |"),
    Locations.CastleTinyCarRace: TextboxChange(34, 4, "BANANA"),
}

rareware_coin_reward = ("RAREWARE COIN", "DOUBLOON OF THE RAREST KIND")
nintendo_coin_reward = ("NINTENDO COIN", "ANCIENT DOUBLOON")

text_rewards = {
    Types.Banana: ("GOLDEN BANANA", "BANANA OF PURE GOLD"),
    Types.Blueprint: ("BLUEPRINT", "MAP O' DEATH MACHINE"),
    Types.Key: ("BOSS KEY", "KEY TO DAVY JONES LOCKER"),
    Types.Crown: ("BATTLE CROWN", "CROWN TO PLACE ATOP YER HEAD"),
    Types.Fairy: ("BANANA FAIRY", "MAGICAL FLYING PIXIE"),
    Types.Medal: ("BANANA MEDAL", "MEDALLION"),
    Types.Shop: ("POTION", "BOTTLE OF GROG"),
    Types.Shockwave: ("POTION", "BOTTLE OF GROG"),
    Types.TrainingBarrel: ("POTION", "BOTTLE OF GROG"),
    Types.Kong: ("KONG", "WEIRD MONKEY"),
    Types.Bean: ("BEAN", "QUESTIONABLE VEGETABLE"),
    Types.Pearl: ("PEARL", "BLACK PEARL"),
    Types.RainbowCoin: ("RAINBOW COIN", "COLORFUL COIN HIDDEN FOR 17 YEARS"),
    Types.NoItem: ("NOTHING", "DIDDLY SQUAT"),
}


def getTextRewardIndex(item) -> int:
    """Get reward index for text item."""
    if item.new_item == Types.Coin:
        if item.new_flag == 379:
            return 5
        return 6
    elif item.new_item in (Types.Shop, Types.Shockwave, Types.TrainingBarrel):
        return 8
    elif item.new_item is None:
        return 13
    else:
        item_text_indexes = (
            Types.Banana,
            Types.Blueprint,
            Types.Key,
            Types.Crown,
            Types.Fairy,
            Types.Coin,
            Types.Coin,
            Types.Medal,
            Types.Shop,
            Types.Kong,
            Types.Bean,
            Types.Pearl,
            Types.RainbowCoin,
            Types.NoItem,
        )
        if item.new_item in item_text_indexes:
            return item_text_indexes.index(item.new_item)
        return 13


def place_randomized_items(spoiler: Spoiler):
    """Place randomized items into ROM."""
    if spoiler.settings.shuffle_items:
        sav = spoiler.settings.rom_data
        ROM().seek(sav + 0x034)
        ROM().write(1)  # Item Rando Enabled
        item_data = spoiler.item_assignment
        model_two_items = [
            0x74,  # GB
            0xDE,  # BP - DK
            0xE0,  # BP - Diddy
            0xE1,  # BP - Lanky
            0xDD,  # BP - Tiny
            0xDF,  # BP - Chunky
            0x48,  # Nintendo Coin
            0x28F,  # Rareware Coin
            0x13C,  # Key
            0x18D,  # Crown
            0x90,  # Medal
            0x288,  # Rareware GB
            0x198,  # Bean
            0x1B4,  # Pearls
        ]
        map_items = {}
        bonus_table_offset = 0
        flut_items = []
        for item in item_data:
            if item.can_have_item:
                if item.is_shop:
                    # Write in placement index
                    ROM().seek(sav + 0xA7)
                    ROM().write(1)
                    movespaceOffset = spoiler.settings.move_location_data
                    for placement in item.placement_index:
                        write_space = movespaceOffset + (4 * placement)
                        if item.new_item is None:
                            # Is Nothing
                            # First check if there is an item here
                            ROM().seek(write_space)
                            check = int.from_bytes(ROM().readBytes(4), "big")
                            if check == 0xE000FFFF or placement >= 120:  # No Item
                                ROM().seek(write_space)
                                ROM().writeMultipleBytes(7 << 5, 1)
                                ROM().writeMultipleBytes(0, 1)
                                ROM().writeMultipleBytes(0xFFFF, 2)
                        elif item.new_flag & 0x8000:
                            # Is Move
                            item_kong = (item.new_flag >> 12) & 7
                            item_subtype = (item.new_flag >> 8) & 0xF
                            if item_subtype == 7:
                                item_subindex = 0
                            else:
                                item_subindex = (item.new_flag & 0xFF) - 1
                            ROM().seek(write_space)
                            ROM().writeMultipleBytes(item_subtype << 5 | (item_subindex << 3) | item_kong, 1)
                            ROM().writeMultipleBytes(item.price, 1)
                            ROM().writeMultipleBytes(0xFFFF, 2)
                        else:
                            # Is Flagged Item
                            subtype = 5
                            if item.new_item == Types.Banana:
                                subtype = 6
                            ROM().seek(write_space)
                            ROM().writeMultipleBytes(subtype << 5, 1)
                            ROM().writeMultipleBytes(item.price, 1)
                            ROM().writeMultipleBytes(item.new_flag, 2)
                elif not item.reward_spot:
                    for map_id in item.placement_data:
                        if map_id not in map_items:
                            map_items[map_id] = []
                        if item.new_item is None:
                            map_items[map_id].append({"id": item.placement_data[map_id], "obj": Types.NoItem, "kong": 0, "flag": 0, "upscale": 1, "shared": False})
                        else:
                            numerator = model_two_scales[item.new_item]
                            denominator = model_two_scales[item.old_item]
                            upscale = numerator / denominator
                            map_items[map_id].append({"id": item.placement_data[map_id], "obj": item.new_item, "kong": item.new_kong, "flag": item.new_flag, "upscale": upscale, "shared": item.shared})
                    if item.location == Locations.NintendoCoin:
                        arcade_rewards = (
                            Types.NoItem,  # Or Nintendo Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Shop,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.Kong,  # Handled in special case
                            Types.RainbowCoin,
                            Types.Coin,  # Flag check handled separately
                        )
                        arcade_reward_index = 0
                        if item.new_item == Types.Coin:
                            if item.new_flag == 379:  # RW Coin
                                arcade_reward_index = 21
                        elif item.new_item == Types.Kong:
                            if item.new_flag in kong_flags:
                                arcade_reward_index = kong_flags.index(item.new_flag)
                        elif item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave):
                            if (item.new_flag & 0x8000) == 0:
                                slot = 5
                            else:
                                slot = (item.new_flag >> 12) & 7
                                if item.shared or slot > 5:
                                    slot = 5
                            arcade_reward_index = 9 + slot
                        elif item.new_item in arcade_rewards:
                            arcade_reward_index = arcade_rewards.index(item.new_item)
                        ROM().seek(sav + 0x110)
                        ROM().write(arcade_reward_index)
                    elif item.location == Locations.RarewareCoin:
                        jetpac_rewards = (
                            Types.NoItem,  # Or RW Coin
                            Types.Bean,
                            Types.Blueprint,
                            Types.Crown,
                            Types.Fairy,
                            Types.Banana,
                            Types.Key,
                            Types.Medal,
                            Types.Pearl,
                            Types.Shop,  # Shockwave/Training handled separately
                            Types.Kong,
                            Types.RainbowCoin,
                            Types.Coin,  # Flag check handled separately
                        )
                        jetpac_reward_index = 0
                        if item.new_item in (Types.Shop, Types.TrainingBarrel, Types.Shockwave):
                            jetpac_reward_index = 9
                        elif item.new_item == Types.Coin:
                            if item.new_flag == 132:  # Nintendo Coin
                                jetpac_reward_index = 12
                        elif item.new_item in jetpac_rewards:
                            jetpac_reward_index = jetpac_rewards.index(item.new_item)
                        ROM().seek(sav + 0x111)
                        ROM().write(jetpac_reward_index)
                    elif item.location in (Locations.ForestDonkeyBaboonBlast, Locations.CavesDonkeyBaboonBlast):
                        # Autocomplete bonus barrel fix
                        if item.new_item is None:
                            actor_index = 153
                        elif item.new_item == Types.Blueprint:
                            actor_index = actor_indexes[Types.Blueprint][item.new_kong]
                        elif item.new_item == Types.Coin:
                            actor_index = actor_indexes[Types.Coin][0]
                            if item.new_flag == 379:  # Is RW Coin
                                actor_index = actor_indexes[Types.Coin][1]
                        elif item.new_item in (Types.Shop, Types.Shockwave, Types.TrainingBarrel):
                            if (item.new_flag & 0x8000) == 0:
                                slot = 5
                            else:
                                slot = (item.new_flag >> 12) & 7
                                if item.shared or slot > 5:
                                    slot = 5
                            actor_index = actor_indexes[Types.Shop][slot]
                        else:
                            actor_index = actor_indexes[item.new_item]
                        ROM().seek(0x1FF1200 + (4 * bonus_table_offset))
                        ROM().writeMultipleBytes(item.old_flag, 2)
                        ROM().writeMultipleBytes(actor_index, 1)
                        bonus_table_offset += 1
                    elif item.location in (Locations.AztecTinyBeetleRace, Locations.CavesLankyBeetleRace):
                        text_index = getTextRewardIndex(item)
                        if item.location == Locations.AztecTinyBeetleRace:
                            ROM().seek(sav + 0x50)
                        else:
                            ROM().seek(sav + 0x51)
                        ROM().write(text_index)
                elif item.old_item == Types.Kong:
                    for i in range(4):
                        if item.new_item is None or item.new_item == Types.NoItem:
                            # Write Empty Cage
                            ROM().seek(sav + 0x152 + (2 * i))
                            ROM().writeMultipleBytes(0xFF, 1)
                else:
                    if item.old_item != Types.Medal:
                        if item.new_item is None:
                            actor_index = 153
                        elif item.new_item == Types.Blueprint:
                            actor_index = actor_indexes[Types.Blueprint][item.new_kong]
                        elif item.new_item == Types.Coin:
                            actor_index = actor_indexes[Types.Coin][0]
                            if item.new_flag == 379:  # Is RW Coin
                                actor_index = actor_indexes[Types.Coin][1]
                        elif item.new_item in (Types.Shop, Types.Shockwave, Types.TrainingBarrel):
                            if (item.new_flag & 0x8000) == 0:
                                slot = 5
                            else:
                                slot = (item.new_flag >> 12) & 7
                                if item.shared or slot > 5:
                                    slot = 5
                            actor_index = actor_indexes[Types.Shop][slot]
                        elif item.new_item == Types.Kong:
                            slot = 0
                            if item.new_flag in kong_flags:
                                slot = kong_flags.index(item.new_flag)
                            actor_index = actor_indexes[Types.Kong][slot]
                        else:
                            actor_index = actor_indexes[item.new_item]
                    if item.old_item == Types.Blueprint:
                        # Write to BP Table
                        # Just needs to store an array of actors spawned
                        offset = item.old_flag - 469
                        ROM().seek(0x1FF1000 + offset)
                        ROM().write(actor_index)
                    elif item.old_item == Types.Crown:
                        # Write to Crown Table
                        crown_flags = [0x261, 0x262, 0x263, 0x264, 0x265, 0x268, 0x269, 0x266, 0x26A, 0x267]
                        ROM().seek(0x1FF10C0 + crown_flags.index(item.old_flag))
                        ROM().write(actor_index)
                    elif item.old_item == Types.Key:
                        key_flags = [26, 74, 138, 168, 236, 292, 317, 380]
                        ROM().seek(0x1FF10D0 + key_flags.index(item.old_flag))
                        ROM().write(actor_index)
                    elif item.old_item == Types.Medal:
                        # Write to Medal Table
                        # Just need offset of subtype:
                        # 0 = Banana
                        # 1 = BP
                        # 2 = Key
                        # 3 = Crown
                        # 4 = Special Coin
                        # 5 = Medal
                        # 6 = Cranky Item
                        # 7 = Funky Item
                        # 8 = Candy Item
                        # 9 = Training Barrel
                        # 10 = Shockwave
                        # 11 = Kong
                        # 12 = Bean
                        # 13 = Pearl
                        # 14 = Nothing
                        slots = [
                            Types.Banana,  # GB
                            Types.Blueprint,  # BP
                            Types.Key,  # Key
                            Types.Crown,  # Crown
                            Types.Coin,  # Special Coin
                            Types.Medal,  # Medal
                            Types.Shop,  # Cranky Item
                            Types.Shop,  # Funky Item
                            Types.Shop,  # Candy Item
                            Types.TrainingBarrel,  # Training Move
                            Types.Shockwave,  # Fairy Item
                            Types.Kong,  # Kong
                            Types.Bean,  # Bean
                            Types.Pearl,  # Pearl
                            None,  # No Item
                        ]
                        offset = item.old_flag - 549
                        ROM().seek(0x1FF1080 + offset)
                        if item.new_item == Types.Shop:
                            medal_index = 6
                            if item.new_flag in (0x290, 0x291):
                                medal_index = 6
                            elif item.new_flag in (0x292, 0x293):
                                medal_index = 7
                            elif item.new_flag in (0x294, 0x295, 0x296):
                                medal_index = 8
                            else:
                                subtype = (item.new_flag >> 8) & 0xF
                                if subtype == 4:
                                    medal_index = 8
                                elif (subtype == 2) or (subtype == 3):
                                    medal_index = 7
                            ROM().write(medal_index)
                        else:
                            ROM().write(slots.index(item.new_item))
                    elif item.location == Locations.JapesChunkyBoulder:
                        # Write to Boulder Spawn Location
                        ROM().seek(sav + 0x114)
                        ROM().write(actor_index)
                    elif item.location == Locations.AztecLankyVulture:
                        # Write to Vulture Spawn Location
                        ROM().seek(sav + 0x115)
                        ROM().write(actor_index)
                    elif item.old_item == Types.Banana:
                        # Bonus GB Table
                        ROM().seek(0x1FF1200 + (4 * bonus_table_offset))
                        ROM().writeMultipleBytes(item.old_flag, 2)
                        ROM().writeMultipleBytes(actor_index, 1)
                        bonus_table_offset += 1
            if not item.is_shop and item.can_have_item and item.old_item != Types.Kong:
                # Write flag lookup table
                data = [item.old_flag]
                if item.new_item is None:
                    data.append(0)
                else:
                    data.append(item.new_flag)
                flut_items.append(data)
            # Text stuff
            if item.location in textboxes:
                textbox = textboxes[item.location]
                replacement = textbox.replacement_text
                if not textbox.force_pipe:
                    reward_text = "|"
                    reference = None
                    if item.new_item in text_rewards:
                        reference = text_rewards[item.new_item]
                    elif item.new_item == Types.Coin:
                        reference = nintendo_coin_reward
                        if item.new_flag == 379:
                            reference = rareware_coin_reward
                    if reference is not None:
                        # Found reference
                        reward_text = reference[0]
                        if item.location == Locations.GalleonDonkeySealRace:
                            # Use pirate text
                            reward_text = reference[1]
                    replacement = replacement.replace("|", reward_text)
                data = {"textbox_index": textbox.textbox_index, "mode": "replace", "search": textbox.text_replace, "target": replacement}
                if textbox.file_index in spoiler.text_changes:
                    spoiler.text_changes[textbox.file_index].append(data)
                else:
                    spoiler.text_changes[textbox.file_index] = [data]

        # Terminate FLUT
        flut_items.append([0xFFFF, 0xFFFF])
        ROM().seek(0x1FF2000)
        for flut in sorted(flut_items, key=lambda x: x[0]):
            for flag in flut:
                ROM().writeMultipleBytes(flag, 2)
        # Setup Changes
        for map_id in map_items:
            cont_map_setup_address = js.pointer_addresses[9]["entries"][map_id]["pointing_to"]
            ROM().seek(cont_map_setup_address)
            model2_count = int.from_bytes(ROM().readBytes(4), "big")
            for item in range(model2_count):
                start = cont_map_setup_address + 4 + (item * 0x30)
                ROM().seek(start + 0x2A)
                item_id = int.from_bytes(ROM().readBytes(2), "big")
                for item_slot in map_items[map_id]:
                    if item_slot["id"] == item_id:
                        ROM().seek(start + 0x28)
                        old_item = int.from_bytes(ROM().readBytes(2), "big")
                        if old_item in model_two_items:
                            ROM().seek(start + 0x28)
                            item_obj_index = 0
                            if item_slot["obj"] == Types.Blueprint:
                                item_obj_index = model_two_indexes[Types.Blueprint][item_slot["kong"]]
                            elif item_slot["obj"] == Types.Coin:
                                item_obj_index = model_two_indexes[Types.Coin][0]
                                if item_slot["flag"] == 379:
                                    item_obj_index = model_two_indexes[Types.Coin][1]
                            elif item_slot["obj"] == Types.Shop:
                                if (item_slot["flag"] & 0x8000) == 0:
                                    slot = 5
                                else:
                                    slot = (item_slot["flag"] >> 12) & 7
                                    if item_slot["shared"] or slot > 5:
                                        slot = 5
                                item_obj_index = model_two_indexes[Types.Shop][slot]
                            elif item_slot["obj"] == Types.Kong:
                                slot = 0
                                if item_slot["flag"] in kong_flags:
                                    slot = kong_flags.index(item_slot["flag"])
                                item_obj_index = model_two_indexes[Types.Kong][slot]
                            else:
                                item_obj_index = model_two_indexes[item_slot["obj"]]
                            ROM().writeMultipleBytes(item_obj_index, 2)
                            # Scaling fix
                            ROM().seek(start + 0xC)
                            old_scale = intf_to_float(int.from_bytes(ROM().readBytes(4), "big"))
                            new_scale = old_scale * item_slot["upscale"]
                            ROM().seek(start + 0xC)
                            ROM().writeMultipleBytes(int(float_to_hex(new_scale), 16), 4)
