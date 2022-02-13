# fmt: off
"""Logic file for Hideout Helm."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, TransitionFront, LocationLogic, Region

LogicRegions = {
    Regions.HideoutHelmStart: Region("Hideout Helm Start", Levels.HideoutHelm, True, None, [], [], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: True),
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.handstand and l.lanky and l.pineapple and l.chunky and l.mini and l.istiny),
    ]),

    Regions.HideoutHelmMain: Region("Hideout Helm Main", Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmBattleArena, lambda l: l.jetpack and l.diddy),
        LocationLogic(Locations.HelmDonkey1, lambda l: l.bongos and l.isdonkey),
        LocationLogic(Locations.HelmDonkey2, lambda l: l.bongos and l.isdonkey),
        LocationLogic(Locations.HelmDonkeyMedal, lambda l: Events.HelmDonkeyDone in l.Events),
        LocationLogic(Locations.HelmChunky1, lambda l: l.triangle and l.ischunky),
        LocationLogic(Locations.HelmChunky2, lambda l: l.triangle and l.ischunky),
        LocationLogic(Locations.HelmChunkyMedal, lambda l: Events.HelmChunkyDone in l.Events),
        LocationLogic(Locations.HelmTiny1, lambda l: l.saxophone and l.istiny),
        LocationLogic(Locations.HelmTiny2, lambda l: l.saxophone and l.istiny),
        LocationLogic(Locations.HelmTinyMedal, lambda l: Events.HelmTinyDone in l.Events),
        LocationLogic(Locations.HelmLanky1, lambda l: l.trombone and l.islanky),
        LocationLogic(Locations.HelmLanky2, lambda l: l.trombone and l.islanky),
        LocationLogic(Locations.HelmLankyMedal, lambda l: Events.HelmLankyDone in l.Events),
        LocationLogic(Locations.HelmDiddy1, lambda l: l.guitar and l.isdiddy),
        LocationLogic(Locations.HelmDiddy2, lambda l: l.guitar and l.isdiddy),
        LocationLogic(Locations.HelmDiddyMedal, lambda l: Events.HelmDiddyDone in l.Events),
        LocationLogic(Locations.HelmBananaFairy1, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmBananaFairy2, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmKey, lambda l: Events.HelmKeyAccess in l.Events),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: l.grab and l.donkey and l.jetpack and l.diddy and l.punch and l.chunky),
        Event(Events.HelmDonkeyDone, lambda l: Events.HelmDoorsOpened in l.Events and l.HelmDonkey1 and l.HelmDonkey2),
        Event(Events.HelmChunkyDone, lambda l: Events.HelmDonkeyDone in l.Events and l.HelmChunky1 and l.HelmChunky2),
        Event(Events.HelmTinyDone, lambda l: Events.HelmChunkyDone in l.Events and l.HelmTiny1 and l.HelmTiny2),
        Event(Events.HelmLankyDone, lambda l: Events.HelmTinyDone in l.Events and l.HelmLanky1 and l.HelmLanky2),
        Event(Events.HelmDiddyDone, lambda l: Events.HelmLankyDone in l.Events and l.HelmDiddy1 and l.HelmDiddy2),
        Event(Events.HelmKeyAccess, lambda l: Events.HelmDiddyDone in l.Events
              and (l.settings.crown_door_open or l.BattleCrowns >= 4) and (l.settings.coin_door_open or l.nintendoCoin and l.rarewareCoin)),
    ], []),
}
