# fmt: off
"""Logic file for Hideout Helm."""

from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MinigameType import MinigameType
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import HelmSetting
from randomizer.LogicClasses import (Event, LocationLogic, Region,
                                     TransitionFront)

LogicRegions = {
    Regions.HideoutHelmStart: Region("Hideout Helm Start", "Hideout Helm", Levels.HideoutHelm, True, None, [
        LocationLogic(Locations.HelmMainEnemy_Start0, lambda l: l.CanAccessHelmStart()),
        LocationLogic(Locations.HelmMainEnemy_Start1, lambda l: l.CanAccessHelmStart()),
        LocationLogic(Locations.HelmMainEnemy_Hill, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky)),
        LocationLogic(Locations.HelmMainEnemy_SwitchRoom0, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky)),
        LocationLogic(Locations.HelmMainEnemy_SwitchRoom1, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky)),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom0, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky) and (l.mini and l.tiny)),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom1, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky) and (l.mini and l.tiny)),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom2, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky) and (l.mini and l.tiny)),
        LocationLogic(Locations.HelmMainEnemy_MiniRoom3, lambda l: l.CanAccessHelmStart() and (l.handstand and l.lanky) and (l.mini and l.tiny)),
    ], [], [
        TransitionFront(Regions.HideoutHelmLobby, lambda l: True),
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.settings.helm_setting == HelmSetting.skip_start or (l.handstand and l.lanky and ((l.pineapple and l.chunky and l.vines and ((l.mini and l.tiny) or l.generalclips)) or (l.CanMoonkick() or l.phasewalk or l.CanOStandTBSNoclip())))),
        TransitionFront(Regions.HideoutHelmDonkeyRoom, lambda l: l.settings.helm_setting == HelmSetting.default and (l.handstand and l.lanky and (l.CanMoonkick() or l.phasewalk or l.CanOStandTBSNoclip() or (l.pineapple and l.chunky and l.vines and l.generalclips)))),
        TransitionFront(Regions.HideoutHelmChunkyRoom, lambda l: l.settings.helm_setting == HelmSetting.default and (l.handstand and l.lanky and l.CanMoonkick())),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: l.settings.helm_setting == HelmSetting.skip_all),
    ]),

    Regions.HideoutHelmMain: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, True, -1, [
        LocationLogic(Locations.HelmBattleArena, lambda l: not l.settings.crown_placement_rando and l.jetpack and l.isdiddy and (l.settings.helm_setting == HelmSetting.skip_all or (Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events))),
        LocationLogic(Locations.HelmDonkey1, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDonkey2, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunky1, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunky2, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTiny1, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTiny2, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLanky1, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLanky2, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddy1, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddy2, lambda l: l.settings.helm_setting == HelmSetting.skip_all, MinigameType.HelmBarrel),
    ], [
        Event(Events.HelmDoorsOpened, lambda l: (l.grab and l.donkey and l.jetpack and l.diddy and l.punch and l.chunky) or l.settings.helm_setting != HelmSetting.default),
        Event(Events.HelmDonkeyDone, lambda l: ((l.isPriorHelmComplete(Kongs.donkey) or l.settings.helm_setting == HelmSetting.skip_all) and l.HelmDonkey1 and l.HelmDonkey2) or not l.settings.helm_donkey),
        Event(Events.HelmChunkyDone, lambda l: ((l.isPriorHelmComplete(Kongs.chunky) or l.settings.helm_setting == HelmSetting.skip_all) and l.HelmChunky1 and l.HelmChunky2) or not l.settings.helm_chunky),
        Event(Events.HelmTinyDone, lambda l: ((l.isPriorHelmComplete(Kongs.tiny) or l.settings.helm_setting == HelmSetting.skip_all) and l.HelmTiny1 and l.HelmTiny2) or not l.settings.helm_tiny),
        Event(Events.HelmLankyDone, lambda l: ((l.isPriorHelmComplete(Kongs.lanky) or l.settings.helm_setting == HelmSetting.skip_all) and l.HelmLanky1 and l.HelmLanky2) or not l.settings.helm_lanky),
        Event(Events.HelmDiddyDone, lambda l: ((l.isPriorHelmComplete(Kongs.diddy) or l.settings.helm_setting == HelmSetting.skip_all) and l.HelmDiddy1 and l.HelmDiddy2) or not l.settings.helm_diddy),
    ], [
        TransitionFront(Regions.HideoutHelmDonkeyRoom, lambda l: (l.bongos and l.isdonkey and Events.HelmDoorsOpened in l.Events) or l.phasewalk),
        TransitionFront(Regions.HideoutHelmChunkyRoom, lambda l: (l.triangle and l.ischunky and Events.HelmDoorsOpened in l.Events) or l.phasewalk),
        TransitionFront(Regions.HideoutHelmTinyRoom, lambda l: (l.saxophone and l.istiny and Events.HelmDoorsOpened in l.Events) or l.phasewalk),
        TransitionFront(Regions.HideoutHelmLankyRoom, lambda l: (l.trombone and l.islanky and Events.HelmDoorsOpened in l.Events) or l.phasewalk),
        TransitionFront(Regions.HideoutHelmDiddyRoom, lambda l: l.isdiddy and l.jetpack and ((Events.HelmDoorsOpened in l.Events and l.guitar) or l.phasewalk)),
        TransitionFront(Regions.HideoutHelmAfterBoM, lambda l: l.settings.helm_setting == HelmSetting.skip_all or (Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events)),
    ]),

    Regions.HideoutHelmDonkeyRoom: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmDonkey1, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDonkey2, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDonkeyMedal, lambda l: Events.HelmDonkeyDone in l.Events and l.isdonkey),
        LocationLogic(Locations.HelmMainEnemy_DKRoom, lambda l: True),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: True),
    ]),

    Regions.HideoutHelmChunkyRoom: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmChunky1, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunky2, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmChunkyMedal, lambda l: Events.HelmChunkyDone in l.Events and l.ischunky),
        LocationLogic(Locations.HelmMainEnemy_ChunkyRoom0, lambda l: True),
        LocationLogic(Locations.HelmMainEnemy_ChunkyRoom1, lambda l: True),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: True),
    ]),
    Regions.HideoutHelmTinyRoom: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmTiny1, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTiny2, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmTinyMedal, lambda l: Events.HelmTinyDone in l.Events and l.istiny),
        LocationLogic(Locations.HelmMainEnemy_TinyRoom, lambda l: True),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: True),
    ]),
    Regions.HideoutHelmLankyRoom: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmLanky1, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLanky2, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmLankyMedal, lambda l: Events.HelmLankyDone in l.Events and l.islanky),
        LocationLogic(Locations.HelmMainEnemy_LankyRoom0, lambda l: True),
        LocationLogic(Locations.HelmMainEnemy_LankyRoom1, lambda l: True),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: True),
    ]),
    Regions.HideoutHelmDiddyRoom: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmDiddy1, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddy2, lambda l: True, MinigameType.HelmBarrel),
        LocationLogic(Locations.HelmDiddyMedal, lambda l: Events.HelmDiddyDone in l.Events and l.isdiddy),
        LocationLogic(Locations.HelmMainEnemy_DiddyRoom0, lambda l: True),
        LocationLogic(Locations.HelmMainEnemy_DiddyRoom1, lambda l: True),
    ], [], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: True),
    ]),
    Regions.HideoutHelmAfterBoM: Region("Hideout Helm Main", "Hideout Helm", Levels.HideoutHelm, False, -1, [
        LocationLogic(Locations.HelmKey, lambda l: Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmBananaFairy1, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmBananaFairy2, lambda l: l.camera and Events.HelmKeyAccess in l.Events),
        LocationLogic(Locations.HelmMainEnemy_NavRight, lambda l: True),
        LocationLogic(Locations.HelmMainEnemy_NavLeft, lambda l: True),
    ], [
        Event(Events.HelmKeyAccess, lambda l: (l.CrownDoorOpened() and l.CoinDoorOpened()) or l.generalclips),
    ], [
        TransitionFront(Regions.HideoutHelmMain, lambda l: l.settings.helm_setting == HelmSetting.skip_all or (Events.HelmDonkeyDone in l.Events and Events.HelmChunkyDone in l.Events and Events.HelmTinyDone in l.Events and Events.HelmLankyDone in l.Events and Events.HelmDiddyDone in l.Events) or (l.generalclips or l.phasewalk)),
        TransitionFront(Regions.HideoutHelmDonkeyRoom, lambda l: l.generalclips or l.phasewalk),
        TransitionFront(Regions.HideoutHelmChunkyRoom, lambda l: l.generalclips or l.phasewalk),
        TransitionFront(Regions.HideoutHelmLankyRoom, lambda l: l.generalclips or l.phasewalk),
        TransitionFront(Regions.HideoutHelmTinyRoom, lambda l: l.generalclips or l.phasewalk),
        TransitionFront(Regions.HideoutHelmDiddyRoom, lambda l: l.generalclips and (l.isdiddy or l.istiny)),
    ])

}
