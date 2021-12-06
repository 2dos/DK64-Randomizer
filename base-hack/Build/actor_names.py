actor_names = [
    "Unknown 0",
    "Unknown 1",
    "DK",
    "Diddy",
    "Lanky",
    "Tiny",
    "Chunky",
    "Krusha",
    "Rambi",
    "Enguarde",
    "Unknown 10", # Always loaded # TODO: Figure out what actors 10-15 do
    "Unknown 11", # Always loaded # What is this?
    "Loading Zone Controller", # Always loaded
    "Object Model 2 Controller", # Always loaded
    "Unknown 14", # Always loaded # TODO: What is this?
    "Unknown 15", # Always loaded # TODO: What is this?
    "Unknown 16",
    "Cannon Barrel",
    "Rambi Crate",
    "Barrel (Diddy 5DI)",
    "Camera Focus Point", # Exists during some cutscenes
    "Pushable Box",
    "Barrel Spawner", # Normal barrel on a star pad, unused?
    "Cannon",
    "Race Hoop", # Vulture Race
    "Hunky Chunky Barrel",
    "TNT Barrel",
    "TNT Barrel Spawner", # Army Dillo
    "Bonus Barrel",
    "Minecart",
    "Fireball", # Boss fights
    "Bridge (Castle)",
    "Swinging Light",
    "Vine", # Brown
    "Kremling Kosh Controller",
    "Melon (Projectile)",
    "Peanut",
    "Rocketbarrel", # On Kong
    "Pineapple",
    "Large Brown Bridge", # Unused
    "Mini Monkey Barrel",
    "Orange",
    "Grape",
    "Feather",
    "Laser", # Projectile
    "Golden Banana", # Vulture, bonus barrels (US code 0x6818EE), probably some other places
    "Barrel Gun", # Teetering Turtle Trouble
    "Watermelon Slice",
    "Coconut",
    "Rocketbarrel", # The Barrel
    "Lime",
    "Ammo Crate", # Dropped by Red Klaptrap
    "Orange Pickup", # Dropped by Klump & Purple Klaptrap
    "Banana Coin", # Dropped by "Diddy", otherwise unused?
    "DK Coin", # Minecart
    "Small Explosion", # Seasick Chunky
    "Orangstand Sprint Barrel",
    "Strong Kong Barrel",
    "Swinging Light",
    "Fireball", # Mad Jack etc.
    "Bananaporter",
    "Boulder",
    "Minecart", # DK?
    "Vase (O)",
    "Vase (:)",
    "Vase (Triangle)",
    "Vase (+)",
    "Cannon Ball",
    "Unknown 68",
    "Vine", # Green
    "Counter", # Unused?
    "Kremling (Red)", # Lanky's Keyboard Game in R&D
    "Boss Key",
    "Cannon", # Galleon Minigame
    "Cannon Ball", # Galleon Minigame Projectile
    "Blueprint (Diddy)",
    "Blueprint (Chunky)",
    "Blueprint (Lanky)",
    "Blueprint (DK)",
    "Blueprint (Tiny)",
    "Minecart", # Chunky?
    "Fire Spawner? (Dogadon)", # TODO: Verify
    "Boulder Debris", # Minecart
    "Spider Web", # Fungi miniBoss
    "Steel Keg Spawner",
    "Steel Keg",
    "Crown",
    "Minecart", # BONUS
    "Unknown 88",
    "Fire", # Unused?
    "Ice Wall?",
    "Balloon (Diddy)",
    "Stalactite",
    "Rock Debris", # Rotating, Unused?
    "Car", # Unused?
    "Pause Menu",
    "Hunky Chunky Barrel (Dogadon)",
    "TNT Barrel Spawner (Dogadon)",
    "Tag Barrel", # 98
    "Fireball", # Get Out
    "1 Pad (Diddy 5DI)", # 100
    "2 Pad (Diddy 5DI)",
    "3 Pad (Diddy 5DI)",
    "4 Pad (Diddy 5DI)",
    "5 Pad (Diddy 5DI)",
    "6 Pad (Diddy 5DI)",
    "Kong Reflection",
    "Bonus Barrel (Hideout Helm)",
    "Unknown 108",
    "Race Checkpoint",
    "CB Bunch", # Unused? Doesn't seem to work, these are normally model 2
    "Balloon (Chunky)",
    "Balloon (Tiny)",
    "Balloon (Lanky)",
    "Balloon (DK)",
    "K. Lumsy's Cage", # TODO: Also rabbit race finish line?
    "Chain",
    "Beanstalk",
    "Yellow ?", # Unused?
    "CB Single (Blue)", # Unused? Doesn't seem to work, these are normally model 2
    "CB Single (Yellow)", # Unused? Doesn't seem to work, these are normally model 2
    "Crystal Coconut", # Unused? Doesn't seem to work, these are normally model 2
    "DK Coin", # Multiplayer
    "Kong Mirror", # Creepy Castle Museum
    "Barrel Gun", # Peril Path Panic
    "Barrel Gun", # Krazy Kong Klamour
    "Fly Swatter",
    "Searchlight", # Searchlight Seek
    "Headphones",
    "Enguarde Crate",
    "Apple", # Fungi
    "Worm", # Fungi
    "Enguarde Crate (Unused?)",
    "Barrel",
    "Training Barrel",
    "Boombox", # Treehouse
    "Tag Barrel",
    "Tag Barrel", # Troff'n'Scoff
    "B. Locker",
    "Rainbow Coin Patch",
    "Rainbow Coin",
    "Unknown 141",
    "Unknown 142",
    "Unknown 143",
    "Unknown 144",
    "Cannon (Seasick Chunky)", # Internal name "Puffer cannon"
    "Unknown 146",
    "Balloon (Unused - K. Rool)", # Internal Name: K. Rool Banana Balloon, unsure of purpose. Can only be popped by Lanky
    "Rope", # K. Rool's Arena
    "Banana Barrel", # Lanky Phase
    "Banana Barrel Spawner", # Lanky Phase, internal name "Skin barrel generator"
    "Unknown 151",
    "Unknown 152",
    "Unknown 153",
    "Unknown 154",
    "Unknown 155",
    "Wrinkly",
    "Unknown 157",
    "Unknown 158",
    "Unknown 159",
    "Unknown 160",
    "Unknown 161",
    "Unknown 162",
    "Banana Fairy (BFI)",
    "Ice Tomato",
    "Tag Barrel (King Kut Out)",
    "King Kut Out Part",
    "Cannon",
    "Unknown 168",
    "Puftup", # Puftoss Fight
    "Damage Source", # K. Rool's Glove
    "Orange", # Krusha's Gun
	"Unknown 172",
    "Cutscene Controller",
    "Unknown 174",
    "Kaboom",
    "Timer",
    "Timer Controller", # Puftoss Fight & Fac Beaver Bother Spawn Timer
    "Beaver", # Blue
    "Shockwave (Mad Jack)",
    "Krash", # Minecart Club Guy
    "Book", # Castle Library
    "Klobber",
    "Zinger",
    "Snide",
    "Army Dillo",
    "Kremling", # Kremling Kosh
    "Klump",
    "Camera",
    "Cranky",
    "Funky",
    "Candy",
    "Beetle", # Race
    "Mermaid",
    "Vulture",
    "Squawks",
    "Cutscene DK",
    "Cutscene Diddy",
    "Cutscene Lanky",
    "Cutscene Tiny",
    "Cutscene Chunky",
    "Llama",
    "Fairy Picture",
    "Padlock (T&S)",
    "Mad Jack",
    "Klaptrap", # Green
    "Zinger",
    "Vulture (Race)",
    "Klaptrap (Purple)",
    "Klaptrap (Red)",
    "GETOUT Controller",
    "Klaptrap (Skeleton)",
    "Beaver (Gold)",
    "Fire Column Spawner", # Japes Minecart
    "Minecart (TNT)", # Minecart Mayhem
    "Minecart (TNT)",
    "Puftoss",
    "Unknown 217",
    "Handle",
    "Slot",
    "Cannon (Seasick Chunky)",
    "Light Piece", # Lanky Phase
    "Banana Peel", # Lanky Phase
    "Fireball Spawner", # Factory Crusher Room
    "Mushroom Man",
    "Unknown 225",
    "Troff",
    "K. Rool's Foot", # Including leftmost toe
    "Bad Hit Detection Man",
    "K. Rool's Toe", # Rightmost 3 toes
    "Ruler",
    "Toy Box",
    "Text Overlay",
    "Squawks",
    "Scoff",
    "Robo-Kremling",
    "Dogadon",
    "Unknown 237",
    "Kremling",
    "Bongos",
    "Spotlight Fish",
    "Kasplat (DK)",
    "Kasplat (Diddy)",
    "Kasplat (Lanky)",
    "Kasplat (Tiny)",
    "Kasplat (Chunky)",
    "Mechanical Fish",
    "Seal",
    "Banana Fairy",
    "Squawks with spotlight",
    "Owl",
    "Spider miniBoss",
    "Rabbit", # Fungi
    "Nintendo Logo",
    "Cutscene Object", # For objects animated by Cutscenes
    "Shockwave",
    "Minigame Controller",
    "Fire Breath Spawner", # Aztec Beetle Race
    "Shockwave", # Boss
    "Guard", # Stealthy Snoop
    "Text Overlay", # K. Rool fight
    "Robo-Zinger",
    "Krossbones",
    "Fire Shockwave (Dogadon)",
    "Squawks",
    "Light beam", # Boss fights etc
    "DK Rap Controller", # Handles the lyrics etc
    "Shuri",
    "Gimpfish",
    "Mr. Dice",
    "Sir Domino",
    "Mr. Dice",
    "Rabbit",
    "Fireball (With Glasses)", # From Chunky 5DI
    "Unknown 274",
    "K. Lumsy",
    "Spiderling",
    "Squawks",
    "Projectile", # Spider miniBoss
    "Trap Bubble", # Spider miniBoss
    "Spider Silk String", # Spider miniBoss
    "K. Rool (DK Phase)",
    "Retexturing Controller", # Beaver Bother
    "Skeleton Head",
    "Unknown 284",
    "Bat",
    "Giant Clam",
    "Unknown 287",
    "Tomato", # Fungi
    "Kritter-in-a-Sheet",
    "Puftup",
    "Kosha",
    "K. Rool (Diddy Phase)",
    "K. Rool (Lanky Phase)",
    "K. Rool (Tiny Phase)",
    "K. Rool (Chunky Phase)",
    "Unknown 296",
    "Battle Crown Controller",
    "Unknown 298",
    "Textbox",
    "Snake", # Teetering Turtle Trouble
    "Turtle", # Teetering Turtle Trouble
    "Toy Car", # Player in the Factory Toy Car Race
    "Toy Car",
    "Camera", # Factory Toy Car Race
    "Missile", # Car Race
    "Unknown 306",
    "Unknown 307",
    "Seal",
    "Kong Logo (Instrument)", # DK for DK, Star for Diddy, DK for Lanky, Flower for Tiny, DK for Chunky
    "Spotlight", # Tag barrel, instrument etc.
    "Race Checkpoint", # Seal race & Castle car race
    "Minecart (TNT)",
    "Idle Particle",
    "Rareware Logo",
    "Unknown 315",
    "Kong (Tag Barrel)",
    "Locked Kong (Tag Barrel)",
    "Unknown 318",
    "Propeller (Boat)",
    "Potion", # Cranky Purchase
    "Fairy (Refill)", # Refill Fairy
    "Car", # Car Race
    "Enemy Car", # Car Race, aka George
    "Text Overlay Controller", # Candy's
    "Shockwave", # Simian Slam
    "Main Menu Controller",
    "Kong", # Krazy Kong Klamour
    "Klaptrap", # Peril Path Panic
    "Fairy", # Peril Path Panic
    "Bug", # Big Bug Bash
    "Klaptrap", # Searchlight Seek
    "Big Bug Bash Controller?", # TODO: Fly swatter?
    "Barrel (Main Menu)",
    "Padlock (K. Lumsy)",
    "Snide's Menu",
    "Training Barrel Controller",
    "Multiplayer Model (Main Menu)",
    "End Sequence Controller",
    "Arena Controller", # Rambi/Enguarde
    "Bug", # Trash Can
    "Unknown 341",
    "Try Again Dialog",
    "Pause Menu", # Mystery menu bosses
]