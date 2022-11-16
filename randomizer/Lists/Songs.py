"""Data of the song breakdowns in ROM."""
from enum import IntEnum, auto

from randomizer.Enums.SongType import SongType


class Song:
    """Class used for managing song objects."""

    def __init__(self, name, type=SongType.System, group=None, memory=None, channel=0, prevent_rando=False):
        """Init SONG objects.

        Args:
            name (str): Name of the song.
            type (enum, optional): Songtype enum of the item. Defaults to SongType.System.
        """
        self.name = name
        self.type = type
        self.group = group
        self.memory = memory
        self.channel = channel
        self.prevent_rando = prevent_rando


class SongGroup(IntEnum):
    """Used to avoid overloading a song or group of songs with larger music data which can crash the game."""

    JungleJapes = auto()
    AngryAztec = auto()
    FranticFactory = auto()
    GloomyGalleon = auto()
    FungiForest = auto()
    CrystalCaves = auto()
    Isles = auto()
    Self = auto()


song_data = [
    Song("Silence", type=SongType.System, memory=0x00),  # 0
    Song("Jungle Japes (Starting Area)", type=SongType.BGM, group=SongGroup.JungleJapes, memory=0x101, channel=1),
    Song("Cranky's Lab", type=SongType.BGM, memory=0x100, channel=1),
    Song("Jungle Japes (Minecart)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Jungle Japes (Army Dillo)", type=SongType.BGM, memory=0x189, channel=2),
    Song("Jungle Japes (Caves/Underground)", type=SongType.BGM, memory=0x100, channel=1),  # 5
    Song("Funky's Hut", type=SongType.BGM, memory=0x100, channel=1),
    Song("Unused Coin Pickup", type=SongType.System, memory=0x440),
    Song("Bonus Minigames", type=SongType.BGM, memory=0x189, channel=2),
    Song("Triangle Trample", type=SongType.Event, memory=0x8C2),
    Song("Guitar Gazump", type=SongType.Event, memory=0x8C2),  # 10
    Song("Bongo Blast", type=SongType.Event, memory=0x8C2),
    Song("Trombone Tremor", type=SongType.Event, memory=0x8C2),
    Song("Saxaphone Slam", type=SongType.Event, memory=0x8C2),
    Song("Angry Aztec", type=SongType.BGM, group=SongGroup.AngryAztec, memory=0x100, channel=1),
    Song("Transformation", type=SongType.Event, memory=0xA34),  # 15
    Song("Mini Monkey", type=SongType.BGM, group=SongGroup.Self, memory=0x19A, channel=4),
    Song("Hunky Chunky", type=SongType.BGM, group=SongGroup.Self, memory=0x19A, channel=4),
    Song("GB/Key Get", type=SongType.Fanfare, memory=0x8C4),
    Song("Angry Aztec (Beetle Slide)", type=SongType.BGM, memory=0x109, channel=2),
    Song("Oh Banana", type=SongType.Fanfare, memory=0xABD),  # 20
    Song("Angry Aztec (Temple)", type=SongType.BGM, memory=0x101, channel=1),
    Song("Company Coin Get", type=SongType.Fanfare, memory=0x637),
    Song("Banana Coin Get", type=SongType.Fanfare, memory=0x637),
    Song("Going through Vulture Ring", type=SongType.Fanfare, memory=0x647),
    Song("Angry Aztec (Dogadon)", type=SongType.BGM, memory=0x100, channel=1),  # 25
    Song("Angry Aztec (5DT)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Frantic Factory (Car Race)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Frantic Factory", type=SongType.BGM, group=SongGroup.FranticFactory, memory=0x100, channel=1),
    Song("Snide's HQ", type=SongType.BGM, memory=0x100, channel=1),
    Song("Jungle Japes (Tunnels)", type=SongType.BGM, group=SongGroup.Self, memory=0x18A, channel=2),  # 30
    Song("Candy's Music Shop", type=SongType.BGM, memory=0x100, channel=1),
    Song("Minecart Coin Get", type=SongType.Fanfare, memory=0x63F),
    Song("Melon Slice Get", type=SongType.Fanfare, memory=0x63F),
    Song("Pause Menu", type=SongType.BGM, group=SongGroup.Self, memory=0x1D4, channel=11),
    Song("Crystal Coconut Get", type=SongType.Fanfare, memory=0x63F),  # 35
    Song("Rambi", type=SongType.BGM, group=SongGroup.JungleJapes, memory=0x198, channel=4),
    Song("Angry Aztec (Tunnels)", type=SongType.BGM, group=SongGroup.AngryAztec, memory=0x192, channel=3),
    Song("Water Droplets", type=SongType.Ambient, memory=0x914),
    Song("Frantic Factory (Mad Jack)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Success", type=SongType.Event, memory=0x8CD),  # 40
    Song("Start (To pause game)", type=SongType.Fanfare, memory=0x85E),
    Song("Failure", type=SongType.Event, memory=0x89D),
    Song("DK Transition (Opening)", type=SongType.System, memory=0x854),
    Song("DK Transition (Closing)", type=SongType.System, memory=0x854),
    Song("Unused High-Pitched Japes", type=SongType.Fanfare, memory=0x444),  # 45
    Song("Fairy Tick", type=SongType.Fanfare, memory=0x8C5),
    Song("Melon Slice Drop", type=SongType.Fanfare, memory=0x635),
    Song("Angry Aztec (Chunky Klaptraps)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Frantic Factory (Crusher Room)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Jungle Japes (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),  # 50
    Song("Frantic Factory (R&D)", type=SongType.BGM, group=SongGroup.FranticFactory, memory=0x18A, channel=2),
    Song("Frantic Factory (Production Room)", type=SongType.BGM, group=SongGroup.FranticFactory, memory=0x18A, channel=2),
    Song("Troff 'n' Scoff", type=SongType.BGM, memory=0x100, channel=1),
    Song("Boss Defeat", type=SongType.Event, memory=0x89A),
    Song("Angry Aztec (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),  # 55
    Song("Gloomy Galleon (Outside)", type=SongType.BGM, group=SongGroup.GloomyGalleon, memory=0x101, channel=1),
    Song("Boss Unlock", type=SongType.Event, memory=0x98),
    Song("Awaiting Entering the Boss", type=SongType.BGM, memory=0x190, channel=3),
    Song("Generic Twinkly Sounds", type=SongType.Ambient, memory=0x934),
    Song("Gloomy Galleon (Pufftoss)", type=SongType.BGM, memory=0x108, channel=2),  # 60
    Song("Gloomy Galleon (Seal Race)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Gloomy Galleon (Tunnels)", type=SongType.BGM, group=SongGroup.Self, memory=0x18B, channel=2),
    Song("Gloomy Galleon (Lighthouse)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Battle Arena", type=SongType.BGM, memory=0x100, channel=1),
    Song("Drop Coins (Minecart)", type=SongType.Fanfare, memory=0x445),  # 65
    Song("Fairy Nearby", type=SongType.Ambient, memory=0x925),
    Song("Checkpoint", type=SongType.Fanfare, memory=0x447),
    Song("Fungi Forest (Day)", type=SongType.BGM, group=SongGroup.FungiForest, memory=0x101, channel=1),
    Song("Blueprint Get", type=SongType.Fanfare, memory=0x4C5),
    Song("Fungi Forest (Night)", type=SongType.BGM, group=SongGroup.FungiForest, memory=0x188, channel=2),  # 70
    Song("Strong Kong", type=SongType.BGM, group=SongGroup.Self, memory=0x19A, channel=4),
    Song("Rocketbarrel Boost", type=SongType.BGM, group=SongGroup.Self, memory=0x192, channel=3),
    Song("Orangstand Sprint", type=SongType.BGM, group=SongGroup.Self, memory=0x190, channel=3),
    Song("Fungi Forest (Minecart)", type=SongType.BGM, memory=0x100, channel=1),
    Song("DK Rap", type=SongType.BGM, memory=0x900, channel=1),  # 75
    Song("Blueprint Drop", type=SongType.Fanfare, memory=0x63D),
    Song("Gloomy Galleon (2DS)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Gloomy Galleon (5DS/Submarine)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Gloomy Galleon (Pearls Chest)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Gloomy Galleon (Mermaid Palace)", type=SongType.BGM, memory=0x100, channel=1),  # 80
    Song("Fungi Forest (Dogadon)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Mad Maze Maul", type=SongType.BGM, memory=0x188, channel=2),
    Song("Crystal Caves", type=SongType.BGM, group=SongGroup.CrystalCaves, memory=0x101, channel=1),
    Song("Crystal Caves (Giant Kosha Tantrum)", type=SongType.BGM, group=SongGroup.CrystalCaves, memory=0x193, channel=3),
    Song("Nintendo Logo (Old?)", type=SongType.System, memory=0x102),  # 85
    Song("Success (Races)", type=SongType.Event, memory=0x118),
    Song("Failure (Races & Try Again)", type=SongType.Event, memory=0x118),
    Song("Bonus Barrel Introduction", type=SongType.BGM, memory=0x100, channel=1),
    Song("Stealthy Snoop", type=SongType.BGM, memory=0x188, channel=2),
    Song("Minecart Mayhem", type=SongType.BGM, memory=0x100, channel=1),  # 90
    Song("Gloomy Galleon (Mechanical Fish)", type=SongType.BGM, memory=0x101, channel=1),
    Song("Gloomy Galleon (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Anthill)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Barn)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Mill)", type=SongType.BGM, memory=0x100, channel=1),  # 95
    Song("Generic Seaside Sounds", type=SongType.Ambient, memory=0x912),
    Song("Fungi Forest (Spider)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Mushroom Top Rooms)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Giant Mushroom)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Boss Introduction", type=SongType.BGM, memory=0x100, channel=1),  # 100
    Song("Tag Barrel (All of them)", type=SongType.System, memory=0x1CA),
    Song("Crystal Caves (Beetle Race)", type=SongType.BGM, memory=0x108, channel=2),
    Song("Crystal Caves (Igloos)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Mini Boss", type=SongType.BGM, memory=0x1AA, channel=6),
    Song("Creepy Castle", type=SongType.BGM, memory=0x101, channel=1),  # 105
    Song("Creepy Castle (Minecart)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Baboon Balloon", type=SongType.Event, memory=0x19A),
    Song("Gorilla Gone", type=SongType.BGM, memory=0x190, channel=3),
    Song("DK Isles", type=SongType.BGM, group=SongGroup.Isles, memory=0x101, channel=1),
    Song("DK Isles (K Rool's Ship)", type=SongType.BGM, group=SongGroup.Isles, memory=0x109, channel=2),  # 110
    Song("DK Isles (Banana Fairy Island)", type=SongType.BGM, group=SongGroup.Isles, memory=0x101, channel=1),
    Song("DK Isles (K-Lumsy's Prison)", type=SongType.BGM, group=SongGroup.Isles, memory=0x101, channel=1),
    Song("Hideout Helm (Blast-O-Matic On)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Move Get", type=SongType.Fanfare, memory=0x892),
    Song("Gun Get", type=SongType.Fanfare, memory=0x892),  # 115
    Song("Hideout Helm (Blast-O-Matic Off)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Hideout Helm (Bonus Barrels)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Crystal Caves (Cabins)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Crystal Caves (Rotating Room)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Crystal Caves (Tile Flipping)", type=SongType.BGM, memory=0x100, channel=1),  # 120
    Song("Creepy Castle (Tunnels)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Intro Story Medley", type=SongType.BGM, memory=0x100, channel=1),
    Song("Training Grounds", type=SongType.BGM, memory=0x101, channel=1),
    Song("Enguarde", type=SongType.BGM, group=SongGroup.GloomyGalleon, memory=0x198, channel=4),
    Song("K-Lumsy Celebration", type=SongType.Event, memory=0x110),  # 125
    Song("Creepy Castle (Crypt)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Headphones Get", type=SongType.Fanfare, memory=0x4BC),
    Song("Pearl Get", type=SongType.Fanfare, memory=0x43E),
    Song("Creepy Castle (Dungeon w/ Chains)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Angry Aztec (Lobby)", type=SongType.BGM, memory=0x100, channel=1),  # 130
    Song("Jungle Japes (Lobby)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Frantic Factory (Lobby)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Gloomy Galleon (Lobby)", type=SongType.BGM, memory=0x101, channel=1),
    Song("Main Menu", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Inner Crypts)", type=SongType.BGM, memory=0x100, channel=1),  # 135
    Song("Creepy Castle (Ballroom)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Greenhouse)", type=SongType.BGM, memory=0x100, channel=1),
    Song("K Rool's Theme", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Winch)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Wind Tower)", type=SongType.BGM, memory=0x100, channel=1),  # 140
    Song("Creepy Castle (Tree)", type=SongType.BGM, memory=0x101, channel=1),
    Song("Creepy Castle (Museum)", type=SongType.BGM, memory=0x100, channel=1),
    Song("BBlast Final Star", type=SongType.Fanfare, memory=0x445),
    Song("Drop Rainbow Coin", type=SongType.Fanfare, memory=0x647),
    Song("Rainbow Coin Get", type=SongType.Fanfare, memory=0x647),  # 145
    Song("Normal Star", type=SongType.Fanfare, memory=0x645),
    Song("Bean Get", type=SongType.Fanfare, memory=0x645),
    Song("Crystal Caves (Army Dillo)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Kut Out)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Dungeon w/out Chains)", type=SongType.BGM, memory=0x100, channel=1),  # 150
    Song("Banana Medal Get", type=SongType.Fanfare, memory=0x645),
    Song("K Rool's Battle", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Lobby)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Crystal Caves (Lobby)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Lobby)", type=SongType.BGM, memory=0x100, channel=1),  # 155
    Song("Hideout Helm (Lobby)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Trash Can)", type=SongType.BGM, memory=0x100, channel=1),
    Song("End Sequence", type=SongType.BGM, memory=0x100, channel=1),
    Song("K-Lumsy Ending", type=SongType.BGM, memory=0x100, channel=1),
    Song("Jungle Japes", type=SongType.BGM, group=SongGroup.JungleJapes, memory=0x101, channel=1),  # 160
    Song("Jungle Japes (Cranky's Area)", type=SongType.BGM, group=SongGroup.JungleJapes, memory=0x100, channel=1),
    Song("K Rool Takeoff", type=SongType.System, memory=0x100, channel=1),
    Song("Crystal Caves (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),
    Song("Creepy Castle (Baboon Blast)", type=SongType.BGM, memory=0x100, channel=1),  # 165
    Song("DK Isles (Snide's Room)", type=SongType.BGM, memory=0x100, channel=1),
    Song("K Rool's Entrance", type=SongType.BGM, memory=0x100, channel=1),
    Song("Monkey Smash", type=SongType.BGM, memory=0x100, channel=1),
    Song("Fungi Forest (Rabbit Race)", type=SongType.BGM, memory=0x188, channel=2),
    Song("Game Over", type=SongType.Event, memory=0x1D8),  # 170
    Song("Wrinkly Kong", type=SongType.BGM, group=SongGroup.Self, memory=0x18A, channel=2),
    Song("100th CB Get", type=SongType.System, memory=0x645),
    Song("K Rool's Defeat", type=SongType.System, memory=0x18),
    Song("Nintendo Logo", type=SongType.BGM, memory=0x108, channel=2),
]
