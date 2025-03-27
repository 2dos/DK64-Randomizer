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

baseclasses_loaded = False
try:
    from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification

    baseclasses_loaded = True
except ImportError:
    pass
if baseclasses_loaded:

    def copy_dependencies(zip_path):
        dest_dir = "./lib"
        zip_dest = os.path.join(dest_dir, "windows.zip")

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

    platform_type = sys.platform
    try:
        from PIL import Image  # Check if PIL is installed
    except ImportError:
        if platform_type == "win32":
            zip_path = "vendor/windows.zip"  # Path inside the package
            copy_dependencies(zip_path)

    sys.path.append("worlds/dk64/")
    sys.path.append("worlds/dk64/archipelago/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/")
    sys.path.append("custom_worlds/dk64.apworld/dk64/archipelago/")
    import randomizer.ItemPool as DK64RItemPool

    from randomizer.Enums.Items import Items as DK64RItems
    from randomizer.SettingStrings import decrypt_settings_string_enum
    from archipelago.Items import DK64Item, full_item_table, setup_items
    from archipelago.Options import DK64Options
    from archipelago.Regions import all_locations, create_regions, connect_regions
    from archipelago.Rules import set_rules
    from worlds.AutoWorld import WebWorld, World
    from archipelago.Logic import LogicVarHolder
    from randomizer.Spoiler import Spoiler
    from randomizer.Settings import Settings
    from randomizer.Enums.Settings import ShuffleLoadingZones
    from randomizer.Patching.ApplyRandomizer import patching_response
    from version import version
    from randomizer.Patching.EnemyRando import randomize_enemies_0
    from randomizer.Fill import ShuffleItems, ItemReference, IdentifyMajorItems
    from randomizer.CompileHints import compileMicrohints
    from randomizer.Enums.Types import Types
    from randomizer.Enums.Locations import Locations
    from randomizer.Lists.Location import PreGivenLocations
    from worlds.LauncherComponents import Component, components, Type, icon_paths
    import randomizer.ShuffleExits as ShuffleExits
    from Utils import open_filename
    import shutil
    import zlib

    def crc32_of_file(file_path):
        """Compute CRC32 checksum of a file."""
        crc_value = 0
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                crc_value = zlib.crc32(chunk, crc_value)
        return f"{crc_value & 0xFFFFFFFF:08X}"  # Convert to 8-character hex

    def launch_client():
        from archipelago.DK64Client import launch
        from worlds.LauncherComponents import launch as launch_component

        launch_component(launch, name="DK64 Client")

    components.append(Component("DK64 Client", "DK64Client", func=launch_client, component_type=Type.CLIENT, icon="dk64"))
    icon_paths["dk64"] = f"ap:{__name__}/static/img/dk.png"

    class DK64Web(WebWorld):
        theme = "jungle"

        setup_en = Tutorial("Multiworld Setup Guide", "A guide to setting up the Donkey Kong 64 randomizer connected to an Archipelago Multiworld.", "English", "setup_en.md", "setup/en", ["PoryGone"])

        tutorials = [setup_en]

    class DK64World(World):
        """
        Donkey Kong 64 is a 3D collectathon platforming game.
        Play as the whole DK Crew and rescue the Golden Banana hoard from King K. Rool.
        """

        game: str = "Donkey Kong 64"
        options_dataclass = DK64Options
        options: DK64Options
        topology_present = False
        data_version = 0

        item_name_to_id = {name: data.code for name, data in full_item_table.items()}
        location_name_to_id = all_locations

        web = DK64Web()

        def __init__(self, multiworld: MultiWorld, player: int):
            # Check if dk64.z64 exists, if it doesn't prompt the user to provide it
            # ANd then we will copy it to the root directory
            crc_values = ["D44B4FC6", "AA0A5979", "96972D67"]
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

            self.rom_name_available_event = threading.Event()
            super().__init__(multiworld, player)

        @classmethod
        def stage_assert_generate(cls, multiworld: MultiWorld):
            # rom_file = get_base_rom_path()
            # if not os.path.exists(rom_file):
            #    raise FileNotFoundError(rom_file)
            pass

        def _get_slot_data(self):
            return {
                # "death_link": self.options.death_link.value,
            }

        def generate_early(self):
            # V1 LIMITATION: We are restricting settings pretty heavily. This string serves as the base for all seeds, with AP options overriding some options
            self.settings_string = "fjNPxAMxDIUx0QSpbHPUlZlBLg5gPQ+oBwRDIhKlsa58Iz8fiNEpEtiFKi4bVAhMF6AAd+AAOCAAGGAAGKAAAdm84FBiMhjoStwFIKW2wLcBJIBpkzVRCjFIKUUwGTLK/BQBuAIMAN4CBwBwAYQAOIECQByAoUAOYGCwB0A4YeXIITIagOrIrwAZTiU1QwkoSjuq1ZLEjQ0gRydoVFtRl6KiLAImIoArFljkbsl4u8igch2MvacgZ5GMGQBlU4IhAALhQALhgAJhwAJiAAHrQAHiQAFigADiwAHjAAFjQADrgALT5XoElypbPZZDCOZJ6Nh8Zq7WBgM5dVhVFZoKZUWjHFKAFBWDReUAnFRaJIuIZiTxrSyDSIjXR2AB0AvCoICQoLDA0OEBESFBUWGBkaHB0eICEiIyQlJicoKSorLC0uLzAxMjM0Nay+AMAAwgDEAJ0AsgBRAA"
            settings_dict = decrypt_settings_string_enum(self.settings_string)
            settings_dict["archipelago"] = True
            settings_dict["starting_kongs_count"] = self.options.starting_kong_count.value
            settings = Settings(settings_dict, self.random)
            # We need to set the freeing kongs here early, as they won't get filled in any other part of the AP process
            settings.diddy_freeing_kong = self.random.randint(0, 4)
            settings.lanky_freeing_kong = self.random.randint(0, 4)
            settings.tiny_freeing_kong = self.random.randint(0, 4)
            settings.chunky_freeing_kong = self.random.randint(0, 4)
            spoiler = Spoiler(settings)
            spoiler.settings.shuffled_location_types.append(Types.ArchipelagoItem)
            self.logic_holder = LogicVarHolder(spoiler, self)

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
            create_regions(self.multiworld, self.player, self.logic_holder)

        def create_items(self) -> None:
            itempool: typing.List[DK64Item] = setup_items(self)
            self.multiworld.itempool += itempool

        def get_filler_item_name(self) -> str:
            return DK64RItems.JunkMelon.name

        def set_rules(self):
            set_rules(self.multiworld, self.player)

        def generate_basic(self):
            connect_regions(self, self.logic_holder)

            self.multiworld.get_location("Banana Hoard", self.player).place_locked_item(DK64Item("BananaHoard", ItemClassification.progression, 0xD64060, self.player))  # TEMP?

        def generate_output(self, output_directory: str):
            try:
                spoiler = self.logic_holder.spoiler
                spoiler.settings.archipelago = True
                spoiler.settings.random = self.random
                spoiler.settings.player_name = self.multiworld.get_player_name(self.player)
                spoiler.pregiven_items = []
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
                        if dk64_loc_id in PreGivenLocations:
                            if spoiler.settings.fast_start_beginning_of_game or dk64_loc_id != Locations.IslesFirstMove:
                                spoiler.pregiven_items.append(dk64_loc.item)
                            else:
                                spoiler.first_move_item = dk64_loc.item
                    if dk64_location_id is not None and ap_location.item is not None:
                        ap_item = ap_location.item
                        # Any item that isn't for this player is placed as an AP item, regardless of whether or not it could be a DK64 item
                        if ap_item.player != self.player:
                            spoiler.LocationList[dk64_location_id].PlaceItem(spoiler, DK64RItems.ArchipelagoItem)
                        # Collectibles don't get placed in the LocationList
                        elif "Collectible" in ap_item.name:
                            continue
                        else:
                            dk64_item = DK64RItems[ap_item.name]
                            if dk64_item is not None:
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
                # TODO: look up if the AP item on Jetpac is a major item
                patch_data, _ = patching_response(spoiler)
                spoiler.FlushAllExcessSpoilerData()
                patch_file = self.update_seed_results(patch_data, spoiler, self.player)
                print("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}-dk64.lanky")
                with open("output/" + f"{self.multiworld.get_out_file_name_base(self.player)}-dk64.lanky", "w") as f:
                    f.write(patch_file)
            except:
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
                zip_file.writestr("seed_number", "ap-patch-player-" + str(player_id))
                zip_file.writestr("seed_id", "ap-seed-player-" + str(player_id))
            zip_data.seek(0)
            # Convert the zip to a string of base64 data
            zip_conv = codecs.encode(zip_data.getvalue(), "base64").decode()

            return zip_conv

        def modify_multidata(self, multidata: dict):
            pass

        def fill_slot_data(self) -> dict:
            return {
                "Goal": self.options.goal.value,
                "ClimbingShuffle": self.options.climbing_shuffle.value,
                "PlayerNum": self.player,
            }

        def create_item(self, name: str, force_non_progression=False) -> Item:
            data = full_item_table[name]

            if force_non_progression:
                classification = ItemClassification.filler
            elif data.progression:
                classification = ItemClassification.progression
            else:
                classification = ItemClassification.filler

            created_item = DK64Item(name, classification, data.code, self.player)

            return created_item
