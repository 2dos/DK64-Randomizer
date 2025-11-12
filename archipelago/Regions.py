"""This file contains the logic for creating and connecting regions in the Donkey Kong 64 world."""

import typing

from BaseClasses import CollectionState, ItemClassification, MultiWorld, Region, Entrance, EntranceType, Location
from entrance_rando import disconnect_entrance_for_randomization
from worlds.AutoWorld import World

from randomizer import Spoiler
from randomizer import Settings
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Minigames import Minigames
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import HelmSetting, FungiTimeSetting, FasterChecksSelected, ShuffleLoadingZones, WinConditionComplex, LevelRandomization
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
        for region_id in all_logic_regions:
            region_obj = all_logic_regions[region_id]
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

    for region_id in all_logic_regions:
        region_obj = all_logic_regions[region_id]
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
        if region_id in all_collectible_regions.keys():
            collectible_types = [Collectibles.bunch, Collectibles.banana, Collectibles.balloon]
            collectible_types.append(Collectibles.coin)
            collectibles = [col for col in all_collectible_regions[region_id] if col.type in collectible_types]
        events = [event for event in region_obj.events]

        # if region_obj.level == Levels.Shops:
        #     multiworld.regions.append(create_shop_region(multiworld, player, region_id.name, region_obj, location_logics, spoiler.settings))
        # else:
        multiworld.regions.append(create_region(multiworld, player, region_id.name, region_obj.level, location_logics, collectibles, events, logic_holder))


def create_region(
    multiworld: MultiWorld,
    player: int,
    region_name: str,
    level: Levels,
    location_logics: typing.List[LocationLogic],
    collectibles: typing.List[Collectible],
    events: typing.List[Event],
    logic_holder: LogicVarHolder,
) -> Region:
    """Create a region for the given player's world."""
    new_region = Region(region_name, player, multiworld)

    # Two special cases - GameStart doesn't need any locations, as AP will handle starting items instead
    if location_logics and region_name != "GameStart":
        # And Isles Medals locations aren't real unless the setting is enabled.
        if region_name == "DKIslesMedals" and not IsItemSelected(logic_holder.settings.cb_rando_enabled, logic_holder.settings.cb_rando_list_selected, Levels.DKIsles):
            location_logics = []
        for location_logic in location_logics:
            location_obj = logic_holder.spoiler.LocationList[location_logic.id]
            # DK Arcade Round 1 is dependent on a setting - don't create the inaccessible location depending on that Faster Checks toggle
            if location_logic.id == Locations.FactoryDonkeyDKArcade:
                if logic_holder.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and region_name == "FactoryArcadeTunnel":
                    continue
                elif not logic_holder.checkFastCheck(FasterChecksSelected.factory_arcade_round_1) and region_name == "FactoryBaboonBlast":
                    continue
            # Starting move locations may be shuffled but their locations are not relevant ever due to item placement restrictions
            if location_obj.type in (Types.TrainingBarrel, Types.PreGivenMove):
                continue
            # Dropsanity would otherwise flood the world with irrelevant locked locations, greatly slowing seed gen
            if location_obj.type == Types.Enemies and Types.Enemies not in logic_holder.settings.shuffled_location_types:
                continue
            # Skip shared shops that are not in the available pool
            if location_obj.type == Types.Shop and location_obj.kong == Kongs.any:
                if location_logic.id not in logic_holder.available_shared_shops:
                    continue

            # Skip individual Kong shops if their vendor/level has a shared shop
            if location_obj.type == Types.Shop and location_obj.kong != Kongs.any:
                vendor_level_key = (location_obj.level, location_obj.vendor)
                if vendor_level_key in logic_holder.shared_shop_vendors:
                    continue
            # Skip enemy photos if the win condition is not Krem Kapture.
            if location_obj.type == Types.EnemyPhoto and logic_holder.settings.win_condition_item != WinConditionComplex.krem_kapture:
                continue
            # Skip hint locations if hints are not in the pool
            if location_obj.type == Types.Hint and Types.Hint not in logic_holder.settings.shuffled_location_types:
                continue
            # Skip locations marked as inaccessible by smaller shops
            if hasattr(location_obj, "smallerShopsInaccessible") and location_obj.smallerShopsInaccessible and logic_holder.settings.smaller_shops:
                continue
            loc_id = all_locations.get(location_obj.name, 0)
            # Universal Tracker: don't add this location if it has no item
            if hasattr(multiworld, "generation_is_fake"):
                if hasattr(multiworld, "re_gen_passthrough"):
                    if "Donkey Kong 64" in multiworld.re_gen_passthrough:
                        if location_obj.name in multiworld.re_gen_passthrough["Donkey Kong 64"]["JunkedLocations"]:
                            continue
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
                quick_success = location.logic(None) and not location_logic.bonusBarrel
            except Exception:
                pass
            # If we can, we can greatly simplify the logic at this location
            if quick_success:
                set_rule(location, lambda state: True)
            # Otherwise we have to work our way through the logic proper
            else:
                set_rule(location, lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic))
            # Our Fill checks for Shockwave independent of the location's logic, so we must do the same
            if location_obj.type == Types.RainbowCoin:
                add_rule(location, lambda state: state.has("Shockwave", player))
            # If this is a bonus barrel location, add logic to check that we can complete the bonus barrel.
            match location_logic.bonusBarrel:
                case MinigameType.BonusBarrel:
                    if not logic_holder.settings.bonus_barrel_auto_complete:
                        add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))
                        if logic_holder.settings.win_condition_item in (WinConditionComplex.req_bonuses, WinConditionComplex.krools_challenge):
                            token_location = DK64Location(player, location_obj.name + " Token", None, new_region)
                            set_rule(
                                token_location,
                                lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic) and canDoBonusBarrel(state, player, location_logic),
                            )
                            token_location.place_locked_item(DK64Item("Bonus Completed", ItemClassification.progression_skip_balancing, None, player))
                            new_region.locations.append(token_location)
                case MinigameType.HelmBarrelFirst:
                    if logic_holder.settings.helm_room_bonus_count > 0:
                        add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))
                        if logic_holder.settings.win_condition_item in (WinConditionComplex.req_bonuses, WinConditionComplex.krools_challenge):
                            token_location = DK64Location(player, location_obj.name + " Token", None, new_region)
                            set_rule(
                                token_location,
                                lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic) and canDoBonusBarrel(state, player, location_logic),
                            )
                            token_location.place_locked_item(DK64Item("Bonus Completed", ItemClassification.progression_skip_balancing, None, player))
                            new_region.locations.append(token_location)
                case MinigameType.HelmBarrelSecond:
                    if logic_holder.settings.helm_room_bonus_count == 2:
                        add_rule(location, lambda state, player=player, location_logic=location_logic: canDoBonusBarrel(state, player, location_logic))
                        if logic_holder.settings.win_condition_item in (WinConditionComplex.req_bonuses, WinConditionComplex.krools_challenge):
                            token_location = DK64Location(player, location_obj.name + " Token", None, new_region)
                            set_rule(
                                token_location,
                                lambda state, player=player, location_logic=location_logic: hasDK64RLocation(state, player, location_logic) and canDoBonusBarrel(state, player, location_logic),
                            )
                            token_location.place_locked_item(DK64Item("Bonus Completed", ItemClassification.progression_skip_balancing, None, player))
                            new_region.locations.append(token_location)
            # Item placement limitations! These only apply to items in your own world, as other worlds' items will be AP items, and those can be anywhere.
            # Fairy locations cannot have your own world's blueprints on them for technical reasons.
            if location_obj.type == Types.Fairy:
                add_item_rule(location, lambda item: not (item.player == player and "Blueprint" in item.name))
            # Bosses and Crowns cannot have Junk due to technical reasons
            if location_obj.type in (Types.Key, Types.Crown):
                add_item_rule(location, lambda item: not (item.player == player and "Junk" in item.name))
            # Shops cannot have shopkeepers for the time being due to funny haha display bug
            if location_obj.type == Types.Shop:
                add_item_rule(location, lambda item: not (item.player == player and item.name in ["Cranky", "Funky", "Candy", "Snide"]))
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
            quick_success = collectible.logic(None)
        except Exception:
            pass
        # If we can, we can greatly simplify the logic at this location
        if quick_success:
            set_rule(location, lambda state: True)
        else:
            set_rule(location, lambda state, player=player, collectible=collectible: hasDK64RCollectible(state, player, collectible))
        kong_name = name_for_kong[collectible.kong]
        add_rule(location, lambda state, kong_name=kong_name: state.has(kong_name, player))
        quantity = collectible.amount
        if collectible.type == Collectibles.bunch:
            quantity *= 5
        elif collectible.type == Collectibles.balloon:
            quantity *= 10
            add_rule(location, lambda state, collectible_kong=collectible.kong: state.has(gun_for_kong[collectible_kong], player))  # We need to be sure we check for gun access for this balloon
        if collectible.type == Collectibles.coin:
            location.place_locked_item(DK64Item("Collectible Coins, " + collectible.kong.name + ", " + str(quantity), ItemClassification.progression_skip_balancing, None, player))
        else:
            location.place_locked_item(DK64Item("Collectible CBs, " + collectible.kong.name + ", " + level.name + ", " + str(quantity), ItemClassification.progression_skip_balancing, None, player))
        new_region.locations.append(location)

    for event in events:
        # Some events don't matter due to Archipelago settings
        # Entering levels in weird spots can require a number of pre-completed events to be handled in Game Start
        # We need to filter out any that will return False (because they will never not return False)
        # V1 LIMITATION: We're not filtering out auto key turn ins, so that setting must be on (not really a problem for basically anyone)
        if region_name == "GameStart" and event.name in (
            Events.Night,
            Events.Day,
            Events.AztecIceMelted,
            Events.MainCoreActivated,
            Events.TestingGateOpened,
            Events.LighthouseGateOpened,
            Events.ShipyardGateOpened,
            Events.ActivatedLighthouse,
            Events.ShipyardTreasureRoomOpened,
            Events.WormGatesOpened,
            Events.HollowTreeGateOpened,
        ):
            if not event.logic(logic_holder):
                continue
        # Most water level altering events are inaccessible, only the one specifically in LighthouseUnderwater is accessible
        if event.name in (Events.WaterLowered, Events.WaterRaised) and region_name != "LighthouseUnderwater":
            continue
        # This event only matters if you enter galleon via the Treasure Room and it spawns open
        if event.name == Events.ShipyardTreasureRoomOpened and region_name == "TreasureRoom":
            if not event.logic(logic_holder):
                continue
        # This HelmFinished event is only necessary for skip all Helm
        if event.name == Events.HelmFinished and region_name == "HideoutHelmEntry" and logic_holder.settings.helm_setting != HelmSetting.skip_all:
            continue
        location_name = region_name + " Event " + event.name.name
        location = DK64Location(player, location_name, None, new_region)
        # Quickly test and see if we can reach this location with zero items
        quick_success = False
        try:
            quick_success = event.logic(None)
        except Exception:
            pass
        # If we can, we can greatly simplify the logic at this location
        if quick_success:
            set_rule(location, lambda state: True)
        else:
            set_rule(location, lambda state, player=player, event=event: hasDK64REvent(state, player, event))
        location.place_locked_item(DK64Item("Event, " + event.name.name, ItemClassification.progression_skip_balancing, None, player))
        new_region.locations.append(location)

    return new_region


# CURRENTLY UNUSED - for some reason some Lanky shops are inaccessible??
def create_shop_region(multiworld: MultiWorld, player: int, region_name: str, region_obj: DK64Region, location_logics: typing.List[LocationLogic], settings: Settings) -> Region:
    """Create a region for the given player's world."""
    # Shop regions have relatively straightforward logic that can be streamlined for performance purposes
    new_region = Region(region_name, player, multiworld)
    # Snide and his blueprint locations are one-to-one every time
    if "Snide" in region_name:
        for _ in range(8):
            for kong in range(5):
                blueprint_obj = DK64RItem.ItemList[Items.DonkeyBlueprint + kong]
                location_name = "Turn In " + blueprint_obj.name
                loc_id = all_locations.get(location_name, 0)
                location = DK64Location(player, location_name, loc_id, new_region)
                set_rule(location, lambda state, blueprint_name=blueprint_obj.name: state.has(blueprint_name, player))
                location.place_locked_item(DK64Item(blueprint_obj.name, ItemClassification.progression_skip_balancing, None, player))
                new_region.locations.append(location)
    # The one special child here is Cranky Generic, home of Jetpac, the only shop location with any relevant logic
    elif region_name == "Cranky Generic":
        location = DK64Location(player, "Jetpac", all_locations.get("Jetpac", 0), new_region)
        set_rule(location, lambda state, player=player, location_logic=location_logics[0]: hasDK64RLocation(state, player, location_logic))
        new_region.locations.append(location)
        settings.location_pool_size += 1
    # All other shops are free because we are *not* touching shop logic with a 20000000000 ft pole (yet)
    else:
        for location_logic in location_logics:
            location_obj = DK64RLocation.LocationListOriginal[location_logic.id]
            if location_obj.kong == Kongs.any:
                continue  # We need to eliminate shared shop locations so shops don't have both a shared item and Kong items
            loc_id = all_locations.get(location_obj.name, 0)
            location = DK64Location(player, location_obj.name, loc_id, new_region)
            required_kong_name = location_obj.kong.name.title()
            set_rule(location, lambda state, required_kong_name=required_kong_name: state.has(required_kong_name, player))
            new_region.locations.append(location)
            settings.location_pool_size += 1

    return new_region


def connect_regions(world: World, settings: Settings):
    """Connect the regions in the given world."""
    connect(world, "Menu", "GameStart")

    # # Example Region Connection
    # connect(
    #     world,
    #     "DK Isles",
    #     "Test",
    #     lambda state: state.has(DK64RItem.ItemList[DK64RItems.GoldenBanana].name, world.player, 2),
    # )

    # Shuffling level order should be going off of our ShufflableExits dictionary, but that's not properly isolated to the spoiler object yet.
    # For now, we have to pre-calculate what the destination region is for each of these transitions.
    # if settings.shuffle_loading_zones == ShuffleLoadingZones.levels:
    #     lobby_transition_mapping = {}
    #     enter_lobby_transitions = {
    #         Transitions.IslesMainToJapesLobby: None,
    #         Transitions.IslesMainToAztecLobby: None,
    #         Transitions.IslesMainToFactoryLobby: None,
    #         Transitions.IslesMainToGalleonLobby: None,
    #         Transitions.IslesMainToForestLobby: None,
    #         Transitions.IslesMainToCavesLobby: None,
    #         Transitions.IslesMainToCastleLobby: None,
    #         Transitions.IslesMainToHelmLobby: None,
    #     }
    #     exit_lobby_transitions = {
    #         Transitions.IslesJapesLobbyToMain: None,
    #         Transitions.IslesAztecLobbyToMain: None,
    #         Transitions.IslesFactoryLobbyToMain: None,
    #         Transitions.IslesGalleonLobbyToMain: None,
    #         Transitions.IslesForestLobbyToMain: None,
    #         Transitions.IslesCavesLobbyToMain: None,
    #         Transitions.IslesCastleLobbyToMain: None,
    #         Transitions.IslesHelmLobbyToMain: None,
    #     }
    #     # Identify which regions each lobby transition leads to in vanilla - this is as un-hard-coded as I can make it
    #     for region_id, region_obj in DKIsles.LogicRegions.items():
    #         for exit in region_obj.exits:
    #             if exit.exitShuffleId in enter_lobby_transitions and not exit.isGlitchTransition:
    #                 enter_lobby_transitions[exit.exitShuffleId] = exit.dest.name
    #             if exit.exitShuffleId in exit_lobby_transitions and not exit.isGlitchTransition:
    #                 exit_lobby_transitions[exit.exitShuffleId] = exit.dest.name
    #     # Now we can map the transitions to the shuffled level order
    #     enter_lobby_transitions_list = list(enter_lobby_transitions.keys())
    #     exit_lobby_transitions_list = list(exit_lobby_transitions.keys())
    #     for i in range(len(settings.level_order)):
    #         level = settings.level_order[i + 1]
    #         lobby_transition_mapping[enter_lobby_transitions_list[i]] = enter_lobby_transitions[enter_lobby_transitions_list[level]]
    #         lobby_transition_mapping[exit_lobby_transitions_list[level]] = exit_lobby_transitions[exit_lobby_transitions_list[i]]

    for region_id, region_obj in all_logic_regions.items():
        if region_id == Regions.HideoutHelmEntry:
            print(region_id)
        for exit in region_obj.exits:
            destination_name = exit.dest.name
            if region_id == Regions.HideoutHelmEntry:
                print(destination_name)
            # If this is a Isles <-> Lobby transition and we're shuffling levels, respect the dictionary built earlier
            # if settings.shuffle_loading_zones == ShuffleLoadingZones.levels and exit.exitShuffleId in lobby_transition_mapping.keys():
            #     destination_name = lobby_transition_mapping[exit.exitShuffleId]
            try:
                # Quickly test and see if we can pass this exit with zero items
                quick_success = False
                try:
                    quick_success = exit.logic(None)
                except Exception:
                    pass
                # If we can, we can greatly simplify the logic for this exit
                if quick_success:
                    converted_logic = lambda state: True
                else:
                    converted_logic = lambda state, player=world.player, exit=exit: hasDK64RTransition(state, player, exit)
                connection = connect(world, region_id.name, destination_name, converted_logic)
                if settings.level_randomization == LevelRandomization.loadingzone:
                    if exit.exitShuffleId and not exit.isGlitchTransition and ShufflableExits[exit.exitShuffleId].back.reverse:
                        disconnect_entrance_for_randomization(connection)
                # print("Connecting " + region_id.name + " to " + destination_name)
            except Exception as e:
                pass

    # V1 LIMITATION: We have pre-activated Isles warps, so we need to make two extra connections to make sure the logic is correct
    connect(world, "IslesMain", "IslesMainUpper", lambda state: True)  # Pre-activated W2
    connect(world, "IslesMain", "KremIsleBeyondLift", lambda state: True)  # Pre-activated W4

    pass


def connect(world: World, source: str, target: str, rule: typing.Optional[typing.Callable] = None) -> Entrance:
    """Connect two regions in the given world."""
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    name = source + "->" + target
    connection = Entrance(world.player, name, source_region, 0, EntranceType.TWO_WAY)

    if rule:
        connection.access_rule = rule

    source_region.exits.append(connection)
    connection.connect(target_region)
    return connection


def hasDK64RTransition(state: CollectionState, player: int, exit: TransitionFront):
    """Check if the given transition is accessible in the given state."""
    return exit.logic(state.dk64_logic_holder[player])


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
    return MinigameRequirements[state.dk64_logic_holder[player].spoiler.shuffled_barrel_data[location.id].minigame].logic(state.dk64_logic_holder[player])
