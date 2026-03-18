"""This file contains the logic for creating and connecting regions in the Donkey Kong 64 world."""

import typing

from BaseClasses import CollectionState, ItemClassification, MultiWorld, Region, Entrance, EntranceType, Location
from entrance_rando import disconnect_entrance_for_randomization, ERPlacementState
from worlds.AutoWorld import World

from randomizer import Spoiler
from randomizer import Settings
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import HelmSetting, FungiTimeSetting, FasterChecksSelected, RemovedBarriersSelected, ShuffleLoadingZones, WinConditionComplex, LevelRandomization, DKPortalRando
from randomizer.Enums.Time import Time
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import Types
from randomizer.Lists import Location as DK64RLocation, Item as DK64RItem
from randomizer.Lists.Location import SharedShopLocations
from randomizer.Lists.Minigame import MinigameRequirements
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.LogicClasses import Collectible, Event, LocationLogic, TransitionFront, Region as DK64Region
from randomizer.Patching.Library.Generic import IsItemSelected
from archipelago.Items import DK64Item
from worlds.generic.Rules import add_item_rule, add_rule, set_rule
from archipelago.Logic import LogicVarHolder
from randomizer.LogicFiles import (
    AngryAztec,
    CreepyCastle,
    CrystalCaves,
    DKIsles,
    FungiForest,
    HideoutHelm,
    JungleJapes,
    FranticFactory,
    GloomyGalleon,
    Shops,
)
from randomizer.CollectibleLogicFiles import (
    AngryAztec as AztecCollectibles,
    CreepyCastle as CastleCollectibles,
    CrystalCaves as CavesCollectibles,
    DKIsles as IslesCollectibles,
    FungiForest as ForestCollectibles,
    JungleJapes as JapesCollectibles,
    FranticFactory as FactoryCollectibles,
    GloomyGalleon as GalleonCollectibles,
)

BASE_ID = 0xD64000


class DK64Location(Location):
    """A class representing a location in Donkey Kong 64."""

    game: str = "Donkey Kong 64"

    def __init__(self, player: int, name: str = "", address: int = None, parent=None):
        """Initialize a new location."""
        super().__init__(player, name, address, parent)


# Complete location table
all_locations = {
    DK64RLocation.LocationListOriginal[location].name: (BASE_ID + index)
    for index, location in enumerate(DK64RLocation.LocationListOriginal)
    if DK64RLocation.LocationListOriginal[location].type != Types.EnemyPhoto
}
all_locations.update({"Victory": 0x00})  # Temp for generating goal location
lookup_id_to_name: typing.Dict[int, str] = {id: name for name, id in all_locations.items()}

all_collectible_regions = {
    **AztecCollectibles.LogicRegions,
    **CastleCollectibles.LogicRegions,
    **CavesCollectibles.LogicRegions,
    **IslesCollectibles.LogicRegions,
    **ForestCollectibles.LogicRegions,
    **JapesCollectibles.LogicRegions,
    **FactoryCollectibles.LogicRegions,
    **GalleonCollectibles.LogicRegions,
}
all_logic_regions = {
    **AngryAztec.LogicRegions,
    **CreepyCastle.LogicRegions,
    **CrystalCaves.LogicRegions,
    **DKIsles.LogicRegions,
    **FungiForest.LogicRegions,
    **HideoutHelm.LogicRegions,
    **JungleJapes.LogicRegions,
    **FranticFactory.LogicRegions,
    **GloomyGalleon.LogicRegions,
    **Shops.LogicRegions,
}

gun_for_kong = {Kongs.donkey: "Coconut", Kongs.diddy: "Peanut", Kongs.lanky: "Grape", Kongs.tiny: "Feather", Kongs.chunky: "Pineapple"}

name_for_kong = {Kongs.donkey: "Donkey", Kongs.diddy: "Diddy", Kongs.lanky: "Lanky", Kongs.tiny: "Tiny", Kongs.chunky: "Chunky"}


def create_regions(multiworld: MultiWorld, player: int, spoiler: Spoiler, options=None):
    """Create the regions for the given player's world."""
    menu_region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu_region)

    # okay okay OKAY you get a logicVarHolder object for JUST THIS ONCE. Codes these days...
    logic_holder = LogicVarHolder(spoiler, player)

    # Build location table from spoiler's LocationList (which may have custom locations)
    all_locations_dynamic = {
        spoiler.LocationList[location].name: (BASE_ID + index) for index, location in enumerate(DK64RLocation.LocationListOriginal) if spoiler.LocationList[location].type != Types.EnemyPhoto
    }
    all_locations_dynamic.update({"Victory": 0x00})  # Temp for generating goal location

    # Debug: check for custom location names
    custom_names = [name for name in all_locations_dynamic.keys() if "Battle Arena" in name or "Melon Crate" in name or "Dirt:" in name]
    if custom_names and len(custom_names) > 0:
        print(f"[DK64 create_regions] Found {len(custom_names)} custom locations, samples:")
        for name in custom_names[:5]:
            print(f"  {name}")

    # Pick random 10 shops to make shared
    # Only if shared shops are enabled in settings
    if options.enable_shared_shops.value:
        # If not set (e.g., free prices), select them now
        if hasattr(logic_holder.spoiler.settings, "selected_shared_shops") and logic_holder.spoiler.settings.selected_shared_shops:
            logic_holder.available_shared_shops = logic_holder.spoiler.settings.selected_shared_shops
        else:
            all_shared_shops = list(SharedShopLocations)
            logic_holder.settings.random.shuffle(all_shared_shops)
            logic_holder.available_shared_shops = set(all_shared_shops[:10])

        # Track which vendor/level combinations have shared shops to make individual shops inaccessible
        shared_shop_vendors = set()

        # Pre-process to identify which vendor/level combinations will have shared shops
        for region_id in logic_holder.spoiler.RegionList:
            region_obj = logic_holder.spoiler.RegionList[region_id]
            location_logics = [loc for loc in region_obj.locations if (not loc.isAuxiliaryLocation) or region_id.name == "FactoryBaboonBlast"]

            for location_logic in location_logics:
                location_obj = logic_holder.spoiler.LocationList[location_logic.id]
                # Check if this is a shared shop that will be created
                if location_obj.type == Types.Shop and location_obj.kong == Kongs.any:
                    if location_logic.id in logic_holder.available_shared_shops:
                        # Mark this vendor/level combination as having a shared shop
                        shared_shop_vendors.add((location_obj.level, location_obj.vendor))

        # Store shared shop vendors in logic_holder for access in create_region
        logic_holder.shared_shop_vendors = shared_shop_vendors
    else:
        # Shared shops disabled - no shared shops available
        logic_holder.available_shared_shops = set()
        logic_holder.shared_shop_vendors = set()

    # # Print contents of all_locations
    # print("All Locations:")
    # for location_name, location_id in all_locations.items():
    #     print(f"{location_name}: {location_id}")

    for region_id in logic_holder.spoiler.RegionList:
        region_obj = logic_holder.spoiler.RegionList[region_id]
        # Filtering out auxiliary locations is detrimental to glitch logic, but is necessary to ensure each location placed exactly once
        location_logics = [loc for loc in region_obj.locations if (not loc.isAuxiliaryLocation) or region_id.name == "FactoryBaboonBlast"]
        # V1 LIMITATION: Helm must be skip_start
        # Special exception time! The locations in HideoutHelmEntry cause more problems than they solve, and cannot exist in conjunction with other locations.
        if region_obj.level == Levels.HideoutHelm:
            # Carefully extract the duplicate Helm locations based on what Helm rooms are required per the settings.
            # If the room is required, the HideoutHelmEntry region cannot have the locations (because you'll have to reach the room to complete the barrels)
            # If the room is not required, the HideoutHelmKongRoom cannot have the locations (because they'll get completed by the Helm Entry Redirect)
            if (region_id == Regions.HideoutHelmEntry and spoiler.settings.helm_donkey) or (region_id == Regions.HideoutHelmDonkeyRoom and not spoiler.settings.helm_donkey):
                location_logics = [loc for loc in location_logics if loc.id not in (Locations.HelmDonkey1, Locations.HelmDonkey2)]
            if (region_id == Regions.HideoutHelmEntry and spoiler.settings.helm_diddy) or (region_id == Regions.HideoutHelmDiddyRoom and not spoiler.settings.helm_diddy):
                location_logics = [loc for loc in location_logics if loc.id not in (Locations.HelmDiddy1, Locations.HelmDiddy2)]
            if (region_id == Regions.HideoutHelmEntry and spoiler.settings.helm_lanky) or (region_id == Regions.HideoutHelmLankyRoom and not spoiler.settings.helm_lanky):
                location_logics = [loc for loc in location_logics if loc.id not in (Locations.HelmLanky1, Locations.HelmLanky2)]
            if (region_id == Regions.HideoutHelmEntry and spoiler.settings.helm_tiny) or (region_id == Regions.HideoutHelmTinyRoom and not spoiler.settings.helm_tiny):
                location_logics = [loc for loc in location_logics if loc.id not in (Locations.HelmTiny1, Locations.HelmTiny2)]
            if (region_id == Regions.HideoutHelmEntry and spoiler.settings.helm_chunky) or (region_id == Regions.HideoutHelmChunkyRoom and not spoiler.settings.helm_chunky):
                location_logics = [loc for loc in location_logics if loc.id not in (Locations.HelmChunky1, Locations.HelmChunky2)]
        collectibles = []
        # Use spoiler.CollectibleRegions which reflects CB randomization if enabled
        if region_id in logic_holder.spoiler.CollectibleRegions.keys():
            collectible_types = [Collectibles.bunch, Collectibles.banana, Collectibles.balloon]
            collectible_types.append(Collectibles.coin)
            collectibles = [col for col in logic_holder.spoiler.CollectibleRegions[region_id] if col.type in collectible_types]
        events = [event for event in region_obj.events]

        # if region_obj.level == Levels.Shops:
        #     multiworld.regions.append(create_shop_region(multiworld, player, region_id.name, region_obj, location_logics, spoiler.settings, all_locations_dynamic))
        # else:
        multiworld.regions.append(create_region(multiworld, player, region_id.name, region_obj.level, location_logics, collectibles, events, logic_holder, all_locations_dynamic))


def create_region(
    multiworld: MultiWorld,
    player: int,
    region_name: str,
    level: Levels,
    location_logics: typing.List[LocationLogic],
    collectibles: typing.List[Collectible],
    events: typing.List[Event],
    logic_holder: LogicVarHolder,
    all_locations_dynamic: typing.Dict[str, int],
) -> Region:
    """Create a region for the given player's world."""
    new_region = Region(region_name, player, multiworld)

    # Check if minimal logic is enabled
    from randomizer.Enums.Settings import LogicType

    minimal_logic = logic_holder.settings.logic_type == LogicType.minimal

    # Two special cases - GameStart doesn't need any locations, as AP will handle starting items instead
    if location_logics and region_name != "GameStart":
        # And Isles Medals locations aren't real unless the setting is enabled.
        if region_name == "DKIslesMedals" and not IsItemSelected(logic_holder.settings.cb_rando_enabled, logic_holder.settings.cb_rando_list_selected, Levels.DKIsles):
            location_logics = []
        for location_logic in location_logics:
            location_obj = logic_holder.spoiler.LocationList[location_logic.id]

            # Check if this location should be skipped based on type and settings
            should_skip = False
            match location_obj.type:
                case Types.TrainingBarrel | Types.PreGivenMove:
                    should_skip = True
                case Types.Enemies:
                    if Types.Enemies not in logic_holder.settings.shuffled_location_types:
                        should_skip = True
                case Types.BoulderItem:
                    if Types.BoulderItem not in logic_holder.settings.shuffled_location_types:
                        should_skip = True
                case Types.Shop:
                    if location_obj.kong == Kongs.any:
                        if location_logic.id not in logic_holder.available_shared_shops:
                            should_skip = True
                    else:
                        vendor_level_key = (location_obj.level, location_obj.vendor)
                        if vendor_level_key in logic_holder.shared_shop_vendors:
                            should_skip = True
                case Types.EnemyPhoto:
                    if logic_holder.settings.win_condition_item != WinConditionComplex.krem_kapture:
                        should_skip = True
                case Types.Hint:
                    if Types.Hint not in logic_holder.settings.shuffled_location_types:
                        should_skip = True

            # DK Arcade Round 1 is dependent on a setting
            if location_logic.id == Locations.FactoryDonkeyDKArcade:
                if logic_holder.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and region_name == "FactoryArcadeTunnel":
                    should_skip = True
                elif not logic_holder.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and region_name == "FactoryBaboonBlast":
                    should_skip = True

            # Skip locations marked as inaccessible by smaller shops
            if hasattr(location_obj, "smallerShopsInaccessible") and location_obj.smallerShopsInaccessible and logic_holder.settings.smaller_shops:
                should_skip = True

            # Universal Tracker: don't add this location if it has no item
            if hasattr(multiworld, "generation_is_fake"):
                if hasattr(multiworld, "re_gen_passthrough"):
                    if "Donkey Kong 64" in multiworld.re_gen_passthrough:
                        if location_obj.name in multiworld.re_gen_passthrough["Donkey Kong 64"]["JunkedLocations"]:
                            should_skip = True

            if should_skip:
                continue

            loc_id = all_locations_dynamic.get(location_obj.name, 0)

            location = DK64Location(player, location_obj.name, loc_id, new_region)
            # If the location is not shuffled, lock in the default item on the location
            if location_logic.id != Locations.BananaHoard and location_obj.type not in logic_holder.settings.shuffled_location_types and location_obj.default is not None:
                location.address = None
                location.place_locked_item(DK64Item(DK64RItem.ItemList[location_obj.default].name, ItemClassification.progression_skip_balancing, None, player))
            # Otherwise, this is a location that can have items in it, and counts towards the number of locations available for items
            else:
                logic_holder.settings.location_pool_size += 1
            # Quickly test and see if we can reach this location with zero items
            quick_success = False
            try:
                quick_success = not location_logic.bonusBarrel and location.logic(logic_holder)
            except Exception:
                pass
            # If we can, we can greatly simplify the logic at this location
            # For minimal logic, all locations are accessible
            if minimal_logic or quick_success:
                set_rule(location, lambda state: True)
            # Otherwise we have to work our way through the logic proper
            else:
                set_rule(location, lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic))
            # Our Fill checks for Shockwave independent of the location's logic, so we must do the same
            # Skip for minimal logic
            if not minimal_logic and location_obj.type == Types.RainbowCoin:
                add_rule(location, lambda state: state.has("Shockwave", player))

            # Add bonus barrel completion logic
            if not minimal_logic:
                match location_logic.bonusBarrel:
                    case MinigameType.BonusBarrel:
                        if not logic_holder.settings.bonus_barrel_auto_complete:
                            add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))
                    case MinigameType.HelmBarrelFirst:
                        if logic_holder.settings.helm_room_bonus_count > 0:
                            add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))
                    case MinigameType.HelmBarrelSecond:
                        if logic_holder.settings.helm_room_bonus_count == 2:
                            add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))

            # Create bonus token location if needed
            if logic_holder.settings.win_condition_item in (WinConditionComplex.req_bonuses, WinConditionComplex.krools_challenge):
                should_create_token = False
                match location_logic.bonusBarrel:
                    case MinigameType.BonusBarrel:
                        should_create_token = True
                    case MinigameType.HelmBarrelFirst:
                        if logic_holder.settings.helm_room_bonus_count > 0:
                            should_create_token = True
                    case MinigameType.HelmBarrelSecond:
                        if logic_holder.settings.helm_room_bonus_count == 2:
                            should_create_token = True

                if should_create_token:
                    token_location = DK64Location(player, location_obj.name + " Token", None, new_region)
                    if minimal_logic:
                        set_rule(token_location, lambda state: True)
                    else:
                        set_rule(
                            token_location,
                            lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic) and canDoBonusBarrel(state, player, location_logic),
                        )
                    token_location.place_locked_item(DK64Item("Bonus Completed", ItemClassification.progression_skip_balancing, None, player))
                    new_region.locations.append(token_location)

            # Apply item placement restrictions based on location type
            match location_obj.type:
                case Types.Key | Types.Crown:
                    add_item_rule(location, lambda item: not (item.player == player and "Junk" in item.name))
                case Types.Shop:
                    add_item_rule(location, lambda item: not (item.player == player and item.name in ["Cranky", "Funky", "Candy", "Snide", "Rainbow Coin"]))
                case Types.Fairy:
                    add_item_rule(location, lambda item: not (item.player == player and "Blueprint" in item.name))

            # Add boss defeated token if needed
            if location_obj.type == Types.Key and logic_holder.settings.win_condition_item in (WinConditionComplex.req_bosses, WinConditionComplex.krools_challenge):
                token_location = DK64Location(player, location_obj.name + " Token", None, new_region)
                set_rule(token_location, lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic))
                token_location.place_locked_item(DK64Item("Boss Defeated", ItemClassification.progression_skip_balancing, None, player))
                new_region.locations.append(token_location)
            new_region.locations.append(location)
            # print("Adding location: " + location.name + " | " + str(loc_id))

    collectible_id = 0
    for collectible in collectibles:
        collectible_id += 1
        location_name = region_name + " Collectible " + str(collectible_id) + ": " + collectible.kong.name + " " + collectible.type.name
        location = DK64Location(player, location_name, None, new_region)
        # Quickly test and see if we can reach this location with zero items
        quick_success = False
        try:
            quick_success = collectible.logic(logic_holder)
        except Exception:
            pass
        # If we can, we can greatly simplify the logic at this location
        # For minimal logic, all collectibles are accessible
        if minimal_logic or quick_success:
            set_rule(location, lambda state: True)
        else:
            set_rule(location, lambda state, player=player, collectible=collectible: hasDK64RCollectible(state, player, collectible))
        # Skip kong requirements for minimal logic
        if not minimal_logic:
            kong_name = name_for_kong[collectible.kong]
            add_rule(location, lambda state, kong_name=kong_name: state.has(kong_name, player))
        quantity = collectible.amount
        if collectible.type == Collectibles.bunch:
            quantity *= 5
        elif collectible.type == Collectibles.balloon:
            quantity *= 10
            # Skip gun requirements for minimal logic
            if not minimal_logic:
                add_rule(location, lambda state, collectible_kong=collectible.kong: state.has(gun_for_kong[collectible_kong], player))  # We need to be sure we check for gun access for this balloon
        if collectible.type == Collectibles.coin:
            location.place_locked_item(DK64Item("Collectible Coins, " + collectible.kong.name + ", " + str(quantity), ItemClassification.progression_skip_balancing, None, player))
        else:
            location.place_locked_item(DK64Item("Collectible CBs, " + collectible.kong.name + ", " + level.name + ", " + str(quantity), ItemClassification.progression_skip_balancing, None, player))
        new_region.locations.append(location)

    for event in events:
        # Check if this event should be skipped based on settings and region
        should_skip_event = False

        # Some events don't matter due to Archipelago settings
        if region_name == "GameStart":
            if event.name in (Events.Night, Events.Day):
                # Only skip these events if time items are NOT shuffled and the logic fails
                # If time items ARE shuffled, we need to keep the events even if not immediately accessible
                if Types.FungiTime not in logic_holder.settings.shuffled_location_types and not event.logic(logic_holder):
                    should_skip_event = True

            # Filter out barrier events that won't be used
            match event.name:
                case Events.AztecIceMelted:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.aztec_tiny_temple_ice):
                        should_skip_event = True
                case Events.MainCoreActivated:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.factory_production_room):
                        should_skip_event = True
                case Events.TestingGateOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.factory_testing_gate):
                        should_skip_event = True
                case Events.LighthouseGateOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.galleon_lighthouse_gate):
                        should_skip_event = True
                case Events.ShipyardGateOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.galleon_shipyard_area_gate):
                        should_skip_event = True
                case Events.ActivatedLighthouse:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.galleon_seasick_ship):
                        should_skip_event = True
                case Events.ShipyardTreasureRoomOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.galleon_treasure_room):
                        should_skip_event = True
                case Events.WormGatesOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.forest_green_tunnel):
                        should_skip_event = True
                case Events.HollowTreeGateOpened:
                    if not logic_holder.checkBarrier(RemovedBarriersSelected.forest_yellow_tunnel):
                        should_skip_event = True

        # Remove duplicate events for barriers that are pre-opened
        if region_name != "GameStart":
            match event.name:
                case Events.AztecIceMelted:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.aztec_tiny_temple_ice):
                        should_skip_event = True
                case Events.MainCoreActivated:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.factory_production_room):
                        should_skip_event = True
                case Events.TestingGateOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.factory_testing_gate):
                        should_skip_event = True
                case Events.LighthouseGateOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.galleon_lighthouse_gate):
                        should_skip_event = True
                case Events.ShipyardGateOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.galleon_shipyard_area_gate):
                        should_skip_event = True
                case Events.ActivatedLighthouse:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.galleon_seasick_ship):
                        should_skip_event = True
                case Events.ShipyardTreasureRoomOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.galleon_treasure_room):
                        should_skip_event = True
                case Events.WormGatesOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.forest_green_tunnel):
                        should_skip_event = True
                case Events.HollowTreeGateOpened:
                    if logic_holder.checkBarrier(RemovedBarriersSelected.forest_yellow_tunnel):
                        should_skip_event = True

        # Water level altering events
        if event.name in (Events.WaterLowered, Events.WaterRaised):
            from randomizer.Enums.Settings import GalleonWaterSetting

            if region_name == "GloomyGalleonStart":
                if event.name == Events.WaterLowered and logic_holder.settings.galleon_water_internal == GalleonWaterSetting.lowered:
                    pass  # Allow this event
                elif event.name == Events.WaterRaised and logic_holder.settings.galleon_water_internal == GalleonWaterSetting.raised:
                    pass  # Allow this event
                else:
                    should_skip_event = True
            elif region_name == "LighthouseUnderwater":
                if event.name == Events.WaterRaised and logic_holder.settings.galleon_water_internal == GalleonWaterSetting.lowered:
                    pass  # Allow switching to raised
                elif event.name == Events.WaterLowered and logic_holder.settings.galleon_water_internal == GalleonWaterSetting.raised:
                    pass  # Allow switching to lowered
                else:
                    should_skip_event = True
            else:
                should_skip_event = True

        # This event only matters if you enter galleon via the Treasure Room and it spawns open
        if event.name == Events.ShipyardTreasureRoomOpened and region_name == "TreasureRoom":
            if not event.logic(logic_holder):
                should_skip_event = True

        # This HelmFinished event is only necessary for skip all Helm
        if event.name == Events.HelmFinished and region_name == "HideoutHelmEntry" and logic_holder.settings.helm_setting != HelmSetting.skip_all:
            should_skip_event = True

        # Helm barrier deduplication
        if event.name == Events.HelmDoorsOpened:
            if region_name == "HideoutHelmEntry" and not logic_holder.checkBarrier(RemovedBarriersSelected.helm_star_gates):
                should_skip_event = True
            elif region_name == "HideoutHelmMain" and logic_holder.checkBarrier(RemovedBarriersSelected.helm_star_gates):
                should_skip_event = True

        if event.name == Events.HelmGatesPunched:
            if region_name == "HideoutHelmEntry" and not logic_holder.checkBarrier(RemovedBarriersSelected.helm_punch_gates):
                should_skip_event = True
            elif region_name == "HideoutHelmMain" and logic_holder.checkBarrier(RemovedBarriersSelected.helm_punch_gates):
                should_skip_event = True

        if should_skip_event:
            continue

        location_name = region_name + " Event " + event.name.name
        location = DK64Location(player, location_name, None, new_region)
        # Quickly test and see if we can reach this location with zero items
        quick_success = False
        try:
            quick_success = event.logic(logic_holder)
        except Exception:
            pass
        # If we can, we can greatly simplify the logic at this location
        # For minimal logic, all events are accessible
        if minimal_logic or quick_success:
            set_rule(location, lambda state: True)
        else:
            set_rule(location, lambda state, player=player, event=event: hasDK64REvent(state, player, event))
        location.place_locked_item(DK64Item("Event, " + event.name.name, ItemClassification.progression_skip_balancing, None, player))
        new_region.locations.append(location)

    return new_region


# CURRENTLY UNUSED - for some reason some Lanky shops are inaccessible??
def create_shop_region(
    multiworld: MultiWorld, player: int, region_name: str, region_obj: DK64Region, location_logics: typing.List[LocationLogic], settings: Settings, all_locations_dynamic: typing.Dict[str, int]
) -> Region:
    """Create a region for the given player's world."""
    # Shop regions have relatively straightforward logic that can be streamlined for performance purposes
    new_region = Region(region_name, player, multiworld)
    # Snide and his blueprint locations are one-to-one every time
    if "Snide" in region_name:
        for _ in range(8):
            for kong in range(5):
                blueprint_obj = DK64RItem.ItemList[Items.DonkeyBlueprint + kong]
                location_name = "Turn In " + blueprint_obj.name
                loc_id = all_locations_dynamic.get(location_name, 0)
                location = DK64Location(player, location_name, loc_id, new_region)
                set_rule(location, lambda state, blueprint_name=blueprint_obj.name: state.has(blueprint_name, player))
                location.place_locked_item(DK64Item(blueprint_obj.name, ItemClassification.progression_skip_balancing, None, player))
                new_region.locations.append(location)
    # The one special child here is Cranky Generic, home of Jetpac, the only shop location with any relevant logic
    elif region_name == "Cranky Generic":
        location = DK64Location(player, "Jetpac", all_locations_dynamic.get("Jetpac", 0), new_region)
        set_rule(location, lambda state, player=player, location_logic=location_logics[0]: hasDK64RLocation(state, player, location_logic))
        new_region.locations.append(location)
        settings.location_pool_size += 1
    # All other shops are free because we are *not* touching shop logic with a 20000000000 ft pole (yet)
    else:
        for location_logic in location_logics:
            location_obj = DK64RLocation.LocationListOriginal[location_logic.id]
            if location_obj.kong == Kongs.any:
                continue  # We need to eliminate shared shop locations so shops don't have both a shared item and Kong items
            loc_id = all_locations_dynamic.get(location_obj.name, 0)
            location = DK64Location(player, location_obj.name, loc_id, new_region)
            required_kong_name = location_obj.kong.name.title()
            set_rule(location, lambda state, required_kong_name=required_kong_name: state.has(required_kong_name, player))
            new_region.locations.append(location)
            settings.location_pool_size += 1

    return new_region


def connect_regions(world: World, settings: Settings, spoiler: Spoiler = None):
    """Connect the regions in the given world."""
    connect(world, "Menu", "GameStart")

    # For minimal logic, connect all regions without any logic requirements
    from randomizer.Enums.Settings import LogicType

    if settings.logic_type == LogicType.minimal:
        # Connect all regions with no requirements for minimal logic
        for region_id, region_obj in all_logic_regions.items():
            for exit in region_obj.exits:
                destination_name = exit.dest.name
                try:
                    connect(world, region_id.name, destination_name, lambda state: True)
                except Exception:
                    # Region connection may already exist or have other issues, skip it
                    pass
        # Pre-activated Isles warps for V1
        connect(world, "IslesMain", "IslesMainUpper", lambda state: True)
        connect(world, "IslesMain", "KremIsleBeyondLift", lambda state: True)
        return

    # Build lobby transition mapping for level order shuffling
    lobby_transition_mapping = None
    if settings.level_randomization == LevelRandomization.level_order_complex:
        lobby_transition_mapping = {}
        enter_lobby_transitions = {
            Transitions.IslesMainToJapesLobby: None,
            Transitions.IslesMainToAztecLobby: None,
            Transitions.IslesMainToFactoryLobby: None,
            Transitions.IslesMainToGalleonLobby: None,
            Transitions.IslesMainToForestLobby: None,
            Transitions.IslesMainToCavesLobby: None,
            Transitions.IslesMainToCastleLobby: None,
            Transitions.IslesMainToHelmLobby: None,
        }
        exit_lobby_transitions = {
            Transitions.IslesJapesLobbyToMain: None,
            Transitions.IslesAztecLobbyToMain: None,
            Transitions.IslesFactoryLobbyToMain: None,
            Transitions.IslesGalleonLobbyToMain: None,
            Transitions.IslesForestLobbyToMain: None,
            Transitions.IslesCavesLobbyToMain: None,
            Transitions.IslesCastleLobbyToMain: None,
            Transitions.IslesHelmLobbyToMain: None,
        }
        #     # Identify which regions each lobby transition leads to in vanilla - this is as un-hard-coded as I can make it
        for region_id, region_obj in DKIsles.LogicRegions.items():
            for exit in region_obj.exits:
                if exit.exitShuffleId in enter_lobby_transitions and not exit.isGlitchTransition:
                    enter_lobby_transitions[exit.exitShuffleId] = exit.dest.name
                if exit.exitShuffleId in exit_lobby_transitions and not exit.isGlitchTransition:
                    exit_lobby_transitions[exit.exitShuffleId] = exit.dest.name
        # Now we can map the transitions to the shuffled level order
        enter_lobby_transitions_list = list(enter_lobby_transitions.keys())
        exit_lobby_transitions_list = list(exit_lobby_transitions.keys())
        for i in range(len(settings.level_order)):
            level = settings.level_order[i + 1]
            lobby_transition_mapping[enter_lobby_transitions_list[i]] = enter_lobby_transitions[enter_lobby_transitions_list[level]]
            lobby_transition_mapping[exit_lobby_transitions_list[level]] = exit_lobby_transitions[exit_lobby_transitions_list[i]]

    # Get entrance randomization pairings if available
    pairings = None
    if hasattr(world.multiworld, "generation_is_fake"):
        if hasattr(world.multiworld, "re_gen_passthrough") and settings.level_randomization == LevelRandomization.loadingzone:
            entrance_rando_data = world.multiworld.re_gen_passthrough["Donkey Kong 64"].get("EntranceRando", {})
            if entrance_rando_data:
                pairings = dict(entrance_rando_data)

    # Connect all region exits
    for region_id, region_obj in all_logic_regions.items():
        # Check if we should use modified region from spoiler
        use_modified = False
        if spoiler:
            # Random starting region modifies GameStart's exits
            if region_id == Regions.GameStart and hasattr(settings, "starting_region") and settings.starting_region:
                use_modified = True
            # DK Portal location rando modifies entry handler exits
            elif settings.dk_portal_location_rando_v2 != DKPortalRando.off:
                entry_handler_regions = {
                    Regions.JungleJapesEntryHandler,
                    Regions.AngryAztecEntryHandler,
                    Regions.FranticFactoryEntryHandler,
                    Regions.GloomyGalleonEntryHandler,
                    Regions.FungiForestEntryHandler,
                    Regions.CrystalCavesEntryHandler,
                    Regions.CreepyCastleEntryHandler,
                }
                if region_id in entry_handler_regions:
                    use_modified = True

        if use_modified:
            region_obj = spoiler.RegionList[region_id]

        for exit in region_obj.exits:
            # Test exit logic
            quick_success = False
            try:
                quick_success = exit.logic(None)
            except Exception:
                pass

            if quick_success:
                converted_logic = lambda state: True
            else:
                converted_logic = lambda state, player=world.player, exit=exit: hasDK64RTransition(state, player, exit)

            # Add time requirements if this transition has time restrictions
            if world.options.time_of_day:
                if exit.time == Time.Day:
                    original_logic = converted_logic
                    converted_logic = lambda state, orig=original_logic: orig(state) and state.has("Day", world.player)
                elif exit.time == Time.Night:
                    original_logic = converted_logic
                    converted_logic = lambda state, orig=original_logic: orig(state) and state.has("Night", world.player)

            # Determine connection type and targets
            destination_name = exit.dest.name
            entrance_name = None

            # Handle level order shuffling
            if settings.level_randomization == LevelRandomization.level_order_complex:
                if lobby_transition_mapping and exit.exitShuffleId in lobby_transition_mapping:
                    destination_name = lobby_transition_mapping[exit.exitShuffleId]

            # Check for loading zone randomization
            if settings.level_randomization == LevelRandomization.loadingzone:
                if exit.exitShuffleId and not exit.isGlitchTransition and ShufflableExits[exit.exitShuffleId].back.reverse:
                    # Skip Helm transitions if Helm location is not being shuffled
                    helm_transitions = {
                        Transitions.IslesMainToHelmLobby,
                        Transitions.IslesHelmLobbyToMain,
                        Transitions.IslesToHelm,
                        Transitions.HelmToIsles,
                    }
                    if not settings.shuffle_helm_location and exit.exitShuffleId in helm_transitions:
                        entrance_name = None
                    else:
                        entrance_name = ShufflableExits[exit.exitShuffleId].name

            # Determine connection type and handle the connection
            try:
                if pairings and entrance_name:
                    if entrance_name in pairings:
                        # Paired - connect to paired target from entrance randomization
                        target_entrance_name = pairings[entrance_name]
                        target_shufflable_exit = None
                        for transition_enum, shufflable_exit in ShufflableExits.items():
                            if shufflable_exit.name == target_entrance_name:
                                target_shufflable_exit = shufflable_exit
                                break

                        if target_shufflable_exit:
                            target_region_name = target_shufflable_exit.region.name
                            connect(world, region_id.name, target_region_name, converted_logic, entrance_name)
                        else:
                            # Fallback to normal connection
                            connection = connect(world, region_id.name, destination_name, converted_logic, entrance_name)
                            if entrance_name is not None:
                                disconnect_entrance_for_randomization(connection)
                    else:
                        # Unpaired - entrance should be shuffled but no pairing found
                        connection = connect(world, region_id.name, destination_name, converted_logic, entrance_name)
                        disconnect_entrance_for_randomization(connection)
                elif settings.level_randomization == LevelRandomization.loadingzone and exit.isGlitchTransition:
                    # Skip glitch transitions during LZR
                    pass
                else:
                    # Normal connection (may or may not be shufflable)
                    connection = connect(world, region_id.name, destination_name, converted_logic, entrance_name)
                    if entrance_name is not None:
                        disconnect_entrance_for_randomization(connection)
            except Exception:
                pass

    # Pre-activated Isles warps
    connect(world, "IslesMain", "IslesMainUpper", lambda state: True)
    connect(world, "IslesMain", "KremIsleBeyondLift", lambda state: True)

    # Random starting region exit connection
    if spoiler and hasattr(settings, "starting_region") and settings.starting_region:
        starting_region_id = settings.starting_region.get("region")
        if starting_region_id is not None:
            starting_region_obj = all_logic_regions.get(starting_region_id)
            if starting_region_obj:
                starting_level = starting_region_obj.level
                level_exit_transitions = {
                    Levels.JungleJapes: Transitions.JapesToIsles,
                    Levels.AngryAztec: Transitions.AztecToIsles,
                    Levels.FranticFactory: Transitions.FactoryToIsles,
                    Levels.GloomyGalleon: Transitions.GalleonToIsles,
                    Levels.FungiForest: Transitions.ForestToIsles,
                    Levels.CrystalCaves: Transitions.CavesToIsles,
                    Levels.CreepyCastle: Transitions.CastleToIsles,
                }

                # Only create exit level connection for non-Isles levels
                if starting_level in level_exit_transitions:
                    exit_transition_id = level_exit_transitions[starting_level]
                    starting_region_name = starting_region_id.name if hasattr(starting_region_id, "name") else str(starting_region_id)

                    level_to_entry_handler = {
                        Levels.JungleJapes: Regions.JungleJapesEntryHandler,
                        Levels.AngryAztec: Regions.AngryAztecEntryHandler,
                        Levels.FranticFactory: Regions.FranticFactoryEntryHandler,
                        Levels.GloomyGalleon: Regions.GloomyGalleonEntryHandler,
                        Levels.FungiForest: Regions.FungiForestEntryHandler,
                        Levels.CrystalCaves: Regions.CrystalCavesEntryHandler,
                        Levels.CreepyCastle: Regions.CreepyCastleEntryHandler,
                    }
                    if starting_level in level_to_entry_handler:
                        entry_handler_region = level_to_entry_handler[starting_level]
                        entry_handler_obj = all_logic_regions.get(entry_handler_region)

                        if entry_handler_obj:
                            # Find the exit transition in the entry handler's exits
                            exit_transition = None
                            for exit in entry_handler_obj.exits:
                                if exit.exitShuffleId == exit_transition_id:
                                    exit_transition = exit
                                    break

                            # Create connection using the exit transition's logic
                            if exit_transition:
                                target_region_name = exit_transition.dest.name
                                connect(
                                    world,
                                    starting_region_name,
                                    target_region_name,
                                    lambda state, player=world.player, exit=exit_transition: hasDK64RTransition(state, player, exit),
                                    "Exit Level from spawn: " + starting_region_name,
                                )

    # Loading zone randomization special connections
    if pairings:
        # Handle deathwarps
        for region_id, region_obj in all_logic_regions.items():
            if region_obj.deathwarp:
                connect(
                    world,
                    region_id.name,
                    region_obj.deathwarp.dest.name,
                    lambda state, player=world.player, exit=region_obj.deathwarp: hasDK64RTransition(state, player, exit),
                    "Deathwarp: " + region_id.name + "->" + region_obj.deathwarp.dest.name,
                )

        # Handle exit level connections
        exit_level_transition_dict = {
            Levels.JungleJapes: ShufflableExits[Transitions.JapesToIsles].name,
            Levels.AngryAztec: ShufflableExits[Transitions.AztecToIsles].name,
            Levels.FranticFactory: ShufflableExits[Transitions.FactoryToIsles].name,
            Levels.GloomyGalleon: ShufflableExits[Transitions.GalleonToIsles].name,
            Levels.FungiForest: ShufflableExits[Transitions.ForestToIsles].name,
            Levels.CrystalCaves: ShufflableExits[Transitions.CavesToIsles].name,
            Levels.CreepyCastle: ShufflableExits[Transitions.CastleToIsles].name,
        }

        # For each level, find where its exit leads using the pairings
        for level, exit_entrance_name in exit_level_transition_dict.items():
            if exit_entrance_name in pairings:
                target_entrance_name = pairings[exit_entrance_name]
                # Look up the target entrance to get its region
                target_shufflable_exit = None
                for transition_enum, shufflable_exit in ShufflableExits.items():
                    if shufflable_exit.name == target_entrance_name:
                        target_shufflable_exit = shufflable_exit
                        break

                if target_shufflable_exit:
                    target_region_name = target_shufflable_exit.region.name
                    # Connect all regions of this level that can exit to the target
                    for region_id, region_obj in all_logic_regions.items():
                        if not region_obj.restart and region_obj.level == level:
                            connect(world, region_id.name, target_region_name, lambda state: True, "Exit Level: " + region_id.name + "->" + target_region_name)


def connect_glitch_transitions(world: World, er_placement_state: ERPlacementState):
    """Connect glitch transitions to the appropriate shuffled exit."""
    entrances = er_placement_state.placements

    for region_id, region_obj in all_logic_regions.items():
        for exit in [exit for exit in region_obj.exits if exit.isGlitchTransition]:
            target = next((entrance for entrance in entrances if entrance.name == ShufflableExits[exit.exitShuffleId].name), None)
            if target:
                connect(
                    world,
                    region_id.name,
                    target.connected_region.name,
                    lambda state, player=world.player, exit=exit: hasDK64RTransition(state, player, exit),
                    "Glitch: " + region_id.name + "->" + target.connected_region.name,
                )


def connect_exit_level_and_deathwarp(world: World, er_placement_state: ERPlacementState):
    """Connect exit level and deathwarp transitions."""
    entrances = er_placement_state.placements

    exit_level_transition_dict = {
        Levels.JungleJapes: ShufflableExits[Transitions.JapesToIsles].name,
        Levels.AngryAztec: ShufflableExits[Transitions.AztecToIsles].name,
        Levels.FranticFactory: ShufflableExits[Transitions.FactoryToIsles].name,
        Levels.GloomyGalleon: ShufflableExits[Transitions.GalleonToIsles].name,
        Levels.FungiForest: ShufflableExits[Transitions.ForestToIsles].name,
        Levels.CrystalCaves: ShufflableExits[Transitions.CavesToIsles].name,
        Levels.CreepyCastle: ShufflableExits[Transitions.CastleToIsles].name,
    }

    exit_level_target_dict = {key: next((entrance for entrance in entrances if entrance.name == value), None) for key, value in exit_level_transition_dict.items()}

    for region_id, region_obj in all_logic_regions.items():
        # Deathwarp
        if region_obj.deathwarp:
            connect(
                world,
                region_id.name,
                region_obj.deathwarp.dest.name,
                lambda state, player=world.player, exit=region_obj.deathwarp: hasDK64RTransition(state, player, exit),
                "Deathwarp: " + region_id.name + "->" + region_obj.deathwarp.dest.name,
            )
        # Exit level
        if not region_obj.restart and region_obj.level in exit_level_target_dict:
            connect(
                world,
                region_id.name,
                exit_level_target_dict[region_obj.level].connected_region.name,
                lambda state: True,
                "Exit Level: " + region_id.name + "->" + exit_level_target_dict[region_obj.level].connected_region.name,
            )


def connect(world: World, source: str, target: str, rule: typing.Optional[typing.Callable] = None, name: typing.Optional[str] = None) -> Entrance:
    """Connect two regions in the given world."""
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if name is None:
        name = source + "->" + target
    connection = Entrance(world.player, name, source_region, 0, EntranceType.TWO_WAY)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection


def hasDK64RTransition(state: CollectionState, player: int, exit: TransitionFront):
    """Check if the given transition is accessible in the given state."""
    logic_holder = state.dk64_logic_holder[player]

    # Check the base logic for the transition
    if not exit.logic(logic_holder):
        return False

    # Check time requirements if this transition has time restrictions
    if exit.time == Time.Day:
        return logic_holder.dayAccess
    elif exit.time == Time.Night:
        return logic_holder.nightAccess
    # Time.Both or no time restriction - always accessible if logic passes
    return True


def hasDK64RLocation(state: CollectionState, player: int, location: LocationLogic):
    """Check if the given location is accessible in the given state."""
    return location.logic(state.dk64_logic_holder[player])


def hasDK64RCollectible(state: CollectionState, player: int, collectible: Collectible):
    """Check if the given collectible is accessible in the given state."""
    return collectible.logic(state.dk64_logic_holder[player])


def hasDK64REvent(state: CollectionState, player: int, event: Event):
    """Check if the given event is accessible in the given state."""
    return event.logic(state.dk64_logic_holder[player])


def canDoBonusBarrel(state: CollectionState, player: int, location: LocationLogic):
    """Check if we can complete the bonus barrel in the given state."""
    logic_holder = state.dk64_logic_holder[player]
    barrel_data = logic_holder.spoiler.shuffled_barrel_data[location.id]
    minigame = barrel_data.minigame
    minigame_obj = MinigameRequirements[minigame]

    # Busy Barrel Barrage doesn't allow tagging inside the bonus barrel
    # We need to check if we can complete it with only the kong that enters the barrel
    if minigame in (Minigames.BusyBarrelBarrageEasy, Minigames.BusyBarrelBarrageNormal, Minigames.BusyBarrelBarrageHard):
        # We can't tag in this bonus barrel
        # The barrel_data.kong tells us which kong is required to enter this specific barrel
        required_kong = barrel_data.kong

        # Check if the required kong is even allowed in this minigame
        if required_kong not in minigame_obj.kong_list:
            return False

        # Save the current "is*" state (tag anywhere assumption)
        saved_isdonkey = logic_holder.isdonkey
        saved_isdiddy = logic_holder.isdiddy
        saved_islanky = logic_holder.islanky
        saved_istiny = logic_holder.istiny
        saved_ischunky = logic_holder.ischunky

        # Temporarily set the logic holder to be only the required kong (disable tag anywhere)
        logic_holder.isdonkey = required_kong == Kongs.donkey and logic_holder.donkey
        logic_holder.isdiddy = required_kong == Kongs.diddy and logic_holder.diddy
        logic_holder.islanky = required_kong == Kongs.lanky and logic_holder.lanky
        logic_holder.istiny = required_kong == Kongs.tiny and logic_holder.tiny
        logic_holder.ischunky = required_kong == Kongs.chunky and logic_holder.chunky

        # Check if this kong can complete the minigame
        can_complete = minigame_obj.logic(logic_holder)

        # Restore the original "is*" state
        logic_holder.isdonkey = saved_isdonkey
        logic_holder.isdiddy = saved_isdiddy
        logic_holder.islanky = saved_islanky
        logic_holder.istiny = saved_istiny
        logic_holder.ischunky = saved_ischunky

        return can_complete
    else:
        return minigame_obj.logic(logic_holder)
