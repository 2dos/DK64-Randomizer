# fmt: off
"""Logic file for Hideout Helm."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.Regions import Regions
from randomizer.LogicClasses import Event, Exit, LocationLogic, Region

LogicRegions = {
    Regions.HideoutHelmStart: Region("Hideout Helm Start", Levels.HideoutHelm, True, [], [], [
        Exit(Regions.HideoutHelmLobby, lambda l: True),
        Exit(Regions.HideoutHelmMain, lambda l: l.handstand and l.pineapple and l.mini),
    ]),

    Regions.HideoutHelmMain: Region("Hideout Helm Main", Levels.HideoutHelm, True, [
        LocationLogic(Locations.HelmBattleArena, lambda l: l.jetpack),
        LocationLogic(Locations.HelmDonkeyMedal, lambda l: Events.HelmDonkeyDone in l.Events),
        LocationLogic(Locations.HelmChunkyMedal, lambda l: Events.HelmChunkyDone in l.Events),
        LocationLogic(Locations.HelmTinyMedal, lambda l: Events.HelmTinyDone in l.Events),
        LocationLogic(Locations.HelmLankyMedal, lambda l: Events.HelmLankyDone in l.Events),
        LocationLogic(Locations.HelmDiddyMedal, lambda l: Events.HelmDiddyDone in l.Events),
        LocationLogic(Locations.HelmBananaFairy1, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmBananaFairy2, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmKey, lambda l: Events.HelmKeyAccess in l.Events),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: l.grab and l.jetpack),
        Event(Events.HelmDonkeyDone, lambda l: Events.HelmDoorsOpened in l.Events and l.punch and l.bongos),
        Event(Events.HelmChunkyDone, lambda l: Events.HelmDonkeyDone and l.triangle and l.hunkyChunky and l.pineapple),
        Event(Events.HelmTinyDone, lambda l: Events.HelmChunkyDone in l.Events and l.saxophone and l.twirl),
        # You're supposed to sprint through the maze but you can make it without
        Event(Events.HelmLankyDone, lambda l: Events.HelmTinyDone in l.Events and l.trombone and l.grape),
        Event(Events.HelmDiddyDone, lambda l: Events.HelmLankyDone in l.Events and l.guitar and l.Slam and l.peanut),
        Event(Events.HelmKeyAccess, lambda l: Events.HelmDiddyDone in l.Events and l.BattleCrowns >= 4 and l.nintendoCoin and l.rarewareCoin),
    ], []),
}
