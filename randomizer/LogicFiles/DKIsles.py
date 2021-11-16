from LogicClasses import Region, Location, Event, Exit, Kongs
from Events import Events

Regions = {
    "Start": Region("Start", False, [], [], [
        Exit("Cranky", lambda l, r: True),
        Exit("Main", lambda l, r: True),
    ])
}
