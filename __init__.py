"""File specifically used for the cases of archipelago generation."""

import os
import typing
import math
import threading
import time
import json
import zipfile
import codecs
from io import BytesIO
import pkgutil
import shutil
import sys

from worlds.dk64.ap_version import version as ap_version

baseclasses_loaded = False
try:
    from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification, CollectionState
    import BaseClasses

    baseclasses_loaded = True
except ImportError:
    pass
if baseclasses_loaded:
    baseclasses_path = os.path.dirname(os.path.dirname(BaseClasses.__file__))
    if not baseclasses_path.endswith("lib"):
        baseclasses_path = os.path.join(baseclasses_path, "lib")

    def display_error_box(title: str, text: str) -> bool | None:
        """Display an error message box."""
        from tkinter import Tk, messagebox

        root = Tk()
        root.withdraw()
        ret = messagebox.showerror(title, text)
        root.update()

    def copy_dependencies(zip_path, file):
        """Copy a ZIP file from the package to a local directory, extracts its contents.

        Ensures the destination directory exists.
        Args:
            zip_path (str): The relative path to the ZIP file within the package.
        Behavior:
            - Creates a `./lib` directory if it does not exist.
            - Reads the ZIP file from the package using `pkgutil.get_data`.
            - Writes the ZIP file to the `./lib` directory if it does not already exist.
            - Extracts the contents of the ZIP file into the `./lib` directory.
        Prints:
            - A message if the ZIP file could not be read.
            - A message when the ZIP file is successfully copied.
            - A message when the ZIP file is successfully extracted.
        """
        # Find the path of BaseClasses, we want to work in the AP directory
        # This is a bit of a hack, but it works
        # Get the path of BaseClasses
        dest_dir = baseclasses_path
        # if baseclasses_path does not end in lib, add lib to the end

        zip_dest = os.path.join(dest_dir, file)
        try:
            # Ensure the destination directory exists
            os.makedirs(dest_dir, exist_ok=True)

            # Load the ZIP file from the package
            zip_data = pkgutil.get_data(__name__, zip_path)
            # Check if the zip already exists in the destination
            if not os.path.exists(zip_dest):
                if zip_data is None:
                    print(f"Failed to read {zip_path}")
                else:
                    # Write the ZIP file to the destination
                    with open(zip_dest, "wb") as f:
                        f.write(zip_data)
                    print(f"Copied {zip_path} to {zip_dest}")

                    # Extract the ZIP file
                    with zipfile.ZipFile(zip_dest, "r") as zip_ref:
                        zip_ref.extractall(dest_dir)
                    print(f"Extracted {zip_dest} into {dest_dir}")
        except PermissionError:
            display_error_box("Permission Error", "Unable to install Dependencies to AP, please try to install AP as an admin.")
            raise PermissionError("Permission Error: Unable to install Dependencies to AP, please try to install AP as an admin.")

    platform_type = sys.platform
    # if the file pyxdelta.cp310-win_amd64.pyd exists, delete pyxdelta.cp310-win_amd64.pyd and PIL and pillow-10.3.0.dist-info and pyxdelta-0.2.0.dist-info
    if os.path.exists(f"{baseclasses_path}/pyxdelta.cp310-win_amd64.pyd"):
        os.remove(f"{baseclasses_path}/pyxdelta.cp310-win_amd64.pyd")
        if os.path.exists(f"{baseclasses_path}/PIL"):
            shutil.rmtree(f"{baseclasses_path}/PIL")
        if os.path.exists(f"{baseclasses_path}/pillow-10.3.0.dist-info"):
            shutil.rmtree(f"{baseclasses_path}/pillow-10.3.0.dist-info")
        if os.path.exists(f"{baseclasses_path}/pyxdelta-0.2.0.dist-info"):
            shutil.rmtree(f"{baseclasses_path}/pyxdelta-0.2.0.dist-info")
        if os.path.exists(f"{baseclasses_path}/windows.zip"):
            os.remove(f"{baseclasses_path}/windows.zip")
        if os.path.exists(f"{baseclasses_path}/linux.zip"):
            os.remove(f"{baseclasses_path}/linux.zip")
    if platform_type == "win32":
        zip_path = "vendor/windows.zip"  # Path inside the package
        copy_dependencies(zip_path, "windows.zip")
    elif platform_type == "linux":
        zip_path = "vendor/linux.zip"
        copy_dependencies(zip_path, "linux.zip")
    else:
        raise Exception(f"Unsupported platform: {platform_type}")

    sys.path.append("worlds/dk64/")
    sys.path.append("worlds/dk64/archipelago/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/archipelago/")
    import randomizer.ItemPool as DK64RItemPool

    from randomizer.Enums.Items import Items as DK64RItems
    from randomizer.SettingStrings import decrypt_settings_string_enum
    from archipelago.Items import DK64Item, full_item_table, setup_items
    from archipelago.Options import DK64Options, Goal
    from archipelago.Regions import all_locations, create_regions, connect_regions
    from archipelago.Rules import set_rules
    from archipelago.client.common import check_version
    from worlds.AutoWorld import WebWorld, World, AutoLogicRegister
    from archipelago.Logic import LogicVarHolder
    from randomizer.Spoiler import Spoiler
    from randomizer.Settings import Settings
    from randomizer.ShuffleWarps import LinkWarps
    from randomizer.Enums.Settings import ShuffleLoadingZones
    from randomizer.Patching.ApplyRandomizer import patching_response
    from version import version
    from randomizer.Patching.EnemyRando import randomize_enemies_0
    from randomizer.Fill import ShuffleItems, ItemReference, IdentifyMajorItems
    from randomizer.CompileHints import compileMicrohints
    from randomizer.Enums.Types import Types
    from randomizer.Enums.Kongs import Kongs
    from randomizer.Enums.Maps import Maps
    from randomizer.Enums.Locations import Locations as DK64RLocations
    from randomizer.Enums.Settings import WinConditionComplex
    from randomizer.Lists import Item as DK64RItem
    from worlds.LauncherComponents import Component, components, Type, icon_paths
    import randomizer.ShuffleExits as ShuffleExits
    from Utils import open_filename
    import shutil
    import zlib

    boss_map_names = {
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

    def crc32_of_file(file_path):
        """Compute CRC32 checksum of a file."""
        crc_value = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                crc_value = zlib.crc32(chunk, crc_value)
        return f"{crc_value & 0xFFFFFFFF:08X}"  # Convert to 8-character hex

    def launch_client():
        """Launch the DK64 client."""
        from archipelago.DK64Client import launch
        from worlds.LauncherComponents import launch as launch_component

        launch_component(launch, name="DK64 Client")

    components.append(Component("DK64 Client", "DK64Client", func=launch_client, component_type=Type.CLIENT, icon="dk64"))
    icon_paths["dk64"] = f"ap:{__name__}/base-hack/assets/DKTV/logo3.png"

    class DK64CollectionState(metaclass=AutoLogicRegister):
        """Logic Mixin to handle some awkward situations when the CollectionState is copied."""

        def init_mixin(self, parent: MultiWorld):
            """Reset the logic holder in all DK64 worlds. This is called on every CollectionState init."""
            dk64_ids = parent.get_game_players(DK64World.game) + parent.get_game_groups(DK64World.game)
            for player in dk64_ids:
                if hasattr(parent.worlds[player], "logic_holder"):
                    parent.worlds[player].logic_holder.Reset()  # If we don't reset here, we double-collect the starting inventory

        def copy_mixin(self, ret) -> CollectionState:
            """Update the current logic holder in all DK64 worlds with the current CollectionState. This is called after the CollectionState init inside the copy() method, so this essentially undoes the above method."""
            dk64_ids = ret.multiworld.get_game_players(DK64World.game) + ret.multiworld.get_game_groups(DK64World.game)
            for player in dk64_ids:
                if hasattr(ret.multiworld.worlds[player], "logic_holder"):
                    ret.multiworld.worlds[player].logic_holder.UpdateFromArchipelagoItems(ret)  # If we don't update here, every copy wipes the logic holder's knowledge
            return ret

    class DK64Web(WebWorld):
        """WebWorld for DK64."""

        theme = "jungle"

        setup_en = Tutorial("Multiworld Setup Guide", "A guide to setting up the Donkey Kong 64 randomizer connected to an Archipelago Multiworld.", "English", "setup_en.md", "setup/en", ["PoryGone"])

        tutorials = [setup_en]

    class DK64World(World):
        """Donkey Kong 64 is a 3D collectathon platforming game.

        Play as the whole DK Crew and rescue the Golden Banana hoard from King K. Rool.
        """

        game: str = "Donkey Kong 64"
        options_dataclass = DK64Options
        options: DK64Options
        topology_present = False

        item_name_to_id = {name: data.code for name, data in full_item_table.items()}
        location_name_to_id = all_locations

        web = DK64Web()

        def __init__(self, multiworld: MultiWorld, player: int):
            """Initialize the DK64 world."""
            self.rom_name_available_event = threading.Event()
            super().__init__(multiworld, player)

        @classmethod
        def stage_assert_generate(cls, multiworld: MultiWorld):
            """Assert the stage and generate the world."""
            # Check if dk64.z64 exists, if it doesn't prompt the user to provide it
            # ANd then we will copy it to the root directory
            crc_values = ["D44B4FC6"]
            rom_file = "dk64.z64"
            if not os.path.exists(rom_file):
                print("Please provide a DK64 ROM file.")
                file = open_filename("Select DK64 ROM", (("N64 ROM", (".z64", ".n64")),))
                if not file:
                    raise FileNotFoundError("No ROM file selected.")
                crc = crc32_of_file(file)
                print(f"CRC32: {crc}")
                if crc not in crc_values:
                    print("Invalid DK64 ROM file, please make sure your ROM is big endian.")
                    raise FileNotFoundError("Invalid DK64 ROM file, please make sure your ROM is a vanilla DK64 file in big endian.")
                # Copy the file to the root directory
                try:
                    shutil.copy(file, rom_file)
                except Exception as e:
                    raise FileNotFoundError(f"Failed to copy ROM file, this may be a permissions issue: {e}")
            else:
                crc = crc32_of_file(rom_file)
                print(f"CRC32: {crc}")
                if crc not in crc_values:
                    print("Invalid DK64 ROM file, please make sure your ROM is big endian.")
                    raise FileNotFoundError("Invalid DK64 ROM file, please make sure your ROM is a vanilla DK64 file in big endian.")
            check_version()

        def _get_slot_data(self):
            """Get the slot data."""
            return {
                # "death_link": self.options.death_link.value,
            }

        def generate_early(self):
            """Generate the world."""
            # V1 LIMITATION: We are restricting settings pretty heavily. This string serves as the base for all seeds, with AP options overriding some options
            self.settings_string = "fjNPxAMxDIUx0QSpbHPUlZlBLg5gPQ+oBwRDIhKlsa58Iz8fiNEpEtiFKi4bVAhMF6AAd+AAOCAAGGAAGKAAAdm84FBiMhjoStwFIKW2wLcBJIBpmTVRCjFIKUUwGTLK/BQBuAIMAN4CBwBwAYQAOIECQByAoUAOYGCwB0A4YeXIITIagOrIrwAZTiU1QwkoSjuq1ZLEjQxUKi2oy9FRFgETEUAViyxyN2S8XeRQOQ7GXtOQM8jGDIAyqcEQgAFwoAFwwAEw4AExAAD1oADxIACxQABxYADxgACxoAB1wAFp8r0CS5UtnsshhHMk9Gw+M1drAwGcuqwqis0FMqLRjilACgrBovKATiotEkXENPGtLINIiNdHYAHQC8KggJCgsMDQ4QERIUFRYYGRocHR4gISIjJCUmJygpKissLS4vMDEyMzQ1rL4AwADCAMQAnQCyAGkAUQA"
            settings_dict = decrypt_settings_string_enum(self.settings_string)
            settings_dict["archipelago"] = True
            settings_dict["starting_kongs_count"] = self.options.starting_kong_count.value
            settings_dict["starting_keys_list_selected"] = []
            for item in self.options.start_inventory:
                if item == "Key 1":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.JungleJapesKey)
                elif item == "Key 2":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.AngryAztecKey)
                elif item == "Key 3":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.FranticFactoryKey)
                elif item == "Key 4":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.GloomyGalleonKey)
                elif item == "Key 5":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.FungiForestKey)
                elif item == "Key 6":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.CrystalCavesKey)
                elif item == "Key 7":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.CreepyCastleKey)
                elif item == "Key 8":
                    settings_dict["starting_keys_list_selected"].append(DK64RItems.HideoutHelmKey)
            if self.options.goal == Goal.option_all_keys:
                settings_dict["win_condition_item"] = WinConditionComplex.req_key
                settings_dict["win_condition_count"] = 8
            settings = Settings(settings_dict, self.random)
            # We need to set the freeing kongs here early, as they won't get filled in any other part of the AP process
            settings.diddy_freeing_kong = self.random.randint(0, 4)
            settings.lanky_freeing_kong = self.random.randint(0, 4)
            settings.tiny_freeing_kong = self.random.randint(0, 4)
            settings.chunky_freeing_kong = self.random.randint(0, 4)
            spoiler = Spoiler(settings)
            # Undo any changes to this location's name, until we find a better way to prevent this from confusing the tracker and the AP code that is responsible for sending out items
            spoiler.LocationList[DK64RLocations.FactoryDonkeyDKArcade].name = "Factory Donkey DK Arcade Round 1"
            spoiler.settings.shuffled_location_types.append(Types.ArchipelagoItem)
            self.logic_holder = LogicVarHolder(spoiler, self.player)

            for item in self.options.start_inventory:
                item_obj = DK64RItem.ItemList[self.logic_holder.item_name_to_id.get(item)]
                if item_obj.type not in [Types.Key, Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing]:
                    # Ensure that the items in the start inventory are only keys, shops, shockwaves, training barrels or climbing items
                    raise ValueError(f"Invalid item type for starting inventory: {item}. Starting inventory can only contain keys or moves.")

            # Handle enemy rando
            spoiler = self.logic_holder.spoiler
            spoiler.enemy_rando_data = {}
            spoiler.pkmn_snap_data = []
            if spoiler.settings.enemy_rando:
                randomize_enemies_0(spoiler)
            # Handle Loading Zones - this will handle LO and (someday?) LZR appropriately
            if spoiler.settings.shuffle_loading_zones != ShuffleLoadingZones.none:
                ShuffleExits.ExitShuffle(spoiler, skip_verification=True)
                spoiler.UpdateExits()

        def create_regions(self) -> None:
            """Create the regions."""
            create_regions(self.multiworld, self.player, self.logic_holder)

        def create_items(self) -> None:
            """Create the items."""
            itempool: typing.List[DK64Item] = setup_items(self)
            self.multiworld.itempool += itempool

        def get_filler_item_name(self) -> str:
            """Get the filler item name."""
            return DK64RItems.JunkMelon.name

        def set_rules(self):
            """Set the rules."""
            set_rules(self.multiworld, self.player)

        def generate_basic(self):
            """Generate the basic world."""
            LinkWarps(self.logic_holder.spoiler)  # I am very skeptical that this works at all - must be resolved if we want to do more than Isles warps preactivated
            connect_regions(self, self.logic_holder)

            self.multiworld.get_location("Banana Hoard", self.player).place_locked_item(DK64Item("Banana Hoard", ItemClassification.progression_skip_balancing, 0xD64060, self.player))  # TEMP?

        def generate_output(self, output_directory: str):
            """Generate the output."""
            try:
                spoiler = self.logic_holder.spoiler
                spoiler.settings.archipelago = True
                spoiler.settings.random = self.random
                spoiler.settings.player_name = self.multiworld.get_player_name(self.player)
                spoiler.first_move_item = None  # Not relevant with Fast Start always enabled
                spoiler.pregiven_items = []
                for item in self.multiworld.precollected_items[self.player]:
                    dk64_item = self.logic_holder.item_name_to_id[item.name]
                    # Only moves can be pushed to the pregiven_items list
                    if DK64RItem.ItemList[dk64_item].type in [Types.Shop, Types.Shockwave, Types.TrainingBarrel, Types.Climbing]:
                        spoiler.pregiven_items.append(dk64_item)
                local_trap_count = 0
                ap_item_is_major_item = False
                # Read through all item assignments in this AP world and find their DK64 equivalents so we can update our world state for patching purposes
                for ap_location in self.multiworld.get_locations(self.player):
                    # We never need to place Collectibles or Events in our world state
                    if "Collectible" in ap_location.name or "Event" in ap_location.name:
                        continue
                    # Find the corresponding DK64 Locations enum
                    dk64_location_id = None
                    for dk64_loc_id, dk64_loc in spoiler.LocationList.items():
                        if dk64_loc.name == ap_location.name:
                            dk64_location_id = dk64_loc_id
                            break
                    if dk64_location_id is not None and ap_location.item is not None:
                        ap_item = ap_location.item
                        # Any item that isn't for this player is placed as an AP item, regardless of whether or not it could be a DK64 item
                        if ap_item.player != self.player:
                            spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, DK64RItems.ArchipelagoItem)
                            # If Jetpac has an progression AP item, we should hint is as if it were a major item
                            if dk64_location_id == DK64RLocations.RarewareCoin and ap_item.advancement:
                                ap_item_is_major_item = True
                        # Collectibles don't get placed in the LocationList
                        elif "Collectible" in ap_item.name:
                            continue
                        else:
                            dk64_item = self.logic_holder.item_name_to_id[ap_item.name]
                            if dk64_item is not None:
                                if dk64_item in [DK64RItems.IceTrapBubble, DK64RItems.IceTrapReverse, DK64RItems.IceTrapSlow]:
                                    local_trap_count += 1

                                dk64_location = spoiler.LocationList[dk64_location_id]
                                # Most of these item restrictions should be handled by item rules, so this is a failsafe.
                                # Junk items can't be placed in shops, bosses, or arenas. Fortunately this is junk, so we can just patch a NoItem there instead.
                                # Shops are allowed to get Junk items placed by AP in order to artificially slightly reduce the number of checks in shops.
                                if dk64_item in [DK64RItems.JunkMelon] and dk64_location.type in [Types.Shop, Types.Key, Types.Crown]:
                                    dk64_item = DK64RItems.NoItem
                                # Blueprints can't be on fairies for technical reasons. Instead we'll patch it in as an AP item and have AP handle it.
                                if dk64_item in DK64RItemPool.Blueprints() and dk64_location.type == Types.Fairy:
                                    dk64_item = DK64RItems.ArchipelagoItem
                                spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, dk64_item)
                            else:
                                print(f"Item {ap_item.name} not found in DK64 item table.")
                    elif dk64_location_id is not None:
                        spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, DK64RItems.NoItem)
                    else:
                        print(f"Location {ap_location.name} not found in DK64 location table.")

                spoiler.settings.ice_trap_count = local_trap_count
                ShuffleItems(spoiler)

                spoiler.location_references = [
                    # DK Moves
                    ItemReference(DK64RItems.BaboonBlast, "Baboon Blast", "DK Japes Cranky"),
                    ItemReference(DK64RItems.StrongKong, "Strong Kong", "DK Aztec Cranky"),
                    ItemReference(DK64RItems.GorillaGrab, "Gorilla Grab", "DK Factory Cranky"),
                    ItemReference(DK64RItems.Coconut, "Coconut Gun", "DK Japes Funky"),
                    ItemReference(DK64RItems.Bongos, "Bongo Blast", "DK Aztec Candy"),
                    # Diddy Moves
                    ItemReference(DK64RItems.ChimpyCharge, "Chimpy Charge", "Diddy Japes Cranky"),
                    ItemReference(DK64RItems.RocketbarrelBoost, "Rocketbarrel Boost", "Diddy Aztec Cranky"),
                    ItemReference(DK64RItems.SimianSpring, "Simian Spring", "Diddy Factory Cranky"),
                    ItemReference(DK64RItems.Peanut, "Peanut Popguns", "Diddy Japes Funky"),
                    ItemReference(DK64RItems.Guitar, "Guitar Gazump", "Diddy Aztec Candy"),
                    # Lanky Moves
                    ItemReference(DK64RItems.Orangstand, "Orangstand", "Lanky Japes Cranky"),
                    ItemReference(DK64RItems.BaboonBalloon, "Baboon Balloon", "Lanky Factory Cranky"),
                    ItemReference(DK64RItems.OrangstandSprint, "Orangstand Sprint", "Lanky Caves Cranky"),
                    ItemReference(DK64RItems.Grape, "Grape Shooter", "Lanky Japes Funky"),
                    ItemReference(DK64RItems.Trombone, "Trombone Tremor", "Lanky Aztec Candy"),
                    # Tiny Moves
                    ItemReference(DK64RItems.MiniMonkey, "Mini Monkey", "Tiny Japes Cranky"),
                    ItemReference(DK64RItems.PonyTailTwirl, "Pony Tail Twirl", "Tiny Factory Cranky"),
                    ItemReference(DK64RItems.Monkeyport, "Monkeyport", "Tiny Caves Cranky"),
                    ItemReference(DK64RItems.Feather, "Feather Bow", "Tiny Japes Funky"),
                    ItemReference(DK64RItems.Saxophone, "Saxophone Slam", "Tiny Aztec Candy"),
                    # Chunky Moves
                    ItemReference(DK64RItems.HunkyChunky, "Hunky Chunky", "Chunky Japes Cranky"),
                    ItemReference(DK64RItems.PrimatePunch, "Primate Punch", "Chunky Factory Cranky"),
                    ItemReference(DK64RItems.GorillaGone, "Gorilla Gone", "Chunky Caves Cranky"),
                    ItemReference(DK64RItems.Pineapple, "Pineapple Launcher", "Chunky Japes Funky"),
                    ItemReference(DK64RItems.Triangle, "Triangle Trample", "Chunky Aztec Candy"),
                    # Gun Upgrades
                    ItemReference(DK64RItems.HomingAmmo, "Homing Ammo", "Shared Forest Funky"),
                    ItemReference(DK64RItems.SniperSight, "Sniper Scope", "Shared Castle Funky"),
                    ItemReference(DK64RItems.ProgressiveAmmoBelt, "Progressive Ammo Belt", ["Shared Factory Funky", "Shared Caves Funky"]),
                    ItemReference(DK64RItems.Camera, "Fairy Camera", "Banana Fairy Gift"),
                    ItemReference(DK64RItems.Shockwave, "Shockwave", "Banana Fairy Gift"),
                    # Basic Moves
                    ItemReference(DK64RItems.Swim, "Diving", "Dive Barrel"),
                    ItemReference(DK64RItems.Oranges, "Orange Throwing", "Orange Barrel"),
                    ItemReference(DK64RItems.Barrels, "Barrel Throwing", "Barrel Barrel"),
                    ItemReference(DK64RItems.Vines, "Vine Swinging", "Vine Barrel"),
                    ItemReference(DK64RItems.Climbing, "Climbing", "Starting Move"),
                    # Instrument Upgrades & Slams
                    ItemReference(
                        DK64RItems.ProgressiveInstrumentUpgrade,
                        "Progressive Instrument Upgrade",
                        ["Shared Galleon Candy", "Shared Caves Candy", "Shared Castle Candy"],
                    ),
                    ItemReference(
                        DK64RItems.ProgressiveSlam,
                        "Progressive Slam",
                        ["Shared Isles Cranky", "Shared Forest Cranky", "Shared Castle Cranky"],
                    ),
                    # Kongs
                    ItemReference(DK64RItems.Donkey, "Donkey Kong", "Starting Kong"),
                    ItemReference(DK64RItems.Diddy, "Diddy Kong", "Japes Diddy Cage"),
                    ItemReference(DK64RItems.Lanky, "Lanky Kong", "Llama Lanky Cage"),
                    ItemReference(DK64RItems.Tiny, "Tiny Kong", "Aztec Tiny Cage"),
                    ItemReference(DK64RItems.Chunky, "Chunky Kong", "Factory Chunky Cage"),
                    # Shopkeepers
                    ItemReference(DK64RItems.Cranky, "Cranky Kong", "Starting Item"),
                    ItemReference(DK64RItems.Candy, "Candy Kong", "Starting Item"),
                    ItemReference(DK64RItems.Funky, "Funky Kong", "Starting Item"),
                    ItemReference(DK64RItems.Snide, "Snide", "Starting Item"),
                    # Early Keys
                    ItemReference(DK64RItems.JungleJapesKey, "Key 1", "Starting Key"),
                    ItemReference(DK64RItems.AngryAztecKey, "Key 2", "Starting Key"),
                    ItemReference(DK64RItems.FranticFactoryKey, "Key 3", "Starting Key"),
                    ItemReference(DK64RItems.GloomyGalleonKey, "Key 4", "Starting Key"),
                    # Late Keys
                    ItemReference(DK64RItems.FungiForestKey, "Key 5", "Starting Key"),
                    ItemReference(DK64RItems.CrystalCavesKey, "Key 6", "Starting Key"),
                    ItemReference(DK64RItems.CreepyCastleKey, "Key 7", "Starting Key"),
                    ItemReference(DK64RItems.HideoutHelmKey, "Key 8", "Starting Key"),
                ]
                spoiler.UpdateLocations(spoiler.LocationList)
                compileMicrohints(spoiler)
                spoiler.majorItems = IdentifyMajorItems(spoiler)
                if ap_item_is_major_item:
                    spoiler.majorItems.append(DK64RItems.ArchipelagoItem)
                patch_data, _ = patching_response(spoiler)
                patch_file = self.update_seed_results(patch_data, spoiler, self.player)
                out_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.lanky")
                print(out_path)
                # with open("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}.lanky", "w") as f:
                with open(out_path, "w") as f:
                    f.write(patch_file)
                # Copy the patch file to the outpath
                # shutil.copy("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}.lanky", out_path)
                # Clear the path_data out of memory to flush memory usage
                del patch_data
            except Exception:
                raise
            finally:
                self.rom_name_available_event.set()  # make sure threading continues and errors are collected

        def update_seed_results(self, patch, spoiler, player_id):
            """Update the seed results."""
            timestamp = time.time()
            hash = spoiler.settings.seed_hash
            spoiler_log = {}
            spoiler_log["Generated Time"] = timestamp
            spoiler_log["Settings"] = {}
            spoiler_log["Cosmetics"] = {}
            # Zip all the data into a single file.
            zip_data = BytesIO()
            with zipfile.ZipFile(zip_data, "w") as zip_file:
                # Write each variable to the zip file
                zip_file.writestr("patch", patch)
                zip_file.writestr("hash", str(hash))
                zip_file.writestr("spoiler_log", str(json.dumps(spoiler_log)))
                zip_file.writestr("generated_time", str(timestamp))
                zip_file.writestr("version", version)
                zip_file.writestr("seed_number", self.multiworld.get_out_file_name_base(self.player))
                zip_file.writestr("seed_id", self.multiworld.get_out_file_name_base(self.player))
            zip_data.seek(0)
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()

            return zip_conv

        def modify_multidata(self, multidata: dict):
            """Modify the multidata."""
            pass

        def fill_slot_data(self) -> dict:
            """Fill the slot data."""
            return {
                "Goal": self.options.goal.value,
                "ClimbingShuffle": self.options.climbing_shuffle.value,
                "PlayerNum": self.player,
                "death_link": self.options.death_link.value,
                "receive_notifications": self.options.receive_notifications.value,
                "LevelOrder": ", ".join([level.name for order, level in self.logic_holder.settings.level_order.items()]),
                "StartingKongs": ", ".join([kong.name for kong in self.logic_holder.settings.starting_kong_list]),
                "ForestTime": self.logic_holder.settings.fungi_time_internal.name,
                "GalleonWater": self.logic_holder.settings.galleon_water_internal.name,
                "MedalCBRequirement": self.logic_holder.settings.medal_cb_req,
                "BLockerValues": self.logic_holder.settings.BLockerEntryCount,
                "RemovedBarriers": ", ".join([barrier.name for barrier in self.logic_holder.settings.remove_barriers_selected]),
                "FairyRequirement": self.logic_holder.settings.rareware_gb_fairies,
                "MermaidPearls": self.logic_holder.settings.mermaid_gb_pearls,
                "JetpacReq": self.logic_holder.settings.medal_requirement,
            }

        def write_spoiler(self, spoiler_handle: typing.TextIO):
            """Write the spoiler."""
            spoiler_handle.write("\n")
            spoiler_handle.write("Additional Settings info for player: " + self.player_name)
            spoiler_handle.write("\n")
            spoiler_handle.write("Level Order: " + ", ".join([level.name for order, level in self.logic_holder.settings.level_order.items()]))
            spoiler_handle.write("\n")
            human_boss_order = []
            for i in range(len(self.logic_holder.settings.boss_maps)):
                human_boss_order.append(boss_map_names[self.logic_holder.settings.boss_maps[i]])
            spoiler_handle.write("Boss Order: " + ", ".join(human_boss_order))
            spoiler_handle.write("\n")
            spoiler_handle.write("Starting Kongs: " + ", ".join([kong.name for kong in self.logic_holder.settings.starting_kong_list]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Helm Order: " + ", ".join([Kongs(room).name for room in self.logic_holder.settings.helm_order]))
            spoiler_handle.write("\n")
            spoiler_handle.write("K. Rool Order: " + ", ".join([phase.name for phase in self.logic_holder.settings.krool_order]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Forest Time: " + self.logic_holder.settings.fungi_time_internal.name)
            spoiler_handle.write("\n")
            spoiler_handle.write("Galleon Water: " + self.logic_holder.settings.galleon_water_internal.name)
            spoiler_handle.write("\n")
            spoiler_handle.write("CBs for Medal: " + str(self.logic_holder.settings.medal_cb_req))
            spoiler_handle.write("\n")
            spoiler_handle.write("B. Locker Requirements: " + ", ".join([str(count) for count in self.logic_holder.settings.BLockerEntryCount]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Removed Barriers: " + ", ".join([barrier.name for barrier in self.logic_holder.settings.remove_barriers_selected]))
            spoiler_handle.write("\n")
            spoiler_handle.write("Generated Time: " + time.strftime("%d-%m-%Y %H:%M:%S", time.gmtime()) + " GMT")
            spoiler_handle.write("\n")
            spoiler_handle.write("Randomizer Version: " + self.logic_holder.settings.version)
            spoiler_handle.write("\n")
            spoiler_handle.write("APWorld Version: " + ap_version)
            spoiler_handle.write("\n")

        def create_item(self, name: str, force_non_progression=False) -> Item:
            """Create an item."""
            data = full_item_table[name]

            if force_non_progression:
                classification = ItemClassification.filler
            elif data.progression:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler

            created_item = DK64Item(name, classification, data.code, self.player)

            return created_item

        def collect(self, state: CollectionState, item: Item) -> bool:
            """Collect the item."""
            change = super().collect(state, item)
            if change:
                self.logic_holder.UpdateFromArchipelagoItems(state)
            return change
