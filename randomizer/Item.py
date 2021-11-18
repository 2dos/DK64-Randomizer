from Enums.Items import Items

class Item():
    def __init__(self, name):
        self.name = name

ItemList = {
    Items.Donkey: Item("Donkey"),
    Items.Diddy: Item("Diddy"),
    Items.Lanky: Item("Lanky"),
    Items.Tiny: Item("Tiny"),
    Items.Chunky: Item("Chunky"),

    Items.ProgressiveSlam: Item("Progressive Slam"),
    Items.BaboonBlast: Item("Baboon Blast"),
    Items.StrongKong: Item("Strong Kong"),
    Items.GorillaGrab: Item("Gorilla Grab"),
    Items.ChimpyCharge: Item("Chimpy Charge"),
    Items.RocketbarrelBoost: Item("Rocketbarrel Boost"),
    Items.SimianSpring: Item("Simian Spring"),
    Items.Orangstand: Item("Orangstand "),
    Items.BaboonBalloon: Item("Baboon Balloon"),
    Items.OrangstandSprint: Item("Orangstand Sprint"),
    Items.MiniMonkey: Item("Mini Monkey"),
    Items.PonyTailTwirl: Item("Pony Tail Twirl"),
    Items.Monkeyport: Item("Monkeyport"),
    Items.HunkyChunky: Item("Hunky Chunky"),
    Items.PrimatePunch: Item("Primate Punch"),
    Items.GorillaGone: Item("Gorilla Gone"),
    
    Items.Coconut: Item("Coconut"),
    Items.Peanut: Item("Peanut"),
    Items.Grape: Item("Grape"),
    Items.Feather: Item("Feather"),
    Items.Pineapple: Item("Pineapple"),
    Items.HomingAmmo: Item("Homing Ammo"),
    Items.SniperSight: Item("Sniper Sight"),
    Items.ProgressiveAmmoBelt: Item("Progressive Ammo Belt"),
    
    Items.Bongos: Item("Bongos"),
    Items.Guitar: Item("Guitar"),
    Items.Trombone: Item("Trombone"),
    Items.Saxophone: Item("Saxophone"),
    Items.Triangle: Item("Triangle"),
    Items.ProgressiveInstrumentUpgrade: Item("Progressive Instrument Upgrade"),
    
    Items.NintendoCoin: Item("Nintendo Coin"),
    Items.RarewareCoin: Item("Rareware Coin"),
    
    Items.CameraAndShockwave: Item("Camera and Shockwave"),
    
    Items.JungleJapesKey: Item("Jungle Japes Key"),
    Items.AngryAztecKey: Item("Angry Aztec Key"),
    Items.FranticFactoryKey: Item("Frantic Factory Key"),
    Items.GloomyGalleonKey: Item("Gloomy Galleon Key"),
    Items.FungiForestKey: Item("Fungi Forest Key"),
    Items.CrystalCavesKey: Item("Crystal Caves Key"),
    Items.CreepyCastleKey: Item("Creepy Castle Key"),
    Items.HideoutHelmKey: Item("Hideout Helm Key"),

    Items.GoldenBanana: Item("Golden Banana"),
    Items.BananaFairy: Item("Banana Fairy"),
    Items.BananaMedal: Item("Banana Medal"),
    Items.BattleCrown: Item("Battle Crown"),
}
