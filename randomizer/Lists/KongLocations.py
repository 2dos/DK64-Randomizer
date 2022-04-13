"""Stores the requirements for kong free location."""
from randomizer.MapsAndExits import Maps


class KongLocation:
    """Class which stores data for a kong location."""

    def __init__(self, name, kong_placement, kongs_who_can_free):
        """Initialize with given parameters."""
        self.name = name
        self.free = kong_placement
        self.puzzle_kong = kongs_who_can_free
        self.base_free = kong_placement
        self.base_puzzle_kong = kongs_who_can_free
        self.kong_placed = 0
        self.kong_puzzle = 0
        self.assigned_locked = False
        self.assigned_puzzle = False


KongRequirements = {
    Maps.TrainingGrounds: KongLocation("Starting Kong", [0, 1, 2, 3, 4], []),
    Maps.JungleJapes: KongLocation("Jungle Japes", [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
    Maps.AztecLlamaTemple: KongLocation("Llama Temple", [0, 1, 2, 3, 4], [0, 1, 2, 3, 4]),
    Maps.AztecTinyTemple: KongLocation("Tiny Temple", [0, 2, 3, 4], [1]),
    Maps.FranticFactory: KongLocation("Frantic Factory", [0, 1, 2, 3, 4], [2, 3]),
}
