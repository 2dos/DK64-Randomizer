"""Data of the song breakdowns in ROM."""
from randomizer.Enums.SongType import SongType
from randomizer.Enums.SongGroups import SongGroup
from randomizer.Enums.Songs import Songs


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


song_data = {
    Songs.Silence: Song("Silence", type=SongType.System, memory=0x00),
    Songs.JapesStart: Song("Jungle Japes (Starting Area)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.Cranky: Song("Cranky's Lab", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy]),
    Songs.JapesCart: Song("Jungle Japes (Minecart)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.JapesDillo: Song("Jungle Japes (Army Dillo)", type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Songs.JapesCaves: Song("Jungle Japes (Caves/Underground)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Funky: Song("Funky's Hut", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy]),
    Songs.UnusedCoin: Song("Unused Coin Pickup", type=SongType.Protected, memory=0x440),
    Songs.Minigames: Song("Bonus Minigames", type=SongType.BGM, memory=0x189, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Triangle: Song("Triangle Trample", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.47),
    Songs.Guitar: Song("Guitar Gazump", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=3.99),
    Songs.Bongos: Song("Bongo Blast", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm], song_length=3.42),
    Songs.Trombone: Song("Trombone Tremor", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=5.05),
    Songs.Saxophone: Song("Saxophone Slam", type=SongType.Event, memory=0x8C2, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=4.22),
    Songs.AztecMain: Song("Angry Aztec", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.Transformation: Song("Transformation", type=SongType.Event, memory=0xA34, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy], song_length=4.31),
    Songs.MiniMonkey: Song("Mini Monkey", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.HunkyChunky: Song("Hunky Chunky", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Songs.GBGet: Song("Golden Banana/Key Get", type=SongType.MajorItem, memory=0x8C4, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.86),
    Songs.AztecBeetle: Song("Angry Aztec (Beetle Slide)", type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.OhBanana: Song("Oh Banana", type=SongType.MajorItem, memory=0xABD, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=3.25),
    Songs.AztecTemple: Song("Angry Aztec (Temple)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CompanyCoinGet: Song("Company Coin Get", type=SongType.MajorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.07),
    Songs.BananaCoinGet: Song("Banana Coin Get", type=SongType.MinorItem, memory=0x637, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=0.46),
    Songs.VultureRing: Song("Going through Vulture Ring", type=SongType.Event, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm]),
    Songs.AztecDogadon: Song("Angry Aztec (Dogadon)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Songs.Aztec5DT: Song("Angry Aztec (5DT)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryCarRace: Song("Frantic Factory (Car Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryMain: Song("Frantic Factory", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.Snide: Song("Snide's HQ", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.JapesTunnels: Song("Jungle Japes (Tunnels)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Candy: Song("Candy's Music Shop", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MinecartCoinGet: Song("Minecart Coin Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.61),
    Songs.MelonSliceGet: Song("Melon Slice Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.87),
    Songs.PauseMenu: Song("Pause Menu", type=SongType.BGM, memory=0x1D4, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CrystalCoconutGet: Song("Crystal Coconut Get", type=SongType.MinorItem, memory=0x63F, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.67),
    Songs.Rambi: Song("Rambi", type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.AztecTunnels: Song("Angry Aztec (Tunnels)", type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.WaterDroplets: Song("Water Droplets", type=SongType.Ambient, memory=0x914),
    Songs.FactoryJack: Song("Frantic Factory (Mad Jack)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy]),
    Songs.Success: Song("Success", type=SongType.Event, memory=0x8CD, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy], song_length=2.13),
    Songs.StartPause: Song("Start (To pause game)", type=SongType.Protected, memory=0x85E),
    Songs.Failure: Song("Failure", type=SongType.Event, memory=0x89D, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy], song_length=3.27),
    Songs.TransitionOpen: Song("DK Transition (Opening)", type=SongType.System, memory=0x854),
    Songs.TransitionClose: Song("DK Transition (Closing)", type=SongType.System, memory=0x854),
    Songs.JapesHighPitched: Song("Unused High-Pitched Japes", type=SongType.Protected, memory=0x444),
    Songs.FairyTick: Song("Fairy Tick", type=SongType.MinorItem, memory=0x8C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Calm], song_length=2.08),
    Songs.MelonSliceDrop: Song("Melon Slice Drop", type=SongType.MinorItem, memory=0x635, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Calm], song_length=1.14),
    Songs.AztecChunkyKlaptraps: Song("Angry Aztec (Chunky Klaptraps)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.FactoryCrusher: Song("Frantic Factory (Crusher Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.JapesBlast: Song("Jungle Japes (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.FactoryResearchAndDevelopment: Song("Frantic Factory (R&D)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.FactoryProduction: Song("Frantic Factory (Production Room)", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.TroffNScoff: Song("Troff 'n' Scoff", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.BossDefeat: Song("Boss Defeat", type=SongType.Event, memory=0x89A, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=5.35),
    Songs.AztecBlast: Song("Angry Aztec (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.GalleonOutside: Song("Gloomy Galleon (Outside)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.BossUnlock: Song("Boss Unlock", type=SongType.Event, memory=0x98, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=12.27),
    Songs.AwaitingBossEntry: Song("Awaiting Entering the Boss", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.TwinklySounds: Song("Generic Twinkly Sounds", type=SongType.Ambient, memory=0x934),
    Songs.GalleonPufftoss: Song("Gloomy Galleon (Pufftoss)", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Songs.GalleonSealRace: Song("Gloomy Galleon (Seal Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.GalleonTunnels: Song("Gloomy Galleon (Tunnels)", type=SongType.BGM, memory=0x18B, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonLighthouse: Song("Gloomy Galleon (Lighthouse)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.BattleArena: Song("Battle Arena", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight, SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.DropCoins: Song("Drop Coins (Minecart)", type=SongType.MinorItem, memory=0x445, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=1.14),
    Songs.FairyNearby: Song("Fairy Nearby", type=SongType.Ambient, memory=0x925),
    Songs.Checkpoint: Song("Checkpoint", type=SongType.MinorItem, memory=0x447, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=0.64),
    Songs.ForestDay: Song("Fungi Forest (Day)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.BlueprintGet: Song("Blueprint Get", type=SongType.MajorItem, memory=0x4C5, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=1.87),
    Songs.ForestNight: Song("Fungi Forest (Night)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.StrongKong: Song("Strong Kong", type=SongType.BGM, memory=0x19A, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Rocketbarrel: Song("Rocketbarrel Boost", type=SongType.BGM, memory=0x192, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Sprint: Song("Orangstand Sprint", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.ForestCart: Song("Fungi Forest (Minecart)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.DKRap: Song("DK Rap", type=SongType.BGM, memory=0x900, location_tags=[SongGroup.Fight, SongGroup.LobbyShop, SongGroup.Interiors, SongGroup.Exteriors, SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.BlueprintDrop: Song("Blueprint Drop", type=SongType.MajorItem, memory=0x63D, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=2.08),
    Songs.Galleon2DS: Song("Gloomy Galleon (2DS)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Galleon5DS: Song("Gloomy Galleon (5DS/Submarine)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonChest: Song("Gloomy Galleon (Pearls Chest)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.GalleonMermaid: Song("Gloomy Galleon (Mermaid Palace)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.ForestDogadon: Song("Fungi Forest (Dogadon)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Songs.MadMazeMaul: Song("Mad Maze Maul", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.Caves: Song("Crystal Caves", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesTantrum: Song("Crystal Caves (Giant Kosha Tantrum)", type=SongType.BGM, memory=0x193, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.NintendoLogoOld: Song("Nintendo Logo (Old?)", type=SongType.System, memory=0x102),
    Songs.SuccessRaces: Song("Success (Races)", type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=23.75),
    Songs.FailureRaces: Song("Failure (Races & Try Again)", type=SongType.Event, memory=0x118, location_tags=[SongGroup.Minigames, SongGroup.Spawning], mood_tags=[SongGroup.Gloomy], song_length=23.75),
    Songs.BonusBarrelIntroduction: Song("Bonus Barrel Introduction", type=SongType.Protected, memory=0x100),
    Songs.StealthySnoop: Song("Stealthy Snoop", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MinecartMayhem: Song("Minecart Mayhem", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.GalleonMechFish: Song("Gloomy Galleon (Mechanical Fish)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.GalleonBlast: Song("Gloomy Galleon (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestAnthill: Song("Fungi Forest (Anthill)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.ForestBarn: Song("Fungi Forest (Barn)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestMill: Song("Fungi Forest (Mill)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.SeasideSounds: Song("Generic Seaside Sounds", type=SongType.Ambient, memory=0x912),
    Songs.ForestSpider: Song("Fungi Forest (Spider)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.ForestMushroomRooms: Song("Fungi Forest (Mushroom Top Rooms)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestMushroom: Song("Fungi Forest (Giant Mushroom)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.BossIntroduction: Song("Boss Introduction", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.TagBarrel: Song("Tag Barrel (All of them)", type=SongType.Protected, memory=0x1CA),
    Songs.CavesBeetleRace: Song("Crystal Caves (Beetle Race)", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.CavesIgloos: Song("Crystal Caves (Igloos)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MiniBoss: Song("Mini Boss", type=SongType.BGM, memory=0x1AA, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Songs.Castle: Song("Creepy Castle", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleCart: Song("Creepy Castle (Minecart)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.BaboonBalloon: Song("Baboon Balloon", type=SongType.Event, memory=0x19A, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy], song_length=20.04),
    Songs.GorillaGone: Song("Gorilla Gone", type=SongType.BGM, memory=0x190, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.Isles: Song("DK Isles", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.IslesKremIsle: Song("DK Isles (K. Rool's Ship)", type=SongType.BGM, memory=0x109, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.IslesBFI: Song("DK Isles (Banana Fairy Island)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.IslesKLumsy: Song("DK Isles (K. Lumsy's Prison)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors, SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HelmBoMOn: Song("Hideout Helm (Blast-O-Matic On)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy]),
    Songs.MoveGet: Song("Move Get", type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=10.05),
    Songs.GunGet: Song("Gun Get", type=SongType.MajorItem, memory=0x892, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.53),
    Songs.HelmBoMOff: Song("Hideout Helm (Blast-O-Matic Off)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HelmBonus: Song("Hideout Helm (Bonus Barrels)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.CavesCabins: Song("Crystal Caves (Cabins)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CavesRotatingRoom: Song("Crystal Caves (Rotating Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.CavesIceCastle: Song("Crystal Caves (Tile Flipping)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.CastleTunnels: Song("Creepy Castle (Tunnels)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.IntroStory: Song("Intro Story Medley", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.TrainingGrounds: Song("Training Grounds", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Calm]),
    Songs.Enguarde: Song("Enguarde", type=SongType.BGM, memory=0x198, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.KLumsyCelebration: Song("K. Lumsy Celebration", type=SongType.BGM, memory=0x110, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.CastleCrypt: Song("Creepy Castle (Crypt)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HeadphonesGet: Song("Headphones Get", type=SongType.MajorItem, memory=0x4BC, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.23),
    Songs.PearlGet: Song("Pearl Get", type=SongType.MajorItem, memory=0x43E, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy, SongGroup.Calm], song_length=0.73),
    Songs.CastleDungeon_Chains: Song("Creepy Castle (Dungeon w/ Chains)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.AztecLobby: Song("Angry Aztec (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.JapesLobby: Song("Jungle Japes (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.FactoryLobby: Song("Frantic Factory (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.GalleonLobby: Song("Gloomy Galleon (Lobby)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.MainMenu: Song("Main Menu", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.CastleInnerCrypts: Song("Creepy Castle (Inner Crypts)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleBallroom: Song("Creepy Castle (Ballroom)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleGreenhouse: Song("Creepy Castle (Greenhouse)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.KRoolTheme: Song("K. Rool's Theme", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.ForestWinch: Song("Fungi Forest (Winch)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleTower: Song("Creepy Castle (Wind Tower)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleTree: Song("Creepy Castle (Tree)", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.CastleMuseum: Song("Creepy Castle (Museum)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy]),
    Songs.BBlastFinalStar: Song("Barrel Blast Final Star", type=SongType.Event, memory=0x445, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.36),
    Songs.DropRainbowCoin: Song("Drop Rainbow Coin", type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Spawning], mood_tags=[SongGroup.Happy], song_length=0.91),
    Songs.RainbowCoinGet: Song("Rainbow Coin Get", type=SongType.MajorItem, memory=0x647, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.06),
    Songs.NormalStar: Song("Normal Star", type=SongType.MinorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.04),
    Songs.BeanGet: Song("Bean Get", type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=1.86),
    Songs.CavesDillo: Song("Crystal Caves (Army Dillo)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleKutOut: Song("Creepy Castle (Kut Out)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.CastleDungeon_NoChains: Song("Creepy Castle (Dungeon w/out Chains)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.BananaMedalGet: Song("Banana Medal Get", type=SongType.MajorItem, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=3.85),
    Songs.KRoolBattle: Song("K. Rool's Battle", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Fight], mood_tags=[SongGroup.Happy]),
    Songs.ForestLobby: Song("Fungi Forest (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.CavesLobby: Song("Crystal Caves (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleLobby: Song("Creepy Castle (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.HelmLobby: Song("Hideout Helm (Lobby)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleTrash: Song("Creepy Castle (Trash Can)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.EndSequence: Song("End Sequence", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.KLumsyEnding: Song("K. Lumsy Ending", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy, SongGroup.Calm]),
    Songs.JapesMain: Song("Jungle Japes", type=SongType.BGM, memory=0x101, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.JapesStorm: Song("Jungle Japes (Cranky's Area)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.KRoolTakeoff: Song("K. Rool Takeoff", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.CavesBlast: Song("Crystal Caves (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.ForestBlast: Song("Fungi Forest (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.CastleBlast: Song("Creepy Castle (Baboon Blast)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.IslesSnideRoom: Song("DK Isles (Snide's Room)", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Interiors], mood_tags=[SongGroup.Happy, SongGroup.Gloomy]),
    Songs.KRoolEntrance: Song("K. Rool's Entrance", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
    Songs.MonkeySmash: Song("Monkey Smash", type=SongType.BGM, memory=0x100, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.ForestRabbitRace: Song("Fungi Forest (Rabbit Race)", type=SongType.BGM, memory=0x188, location_tags=[SongGroup.Minigames], mood_tags=[SongGroup.Happy]),
    Songs.GameOver: Song("Game Over", type=SongType.Protected, memory=0x1D8),
    Songs.WrinklyKong: Song("Wrinkly Kong", type=SongType.BGM, memory=0x18A, location_tags=[SongGroup.LobbyShop], mood_tags=[SongGroup.Gloomy, SongGroup.Calm]),
    Songs.FinalCBGet: Song("100th CB Get", type=SongType.Event, memory=0x645, location_tags=[SongGroup.Collection], mood_tags=[SongGroup.Happy], song_length=2.10),
    Songs.KRoolDefeat: Song("K. Rool's Defeat", type=SongType.Protected, memory=0x18),
    Songs.NintendoLogo: Song("Nintendo Logo", type=SongType.BGM, memory=0x108, location_tags=[SongGroup.Exteriors], mood_tags=[SongGroup.Happy]),
}

SortedSongList = [
    # DK Isles BGM
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
    # Jungle Japes BGM
    Songs.JapesMain,
    Songs.JapesStart,
    Songs.JapesTunnels,
    Songs.JapesStorm,
    Songs.JapesCaves,
    Songs.JapesBlast,
    Songs.JapesCart,
    Songs.JapesDillo,
    # Angry Aztec BGM
    Songs.AztecMain,
    Songs.AztecTunnels,
    Songs.AztecTemple,
    Songs.Aztec5DT,
    Songs.AztecBlast,
    Songs.AztecBeetle,
    Songs.AztecChunkyKlaptraps,
    Songs.AztecDogadon,
    # Frantic Factory BGM
    Songs.FactoryMain,
    Songs.FactoryProduction,
    Songs.FactoryResearchAndDevelopment,
    Songs.FactoryCrusher,
    Songs.FactoryCarRace,
    Songs.FactoryJack,
    # Gloomy Galleon BGM
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
    # Fungi Forest BGM
    Songs.ForestDay,
    Songs.ForestNight,
    Songs.ForestBarn,
    Songs.ForestMill,
    Songs.ForestAnthill,
    Songs.ForestMushroom,
    Songs.ForestMushroomRooms,
    Songs.ForestWinch,
    Songs.ForestSpider,
    Songs.ForestBlast,
    Songs.ForestRabbitRace,
    Songs.ForestCart,
    Songs.ForestDogadon,
    # Crystal Caves BGM
    Songs.Caves,
    Songs.CavesIgloos,
    Songs.CavesCabins,
    Songs.CavesRotatingRoom,
    Songs.CavesTantrum,
    Songs.CavesBlast,
    Songs.CavesIceCastle,
    Songs.CavesBeetleRace,
    Songs.CavesDillo,
    # Creepy Castle BGM
    Songs.Castle,
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
    # Hideout Helm BGM
    Songs.HelmBoMOn,
    Songs.HelmBoMOff,
    Songs.HelmBonus,
    # NPC BGM
    Songs.Cranky,
    Songs.Funky,
    Songs.Candy,
    Songs.Snide,
    Songs.WrinklyKong,
    # Moves and Animals BGM
    Songs.StrongKong,
    Songs.Rocketbarrel,
    Songs.Sprint,
    Songs.MiniMonkey,
    Songs.HunkyChunky,
    Songs.GorillaGone,
    Songs.Rambi,
    Songs.Enguarde,
    # Battle BGM
    Songs.BattleArena,
    Songs.TroffNScoff,
    Songs.AwaitingBossEntry,
    Songs.BossIntroduction,
    Songs.MiniBoss,
    Songs.KRoolBattle,
    # Menu and Story BGM
    Songs.MainMenu,
    Songs.PauseMenu,
    Songs.NintendoLogo,
    Songs.DKRap,
    Songs.IntroStory,
    Songs.KRoolTheme,
    Songs.KLumsyCelebration,
    Songs.KRoolTakeoff,
    Songs.KRoolEntrance,
    Songs.KLumsyEnding,
    Songs.EndSequence,
    # Minigame BGM
    Songs.Minigames,
    Songs.MadMazeMaul,
    Songs.StealthySnoop,
    Songs.MinecartMayhem,
    Songs.MonkeySmash,
    # Major Items
    Songs.OhBanana,
    Songs.GBGet,
    Songs.MoveGet,
    Songs.GunGet,
    Songs.BananaMedalGet,
    Songs.BlueprintDrop,
    Songs.BlueprintGet,
    Songs.HeadphonesGet,
    Songs.DropRainbowCoin,
    Songs.RainbowCoinGet,
    Songs.CompanyCoinGet,
    Songs.BeanGet,
    Songs.PearlGet,
    # Minor Items
    Songs.MelonSliceDrop,
    Songs.MelonSliceGet,
    Songs.BananaCoinGet,
    Songs.CrystalCoconutGet,
    Songs.FairyTick,
    Songs.MinecartCoinGet,
    Songs.DropCoins,
    Songs.Checkpoint,
    Songs.NormalStar,
    # Events
    Songs.Success,
    Songs.Failure,
    Songs.SuccessRaces,
    Songs.FailureRaces,
    Songs.BossUnlock,
    Songs.BossDefeat,
    Songs.Bongos,
    Songs.Guitar,
    Songs.Trombone,
    Songs.Saxophone,
    Songs.Triangle,
    Songs.BaboonBalloon,
    Songs.Transformation,
    Songs.VultureRing,
    Songs.BBlastFinalStar,
    Songs.FinalCBGet,
    # Ambient
    Songs.WaterDroplets,
    Songs.TwinklySounds,
    Songs.FairyNearby,
    Songs.SeasideSounds,
    # Protected
    Songs.UnusedCoin,
    Songs.StartPause,
    Songs.JapesHighPitched,
    Songs.BonusBarrelIntroduction,
    Songs.TagBarrel,
    Songs.GameOver,
    Songs.KRoolDefeat,
    # System
    Songs.Silence,
    Songs.TransitionOpen,
    Songs.TransitionClose,
    Songs.NintendoLogoOld,
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
    Songs.ForestWinch,
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

# This dict determines all of the dropdowns for selecting music, and how they
# will be grouped together.
MusicSelectionPanel = {
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
    "MajorItem": {"name": "Major Items", "type": "MajorItem", "songs": []},
    "MinorItem": {"name": "Minor Items", "type": "MinorItem", "songs": []},
    "Event": {"name": "Events", "type": "Event", "songs": []},
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
for songEnum in SortedSongList:
    song = song_data[songEnum]
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
                MusicSelectionPanel[category]["songs"].append(songJson)
    else:
        PlannableSongs[song.type.name].append(songJson)
        SongLocationList.append(songEnum.name)
        MusicSelectionPanel[song.type.name]["songs"].append(songJson)
