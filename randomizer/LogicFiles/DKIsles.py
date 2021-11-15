from LogicClasses import Region, LogicLocation, Event, Exit

Regions = {
    "Start": Region("Start", False, [
        LogicLocation("Cool", lambda l, r: True),
        LogicLocation("Lame", lambda l, r: True),
    ], [], [
        Exit("Main", lambda l, r: l.a or l.b),
    ]),
    "Main": Region("Main", True, [
        LogicLocation("Wow", lambda l, r: True),
        LogicLocation("Huh", lambda l, r: l.a and l.b),
    ], [
        Event("2 banan", lambda l, r: l.GoldenBananas >= 2)
    ], [
        Exit("End", lambda l, r: "2 banan" in l.Events and r.donkeyAccess)
    ]),
    "End": Region("End", False, [
        LogicLocation("Nice", lambda l, r: True)
    ], [], []),
}
