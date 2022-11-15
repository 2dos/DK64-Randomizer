# fmt: off
"""Logic file for Hideout Helm."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Transitions import Transitions
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.HideoutHelmStart: Region("Hideout Helm Start", "Hideout Helm", Levels.HideoutHelm, True, None, [], [], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: True),
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.settings.helm_setting != "default" or (l.handstand and l.lanky and l.pineapple and l.chunky and l.vines and l.mini and l.tiny)),
    ]),

    Regions.HideoutHelmMain: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmBattleArena, lambda l: not l.settings.crown_placement_rando and l.jetpack and l.diddy),
        LocationLogic(Locations.HelmDonkey1, lambda l: l.settings.helm_setting == "skip_all" or (l.bongos and l.isdonkey), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDonkey2, lambda l: l.settings.helm_setting == "skip_all" or (l.bongos and l.isdonkey), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDonkeyMedal, lambda l: Events.HelmDonkeyDone in l.Events and l.bongos and l.isdonkey),
        LocationLogic(Locations.HelmChunky1, lambda l: l.settings.helm_setting == "skip_all" or (l.triangle and l.ischunky), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunky2, lambda l: l.settings.helm_setting == "skip_all" or (l.triangle and l.ischunky), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunkyMedal, lambda l: Events.HelmChunkyDone in l.Events and l.triangle and l.ischunky),
        LocationLogic(Locations.HelmTiny1, lambda l: l.settings.helm_setting == "skip_all" or (l.saxophone and l.istiny), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTiny2, lambda l: l.settings.helm_setting == "skip_all" or (l.saxophone and l.istiny), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTinyMedal, lambda l: Events.HelmTinyDone in l.Events and l.saxophone and l.istiny),
        LocationLogic(Locations.HelmLanky1, lambda l: l.settings.helm_setting == "skip_all" or (l.trombone and l.islanky), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLanky2, lambda l: l.settings.helm_setting == "skip_all" or (l.trombone and l.islanky), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLankyMedal, lambda l: Events.HelmLankyDone in l.Events and l.trombone and l.islanky),
        LocationLogic(Locations.HelmDiddy1, lambda l: l.settings.helm_setting == "skip_all" or (l.guitar and l.jetpack and l.isdiddy), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddy2, lambda l: l.settings.helm_setting == "skip_all" or (l.guitar and l.jetpack and l.isdiddy), MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddyMedal, lambda l: Events.HelmDiddyDone in l.Events and l.guitar and l.jetpack and l.isdiddy),
        LocationLogic(Locations.HelmBananaFairy1, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmBananaFairy2, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmKey, lambda l: Events.HelmKeyAccess in l.Events),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: (l.grab and l.donkey and l.jetpack and l.diddy and l.punch and l.chunky) or l.settings.helm_setting != "default"),
        Event(Events.HelmDonkeyDone, lambda l: ((l.isPriorHelmComplete(Kongs.donkey) or l.settings.helm_setting == "skip_all") and l.HelmDonkey1 and l.HelmDonkey2) or not l.settings.helm_donkey),
        Event(Events.HelmChunkyDone, lambda l: ((l.isPriorHelmComplete(Kongs.chunky) or l.settings.helm_setting == "skip_all") and l.HelmChunky1 and l.HelmChunky2) or not l.settings.helm_chunky),
        Event(Events.HelmTinyDone, lambda l: ((l.isPriorHelmComplete(Kongs.tiny) or l.settings.helm_setting == "skip_all") and l.HelmTiny1 and l.HelmTiny2) or not l.settings.helm_tiny),
        Event(Events.HelmLankyDone, lambda l: ((l.isPriorHelmComplete(Kongs.lanky) or l.settings.helm_setting == "skip_all") and l.HelmLanky1 and l.HelmLanky2) or not l.settings.helm_lanky),
        Event(Events.HelmDiddyDone, lambda l: ((l.isPriorHelmComplete(Kongs.diddy) or l.settings.helm_setting == "skip_all") and l.HelmDiddy1 and l.HelmDiddy2) or not l.settings.helm_diddy),
        Event(Events.HelmKeyAccess, lambda l: (l.settings.helm_setting == "skip_all" or (Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events
              and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events))
              and (l.settings.crown_door_open or l.BattleCrowns >= 4) and (l.settings.coin_door_open or l.nintendoCoin and l.rarewareCoin)),
    ], []),
}
