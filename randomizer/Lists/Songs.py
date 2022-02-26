"""Data of the song breakdowns in ROM."""
from enum import IntEnum, auto
from randomizer.Enums.SongType import SongType

class Song:
    """Class used for managing song objects."""

    def __init__(self, name, type=SongType.System, group=None):
        """Init SONG objects.

        Args:
            name (str): Name of the song.
            type (enum, optional): Songtype enum of the item. Defaults to SongType.System.
        """
        self.name = name
        self.type = type
        self.group = group # Use this to avoid overloading certain SongGroup with too many large songs

class SongGroup(IntEnum):
    JungleJapes = auto()
    AngryAztec = auto()
    FranticFactory = auto()
    GloomyGalleon = auto()
    FungiForest = auto()
    CrystalCaves = auto()
    Isles = auto()
    Self = auto()

song_data = [
    Song("Silence", SongType.System), # 0
    Song("Jungle Japes (Starting Area)", SongType.BGM, SongGroup.JungleJapes),
    Song("Cranky's Lab", SongType.BGM),
    Song("Jungle Japes (Minecart)", SongType.BGM),
    Song("Jungle Japes (Army Dillo)", SongType.BGM),
    Song("Jungle Japes (Caves/Underground)", SongType.BGM), # 5
    Song("Funky's Hut", SongType.BGM),
    Song("Unused Coin Pickup", SongType.Fanfare),
    Song("Bonus Minigames", SongType.BGM),
    Song("Triangle Trample", SongType.Event),
    Song("Guitar Gazump", SongType.Event), # 10
    Song("Bongo Blast", SongType.Event),
    Song("Trombone Tremor", SongType.Event),
    Song("Saxaphone Slam", SongType.Event),
    Song("Angry Aztec", SongType.BGM, SongGroup.AngryAztec),
    Song("Transformation", SongType.Event), # 15
    Song("Mini Monkey", SongType.BGM, SongGroup.Self),
    Song("Hunky Chunky", SongType.BGM, SongGroup.Self),
    Song("GB/Key Get", SongType.Fanfare),
    Song("Angry Aztec (Beetle Slide)", SongType.BGM),
    Song("Oh Banana", SongType.Fanfare), # 20
    Song("Angry Aztec (Temple)", SongType.BGM),
    Song("Company Coin Get", SongType.Fanfare),
    Song("Banana Coin Get", SongType.Fanfare),
    Song("Going through Vulture Ring", SongType.Fanfare),
    Song("Angry Aztec (Dogadon)", SongType.BGM), # 25
    Song("Angry Aztec (5DT)", SongType.BGM),
    Song("Frantic Factory (Car Race)", SongType.BGM),
    Song("Frantic Factory", SongType.BGM, SongGroup.FranticFactory),
    Song("Snide's HQ", SongType.BGM),
    Song("Jungle Japes (Tunnels)", SongType.BGM, SongGroup.Self), # 30
    Song("Candy's Music Shop", SongType.BGM),
    Song("Minecart Coin Get", SongType.Fanfare),
    Song("Melon Slice Get", SongType.Fanfare),
    Song("Pause Menu", SongType.BGM, SongGroup.Self),
    Song("Crystal Coconut Get", SongType.Fanfare), # 35
    Song("Rambi", SongType.BGM, SongGroup.JungleJapes),
    Song("Angry Aztec (Tunnels)", SongType.BGM, SongGroup.AngryAztec),
    Song("Water Droplets", SongType.Ambient),
    Song("Frantic Factory (Mad Jack)", SongType.BGM),
    Song("Success", SongType.Event), # 40
    Song("Start (To pause game)", SongType.Fanfare),
    Song("Failure", SongType.Event),
    Song("DK Transition (Opening)", SongType.System),
    Song("DK Transition (Closing)", SongType.System),
    Song("Unused High-Pitched Japes", SongType.Fanfare), # 45
    Song("Fairy Tick", SongType.Fanfare),
    Song("Melon Slice Drop", SongType.Fanfare),
    Song("Angry Aztec (Chunky Klaptraps)", SongType.BGM),
    Song("Frantic Factory (Crusher Room)", SongType.BGM),
    Song("Jungle Japes (Baboon Blast)", SongType.BGM), # 50
    Song("Frantic Factory (R&D)", SongType.BGM, SongGroup.FranticFactory),
    Song("Frantic Factory (Production Room)", SongType.BGM, SongGroup.FranticFactory),
    Song("Troff 'n' Scoff", SongType.BGM),
    Song("Boss Defeat", SongType.Event),
    Song("Angry Aztec (Baboon Blast)", SongType.BGM), # 55
    Song("Gloomy Galleon (Outside)", SongType.BGM, SongGroup.GloomyGalleon),
    Song("Boss Unlock", SongType.Event),
    Song("Awaiting Entering the Boss", SongType.BGM),
    Song("Generic Twinkly Sounds", SongType.Ambient),
    Song("Gloomy Galleon (Pufftoss)", SongType.BGM), # 60
    Song("Gloomy Galleon (Seal Race)", SongType.BGM),
    Song("Gloomy Galleon (Tunnels)", SongType.BGM, SongGroup.Self),
    Song("Gloomy Galleon (Lighthouse)", SongType.BGM),
    Song("Battle Arena", SongType.BGM),
    Song("Drop Coins (Minecart)", SongType.Fanfare), # 65
    Song("Fairy Nearby", SongType.Ambient),
    Song("Checkpoint", SongType.Fanfare),
    Song("Fungi Forest (Day)", SongType.BGM, SongGroup.FungiForest),
    Song("Blueprint Get", SongType.Fanfare),
    Song("Fungi Forest (Night)", SongType.BGM, SongGroup.FungiForest), # 70
    Song("Strong Kong", SongType.BGM, SongGroup.Self),
    Song("Rocketbarrel Boost", SongType.BGM, SongGroup.Self),
    Song("Orangstand Sprint", SongType.BGM, SongGroup.Self),
    Song("Fungi Forest (Minecart)", SongType.BGM),
    Song("DK Rap", SongType.BGM), # 75
    Song("Blueprint Drop", SongType.Fanfare),
    Song("Gloomy Galleon (2DS)", SongType.BGM),
    Song("Gloomy Galleon (5DS/Submarine)", SongType.BGM),
    Song("Gloomy Galleon (Pearls Chest)", SongType.BGM),
    Song("Gloomy Galleon (Mermaid Palace)", SongType.BGM), # 80
    Song("Fungi Forest (Dogadon)", SongType.BGM),
    Song("Mad Maze Maul", SongType.BGM),
    Song("Crystal Caves", SongType.BGM, SongGroup.CrystalCaves),
    Song("Crystal Caves (Giant Kosha Tantrum)", SongType.BGM, SongGroup.CrystalCaves),
    Song("Nintendo Logo (Old?)", SongType.System), # 85
    Song("Success (Races)", SongType.Event),
    Song("Failure (Races & Try Again)", SongType.Event),
    Song("Bonus Barrel Introduction", SongType.BGM),
    Song("Stealthy Snoop", SongType.BGM),
    Song("Minecart Mayhem", SongType.BGM), # 90
    Song("Gloomy Galleon (Mechanical Fish)", SongType.BGM),
    Song("Gloomy Galleon (Baboon Blast)", SongType.BGM),
    Song("Fungi Forest (Anthill)", SongType.BGM),
    Song("Fungi Forest (Barn)", SongType.BGM),
    Song("Fungi Forest (Mill)", SongType.BGM), # 95
    Song("Generic Seaside Sounds", SongType.Ambient),
    Song("Fungi Forest (Spider)", SongType.BGM),
    Song("Fungi Forest (Mushroom Top Rooms)", SongType.BGM),
    Song("Fungi Forest (Giant Mushroom)", SongType.BGM),
    Song("Boss Introduction", SongType.BGM), # 100
    Song("Tag Barrel (All of them)", SongType.System),
    Song("Crystal Caves (Beetle Race)", SongType.BGM),
    Song("Crystal Caves (Igloos)", SongType.BGM),
    Song("Mini Boss", SongType.BGM),
    Song("Creepy Castle", SongType.BGM), # 105
    Song("Creepy Castle (Minecart)", SongType.BGM),
    Song("Baboon Balloon", SongType.Event),
    Song("Gorilla Gone", SongType.BGM),
    Song("DK Isles", SongType.BGM, SongGroup.Isles),
    Song("DK Isles (K Rool's Ship)", SongType.BGM, SongGroup.Isles), # 110
    Song("DK Isles (Banana Fairy Island)", SongType.BGM, SongGroup.Isles),
    Song("DK Isles (K-Lumsy's Prison)", SongType.BGM, SongGroup.Isles),
    Song("Hideout Helm (Blast-O-Matic On)", SongType.BGM),
    Song("Move Get", SongType.Fanfare),
    Song("Gun Get", SongType.Fanfare), # 115
    Song("Hideout Helm (Blast-O-Matic Off)", SongType.BGM),
    Song("Hideout Helm (Bonus Barrels)", SongType.BGM),
    Song("Crystal Caves (Cabins)", SongType.BGM),
    Song("Crystal Caves (Rotating Room)", SongType.BGM),
    Song("Crystal Caves (Tile Flipping)", SongType.BGM), # 120
    Song("Creepy Castle (Tunnels)", SongType.BGM),
    Song("Intro Story Medley", SongType.BGM),
    Song("Training Grounds", SongType.BGM),
    Song("Enguarde", SongType.BGM, SongGroup.GloomyGalleon),
    Song("K-Lumsy Celebration", SongType.Event), # 125
    Song("Creepy Castle (Crypt)", SongType.BGM),
    Song("Headphones Get", SongType.Fanfare),
    Song("Pearl Get", SongType.Fanfare),
    Song("Creepy Castle (Dungeon w/ Chains)", SongType.BGM),
    Song("Angry Aztec (Lobby)", SongType.BGM), # 130
    Song("Jungle Japes (Lobby)", SongType.BGM),
    Song("Frantic Factory (Lobby)", SongType.BGM),
    Song("Gloomy Galleon (Lobby)", SongType.BGM),
    Song("Main Menu", SongType.BGM),
    Song("Creepy Castle (Inner Crypts)", SongType.BGM), # 135
    Song("Creepy Castle (Ballroom)", SongType.BGM),
    Song("Creepy Castle (Greenhouse)", SongType.BGM),
    Song("K Rool's Theme", SongType.BGM),
    Song("Fungi Forest (Winch)", SongType.BGM),
    Song("Creepy Castle (Wind Tower)", SongType.BGM), # 140
    Song("Creepy Castle (Tree)", SongType.BGM),
    Song("Creepy Castle (Museum)", SongType.BGM),
    Song("BBlast Final Star", SongType.Fanfare),
    Song("Drop Rainbow Coin", SongType.Fanfare),
    Song("Rainbow Coin Get", SongType.Fanfare), # 145
    Song("Normal Star", SongType.Fanfare),
    Song("Bean Get", SongType.Fanfare),
    Song("Crystal Caves (Army Dillo)", SongType.BGM),
    Song("Creepy Castle (Kut Out)", SongType.BGM),
    Song("Creepy Castle (Dungeon w/out Chains)", SongType.BGM), # 150
    Song("Banana Medal Get", SongType.Fanfare),
    Song("K Rool's Battle", SongType.BGM),
    Song("Fungi Forest (Lobby)", SongType.BGM),
    Song("Crystal Caves (Lobby)", SongType.BGM),
    Song("Creepy Castle (Lobby)", SongType.BGM), # 155
    Song("Hideout Helm (Lobby)", SongType.BGM),
    Song("Creepy Castle (Trash Can)", SongType.BGM),
    Song("End Sequence", SongType.BGM),
    Song("K-Lumsy Ending", SongType.BGM),
    Song("Jungle Japes", SongType.BGM, SongGroup.JungleJapes), # 160
    Song("Jungle Japes (Cranky's Area)", SongType.BGM, SongGroup.JungleJapes),
    Song("K Rool Takeoff", SongType.System),
    Song("Crystal Caves (Baboon Blast)", SongType.BGM),
    Song("Fungi Forest (Baboon Blast)", SongType.BGM),
    Song("Creepy Castle (Baboon Blast)", SongType.BGM), # 165
    Song("DK Isles (Snide's Room)", SongType.BGM),
    Song("K Rool's Entrance", SongType.BGM),
    Song("Monkey Smash", SongType.BGM),
    Song("Fungi Forest (Rabbit Race)", SongType.BGM),
    Song("Game Over", SongType.Event), # 170
    Song("Wrinkly Kong", SongType.BGM, SongGroup.Self),
    Song("100th CB Get", SongType.System),
    Song("K Rool's Defeat", SongType.System),
    Song("Nintendo Logo", SongType.BGM),
]
