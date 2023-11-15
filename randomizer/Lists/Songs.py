"""Data of the song breakdowns in ROM."""
from randomizer.Enums.SongType import SongType
from randomizer.Enums.SongGroups import SongGroup


class Song:
    """Class used for managing song objects."""

    def __init__(self, name, type=SongType.System, memory=None, location_tags=[], mood_tags=[], song_length=0):
        """Init SONG objects.

        Args:
            name (str): Name of the song.
            type (enum, optional): Songtype enum of the item. Defaults to SongType.System.
        """
        self.name = name
        self.output_name = name
        self.type = type
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
        self.memory = self.default_memory
        self.shuffled = False


class SongExclusionItem:
    """Song Exclusion multiselector information."""

    def __init__(self, name, shift, tooltip=""):
        """Initialize with given data."""
        self.name = name
        self.shift = shift
        self.tooltip = tooltip


song_data = [
    Song("Silence", type=SongType.System, memory=0x00),
    Song("Jungle Japes (Starting Area)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Cranky's Lab", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy]),
    Song("Jungle Japes (Minecart)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Jungle Japes (Army Dillo)", type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Song("Jungle Japes (Caves/Underground)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Funky's Hut", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy]),
    Song("Unused Coin Pickup", type=SongType.Protected, memory=0x440),
    Song("Bonus Minigames", type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Triangle Trample", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.47),
    Song("Guitar Gazump", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=3.99),
    Song("Bongo Blast", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm], song_length=3.42),
    Song("Trombone Tremor", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=5.05),
    Song("Saxaphone Slam", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.22),
    Song("Angry Aztec", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Song("Transformation", type=SongType.Event, memory=0xA34, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy], song_length=4.31),
    Song("Mini Monkey", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Hunky Chunky", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Song("GB/Key Get", type=SongType.MajorItem, memory=0x8C4, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.86),
    Song("Angry Aztec (Beetle Slide)", type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Oh Banana", type=SongType.MajorItem, memory=0xABD, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=3.25),
    Song("Angry Aztec (Temple)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Company Coin Get", type=SongType.MajorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.07),
    Song("Banana Coin Get", type=SongType.MinorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=0.46),
    Song("Going through Vulture Ring", type=SongType.Event, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm]),
    Song("Angry Aztec (Dogadon)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Song("Angry Aztec (5DT)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Frantic Factory (Car Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy]),
    Song("Frantic Factory", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Song("Snide's HQ", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Jungle Japes (Tunnels)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Candy's Music Shop", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Minecart Coin Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.61),
    Song("Melon Slice Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.87),
    Song("Pause Menu", type=SongType.BGM, memory=0x1D4, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Crystal Coconut Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.67),
    Song("Rambi", type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Angry Aztec (Tunnels)", type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Water Droplets", type=SongType.Ambient, memory=0x914),
    Song("Frantic Factory (Mad Jack)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Song("Success", type=SongType.Event, memory=0x8CD, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy], song_length=2.13),
    Song("Start (To pause game)", type=SongType.Protected, memory=0x85E),
    Song("Failure", type=SongType.Event, memory=0x89D, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy], song_length=3.27),
    Song("DK Transition (Opening)", type=SongType.System, memory=0x854),
    Song("DK Transition (Closing)", type=SongType.System, memory=0x854),
    Song("Unused High-Pitched Japes", type=SongType.Protected, memory=0x444),
    Song("Fairy Tick", type=SongType.MinorItem, memory=0x8C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=2.08),
    Song("Melon Slice Drop", type=SongType.MinorItem, memory=0x635, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=1.14),
    Song("Angry Aztec (Chunky Klaptraps)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Frantic Factory (Crusher Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Jungle Japes (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Song("Frantic Factory (R&D)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Frantic Factory (Production Room)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Troff 'n' Scoff", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Boss Defeat", type=SongType.Event, memory=0x89A, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=5.35),
    Song("Angry Aztec (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Song("Gloomy Galleon (Outside)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Boss Unlock", type=SongType.Event, memory=0x98, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=12.27),
    Song("Awaiting Entering the Boss", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Generic Twinkly Sounds", type=SongType.Ambient, memory=0x934),
    Song("Gloomy Galleon (Pufftoss)", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Song("Gloomy Galleon (Seal Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Gloomy Galleon (Tunnels)", type=SongType.BGM, memory=0x18B, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Gloomy Galleon (Lighthouse)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Battle Arena", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight, SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Drop Coins (Minecart)", type=SongType.MinorItem, memory=0x445, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=1.14),
    Song("Fairy Nearby", type=SongType.Ambient, memory=0x925),
    Song("Checkpoint", type=SongType.MinorItem, memory=0x447, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.64),
    Song("Fungi Forest (Day)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Blueprint Get", type=SongType.MajorItem, memory=0x4C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=1.87),
    Song("Fungi Forest (Night)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Strong Kong", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Rocketbarrel Boost", type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Orangstand Sprint", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Fungi Forest (Minecart)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("DK Rap", type=SongType.BGM, memory=0x900, location_tags=[SongGroup.Fight, SongGroup.LobbyShop, SongGroup.Interiors, SongGroup.Exteriors, SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Blueprint Drop", type=SongType.MajorItem, memory=0x63D, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=2.08),
    Song("Gloomy Galleon (2DS)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Gloomy Galleon (5DS/Submarine)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Gloomy Galleon (Pearls Chest)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Gloomy Galleon (Mermaid Palace)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Fungi Forest (Dogadon)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Song("Mad Maze Maul", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Crystal Caves", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Crystal Caves (Giant Kosha Tantrum)", type=SongType.BGM, memory=0x193, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Nintendo Logo (Old?)", type=SongType.System, memory=0x102),
    Song("Success (Races)", type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=23.75),
    Song("Failure (Races & Try Again)", type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=23.75),
    Song("Bonus Barrel Introduction", type=SongType.Protected, memory=0x100),
    Song("Stealthy Snoop", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Minecart Mayhem", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Gloomy Galleon (Mechanical Fish)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Gloomy Galleon (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Fungi Forest (Anthill)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Fungi Forest (Barn)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Fungi Forest (Mill)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Generic Seaside Sounds", type=SongType.Ambient, memory=0x912),
    Song("Fungi Forest (Spider)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Fungi Forest (Mushroom Top Rooms)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Fungi Forest (Giant Mushroom)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Boss Introduction", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Tag Barrel (All of them)", type=SongType.Protected, memory=0x1CA),
    Song("Crystal Caves (Beetle Race)", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Crystal Caves (Igloos)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Mini Boss", type=SongType.BGM, memory=0x1AA, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Song("Creepy Castle", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Creepy Castle (Minecart)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Baboon Balloon", type=SongType.Event, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=20.04),
    Song("Gorilla Gone", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("DK Isles", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("DK Isles (K Rool's Ship)", type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("DK Isles (Banana Fairy Island)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("DK Isles (K-Lumsy's Prison)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Hideout Helm (Blast-O-Matic On)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Song("Move Get", type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=10.05),
    Song("Gun Get", type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.53),
    Song("Hideout Helm (Blast-O-Matic Off)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Hideout Helm (Bonus Barrels)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Crystal Caves (Cabins)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Crystal Caves (Rotating Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Crystal Caves (Tile Flipping)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Creepy Castle (Tunnels)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Intro Story Medley", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Training Grounds", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Song("Enguarde", type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("K-Lumsy Celebration", type=SongType.BGM, memory=0x110, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Creepy Castle (Crypt)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Headphones Get", type=SongType.MajorItem, memory=0x4BC, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.23),
    Song("Pearl Get", type=SongType.MajorItem, memory=0x43E, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=0.73),
    Song("Creepy Castle (Dungeon w/ Chains)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Angry Aztec (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Jungle Japes (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Frantic Factory (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Gloomy Galleon (Lobby)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Main Menu", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Creepy Castle (Inner Crypts)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Creepy Castle (Ballroom)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Creepy Castle (Greenhouse)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("K Rool's Theme", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Fungi Forest (Winch)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Creepy Castle (Wind Tower)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Creepy Castle (Tree)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("Creepy Castle (Museum)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Song("BBlast Final Star", type=SongType.Event, memory=0x445, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.36),
    Song("Drop Rainbow Coin", type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=0.91),
    Song("Rainbow Coin Get", type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.06),
    Song("Normal Star", type=SongType.MinorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.04),
    Song("Bean Get", type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.86),
    Song("Crystal Caves (Army Dillo)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Creepy Castle (Kut Out)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("Creepy Castle (Dungeon w/out Chains)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Banana Medal Get", type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.85),
    Song("K Rool's Battle", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Song("Fungi Forest (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Crystal Caves (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Creepy Castle (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Hideout Helm (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Creepy Castle (Trash Can)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("End Sequence", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("K-Lumsy Ending", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Song("Jungle Japes", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Jungle Japes (Cranky's Area)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("K Rool Takeoff", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Crystal Caves (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Fungi Forest (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("Creepy Castle (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("DK Isles (Snide's Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Song("K Rool's Entrance", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Song("Monkey Smash", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Fungi Forest (Rabbit Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Song("Game Over", type=SongType.Protected, memory=0x1D8),
    Song("Wrinkly Kong", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Song("100th CB Get", type=SongType.Event, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=2.10),
    Song("K Rool's Defeat", type=SongType.Protected, memory=0x18),
    Song("Nintendo Logo", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
]

ExcludedSongsSelector = []
ExclSongsItems = [
    SongExclusionItem("Wrinkly", 0, "Removes Wrinkly doors from playing her theme."),
    SongExclusionItem("Transformation", 3, "The game will no longer play the transformation sound effect."),
    SongExclusionItem("Pause Music", 4, "The pause menu music will no longer play."),
    SongExclusionItem("Sub Areas", 5, "Sub-Areas will no longer play their song, meaning that there's 1 piece of music for the entire level."),
    # SongExclusionItem("Shops", 1, "COMING SOON: Makes shops inherit the previous song."), # TODO: Fix this
    # SongExclusionItem("Events", 2, "COMING SOON: Events will no longer play a song."), # TODO: Fix this
]
for item in ExclSongsItems:
    if item.name != "No Group":
        ExcludedSongsSelector.append({"name": item.name, "value": item.name.lower().replace(" ", "_"), "tooltip": item.tooltip, "shift": item.shift})
