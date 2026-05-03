"""Adapter that wraps a FillResult protobuf message in a Spoiler-like interface."""

import json
from copy import deepcopy
from typing import Any, Iterator

from randomizer.Enums.DoorType import DoorType
from randomizer.Enums.Enemies import Enemies
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import SlamRequirement
from randomizer.Enums.Switches import Switches
from randomizer.Enums.SwitchTypes import SwitchType
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists.EnemyTypes import enemy_location_list
from randomizer.Lists.Location import LocationListOriginal, PreGivenLocations
from randomizer.Lists.Minigame import BarrelMetaData, MinigameLocationData
from randomizer.Lists.Switches import SwitchData
from randomizer.Logic import RegionsOriginal


class PatchingLocationDict:
    """Spoiler-like LocationList view backed by a FillResult.location_assignments proto."""

    def __init__(self, assignments: Any) -> None:
        self._assignments = assignments
        self._cache: dict[int, Any] = {}  # Cache LocationObj instances to persist attribute changes

    def get_or_create_location(self, location_id: int) -> Any:
        """Get or create a LocationObj for the given location_id."""
        if location_id not in self._cache:

            class LocationObj:
                def __init__(self, item_id: int, location_id: int) -> None:
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

    def items(self) -> Iterator[tuple[int, Any]]:
        """Return (location_id, location_obj) pairs."""
        for loc_id in self._assignments.assignments.keys():
            yield (loc_id, self.get_or_create_location(loc_id))

    def __iter__(self) -> Iterator[int]:
        """Iterate over location IDs."""
        return iter(self._assignments.assignments.keys())

    def __len__(self) -> int:
        """Return number of locations."""
        return len(self._assignments.assignments)

    def __getitem__(self, key: Any) -> Any:
        # Handle multiple key types: int, Locations enum, LocationObj, etc.
        if isinstance(key, int):
            key_int = key
        elif hasattr(key, "location"):
            # LocationObj from our own adapter - has .location attribute with the ID
            key_int = int(key.location)
        elif hasattr(key, "value"):
            # Enum type (Locations has .value attribute)
            key_int = int(key.value)
        else:
            # Try direct conversion
            key_int = int(key)
        return self.get_or_create_location(key_int)

    def __contains__(self, key: Any) -> bool:
        """Check if location exists in assignments."""
        if isinstance(key, int):
            key_int = key
        elif hasattr(key, "location"):
            # LocationObj from our own adapter
            key_int = int(key.location)
        elif hasattr(key, "value"):
            key_int = int(key.value)
        else:
            key_int = int(key)
        return key_int in self._assignments.assignments


def create_patching_adapter(fill_result: Any, settings: Any) -> Any:
    """Create an adapter object that converts FillResult proto to spoiler-like interface.

    This adapter allows existing patching code to work with the proto without
    requiring immediate refactoring of all patching functions.

    Args:
        fill_result: FillResult protobuf message
        settings: Settings object

    Returns:
        Adapter object with spoiler-like interface
    """

    class PatchingAdapter:
        """Adapter that provides spoiler-like interface for FillResult proto."""

        def __init__(self, fill_result: Any, settings: Any) -> None:
            self.settings = settings
            self.fill_result = fill_result
            self.json = "{}"  # Will be populated in patching_response
            self.text_changes = {}
            self.microhints = dict(fill_result.hint_data.microhints)
            self.pregiven_items = []  # Items given at start (populated during Fill)
            self.arcade_item_reward = None  # Set in patching_response
            self.jetpac_item_reward = None  # Set in patching_response

            if list(fill_result.misc_data.switch_allocation):
                restored = []
                for raw in fill_result.misc_data.switch_allocation:
                    try:
                        restored.append(SlamRequirement(int(raw)))
                    except ValueError:
                        restored.append(int(raw))
                settings.switch_allocation = restored

            # Switchsanity
            if fill_result.misc_data.HasField("switchsanity_enabled"):
                settings.switchsanity_enabled = bool(fill_result.misc_data.switchsanity_enabled)
            if list(fill_result.misc_data.switchsanity_data):
                settings.switchsanity_data = deepcopy(SwitchData)
                for entry in fill_result.misc_data.switchsanity_data:
                    switch_enum = Switches(int(entry.switch))
                    if switch_enum not in settings.switchsanity_data:
                        continue
                    info = settings.switchsanity_data[switch_enum]
                    info.kong = Kongs(int(entry.kong))
                    info.switch_type = SwitchType(int(entry.switch_type))
                # Update the locations' assigned kong with the set freeing kong list
                settings.diddy_freeing_kong = settings.switchsanity_data[Switches.JapesFreeKong].kong
                settings.lanky_freeing_kong = settings.switchsanity_data[Switches.AztecLlamaPuzzle].kong
                settings.tiny_freeing_kong = settings.switchsanity_data[Switches.AztecOKONGPuzzle].kong
                settings.chunky_freeing_kong = settings.switchsanity_data[Switches.FactoryFreeKong].kong

            # Ship location rando result
            self.ship_location_index = None
            self.ship_name = ""
            if fill_result.misc_data.HasField("ship_location_index"):
                self.ship_location_index = int(fill_result.misc_data.ship_location_index)
            if fill_result.misc_data.HasField("ship_name"):
                self.ship_name = str(fill_result.misc_data.ship_name)

            # ---- Enemy rando data ----
            # Reconstruct spoiler.enemy_rando_data (map_id -> list of dicts)
            # from the proto. Consumed by randomize_enemies at patch time.
            enemy_rando_data = {}
            for map_id, map_entries in fill_result.placement_data.enemy_rando_data.items():
                entries_list = []
                for entry in map_entries.entries:
                    try:
                        enemy_enum = Enemies(int(entry.enemy))
                    except Exception:
                        enemy_enum = int(entry.enemy)
                    entries_list.append(
                        {
                            "enemy": enemy_enum,
                            "speeds": list(entry.speeds),
                            "id": int(entry.spawner_id),
                            "location": entry.location,
                        }
                    )
                enemy_rando_data[int(map_id)] = entries_list
            self.enemy_rando_data = enemy_rando_data

            # valid_photo_items, pkmn_snap_data and the static enemy_location_list
            # are all read by the patching code; restore them from the proto /
            # static source so the adapter behaves like a real Spoiler.
            valid_photo_items = []
            for pid in fill_result.misc_data.valid_photo_items:
                try:
                    valid_photo_items.append(Items(int(pid)))
                except Exception:
                    valid_photo_items.append(int(pid))
            self.valid_photo_items = valid_photo_items
            self.pkmn_snap_data = list(fill_result.placement_data.pkmn_snap_data)
            try:
                self.enemy_location_list = deepcopy(enemy_location_list)
            except Exception as _e:
                self.enemy_location_list = {}

            # Populate pregiven_items. Prefer the explicit `pregiven_items`
            # field on the proto (populated in both local-rando and AP flows);
            # fall back to reconstructing from PreGivenLocations in
            # location_assignments for old proto files that predate the field.
            try:
                fast_start = getattr(settings, "fast_start_beginning_of_game", True)
                self.first_move_item = None

                misc = fill_result.misc_data
                explicit_pregiven = list(misc.pregiven_items) if len(misc.pregiven_items) > 0 else None
                if explicit_pregiven is not None:
                    for item_id in explicit_pregiven:
                        try:
                            self.pregiven_items.append(Items(int(item_id)))
                        except Exception:
                            continue
                    if misc.HasField("first_move_item"):
                        try:
                            self.first_move_item = Items(int(misc.first_move_item))
                        except Exception:
                            self.first_move_item = None
                else:
                    for loc_id, item_id in fill_result.location_assignments.assignments.items():
                        try:
                            loc_enum = Locations(int(loc_id))
                        except Exception:
                            continue
                        if loc_enum not in PreGivenLocations:
                            continue
                        try:
                            item_enum = Items(int(item_id))
                        except Exception:
                            continue
                        if fast_start or loc_enum != Locations.IslesFirstMove:
                            self.pregiven_items.append(item_enum)
                        else:
                            self.first_move_item = item_enum
            except Exception as _e:
                self.first_move_item = None

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
                # Special Items
                ItemReference(Items.Bean, "The Bean", "Forst Anthill Second Reward"),
                ItemReference(Items.NintendoCoin, "Nintendo Coin", "Factory Arcade Round 2"),
                ItemReference(Items.RarewareCoin, "Rareware Coin", "Jetpac"),
            ]

            # Convert shuffled exits from proto to TransitionBack-like objects
            self.shuffled_exit_data = {}
            for exit_id, exit_dest in fill_result.shuffle_data.shuffled_exits.items():
                # Mirror randomizer.LogicClasses.TransitionBack attributes so downstream
                # consumers (EntranceRando, CompileHints, Spoiler) work unchanged.
                class ExitDestination:
                    def __init__(self, region_id: Any, reverse: Any, exit_name: str, spoiler_name: str) -> None:
                        self.regionId = region_id if isinstance(region_id, Regions) else Regions(region_id)
                        try:
                            self.reverse = Transitions(reverse) if reverse is not None else None
                        except ValueError:
                            self.reverse = None
                        self.name = exit_name
                        self.spoilerName = spoiler_name
                        # Back-compat aliases for any remaining legacy access patterns.
                        self.dest = self.regionId
                        self.exit = exit_name

                transition_key = exit_id
                try:
                    transition_key = Transitions(exit_id)
                except ValueError:
                    pass
                self.shuffled_exit_data[transition_key] = ExitDestination(exit_dest.destination_region, exit_dest.reverse_transition, exit_dest.exit_name, exit_dest.spoiler_name)

            # Store proto references for functions that need them
            self._location_assignments = fill_result.location_assignments
            self._move_shop_data = fill_result.move_shop_data
            self._shuffle_data = fill_result.shuffle_data
            self._placement_data = fill_result.placement_data
            self._hint_data = fill_result.hint_data
            self._path_data = fill_result.path_data
            self._misc_data = fill_result.misc_data

            # One LocationDict per adapter so its _cache survives across reads and
            # in-place mutations land on the same LocationObj on every access.
            self._location_dict = PatchingLocationDict(self._location_assignments)

        # Properties to access proto data with backward-compatible interface
        @property
        def LocationList(self) -> "PatchingLocationDict":
            """Simulate LocationList for item rando."""
            return self._location_dict

        @property
        def move_data(self) -> list:
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
                            level_moves.append(move_entry_proto_to_dict(move_entry))
                        # Ensure we always have exactly 8 levels (pad with empty moves if needed)
                        while len(level_moves) < 8:
                            level_moves.append({"move_type": None})
                        kong_moves_list.append(level_moves)
                    shop_moves.append(kong_moves_list)
            result.append(shop_moves)

            # Index 1: Training barrels
            training = []
            for move_entry in self._move_shop_data.training_barrels:
                training.append(move_entry_proto_to_dict(move_entry))
            result.append(training)

            # Index 2: BFI moves
            bfi = []
            for move_entry in self._move_shop_data.bfi_moves:
                bfi.append(move_entry_proto_to_dict(move_entry))
            result.append(bfi)

            return result

        @property
        def shuffled_barrel_data(self) -> dict:
            """Return barrel shuffle data - reconstruct MinigameLocationData objects."""
            result = {}
            for location_id, minigame_type in self._shuffle_data.shuffled_barrels.items():
                # Get the original barrel metadata for this location
                if location_id in BarrelMetaData:
                    original = BarrelMetaData[location_id]
                    # Create new MinigameLocationData with shuffled minigame but original location data
                    result[location_id] = MinigameLocationData(original.map, original.barrel_id, Minigames(minigame_type), original.kong)
                else:
                    # Fallback - shouldn't happen but be defensive
                    result[location_id] = minigame_type
            return result

        @property
        def shuffled_door_data(self) -> dict[Levels, list[tuple]]:
            """Return door shuffle data."""
            # Convert proto door shuffles back to the legacy tuple shape expected
            # by DoorPlacer.place_door_locations:
            #   (door_index, DoorType.wrinkly, kong_assignee)
            #   (door_index, DoorType.boss)
            #   (door_index, DoorType.dk_portal)
            # Make sure every level key is present (with an empty list) so
            # `for level in spoiler.shuffled_door_data` iterates all 7 levels.
            result = {
                lvl: []
                for lvl in (
                    Levels.JungleJapes,
                    Levels.AngryAztec,
                    Levels.FranticFactory,
                    Levels.GloomyGalleon,
                    Levels.FungiForest,
                    Levels.CrystalCaves,
                    Levels.CreepyCastle,
                )
            }
            for door_shuffle in self._shuffle_data.shuffled_doors:
                level = Levels(door_shuffle.level)
                entries = []
                for door in door_shuffle.doors:
                    try:
                        door_type = DoorType(int(door.door_type))
                    except (ValueError, TypeError):
                        continue
                    if door_type == DoorType.wrinkly:
                        entries.append((int(door.door_location), door_type, int(door.kong_assignee)))
                    else:
                        entries.append((int(door.door_location), door_type))
                result[level] = entries
            return result

        @property
        def shuffled_exit_instructions(self) -> list:
            """Return exit instructions."""
            instructions = []
            for entry in self._shuffle_data.exit_instructions:
                if isinstance(entry, str):
                    try:
                        parsed = json.loads(entry)
                        if isinstance(parsed, (dict, list)):
                            instructions.append(parsed)
                            continue
                    except (ValueError, json.JSONDecodeError):
                        pass
                instructions.append(entry)
            return instructions

        @property
        def cb_placements(self) -> list[dict]:
            """Return CB placements."""
            result = []
            for cb_proto in self._placement_data.cb_placements:
                cb_dict = {
                    "id": cb_proto.id,
                    "name": cb_proto.name,
                    "kong": cb_proto.kong,
                    "level": cb_proto.level,
                    "type": cb_proto.type,
                    "map": cb_proto.map,
                }
                if cb_proto.locations:
                    cb_dict["locations"] = [[loc.amount, loc.scale, loc.x, loc.y, loc.z] for loc in cb_proto.locations]
                result.append(cb_dict)
            return result

        @property
        def balloon_placement(self) -> list[dict]:
            """Return balloon placements."""
            result = []
            for balloon_proto in self._placement_data.balloon_placements:
                result.append(
                    {
                        "id": balloon_proto.id,
                        "name": balloon_proto.name,
                        "kong": balloon_proto.kong,
                        "level": balloon_proto.level,
                        "map": balloon_proto.map,
                        "score": balloon_proto.score,
                    }
                )
            return result

        @property
        def enemy_replacements(self) -> list[dict]:
            """Return enemy replacements."""
            result = []
            for enemy_proto in self._placement_data.enemy_replacements:
                swaps = []
                for swap_proto in enemy_proto.kasplat_swaps:
                    swaps.append(
                        {
                            "vanilla_location": swap_proto.vanilla_location,
                            "replace_with": swap_proto.replace_with,
                        }
                    )
                result.append(
                    {
                        "container_map": enemy_proto.container_map,
                        "kasplat_swaps": swaps,
                    }
                )
            return result

        @property
        def coin_requirements(self) -> dict:
            """Return coin requirements."""
            return dict(self._placement_data.coin_requirements)

        @property
        def item_assignment(self) -> list:
            """Return item assignments."""
            result = []
            for assign_proto in self._misc_data.item_assignments:

                class ItemAssignment:
                    pass

                assign_obj = ItemAssignment()

                # Proto fields (all sint32 on the wire; -1 == None sentinel).
                assign_obj.old_type = Types(assign_proto.old_type) if assign_proto.old_type >= 0 else None
                assign_obj.old_flag = assign_proto.old_flag  # -1 means no flag
                assign_obj.old_item = Types(assign_proto.old_item) if assign_proto.old_item >= 0 else None
                assign_obj.old_kong = Kongs(assign_proto.old_kong) if assign_proto.old_kong >= 0 else Kongs.any

                # placement_data is the canonical attribute on LocationSelection;
                # maps_to_actor_ids is kept as an alias for any legacy readers.
                placement_data = dict(assign_proto.maps_to_actor_ids)
                assign_obj.placement_data = placement_data
                assign_obj.maps_to_actor_ids = placement_data

                assign_obj.location = assign_proto.location
                assign_obj.new_flag = assign_proto.new_flag
                assign_obj.new_type = Types(assign_proto.new_type) if assign_proto.new_type >= 0 else None
                assign_obj.new_item = Items(assign_proto.new_item) if assign_proto.new_item >= 0 else None
                assign_obj.new_kong = Kongs(assign_proto.new_kong) if assign_proto.new_kong >= 0 else Kongs.any
                assign_obj.shared = assign_proto.shared

                # placement_index is a repeated sint32 — preserve the whole list
                # (shared shop items patch multiple slots).
                assign_obj.placement_index = [int(p) for p in assign_proto.placement_index]
                assign_obj.placement_subindex = assign_proto.placement_subindex

                # LocationSelection metadata consumed by the patcher.
                assign_obj.reward_spot = bool(assign_proto.is_reward_point)
                assign_obj.is_shop = bool(assign_proto.is_shop)
                assign_obj.price = int(assign_proto.price)
                assign_obj.can_have_item = bool(assign_proto.can_have_item)
                assign_obj.can_place_item = bool(assign_proto.can_place_item)
                assign_obj.shop_locked = bool(assign_proto.shop_locked)
                assign_obj.order = int(assign_proto.order)
                assign_obj.name = assign_proto.name
                assign_obj.move_name = assign_proto.move_name

                result.append(assign_obj)
            return result

        @property
        def music_bgm_data(self) -> dict:
            """Return BGM music data."""
            return dict(self._misc_data.music_bgm_data)

        @property
        def music_majoritem_data(self) -> dict:
            """Return major item music data."""
            return dict(self._misc_data.music_majoritem_data)

        @property
        def music_minoritem_data(self) -> dict:
            """Return minor item music data."""
            return dict(self._misc_data.music_minoritem_data)

        @property
        def music_event_data(self) -> dict:
            """Return event music data."""
            return dict(self._misc_data.music_event_data)

        @property
        def hintset(self) -> Any:
            """Return hint set."""

            class HintSet:
                def __init__(self, proto: Any) -> None:
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

                def RemoveFTT(self) -> None:
                    """Remove the First Time Talk hint (called after writing to ROM)."""
                    # FTT is the first hint, remove it from the list
                    if self.hints:
                        self.hints = self.hints[1:]

            return HintSet(self._hint_data.hint_set)

        @property
        def tied_hint_flags(self) -> dict:
            """Return tied hint flags."""
            return dict(self._hint_data.tied_hint_flags)

        @property
        def tied_hint_regions(self) -> list:
            """Return tied hint regions."""
            return list(self._hint_data.tied_hint_regions)

        @property
        def RegionList(self) -> dict:
            """Return region list - this is logic data not part of Fill output."""
            return RegionsOriginal

        @property
        def majorItems(self) -> list[Items]:
            """Return major items list."""
            return [Items(item_id) for item_id in self._path_data.major_items]

        @property
        def woth_locations(self) -> list[Locations]:
            """Return Way of the Hoard locations."""
            return [Locations(loc_id) for loc_id in self._path_data.woth_locations]

        @property
        def woth_paths(self) -> dict[Locations, list[Locations]]:
            """Return Way of the Hoard paths."""
            result = {}
            for loc_id, path_proto in self._path_data.woth_paths.items():
                result[Locations(loc_id)] = [Locations(l) for l in path_proto.locations]
            return result

        @property
        def foolish_region_names(self) -> list[str]:
            """Return foolish region names."""
            return list(self._path_data.foolish_region_names)

        @property
        def pathless_moves(self) -> list[Items]:
            """Return pathless moves."""
            return [Items(item_id) for item_id in self._path_data.pathless_moves]

        @property
        def playthrough(self) -> dict[int, dict[Locations, Items]]:
            """Return playthrough spheres."""
            result = {}
            for i, sphere_proto in enumerate(self._path_data.playthrough):
                sphere_dict = {}
                for loc_proto in sphere_proto.locations:
                    sphere_dict[Locations(loc_proto.location_id)] = Items(loc_proto.item_id)
                result[i] = sphere_dict
            return result

        @property
        def region_hintable_count(self) -> dict[str, dict[int, dict]]:
            """Return region hintable count."""
            result = {}
            for region_name, counts_proto in self._path_data.region_hintable_count.items():
                region_dict = {}
                for item_type, item_data in counts_proto.items.items():
                    region_dict[int(item_type)] = {"count": item_data.count, "locations": [Locations(loc_id) for loc_id in item_data.location_ids]}
                result[region_name] = region_dict
            return result

        @property
        def crown_locations(self) -> dict[Levels, dict[int, int]]:
            """Return crown locations as {Levels: {crown_index: subindex}}."""
            result = {}
            for crown_proto in self._shuffle_data.crown_placements:
                level = Levels(crown_proto.level)
                if level not in result:
                    result[level] = {}
                result[level][int(crown_proto.crown_index)] = int(crown_proto.subindex)
            return result

        @property
        def dirt_patch_placement(self) -> list[dict]:
            """Return dirt patch placements as list of dicts."""
            result = []
            for patch_proto in self._shuffle_data.patch_placements:
                result.append(
                    {
                        "name": patch_proto.name,
                        "map": int(patch_proto.map_id),
                        "level": Levels(patch_proto.level),
                    }
                )
            return result

        @property
        def meloncrate_placement(self) -> list[dict]:
            """Return melon crate placements as list of dicts."""
            result = []
            for crate_proto in self._shuffle_data.crate_placements:
                result.append(
                    {
                        "name": crate_proto.name,
                        "map": int(crate_proto.map_id),
                        "level": Levels(crate_proto.level),
                    }
                )
            return result

        @property
        def coin_placements(self) -> list[dict]:
            """Return coin placements."""
            result = []
            for coin_proto in self._placement_data.coin_placements:
                locations = [[loc.scale, loc.x, loc.y, loc.z] for loc in coin_proto.locations]
                result.append(
                    {
                        "level": int(coin_proto.level),
                        "map": int(coin_proto.map),
                        "kong": int(coin_proto.kong),
                        "type": coin_proto.type,
                        "name": coin_proto.name,
                        "locations": locations,
                    }
                )
            return result

        @property
        def race_coin_placements(self) -> list[dict]:
            """Return race coin placements."""
            result = []
            for coin_proto in self._placement_data.race_coin_placements:
                locations = [[loc.scale, loc.x, loc.y, loc.z] for loc in coin_proto.locations]
                result.append(
                    {
                        "map": int(coin_proto.map),
                        "level": int(coin_proto.level),
                        "name": coin_proto.name,
                        "locations": locations,
                    }
                )
            return result

        @property
        def shuffled_shop_locations(self) -> dict[Levels, dict[Regions, Regions]]:
            """Return shuffled shop locations as {Levels: {old_shop: new_shop}}."""
            result = {}
            for shuffle_proto in self._shuffle_data.shuffled_shop_locations:
                level = Levels(shuffle_proto.level)
                level_map = {}
                for assign in shuffle_proto.assignments:
                    level_map[Regions(assign.old_shop)] = Regions(assign.new_shop)
                result[level] = level_map
            return result

        @property
        def shuffled_kasplat_map(self) -> dict:
            """Return kasplat shuffles as {name: kong_index}."""
            return dict(self._shuffle_data.shuffled_kasplat_map)

        @property
        def fairy_locations(self) -> dict[Levels, list[int]]:
            """Return fairy locations as {Levels: [fairy_indexes]}."""
            result = {}
            for fairy_proto in self._shuffle_data.fairy_locations:
                result[Levels(fairy_proto.level)] = list(fairy_proto.fairy_indexes)
            return result

        @property
        def fairy_data_table(self) -> list[dict | None]:
            """Return fairy data table as list of 20 dicts (or None)."""
            result = []
            for entry_proto in self._shuffle_data.fairy_data_table:
                if entry_proto.present:
                    result.append(
                        {
                            "fairy_index": int(entry_proto.fairy_index),
                            "level": Levels(entry_proto.level),
                            "flag": int(entry_proto.flag),
                            "id": int(entry_proto.id),
                            "shift": int(entry_proto.shift),
                            "script_id": int(entry_proto.script_id),
                            "map_id": int(entry_proto.map_id),
                        }
                    )
                else:
                    result.append(None)
            return result

        @property
        def bananaport_replacements(self) -> list[tuple[int, int]]:
            """Return bananaport replacements as [(new_pad_index, visual_type)]."""
            return [(int(bp.new_pad_index), int(bp.visual_type)) for bp in self._shuffle_data.bananaport_replacements]

        @property
        def warp_locations(self) -> dict:
            """Return warp locations as {warp_id: custom_location_id}."""
            return dict(self._shuffle_data.warp_locations)

        @property
        def level_spoiler(self) -> dict[Levels, Any]:
            """Return level spoiler as {Levels: obj with .level_items}."""

            class LevelSpoiler:
                def __init__(self, level_items: list[dict]) -> None:
                    self.level_items = level_items

            result = {}
            for level_id, hints_proto in self._hint_data.level_spoiler_hints.items():
                items = []
                for item_proto in hints_proto.level_items:
                    items.append(
                        {
                            "item": Items(item_proto.item) if item_proto.item else None,
                            "points": int(item_proto.points),
                            "flag": int(item_proto.flag),
                        }
                    )
                result[Levels(level_id)] = LevelSpoiler(items)
            return result

    return PatchingAdapter(fill_result, settings)


def move_entry_proto_to_dict(move_entry_proto: Any) -> dict:
    """Convert a MoveEntry proto to a dictionary."""
    which = move_entry_proto.WhichOneof("entry")

    if which == "empty_move":
        return {"move_type": None}
    elif which == "flag_move":
        return {
            "move_type": "flag",
            "flag": move_entry_proto.flag_move.flag,
            "price": move_entry_proto.flag_move.price,
        }
    elif which == "special_move":
        return {
            "move_type": "special",
            "move_lvl": move_entry_proto.special_move.move_lvl,
            "move_kong": move_entry_proto.special_move.move_kong,
            "price": move_entry_proto.special_move.price,
        }
    elif which == "slam_move":
        return {
            "move_type": "slam",
            "move_lvl": move_entry_proto.slam_move.move_lvl,
            "move_kong": move_entry_proto.slam_move.move_kong,
            "price": move_entry_proto.slam_move.price,
        }
    elif which == "gun_move":
        return {
            "move_type": "gun",
            "move_lvl": move_entry_proto.gun_move.move_lvl,
            "move_kong": move_entry_proto.gun_move.move_kong,
            "price": move_entry_proto.gun_move.price,
        }
    elif which == "ammo_belt_move":
        return {
            "move_type": "ammo_belt",
            "move_lvl": move_entry_proto.ammo_belt_move.move_lvl,
            "move_kong": move_entry_proto.ammo_belt_move.move_kong,
            "price": move_entry_proto.ammo_belt_move.price,
        }
    elif which == "instrument_move":
        return {
            "move_type": "instrument",
            "move_lvl": move_entry_proto.instrument_move.move_lvl,
            "move_kong": move_entry_proto.instrument_move.move_kong,
            "price": move_entry_proto.instrument_move.price,
        }
    else:
        return {"move_type": None}
