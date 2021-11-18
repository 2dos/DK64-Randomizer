from LogicClasses import Region, Location, Event, Exit
from Enums.Events import Events

Regions = {
    "Hideout Helm Start": Region("Hideout Helm Start", True, [], [], [
        Exit("Hideout Helm Lobby", lambda l: True),
        Exit("Hideout Helm Main", lambda l: l.handstand and l.pineapple and l.mini),
    ]),

    "Hideout Helm Main": Region("Hideout Helm Main", True, [
        Location("Helm Battle Arena", lambda l: l.jetpack),
        Location("Helm Donkey Medal", lambda l: Events.HelmDonkeyDone in l.Events),
        Location("Helm Chunky Medal", lambda l: Events.HelmChunkyDone in l.Events),
        Location("Helm Tiny Medal", lambda l: Events.HelmTinyDone in l.Events),
        Location("Helm Lanky Medal", lambda l: Events.HelmLankyDone in l.Events),
        Location("Helm Diddy Medal", lambda l: Events.HelmDiddyDone in l.Events),
        Location("Helm Banana Fairy 1", lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        Location("Helm Banana Fairy 2", lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        Location("Helm Key", lambda l: Events.HelmKeyAccess in l.Events),
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
