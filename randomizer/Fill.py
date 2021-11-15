import random

import Logic
from Logic import LogicVariables

def GetAccessibleLocations(ownedItems):
    accessible = []

    newLocations = []
    items = ownedItems.copy()
    addedEvents = True
    while len(newLocations) > 0 or addedEvents:
        addedEvents = False
        for location in newLocations:
            accessible.append(location)
            if location.item is not None:
                items.append(location.item)
        newLocations = []
        LogicVariables.Update(items)

        for kong in LogicVariables.GetKongs():
            LogicVariables.SetKong(kong)

            regionPool = [Logic.Regions["Start"]]
            addedRegions = ["Start"]

            while len(regionPool) > 0:
                region = regionPool.pop()

                region.UpdateAccess(kong, LogicVariables)

                for location in region.locations:
                    if location not in accessible and location.logic(LogicVariables, region):
                        newLocations.append(location)

                for event in region.events:
                    if event.name not in LogicVariables.Events and event.logic(LogicVariables, region):
                        LogicVariables.AddEvent(event.name)
                        addedEvents = True

                for exit in region.exits:
                    if exit.dest not in addedRegions and exit.logic(LogicVariables, region):
                        addedRegions.append(exit.dest)
                        regionPool.append(Logic.Regions[exit.dest])

                # No regions left, check if there are any this kong has access to
                # through a tag barrel but has not yet visited.
                if len(regionPool) == 0:
                    tagAccess = [x for x in Logic.Regions.values() if x.name not in addedRegions and x.HasAccess(kong)]
                    addedRegions.extend([x.name for x in tagAccess])
                    regionPool = tagAccess


    return accessible

def AssumedFill():
    itemPool = ["a", "b", "Golden Banana", "Golden Banana", "Golden Banana"]

    reachable = GetAccessibleLocations(itemPool)
    random.shuffle(itemPool)
    while len(itemPool) > 0:
        item = itemPool.pop()
        LogicVariables.Reset()
        reachable = GetAccessibleLocations(itemPool)
        for location in reachable:
            itemName = "None" if location.item == None else location.item
            print(location.name + " " + itemName)
        reachable = [x for x in reachable if x.item == None]
        if len(reachable) == 0:
            break
        random.shuffle(reachable)
        location = reachable.pop()
        location.PlaceItem(item)
