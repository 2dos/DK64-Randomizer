"""A script to automatically calculate the requirements for various CBs."""

# Python built-ins
import collections
import itertools

# Data for region traversal and banana requirements
from randomizer.CollectibleLogicFiles.AngryAztec import LogicRegions as AztecBananas
from randomizer.CollectibleLogicFiles.CreepyCastle import LogicRegions as CastleBananas
from randomizer.CollectibleLogicFiles.CrystalCaves import LogicRegions as CavesBananas
from randomizer.CollectibleLogicFiles.FranticFactory import LogicRegions as FactoryBananas
from randomizer.CollectibleLogicFiles.FungiForest import LogicRegions as ForestBananas
from randomizer.CollectibleLogicFiles.GloomyGalleon import LogicRegions as GalleonBananas
from randomizer.CollectibleLogicFiles.JungleJapes import LogicRegions as JapesBananas
from randomizer.LogicFiles.AngryAztec import LogicRegions as AztecLogic
from randomizer.LogicFiles.CreepyCastle import LogicRegions as CastleLogic
from randomizer.LogicFiles.CrystalCaves import LogicRegions as CavesLogic
from randomizer.LogicFiles.FranticFactory import LogicRegions as FactoryLogic
from randomizer.LogicFiles.FungiForest import LogicRegions as ForestLogic
from randomizer.LogicFiles.GloomyGalleon import LogicRegions as GalleonLogic
from randomizer.LogicFiles.JungleJapes import LogicRegions as JapesLogic

# Enums galore
from randomizer.Enums.Collectibles import Collectibles
from randomizer.Enums.Events import Events
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Regions import Regions
from randomizer.Enums.Settings import RemovedBarriersSelected
from randomizer.Enums.Switches import Switches
from randomizer.Enums.Time import Time


class MockSettings:
    """Mock of the Settings object."""

    tns_location_rando = False
    free_trade_items = False
    galleon_water_internal = None
    fungi_time_internal = None
    shuffle_shops = False


class MockEvents:
    """Mock of the Events object."""

    def __init__(self, requirements):
        """Initialize the events class with a set of requirements."""
        self.reqs = requirements

    def __contains__(self, event):
        """Check if a given event is in the events (requirements)."""
        return event in self.reqs


TINY_TEMPLE_REGIONS = {Regions.TempleStart, Regions.TempleGuitarPad, Regions.TempleUnderwater, Regions.TempleVultureRoom, Regions.TempleKONGRoom}
CASTLE_CRYPT_REGIONS = {Regions.Crypt, Regions.CryptDonkeyRoom, Regions.CryptDiddyRoom, Regions.CryptChunkyRoom, Regions.CastleMinecarts}
GUN_MAP = {Kongs.donkey: "coconut", Kongs.lanky: "grape", Kongs.diddy: "peanut", Kongs.tiny: "feather", Kongs.chunky: "pineapple"}
SWITCHSANITY_MOVES = {
    # These first two switches are removed because they are special_requirements
    Switches.FungiGreenFeather: None,
    Switches.FungiGreenPineapple: None,
    # These switches are all just mapped to their default (non-switchsanity) behavior
    Switches.FungiYellow: "grape",
    Switches.GalleonCannonGame: "pineapple",
    Switches.GalleonLighthouse: "coconut",
    Switches.GalleonShipwreck: "peanut",
    Switches.JapesDiddyCave: "peanut",
    Switches.JapesFeather: "japes_shellhive_gate",
    Switches.JapesPainting: "peanut",
    Switches.JapesRambi: "coconut",
    Switches.AztecQuicksandSwitch: "levelSlam",
    Switches.AztecGuitar: "guitar",
    Switches.AztecBlueprintDoor: "coconut",
}
BASE_REQUIREMENTS = [
    # Moves for all kongs
    *["can_use_vines", "swim", "oranges", "barrels", "climbing"],
    *["camera", "shockwave", "scope", "homing", "Slam", "levelSlam"],
    # Moves for single kongs
    *["coconut", "bongos", "grab", "strongKong", "blast"],
    *["peanut", "guitar", "charge", "jetpack", "spring"],
    *["grape", "trombone", "handstand", "sprint", "balloon"],
    *["feather", "saxophone", "twirl", "mini", "monkeyport"],
    *["pineapple", "triangle", "punch", "hunkyChunky", "gorillaGone"],
]
ALWAYS_IN_LOGIC = [
    # These represent 'you are kong X', which assumes that you have a tag barrel accessible.
    *["isdonkey", "islanky", "isdiddy", "istiny", "ischunky"],
    # These represent 'is kong X unlocked'
    *["donkey", "lanky", "diddy", "tiny", "chunky"],
    # These are region-based assumptions (should be quite rare)
    Events.HatchOpened,
    # 'assumeAztecEntry',  # I could use this but I'm using a different starting region instead.
]


class Logic:
    """Mock of the randomizer/Logic.py file."""

    def __init__(self, requirements):
        """Initialize the logic class with custom requirements."""
        self.reqs = set([*ALWAYS_IN_LOGIC, *requirements])
        self.settings = MockSettings()
        self.Events = MockEvents(self.reqs)  # Just a small wrapper since the code uses 'if Events.Foo in l.Events'

    def get(self, key):
        """Check if a given key is in the requirements."""
        return key in self.reqs

    def __getattr__(self, key):
        """Check if a given key is in the requirements."""
        return key in self.reqs

    def TimeAccess(self, region, time):
        """Check if a given time is in the requirements."""
        if time == Time.Day:
            return Events.Day in self.Events
        elif time == Time.Night:
            return Events.Night in self.Events
        # elif time == Time.Both:
        return True

    def hasMoveSwitchsanity(self, switchsanity_setting, kong_needs_current=True, level=None, default_slam_level=0):
        """Check if a given switch is in the requirements."""
        if switchsanity_setting in self.reqs:
            return True
        actual_move = SWITCHSANITY_MOVES[switchsanity_setting]
        return actual_move in self.reqs

    def checkBarrier(self, barrier):
        """Check if a given barrier is in the requirements."""
        return barrier in self.reqs

    def HasGun(self, kong):
        """Is handled separately by Moves.Night / Moves.Day."""
        return False

    def CanSlamSwitch(self, level, default_requirement_level):
        """Check if a level slam is in the requirements."""
        return "levelSlam" in self.reqs

    def canOpenLlamaTemple(self):
        """Check if a access to the llama temple is in the requirements."""
        return Events.LlamaFreed in self.Events and (self.coconut or self.grape or self.feather)

    def canTravelToMechFish(self):
        """Check if diving is in the requirements."""
        return self.swim

    def IsBossReachable(self, level):
        """Not strictly necessary (there aren't CBs inside boss rooms) but allows for assumed tagging inside boss rooms."""
        return True

    def HasInstrument(self, kong):
        """Not strictly necessary but I'm not sure why."""
        return False

    def galleonGatesStayOpen(self):
        """I'm pretty sure this QoL is always enabled in rando."""
        return True

    def CanOpenJapesGates(self):
        """Quality of life improvement from rando."""
        return True

    def CanLlamaSpit(self):
        """I don't think this matters but I think tiny canonically frees lanky."""
        return lambda: self.saxophone

    def IsLavaWater(self):
        """Hardmode requirements are all assumed false."""
        return False

    def IsHardFallDamage(self):
        """Hardmode requirements are all assumed false."""
        return False

    def CanPhase(self):
        """Assume all glitches are not possible."""
        return False

    def CanMoonkick(self):
        """Assume all glitches are not possible."""
        return False

    def CanOStandTBSNoclip(self):
        """Assume all glitches are not possible."""
        return False

    def CanMoontail(self):
        """Assume all glitches are not possible."""
        return False

    def CanAccessRNDRoom(self):
        """Assume all glitches are not possible.

        Determines whether the player can enter an R&D Room with glitches.
        """
        return False

    def CanPhaseswim(self):
        """Assume all glitches are not possible."""
        return False

    def CanSTS(self):
        """Assume all glitches are not possible."""
        return False

    def CanSkew(self, swim, is_japes=True, kong_req=Kongs.any):
        """Assume all glitches are not possible."""
        return False


class SetOfSets:
    """Wrapper class to handle composite requirements.

    In practice, it can be possible to collect CBs using multiple options (an "either/or").
    To represent this comfortably, we use a "set of sets", where each inner set represents
    a unique way of accomplishing a task, and the overall set represents all ways of doing the task.
    There should not be duplicates nor overlap; this class helps to keep that invariant true.
    """

    def __init__(self, requirements=None):
        """Initialize the SetOfSets with requirements."""
        self.requirements = [requirements] if requirements is not None else []

    def __iter__(self):
        """Iterate the requirements in the SetOfSets."""
        return self.requirements.__iter__()

    def __repr__(self):
        """Reproduce the SetOfSets."""
        return str(self.requirements)

    def __len__(self):
        """Get the length of the SetOfSets."""
        return len(self.requirements)

    def __hash__(self):
        """Hash the SetOfSets.

        In order for the type to be hashable (i.e. used as a key in a dictionary) we need a hash function.
        But the dictionaries are small (and hashing is hard) so we're just telling python to fall back to __eq__.
        """
        return 0

    def __eq__(self, other):
        """Compare this SetOfSets with another."""
        if len(self) != len(other):
            return False
        for requirement in self.requirements:
            if requirement not in other.requirements:
                return False
        return True

    def add(self, requirement):
        """Add a requirement to this SetOfSets, if it's distinctive."""
        i = 0
        while i < len(self.requirements):
            if requirement.issuperset(self.requirements[i]):
                return False  # We're trying to add something that's already here, in a simpler form.
            if requirement.issubset(self.requirements[i]):
                self.requirements.pop(i)  # In rare cases we might find a simpler way to do something later, and need to clean up.
                # Keep going here in case there are other supersets still in the list
            else:
                i += 1
        self.requirements.append(set(requirement))  # Copy to avoid sharing set objects between every requirement
        return True

    def replace_event(self, event, event_requirements):
        """Replace an event with its requirements.

        This helps deal with transitive requirements,
        i.e. a required event which also has its own SetOfSets requirements.
        This breaks some encapsulation rules, but is tremendously helpful and simple.
        """
        did_any_replacements = False
        i = 0
        while i < len(self.requirements):
            requirement = self.requirements[i]
            if event not in requirement:
                i += 1
                continue

            did_any_replacements = True
            self.requirements.pop(i)
            requirement = requirement - {event}
            for event_requirement in event_requirements:
                self.add(requirement | event_requirement)

        return did_any_replacements


class MockRegion:
    """A mock of randomizer.LogicClasses.Region."""

    def __init__(self, region_id):
        """Initialize the MockRegion with a region ID."""
        self.events = collections.defaultdict(SetOfSets)  # Will be populated later
        self.cbs = collections.defaultdict(SetOfSets)  # Will be populated later
        self.exits = collections.defaultdict(SetOfSets)  # Will be populated later

        self.name = region_id

    def __str__(self):
        """Print the MockRegion for debugging purposes."""
        output = "{\n"
        output += f'  "name": "{self.name.__repr__()}"' + ",\n"
        if len(self.exits) > 0:
            output += '  "exits": {\n'
            for k, v in self.exits.items():
                output += f'    "{k.__repr__()}": {v}' + ",\n"
            output += "  }\n"
        output += "}"
        return output


def possible_requirements(requirements):
    """Iterate all possible combinations of requirements, in order. Max 5."""
    for i in range(5):
        for combination in itertools.combinations(requirements, i):
            yield set(combination)


def walk_region_graph(regions, starting_region):
    """Traverse all regions in a graph along transitions, without doubling up.

    This generally improves the performance of some of our 'while true' floodfill algorithms,
    since requirements can be naturally flooded through the system.
    """
    visited_regions = set()
    adjacent_regions = {starting_region}
    while len(adjacent_regions) > 0:
        next_region = next(adjacent_regions.__iter__())
        yield next_region
        visited_regions.add(next_region)
        adjacent_regions.remove(next_region)
        for other_region in regions[next_region].exits:
            if other_region not in visited_regions:
                adjacent_regions.add(other_region)


def flatten_graph(region_logic, region_bananas, requirements):
    """Stage 1 of computation: Convert the raw data formats.

    The code in the repo is not tuned for brute force, i.e. logic requirements are listed as lambdas.
    While it is possible to use ast and other smarts to reverse those into their SetOfSets requirement,
    I found it easier (and not overly time consuming) to just brute force all possible combinations,
    and then just evaluate the logic against each possible combination.

    Regardless of methodology, this is a very helpful function, since it allows all further code
    to basically ignore the complexities of DK64, and just treat this like a graph traversal problem.
    """
    # Initialize all regions first, since we're caching data on them as we iterate
    regions = {}
    for region_id in region_logic:
        regions[region_id] = MockRegion(region_id)

    # Used during pre-passes to reduce the number of objects to process.
    no_requirements = Logic(set())

    print("Finding all events")
    events = []
    event_names = set()
    for region_id, region in region_logic.items():
        for event in region.events:
            if Events.JapesW1aTagged <= event.name <= Events.IslesW5bTagged:
                continue  # Warps do not contribute to new regions becoming accessible, so we ignore them for perf benefits
            elif event.name in requirements:
                regions[region_id].events[event.name] = SetOfSets()
                continue  # Events which are explicitly listed as requirements shouldn't be satisfiable
            elif event.logic(no_requirements):
                regions[region_id].events[event.name].add(set())
                event_names.add(event.name)
            else:
                events.append((region_id, event))
                event_names.add(event.name)

    # For the purposes of further graph flattening, allow events as requirements, but don't modify the original list.
    requirements = {*requirements, *event_names}

    print("Computing event requirements")
    for requirement in possible_requirements({*requirements, *event_names}):  # Events may be requirements for other events
        l = Logic(requirement)
        for region_id, event in events:
            if event.logic(l):
                if regions[region_id].events[event.name].add(requirement):
                    # print('Event', event.name.name, 'in region', region.name, 'is directly possible using requirement', requirement)
                    pass

    # Sanity check to make sure all events were processed
    raw_events = {event.name for region in region_logic.values() for event in region.events}
    handled_events = {event for region in regions.values() for event in region.events}
    unhandled_events = raw_events - handled_events
    for event in unhandled_events:
        if Events.JapesW1aTagged <= event <= Events.IslesW5bTagged:
            continue  # Warps do not contribute to new regions becoming accessible, so we ignore them for perf benefits
        raise ValueError(f"Unable to determine requirements for event {event.name}")

    print("Finding all collectibles")
    collectibles = []
    for region in region_bananas:
        for collectible in region_bananas[region]:
            if collectible.type not in [Collectibles.banana, Collectibles.bunch, Collectibles.balloon]:
                continue
            elif collectible.logic(no_requirements):
                regions[region].cbs[collectible].add(set())
            else:
                collectibles.append((region, collectible))

    print("Computing collectible requirements")
    for requirement in possible_requirements(requirements):
        l = Logic(requirement)
        for region, collectible in collectibles:
            if collectible.logic(l):
                regions[region].cbs[collectible].add(requirement)

    print("Finding all region transitions")
    transitions = []
    for region_id, region in region_logic.items():
        for transition in region.exits:
            if transition.dest not in region_logic:
                continue  # Ignore transitions which leave the region (e.g. to the lobby)
            if transition.logic(no_requirements) and no_requirements.TimeAccess(transition.dest, transition.time):
                regions[region_id].exits[transition.dest].add(set())  # Small perf improvement: filter out transitions which are free
            else:
                transitions.append((region_id, transition))

    print("Computing region transition requirements")
    for requirement in possible_requirements(requirements):
        l = Logic(requirement)
        for source, transition in transitions:
            if transition.logic(l) and l.TimeAccess(transition.dest, transition.time):
                if regions[source].exits[transition.dest].add(requirement):
                    # print('Found transition from', source.name, 'to', transition.dest.name, 'with requirement', requirement)
                    pass

    # Hack: The ice walls in Crystal Caves aren't events, so they aren't nicely compatible with the event_requirements system.
    # Instead, I'm manually replacing punch with ice_walls and rbb with igloo_pads here.
    # This was also needed for crypt, because we need to report on the crypt doors for some reason.
    for source in regions:
        for requirement in regions[source].exits.values():
            if any((RemovedBarriersSelected.caves_ice_walls in r for r in requirement)):
                requirement.replace_event("punch", SetOfSets({RemovedBarriersSelected.caves_ice_walls}))
            if any((RemovedBarriersSelected.caves_igloo_pads in r for r in requirement)):
                requirement.replace_event("jetpack", SetOfSets({RemovedBarriersSelected.caves_igloo_pads}))
            if any((RemovedBarriersSelected.castle_crypt_doors in r for r in requirement)):
                requirement.replace_event("coconut", SetOfSets({RemovedBarriersSelected.castle_crypt_doors}))
                requirement.replace_event("peanut", SetOfSets({RemovedBarriersSelected.castle_crypt_doors}))
                requirement.replace_event("grape", SetOfSets({RemovedBarriersSelected.castle_crypt_doors}))
                requirement.replace_event("feather", SetOfSets({RemovedBarriersSelected.castle_crypt_doors}))
                requirement.replace_event("pineapple", SetOfSets({RemovedBarriersSelected.castle_crypt_doors}))

    return regions


def traverse_graph(regions, entry_region):
    """Stage 2: Flood-fill region requirements.

    It is not sufficient to know what the requirements are for each region-to-region transition,
    we actually need to know how to get to each region from the entry point in each world.

    To that end, we run a really big 'while true' loop which just keeps bouncing around the world
    until it runs out of things to do.
    This is *not* an efficient graph traversal algo, but it's fast enough with the size of DK64 worlds.

    While we're traversing, we also compute the same data for events, since we'll need it later.
    """
    # Now that we have the requirements in a reasonable format, we can compute the path(s) to each collectible.
    region_requirements = collections.defaultdict(SetOfSets)
    region_requirements[entry_region].add(set())  # The entry region is always accessible with zero requirements

    event_requirements = collections.defaultdict(SetOfSets)

    print("Exploring region graph to find all possible requirements")
    while True:
        found_new_requirement = False
        for next_region in walk_region_graph(regions, entry_region):
            # Find all ways to reach this node from the current graph
            for region in list(region_requirements.keys()):
                if next_region not in regions[region].exits:
                    continue

                for region_requirement in region_requirements[region]:
                    # Find the cross product between 'ways to access region' and 'ways to traverse from region -> next_region'
                    for exit_requirement in regions[region].exits[next_region]:
                        # If any of those products are new ways to reach next_region, then we do another loop afterwards
                        if region_requirements[next_region].add(exit_requirement | region_requirement):
                            # print('Found new transition from', region.name, 'to', next_region.name, 'using exit requirement', exit_requirement, 'and region requirement', region_requirement)
                            found_new_requirement = True

                    # Find the cross product between 'ways to access region' and 'ways to trigger events in the region'
                    for event in regions[region].events:
                        for event_requirement in regions[region].events[event]:
                            if event_requirements[event].add(event_requirement | region_requirement):
                                # print('Found new path to event', event.name, 'in region', region.name, 'using event requirement', event_requirement, 'and region requirement', region_requirement)
                                found_new_requirement = True

        if not found_new_requirement:
            break

    # Now that we have the requirements, we need to "flatten" any event requirements, i.e. events which are not requirements themselves.
    # This will also incorporate access to the region where the event is into the requirements.
    print("Expanding events")
    for i in range(10):  # Limited to 10 layers of event-which-requires-event
        expanded_any_events = False
        for event in event_requirements:
            for other_event in event_requirements:
                if event_requirements[event].replace_event(other_event, event_requirements[other_event]):
                    expanded_any_events = True
        if not expanded_any_events:
            break
    else:
        raise ValueError("Unable to resolve all event-inside-event dependencies within 10 loops -- possible infinite event requirements")

    for region in region_requirements:
        for event in event_requirements:
            if region_requirements[region].replace_event(event, event_requirements[event]):
                # print('Replaced event', event.name, 'in region', region.name, 'with its requirements', event_requirements[event])
                pass

    return region_requirements, event_requirements


def compute_cb_requirements(regions, region_requirements, event_requirements):
    """Stage 3: Compute the requirements to reach each CB/Bunch/Balloon.

    We already parsed out the relevant collectible objects during our flatten_graph prepass.
    Now, it's time to actually make the magic happen, and use our knowledge of region and
    event requirements to figure out how to get all the colored bananas.

    Since we've done a pretty thorough job already, this turns out to be pretty simple:
    Just determine the cross-product between the direct requirements to acquire a CB
    (e.g. 'coconut' for a balloon), and the transitive requirements to access a region
    (e.g. 'climbing' to get up to the japes hillside).

    We also need to do a quick fix-up for event requirements, but there's a handy utility for that.
    """
    print("Computing CB requirements")
    all_cb_requirements = collections.defaultdict(lambda: collections.defaultdict(list))
    for region in region_requirements:
        # For each CB in the region, combine all the ways of obtaining the CB(s) with all the ways of reaching the region.
        for cb, cb_requirements in regions[region].cbs.items():
            requirements_crossproduct = SetOfSets()
            for cb_requirement in cb_requirements:
                for region_requirement in region_requirements[region]:
                    requirement = region_requirement | cb_requirement
                    # Slight hack -- this logic does not check region.tagbarrel when evaluating region requirements.
                    # The tiny temple famously does not have a tag barrel, and so you cannot (logically) change kongs inside of it.
                    # The main way this assumption manifests is assuming access to the tiny temple with another kong's gun.
                    if region in TINY_TEMPLE_REGIONS and GUN_MAP[cb.kong] not in region_requirement:
                        continue
                    # The castle crypt rooms are also bereft of a tag barrel, but since this script is already reporting on
                    # castle_crypt_doors directly, it's implicitly handled by separating out those requirements during flatten_graph.
                    #
                    # The third tag anywhere "gotcha" is access to the 10 diddy CBs inside the Caves Blueprint Cave.
                    # You can only access this cave as mini, but it has warp 4 in it so you can come back as diddy.
                    # However, warp 4 logically requires jetpack to reach it, so we adjust the requirements here.
                    if cb.kong == Kongs.diddy and region == Regions.CavesBlueprintCave:
                        requirement |= {"jetpack"}
                    # On the other hand, there is a bunch of lanky CBs on top of the sprint cabin (on the trombone pad).
                    # Logically you are supposed to use balloon to reach them, but you can also get up there with jetpack.
                    # If there isn't a boss portal up there (uncommon with Dos's doors), the bunch is not in logic.
                    if cb.kong == Kongs.lanky and region == Regions.CavesSprintCabinRoof and region_requirement == {"jetpack"}:
                        continue
                    # Additional hack #1: We require "night" and "day" separately from guns, but they are overlapping.
                    # If the requirement contains night or day access *and* one of the 5 guns, remove night/day.
                    if requirement.intersection({"coconut", "peanut", "grape", "feather", "pineapple"}):
                        requirement.discard(Events.Night)
                        requirement.discard(Events.Day)
                    # Additional hack #2: We require "levelSlam" (i.e. switch color) separately from just "slam" (i.e. pounding a box).
                    # If the requirement contains both, just report levelSlam (the more restrictive requirement)
                    if requirement.intersection({"levelSlam"}):
                        requirement.discard("Slam")
                    # Additional hack #3: We list Enguarde as a requirement for the DK CBs in Galleon (idk why).
                    # For everyone's sanity, we *shouldn't* list Enguarde as a requirement for any Lanky CBs.
                    if cb.kong == Kongs.lanky:
                        requirement.discard(Events.ShipyardEnguarde)
                        requirement.discard(Events.LighthouseEnguarde)
                    # Finally, once we're done processing all the hacks, add the requirements.
                    requirements_crossproduct.add(requirement)
            # If the cb requires a non-requirement event, substitute in the event's requirements
            for event in event_requirements:
                requirements_crossproduct.replace_event(event, event_requirements[event])

            if len(requirements_crossproduct) == 0:
                raise ValueError("Unable to determine requirements for cb in region", region.name, "with original requirements", cb_requirements)

            all_cb_requirements[cb.kong][requirements_crossproduct].append((cb, region))

    return all_cb_requirements


def to_javascript(cb_requirements, special_requirements):
    """Stage 4: Generate the output for Ballaam.

    And finally, we need to emit this data in some format that Javascript can understand.
    Thankfully, that's not too bad -- there's just a bit of renaming and other small fixups.
    We've already grouped CBs by their requirements in the previous step, but this stage is also
    responsible for counting the total number of CBs for each SetOfSets requirement.

    For debugability, I'm also including a comment which describes which CBs are available
    for each set of requirements. It's not perfect but it should be good enough for reading.
    """
    # The javascript code uses slightly different names for kongs and moves.
    kong_map = {Kongs.donkey: "DK", Kongs.diddy: "Diddy", Kongs.lanky: "Lanky", Kongs.tiny: "Tiny", Kongs.chunky: "Chunky"}
    move_map = {
        **{"can_use_vines": "Vines", "swim": "Diving", "oranges": "Oranges", "barrels": "Barrels", "climbing": "ClimbingCheck"},
        **{"Slam": "Slam", "levelSlam": "LevelSlam"},
        # Kong-specific
        **{"coconut": "Coconut", "bongos": "Bongos", "grab": "Grab", "strongKong": "Strong", "blast": "Blast"},
        **{"peanut": "Peanut", "guitar": "Guitar", "charge": "Charge", "jetpack": "Rocket", "spring": "Spring"},
        **{"grape": "Grape", "trombone": "Trombone", "handstand": "Orangstand", "sprint": "Sprint", "balloon": "Balloon"},
        **{"feather": "Feather", "saxophone": "Sax", "twirl": "Twirl", "mini": "Mini", "monkeyport": "Monkeyport"},
        **{"pineapple": "Pineapple", "triangle": "Triangle", "punch": "Punch", "hunkyChunky": "Hunky", "gorillaGone": "Gone"},
    }
    move_map.update(special_requirements)
    move_map_keys = list(move_map.keys())
    move_map_values = list(move_map.values())

    output = ""
    for kong in kong_map:
        output += f'        "{kong_map[kong]}": [\n'
        entries = []
        kong_total = 0
        for requirements in cb_requirements[kong]:
            locations = collections.defaultdict(list)
            count = 0
            for cb, region in cb_requirements[kong][requirements]:
                if cb.type == Collectibles.banana:
                    count += 1 * cb.amount
                    locations[region.name].append(f"{cb.amount} banana{'s'[:cb.amount ^ 1]}")
                elif cb.type == Collectibles.bunch:
                    count += 5 * cb.amount
                    locations[region.name].append(f"{cb.amount} bunch{'es'[:2 * cb.amount ^ 2]}")
                elif cb.type == Collectibles.balloon:
                    count += 10 * cb.amount
                    locations[region.name].append(f"{cb.amount} balloon{'s'[:cb.amount ^ 1]}")
            kong_total += count

            # Sort the output (for consistency).
            # 1. Each requirement is ordered by the moves in the move map
            # 2. Either/or requirements are ordered by length, then by moves in the move map
            # 3. CBs with fewer requirements come first, ties broken by moves in the move map
            converted = []
            for requirement in requirements:
                converted_requirement = [move_map_keys.index(r) for r in requirement]
                converted_requirement.sort()
                converted.append(converted_requirement)
            converted.sort(key=lambda row: (len(row), *row))
            entries.append((converted, count, locations))

        # One final sanity check: There should be 100 CBs per kong.
        assert kong_total == 100, f"Missing {100 - kong_total} CBs for {kong}"

        def sort_key(entry):
            overall_sort_key = []
            for converted_requirement in entry[0]:
                overall_sort_key += converted_requirement
            return (len(overall_sort_key), *overall_sort_key)

        entries.sort(key=sort_key)

        for converted_requirements, count, locations in entries:
            output += f"            new Requirement({count}, "

            location_string = []
            for region in sorted(locations.keys()):
                location_string.append(", ".join(sorted(locations[region])) + f" in {region}")

            moves = []
            for converted_requirement in converted_requirements:
                if converted_requirement == []:
                    moves.append("Moves.Moveless")
                else:
                    move_names = ", ".join(("Moves." + move_map_values[c] for c in converted_requirement))
                    # Hack: this requirement has a different name depending on which kong is responsible.
                    move_names = move_names.replace("Moves.CastleCryptDoors", f"Moves.Crypt{kong_map[kong]}Entry")
                    moves.append(move_names)

            # Some slight formatting here to put the comment on the first line, regardless of the number of moves.
            if len(moves) == 1:
                output += f"[[{moves[0]}]]), // " + "; ".join(location_string) + "\n"
            else:
                output += "[ // " + "; ".join(location_string) + "\n"
                for move in moves:
                    output += f"                [{move}]" + ",\n"
                output += "            ]),\n"
        output += "        ],\n"
    return output


LEVELS = [
    {
        "name": "Japes",
        "logic": JapesLogic,
        "bananas": JapesBananas,
        "entry_region": Regions.JungleJapesEntryHandler,
        "special_requirements": {
            Events.JapesFreeKongOpenGates: "JapesCoconut",
            "japes_shellhive_gate": "JapesShellhive",
        },
    },
    {
        "name": "Aztec",
        "logic": AztecLogic,
        "bananas": AztecBananas,
        # I have moved the Angry Aztec entry region to avoid having all CBs locked by Twirl/Vines.
        "entry_region": Regions.AngryAztecOasis,
        "special_requirements": {
            Events.AztecGuitarPad: "AztecTunnelDoor",
            Events.LlamaFreed: "AztecLlama",
            Events.AztecIceMelted: "TinyTempleIce",
            Events.FedTotem: "Aztec5DT",
        },
    },
    {
        "name": "Factory",
        "logic": FactoryLogic,
        "bananas": FactoryBananas,
        "entry_region": Regions.FranticFactoryEntryHandler,
        "special_requirements": {
            Events.TestingGateOpened: "FactoryTesting",
            Events.MainCoreActivated: "FactoryProduction",
        },
    },
    {
        "name": "Galleon",
        "logic": GalleonLogic,
        "bananas": GalleonBananas,
        "entry_region": Regions.GloomyGalleonEntryHandler,
        "special_requirements": {
            Events.WaterRaised: "RaisedWater",
            Events.WaterLowered: "LoweredWater",
            Events.LighthouseGateOpened: "GalleonLighthouse",
            Events.ShipyardGateOpened: "GalleonPeanut",
            Events.ActivatedLighthouse: "GalleonShipSpawned",
            Events.ShipyardTreasureRoomOpened: "GalleonTreasure",
            Events.ShipyardEnguarde: "Enguarde",
            Events.LighthouseEnguarde: "Enguarde",
        },
    },
    {
        "name": "Fungi",
        "logic": ForestLogic,
        "bananas": ForestBananas,
        "entry_region": Regions.FungiForestEntryHandler,
        "special_requirements": {
            Events.Night: "Night",
            Events.Day: "Day",
            Events.HollowTreeGateOpened: "ForestYellowTunnel",
            Switches.FungiGreenFeather: "ForestGreenTunnelFeather",
            Switches.FungiGreenPineapple: "ForestGreenTunnelPineapple",
            Events.MushroomCannonsSpawned: "CheckOfLegends",
        },
    },
    {
        "name": "Caves",
        "logic": CavesLogic,
        "bananas": CavesBananas,
        "entry_region": Regions.CrystalCavesEntryHandler,
        "special_requirements": {
            RemovedBarriersSelected.caves_ice_walls: "CavesIceWalls",
            RemovedBarriersSelected.caves_igloo_pads: "CavesIglooPads",
        },
    },
    {
        "name": "Castle",
        "logic": CastleLogic,
        "bananas": CastleBananas,
        "entry_region": Regions.CreepyCastleEntryHandler,
        "special_requirements": {
            RemovedBarriersSelected.castle_crypt_doors: "CastleCryptDoors",
        },
    },
]

if __name__ == "__main__":
    output = "const requirement_data = {\n"
    for level in LEVELS:
        requirements = [*BASE_REQUIREMENTS, *level["special_requirements"].keys()]

        print("Evaluating level", level["name"])

        regions = flatten_graph(level["logic"], level["bananas"], requirements)

        region_requirements, event_requirements = traverse_graph(regions, level["entry_region"])

        cb_requirements = compute_cb_requirements(regions, region_requirements, event_requirements)

        output += f'    "{level["name"]}": {{\n'
        output += to_javascript(cb_requirements, level["special_requirements"])
        output += "    },\n"
    output += "}\n"
    with open("requirement_data.js", "w") as f:
        f.write(output)
