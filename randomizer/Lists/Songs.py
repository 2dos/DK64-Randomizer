"""Data of the song breakdowns in ROM."""

from randomizer.Enums.SongType import SongType
from randomizer.Enums.SongGroups import SongGroup
from randomizer.Enums.Songs import Songs


class Song:
    """Class used for managing song objects."""

    def __init__(self, name, mem_idx, type=SongType.System, memory=None, location_tags=[], mood_tags=[], song_length=0):
        """Init SONG objects.

        Args:
            name (str): Name of the song.
            mem_idx (int): Memory index of the song.
            type (enum, optional): Songtype enum of the item. Defaults to SongType.System.
        """
        self.name = name
        self.mem_idx = mem_idx
        self.output_name = name
        self.output_name_short = name
        self.type = type
        self.default_type = type
        self.memory = memory
        self.default_memory = memory
        self.channel = (memory >> 3) & 0xF
        self.location_tags = location_tags.copy()
        self.mood_tags = mood_tags.copy()
        self.song_length = song_length
        self.shuffled = False

    def Reset(self):
        """Reset song object so that output_name is reset between generations."""
        self.output_name = self.name
        self.output_name_short = self.name
        self.memory = self.default_memory
        self.shuffled = False
        self.type = self.default_type


class SongMultiselectorItem:
    """Song Exclusion multiselector information."""

    def __init__(self, name, shift, tooltip=""):
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


# Do not change the sorting of this dictionary!
song_data = {
    # DK Isles BGM
    Songs.TrainingGrounds: Song("Training Grounds", mem_idx=123, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.Isles: Song("DK Isles", mem_idx=109, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.IslesKremIsle: Song("DK Isles (K. Rool's Ship)", mem_idx=110, type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.IslesKLumsy: Song(
        "DK Isles (K. Lumsy's Prison)", mem_idx=112, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]
    ),
    Songs.IslesBFI: Song(
        "DK Isles (Banana Fairy Island)", mem_idx=111, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]
    ),
    Songs.IslesSnideRoom: Song("DK Isles (Snide's Room)", mem_idx=166, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.JapesLobby: Song("Jungle Japes (Lobby)", mem_idx=131, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.AztecLobby: Song("Angry Aztec (Lobby)", mem_idx=130, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.FactoryLobby: Song("Frantic Factory (Lobby)", mem_idx=132, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonLobby: Song("Gloomy Galleon (Lobby)", mem_idx=133, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestLobby: Song("Fungi Forest (Lobby)", mem_idx=153, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.CavesLobby: Song("Crystal Caves (Lobby)", mem_idx=154, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleLobby: Song("Creepy Castle (Lobby)", mem_idx=155, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HelmLobby: Song("Hideout Helm (Lobby)", mem_idx=156, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    # Jungle Japes BGM
    Songs.JapesMain: Song("Jungle Japes", mem_idx=160, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.JapesStart: Song("Jungle Japes (Starting Area)", mem_idx=1, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.JapesTunnels: Song("Jungle Japes (Tunnels)", mem_idx=30, type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.JapesStorm: Song("Jungle Japes (Cranky's Area)", mem_idx=161, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.JapesCaves: Song("Jungle Japes (Caves/Underground)", mem_idx=5, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.JapesBlast: Song("Jungle Japes (Baboon Blast)", mem_idx=50, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.JapesCart: Song("Jungle Japes (Minecart)", mem_idx=3, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.JapesDillo: Song("Jungle Japes (Army Dillo)", mem_idx=4, type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    # Angry Aztec BGM
    Songs.AztecMain: Song("Angry Aztec", mem_idx=14, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.AztecTunnels: Song("Angry Aztec (Tunnels)", mem_idx=37, type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.AztecTemple: Song("Angry Aztec (Temple)", mem_idx=21, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Aztec5DT: Song("Angry Aztec (5DT)", mem_idx=26, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.AztecBlast: Song("Angry Aztec (Baboon Blast)", mem_idx=55, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.AztecBeetle: Song("Angry Aztec (Beetle Slide)", mem_idx=19, type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.AztecChunkyKlaptraps: Song("Angry Aztec (Chunky Klaptraps)", mem_idx=48, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.AztecDogadon: Song("Angry Aztec (Dogadon)", mem_idx=25, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    # Frantic Factory BGM
    Songs.FactoryMain: Song("Frantic Factory", mem_idx=28, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.FactoryProduction: Song("Frantic Factory (Production Room)", mem_idx=52, type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.FactoryResearchAndDevelopment: Song("Frantic Factory (R&D)", mem_idx=51, type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryCrusher: Song("Frantic Factory (Crusher Room)", mem_idx=49, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryCarRace: Song("Frantic Factory (Car Race)", mem_idx=27, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryJack: Song("Frantic Factory (Mad Jack)", mem_idx=39, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    # Gloomy Galleon BGM
    Songs.GalleonTunnels: Song("Gloomy Galleon (Tunnels)", mem_idx=62, type=SongType.BGM, memory=0x18B, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonOutside: Song("Gloomy Galleon (Outside)", mem_idx=56, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonLighthouse: Song("Gloomy Galleon (Lighthouse)", mem_idx=63, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.GalleonMechFish: Song("Gloomy Galleon (Mechanical Fish)", mem_idx=91, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.Galleon2DS: Song("Gloomy Galleon (2DS)", mem_idx=77, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Galleon5DS: Song("Gloomy Galleon (5DS/Submarine)", mem_idx=78, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonMermaid: Song("Gloomy Galleon (Mermaid Palace)", mem_idx=80, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.GalleonChest: Song("Gloomy Galleon (Pearls Chest)", mem_idx=79, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.GalleonBlast: Song("Gloomy Galleon (Baboon Blast)", mem_idx=92, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonSealRace: Song("Gloomy Galleon (Seal Race)", mem_idx=61, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.GalleonPufftoss: Song("Gloomy Galleon (Pufftoss)", mem_idx=60, type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    # Fungi Forest BGM
    Songs.ForestDay: Song("Fungi Forest (Day)", mem_idx=68, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.ForestNight: Song("Fungi Forest (Night)", mem_idx=70, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestBarn: Song("Fungi Forest (Barn)", mem_idx=94, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestMill: Song("Fungi Forest (Mill)", mem_idx=95, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestAnthill: Song("Fungi Forest (Anthill)", mem_idx=93, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.ForestMushroom: Song("Fungi Forest (Giant Mushroom)", mem_idx=99, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestMushroomRooms: Song(
        "Fungi Forest (Mushroom Top Rooms)", mem_idx=98, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]
    ),
    Songs.ForestSpider: Song("Fungi Forest (Spider)", mem_idx=97, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.ForestBlast: Song("Fungi Forest (Baboon Blast)", mem_idx=164, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestRabbitRace: Song("Fungi Forest (Rabbit Race)", mem_idx=169, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.ForestCart: Song("Fungi Forest (Minecart)", mem_idx=74, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestDogadon: Song("Fungi Forest (Dogadon)", mem_idx=81, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    # Crystal Caves BGM
    Songs.Caves: Song("Crystal Caves", mem_idx=83, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesIgloos: Song("Crystal Caves (Igloos)", mem_idx=103, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesCabins: Song("Crystal Caves (Cabins)", mem_idx=118, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesRotatingRoom: Song("Crystal Caves (Rotating Room)", mem_idx=119, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.CavesTantrum: Song("Crystal Caves (Giant Kosha Tantrum)", mem_idx=84, type=SongType.BGM, memory=0x193, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CavesBlast: Song("Crystal Caves (Baboon Blast)", mem_idx=163, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesIceCastle: Song("Crystal Caves (Tile Flipping)", mem_idx=120, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.CavesBeetleRace: Song("Crystal Caves (Beetle Race)", mem_idx=102, type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.CavesDillo: Song("Crystal Caves (Army Dillo)", mem_idx=148, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    # Creepy Castle BGM
    Songs.Castle: Song("Creepy Castle", mem_idx=105, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleShed: Song("Fungi Forest (Winch)", mem_idx=139, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleTree: Song("Creepy Castle (Tree)", mem_idx=141, type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleTunnels: Song("Creepy Castle (Tunnels)", mem_idx=121, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleCrypt: Song("Creepy Castle (Crypt)", mem_idx=126, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleInnerCrypts: Song("Creepy Castle (Inner Crypts)", mem_idx=135, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleDungeon_Chains: Song(
        "Creepy Castle (Dungeon w/ Chains)", mem_idx=129, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]
    ),
    Songs.CastleDungeon_NoChains: Song(
        "Creepy Castle (Dungeon w/out Chains)", mem_idx=150, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]
    ),
    Songs.CastleBallroom: Song("Creepy Castle (Ballroom)", mem_idx=136, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleMuseum: Song("Creepy Castle (Museum)", mem_idx=142, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleGreenhouse: Song("Creepy Castle (Greenhouse)", mem_idx=137, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleTrash: Song("Creepy Castle (Trash Can)", mem_idx=157, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleTower: Song("Creepy Castle (Wind Tower)", mem_idx=140, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleBlast: Song("Creepy Castle (Baboon Blast)", mem_idx=165, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleCart: Song("Creepy Castle (Minecart)", mem_idx=106, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleKutOut: Song("Creepy Castle (King Kut-Out)", mem_idx=149, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    # Hideout Helm BGM
    Songs.HelmBoMOn: Song("Hideout Helm (Blast-O-Matic On)", mem_idx=113, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Songs.HelmBoMOff: Song("Hideout Helm (Blast-O-Matic Off)", mem_idx=116, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HelmBonus: Song("Hideout Helm (Bonus Barrels)", mem_idx=117, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    # NPC BGM
    Songs.Cranky: Song("Cranky's Lab", mem_idx=2, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy]),
    Songs.Funky: Song("Funky's Hut", mem_idx=6, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy]),
    Songs.Candy: Song("Candy's Music Shop", mem_idx=31, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Snide: Song("Snide's HQ", mem_idx=29, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.WrinklyKong: Song("Wrinkly Kong", mem_idx=171, type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    # Moves and Animals BGM
    Songs.StrongKong: Song("Strong Kong", mem_idx=71, type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Rocketbarrel: Song("Rocketbarrel Boost", mem_idx=72, type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Sprint: Song("Orangstand Sprint", mem_idx=73, type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.MiniMonkey: Song("Mini Monkey", mem_idx=16, type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.HunkyChunky: Song("Hunky Chunky", mem_idx=17, type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Songs.GorillaGone: Song("Gorilla Gone", mem_idx=108, type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Rambi: Song("Rambi", mem_idx=36, type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Enguarde: Song("Enguarde", mem_idx=124, type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    # Battle BGM
    Songs.BattleArena: Song("Battle Arena", mem_idx=64, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight, SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.TroffNScoff: Song("Troff 'n' Scoff", mem_idx=53, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.AwaitingBossEntry: Song("Awaiting Entering the Boss", mem_idx=58, type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.BossIntroduction: Song("Boss Introduction", mem_idx=100, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MiniBoss: Song("Mini Boss", mem_idx=104, type=SongType.BGM, memory=0x1AA, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Songs.KRoolBattle: Song("K. Rool's Battle", mem_idx=152, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    # Menu and Story BGM
    Songs.MainMenu: Song("Main Menu", mem_idx=134, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.PauseMenu: Song("Pause Menu", mem_idx=34, type=SongType.BGM, memory=0x1D4, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.NintendoLogo: Song("Nintendo Logo", mem_idx=174, type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.DKRap: Song(
        "DK Rap",
        mem_idx=75,
        type=SongType.Protected,  # Needed for CC and complete the rap. Mostly protecting for the former
        memory=0x900,
        location_tags=[SongGroup.Fight, SongGroup.LobbyShop, SongGroup.Interiors, SongGroup.Exteriors, SongGroup.Minigames],
        mood_tags=[SongGroup.Happy],
    ),
    Songs.IntroStory: Song("Intro Story Medley", mem_idx=122, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.KRoolTheme: Song("K. Rool's Theme", mem_idx=138, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.KLumsyCelebration: Song("K. Lumsy Celebration", mem_idx=125, type=SongType.BGM, memory=0x110, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.KRoolTakeoff: Song("K. Rool Takeoff", mem_idx=162, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.KRoolEntrance: Song("K. Rool's Entrance", mem_idx=167, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.KLumsyEnding: Song("K. Lumsy Ending", mem_idx=159, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.EndSequence: Song("End Sequence", mem_idx=158, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    # Minigame BGM
    Songs.Minigames: Song("Bonus Minigames", mem_idx=8, type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.MadMazeMaul: Song("Mad Maze Maul", mem_idx=82, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.StealthySnoop: Song("Stealthy Snoop", mem_idx=89, type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MinecartMayhem: Song("Minecart Mayhem", mem_idx=90, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.MonkeySmash: Song("Monkey Smash", mem_idx=168, type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    # Major Items
    Songs.OhBanana: Song("Oh Banana", mem_idx=20, type=SongType.MajorItem, memory=0xABD, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=3.25),
    Songs.GBGet: Song("Golden Banana/Key Get", mem_idx=18, type=SongType.MajorItem, memory=0x8C4, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.86),
    Songs.MoveGet: Song("Move Get", mem_idx=114, type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=6.36),
    Songs.GunGet: Song("Gun Get", mem_idx=115, type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.53),
    Songs.BananaMedalGet: Song("Banana Medal Get", mem_idx=151, type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.85),
    Songs.BlueprintDrop: Song("Blueprint Drop", mem_idx=76, type=SongType.MajorItem, memory=0x63D, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=2.08),
    Songs.BlueprintGet: Song("Blueprint Get", mem_idx=69, type=SongType.MajorItem, memory=0x4C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=1.87),
    Songs.HeadphonesGet: Song("Headphones Get", mem_idx=127, type=SongType.MajorItem, memory=0x4BC, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.23),
    Songs.DropRainbowCoin: Song("Drop Rainbow Coin", mem_idx=144, type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=0.91),
    Songs.RainbowCoinGet: Song("Rainbow Coin Get", mem_idx=145, type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.06),
    Songs.CompanyCoinGet: Song("Company Coin Get", mem_idx=22, type=SongType.MajorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.07),
    Songs.BeanGet: Song("Bean Get", mem_idx=147, type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.86),
    Songs.PearlGet: Song("Pearl Get", mem_idx=128, type=SongType.MajorItem, memory=0x43E, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=0.73),
    # Minor Items
    Songs.MelonSliceDrop: Song("Melon Slice Drop", mem_idx=47, type=SongType.MinorItem, memory=0x635, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=1.14),
    Songs.MelonSliceGet: Song("Melon Slice Get", mem_idx=33, type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.87),
    Songs.BananaCoinGet: Song("Banana Coin Get", mem_idx=23, type=SongType.MinorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=0.46),
    Songs.CrystalCoconutGet: Song("Crystal Coconut Get", mem_idx=35, type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.67),
    Songs.FairyTick: Song("Fairy Tick", mem_idx=46, type=SongType.MinorItem, memory=0x8C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=2.08),
    Songs.MinecartCoinGet: Song("Minecart Coin Get", mem_idx=32, type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.61),
    Songs.DropCoins: Song("Drop Coins (Minecart)", mem_idx=65, type=SongType.MinorItem, memory=0x445, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=1.14),
    Songs.Checkpoint: Song("Checkpoint", mem_idx=67, type=SongType.MinorItem, memory=0x447, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.64),
    Songs.NormalStar: Song("Normal Star", mem_idx=146, type=SongType.MinorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.04),
    # Events
    Songs.Success: Song("Success", mem_idx=40, type=SongType.Event, memory=0x8CD, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy], song_length=2.13),
    Songs.Failure: Song("Failure", mem_idx=42, type=SongType.Event, memory=0x89D, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy], song_length=3.27),
    Songs.SuccessRaces: Song("Success (Races)", mem_idx=86, type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=23.75),
    Songs.FailureRaces: Song(
        "Failure (Races & Try Again)", mem_idx=87, type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=23.75
    ),
    Songs.BossUnlock: Song("Boss Unlock", mem_idx=57, type=SongType.Event, memory=0x98, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=12.27),
    Songs.BossDefeat: Song("Boss Defeat", mem_idx=54, type=SongType.Event, memory=0x89A, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=5.35),
    Songs.Bongos: Song("Bongo Blast", mem_idx=11, type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm], song_length=3.42),
    Songs.Guitar: Song("Guitar Gazump", mem_idx=10, type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=3.99),
    Songs.Trombone: Song("Trombone Tremor", mem_idx=12, type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=5.05),
    Songs.Saxophone: Song("Saxophone Slam", mem_idx=13, type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.22),
    Songs.Triangle: Song("Triangle Trample", mem_idx=9, type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.47),
    Songs.BaboonBalloon: Song("Baboon Balloon", mem_idx=107, type=SongType.Event, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=20.04),
    Songs.Transformation: Song("Transformation", mem_idx=15, type=SongType.Event, memory=0xA34, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy], song_length=4.31),
    Songs.VultureRing: Song("Going through Vulture Ring", mem_idx=24, type=SongType.Event, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm]),
    Songs.BBlastFinalStar: Song("Barrel Blast Final Star", mem_idx=143, type=SongType.Event, memory=0x445, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.36),
    Songs.FinalCBGet: Song("100th CB Get", mem_idx=172, type=SongType.Event, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=2.10),
    # Ambient
    Songs.WaterDroplets: Song("Water Droplets", mem_idx=38, type=SongType.Ambient, memory=0x914),
    Songs.TwinklySounds: Song("Generic Twinkly Sounds", mem_idx=59, type=SongType.Ambient, memory=0x934),
    Songs.FairyNearby: Song("Fairy Nearby", mem_idx=66, type=SongType.Ambient, memory=0x925),
    Songs.SeasideSounds: Song("Generic Seaside Sounds", mem_idx=96, type=SongType.Ambient, memory=0x912),
    # Protected
    Songs.UnusedCoin: Song("Unused Coin Pickup", mem_idx=7, type=SongType.Protected, memory=0x440),
    Songs.StartPause: Song("Start (To pause game)", mem_idx=41, type=SongType.Protected, memory=0x85E),
    Songs.JapesHighPitched: Song("Unused High-Pitched Japes", mem_idx=45, type=SongType.Protected, memory=0x444),
    Songs.BonusBarrelIntroduction: Song("Bonus Barrel Introduction", mem_idx=88, type=SongType.Protected, memory=0x100),
    Songs.TagBarrel: Song("Tag Barrel (All of them)", mem_idx=101, type=SongType.Protected, memory=0x1CA),
    Songs.GameOver: Song("Game Over", mem_idx=170, type=SongType.Protected, memory=0x1D8),
    Songs.KRoolDefeat: Song("K. Rool's Defeat", mem_idx=173, type=SongType.Protected, memory=0x18),
    # System
    Songs.Silence: Song("Silence", mem_idx=0, type=SongType.System, memory=0x00),
    Songs.TransitionOpen: Song("DK Transition (Opening)", mem_idx=43, type=SongType.System, memory=0x854),
    Songs.TransitionClose: Song("DK Transition (Closing)", mem_idx=44, type=SongType.System, memory=0x854),
    Songs.NintendoLogoOld: Song("Nintendo Logo (Old?)", mem_idx=85, type=SongType.System, memory=0x102),
}

# Do not change the sorting of this list!
song_idx_list = [
    song_data[Songs.Silence],
    song_data[Songs.JapesStart],
    song_data[Songs.Cranky],
    song_data[Songs.JapesCart],
    song_data[Songs.JapesDillo],
    song_data[Songs.JapesCaves],
    song_data[Songs.Funky],
    song_data[Songs.UnusedCoin],
    song_data[Songs.Minigames],
    song_data[Songs.Triangle],
    song_data[Songs.Guitar],
    song_data[Songs.Bongos],
    song_data[Songs.Trombone],
    song_data[Songs.Saxophone],
    song_data[Songs.AztecMain],
    song_data[Songs.Transformation],
    song_data[Songs.MiniMonkey],
    song_data[Songs.HunkyChunky],
    song_data[Songs.GBGet],
    song_data[Songs.AztecBeetle],
    song_data[Songs.OhBanana],
    song_data[Songs.AztecTemple],
    song_data[Songs.CompanyCoinGet],
    song_data[Songs.BananaCoinGet],
    song_data[Songs.VultureRing],
    song_data[Songs.AztecDogadon],
    song_data[Songs.Aztec5DT],
    song_data[Songs.FactoryCarRace],
    song_data[Songs.FactoryMain],
    song_data[Songs.Snide],
    song_data[Songs.JapesTunnels],
    song_data[Songs.Candy],
    song_data[Songs.MinecartCoinGet],
    song_data[Songs.MelonSliceGet],
    song_data[Songs.PauseMenu],
    song_data[Songs.CrystalCoconutGet],
    song_data[Songs.Rambi],
    song_data[Songs.AztecTunnels],
    song_data[Songs.WaterDroplets],
    song_data[Songs.FactoryJack],
    song_data[Songs.Success],
    song_data[Songs.StartPause],
    song_data[Songs.Failure],
    song_data[Songs.TransitionOpen],
    song_data[Songs.TransitionClose],
    song_data[Songs.JapesHighPitched],
    song_data[Songs.FairyTick],
    song_data[Songs.MelonSliceDrop],
    song_data[Songs.AztecChunkyKlaptraps],
    song_data[Songs.FactoryCrusher],
    song_data[Songs.JapesBlast],
    song_data[Songs.FactoryResearchAndDevelopment],
    song_data[Songs.FactoryProduction],
    song_data[Songs.TroffNScoff],
    song_data[Songs.BossDefeat],
    song_data[Songs.AztecBlast],
    song_data[Songs.GalleonOutside],
    song_data[Songs.BossUnlock],
    song_data[Songs.AwaitingBossEntry],
    song_data[Songs.TwinklySounds],
    song_data[Songs.GalleonPufftoss],
    song_data[Songs.GalleonSealRace],
    song_data[Songs.GalleonTunnels],
    song_data[Songs.GalleonLighthouse],
    song_data[Songs.BattleArena],
    song_data[Songs.DropCoins],
    song_data[Songs.FairyNearby],
    song_data[Songs.Checkpoint],
    song_data[Songs.ForestDay],
    song_data[Songs.BlueprintGet],
    song_data[Songs.ForestNight],
    song_data[Songs.StrongKong],
    song_data[Songs.Rocketbarrel],
    song_data[Songs.Sprint],
    song_data[Songs.ForestCart],
    song_data[Songs.DKRap],
    song_data[Songs.BlueprintDrop],
    song_data[Songs.Galleon2DS],
    song_data[Songs.Galleon5DS],
    song_data[Songs.GalleonChest],
    song_data[Songs.GalleonMermaid],
    song_data[Songs.ForestDogadon],
    song_data[Songs.MadMazeMaul],
    song_data[Songs.Caves],
    song_data[Songs.CavesTantrum],
    song_data[Songs.NintendoLogoOld],
    song_data[Songs.SuccessRaces],
    song_data[Songs.FailureRaces],
    song_data[Songs.BonusBarrelIntroduction],
    song_data[Songs.StealthySnoop],
    song_data[Songs.MinecartMayhem],
    song_data[Songs.GalleonMechFish],
    song_data[Songs.GalleonBlast],
    song_data[Songs.ForestAnthill],
    song_data[Songs.ForestBarn],
    song_data[Songs.ForestMill],
    song_data[Songs.SeasideSounds],
    song_data[Songs.ForestSpider],
    song_data[Songs.ForestMushroomRooms],
    song_data[Songs.ForestMushroom],
    song_data[Songs.BossIntroduction],
    song_data[Songs.TagBarrel],
    song_data[Songs.CavesBeetleRace],
    song_data[Songs.CavesIgloos],
    song_data[Songs.MiniBoss],
    song_data[Songs.Castle],
    song_data[Songs.CastleCart],
    song_data[Songs.BaboonBalloon],
    song_data[Songs.GorillaGone],
    song_data[Songs.Isles],
    song_data[Songs.IslesKremIsle],
    song_data[Songs.IslesBFI],
    song_data[Songs.IslesKLumsy],
    song_data[Songs.HelmBoMOn],
    song_data[Songs.MoveGet],
    song_data[Songs.GunGet],
    song_data[Songs.HelmBoMOff],
    song_data[Songs.HelmBonus],
    song_data[Songs.CavesCabins],
    song_data[Songs.CavesRotatingRoom],
    song_data[Songs.CavesIceCastle],
    song_data[Songs.CastleTunnels],
    song_data[Songs.IntroStory],
    song_data[Songs.TrainingGrounds],
    song_data[Songs.Enguarde],
    song_data[Songs.KLumsyCelebration],
    song_data[Songs.CastleCrypt],
    song_data[Songs.HeadphonesGet],
    song_data[Songs.PearlGet],
    song_data[Songs.CastleDungeon_Chains],
    song_data[Songs.AztecLobby],
    song_data[Songs.JapesLobby],
    song_data[Songs.FactoryLobby],
    song_data[Songs.GalleonLobby],
    song_data[Songs.MainMenu],
    song_data[Songs.CastleInnerCrypts],
    song_data[Songs.CastleBallroom],
    song_data[Songs.CastleGreenhouse],
    song_data[Songs.KRoolTheme],
    song_data[Songs.CastleShed],
    song_data[Songs.CastleTower],
    song_data[Songs.CastleTree],
    song_data[Songs.CastleMuseum],
    song_data[Songs.BBlastFinalStar],
    song_data[Songs.DropRainbowCoin],
    song_data[Songs.RainbowCoinGet],
    song_data[Songs.NormalStar],
    song_data[Songs.BeanGet],
    song_data[Songs.CavesDillo],
    song_data[Songs.CastleKutOut],
    song_data[Songs.CastleDungeon_NoChains],
    song_data[Songs.BananaMedalGet],
    song_data[Songs.KRoolBattle],
    song_data[Songs.ForestLobby],
    song_data[Songs.CavesLobby],
    song_data[Songs.CastleLobby],
    song_data[Songs.HelmLobby],
    song_data[Songs.CastleTrash],
    song_data[Songs.EndSequence],
    song_data[Songs.KLumsyEnding],
    song_data[Songs.JapesMain],
    song_data[Songs.JapesStorm],
    song_data[Songs.KRoolTakeoff],
    song_data[Songs.CavesBlast],
    song_data[Songs.ForestBlast],
    song_data[Songs.CastleBlast],
    song_data[Songs.IslesSnideRoom],
    song_data[Songs.KRoolEntrance],
    song_data[Songs.MonkeySmash],
    song_data[Songs.ForestRabbitRace],
    song_data[Songs.GameOver],
    song_data[Songs.WrinklyKong],
    song_data[Songs.FinalCBGet],
    song_data[Songs.KRoolDefeat],
    song_data[Songs.NintendoLogo],
]

DKIslesSongs = {
    Songs.TrainingGrounds,
    Songs.Isles,
    Songs.IslesKremIsle,
    Songs.IslesKLumsy,
    Songs.IslesBFI,
    Songs.IslesSnideRoom,
    Songs.JapesLobby,
    Songs.AztecLobby,
    Songs.FactoryLobby,
    Songs.GalleonLobby,
    Songs.ForestLobby,
    Songs.CavesLobby,
    Songs.CastleLobby,
    Songs.HelmLobby,
}
JungleJapesSongs = {
    Songs.JapesMain,
    Songs.JapesStart,
    Songs.JapesTunnels,
    Songs.JapesStorm,
    Songs.JapesCaves,
    Songs.JapesBlast,
    Songs.JapesCart,
    Songs.JapesDillo,
}
AngryAztecSongs = {
    Songs.AztecMain,
    Songs.AztecTunnels,
    Songs.AztecTemple,
    Songs.Aztec5DT,
    Songs.AztecBlast,
    Songs.AztecBeetle,
    Songs.AztecChunkyKlaptraps,
    Songs.AztecDogadon,
}
FranticFactorySongs = {
    Songs.FactoryMain,
    Songs.FactoryProduction,
    Songs.FactoryResearchAndDevelopment,
    Songs.FactoryCrusher,
    Songs.FactoryCarRace,
    Songs.FactoryJack,
}
GloomyGalleonSongs = {
    Songs.GalleonTunnels,
    Songs.GalleonOutside,
    Songs.GalleonLighthouse,
    Songs.GalleonMechFish,
    Songs.Galleon2DS,
    Songs.Galleon5DS,
    Songs.GalleonMermaid,
    Songs.GalleonChest,
    Songs.GalleonBlast,
    Songs.GalleonSealRace,
    Songs.GalleonPufftoss,
}
FungiForestSongs = {
    Songs.ForestDay,
    Songs.ForestNight,
    Songs.ForestBarn,
    Songs.ForestMill,
    Songs.ForestAnthill,
    Songs.ForestMushroom,
    Songs.ForestMushroomRooms,
    Songs.ForestSpider,
    Songs.ForestBlast,
    Songs.ForestRabbitRace,
    Songs.ForestCart,
    Songs.ForestDogadon,
}
CrystalCavesSongs = {
    Songs.Caves,
    Songs.CavesIgloos,
    Songs.CavesCabins,
    Songs.CavesRotatingRoom,
    Songs.CavesTantrum,
    Songs.CavesBlast,
    Songs.CavesIceCastle,
    Songs.CavesBeetleRace,
    Songs.CavesDillo,
}
CreepyCastleSongs = {
    Songs.Castle,
    Songs.CastleShed,
    Songs.CastleTree,
    Songs.CastleTunnels,
    Songs.CastleCrypt,
    Songs.CastleInnerCrypts,
    Songs.CastleDungeon_Chains,
    Songs.CastleDungeon_NoChains,
    Songs.CastleBallroom,
    Songs.CastleMuseum,
    Songs.CastleGreenhouse,
    Songs.CastleTrash,
    Songs.CastleTower,
    Songs.CastleBlast,
    Songs.CastleCart,
    Songs.CastleKutOut,
}
HideoutHelmSongs = {
    Songs.HelmBoMOn,
    Songs.HelmBoMOff,
    Songs.HelmBonus,
}
NPCSongs = {
    Songs.Cranky,
    Songs.Funky,
    Songs.Candy,
    Songs.Snide,
    Songs.WrinklyKong,
}
MoveSongs = {
    Songs.StrongKong,
    Songs.Rocketbarrel,
    Songs.Sprint,
    Songs.MiniMonkey,
    Songs.HunkyChunky,
    Songs.GorillaGone,
    Songs.Rambi,
    Songs.Enguarde,
}
BattleSongs = {
    Songs.BattleArena,
    Songs.MiniBoss,
    Songs.TroffNScoff,
    Songs.AwaitingBossEntry,
    Songs.BossIntroduction,
    Songs.KRoolBattle,
}
MenusAndStorySongs = {
    Songs.NintendoLogo,
    Songs.DKRap,
    Songs.MainMenu,
    Songs.PauseMenu,
    Songs.IntroStory,
    Songs.KRoolTheme,
    Songs.KLumsyCelebration,
    Songs.KRoolTakeoff,
    Songs.KRoolEntrance,
    Songs.KLumsyEnding,
    Songs.EndSequence,
}
MinigameSongs = {
    Songs.Minigames,
    Songs.MadMazeMaul,
    Songs.StealthySnoop,
    Songs.MinecartMayhem,
    Songs.MonkeySmash,
}

ExcludedSongsSelector = []
ExclSongsItems = [
    SongMultiselectorItem("Wrinkly", 0, "Removes Wrinkly doors from playing her theme."),
    SongMultiselectorItem("Transformation", 3, "The game will no longer play the transformation sound effect."),
    SongMultiselectorItem("Pause Music", 4, "The pause menu music will no longer play."),
    SongMultiselectorItem("Sub Areas", 5, "Sub-Areas will no longer play their song, meaning that there's 1 piece of music for the entire level."),
    # SongMultiselectorItem("Shops", 1, "COMING SOON: Makes shops inherit the previous song."), # TODO: Fix this
    # SongMultiselectorItem("Events", 2, "COMING SOON: Events will no longer play a song."), # TODO: Fix this
]
for item in ExclSongsItems:
    if item.name != "No Group":
        ExcludedSongsSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})
SongFilteringSelector = []
SongFilterItems = [
    SongMultiselectorItem("Length", 0, "Non-BGM Tracks will be filtered to be roughly the same length as the slot they replace."),
    SongMultiselectorItem("Location", 3, "BGM tracks will be filtered so that the mood of the song fits the location it's placed in."),
]
for item in SongFilterItems:
    if item.name != "No Group":
        SongFilteringSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})

# This dict determines all of the dropdowns for selecting music, and how they
# will be grouped together.
MusicSelectionPanel = {
    "BGM": {
        "name": "BGM",
        "subcategories": {
            "Isles": {"name": "DK Isles", "type": "BGM", "songs": []},
            "Japes": {"name": "Jungle Japes", "type": "BGM", "songs": []},
            "Aztec": {"name": "Angry Aztec", "type": "BGM", "songs": []},
            "Factory": {"name": "Frantic Factory", "type": "BGM", "songs": []},
            "Galleon": {"name": "Gloomy Galleon", "type": "BGM", "songs": []},
            "Forest": {"name": "Fungi Forest", "type": "BGM", "songs": []},
            "Caves": {"name": "Crystal Caves", "type": "BGM", "songs": []},
            "Castle": {"name": "Creepy Castle", "type": "BGM", "songs": []},
            "Helm": {"name": "Hideout Helm", "type": "BGM", "songs": []},
            "NPC": {"name": "NPCs", "type": "BGM", "songs": []},
            "Moves": {"name": "Moves and Animals", "type": "BGM", "songs": []},
            "Battle": {"name": "Battles", "type": "BGM", "songs": []},
            "Story": {"name": "Menus and Story", "type": "BGM", "songs": []},
            "Minigame": {"name": "Minigames", "type": "BGM", "songs": []},
        },
    },
    "ItemsEvents": {
        "name": "Items and Events",
        "subcategories": {
            "MajorItem": {"name": "Major Items", "type": "MajorItem", "songs": []},
            "MinorItem": {"name": "Minor Items", "type": "MinorItem", "songs": []},
            "Event": {"name": "Events", "type": "Event", "songs": []},
        },
    },
}

bgmCategoryMap = {
    "Isles": DKIslesSongs,
    "Japes": JungleJapesSongs,
    "Aztec": AngryAztecSongs,
    "Factory": FranticFactorySongs,
    "Galleon": GloomyGalleonSongs,
    "Forest": FungiForestSongs,
    "Caves": CrystalCavesSongs,
    "Castle": CreepyCastleSongs,
    "Helm": HideoutHelmSongs,
    "NPC": NPCSongs,
    "Moves": MoveSongs,
    "Battle": BattleSongs,
    "Story": MenusAndStorySongs,
    "Minigame": MinigameSongs,
}

# This dict groups songs together by type, to determine which songs can be
# placed in which locations.
PlannableSongs = {
    "BGM": [],
    "MajorItem": [],
    "MinorItem": [],
    "Event": [],
}

# This list is used when resetting all selected songs at once.
SongLocationList = []

# Process possible song locations.
for songEnum, song in song_data.items():
    if song.type in [SongType.Ambient, SongType.Protected, SongType.System]:
        continue
    songJson = {
        "name": song.name,
        "value": songEnum.name,
    }
    if song.type == SongType.BGM:
        PlannableSongs["BGM"].append(songJson)
        # Remove Monkey Smash as a location, but keep it as an option for other
        # songs.
        if songEnum == Songs.MonkeySmash:
            continue
        SongLocationList.append(songEnum.name)
        # Find the category this song belongs to.
        for category, songSet in bgmCategoryMap.items():
            if songEnum in songSet:
                MusicSelectionPanel["BGM"]["subcategories"][category]["songs"].append(songJson)
    else:
        PlannableSongs[song.type.name].append(songJson)
        SongLocationList.append(songEnum.name)
        MusicSelectionPanel["ItemsEvents"]["subcategories"][song.type.name]["songs"].append(songJson)


def MusicSelectFilter(songList: list[dict], location: str) -> list[dict]:
    """Return a filtered list of songs that can be placed in this location.

    Args:
        songList (dict[]): The list of possible songs. Each item contains
            "name" and "value" string fields.
        location (str): The location where we are trying to place a song.
            Equal to the string name of the Song enum.
    """
    return [song for song in songList if song_data[Songs[song["value"]]].type != SongType.BGM or song_data[Songs[song["value"]]].channel == song_data[Songs[location]].channel]


def getSongIndexFromName(name: str) -> Songs:
    """Obtain the song index from the name of the vanilla song."""
    for song_idx in song_data:
        if song_data[song_idx].name == name:
            return song_idx
    return None
