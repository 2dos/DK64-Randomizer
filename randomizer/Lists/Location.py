# fmt: off
"""Stores the Location class and a list of each location in the game."""

from randomizer.Enums.Items import Items
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Locations import Locations
from randomizer.Enums.MoveTypes import MoveTypes
from randomizer.Enums.Types import Types
from randomizer.Lists.MapsAndExits import Maps
from randomizer.Enums.VendorType import VendorType


class MapIDCombo:
    """A combination of a map and an associated item ID. If id == -1 and map == 0, has no model 2 item, ignore those."""

    def __init__(self, map=None, id=None, flag=None, kong=Kongs.any):
        """Initialize with given parameters."""
        self.map = map
        self.id = id
        self.flag = flag
        self.kong = kong


class Location:
    """A shufflable location at which a random item can be placed."""

    def __init__(self, level, name, default, location_type, kong=Kongs.any, data=None):
        """Initialize with given parameters."""
        if data is None:
            data = []
        self.name = name
        self.default = default
        self.type = location_type
        self.item = None
        self.delayedItem = None
        self.constant = False
        self.is_reward = False
        self.map_id_list = None
        self.level = level
        self.kong = kong
        self.placement_index = None
        if self.type == Types.Shop:
            self.movetype = data[0]
            self.index = data[1]
            self.vendor = data[2]
            lvl_index = self.level
            if lvl_index == Levels.DKIsles:
                lvl_index = 7
            lst = []
            if self.kong < 5:
                lst.append((self.vendor * 40) + (self.kong * 8) + lvl_index)
            else:
                for kong_index in range(5):
                    lst.append((self.vendor * 40) + (kong_index * 8) + lvl_index)
            self.placement_index = lst
        elif self.type in (Types.TrainingBarrel, Types.Shockwave):
            self.placement_index = [data[0]]
        elif self.type == Types.Blueprint:
            self.map = data[0]
            level_index = int(self.level)
            if self.level in (Levels.DKIsles, Levels.HideoutHelm):
                level_index = 7
            self.map_id_list = [MapIDCombo(0, -1, 469 + self.kong + (5 * level_index), self.kong)]
        elif self.type == Types.Medal and self.level != Levels.HideoutHelm:
            level_index = int(self.level)
            if self.level in (Levels.DKIsles, Levels.HideoutHelm):
                level_index = 7
            self.map_id_list = [MapIDCombo(0, -1, 549 + self.kong + (5 * level_index), self.kong)]
        elif self.type in (Types.Banana, Types.Key, Types.Coin, Types.Crown, Types.Medal):
            if data is None:
                self.map_id_list = []
            else:
                self.map_id_list = data
        self.default_mapid_data = self.map_id_list
        # "Reward" locations are locations that require an actor to exist for the location's item - something not all items have
        if self.default_mapid_data is not None and len(self.default_mapid_data) > 0 and type(self.default_mapid_data[0]) is MapIDCombo and self.default_mapid_data[0].id == -1:
            self.is_reward = True

    def PlaceItem(self, item):
        """Place item at this location."""
        self.item = item
        # If we're placing a real move here, lock out mutually exclusive shop locations
        if item != Items.NoItem and self.type == Types.Shop:
            for location in ShopLocationReference[self.level][self.vendor]:
                # If this is a shared spot, lock out kong-specific locations in this shop
                if self.kong == Kongs.any and LocationList[location].kong != Kongs.any:
                    LocationList[location].PlaceItem(Items.NoItem)
                # If this is a kong-specific spot, lock out the shared location in this shop
                if self.kong != Kongs.any and LocationList[location].kong == Kongs.any:
                    LocationList[location].PlaceItem(Items.NoItem)
                    break  # There's only one shared spot to block

    def PlaceConstantItem(self, item):
        """Place item at this location, and set constant so it's ignored in the spoiler."""
        self.PlaceItem(item)
        self.constant = True

    def SetDelayedItem(self, item):
        """Set an item to be added back later."""
        self.delayedItem = item

    def PlaceDelayedItem(self):
        """Place the delayed item at this location."""
        self.PlaceItem(self.delayedItem)
        self.delayedItem = None

    def PlaceDefaultItem(self):
        """Place whatever this location's default (vanilla) item is at it."""
        self.PlaceItem(self.default)
        self.constant = True


LocationList = {
    # DK Isles locations
    Locations.IslesVinesTrainingBarrel: Location(Levels.DKIsles, "Isles Vines Training Barrel", Items.Vines, Types.TrainingBarrel, Kongs.any, [123]),
    Locations.IslesSwimTrainingBarrel: Location(Levels.DKIsles, "Isles Swim Training Barrel", Items.Swim, Types.TrainingBarrel, Kongs.any, [120]),
    Locations.IslesOrangesTrainingBarrel: Location(Levels.DKIsles, "Isles Oranges Training Barrel", Items.Oranges, Types.TrainingBarrel, Kongs.any, [121]),
    Locations.IslesBarrelsTrainingBarrel: Location(Levels.DKIsles, "Isles Barrels Training Barrel", Items.Barrels, Types.TrainingBarrel, Kongs.any, [122]),
    Locations.IslesDonkeyJapesRock: Location(Levels.DKIsles, "Isles Donkey Japes Rock", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.Isles, 0x4, 381, Kongs.donkey)]),  # Can be assigned to other kongs
    Locations.IslesTinyCagedBanana: Location(Levels.DKIsles, "Isles Tiny Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.Isles, 0x2B, 420, Kongs.tiny)]),
    Locations.IslesTinyInstrumentPad: Location(Levels.DKIsles, "Isles Tiny Instrument Pad", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 425, Kongs.tiny)]),
    Locations.IslesLankyCagedBanana: Location(Levels.DKIsles, "Isles Lanky Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.Isles, 0x2F, 421, Kongs.lanky)]),
    Locations.IslesChunkyCagedBanana: Location(Levels.DKIsles, "Isles Chunky Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.Isles, 0x2D, 422, Kongs.chunky)]),
    Locations.IslesChunkyInstrumentPad: Location(Levels.DKIsles, "Isles Chunky Instrument Pad", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 424, Kongs.chunky)]),
    Locations.IslesChunkyPoundtheX: Location(Levels.DKIsles, "Isles Chunky Pound the X", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.Isles, 0x56, 431, Kongs.chunky)]),
    Locations.IslesBananaFairyIsland: Location(Levels.DKIsles, "Isles Banana Fairy Island", Items.BananaFairy, Types.Fairy),
    Locations.IslesBananaFairyCrocodisleIsle: Location(Levels.DKIsles, "Isles Banana Fairy Crocodisle Isle", Items.BananaFairy, Types.Fairy),
    Locations.IslesLankyPrisonOrangsprint: Location(Levels.DKIsles, "Isles Lanky Prison Orangsprint", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.KLumsy, 0x3, 429, Kongs.lanky)]),
    Locations.CameraAndShockwave: Location(Levels.DKIsles, "Camera and Shockwave", Items.CameraAndShockwave, Types.Shockwave, Kongs.tiny, [124]),
    Locations.RarewareBanana: Location(Levels.DKIsles, "Rareware Banana", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.BananaFairyRoom, 0x1E, 301, Kongs.tiny)]),
    Locations.IslesLankyInstrumentPad: Location(Levels.DKIsles, "Isles Lanky Instrument Pad", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 398, Kongs.lanky)]),
    Locations.IslesTinyAztecLobby: Location(Levels.DKIsles, "Isles Tiny Aztec Lobby", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 402, Kongs.tiny)]),
    Locations.IslesDonkeyCagedBanana: Location(Levels.DKIsles, "Isles Donkey Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.Isles, 0x4D, 419, Kongs.donkey)]),
    Locations.IslesDiddySnidesLobby: Location(Levels.DKIsles, "Isles Diddy Snides Lobby", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 416, Kongs.diddy)]),
    Locations.IslesBattleArena1: Location(Levels.DKIsles, "Isles Battle Arena 1", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.SnidesCrown, -1, 615)]),
    Locations.IslesDonkeyInstrumentPad: Location(Levels.DKIsles, "Isles Donkey Instrument Pad", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(0, -1, 404, Kongs.donkey)]),
    Locations.IslesKasplatFactoryLobby: Location(Levels.DKIsles, "Isles Kasplat Frantic Factory Lobby", Items.DKIslesTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.FranticFactoryLobby]),
    Locations.IslesBananaFairyFactoryLobby: Location(Levels.DKIsles, "Isles Banana Fairy Factory Lobby", Items.BananaFairy, Types.Fairy),
    Locations.IslesTinyGalleonLobby: Location(Levels.DKIsles, "Isles Tiny Galleon Lobby", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.GloomyGalleonLobby, 0x9, 403)]),
    Locations.IslesKasplatGalleonLobby: Location(Levels.DKIsles, "Isles Kasplat Gloomy Galleon Lobby", Items.DKIslesChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.GloomyGalleonLobby]),
    Locations.IslesDiddyCagedBanana: Location(Levels.DKIsles, "Isles Diddy Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.Isles, 0x2E, 423, Kongs.diddy)]),
    Locations.IslesDiddySummit: Location(Levels.DKIsles, "Isles Diddy Summit", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 428, Kongs.diddy)]),
    Locations.IslesBattleArena2: Location(Levels.DKIsles, "Isles Battle Arena 2", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.LobbyCrown, -1, 614)]),
    Locations.IslesBananaFairyForestLobby: Location(Levels.DKIsles, "Isles Banana Fairy Forest Lobby", Items.BananaFairy, Types.Fairy),
    Locations.IslesDonkeyLavaBanana: Location(Levels.DKIsles, "Isles Donkey Lava Banana", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CrystalCavesLobby, 0x5, 411, Kongs.donkey)]),
    Locations.IslesDiddyInstrumentPad: Location(Levels.DKIsles, "Isles Diddy Instrument Pad", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 410, Kongs.diddy)]),
    Locations.IslesKasplatCavesLobby: Location(Levels.DKIsles, "Isles Kasplat Crystal Caves Lobby", Items.DKIslesLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.CrystalCavesLobby]),
    Locations.IslesLankyCastleLobby: Location(Levels.DKIsles, "Isles Lanky Castle Lobby", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 415, Kongs.lanky)]),
    Locations.IslesKasplatCastleLobby: Location(Levels.DKIsles, "Isles Kasplat Creepy Castle Lobby", Items.DKIslesDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.CreepyCastleLobby]),
    Locations.IslesChunkyHelmLobby: Location(Levels.DKIsles, "Isles Chunky Helm Lobby", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 406, Kongs.chunky)]),
    Locations.IslesKasplatHelmLobby: Location(Levels.DKIsles, "Isles Kasplat Hideout Helm Lobby", Items.DKIslesDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.HideoutHelmLobby]),
    Locations.BananaHoard: Location(Levels.DKIsles, "Banana Hoard", Items.BananaHoard, Types.Constant),
    # Jungle Japes location
    Locations.JapesDonkeyMedal: Location(Levels.JungleJapes, "Japes Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.JapesDiddyMedal: Location(Levels.JungleJapes, "Japes Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.JapesLankyMedal: Location(Levels.JungleJapes, "Japes Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.JapesTinyMedal: Location(Levels.JungleJapes, "Japes Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.JapesChunkyMedal: Location(Levels.JungleJapes, "Japes Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.DiddyKong: Location(Levels.JungleJapes, "Diddy Kong", Items.Diddy, Types.Kong),
    Locations.JapesDonkeyFrontofCage: Location(Levels.JungleJapes, "Japes Donkey Front of Cage", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.JungleJapes, 0x69, 4, Kongs.donkey)]),  # Can be assigned to other kongs
    Locations.JapesDonkeyFreeDiddy: Location(Levels.JungleJapes, "Japes Donkey Free Diddy", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.JungleJapes, 0x48, 5, Kongs.donkey)]),  # Can be assigned to other kongs
    Locations.JapesDonkeyCagedBanana: Location(Levels.JungleJapes, "Japes Donkey Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.JungleJapes, 0x44, 20, Kongs.donkey)]),
    Locations.JapesDonkeyBaboonBlast: Location(Levels.JungleJapes, "Japes Donkey Baboon Blast", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.JapesBaboonBlast, 1, 3, Kongs.donkey)]),
    Locations.JapesDiddyCagedBanana: Location(Levels.JungleJapes, "Japes Diddy Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.JungleJapes, 0x4D, 18, Kongs.diddy)]),
    Locations.JapesDiddyMountain: Location(Levels.JungleJapes, "Japes Diddy Mountain", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.JungleJapes, 0x52, 23, Kongs.diddy)]),
    Locations.JapesLankyCagedBanana: Location(Levels.JungleJapes, "Japes Lanky Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.JungleJapes, 0x4F, 19, Kongs.lanky)]),
    Locations.JapesTinyCagedBanana: Location(Levels.JungleJapes, "Japes Tiny Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.JungleJapes, 0x4C, 21, Kongs.tiny)]),
    Locations.JapesChunkyBoulder: Location(Levels.JungleJapes, "Japes Chunky Boulder", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 25, Kongs.chunky)]),
    Locations.JapesChunkyCagedBanana: Location(Levels.JungleJapes, "Japes Chunky Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.JungleJapes, 0x50, 22, Kongs.chunky)]),
    Locations.JapesBattleArena: Location(Levels.JungleJapes, "Japes Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.JapesCrown, -1, 609)]),
    Locations.JapesDiddyTunnel: Location(Levels.JungleJapes, "Japes Diddy Tunnel", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.JungleJapes, 0x1E, 31, Kongs.diddy)]),
    Locations.JapesLankyGrapeGate: Location(Levels.JungleJapes, "Japes Lanky Grape Gate", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 1, Kongs.lanky)]),
    Locations.JapesTinyFeatherGateBarrel: Location(Levels.JungleJapes, "Japes Tiny Feather Gate Barrel", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 2, Kongs.tiny)]),
    Locations.JapesKasplatLeftTunnelNear: Location(Levels.JungleJapes, "Japes Kasplat Left Tunnel (Near)", Items.JungleJapesDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.JungleJapes]),
    Locations.JapesKasplatLeftTunnelFar: Location(Levels.JungleJapes, "Japes Kasplat Left Tunnel (Far)", Items.JungleJapesTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.JungleJapes]),
    Locations.JapesTinyStump: Location(Levels.JungleJapes, "Japes Tiny Stump", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.JungleJapes, 0x68, 8, Kongs.tiny)]),
    Locations.JapesChunkyGiantBonusBarrel: Location(Levels.JungleJapes, "Japes Chunky Giant Bonus Barrel", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 28, Kongs.chunky)]),
    Locations.JapesTinyBeehive: Location(Levels.JungleJapes, "Japes Tiny Beehive", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.JapesTinyHive, 0x3F, 9, Kongs.tiny)]),
    Locations.JapesLankySlope: Location(Levels.JungleJapes, "Japes Lanky Slope", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 11, Kongs.lanky)]),
    Locations.JapesKasplatNearPaintingRoom: Location(Levels.JungleJapes, "Japes Kasplat Near Painting Room", Items.JungleJapesDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.JungleJapes]),
    Locations.JapesKasplatNearLab: Location(Levels.JungleJapes, "Japes Kasplat Near Cranky's Lab", Items.JungleJapesLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.JungleJapes]),
    Locations.JapesBananaFairyRambiCave: Location(Levels.JungleJapes, "Japes Banana Fairy Rambi Cave", Items.BananaFairy, Types.Fairy),
    Locations.JapesLankyFairyCave: Location(Levels.JungleJapes, "Japes Lanky Fairy Cave", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.JapesLankyCave, 0x4, 10, Kongs.lanky)]),
    Locations.JapesBananaFairyLankyCave: Location(Levels.JungleJapes, "Japes Banana Fairy Lanky Cave", Items.BananaFairy, Types.Fairy),
    Locations.JapesDiddyMinecarts: Location(Levels.JungleJapes, "Japes Diddy Minecarts", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 24, Kongs.diddy)]),
    Locations.JapesChunkyUnderground: Location(Levels.JungleJapes, "Japes Chunky Underground", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.JapesUnderGround, 0x3, 12, Kongs.chunky)]),
    Locations.JapesKasplatUnderground: Location(Levels.JungleJapes, "Japes Kasplat Underground", Items.JungleJapesChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.JapesUnderGround]),
    Locations.JapesKey: Location(Levels.JungleJapes, "Japes Boss Defeated", Items.JungleJapesKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 26)]),  # Can be assigned to any kong
    # Angry Aztec
    Locations.AztecDonkeyMedal: Location(Levels.AngryAztec, "Aztec Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.AztecDiddyMedal: Location(Levels.AngryAztec, "Aztec Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.AztecLankyMedal: Location(Levels.AngryAztec, "Aztec Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.AztecTinyMedal: Location(Levels.AngryAztec, "Aztec Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.AztecChunkyMedal: Location(Levels.AngryAztec, "Aztec Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.AztecDonkeyFreeLlama: Location(Levels.AngryAztec, "Aztec Donkey Free Llama", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.AngryAztec, 0x26, 51, Kongs.donkey)]),
    Locations.AztecChunkyVases: Location(Levels.AngryAztec, "Aztec Chunky Vases", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.AngryAztec, 0x23, 49, Kongs.chunky)]),
    Locations.AztecKasplatSandyBridge: Location(Levels.AngryAztec, "Aztec Kasplat Sandy Bridge", Items.AngryAztecDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.AngryAztec]),
    Locations.AztecKasplatOnTinyTemple: Location(Levels.AngryAztec, "Aztec Kasplat On Tiny Temple", Items.AngryAztecDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.AngryAztec]),
    Locations.AztecTinyKlaptrapRoom: Location(Levels.AngryAztec, "Aztec Tiny Klaptrap Room", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.AztecTinyTemple, 0x7E, 65, Kongs.tiny)]),
    Locations.AztecChunkyKlaptrapRoom: Location(Levels.AngryAztec, "Aztec Chunky Klaptrap Room", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.AztecTinyTemple, 0x9, 64, Kongs.chunky)]),
    Locations.TinyKong: Location(Levels.AngryAztec, "Tiny Kong", Items.Tiny, Types.Kong),
    Locations.AztecDiddyFreeTiny: Location(Levels.AngryAztec, "Aztec Diddy Free Tiny", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.AztecTinyTemple, 0x5B, 67, Kongs.diddy)]),  # Can be assigned to other kongs
    Locations.AztecLankyVulture: Location(Levels.AngryAztec, "Aztec Lanky Vulture", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 68, Kongs.lanky)]),
    Locations.AztecBattleArena: Location(Levels.AngryAztec, "Aztec Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.AztecCrown, -1, 610)]),
    Locations.AztecDonkeyQuicksandCave: Location(Levels.AngryAztec, "Aztec Donkey Quicksand Cave", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(0, -1, 62, Kongs.donkey)]),
    Locations.AztecDiddyRamGongs: Location(Levels.AngryAztec, "Aztec Diddy Ram Gongs", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.AngryAztec, 0xA3, 54, Kongs.diddy)]),
    Locations.AztecDiddyVultureRace: Location(Levels.AngryAztec, "Aztec Diddy Vulture Race", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.AngryAztec, 0xEB, 63, Kongs.diddy)]),
    Locations.AztecChunkyCagedBarrel: Location(Levels.AngryAztec, "Aztec Chunky Caged Barrel", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 52, Kongs.chunky)]),
    Locations.AztecKasplatNearLab: Location(Levels.AngryAztec, "Aztec Kasplat Near Cranky's Lab", Items.AngryAztecTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.AngryAztec]),
    Locations.AztecDonkey5DoorTemple: Location(Levels.AngryAztec, "Aztec Donkey 5 Door Temple", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.AztecDonkey5DTemple, 0x6, 57, Kongs.donkey)]),
    Locations.AztecDiddy5DoorTemple: Location(Levels.AngryAztec, "Aztec Diddy 5 Door Temple", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.AztecDiddy5DTemple, 0x6, 56, Kongs.diddy)]),
    Locations.AztecLanky5DoorTemple: Location(Levels.AngryAztec, "Aztec Lanky 5 Door Temple", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 60, Kongs.lanky)]),
    Locations.AztecTiny5DoorTemple: Location(Levels.AngryAztec, "Aztec Tiny 5 Door Temple", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.AztecTiny5DTemple, 0x6, 58, Kongs.tiny)]),
    Locations.AztecBananaFairyTinyTemple: Location(Levels.AngryAztec, "Aztec Banana Fairy Tiny Temple", Items.BananaFairy, Types.Fairy),
    Locations.AztecChunky5DoorTemple: Location(Levels.AngryAztec, "Aztec Chunky 5 Door Temple", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 59, Kongs.chunky)]),
    Locations.AztecKasplatChunky5DT: Location(Levels.AngryAztec, "Aztec Kasplat Inside Chunky's 5-Door Temple", Items.AngryAztecChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.AztecChunky5DTemple]),
    Locations.AztecTinyBeetleRace: Location(Levels.AngryAztec, "Aztec Tiny Beetle Race", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.AztecTinyRace, 0x48, 75, Kongs.tiny)]),
    Locations.LankyKong: Location(Levels.AngryAztec, "Lanky Kong", Items.Lanky, Types.Kong),
    Locations.AztecDonkeyFreeLanky: Location(Levels.AngryAztec, "Aztec Donkey Free Lanky", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.AztecLlamaTemple, 0x6C, 77, Kongs.donkey)]),  # Can be assigned to other kongs
    Locations.AztecLankyLlamaTempleBarrel: Location(Levels.AngryAztec, "Aztec Lanky Llama Temple Barrel", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 73, Kongs.lanky)]),
    Locations.AztecLankyMatchingGame: Location(Levels.AngryAztec, "Aztec Lanky Matching Game", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.AztecLlamaTemple, 0x2B, 72, Kongs.lanky)]),
    Locations.AztecBananaFairyLlamaTemple: Location(Levels.AngryAztec, "Aztec Banana Fairy Llama Temple", Items.BananaFairy, Types.Fairy),
    Locations.AztecTinyLlamaTemple: Location(Levels.AngryAztec, "Aztec Tiny Llama Temple", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.AztecLlamaTemple, 0xAA, 71, Kongs.tiny)]),
    Locations.AztecKasplatLlamaTemple: Location(Levels.AngryAztec, "Aztec Kasplat Inside Llama Temple", Items.AngryAztecLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.AztecLlamaTemple]),
    Locations.AztecKey: Location(Levels.AngryAztec, "Aztec Boss Defeated", Items.AngryAztecKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 74)]),  # Can be assigned to any kong
    # Frantic Factory locations
    Locations.FactoryDonkeyMedal: Location(Levels.FranticFactory, "Factory Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.FactoryDiddyMedal: Location(Levels.FranticFactory, "Factory Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.FactoryLankyMedal: Location(Levels.FranticFactory, "Factory Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.FactoryTinyMedal: Location(Levels.FranticFactory, "Factory Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.FactoryChunkyMedal: Location(Levels.FranticFactory, "Factory Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.FactoryDonkeyNumberGame: Location(Levels.FranticFactory, "Factory Donkey Number Game", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FranticFactory, 0x7E, 122, Kongs.donkey)]),
    Locations.FactoryDiddyBlockTower: Location(Levels.FranticFactory, "Factory Diddy Block Tower", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 135, Kongs.diddy)]),
    Locations.FactoryLankyTestingRoomBarrel: Location(Levels.FranticFactory, "Factory Lanky Testing Room Barrel", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 137, Kongs.lanky)]),
    Locations.FactoryTinyDartboard: Location(Levels.FranticFactory, "Factory Tiny Dartboard", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.FranticFactory, 0x82, 124, Kongs.tiny)]),
    Locations.FactoryKasplatBlocks: Location(Levels.FranticFactory, "Factory Kasplat Block Tower Room", Items.FranticFactoryChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.FranticFactory]),
    Locations.FactoryBananaFairybyCounting: Location(Levels.FranticFactory, "Factory Banana Fairy by Counting", Items.BananaFairy, Types.Fairy),
    Locations.FactoryBananaFairybyFunky: Location(Levels.FranticFactory, "Factory Banana Fairy by Funky", Items.BananaFairy, Types.Fairy),
    Locations.FactoryDiddyRandD: Location(Levels.FranticFactory, "Factory Diddy Research and Development", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.FranticFactory, 0x60, 126, Kongs.diddy)]),
    Locations.FactoryLankyRandD: Location(Levels.FranticFactory, "Factory Lanky Research and Development", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.FranticFactory, 0x3E, 125, Kongs.lanky)]),
    Locations.FactoryChunkyRandD: Location(Levels.FranticFactory, "Factory Chunky Research and Development", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.FranticFactory, 0x7C, 127, Kongs.chunky)]),
    Locations.FactoryKasplatRandD: Location(Levels.FranticFactory, "Factory Kasplat Research and Development", Items.FranticFactoryLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.FranticFactory]),
    Locations.FactoryBattleArena: Location(Levels.FranticFactory, "Factory Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.FactoryCrown, -1, 611)]),
    Locations.FactoryTinyCarRace: Location(Levels.FranticFactory, "Factory Tiny Car Race", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.FactoryTinyRace, 0x62, 139, Kongs.tiny)]),
    Locations.FactoryDiddyChunkyRoomBarrel: Location(Levels.FranticFactory, "Factory Diddy Chunky Room Barrel", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 134, Kongs.diddy)]),
    Locations.FactoryDonkeyPowerHut: Location(Levels.FranticFactory, "Factory Donkey Power Hut", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FactoryPowerHut, 0x2, 112, Kongs.donkey)]),
    Locations.ChunkyKong: Location(Levels.FranticFactory, "Chunky Kong", Items.Chunky, Types.Kong),
    Locations.NintendoCoin: Location(Levels.FranticFactory, "Nintendo Coin", Items.NintendoCoin, Types.Coin, Kongs.donkey, [MapIDCombo(Maps.FranticFactory, 0x13E, 132)]),
    Locations.FactoryDonkeyDKArcade: Location(Levels.FranticFactory, "Factory Donkey DK Arcade", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FranticFactory, 0x108, 130, Kongs.donkey), MapIDCombo(Maps.FactoryBaboonBlast, 0, 130, Kongs.donkey)]),
    Locations.FactoryLankyFreeChunky: Location(Levels.FranticFactory, "Factory Lanky Free Chunky", Items.GoldenBanana, Types.Banana, Kongs.any, [MapIDCombo(Maps.FranticFactory, 0x78, 118, Kongs.lanky)]),  # Can be assigned to other kongs
    Locations.FactoryTinybyArcade: Location(Levels.FranticFactory, "Factory Tiny by Arcade", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.FranticFactory, 0x23, 123, Kongs.tiny)]),
    Locations.FactoryChunkyDarkRoom: Location(Levels.FranticFactory, "Factory Chunky Dark Room", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.FranticFactory, 0x63, 121, Kongs.chunky)]),
    Locations.FactoryChunkybyArcade: Location(Levels.FranticFactory, "Factory Chunky by Arcade", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 136, Kongs.chunky)]),
    Locations.FactoryKasplatProductionBottom: Location(Levels.FranticFactory, "Factory Kasplat Bottom of Production Room", Items.FranticFactoryDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.FranticFactory]),
    Locations.FactoryKasplatStorage: Location(Levels.FranticFactory, "Factory Kasplat Storage Room", Items.FranticFactoryTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.FranticFactory, Kongs.tiny]),
    Locations.FactoryDonkeyCrusherRoom: Location(Levels.FranticFactory, "Factory Donkey Crusher Room", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FactoryCrusher, 0x7, 128, Kongs.donkey)]),
    Locations.FactoryDiddyProductionRoom: Location(Levels.FranticFactory, "Factory Diddy Production Room", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.FranticFactory, 0x2C, 113, Kongs.diddy)]),
    Locations.FactoryLankyProductionRoom: Location(Levels.FranticFactory, "Factory Lanky Production Room", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.FranticFactory, 0x2A, 115, Kongs.lanky)]),
    Locations.FactoryTinyProductionRoom: Location(Levels.FranticFactory, "Factory Tiny Production Room", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 116, Kongs.tiny)]),
    Locations.FactoryChunkyProductionRoom: Location(Levels.FranticFactory, "Factory Chunky Production Room", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.FranticFactory, 0x29, 114, Kongs.chunky)]),
    Locations.FactoryKasplatProductionTop: Location(Levels.FranticFactory, "Factory Kasplat Top of Production Room", Items.FranticFactoryDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.FranticFactory]),
    Locations.FactoryKey: Location(Levels.FranticFactory, "Factory Boss Defeated", Items.FranticFactoryKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 138)]),  # Can be assigned to any kong
    # Gloomy Galleon locations
    Locations.GalleonDonkeyMedal: Location(Levels.GloomyGalleon, "Galleon Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.GalleonDiddyMedal: Location(Levels.GloomyGalleon, "Galleon Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.GalleonLankyMedal: Location(Levels.GloomyGalleon, "Galleon Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.GalleonTinyMedal: Location(Levels.GloomyGalleon, "Galleon Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.GalleonChunkyMedal: Location(Levels.GloomyGalleon, "Galleon Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.GalleonChunkyChest: Location(Levels.GloomyGalleon, "Galleon Chunky Chest", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.GloomyGalleon, 0xE, 182, Kongs.chunky)]),
    Locations.GalleonKasplatNearLab: Location(Levels.GloomyGalleon, "Galleon Kasplat Near Cranky's Lab", Items.GloomyGalleonTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.GloomyGalleon]),
    Locations.GalleonBattleArena: Location(Levels.GloomyGalleon, "Galleon Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.GalleonCrown, -1, 612)]),
    Locations.GalleonBananaFairybyCranky: Location(Levels.GloomyGalleon, "Galleon Banana Fairy by Cranky", Items.BananaFairy, Types.Fairy),
    Locations.GalleonChunkyCannonGame: Location(Levels.GloomyGalleon, "Galleon Chunky Cannon Game", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.GloomyGalleon, 0x32, 154, Kongs.chunky)]),
    Locations.GalleonKasplatCannons: Location(Levels.GloomyGalleon, "Galleon Kasplat Cannon Room", Items.GloomyGalleonLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.GloomyGalleon]),
    Locations.GalleonDiddyShipSwitch: Location(Levels.GloomyGalleon, "Galleon Diddy Ship Switch", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.GloomyGalleon, 0x2D, 204, Kongs.diddy)]),
    Locations.GalleonLankyEnguardeChest: Location(Levels.GloomyGalleon, "Galleon Lanky Enguarde Chest", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.GloomyGalleon, 0x6B, 192, Kongs.lanky)]),
    Locations.GalleonKasplatLighthouseArea: Location(Levels.GloomyGalleon, "Galleon Kasplat Lighthouse Area", Items.GloomyGalleonDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.GloomyGalleon]),
    Locations.GalleonDonkeyLighthouse: Location(Levels.GloomyGalleon, "Galleon Donkey Lighthouse", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.GalleonLighthouse, 0x2F, 157, Kongs.donkey)]),
    Locations.GalleonTinyPearls: Location(Levels.GloomyGalleon, "Galleon Tiny Pearls", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.GalleonMermaidRoom, 0xE, 191, Kongs.tiny)]),
    Locations.GalleonChunkySeasick: Location(Levels.GloomyGalleon, "Galleon Chunky Seasick", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.GalleonSickBay, 0x6, 166, Kongs.chunky)]),
    Locations.GalleonDonkeyFreetheSeal: Location(Levels.GloomyGalleon, "Galleon Donkey Free the Seal", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.GloomyGalleon, 0x2E, 193, Kongs.donkey)]),
    Locations.GalleonKasplatNearSub: Location(Levels.GloomyGalleon, "Galleon Kasplat Near Submarine", Items.GloomyGalleonChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.GloomyGalleon]),
    Locations.GalleonDonkeySealRace: Location(Levels.GloomyGalleon, "Galleon Donkey Seal Race", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.GalleonSealRace, 0x3B, 165, Kongs.donkey)]),
    Locations.GalleonDiddyGoldTower: Location(Levels.GloomyGalleon, "Galleon Diddy Gold Tower", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 163, Kongs.diddy)]),
    Locations.GalleonLankyGoldTower: Location(Levels.GloomyGalleon, "Galleon Lanky Gold Tower", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 164, Kongs.lanky)]),
    Locations.GalleonKasplatGoldTower: Location(Levels.GloomyGalleon, "Galleon Kasplat Gold Tower Room", Items.GloomyGalleonDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.GloomyGalleon]),
    Locations.GalleonTinySubmarine: Location(Levels.GloomyGalleon, "Galleon Tiny Submarine", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 202, Kongs.tiny)]),
    Locations.GalleonDiddyMechafish: Location(Levels.GloomyGalleon, "Galleon Diddy Mechafish", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.GalleonMechafish, 0xF, 167, Kongs.diddy)]),
    Locations.GalleonLanky2DoorShip: Location(Levels.GloomyGalleon, "Galleon Lanky 2 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.Galleon2DShip, 0x0, 183, Kongs.lanky)]),
    Locations.GalleonTiny2DoorShip: Location(Levels.GloomyGalleon, "Galleon Tiny 2 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 184, Kongs.tiny)]),
    Locations.GalleonDonkey5DoorShip: Location(Levels.GloomyGalleon, "Galleon Donkey 5 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(0, -1, 200, Kongs.donkey)]),
    Locations.GalleonDiddy5DoorShip: Location(Levels.GloomyGalleon, "Galleon Diddy 5 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 198, Kongs.diddy)]),
    Locations.GalleonLanky5DoorShip: Location(Levels.GloomyGalleon, "Galleon Lanky 5 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.Galleon5DShipDiddyLankyChunky, 0xE, 199, Kongs.lanky)]),
    Locations.GalleonTiny5DoorShip: Location(Levels.GloomyGalleon, "Galleon Tiny 5 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.Galleon5DShipDKTiny, 0x21, 201, Kongs.tiny)]),
    Locations.GalleonBananaFairy5DoorShip: Location(Levels.GloomyGalleon, "Galleon Banana Fairy 5 Door Ship", Items.BananaFairy, Types.Fairy),
    Locations.GalleonChunky5DoorShip: Location(Levels.GloomyGalleon, "Galleon Chunky 5 Door Ship", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 197, Kongs.chunky)]),
    Locations.GalleonKey: Location(Levels.GloomyGalleon, "Galleon Boss Defeated", Items.GloomyGalleonKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 168)]),  # Can be assigned to any kong
    # Fungi Forest locations
    Locations.ForestDonkeyMedal: Location(Levels.FungiForest, "Forest Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.ForestDiddyMedal: Location(Levels.FungiForest, "Forest Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.ForestLankyMedal: Location(Levels.FungiForest, "Forest Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.ForestTinyMedal: Location(Levels.FungiForest, "Forest Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.ForestChunkyMedal: Location(Levels.FungiForest, "Forest Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.ForestChunkyMinecarts: Location(Levels.FungiForest, "Forest Chunky Minecarts", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 215, Kongs.chunky)]),
    Locations.ForestDiddyTopofMushroom: Location(Levels.FungiForest, "Forest Diddy Top of Mushroom", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 211, Kongs.diddy)]),
    Locations.ForestTinyMushroomBarrel: Location(Levels.FungiForest, "Forest Tiny Mushroom Barrel", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 227, Kongs.tiny)]),
    Locations.ForestDonkeyBaboonBlast: Location(Levels.FungiForest, "Forest Donkey Baboon Blast", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FungiForest, 0x39, 254, Kongs.donkey)]),
    Locations.ForestKasplatLowerMushroomExterior: Location(Levels.FungiForest, "Forest Kasplat Lower Giant Mushroom Exterior", Items.FungiForestTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.FungiForest]),
    Locations.ForestDonkeyMushroomCannons: Location(Levels.FungiForest, "Forest Donkey Mushroom Cannons", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.ForestGiantMushroom, 0x3, 228, Kongs.donkey)]),
    Locations.ForestKasplatInsideMushroom: Location(Levels.FungiForest, "Forest Kasplat Inside Giant Mushroom", Items.FungiForestDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.ForestGiantMushroom]),
    Locations.ForestKasplatUpperMushroomExterior: Location(Levels.FungiForest, "Forest Kasplat Upper Giant Mushroom Exterior", Items.FungiForestChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.FungiForest]),
    Locations.ForestBattleArena: Location(Levels.FungiForest, "Forest Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.ForestCrown, -1, 613)]),
    Locations.ForestChunkyFacePuzzle: Location(Levels.FungiForest, "Forest Chunky Face Puzzle", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.ForestChunkyFaceRoom, 0x2, 225, Kongs.chunky)]),
    Locations.ForestLankyZingers: Location(Levels.FungiForest, "Forest Lanky Zingers", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.ForestLankyZingersRoom, 0x0, 226, Kongs.lanky)]),
    Locations.ForestLankyColoredMushrooms: Location(Levels.FungiForest, "Forest Lanky Colored Mushrooms", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 224, Kongs.lanky)]),
    Locations.ForestDiddyOwlRace: Location(Levels.FungiForest, "Forest Diddy Owl Race", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 250, Kongs.diddy)]),
    Locations.ForestLankyRabbitRace: Location(Levels.FungiForest, "Forest Lanky Rabbit Race", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.FungiForest, 0x57, 249)]),
    Locations.ForestKasplatOwlTree: Location(Levels.FungiForest, "Forest Kasplat Owl Tree", Items.FungiForestLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.FungiForest]),
    Locations.ForestTinyAnthill: Location(Levels.FungiForest, "Forest Tiny Anthill", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.ForestAnthill, 0x0, 205, Kongs.tiny)]),
    Locations.ForestDonkeyMill: Location(Levels.FungiForest, "Forest Donkey Mill", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.FungiForest, 0x2B, 219, Kongs.donkey), MapIDCombo(Maps.ForestMillFront, 0xA, 219, Kongs.donkey)]),
    Locations.ForestDiddyCagedBanana: Location(Levels.FungiForest, "Forest Diddy Caged Banana", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.FungiForest, 0x28, 214, Kongs.diddy)]),
    Locations.ForestTinySpiderBoss: Location(Levels.FungiForest, "Forest Tiny Spider Boss", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.ForestSpider, 0x1, 247, Kongs.tiny)]),
    Locations.ForestChunkyKegs: Location(Levels.FungiForest, "Forest Chunky Kegs", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.ForestMillFront, 0xD, 221, Kongs.chunky)]),
    Locations.ForestDiddyRafters: Location(Levels.FungiForest, "Forest Diddy Rafters", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.ForestRafters, 0x3, 216, Kongs.diddy)]),
    Locations.ForestBananaFairyRafters: Location(Levels.FungiForest, "Forest Banana Fairy Rafters", Items.BananaFairy, Types.Fairy),
    Locations.ForestLankyAttic: Location(Levels.FungiForest, "Forest Lanky Attic", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.ForestMillAttic, 0x2, 217, Kongs.lanky)]),
    Locations.ForestKasplatNearBarn: Location(Levels.FungiForest, "Forest Kasplat Near Thorny Barn", Items.FungiForestDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.FungiForest]),
    Locations.ForestDonkeyBarn: Location(Levels.FungiForest, "Forest Donkey Barn", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(0, -1, 235, Kongs.donkey)]),
    Locations.ForestBananaFairyThornvines: Location(Levels.FungiForest, "Forest Banana Fairy Thornvines", Items.BananaFairy, Types.Fairy),
    Locations.ForestTinyBeanstalk: Location(Levels.FungiForest, "Forest Tiny Beanstalk", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.FungiForest, 0x50, 209, Kongs.tiny)]),
    Locations.ForestChunkyApple: Location(Levels.FungiForest, "Forest Chunky Apple", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.FungiForest, 0x3E, 253, Kongs.chunky)]),
    Locations.ForestKey: Location(Levels.FungiForest, "Forest Boss Defeated", Items.FungiForestKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 236)]),  # Can be assigned to any kong
    # Crystal Caves locations
    Locations.CavesDonkeyMedal: Location(Levels.CrystalCaves, "Caves Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.CavesDiddyMedal: Location(Levels.CrystalCaves, "Caves Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.CavesLankyMedal: Location(Levels.CrystalCaves, "Caves Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.CavesTinyMedal: Location(Levels.CrystalCaves, "Caves Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.CavesChunkyMedal: Location(Levels.CrystalCaves, "Caves Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.CavesDonkeyBaboonBlast: Location(Levels.CrystalCaves, "Caves Donkey Baboon Blast", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CrystalCaves, 0x32, 298, Kongs.donkey)]),
    Locations.CavesDiddyJetpackBarrel: Location(Levels.CrystalCaves, "Caves Diddy Jetpack Barrel", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 294, Kongs.diddy)]),
    Locations.CavesTinyCaveBarrel: Location(Levels.CrystalCaves, "Caves Tiny Cave Barrel", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 295, Kongs.tiny)]),
    Locations.CavesTinyMonkeyportIgloo: Location(Levels.CrystalCaves, "Caves Tiny Monkeyport Igloo", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CrystalCaves, 0x29, 297, Kongs.tiny)]),
    Locations.CavesChunkyGorillaGone: Location(Levels.CrystalCaves, "Caves Chunky Gorilla Gone", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.CrystalCaves, 0x3E, 268, Kongs.chunky)]),
    Locations.CavesKasplatNearLab: Location(Levels.CrystalCaves, "Caves Kasplat Near Cranky's Lab", Items.CrystalCavesDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.CrystalCaves]),
    Locations.CavesKasplatNearFunky: Location(Levels.CrystalCaves, "Caves Kasplat Near Funky's Hut", Items.CrystalCavesDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.CrystalCaves]),
    Locations.CavesKasplatPillar: Location(Levels.CrystalCaves, "Caves Kasplat On Large Pillar", Items.CrystalCavesLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.CrystalCaves]),
    Locations.CavesKasplatNearCandy: Location(Levels.CrystalCaves, "Caves Kasplat Near Candy's Music Shop", Items.CrystalCavesTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.CrystalCaves]),
    Locations.CavesLankyBeetleRace: Location(Levels.CrystalCaves, "Caves Lanky Beetle Race", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CavesLankyRace, 0x1, 259, Kongs.lanky)]),
    Locations.CavesLankyCastle: Location(Levels.CrystalCaves, "Caves Lanky Castle", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CavesFrozenCastle, 0x10, 271, Kongs.lanky)]),
    Locations.CavesChunkyTransparentIgloo: Location(Levels.CrystalCaves, "Caves Chunky Transparent Igloo", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.CrystalCaves, 0x28, 270, Kongs.chunky)]),
    Locations.CavesKasplatOn5DI: Location(Levels.CrystalCaves, "Caves Kasplat On 5 Door Igloo", Items.CrystalCavesChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.CrystalCaves]),
    Locations.CavesDonkey5DoorIgloo: Location(Levels.CrystalCaves, "Caves Donkey 5 Door Igloo", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CavesDonkeyIgloo, 0x1, 275, Kongs.donkey)]),
    Locations.CavesDiddy5DoorIgloo: Location(Levels.CrystalCaves, "Caves Diddy 5 Door Igloo", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.CavesDiddyIgloo, 0x1, 274, Kongs.diddy)]),
    Locations.CavesLanky5DoorIgloo: Location(Levels.CrystalCaves, "Caves Lanky 5 Door Igloo", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CavesLankyIgloo, 0x3, 281, Kongs.lanky)]),
    Locations.CavesTiny5DoorIgloo: Location(Levels.CrystalCaves, "Caves Tiny 5 Door Igloo", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CavesTinyIgloo, 0x2, 279, Kongs.tiny)]),
    Locations.CavesBananaFairyIgloo: Location(Levels.CrystalCaves, "Caves Banana Fairy Igloo", Items.BananaFairy, Types.Fairy),
    Locations.CavesChunky5DoorIgloo: Location(Levels.CrystalCaves, "Caves Chunky 5 Door Igloo", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.CavesChunkyIgloo, 0x0, 278, Kongs.chunky)]),
    Locations.CavesDonkeyRotatingCabin: Location(Levels.CrystalCaves, "Caves Donkey Rotating Cabin", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CavesRotatingCabin, 0x1, 276, Kongs.donkey)]),
    Locations.CavesBattleArena: Location(Levels.CrystalCaves, "Caves Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.CavesCrown, -1, 616)]),
    Locations.CavesDonkey5DoorCabin: Location(Levels.CrystalCaves, "Caves Donkey 5 Door Cabin", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CavesDonkeyCabin, 0x8, 261, Kongs.donkey)]),
    Locations.CavesDiddy5DoorCabinLower: Location(Levels.CrystalCaves, "Caves Diddy 5 Door Cabin Lower", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.CavesDiddyLowerCabin, 0x1, 262, Kongs.diddy)]),
    Locations.CavesDiddy5DoorCabinUpper: Location(Levels.CrystalCaves, "Caves Diddy 5 Door Cabin Upper", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.CavesDiddyUpperCabin, 0x4, 293, Kongs.diddy)]),
    Locations.CavesBananaFairyCabin: Location(Levels.CrystalCaves, "Caves Banana Fairy Cabin", Items.BananaFairy, Types.Fairy),
    Locations.CavesLanky1DoorCabin: Location(Levels.CrystalCaves, "Caves Lanky 1 Door Cabin", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CavesLankyCabin, 0x1, 264, Kongs.lanky)]),
    Locations.CavesTiny5DoorCabin: Location(Levels.CrystalCaves, "Caves Tiny 5 Door Cabin", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CavesTinyCabin, 0x0, 260, Kongs.tiny)]),
    Locations.CavesChunky5DoorCabin: Location(Levels.CrystalCaves, "Caves Chunky 5 Door Cabin", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 263, Kongs.chunky)]),
    Locations.CavesKey: Location(Levels.CrystalCaves, "Caves Boss Defeated", Items.CrystalCavesKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 292)]),  # Can be assigned to any kong
    # Creepy Castle locations
    Locations.CastleDonkeyMedal: Location(Levels.CreepyCastle, "Castle Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey),
    Locations.CastleDiddyMedal: Location(Levels.CreepyCastle, "Castle Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy),
    Locations.CastleLankyMedal: Location(Levels.CreepyCastle, "Castle Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky),
    Locations.CastleTinyMedal: Location(Levels.CreepyCastle, "Castle Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny),
    Locations.CastleChunkyMedal: Location(Levels.CreepyCastle, "Castle Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky),
    Locations.CastleDiddyAboveCastle: Location(Levels.CreepyCastle, "Castle Diddy Above Castle", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 350, Kongs.diddy)]),
    Locations.CastleKasplatHalfway: Location(Levels.CreepyCastle, "Castle Kasplat Half-way up Castle", Items.CreepyCastleLankyBlueprint, Types.Blueprint, Kongs.lanky, [Maps.CreepyCastle]),
    Locations.CastleKasplatLowerLedge: Location(Levels.CreepyCastle, "Castle Kasplat Lower Ledge", Items.CreepyCastleTinyBlueprint, Types.Blueprint, Kongs.tiny, [Maps.CreepyCastle]),
    Locations.CastleDonkeyTree: Location(Levels.CreepyCastle, "Castle Donkey Tree", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CastleTree, 0x8, 320, Kongs.donkey)]),
    Locations.CastleChunkyTree: Location(Levels.CreepyCastle, "Castle Chunky Tree", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 319, Kongs.chunky)]),
    Locations.CastleKasplatTree: Location(Levels.CreepyCastle, "Castle Kasplat Inside Tree", Items.CreepyCastleDonkeyBlueprint, Types.Blueprint, Kongs.donkey, [Maps.CastleTree]),
    Locations.CastleBananaFairyTree: Location(Levels.CreepyCastle, "Castle Banana Fairy Tree", Items.BananaFairy, Types.Fairy),
    Locations.CastleDonkeyLibrary: Location(Levels.CreepyCastle, "Castle Donkey Library", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CastleLibrary, 0x3, 313, Kongs.donkey)]),
    Locations.CastleDiddyBallroom: Location(Levels.CreepyCastle, "Castle Diddy Ballroom", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(0, -1, 305, Kongs.diddy)]),
    Locations.CastleBananaFairyBallroom: Location(Levels.CreepyCastle, "Castle Banana Fairy Ballroom", Items.BananaFairy, Types.Fairy),
    Locations.CastleTinyCarRace: Location(Levels.CreepyCastle, "Castle Tiny Car Race", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CastleTinyRace, 0x1, 325, Kongs.tiny)]),
    Locations.CastleLankyTower: Location(Levels.CreepyCastle, "Castle Lanky Tower", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 306, Kongs.lanky)]),
    Locations.CastleLankyGreenhouse: Location(Levels.CreepyCastle, "Castle Lanky Greenhouse", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CastleGreenhouse, 0x1, 323, Kongs.lanky)]),
    Locations.CastleBattleArena: Location(Levels.CreepyCastle, "Castle Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.CastleCrown, -1, 617)]),
    Locations.CastleTinyTrashCan: Location(Levels.CreepyCastle, "Castle Tiny Trash Can", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CastleTrashCan, 0x4, 351, Kongs.tiny)]),
    Locations.CastleChunkyShed: Location(Levels.CreepyCastle, "Castle Chunky Shed", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.CastleShed, 0x6, 322, Kongs.chunky)]),
    Locations.CastleChunkyMuseum: Location(Levels.CreepyCastle, "Castle Chunky Museum", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(Maps.CastleMuseum, 0x7, 314, Kongs.chunky)]),
    Locations.CastleKasplatCrypt: Location(Levels.CreepyCastle, "Castle Kasplat Inside Crypt", Items.CreepyCastleDiddyBlueprint, Types.Blueprint, Kongs.diddy, [Maps.CastleLowerCave]),
    Locations.CastleDiddyCrypt: Location(Levels.CreepyCastle, "Castle Diddy Crypt", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.CastleCrypt, 0x8, 310, Kongs.diddy)]),
    Locations.CastleChunkyCrypt: Location(Levels.CreepyCastle, "Castle Chunky Crypt", Items.GoldenBanana, Types.Banana, Kongs.chunky, [MapIDCombo(0, -1, 311, Kongs.chunky)]),
    Locations.CastleDonkeyMinecarts: Location(Levels.CreepyCastle, "Castle Donkey Minecarts", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(0, -1, 318, Kongs.donkey)]),
    Locations.CastleLankyMausoleum: Location(Levels.CreepyCastle, "Castle Lanky Mausoleum", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(Maps.CastleMausoleum, 0x3, 308, Kongs.lanky)]),
    Locations.CastleTinyMausoleum: Location(Levels.CreepyCastle, "Castle Tiny Mausoleum", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(Maps.CastleMausoleum, 0xD, 309, Kongs.tiny)]),
    Locations.CastleTinyOverChasm: Location(Levels.CreepyCastle, "Castle Tiny Over Chasm", Items.GoldenBanana, Types.Banana, Kongs.tiny, [MapIDCombo(0, -1, 315, Kongs.tiny)]),
    Locations.CastleKasplatNearCandy: Location(Levels.CreepyCastle, "Castle Kasplat Near Candy's Music Shop", Items.CreepyCastleChunkyBlueprint, Types.Blueprint, Kongs.chunky, [Maps.CastleUpperCave]),
    Locations.CastleDonkeyDungeon: Location(Levels.CreepyCastle, "Castle Donkey Dungeon", Items.GoldenBanana, Types.Banana, Kongs.donkey, [MapIDCombo(Maps.CastleDungeon, 0xF, 326, Kongs.donkey)]),
    Locations.CastleDiddyDungeon: Location(Levels.CreepyCastle, "Castle Diddy Dungeon", Items.GoldenBanana, Types.Banana, Kongs.diddy, [MapIDCombo(Maps.CastleDungeon, 0xD, 353, Kongs.diddy)]),
    Locations.CastleLankyDungeon: Location(Levels.CreepyCastle, "Castle Lanky Dungeon", Items.GoldenBanana, Types.Banana, Kongs.lanky, [MapIDCombo(0, -1, 316, Kongs.lanky)]),
    Locations.CastleKey: Location(Levels.CreepyCastle, "Castle Boss Defeated", Items.CreepyCastleKey, Types.Key, Kongs.any, [MapIDCombo(0, -1, 317)]),  # Can be assigned to any kong
    # Hideout Helm locations
    Locations.HelmDonkey1: Location(Levels.HideoutHelm, "Helm Donkey Barrel 1", Items.HelmDonkey1, Types.Constant, Kongs.donkey),
    Locations.HelmDonkey2: Location(Levels.HideoutHelm, "Helm Donkey Barrel 2", Items.HelmDonkey2, Types.Constant, Kongs.donkey),
    Locations.HelmDiddy1: Location(Levels.HideoutHelm, "Helm Diddy Barrel 1", Items.HelmDiddy1, Types.Constant, Kongs.diddy),
    Locations.HelmDiddy2: Location(Levels.HideoutHelm, "Helm Diddy Barrel 2", Items.HelmDiddy2, Types.Constant, Kongs.diddy),
    Locations.HelmLanky1: Location(Levels.HideoutHelm, "Helm Lanky Barrel 1", Items.HelmLanky1, Types.Constant, Kongs.lanky),
    Locations.HelmLanky2: Location(Levels.HideoutHelm, "Helm Lanky Barrel 2", Items.HelmLanky2, Types.Constant, Kongs.lanky),
    Locations.HelmTiny1: Location(Levels.HideoutHelm, "Helm Tiny Barrel 1", Items.HelmTiny1, Types.Constant, Kongs.tiny),
    Locations.HelmTiny2: Location(Levels.HideoutHelm, "Helm Tiny Barrel 2", Items.HelmTiny2, Types.Constant, Kongs.tiny),
    Locations.HelmChunky1: Location(Levels.HideoutHelm, "Helm Chunky Barrel 1", Items.HelmChunky1, Types.Constant, Kongs.chunky),
    Locations.HelmChunky2: Location(Levels.HideoutHelm, "Helm Chunky Barrel 2", Items.HelmChunky2, Types.Constant, Kongs.chunky),
    Locations.HelmBattleArena: Location(Levels.HideoutHelm, "Helm Battle Arena", Items.BattleCrown, Types.Crown, Kongs.any, [MapIDCombo(Maps.HelmCrown, -1, 618)]),
    Locations.HelmDonkeyMedal: Location(Levels.HideoutHelm, "Helm Donkey Medal", Items.BananaMedal, Types.Medal, Kongs.donkey, [MapIDCombo(Maps.HideoutHelm, 0x5D, 584, Kongs.donkey)]),
    Locations.HelmChunkyMedal: Location(Levels.HideoutHelm, "Helm Chunky Medal", Items.BananaMedal, Types.Medal, Kongs.chunky, [MapIDCombo(Maps.HideoutHelm, 0x5E, 588, Kongs.chunky)]),
    Locations.HelmTinyMedal: Location(Levels.HideoutHelm, "Helm Tiny Medal", Items.BananaMedal, Types.Medal, Kongs.tiny, [MapIDCombo(Maps.HideoutHelm, 0x60, 587, Kongs.tiny)]),
    Locations.HelmLankyMedal: Location(Levels.HideoutHelm, "Helm Lanky Medal", Items.BananaMedal, Types.Medal, Kongs.lanky, [MapIDCombo(Maps.HideoutHelm, 0x5F, 586, Kongs.lanky)]),
    Locations.HelmDiddyMedal: Location(Levels.HideoutHelm, "Helm Diddy Medal", Items.BananaMedal, Types.Medal, Kongs.diddy, [MapIDCombo(Maps.HideoutHelm, 0x61, 585, Kongs.diddy)]),
    Locations.HelmBananaFairy1: Location(Levels.HideoutHelm, "Helm Banana Fairy 1", Items.BananaFairy, Types.Fairy),
    Locations.HelmBananaFairy2: Location(Levels.HideoutHelm, "Helm Banana Fairy 2", Items.BananaFairy, Types.Fairy),
    Locations.HelmKey: Location(Levels.HideoutHelm, "Helm Key", Items.HideoutHelmKey, Types.Key, Kongs.any, [MapIDCombo(Maps.HideoutHelm, 0x5A, 380)]),

    # Normal shop locations
    Locations.SimianSlam: Location(Levels.DKIsles, "DK Isles Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Slam, 1, VendorType.Cranky]),
    Locations.BaboonBlast: Location(Levels.JungleJapes, "Japes Cranky Donkey", Items.BaboonBlast, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 1, VendorType.Cranky]),
    Locations.ChimpyCharge: Location(Levels.JungleJapes, "Japes Cranky Diddy", Items.ChimpyCharge, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 1, VendorType.Cranky]),
    Locations.Orangstand: Location(Levels.JungleJapes, "Japes Cranky Lanky", Items.Orangstand, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 1, VendorType.Cranky]),
    Locations.MiniMonkey: Location(Levels.JungleJapes, "Japes Cranky Tiny", Items.MiniMonkey, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 1, VendorType.Cranky]),
    Locations.HunkyChunky: Location(Levels.JungleJapes, "Japes Cranky Chunky", Items.HunkyChunky, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 1, VendorType.Cranky]),
    Locations.CoconutGun: Location(Levels.JungleJapes, "Japes Funky Donkey", Items.Coconut, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 1, VendorType.Funky]),
    Locations.PeanutGun: Location(Levels.JungleJapes, "Japes Funky Diddy", Items.Peanut, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 1, VendorType.Funky]),
    Locations.GrapeGun: Location(Levels.JungleJapes, "Japes Funky Lanky", Items.Grape, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 1, VendorType.Funky]),
    Locations.FeatherGun: Location(Levels.JungleJapes, "Japes Funky Tiny", Items.Feather, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 1, VendorType.Funky]),
    Locations.PineappleGun: Location(Levels.JungleJapes, "Japes Funky Chunky", Items.Pineapple, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 1, VendorType.Funky]),
    Locations.StrongKong: Location(Levels.AngryAztec, "Aztec Cranky Donkey", Items.StrongKong, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 2, VendorType.Cranky]),
    Locations.RocketbarrelBoost: Location(Levels.AngryAztec, "Aztec Cranky Diddy", Items.RocketbarrelBoost, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 2, VendorType.Cranky]),
    Locations.Bongos: Location(Levels.AngryAztec, "Aztec Candy Donkey", Items.Bongos, Types.Shop, Kongs.donkey, [MoveTypes.Instruments, 1, VendorType.Candy]),
    Locations.Guitar: Location(Levels.AngryAztec, "Aztec Candy Diddy", Items.Guitar, Types.Shop, Kongs.diddy, [MoveTypes.Instruments, 1, VendorType.Candy]),
    Locations.Trombone: Location(Levels.AngryAztec, "Aztec Candy Lanky", Items.Trombone, Types.Shop, Kongs.lanky, [MoveTypes.Instruments, 1, VendorType.Candy]),
    Locations.Saxophone: Location(Levels.AngryAztec, "Aztec Candy Tiny", Items.Saxophone, Types.Shop, Kongs.tiny, [MoveTypes.Instruments, 1, VendorType.Candy]),
    Locations.Triangle: Location(Levels.AngryAztec, "Aztec Candy Chunky", Items.Triangle, Types.Shop, Kongs.chunky, [MoveTypes.Instruments, 1, VendorType.Candy]),
    Locations.GorillaGrab: Location(Levels.FranticFactory, "Factory Cranky Donkey", Items.GorillaGrab, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 3, VendorType.Cranky]),
    Locations.SimianSpring: Location(Levels.FranticFactory, "Factory Cranky Diddy", Items.SimianSpring, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 3, VendorType.Cranky]),
    Locations.BaboonBalloon: Location(Levels.FranticFactory, "Factory Cranky Lanky", Items.BaboonBalloon, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 2, VendorType.Cranky]),
    Locations.PonyTailTwirl: Location(Levels.FranticFactory, "Factory Cranky Tiny", Items.PonyTailTwirl, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 2, VendorType.Cranky]),
    Locations.PrimatePunch: Location(Levels.FranticFactory, "Factory Cranky Chunky", Items.PrimatePunch, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 2, VendorType.Cranky]),
    Locations.AmmoBelt1: Location(Levels.FranticFactory, "Factory Funky Shared", Items.ProgressiveAmmoBelt, Types.Shop, Kongs.any, [MoveTypes.AmmoBelt, 1, VendorType.Funky]),
    Locations.MusicUpgrade1: Location(Levels.GloomyGalleon, "Galleon Candy Shared", Items.ProgressiveInstrumentUpgrade, Types.Shop, Kongs.any, [MoveTypes.Instruments, 2, VendorType.Candy]),
    Locations.SuperSimianSlam: Location(Levels.FungiForest, "Forest Cranky Shared", Items.ProgressiveSlam, Types.Shop, Kongs.any, [MoveTypes.Slam, 2, VendorType.Cranky]),
    Locations.HomingAmmo: Location(Levels.FungiForest, "Forest Funky Shared", Items.HomingAmmo, Types.Shop, Kongs.any, [MoveTypes.Guns, 2, VendorType.Funky]),
    Locations.OrangstandSprint: Location(Levels.CrystalCaves, "Caves Cranky Lanky", Items.OrangstandSprint, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 3, VendorType.Cranky]),
    Locations.Monkeyport: Location(Levels.CrystalCaves, "Caves Cranky Tiny", Items.Monkeyport, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 3, VendorType.Cranky]),
    Locations.GorillaGone: Location(Levels.CrystalCaves, "Caves Cranky Chunky", Items.GorillaGone, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 3, VendorType.Cranky]),
    Locations.AmmoBelt2: Location(Levels.CrystalCaves, "Caves Funky Shared", Items.ProgressiveAmmoBelt, Types.Shop, Kongs.any, [MoveTypes.AmmoBelt, 2, VendorType.Funky]),
    Locations.ThirdMelon: Location(Levels.CrystalCaves, "Caves Candy Shared", Items.ProgressiveInstrumentUpgrade, Types.Shop, Kongs.any, [MoveTypes.Instruments, 3, VendorType.Candy]),
    Locations.SuperDuperSimianSlam: Location(Levels.CreepyCastle, "Castle Cranky Shared", Items.ProgressiveSlam, Types.Shop, Kongs.any, [MoveTypes.Slam, 3, VendorType.Cranky]),
    Locations.SniperSight: Location(Levels.CreepyCastle, "Castle Funky Shared", Items.SniperSight, Types.Shop, Kongs.any, [MoveTypes.Guns, 3, VendorType.Funky]),
    Locations.MusicUpgrade2: Location(Levels.CreepyCastle, "Castle Candy Shared", Items.ProgressiveInstrumentUpgrade, Types.Shop, Kongs.any, [MoveTypes.Instruments, 4, VendorType.Candy]),
    Locations.RarewareCoin: Location(Levels.Shops, "Rareware Coin", Items.RarewareCoin, Types.Coin, Kongs.any, [MapIDCombo(Maps.Cranky, 0x2, 379)]),
    # Additional shop locations for randomized moves- Index doesn't really matter, just set to 0
    # Japes
    Locations.SharedJapesPotion: Location(Levels.JungleJapes, "Japes Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.SharedJapesGun: Location(Levels.JungleJapes, "Japes Funky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Guns, 0, VendorType.Funky]),
    # Aztec
    Locations.SharedAztecPotion: Location(Levels.AngryAztec, "Aztec Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.LankyAztecPotion: Location(Levels.AngryAztec, "Aztec Cranky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.TinyAztecPotion: Location(Levels.AngryAztec, "Aztec Cranky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.ChunkyAztecPotion: Location(Levels.AngryAztec, "Aztec Cranky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.SharedAztecGun: Location(Levels.AngryAztec, "Aztec Funky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DonkeyAztecGun: Location(Levels.AngryAztec, "Aztec Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyAztecGun: Location(Levels.AngryAztec, "Aztec Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyAztecGun: Location(Levels.AngryAztec, "Aztec Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyAztecGun: Location(Levels.AngryAztec, "Aztec Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyAztecGun: Location(Levels.AngryAztec, "Aztec Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.SharedAztecInstrument: Location(Levels.AngryAztec, "Aztec Candy Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Instruments, 0, VendorType.Candy]),
    # Factory
    Locations.SharedFactoryPotion: Location(Levels.FranticFactory, "Factory Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyFactoryGun: Location(Levels.FranticFactory, "Factory Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyFactoryGun: Location(Levels.FranticFactory, "Factory Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyFactoryGun: Location(Levels.FranticFactory, "Factory Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyFactoryGun: Location(Levels.FranticFactory, "Factory Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyFactoryGun: Location(Levels.FranticFactory, "Factory Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.SharedFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.DonkeyFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.DiddyFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.LankyFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.TinyFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.ChunkyFactoryInstrument: Location(Levels.FranticFactory, "Factory Candy Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    # Galleon
    Locations.SharedGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DiddyGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.LankyGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.TinyGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.ChunkyGalleonPotion: Location(Levels.GloomyGalleon, "Galleon Cranky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.SharedGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DonkeyGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyGalleonGun: Location(Levels.GloomyGalleon, "Galleon Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DonkeyGalleonInstrument: Location(Levels.GloomyGalleon, "Galleon Candy Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.DiddyGalleonInstrument: Location(Levels.GloomyGalleon, "Galleon Candy Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.LankyGalleonInstrument: Location(Levels.GloomyGalleon, "Galleon Candy Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.TinyGalleonInstrument: Location(Levels.GloomyGalleon, "Galleon Candy Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.ChunkyGalleonInstrument: Location(Levels.GloomyGalleon, "Galleon Candy Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    # Forest
    Locations.DonkeyForestPotion: Location(Levels.FungiForest, "Forest Cranky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DiddyForestPotion: Location(Levels.FungiForest, "Forest Cranky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.LankyForestPotion: Location(Levels.FungiForest, "Forest Cranky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.TinyForestPotion: Location(Levels.FungiForest, "Forest Cranky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.ChunkyForestPotion: Location(Levels.FungiForest, "Forest Cranky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyForestGun: Location(Levels.FungiForest, "Forest Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyForestGun: Location(Levels.FungiForest, "Forest Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyForestGun: Location(Levels.FungiForest, "Forest Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyForestGun: Location(Levels.FungiForest, "Forest Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyForestGun: Location(Levels.FungiForest, "Forest Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    # Caves
    Locations.SharedCavesPotion: Location(Levels.CrystalCaves, "Caves Cranky Shared", Items.NoItem, Types.Shop, Kongs.any, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyCavesPotion: Location(Levels.CrystalCaves, "Caves Cranky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DiddyCavesPotion: Location(Levels.CrystalCaves, "Caves Cranky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyCavesGun: Location(Levels.CrystalCaves, "Caves Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyCavesGun: Location(Levels.CrystalCaves, "Caves Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyCavesGun: Location(Levels.CrystalCaves, "Caves Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyCavesGun: Location(Levels.CrystalCaves, "Caves Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyCavesGun: Location(Levels.CrystalCaves, "Caves Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DonkeyCavesInstrument: Location(Levels.CrystalCaves, "Caves Candy Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.DiddyCavesInstrument: Location(Levels.CrystalCaves, "Caves Candy Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.LankyCavesInstrument: Location(Levels.CrystalCaves, "Caves Candy Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.TinyCavesInstrument: Location(Levels.CrystalCaves, "Caves Candy Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.ChunkyCavesInstrument: Location(Levels.CrystalCaves, "Caves Candy Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    # Castle
    Locations.DonkeyCastlePotion: Location(Levels.CreepyCastle, "Castle Cranky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DiddyCastlePotion: Location(Levels.CreepyCastle, "Castle Cranky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.LankyCastlePotion: Location(Levels.CreepyCastle, "Castle Cranky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.TinyCastlePotion: Location(Levels.CreepyCastle, "Castle Cranky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.ChunkyCastlePotion: Location(Levels.CreepyCastle, "Castle Cranky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DonkeyCastleGun: Location(Levels.CreepyCastle, "Castle Funky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DiddyCastleGun: Location(Levels.CreepyCastle, "Castle Funky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.LankyCastleGun: Location(Levels.CreepyCastle, "Castle Funky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.TinyCastleGun: Location(Levels.CreepyCastle, "Castle Funky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.ChunkyCastleGun: Location(Levels.CreepyCastle, "Castle Funky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Guns, 0, VendorType.Funky]),
    Locations.DonkeyCastleInstrument: Location(Levels.CreepyCastle, "Castle Candy Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.DiddyCastleInstrument: Location(Levels.CreepyCastle, "Castle Candy Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.LankyCastleInstrument: Location(Levels.CreepyCastle, "Castle Candy Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.TinyCastleInstrument: Location(Levels.CreepyCastle, "Castle Candy Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Instruments, 0, VendorType.Candy]),
    Locations.ChunkyCastleInstrument: Location(Levels.CreepyCastle, "Castle Candy Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Instruments, 0, VendorType.Candy]),
    # Isles
    Locations.DonkeyIslesPotion: Location(Levels.DKIsles, "DK Isles Cranky Donkey", Items.NoItem, Types.Shop, Kongs.donkey, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.DiddyIslesPotion: Location(Levels.DKIsles, "DK Isles Cranky Diddy", Items.NoItem, Types.Shop, Kongs.diddy, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.LankyIslesPotion: Location(Levels.DKIsles, "DK Isles Cranky Lanky", Items.NoItem, Types.Shop, Kongs.lanky, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.TinyIslesPotion: Location(Levels.DKIsles, "DK Isles Cranky Tiny", Items.NoItem, Types.Shop, Kongs.tiny, [MoveTypes.Moves, 0, VendorType.Cranky]),
    Locations.ChunkyIslesPotion: Location(Levels.DKIsles, "DK Isles Cranky Chunky", Items.NoItem, Types.Shop, Kongs.chunky, [MoveTypes.Moves, 0, VendorType.Cranky]),

    # Blueprints
    Locations.TurnInDKIslesDonkeyBlueprint: Location(Levels.Shops, "Turn In DK Isles Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInDKIslesDiddyBlueprint: Location(Levels.Shops, "Turn In DK Isles Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInDKIslesLankyBlueprint: Location(Levels.Shops, "Turn In DK Isles Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInDKIslesTinyBlueprint: Location(Levels.Shops, "Turn In DK Isles Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInDKIslesChunkyBlueprint: Location(Levels.Shops, "Turn In DK Isles Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInJungleJapesDonkeyBlueprint: Location(Levels.Shops, "Turn In Jungle Japes Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInJungleJapesDiddyBlueprint: Location(Levels.Shops, "Turn In Jungle Japes Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInJungleJapesLankyBlueprint: Location(Levels.Shops, "Turn In Jungle Japes Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInJungleJapesTinyBlueprint: Location(Levels.Shops, "Turn In Jungle Japes Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInJungleJapesChunkyBlueprint: Location(Levels.Shops, "Turn In Jungle Japes Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInAngryAztecDonkeyBlueprint: Location(Levels.Shops, "Turn In Angry Aztec Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInAngryAztecDiddyBlueprint: Location(Levels.Shops, "Turn In Angry Aztec Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInAngryAztecLankyBlueprint: Location(Levels.Shops, "Turn In Angry Aztec Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInAngryAztecTinyBlueprint: Location(Levels.Shops, "Turn In Angry Aztec Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInAngryAztecChunkyBlueprint: Location(Levels.Shops, "Turn In Angry Aztec Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInFranticFactoryDonkeyBlueprint: Location(Levels.Shops, "Turn In Frantic Factory Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInFranticFactoryDiddyBlueprint: Location(Levels.Shops, "Turn In Frantic Factory Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInFranticFactoryLankyBlueprint: Location(Levels.Shops, "Turn In Frantic Factory Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInFranticFactoryTinyBlueprint: Location(Levels.Shops, "Turn In Frantic Factory Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInFranticFactoryChunkyBlueprint: Location(Levels.Shops, "Turn In Frantic Factory Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInGloomyGalleonDonkeyBlueprint: Location(Levels.Shops, "Turn In Gloomy Galleon Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInGloomyGalleonDiddyBlueprint: Location(Levels.Shops, "Turn In Gloomy Galleon Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInGloomyGalleonLankyBlueprint: Location(Levels.Shops, "Turn In Gloomy Galleon Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInGloomyGalleonTinyBlueprint: Location(Levels.Shops, "Turn In Gloomy Galleon Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInGloomyGalleonChunkyBlueprint: Location(Levels.Shops, "Turn In Gloomy Galleon Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInFungiForestDonkeyBlueprint: Location(Levels.Shops, "Turn In Fungi Forest Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInFungiForestDiddyBlueprint: Location(Levels.Shops, "Turn In Fungi Forest Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInFungiForestLankyBlueprint: Location(Levels.Shops, "Turn In Fungi Forest Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInFungiForestTinyBlueprint: Location(Levels.Shops, "Turn In Fungi Forest Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInFungiForestChunkyBlueprint: Location(Levels.Shops, "Turn In Fungi Forest Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInCrystalCavesDonkeyBlueprint: Location(Levels.Shops, "Turn In Crystal Caves Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInCrystalCavesDiddyBlueprint: Location(Levels.Shops, "Turn In Crystal Caves Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInCrystalCavesLankyBlueprint: Location(Levels.Shops, "Turn In Crystal Caves Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInCrystalCavesTinyBlueprint: Location(Levels.Shops, "Turn In Crystal Caves Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInCrystalCavesChunkyBlueprint: Location(Levels.Shops, "Turn In Crystal Caves Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
    Locations.TurnInCreepyCastleDonkeyBlueprint: Location(Levels.Shops, "Turn In Creepy Castle Donkey Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.donkey),
    Locations.TurnInCreepyCastleDiddyBlueprint: Location(Levels.Shops, "Turn In Creepy Castle Diddy Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.diddy),
    Locations.TurnInCreepyCastleLankyBlueprint: Location(Levels.Shops, "Turn In Creepy Castle Lanky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.lanky),
    Locations.TurnInCreepyCastleTinyBlueprint: Location(Levels.Shops, "Turn In Creepy Castle Tiny Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.tiny),
    Locations.TurnInCreepyCastleChunkyBlueprint: Location(Levels.Shops, "Turn In Creepy Castle Chunky Blueprint", Items.GoldenBanana, Types.BlueprintBanana, Kongs.chunky),
}

TrainingBarrelLocations = {
    Locations.IslesSwimTrainingBarrel,
    Locations.IslesVinesTrainingBarrel,
    Locations.IslesBarrelsTrainingBarrel,
    Locations.IslesOrangesTrainingBarrel,
}
DonkeyMoveLocations = {
    Locations.BaboonBlast,
    Locations.StrongKong,
    Locations.GorillaGrab,
    Locations.CoconutGun,
    Locations.Bongos,
    Locations.DonkeyGalleonPotion,
    Locations.DonkeyForestPotion,
    Locations.DonkeyCavesPotion,
    Locations.DonkeyCastlePotion,
    Locations.DonkeyAztecGun,
    Locations.DonkeyFactoryGun,
    Locations.DonkeyGalleonGun,
    Locations.DonkeyForestGun,
    Locations.DonkeyCavesGun,
    Locations.DonkeyCastleGun,
    Locations.DonkeyFactoryInstrument,
    Locations.DonkeyGalleonInstrument,
    Locations.DonkeyCavesInstrument,
    Locations.DonkeyCastleInstrument,
    Locations.DonkeyIslesPotion,
}
DiddyMoveLocations = {
    Locations.ChimpyCharge,
    Locations.RocketbarrelBoost,
    Locations.SimianSpring,
    Locations.PeanutGun,
    Locations.Guitar,
    Locations.DiddyGalleonPotion,
    Locations.DiddyForestPotion,
    Locations.DiddyCavesPotion,
    Locations.DiddyCastlePotion,
    Locations.DiddyAztecGun,
    Locations.DiddyFactoryGun,
    Locations.DiddyGalleonGun,
    Locations.DiddyForestGun,
    Locations.DiddyCavesGun,
    Locations.DiddyCastleGun,
    Locations.DiddyFactoryInstrument,
    Locations.DiddyGalleonInstrument,
    Locations.DiddyCavesInstrument,
    Locations.DiddyCastleInstrument,
    Locations.DiddyIslesPotion,
}
LankyMoveLocations = {
    Locations.Orangstand,
    Locations.BaboonBalloon,
    Locations.OrangstandSprint,
    Locations.GrapeGun,
    Locations.Trombone,
    Locations.LankyAztecPotion,
    Locations.LankyGalleonPotion,
    Locations.LankyForestPotion,
    Locations.LankyCastlePotion,
    Locations.LankyAztecGun,
    Locations.LankyFactoryGun,
    Locations.LankyGalleonGun,
    Locations.LankyForestGun,
    Locations.LankyCavesGun,
    Locations.LankyCastleGun,
    Locations.LankyFactoryInstrument,
    Locations.LankyGalleonInstrument,
    Locations.LankyCavesInstrument,
    Locations.LankyCastleInstrument,
    Locations.LankyIslesPotion,
}
TinyMoveLocations = {
    Locations.MiniMonkey,
    Locations.PonyTailTwirl,
    Locations.Monkeyport,
    Locations.FeatherGun,
    Locations.Saxophone,
    Locations.TinyAztecPotion,
    Locations.TinyGalleonPotion,
    Locations.TinyForestPotion,
    Locations.TinyCastlePotion,
    Locations.TinyAztecGun,
    Locations.TinyFactoryGun,
    Locations.TinyGalleonGun,
    Locations.TinyForestGun,
    Locations.TinyCavesGun,
    Locations.TinyCastleGun,
    Locations.TinyFactoryInstrument,
    Locations.TinyGalleonInstrument,
    Locations.TinyCavesInstrument,
    Locations.TinyCastleInstrument,
    Locations.TinyIslesPotion,
    Locations.CameraAndShockwave,
}
ChunkyMoveLocations = {
    Locations.HunkyChunky,
    Locations.PrimatePunch,
    Locations.GorillaGone,
    Locations.PineappleGun,
    Locations.Triangle,
    Locations.ChunkyAztecPotion,
    Locations.ChunkyGalleonPotion,
    Locations.ChunkyForestPotion,
    Locations.ChunkyCastlePotion,
    Locations.ChunkyAztecGun,
    Locations.ChunkyFactoryGun,
    Locations.ChunkyGalleonGun,
    Locations.ChunkyForestGun,
    Locations.ChunkyCavesGun,
    Locations.ChunkyCastleGun,
    Locations.ChunkyFactoryInstrument,
    Locations.ChunkyGalleonInstrument,
    Locations.ChunkyCavesInstrument,
    Locations.ChunkyCastleInstrument,
    Locations.ChunkyIslesPotion,
}
SharedMoveLocations = {
    Locations.SimianSlam,
    Locations.SuperSimianSlam,
    Locations.SuperDuperSimianSlam,
    Locations.SniperSight,
    Locations.HomingAmmo,
    Locations.AmmoBelt1,
    Locations.AmmoBelt2,
    Locations.MusicUpgrade1,
    Locations.ThirdMelon,
    Locations.MusicUpgrade2,
    Locations.SharedJapesPotion,
    Locations.SharedJapesGun,
    Locations.SharedAztecPotion,
    Locations.SharedAztecGun,
    Locations.SharedAztecInstrument,
    Locations.SharedFactoryPotion,
    Locations.SharedFactoryInstrument,
    Locations.SharedGalleonPotion,
    Locations.SharedGalleonGun,
    Locations.SharedCavesPotion,
    Locations.IslesSwimTrainingBarrel,
    Locations.IslesVinesTrainingBarrel,
    Locations.IslesBarrelsTrainingBarrel,
    Locations.IslesOrangesTrainingBarrel,
    Locations.CameraAndShockwave,
}
SharedShopLocations = {
    Locations.SimianSlam,
    Locations.SuperSimianSlam,
    Locations.SuperDuperSimianSlam,
    Locations.SniperSight,
    Locations.HomingAmmo,
    Locations.AmmoBelt1,
    Locations.AmmoBelt2,
    Locations.MusicUpgrade1,
    Locations.ThirdMelon,
    Locations.MusicUpgrade2,
    Locations.SharedJapesPotion,
    Locations.SharedJapesGun,
    Locations.SharedAztecPotion,
    Locations.SharedAztecGun,
    Locations.SharedAztecInstrument,
    Locations.SharedFactoryPotion,
    Locations.SharedFactoryInstrument,
    Locations.SharedGalleonPotion,
    Locations.SharedGalleonGun,
    Locations.SharedCavesPotion,
}

# Dictionary to speed up lookups of related shop locations
ShopLocationReference = {}
ShopLocationReference[Levels.JungleJapes] = {}
ShopLocationReference[Levels.JungleJapes][VendorType.Cranky] = {
    Locations.BaboonBlast,
    Locations.ChimpyCharge,
    Locations.Orangstand,
    Locations.MiniMonkey,
    Locations.HunkyChunky,
    Locations.SharedJapesPotion,
}
ShopLocationReference[Levels.JungleJapes][VendorType.Funky] = {
    Locations.CoconutGun,
    Locations.PeanutGun,
    Locations.GrapeGun,
    Locations.FeatherGun,
    Locations.PineappleGun,
    Locations.SharedJapesGun,
}
ShopLocationReference[Levels.AngryAztec] = {}
ShopLocationReference[Levels.AngryAztec][VendorType.Cranky] = {
    Locations.StrongKong,
    Locations.RocketbarrelBoost,
    Locations.LankyAztecPotion,
    Locations.TinyAztecPotion,
    Locations.ChunkyAztecPotion,
    Locations.SharedAztecPotion,
}
ShopLocationReference[Levels.AngryAztec][VendorType.Candy] = {
    Locations.Bongos,
    Locations.Guitar,
    Locations.Trombone,
    Locations.Saxophone,
    Locations.Triangle,
    Locations.SharedAztecInstrument,
}
ShopLocationReference[Levels.AngryAztec][VendorType.Funky] = {
    Locations.DonkeyAztecGun,
    Locations.DiddyAztecGun,
    Locations.LankyAztecGun,
    Locations.TinyAztecGun,
    Locations.ChunkyAztecGun,
    Locations.SharedAztecGun,
}
ShopLocationReference[Levels.FranticFactory] = {}
ShopLocationReference[Levels.FranticFactory][VendorType.Cranky] = {
    Locations.GorillaGrab,
    Locations.SimianSpring,
    Locations.BaboonBalloon,
    Locations.PonyTailTwirl,
    Locations.PrimatePunch,
    Locations.SharedFactoryPotion,
}
ShopLocationReference[Levels.FranticFactory][VendorType.Candy] = {
    Locations.DonkeyFactoryInstrument,
    Locations.DiddyFactoryInstrument,
    Locations.LankyFactoryInstrument,
    Locations.TinyFactoryInstrument,
    Locations.ChunkyFactoryInstrument,
    Locations.SharedFactoryInstrument,
}
ShopLocationReference[Levels.FranticFactory][VendorType.Funky] = {
    Locations.DonkeyFactoryGun,
    Locations.DiddyFactoryGun,
    Locations.LankyFactoryGun,
    Locations.TinyFactoryGun,
    Locations.ChunkyFactoryGun,
    Locations.AmmoBelt1,
}
ShopLocationReference[Levels.GloomyGalleon] = {}
ShopLocationReference[Levels.GloomyGalleon][VendorType.Cranky] = {
    Locations.DonkeyGalleonPotion,
    Locations.DiddyGalleonPotion,
    Locations.LankyGalleonPotion,
    Locations.TinyGalleonPotion,
    Locations.ChunkyGalleonPotion,
    Locations.SharedGalleonPotion,
}
ShopLocationReference[Levels.GloomyGalleon][VendorType.Candy] = {
    Locations.DonkeyGalleonInstrument,
    Locations.DiddyGalleonInstrument,
    Locations.LankyGalleonInstrument,
    Locations.TinyGalleonInstrument,
    Locations.ChunkyGalleonInstrument,
    Locations.MusicUpgrade1,
}
ShopLocationReference[Levels.GloomyGalleon][VendorType.Funky] = {
    Locations.DonkeyGalleonGun,
    Locations.DiddyGalleonGun,
    Locations.LankyGalleonGun,
    Locations.TinyGalleonGun,
    Locations.ChunkyGalleonGun,
    Locations.SharedGalleonGun,
}
ShopLocationReference[Levels.FungiForest] = {}
ShopLocationReference[Levels.FungiForest][VendorType.Cranky] = {
    Locations.DonkeyForestPotion,
    Locations.DiddyForestPotion,
    Locations.LankyForestPotion,
    Locations.TinyForestPotion,
    Locations.ChunkyForestPotion,
    Locations.SuperSimianSlam,
}
ShopLocationReference[Levels.FungiForest][VendorType.Funky] = {
    Locations.DonkeyForestGun,
    Locations.DiddyForestGun,
    Locations.LankyForestGun,
    Locations.TinyForestGun,
    Locations.ChunkyForestGun,
    Locations.HomingAmmo,
}
ShopLocationReference[Levels.CrystalCaves] = {}
ShopLocationReference[Levels.CrystalCaves][VendorType.Cranky] = {
    Locations.DonkeyCavesPotion,
    Locations.DiddyCavesPotion,
    Locations.OrangstandSprint,
    Locations.Monkeyport,
    Locations.GorillaGone,
    Locations.SharedCavesPotion,
}
ShopLocationReference[Levels.CrystalCaves][VendorType.Candy] = {
    Locations.DonkeyCavesInstrument,
    Locations.DiddyCavesInstrument,
    Locations.LankyCavesInstrument,
    Locations.TinyCavesInstrument,
    Locations.ChunkyCavesInstrument,
    Locations.ThirdMelon,
}
ShopLocationReference[Levels.CrystalCaves][VendorType.Funky] = {
    Locations.DonkeyCavesGun,
    Locations.DiddyCavesGun,
    Locations.LankyCavesGun,
    Locations.TinyCavesGun,
    Locations.ChunkyCavesGun,
    Locations.AmmoBelt2,
}
ShopLocationReference[Levels.CreepyCastle] = {}
ShopLocationReference[Levels.CreepyCastle][VendorType.Cranky] = {
    Locations.DonkeyCastlePotion,
    Locations.DiddyCastlePotion,
    Locations.LankyCastlePotion,
    Locations.TinyCastlePotion,
    Locations.ChunkyCastlePotion,
    Locations.SuperDuperSimianSlam,
}
ShopLocationReference[Levels.CreepyCastle][VendorType.Candy] = {
    Locations.DonkeyCastleInstrument,
    Locations.DiddyCastleInstrument,
    Locations.LankyCastleInstrument,
    Locations.TinyCastleInstrument,
    Locations.ChunkyCastleInstrument,
    Locations.MusicUpgrade2,
}
ShopLocationReference[Levels.CreepyCastle][VendorType.Funky] = {
    Locations.DonkeyCastleGun,
    Locations.DiddyCastleGun,
    Locations.LankyCastleGun,
    Locations.TinyCastleGun,
    Locations.ChunkyCastleGun,
    Locations.SniperSight,
}
ShopLocationReference[Levels.DKIsles] = {}
ShopLocationReference[Levels.DKIsles][VendorType.Cranky] = {Locations.DonkeyIslesPotion, Locations.DiddyIslesPotion, Locations.LankyIslesPotion, Locations.TinyIslesPotion, Locations.ChunkyIslesPotion, Locations.SimianSlam}
