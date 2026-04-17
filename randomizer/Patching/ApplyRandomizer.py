"""Apply Patch data to the ROM."""

import json
import os
from datetime import datetime as Datetime
from datetime import timezone
import time
from tempfile import mktemp
from randomizer.Enums.Settings import (
    BananaportRando,
    ColorblindMode,
    DamageAmount,
    FasterChecksSelected,
    FungiTimeSetting,
    GalleonWaterSetting,
    HardModeSelected,
    HardBossesSelected,
    MiscChangesSelected,
    ProgressiveHintItem,
    PuzzleRando,
    RemovedBarriersSelected,
    RandomStartingRegion,
    ShockwaveStatus,
    ShuffleLoadingZones,
    SlamRequirement,
    WinConditionComplex,
    WrinklyHints,
)
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
import randomizer.ItemPool as ItemPool
from randomizer.Enums.Items import Items
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Maps import Maps
from randomizer.Enums.ScriptTypes import ScriptTypes
from randomizer.Lists.HardMode import HardSelector
from randomizer.Lists.Multiselectors import QoLSelector, RemovedBarrierSelector, FasterCheckSelector
from randomizer.Patching.BananaPlacer import randomize_cbs
from randomizer.Patching.BananaPortRando import randomize_bananaport, move_bananaports
from randomizer.Patching.BarrelRando import randomize_barrels
from randomizer.Patching.CoinPlacer import randomize_coins, place_mayhem_coins
from randomizer.Patching.Cosmetics.TextRando import writeBootMessages
from randomizer.Patching.Cosmetics.Puzzles import updateMillLeverTexture, updateCryptLeverTexture, updateDiddyDoors, updateHelmFaces, updateSnidePanel
from randomizer.Patching.Cosmetics.Colorblind import addBalloonBulb
from randomizer.Patching.CosmeticColors import (
    applyHelmDoorCosmetics,
    applyKongModelSwaps,
    showWinCondition,
)
from randomizer.Patching.CratePlacer import randomize_melon_crate
from randomizer.Patching.CrownPlacer import randomize_crown_pads
from randomizer.Patching.DoorPlacer import place_door_locations, remove_existing_indicators, alterStoryCutsceneWarps, placeVanillaTNSScripts
from randomizer.Patching.EnemyRando import randomize_enemies
from randomizer.Patching.EntranceRando import (
    enableTriggerText,
    filterEntranceType,
    randomize_entrances,
    placeLevelOrder,
)
from randomizer.Patching.FairyPlacer import PlaceFairies
from randomizer.Patching.ItemRando import place_randomized_items, alterTextboxRequirements, calculateInitFileScreen, place_spoiler_hint_data
from randomizer.Patching.KasplatLocationRando import randomize_kasplat_locations
from randomizer.Patching.KongRando import apply_kongrando_cosmetic
from randomizer.Patching.Library.Scripts import addNewScript, replaceScriptLines, setProgSlamStrength
from randomizer.Patching.Library.Generic import setItemReferenceName, IsItemSelected, getProgHintBarrierItem, getHintRequirementBatch, IsDDMSSelected
from randomizer.Patching.Library.Assets import CompTextFiles, ItemPreview
from randomizer.Patching.MiscSetupChanges import (
    randomize_setup,
    updateKrushaMoveNames,
    updateRandomSwitches,
    updateSwitchsanity,
    remove5DSCameraPoint,
)
from randomizer.Patching.MoveLocationRando import place_pregiven_moves, randomize_moves
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.PhaseRando import randomize_helm, randomize_krool
from randomizer.Patching.PriceRando import randomize_prices
from randomizer.Patching.PuzzleRando import randomize_puzzles, shortenCastleMinecart
from randomizer.Patching.ShopRandomizer import ApplyShopRandomizer
from randomizer.Patching.UpdateHints import (
    PushHints,
    replaceIngameText,
    PushItemLocations,
    PushHelpfulHints,
    PushHintTiedRegions,
)
from randomizer.Patching.ASMPatcher import patchAssembly, precalcBoot
from randomizer.Patching.ScriptPatcher import patchScripts
from randomizer.Patching.MirrorMode import ApplyMirrorMode
from randomizer.CompileHints import getHelmOrderHint

# from randomizer.Spoiler import Spoiler


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def writeMultiselector(
    enabled_selections: list,
    selector: list[dict],
    selection_enum,
    data_length: int,
    ROM_COPY: LocalROM,
    write_start: int,
):
    """Write multiselector choices to ROM."""
    write_data = [0] * data_length
    for item in selector:
        if item["shift"] >= 0:
            if selection_enum[item["value"]] in enabled_selections:
                offset = int(item["shift"] >> 3)
                check = int(item["shift"] % 8)
                write_data[offset] |= 0x80 >> check
    ROM_COPY.seek(write_start)
    for byte_data in write_data:
        ROM_COPY.writeMultipleBytes(byte_data, 1)


def encPass(spoiler) -> int:
    """Encrypt the password."""
    # Try to import randomizer.Encryption encrypt function, if we can pass all args to it.
    try:
        from randomizer.Encryption import encrypt

        return encrypt(spoiler)
    except Exception as e:
        print(e)
        return 0, 0


def _create_patching_adapter(fill_result, settings):
    """Create an adapter object that converts FillResult proto to spoiler-like interface.
    
    This adapter allows existing patching code to work with the proto without
    requiring immediate refactoring of all patching functions.
    
    Args:
        fill_result: FillResult protobuf message
        settings: Settings object
        
    Returns:
        Adapter object with spoiler-like interface
    """
    from randomizer.Enums.Regions import Regions
    from randomizer.LogicClasses import TransitionFront
    
    class PatchingAdapter:
        """Adapter that provides spoiler-like interface for FillResult proto."""
        
        def __init__(self, fill_result, settings):
            self.settings = settings
            self.fill_result = fill_result
            self.json = "{}"  # Will be populated in patching_response
            self.text_changes = {}
            self.enemy_rando_data = {}  # Will be populated by EnemyRando if needed
            self.microhints = {}  # Will be populated by compileMicrohints during patching
            self.pregiven_items = []  # Items given at start (populated during Fill)
            self.arcade_item_reward = None  # Set in patching_response
            self.jetpac_item_reward = None  # Set in patching_response
            
            # Initialize location_references - static mapping of items to reference names
            from randomizer.Fill import ItemReference
            self.location_references = [
                # DK Moves
                ItemReference(Items.BaboonBlast, "Baboon Blast", "DK Japes Cranky"),
                ItemReference(Items.StrongKong, "Strong Kong", "DK Aztec Cranky"),
                ItemReference(Items.GorillaGrab, "Gorilla Grab", "DK Factory Cranky"),
                ItemReference(Items.Coconut, "Coconut Gun", "DK Japes Funky"),
                ItemReference(Items.Bongos, "Bongo Blast", "DK Aztec Candy"),
                # Diddy Moves
                ItemReference(Items.ChimpyCharge, "Chimpy Charge", "Diddy Japes Cranky"),
                ItemReference(Items.RocketbarrelBoost, "Rocketbarrel Boost", "Diddy Aztec Cranky"),
                ItemReference(Items.SimianSpring, "Simian Spring", "Diddy Factory Cranky"),
                ItemReference(Items.Peanut, "Peanut Popguns", "Diddy Japes Funky"),
                ItemReference(Items.Guitar, "Guitar Gazump", "Diddy Aztec Candy"),
                # Lanky Moves
                ItemReference(Items.Orangstand, "Orangstand", "Lanky Japes Cranky"),
                ItemReference(Items.BaboonBalloon, "Baboon Balloon", "Lanky Factory Cranky"),
                ItemReference(Items.OrangstandSprint, "Orangstand Sprint", "Lanky Caves Cranky"),
                ItemReference(Items.Grape, "Grape Shooter", "Lanky Japes Funky"),
                ItemReference(Items.Trombone, "Trombone Tremor", "Lanky Aztec Candy"),
                # Tiny Moves
                ItemReference(Items.MiniMonkey, "Mini Monkey", "Tiny Japes Cranky"),
                ItemReference(Items.PonyTailTwirl, "Pony Tail Twirl", "Tiny Factory Cranky"),
                ItemReference(Items.Monkeyport, "Monkeyport", "Tiny Caves Cranky"),
                ItemReference(Items.Feather, "Feather Bow", "Tiny Japes Funky"),
                ItemReference(Items.Saxophone, "Saxophone Slam", "Tiny Aztec Candy"),
                # Chunky Moves
                ItemReference(Items.HunkyChunky, "Hunky Chunky", "Chunky Japes Cranky"),
                ItemReference(Items.PrimatePunch, "Primate Punch", "Chunky Factory Cranky"),
                ItemReference(Items.GorillaGone, "Gorilla Gone", "Chunky Caves Cranky"),
                ItemReference(Items.Pineapple, "Pineapple Launcher", "Chunky Japes Funky"),
                ItemReference(Items.Triangle, "Triangle Trample", "Chunky Aztec Candy"),
                # Gun Upgrades
                ItemReference(Items.HomingAmmo, "Homing Ammo", "Shared Forest Funky"),
                ItemReference(Items.SniperSight, "Sniper Scope", "Shared Castle Funky"),
                ItemReference(Items.ProgressiveAmmoBelt, "Progressive Ammo Belt", ["Shared Factory Funky", "Shared Caves Funky"]),
                ItemReference(Items.Camera, "Fairy Camera", "Banana Fairy Gift"),
                ItemReference(Items.Shockwave, "Shockwave", "Banana Fairy Gift"),
                # Basic Moves
                ItemReference(Items.Swim, "Diving", "Dive Barrel"),
                ItemReference(Items.Oranges, "Orange Throwing", "Orange Barrel"),
                ItemReference(Items.Barrels, "Barrel Throwing", "Barrel Barrel"),
                ItemReference(Items.Vines, "Vine Swinging", "Vine Barrel"),
                ItemReference(Items.Climbing, "Climbing", "Starting Move"),
                ItemReference(Items.Cannons, "Cannons", "Starting Move"),
                # Instrument Upgrades & Slams
                ItemReference(
                    Items.ProgressiveInstrumentUpgrade,
                    "Progressive Instrument Upgrade",
                    ["Shared Galleon Candy", "Shared Caves Candy", "Shared Castle Candy"],
                ),
                ItemReference(
                    Items.ProgressiveSlam,
                    "Progressive Slam",
                    ["Shared Isles Cranky", "Shared Forest Cranky", "Shared Castle Cranky"],
                ),
                # Kongs
                ItemReference(Items.Donkey, "Donkey Kong", "Starting Kong"),
                ItemReference(Items.Diddy, "Diddy Kong", "Japes Diddy Cage"),
                ItemReference(Items.Lanky, "Lanky Kong", "Llama Lanky Cage"),
                ItemReference(Items.Tiny, "Tiny Kong", "Aztec Tiny Cage"),
                ItemReference(Items.Chunky, "Chunky Kong", "Factory Chunky Cage"),
                # Shopkeepers
                ItemReference(Items.Cranky, "Cranky Kong", "Starting Item"),
                ItemReference(Items.Candy, "Candy Kong", "Starting Item"),
                ItemReference(Items.Funky, "Funky Kong", "Starting Item"),
                ItemReference(Items.Snide, "Snide", "Starting Item"),
                # Early Keys
                ItemReference(Items.JungleJapesKey, "Key 1", "Starting Key", True),
                ItemReference(Items.AngryAztecKey, "Key 2", "Starting Key", True),
                ItemReference(Items.FranticFactoryKey, "Key 3", "Starting Key", True),
                ItemReference(Items.GloomyGalleonKey, "Key 4", "Starting Key", True),
                # Late Keys
                ItemReference(Items.FungiForestKey, "Key 5", "Starting Key", True),
                ItemReference(Items.CrystalCavesKey, "Key 6", "Starting Key", True),
                ItemReference(Items.CreepyCastleKey, "Key 7", "Starting Key", True),
                ItemReference(Items.HideoutHelmKey, "Key 8", "Starting Key", True),
            ]
            
            # Convert shuffled exits from proto to TransitionFront objects
            self.shuffled_exit_data = {}
            for exit_id, exit_dest in fill_result.shuffle_data.shuffled_exits.items():
                # Create TransitionFront-like object
                class ExitDestination:
                    def __init__(self, dest, reverse, exit_name, spoiler_name):
                        self.dest = dest if isinstance(dest, Regions) else Regions(dest)
                        self.reverse = reverse
                        self.exit = exit_name
                        self.spoilerName = spoiler_name
                
                self.shuffled_exit_data[exit_id] = ExitDestination(
                    exit_dest.destination_region,
                    exit_dest.reverse_transition,
                    exit_dest.exit_name,
                    exit_dest.spoiler_name
                )
            
            # Store proto references for functions that need them
            self._location_assignments = fill_result.location_assignments
            self._move_shop_data = fill_result.move_shop_data
            self._shuffle_data = fill_result.shuffle_data
            self._placement_data = fill_result.placement_data
            self._hint_data = fill_result.hint_data
            self._path_data = fill_result.path_data
            self._misc_data = fill_result.misc_data
            
        # Properties to access proto data with backward-compatible interface
        @property
        def LocationList(self):
            """Simulate LocationList for item rando."""
            from randomizer.Lists.Location import LocationListOriginal
            from randomizer.Enums.Locations import Locations
            
            # Create a dict-like object that provides location->item mapping
            class LocationDict:
                def __init__(self, assignments):
                    self._assignments = assignments
                    self._cache = {}  # Cache LocationObj instances to persist attribute changes
                
                def _get_or_create_location(self, location_id):
                    """Get or create a LocationObj for the given location_id."""
                    if location_id not in self._cache:
                        class LocationObj:
                            def __init__(self, item_id, location_id):
                                self.item = item_id if item_id != 0 else None
                                self.location = location_id  # Store location ID for key lookups
                                # Get location properties from LocationListOriginal if available
                                try:
                                    loc_enum = Locations(location_id)
                                    if loc_enum in LocationListOriginal:
                                        orig_loc = LocationListOriginal[loc_enum]
                                        self.name = orig_loc.name
                                        self.type = orig_loc.type
                                        self.kong = orig_loc.kong
                                        self.level = orig_loc.level
                                        self.default = orig_loc.default
                                        self.inaccessible = orig_loc.inaccessible
                                        self.smallerShopsInaccessible = orig_loc.smallerShopsInaccessible
                                        self.tooExpensiveInaccessible = orig_loc.tooExpensiveInaccessible
                                    else:
                                        self.name = f"Location_{location_id}"
                                        self.type = None
                                        self.kong = None
                                        self.level = None
                                        self.default = None
                                        self.inaccessible = False
                                        self.smallerShopsInaccessible = False
                                        self.tooExpensiveInaccessible = False
                                except:
                                    self.name = f"Location_{location_id}"
                                    self.type = None
                                    self.kong = None
                                    self.level = None
                                    self.default = None
                                    self.inaccessible = False
                                    self.smallerShopsInaccessible = False
                                    self.tooExpensiveInaccessible = False
                        
                        item_id = self._assignments.assignments.get(int(location_id), 0)
                        self._cache[location_id] = LocationObj(item_id, location_id)
                    
                    return self._cache[location_id]
                
                def items(self):
                    """Return (location_id, location_obj) pairs."""
                    for loc_id in self._assignments.assignments.keys():
                        yield (loc_id, self._get_or_create_location(loc_id))
                
                def __iter__(self):
                    """Iterate over location IDs."""
                    return iter(self._assignments.assignments.keys())
                
                def __len__(self):
                    """Return number of locations."""
                    return len(self._assignments.assignments)
                
                def __getitem__(self, key):
                    # Handle multiple key types: int, Locations enum, LocationObj, etc.
                    if isinstance(key, int):
                        key_int = key
                    elif hasattr(key, 'location'):
                        # LocationObj from our own adapter - has .location attribute with the ID
                        key_int = int(key.location)
                    elif hasattr(key, 'value'):
                        # Enum type (Locations has .value attribute)
                        key_int = int(key.value)
                    else:
                        # Try direct conversion
                        key_int = int(key)
                    return self._get_or_create_location(key_int)
                
                def __contains__(self, key):
                    """Check if location exists in assignments."""
                    if isinstance(key, int):
                        key_int = key
                    elif hasattr(key, 'location'):
                        # LocationObj from our own adapter
                        key_int = int(key.location)
                    elif hasattr(key, 'value'):
                        key_int = int(key.value)
                    else:
                        key_int = int(key)
                    return key_int in self._assignments.assignments
            
            return LocationDict(self._location_assignments)
        
        @property
        def move_data(self):
            """Return move shop data from proto."""
            # Convert proto MoveShopData back to the 3-element list structure
            result = []
            
            # Index 0: Shop moves - structure is [shop_tier][kong][level]
            # Proto structure: shop_types[0].shop_indices[N] where N is shop_tier
            shop_moves = []
            if len(self._move_shop_data.shop_types) > 0:
                shop_type = self._move_shop_data.shop_types[0]  # There's only one shop type
                for shop_index in shop_type.shop_indices:  # 3 tiers
                    kong_moves_list = []
                    for kong_moves in shop_index.kong_moves:  # 5 kongs
                        level_moves = []
                        for move_entry in kong_moves.moves:  # 8 levels
                            level_moves.append(_move_entry_proto_to_dict(move_entry))
                        # Ensure we always have exactly 8 levels (pad with empty moves if needed)
                        while len(level_moves) < 8:
                            level_moves.append({'move_type': None})
                        kong_moves_list.append(level_moves)
                    shop_moves.append(kong_moves_list)
            result.append(shop_moves)
            
            # Index 1: Training barrels
            training = []
            for move_entry in self._move_shop_data.training_barrels:
                training.append(_move_entry_proto_to_dict(move_entry))
            result.append(training)
            
            # Index 2: BFI moves
            bfi = []
            for move_entry in self._move_shop_data.bfi_moves:
                bfi.append(_move_entry_proto_to_dict(move_entry))
            result.append(bfi)
            
            return result
        
        @property
        def shuffled_barrel_data(self):
            """Return barrel shuffle data - reconstruct MinigameLocationData objects."""
            from randomizer.Lists.Minigame import BarrelMetaData, MinigameLocationData
            from randomizer.Enums.Minigames import Minigames
            
            result = {}
            for location_id, minigame_type in self._shuffle_data.shuffled_barrels.items():
                # Get the original barrel metadata for this location
                if location_id in BarrelMetaData:
                    original = BarrelMetaData[location_id]
                    # Create new MinigameLocationData with shuffled minigame but original location data
                    result[location_id] = MinigameLocationData(
                        original.map,
                        original.barrel_id,
                        Minigames(minigame_type),
                        original.kong
                    )
                else:
                    # Fallback - shouldn't happen but be defensive
                    result[location_id] = minigame_type
            return result
        
        @property
        def shuffled_door_data(self):
            """Return door shuffle data."""
            from randomizer.Enums.Levels import Levels
            from collections import defaultdict
            # Convert proto door shuffles back to dict with empty lists as default
            result = defaultdict(list)
            for door_shuffle in self._shuffle_data.shuffled_doors:
                result[Levels(door_shuffle.level)] = list(door_shuffle.doors)
            return result
        
        @property
        def shuffled_exit_instructions(self):
            """Return exit instructions."""
            return list(self._shuffle_data.exit_instructions)
        
        @property
        def cb_placements(self):
            """Return CB placements."""
            result = []
            for cb_proto in self._placement_data.cb_placements:
                cb_dict = {
                    'id': cb_proto.id,
                    'name': cb_proto.name,
                    'kong': cb_proto.kong,
                    'level': cb_proto.level,
                    'type': cb_proto.type,
                    'map': cb_proto.map,
                }
                if cb_proto.locations:
                    cb_dict['locations'] = [
                        [loc.amount, loc.scale, loc.x, loc.y, loc.z]
                        for loc in cb_proto.locations
                    ]
                result.append(cb_dict)
            return result
        
        @property
        def balloon_placement(self):
            """Return balloon placements."""
            result = []
            for balloon_proto in self._placement_data.balloon_placements:
                result.append({
                    'id': balloon_proto.id,
                    'name': balloon_proto.name,
                    'kong': balloon_proto.kong,
                    'level': balloon_proto.level,
                    'map': balloon_proto.map,
                    'score': balloon_proto.score,
                })
            return result
        
        @property
        def enemy_replacements(self):
            """Return enemy replacements."""
            result = []
            for enemy_proto in self._placement_data.enemy_replacements:
                swaps = []
                for swap_proto in enemy_proto.kasplat_swaps:
                    swaps.append({
                        'vanilla_location': swap_proto.vanilla_location,
                        'replace_with': swap_proto.replace_with,
                    })
                result.append({
                    'container_map': enemy_proto.container_map,
                    'kasplat_swaps': swaps,
                })
            return result
        
        @property
        def coin_requirements(self):
            """Return coin requirements."""
            return dict(self._placement_data.coin_requirements)
        
        @property
        def item_assignment(self):
            """Return item assignments."""
            from randomizer.Enums.Types import Types
            from randomizer.Enums.Items import Items
            from randomizer.Enums.Kongs import Kongs as KongEnum
            
            result = []
            for assign_proto in self._misc_data.item_assignments:
                class ItemAssignment:
                    pass
                
                assign_obj = ItemAssignment()
                
                # Proto fields
                assign_obj.old_type = Types(assign_proto.old_type) if assign_proto.old_type > 0 else None
                assign_obj.old_flag = assign_proto.old_flag
                assign_obj.maps_to_actor_ids = dict(assign_proto.maps_to_actor_ids)
                assign_obj.placement_data = dict(assign_proto.maps_to_actor_ids)  # placement_data is same as maps_to_actor_ids
                assign_obj.location = assign_proto.location
                assign_obj.new_flag = assign_proto.new_flag
                assign_obj.new_type = Types(assign_proto.new_type) if assign_proto.new_type > 0 else None
                assign_obj.new_item = Items(assign_proto.new_item) if assign_proto.new_item > 0 else None
                assign_obj.new_kong = KongEnum(assign_proto.new_kong) if assign_proto.new_kong >= 0 else KongEnum.any
                assign_obj.shared = assign_proto.shared
                assign_obj.placement_index = [assign_proto.placement_index] if assign_proto.placement_index > 0 else []
                assign_obj.placement_subindex = assign_proto.placement_subindex
                
                # Additional attributes expected by patching code (from LocationSelection class)
                assign_obj.name = ""
                assign_obj.old_item = None  # vanilla_item - not stored in proto
                assign_obj.old_kong = KongEnum.any  # Default kong
                assign_obj.reward_spot = False  # is_reward_point
                assign_obj.is_shop = (assign_proto.placement_index > 0 and assign_proto.placement_index < 120)
                assign_obj.price = 0  # Default price
                assign_obj.can_have_item = True
                assign_obj.can_place_item = True
                assign_obj.shop_locked = False
                assign_obj.order = 0
                assign_obj.move_name = ""
                
                result.append(assign_obj)
            return result
        
        @property
        def music_bgm_data(self):
            """Return BGM music data."""
            return dict(self._misc_data.music_bgm_data)
        
        @property
        def music_majoritem_data(self):
            """Return major item music data."""
            return dict(self._misc_data.music_majoritem_data)
        
        @property
        def music_minoritem_data(self):
            """Return minor item music data."""
            return dict(self._misc_data.music_minoritem_data)
        
        @property
        def music_event_data(self):
            """Return event music data."""
            return dict(self._misc_data.music_event_data)
        
        @property
        def hintset(self):
            """Return hint set."""
            class HintSet:
                def __init__(self, proto):
                    self.max_hints = proto.max_hints
                    self.hints = []
                    for hint_proto in proto.hints:
                        class Hint:
                            pass
                        h = Hint()
                        h.location = hint_proto.location_id
                        h.hint = hint_proto.hint_text
                        h.short_hint = None  # Short hints are not in proto
                        h.important = hint_proto.important
                        h.priority = hint_proto.priority
                        self.hints.append(h)
                
                def RemoveFTT(self):
                    """Remove the First Time Talk hint (called after writing to ROM)."""
                    # FTT is the first hint, remove it from the list
                    if self.hints:
                        self.hints = self.hints[1:]
            
            return HintSet(self._hint_data.hint_set)
        
        @property
        def tied_hint_flags(self):
            """Return tied hint flags."""
            return dict(self._hint_data.tied_hint_flags)
        
        @property
        def tied_hint_regions(self):
            """Return tied hint regions."""
            return list(self._hint_data.tied_hint_regions)
        
        @property
        def RegionList(self):
            """Return region list - this is logic data not part of Fill output."""
            from randomizer.Logic import RegionsOriginal
            return RegionsOriginal
        
        @property
        def majorItems(self):
            """Return major items list."""
            from randomizer.Enums.Items import Items
            return [Items(item_id) for item_id in self._path_data.major_items]
        
        @property
        def woth_locations(self):
            """Return Way of the Hoard locations."""
            from randomizer.Enums.Locations import Locations
            return [Locations(loc_id) for loc_id in self._path_data.woth_locations]
        
        @property
        def woth_paths(self):
            """Return Way of the Hoard paths."""
            from randomizer.Enums.Locations import Locations
            result = {}
            for loc_id, path_proto in self._path_data.woth_paths.items():
                result[Locations(loc_id)] = [Locations(l) for l in path_proto.locations]
            return result
        
        @property
        def foolish_region_names(self):
            """Return foolish region names."""
            return list(self._path_data.foolish_region_names)
        
        @property
        def pathless_moves(self):
            """Return pathless moves."""
            from randomizer.Enums.Items import Items
            return [Items(item_id) for item_id in self._path_data.pathless_moves]
        
        @property
        def playthrough(self):
            """Return playthrough spheres."""
            from randomizer.Enums.Locations import Locations
            from randomizer.Enums.Items import Items
            result = {}
            for i, sphere_proto in enumerate(self._path_data.playthrough):
                sphere_dict = {}
                for loc_proto in sphere_proto.locations:
                    sphere_dict[Locations(loc_proto.location_id)] = Items(loc_proto.item_id)
                result[i] = sphere_dict
            return result
        
        @property
        def region_hintable_count(self):
            """Return region hintable count."""
            result = {}
            for region_name, counts_proto in self._path_data.region_hintable_count.items():
                region_dict = {}
                for item_type, item_data in counts_proto.items.items():
                    from randomizer.Enums.Locations import Locations
                    region_dict[int(item_type)] = {
                        'count': item_data.count,
                        'locations': [Locations(loc_id) for loc_id in item_data.location_ids]
                    }
                result[region_name] = region_dict
            return result
    
    return PatchingAdapter(fill_result, settings)


def _move_entry_proto_to_dict(move_entry_proto):
    """Convert a MoveEntry proto to a dictionary."""
    from randomizer.proto_gen import fill_result_pb2
    
    which = move_entry_proto.WhichOneof('entry')
    
    if which == 'empty_move':
        return {'move_type': None}
    elif which == 'flag_move':
        return {
            'move_type': 'flag',
            'flag': move_entry_proto.flag_move.flag,
            'price': move_entry_proto.flag_move.price,
        }
    elif which == 'special_move':
        return {
            'move_type': 'special',
            'move_lvl': move_entry_proto.special_move.move_lvl,
            'move_kong': move_entry_proto.special_move.move_kong,
            'price': move_entry_proto.special_move.price,
        }
    elif which == 'slam_move':
        return {
            'move_type': 'slam',
            'move_lvl': move_entry_proto.slam_move.move_lvl,
            'move_kong': move_entry_proto.slam_move.move_kong,
            'price': move_entry_proto.slam_move.price,
        }
    elif which == 'gun_move':
        return {
            'move_type': 'gun',
            'move_lvl': move_entry_proto.gun_move.move_lvl,
            'move_kong': move_entry_proto.gun_move.move_kong,
            'price': move_entry_proto.gun_move.price,
        }
    elif which == 'ammo_belt_move':
        return {
            'move_type': 'ammo_belt',
            'move_lvl': move_entry_proto.ammo_belt_move.move_lvl,
            'move_kong': move_entry_proto.ammo_belt_move.move_kong,
            'price': move_entry_proto.ammo_belt_move.price,
        }
    elif which == 'instrument_move':
        return {
            'move_type': 'instrument',
            'move_lvl': move_entry_proto.instrument_move.move_lvl,
            'move_kong': move_entry_proto.instrument_move.move_kong,
            'price': move_entry_proto.instrument_move.price,
        }
    else:
        return {'move_type': None}


def patching_response(fill_result_or_spoiler, settings=None, rom=None):
    """Apply the patch data to the ROM in the local server to be returned to the client.
    
    Args:
        fill_result_or_spoiler: Either a FillResult proto (new path) or Spoiler object (legacy path)
        settings: Settings object (required when fill_result_or_spoiler is a FillResult proto)
        rom: Optional ROM object to patch (browser case). If None, loads from file (server case).
    """
    # Handle both old (Spoiler) and new (FillResult proto + Settings) APIs
    from randomizer.proto_gen import fill_result_pb2
    
    if isinstance(fill_result_or_spoiler, fill_result_pb2.FillResult):
        # New proto-based path - convert proto to adapter object
        print("[Patching] ✓ Received FillResult protobuf")
        fill_result = fill_result_or_spoiler
        if settings is None:
            raise ValueError("settings parameter required when using FillResult proto")
        
        print("[Patching] Creating adapter to convert proto to patching interface...")
        spoiler = _create_patching_adapter(fill_result, settings)
        
        # Initialize valid_locations on settings - required for patching functions
        print("[Patching] Initializing valid_locations for settings...")
        settings.update_valid_locations(spoiler)
        
        print("[Patching] ✓ Proto adapter created, proceeding with ROM patching")
    else:
        # Legacy path - treat as Spoiler object
        print("[Patching] Using legacy Spoiler object (not proto)")
        spoiler = fill_result_or_spoiler
    
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()

    # Write date to ROM for debugging purposes
    try:
        temp_json = json.loads(spoiler.json)
        if "Settings" not in temp_json:
            temp_json["Settings"] = {}
    except Exception:
        temp_json = {"Settings": {}}
    dt = Datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    temp_json["Settings"]["Generation Timestamp"] = dt
    spoiler.json = json.dumps(temp_json, indent=4)
    
    # Use provided ROM if available (browser case), otherwise load from file (server case)
    if rom is not None:
        ROM_COPY = rom
    else:
        ROM_COPY = LocalROM()
    
    ROM_COPY.seek(0x1FFF200)
    ROM_COPY.writeBytes(dt.encode("ascii"))
    # Initialize Text Changes
    spoiler.text_changes = {}

    # Starting index for our settings
    sav = spoiler.settings.rom_data
    placeVanillaTNSScripts(ROM_COPY)

    # Shuffle Levels
    if spoiler.settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
        # Update Level Order
        vanilla_lobby_entrance_order = [
            Transitions.IslesMainToJapesLobby,
            Transitions.IslesMainToAztecLobby,
            Transitions.IslesMainToFactoryLobby,
            Transitions.IslesMainToGalleonLobby,
            Transitions.IslesMainToForestLobby,
            Transitions.IslesMainToCavesLobby,
            Transitions.IslesMainToCastleLobby,
            Transitions.IslesMainToHelmLobby,
        ]
        vanilla_lobby_exit_order = [
            Transitions.IslesJapesLobbyToMain,
            Transitions.IslesAztecLobbyToMain,
            Transitions.IslesFactoryLobbyToMain,
            Transitions.IslesGalleonLobbyToMain,
            Transitions.IslesForestLobbyToMain,
            Transitions.IslesCavesLobbyToMain,
            Transitions.IslesCastleLobbyToMain,
            Transitions.IslesHelmLobbyToMain,
        ]
        level_order = []
        for level in vanilla_lobby_entrance_order:
            level_order.append(vanilla_lobby_exit_order.index(spoiler.shuffled_exit_data[int(level)].reverse))
        placeLevelOrder(spoiler, level_order, ROM_COPY)

    ROM_COPY.seek(sav + 0x151)
    ROM_COPY.writeMultipleBytes(spoiler.settings.starting_kong, 1)

    boolean_props = [
        BooleanProperties(spoiler.settings.fast_start_beginning_of_game, 0x2E),  # Fast Start Game
        BooleanProperties(spoiler.settings.enable_tag_anywhere, 0x30),  # Tag Anywhere
        BooleanProperties(spoiler.settings.no_melons, 0x128),  # No Melon Drops
        BooleanProperties(spoiler.settings.bonus_barrel_auto_complete, 0x126),  # Auto-Complete Bonus Barrels
        BooleanProperties(spoiler.settings.warp_to_isles, 0x135),  # Warp to Isles
        BooleanProperties(spoiler.settings.ice_traps_damage, 0x150),  # Enable Ice Trap Damage
        BooleanProperties(spoiler.settings.shorten_boss, 0x13B),  # Shorten Boss Fights
        BooleanProperties(spoiler.settings.fast_warps, 0x13A),  # Fast Warps
        BooleanProperties(spoiler.settings.auto_keys, 0x15B),  # Auto-Turn Keys
        BooleanProperties(IsItemSelected(spoiler.settings.cb_rando_enabled, spoiler.settings.cb_rando_list_selected, Levels.DKIsles), 0x10B),  # 5 extra medal handling
        BooleanProperties(spoiler.settings.helm_hurry, 0xAE),  # Helm Hurry
        BooleanProperties(spoiler.settings.wrinkly_available, 0x52),  # Remove Wrinkly Kong Checks
        BooleanProperties(
            spoiler.settings.bananaport_rando in (BananaportRando.crossmap_coupled, BananaportRando.crossmap_decoupled),
            0x47,
        ),  # Parent Map Filter
        BooleanProperties(spoiler.settings.shop_indicator, 0x134, 2),  # Shop Indicator
        BooleanProperties(spoiler.settings.open_lobbies, 0x14C, 0xFF),  # Open Lobbies
        BooleanProperties(spoiler.settings.item_reward_previews, 0x101, 255),  # Bonus Matches Contents
        BooleanProperties(spoiler.settings.fix_lanky_tiny_prod, 0x114),  # Fix Lanky Tiny Prod
        BooleanProperties(spoiler.settings.enemy_kill_crown_timer, 0x35),  # Enemy crown timer reduction
        BooleanProperties(spoiler.settings.race_coin_rando, 0x94),  # Race Coin Location Rando
        BooleanProperties(spoiler.settings.disable_racing_patches, 0x91),  # Disable Racing Patches
        BooleanProperties(spoiler.settings.shops_dont_cost, 0x95),  # Shops don't cost
        BooleanProperties(spoiler.settings.snide_reward_rando, 0x69),  # Snides has rewards
    ]

    for prop in boolean_props:
        if prop.check:
            ROM_COPY.seek(sav + prop.offset)
            ROM_COPY.write(prop.target)

    # Fast Hideout
    ROM_COPY.seek(sav + 0x031)
    # The HelmSetting enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.helm_setting))

    # Crown Door & Coin Door
    # Crown Door
    ROM_COPY.seek(sav + 0x4C)
    ROM_COPY.write(int(spoiler.settings.crown_door_item))
    ROM_COPY.write(spoiler.settings.crown_door_item_count)
    # Coin Door
    ROM_COPY.seek(sav + 0x4E)
    ROM_COPY.write(int(spoiler.settings.coin_door_item))
    ROM_COPY.write(spoiler.settings.coin_door_item_count)

    kong_free_switches = [
        Switches.JapesFreeKong,
        Switches.AztecLlamaPuzzle,
        Switches.AztecOKONGPuzzle,
        Switches.FactoryFreeKong,
    ]
    if spoiler.settings.switchsanity_enabled:
        for slot in spoiler.settings.switchsanity_data:
            slot_data = spoiler.settings.switchsanity_data[slot]
            rom_offset = slot_data.rom_offset
            pad_kong = slot_data.kong
            pad_type = slot_data.switch_type
            if rom_offset is not None:
                # ROM Write
                ROM_COPY.seek(sav + rom_offset)
                if slot == Switches.IslesMonkeyport:
                    if pad_kong == Kongs.lanky:
                        ROM_COPY.writeMultipleBytes(2, 1)
                    elif pad_kong == Kongs.donkey:
                        ROM_COPY.writeMultipleBytes(1, 1)
                elif slot == Switches.IslesHelmLobbyGone:
                    if pad_type == SwitchType.MiscActivator:
                        if pad_kong == Kongs.donkey:
                            ROM_COPY.writeMultipleBytes(6, 1)
                        elif pad_kong == Kongs.diddy:
                            ROM_COPY.writeMultipleBytes(7, 1)
                    elif pad_type != SwitchType.PadMove:
                        ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)
                elif slot in kong_free_switches:
                    ROM_COPY.writeMultipleBytes(int(pad_kong), 1)
                else:
                    ROM_COPY.writeMultipleBytes(int(pad_kong) + 1, 1)
            else:
                # Only modify the instance script
                if pad_type == SwitchType.GunSwitch:
                    if pad_kong == Kongs.any:
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 24 | {KONG_PELLETS[slot_data.default_kong]} 1 0": "COND 16 | 4 1 0"})
                    else:
                        KONG_PELLETS = [48, 36, 42, 43, 38]
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 24 | {KONG_PELLETS[slot_data.default_kong]} 1 0": f"COND 24 | {KONG_PELLETS[pad_kong]} 1 0"})
                elif pad_type in (SwitchType.InstrumentPad, SwitchType.SlamSwitch):
                    if pad_kong == Kongs.any:
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 25 | {slot_data.default_kong + 2} 0 0": "COND 0 | 0 0 0"})
                    else:
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 25 | {slot_data.default_kong + 2} 0 0": f"COND 25 | {pad_kong + 2} 0 0"})
                elif pad_type in (SwitchType.PushableButton, SwitchType.PunchGrate, SwitchType.IceWall, SwitchType.Gong):
                    control_states = [
                        [0, 0],
                        [0x2E, 1],  # Chimpy Charge
                        [0, 0],
                        [0, 0],
                        [0x24, 2],  # Primate Punch
                    ]
                    if pad_type == SwitchType.Gong:
                        replaceScriptLines(
                            ROM_COPY,
                            slot_data.map_id,
                            slot_data.ids,
                            {
                                f"COND 23 | {control_states[slot_data.default_kong][0]} {control_states[slot_data.default_kong][1]} 0": f"COND 23 | {control_states[pad_kong][0]} {control_states[pad_kong][1]} 0"
                            },
                        )
                    else:
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 23 | {control_states[slot_data.default_kong][0]} 0 0": f"COND 23 | {control_states[pad_kong][0]} 0 0"})
                        replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 33 | {control_states[slot_data.default_kong][1]} 0 0": f"COND 33 | {control_states[pad_kong][1]} 0 0"})
                    replaceScriptLines(ROM_COPY, slot_data.map_id, slot_data.ids, {f"COND 24 | {slot_data.default_kong + 2} 1 0": f"COND 24 | {pad_kong + 2} 1 0"})
                elif pad_type == SwitchType.GunInstrumentCombo:
                    if pad_kong == Kongs.any:
                        replaceScriptLines(ROM_COPY, slot_data.map_id, [slot_data.ids[0]], {f"COND 24 | {KONG_PELLETS[slot_data.default_kong]} 1 0": "COND 16 | 4 1 0"})
                        replaceScriptLines(ROM_COPY, slot_data.map_id, [slot_data.ids[1]], {f"COND 25 | {slot_data.default_kong + 2} 0 0": "COND 0 | 0 0 0"})
                    else:
                        KONG_PELLETS = [48, 36, 42, 43, 38]
                        replaceScriptLines(ROM_COPY, slot_data.map_id, [slot_data.ids[0]], {f"COND 24 | {KONG_PELLETS[slot_data.default_kong]} 1 0": f"COND 24 | {KONG_PELLETS[pad_kong]} 1 0"})
                        replaceScriptLines(ROM_COPY, slot_data.map_id, [slot_data.ids[1]], {f"COND 25 | {slot_data.default_kong + 2} 0 0": f"COND 25 | {pad_kong + 2} 0 0"})

    slam_req_values = {
        SlamRequirement.green: 1,
        SlamRequirement.blue: 2,
        SlamRequirement.red: 3,
    }
    req_val = slam_req_values[spoiler.settings.chunky_phase_slam_req_internal]
    replaceScriptLines(ROM_COPY, Maps.KroolChunkyPhase, [0xA], {"COND 37 | 2 0 0": f"COND 37 | {req_val} 0 0"})
    ROM_COPY.seek(sav + 0x1E3)
    ROM_COPY.write(req_val)

    if spoiler.settings.enable_tag_anywhere:
        ta_blocks = {
            Maps.AngryAztec: [0x24],
            Maps.CastleCrypt: [0xD, 0xE, 0xF],
            Maps.CastleDungeon: [0x4, 0x5, 0x6],
            Maps.CastleTree: [0x1, 0x9],
            Maps.FranticFactory: [0x15, 0x38, 0x37, 0x3B],
            Maps.AztecLlamaTemple: [0x6B],
            Maps.Isles: [0x32, 0x2A, 0x27, 0x29, 0x28],
        }
        for map_id, obj_ids in ta_blocks.items():
            for x in range(5):
                replaceScriptLines(ROM_COPY, map_id, obj_ids, {f"CONDINV 25 | {x + 2} 0 0": "COND 25 | 0 0 0"})

    # Camera unlocked
    given_moves = []
    if spoiler.settings.shockwave_status == ShockwaveStatus.start_with:
        given_moves.extend([39, 40])  # 39 = Camera, 40 = Shockwave
        setItemReferenceName(spoiler, Items.CameraAndShockwave, 0, "Extra Training", 0)

    writeMultiselector(
        spoiler.settings.misc_changes_selected,
        QoLSelector,
        MiscChangesSelected,
        4,
        ROM_COPY,
        sav + 0x0B0,
    )
    writeMultiselector(
        spoiler.settings.faster_checks_selected,
        FasterCheckSelector,
        FasterChecksSelected,
        2,
        ROM_COPY,
        sav + 0x1E0,
    )
    writeMultiselector(
        spoiler.settings.hard_mode_selected,
        HardSelector,
        HardModeSelected,
        1,
        ROM_COPY,
        sav + 0x0C6,
    )

    is_dw = IsDDMSSelected(spoiler.settings.hard_mode_selected, HardModeSelected.donk_in_the_dark_world)
    is_sky = IsDDMSSelected(spoiler.settings.hard_mode_selected, HardModeSelected.donk_in_the_sky)
    ROM_COPY.seek(sav + 0x0C6)
    old = int.from_bytes(ROM_COPY.readBytes(1), "big")
    new = old
    if is_dw and is_sky:
        # Memory Challenge
        new = old | (0x8 | 0x2)
    elif is_dw and not is_sky:
        # Dark world only
        new = old | 0x8
    elif is_sky and not is_dw:
        # Sky only
        new = old | 0x4
    if new != old:
        ROM_COPY.seek(sav + 0x0C6)
        ROM_COPY.write(new)

    # Damage amount
    damage_multipliers = {
        DamageAmount.default: 1,
        DamageAmount.double: 2,
        DamageAmount.quad: 4,
        DamageAmount.ohko: 12,
    }
    ROM_COPY.seek(sav + 0x097)
    ROM_COPY.write(damage_multipliers[spoiler.settings.damage_amount])

    ROM_COPY.seek(sav + 0x0C5)
    ROM_COPY.write(int(Types.Enemies in spoiler.settings.shuffled_location_types))

    ROM_COPY.seek(sav + 0x0C2)
    hints_in_pool_handler = 0
    if Types.Hint in spoiler.settings.shuffled_location_types:
        hints_in_pool_handler = 1
        if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
            hints_in_pool_handler = 2
    ROM_COPY.write(int(hints_in_pool_handler))

    # Progressive Hints
    count = 0
    if spoiler.settings.progressive_hint_item != ProgressiveHintItem.off:
        count = spoiler.settings.progressive_hint_count
        ROM_COPY.seek(sav + 0x0C3)
        ROM_COPY.write(getProgHintBarrierItem(spoiler.settings.progressive_hint_item))
        for x in range(10):
            ROM_COPY.seek(sav + 0x98 + (x * 2))
            ROM_COPY.writeMultipleBytes(getHintRequirementBatch(x, count), 2)
    ROM_COPY.seek(sav + 0x115)
    ROM_COPY.writeMultipleBytes(count, 1)

    # Microhints
    ROM_COPY.seek(sav + 0x102)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.microhints_enabled))

    # Cutscene Skip Setting
    ROM_COPY.seek(sav + 0x116)
    # The MicrohintsEnabled enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.more_cutscene_skips))

    # Helm Hurry
    helm_hurry_bonuses = [
        spoiler.settings.helmhurry_list_starting_time,
        spoiler.settings.helmhurry_list_golden_banana,
        spoiler.settings.helmhurry_list_blueprint,
        spoiler.settings.helmhurry_list_company_coins,
        spoiler.settings.helmhurry_list_move,
        spoiler.settings.helmhurry_list_banana_medal,
        spoiler.settings.helmhurry_list_rainbow_coin,
        spoiler.settings.helmhurry_list_boss_key,
        spoiler.settings.helmhurry_list_battle_crown,
        spoiler.settings.helmhurry_list_bean,
        spoiler.settings.helmhurry_list_pearl,
        spoiler.settings.helmhurry_list_kongs,
        spoiler.settings.helmhurry_list_fairies,
        spoiler.settings.helmhurry_list_colored_bananas,
        spoiler.settings.helmhurry_list_ice_traps,
    ]
    ROM_COPY.seek(sav + 0xE2)
    for bonus in helm_hurry_bonuses:
        if bonus < 0:
            bonus += 65536
        ROM_COPY.writeMultipleBytes(bonus, 2)

    # Activate Bananaports
    ROM_COPY.seek(sav + 0x138)
    # The ActivateAllBananaports enum is indexed to allow this.
    ROM_COPY.write(int(spoiler.settings.activate_all_bananaports))

    # Fast GBs - Change jetpac text
    if IsDDMSSelected(spoiler.settings.faster_checks_selected, FasterChecksSelected.jetpac):
        data = {"textbox_index": ItemPreview.JetpacIntro, "mode": "replace", "search": "5000", "target": "2500"}
        for file in [CompTextFiles.PreviewsFlavor, CompTextFiles.PreviewsNormal]:
            if file in spoiler.text_changes:
                spoiler.text_changes[file].append(data)
            else:
                spoiler.text_changes[file] = [data]

    # Win Condition
    win_con_table = {
        WinConditionComplex.beat_krool: {
            "index": 0,
        },
        WinConditionComplex.get_key8: {
            "index": 1,
        },
        WinConditionComplex.get_keys_3_and_8: {
            "index": 7,
        },
        WinConditionComplex.krem_kapture: {
            "index": 2,
        },
        WinConditionComplex.dk_rap_items: {
            "index": 4,
        },
        WinConditionComplex.krools_challenge: {
            "index": 5,
        },
        WinConditionComplex.kill_the_rabbit: {
            "index": 6,
        },
        WinConditionComplex.req_bean: {
            "index": 3,
            "item": 0xA,
        },
        WinConditionComplex.req_bp: {
            "index": 3,
            "item": 4,
        },
        WinConditionComplex.req_companycoins: {
            "index": 3,
            "item": 8,
        },
        WinConditionComplex.req_crown: {
            "index": 3,
            "item": 7,
        },
        WinConditionComplex.req_fairy: {
            "index": 3,
            "item": 5,
        },
        WinConditionComplex.req_gb: {
            "index": 3,
            "item": 3,
        },
        WinConditionComplex.req_pearl: {
            "index": 3,
            "item": 0xB,
        },
        WinConditionComplex.req_key: {
            "index": 3,
            "item": 6,
        },
        WinConditionComplex.req_medal: {
            "index": 3,
            "item": 9,
        },
        WinConditionComplex.req_rainbowcoin: {
            "index": 3,
            "item": 0xC,
        },
        WinConditionComplex.req_bonuses: {
            "index": 3,
            "item": 0x11,
        },
        WinConditionComplex.req_bosses: {
            "index": 3,
            "item": 0x10,
        },
    }
    win_con = spoiler.settings.win_condition_item
    win_con_data = win_con_table.get(win_con, None)
    if win_con_data is not None:
        ROM_COPY.seek(sav + 0x11D)
        ROM_COPY.write(win_con_data["index"])
        if "item" in win_con_data:
            ROM_COPY.seek(sav + 0xC0)
            ROM_COPY.write(win_con_data["item"])
            ROM_COPY.write(spoiler.settings.win_condition_count)

    # Fungi Time of Day
    fungi_times = (FungiTimeSetting.day, FungiTimeSetting.night, FungiTimeSetting.dusk, FungiTimeSetting.progressive)
    progressive_removals = [5, 4]  # Day Switch, Night Switch
    day_script = {
        Maps.FungiForest: [
            0xC,  # Day Gate - Mill Front Entry
            0xE,  # Day Gate - Punch Door
            0x12,  # Day Gate - Snide Area
        ],
    }
    night_script = {
        Maps.FungiForest: [
            8,  # Night Gate - Mill Lanky Attic
            0xB,  # Night Gate - Mill Winch Attic
            0xD,  # Night Gate - Dark Attic
            0x11,  # Night Gate - Thornvine Area
            0x2A,  # Night Gate - Mill GB
            0x53,  # Night Gate - Owl Tree Diddy Coins
            0x48,  # Night Gate - Beanstalk T&S
            0x1F1,  # Night Gate - Mushroom Night Door
            0x46,  # Night Gate - Crown Trapdoor
        ],
        Maps.ForestGiantMushroom: [0x11],  # Night Gate - GMush Interior
        Maps.ForestMillFront: [0xB],  # Night Gate - Mill Front
        Maps.ForestMillBack: [
            0xF,  # Night Gate - Mill Rear
            0x2,  # Night Gate - Spider Web
        ],
    }
    time_val = spoiler.settings.fungi_time_internal
    if time_val in fungi_times:
        ROM_COPY.seek(sav + 0x1DB)
        ROM_COPY.write(fungi_times.index(time_val))
        if time_val in (FungiTimeSetting.progressive, FungiTimeSetting.dusk):
            addNewScript(ROM_COPY, Maps.FungiForest, progressive_removals, ScriptTypes.DeleteItem)
    for map_id, changes in day_script.items():
        replaceScriptLines(
            ROM_COPY,
            map_id,
            changes,
            {
                "CONDINV 38 | 16 0 0": "COND 6 | 7 65519 0",
                "COND 38 | 16 0 0": "CONDINV 6 | 7 65519 0",
            },
        )
    for map_id, changes in night_script.items():
        replaceScriptLines(
            ROM_COPY,
            map_id,
            changes,
            {
                "COND 38 | 16 0 0": "COND 6 | 7 65519 1",
                "CONDINV 38 | 16 0 0": "CONDINV 6 | 7 65519 1",
            },
        )

    if spoiler.settings.fast_start_beginning_of_game:
        # Write a null move to this spot if fast start beginning of game is on
        ROM_COPY.seek(spoiler.settings.move_location_data + (125 * 6))
        ROM_COPY.writeMultipleBytes(0, 2)
        ROM_COPY.writeMultipleBytes(0, 4)

    # ROM Flags
    rom_flags = 0
    rom_flags |= 0x80 if spoiler.settings.enable_plandomizer else 0
    rom_flags |= 0x40 if spoiler.settings.generate_spoilerlog else 0
    rom_flags |= 0x20 if spoiler.settings.has_password else 0
    rom_flags |= 0x10 if spoiler.settings.archipelago else 0
    if spoiler.settings.archipelago:
        # Write spoiler.settings.player_name to ROM ASCII only
        ROM_COPY.seek(0x1FF3000)
        # Player name
        player_name = spoiler.settings.player_name[:16]
        # if we're shot on characters, pad with null bytes if we're short on characters
        if len(player_name) < 16:
            player_name += "\0" * (16 - len(player_name))
        # Convert playername to a bytestring and write it to the ROM
        bytestring = str(player_name).encode("ascii")
        ROM_COPY.writeBytes(bytestring)
    ROM_COPY.seek(sav + 0xC4)
    ROM_COPY.writeMultipleBytes(rom_flags, 1)
    password = None
    if spoiler.settings.has_password:
        ROM_COPY.seek(sav + 0x1B0)
        byte_data, password = encPass(spoiler)
        ROM_COPY.writeMultipleBytes(byte_data, 4)

    # Set K. Rool ship spawn method
    ROM_COPY.seek(sav + 0x1B6)
    # Write the user's setting directly - beat_krool/krools_challenge will use key-based spawning unless this is explicitly enabled
    ROM_COPY.writeMultipleBytes(spoiler.settings.win_condition_spawns_ship, 1)

    # Mill Levers
    if spoiler.settings.mill_levers[0] > 0:
        mill_text = ""
        for x in range(5):
            if spoiler.settings.mill_levers[x] > 0:
                mill_text += str(spoiler.settings.mill_levers[x])
        # Change default wrinkly hint
        if spoiler.settings.wrinkly_hints == WrinklyHints.off:
            if (
                IsDDMSSelected(
                    spoiler.settings.faster_checks_selected,
                    FasterChecksSelected.forest_mill_conveyor,
                )
                or spoiler.settings.puzzle_rando_difficulty != PuzzleRando.off
            ):
                data = {"textbox_index": 21, "mode": "replace", "search": "21132", "target": mill_text}
                for file in [CompTextFiles.Wrinkly]:
                    if file in spoiler.text_changes:
                        spoiler.text_changes[file].append(data)
                    else:
                        spoiler.text_changes[file] = [data]

    ROM_COPY.seek(sav + 0x36)
    ROM_COPY.write(spoiler.settings.rareware_gb_fairies)

    ROM_COPY.seek(sav + 0x1EB)
    ROM_COPY.write(spoiler.settings.mermaid_gb_pearls)

    if spoiler.settings.random_starting_region_new != RandomStartingRegion.off:
        ROM_COPY.seek(sav + 0x10C)
        ROM_COPY.write(spoiler.settings.starting_region["map"])
        exit_val = spoiler.settings.starting_region["exit"]
        if exit_val == -1:
            exit_val = 0xFF
        ROM_COPY.write(exit_val)
    if spoiler.settings.alter_switch_allocation:
        setProgSlamStrength(ROM_COPY, spoiler.settings)
    # Dartboard order
    DARTBOARD_IMAGES = [3, 1, 2, 0, 5, 4, 6, 7]
    DARTBOARD_DEFAULT_ORDER = [4, 2, 3, 1, 6, 5]
    for x in range(6):
        # Conversion to prevent repeated overwrites
        replaceScriptLines(ROM_COPY, Maps.FranticFactory, [0x7F], {f"EXEC 40 | 1 {x} 0": f"EXEC 40 | 1 {x} 1"})
        replaceScriptLines(
            ROM_COPY,
            Maps.FranticFactory,
            [0x7F],
            {
                f"COND 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 0": f"COND 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 1",
            },
        )
        replaceScriptLines(
            ROM_COPY,
            Maps.FranticFactory,
            [0x7F],
            {
                f"CONDINV 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 0": f"CONDINV 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 1",
            },
        )
    for x in range(6):
        index = spoiler.settings.dartboard_order[x]
        replaceScriptLines(ROM_COPY, Maps.FranticFactory, [0x7F], {f"EXEC 40 | 1 {x} 1": f"EXEC 40 | 1 {DARTBOARD_IMAGES[index]} 0"})
        replaceScriptLines(
            ROM_COPY,
            Maps.FranticFactory,
            [0x7F],
            {
                f"COND 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 1": f"COND 24 | 43 {index + 1} 0",
            },
        )
        replaceScriptLines(
            ROM_COPY,
            Maps.FranticFactory,
            [0x7F],
            {
                f"CONDINV 24 | 43 {DARTBOARD_DEFAULT_ORDER[x]} 1": f"CONDINV 24 | 43 {index + 1} 0",
            },
        )

    ROM_COPY.seek(sav + 0x060)
    for x in spoiler.settings.medal_cb_req_level:
        ROM_COPY.writeMultipleBytes(x, 1)
    if Types.HalfMedal in spoiler.settings.shuffled_location_types:
        ROM_COPY.seek(sav + 0x068)
        ROM_COPY.write(1)

    # Helm Required Minigames - Always set to 2 for now
    ROM_COPY.seek(sav + 0x2D)
    ROM_COPY.write(int(spoiler.settings.helm_room_bonus_count))

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        getHelmOrderHint(spoiler)
    randomize_entrances(spoiler, ROM_COPY)
    randomize_moves(spoiler, ROM_COPY)
    randomize_prices(spoiler, ROM_COPY)
    randomize_krool(spoiler, ROM_COPY)
    randomize_helm(spoiler, ROM_COPY)
    randomize_barrels(spoiler, ROM_COPY)
    move_bananaports(spoiler, ROM_COPY)  # Has to be before randomize_bananaport
    randomize_bananaport(spoiler, ROM_COPY)
    randomize_kasplat_locations(spoiler, ROM_COPY)
    randomize_enemies(spoiler, ROM_COPY)
    apply_kongrando_cosmetic(ROM_COPY)
    randomize_setup(spoiler, ROM_COPY)
    randomize_puzzles(spoiler, ROM_COPY)
    randomize_cbs(spoiler, ROM_COPY)
    randomize_coins(spoiler, ROM_COPY)
    place_mayhem_coins(spoiler, ROM_COPY)
    ApplyShopRandomizer(spoiler, ROM_COPY)
    remove5DSCameraPoint(spoiler, ROM_COPY)
    alterTextboxRequirements(spoiler)
    spoiler.arcade_item_reward = Items.NintendoCoin
    spoiler.jetpac_item_reward = Items.RarewareCoin
    place_randomized_items(spoiler, ROM_COPY)  # Has to be after kong rando cosmetic and moves
    place_spoiler_hint_data(sav, spoiler, ROM_COPY)
    # Arcade detection for colorblind mode
    arcade_item_index = 0
    potion_pools = [
        ItemPool.DonkeyMoves,
        ItemPool.DiddyMoves,
        ItemPool.LankyMoves,
        ItemPool.TinyMoves,
        ItemPool.ChunkyMoves,
        ItemPool.ImportantSharedMoves
        + ItemPool.JunkSharedMoves
        + ItemPool.TrainingBarrelAbilities()
        + ItemPool.ClimbingAbilities()
        + ItemPool.CannonAbilities()
        + [Items.Shockwave, Items.Camera, Items.CameraAndShockwave],
    ]
    for index, lst in enumerate(potion_pools):
        if spoiler.arcade_item_reward in lst:
            arcade_item_index = 1 + index
    ROM_COPY.seek(sav + 0x15A)
    ROM_COPY.writeMultipleBytes(arcade_item_index, 1)
    # Other funcs
    place_pregiven_moves(spoiler, ROM_COPY)
    remove_existing_indicators(spoiler, ROM_COPY)
    place_door_locations(spoiler, ROM_COPY)
    randomize_crown_pads(spoiler, ROM_COPY)
    randomize_melon_crate(spoiler, ROM_COPY)
    PlaceFairies(spoiler, ROM_COPY)
    filterEntranceType(ROM_COPY)
    updateKrushaMoveNames(spoiler)
    updateSwitchsanity(spoiler, ROM_COPY)
    updateRandomSwitches(spoiler, ROM_COPY)  # Has to be after all setup changes that may alter the item type of slam switches
    PushItemLocations(spoiler, ROM_COPY)

    if spoiler.settings.wrinkly_hints != WrinklyHints.off:
        PushHints(spoiler, ROM_COPY)
        if spoiler.settings.dim_solved_hints:
            PushHelpfulHints(spoiler, ROM_COPY)
    if Types.Hint in spoiler.settings.shuffled_location_types and spoiler.settings.progressive_hint_item == ProgressiveHintItem.off:
        PushHintTiedRegions(spoiler, ROM_COPY)

    writeBootMessages(ROM_COPY, spoiler)
    enableTriggerText(spoiler, ROM_COPY)
    shortenCastleMinecart(spoiler, ROM_COPY)
    alterStoryCutsceneWarps(spoiler, ROM_COPY)

    if "PYTEST_CURRENT_TEST" not in os.environ:
        replaceIngameText(spoiler, ROM_COPY)
        updateMillLeverTexture(spoiler.settings, ROM_COPY)
        updateCryptLeverTexture(spoiler.settings, ROM_COPY)
        updateDiddyDoors(spoiler.settings, ROM_COPY)
        applyHelmDoorCosmetics(spoiler.settings, ROM_COPY)
        applyKongModelSwaps(spoiler.settings, ROM_COPY)
        updateHelmFaces(spoiler.settings, ROM_COPY)
        updateSnidePanel(spoiler.settings, ROM_COPY)
        showWinCondition(spoiler.settings, ROM_COPY)
        addBalloonBulb(spoiler.settings, ROM_COPY, ColorblindMode.off)

        patchAssembly(ROM_COPY, spoiler)
        patchScripts(spoiler, ROM_COPY)
        calculateInitFileScreen(spoiler, ROM_COPY)
        ApplyMirrorMode(spoiler.settings, ROM_COPY)

    precalcBoot(ROM_COPY, spoiler)  # Needs to be done after any updates to setup for CBs, patches and crates

    # Apply Hash
    order = 0
    for count in spoiler.settings.seed_hash:
        ROM_COPY.seek(sav + 0x129 + order)
        ROM_COPY.write(count)
        order += 1

    # Create a dummy time to attach to the end of the file name non decimal
    str(time.time()).replace(".", "")
    if "PYTEST_CURRENT_TEST" not in os.environ:
        created_tempfile = mktemp()
        delta_tempfile = mktemp()
        # Write the LocalROM.rom bytesIo to a file
        with open(created_tempfile, "wb") as f:
            f.write(ROM_COPY.rom.getvalue())

        import pyxdelta

        pyxdelta.run("dk64.z64", created_tempfile, delta_tempfile)
        # Read the patch file
        with open(delta_tempfile, "rb") as f:
            patch = f.read()
        # Delete the patch.z64 file
        os.remove(created_tempfile)
        os.remove(delta_tempfile)
    else:
        patch = None
    del ROM_COPY
    return patch, password


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result
