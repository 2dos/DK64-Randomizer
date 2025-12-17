
# Jungle Japes
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Jungle Japes | Near Funky |  | `self.logic = lambda _: True` | 
| Jungle Japes | On Painting Hill |  | `self.logic = lambda _: True` | 
| Jungle Japes | Next to level entrance |  | `self.logic = lambda _: True` | 
| Jungle Japes | On Tree (Starting Area) |  | `l.climbing` | 
| Jungle Japes | Next to first tunnel entrance |  | `self.logic = lambda _: True` | 
| Jungle Japes | Diddy Cavern |  | `self.logic = lambda _: True` | 
| Jungle Japes | Inside Diddy's Cavern |  | `self.logic = lambda _: True` | 
| Jungle Japes | First tunnel - later half |  | `self.logic = lambda _: True` | 
| Jungle Japes | Painting Hill | MelonCrate | `self.logic = lambda _: True` | 
| Jungle Japes | Hive area near Hunky barrel |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near Stump |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near Log |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near the Vine Pit |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vine Pit |  | `self.logic = lambda _: True` | 
| Jungle Japes | Lanky useless slope - middle |  | `self.logic = lambda _: True` | 
| Jungle Japes | Lanky useless slope - left | MelonCrate | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky-tunnel Crossing |  | `self.logic = lambda _: True` | 
| Jungle Japes | In the Rambi Cave | CrownPad, Bananaport | `self.logic = lambda _: True` | 
| Jungle Japes | Fairy Pool |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind Lanky Hut |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind DK Hut |  | `self.logic = lambda _: True` | 
| Jungle Japes | Left of DK hut |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near the Rambi cage |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind Stormy Shop |  | `self.logic = lambda _: True` | 
| Jungle Japes | Minecart Alcove |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near highest shop |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind Diddy's Mountain |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near Kong Cage |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near the cannon |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind the Mountain |  | `self.logic = lambda _: True` | 
| Jungle Japes | Near Cannon Platform |  | `self.logic = lambda _: True` | 
| Jungle Japes | In Troff 'n' Scoff Alcove |  | `self.logic = lambda _: True` | 
| Jungle Japes | Lower River |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Near Warp 1 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Hive Warp 5 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Near Warp 2 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Painting Warp 3 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Far Warp 1 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Blast Warp 3 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Mountain Warp 2 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Tunnel Warp 4 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Mountain Warp 5 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Vanilla Stormy Warp 4 |  | `self.logic = lambda _: True` | 
| Jungle Japes | Behind the boulder |  | `self.logic = lambda _: True` | 
| Japes Under Ground | Underground: Behind Cannon |  | `self.logic = lambda _: True` | 
| Japes Under Ground | Underground: Near Vines |  | `self.logic = lambda _: True` | 
| Japes Lanky Cave | Painting Room: Near Peg | CrownPad, Bananaport | `self.logic = lambda _: True` | 
| Japes Mountain | Mountain: Near Entrance (Ground) |  | `self.logic = lambda _: True` | 
| Japes Mountain | Mountain: Near Entrance (High) |  | `self.logic = lambda _: True` | 
| Japes Mountain | Mountain: On Barrel |  | `self.logic = lambda _: True` | 
| Japes Mountain | Mountain: Near HiLo Machine |  | `(l.charge and l.isdiddy) or l.CanPhase(), group=5` | 
| Japes Mountain | Mountain: Under Conveyor | CrownPad, Bananaport | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase()` | 
| Japes Tiny Hive | Hive: Main Room |  | `self.logic = lambda _: True` | 
| Japes Tiny Hive | Hive: 1st Room |  | `self.logic = lambda _: True` | 
| Japes Tiny Hive | Hive: 3rd Room |  | `(l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()) and l.tiny` | 

# Angry Aztec
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Aztec Tiny Temple | Tiny Temple: Vulture Room |  | `l.CanSlamSwitch(Levels.AngryAztec, 1) and l.grape and l.islanky` | 
| Angry Aztec | Oasis |  | `self.logic = lambda _: True` | 
| Aztec Chunky5DTemple | Chunky 5DT |  | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple: Main room back left |  | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple: Starting Room (Low) |  | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple: Starting Room (High) |  | `l.CanSlamSwitch(Levels.AngryAztec, 1) and l.diddy` | 
| Aztec Tiny Temple | Tiny Temple: Kong Free Room |  | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple: Next to Kong cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Entrance tunnel - near DK door |  | `self.logic = lambda _: True` | 
| Angry Aztec | Blueprint Room | Bananaport | `l.CanPhase() or (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny)))` | 
| Angry Aztec | Near Oasis Sand |  | `self.logic = lambda _: True` | 
| Angry Aztec | Behind Tiny Temple |  | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - left |  | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - right |  | `self.logic = lambda _: True` | 
| Angry Aztec | On Tiny Temple |  | `((l.jetpack and l.diddy) or l.CanMoonkick()) and l.climbing` | 
| Angry Aztec | Near Oasis Shop |  | `self.logic = lambda _: True` | 
| Angry Aztec | Behind Llama Cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Near Hunky Chunky Barrel |  | `self.logic = lambda _: True` | 
| Angry Aztec | Left of Hunky Cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Right of Hunky Cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Behind Hunky Cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Near Llama Temple (Left) |  | `self.logic = lambda _: True` | 
| Angry Aztec | Near Llama Temple (Right) |  | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Llama Temple |  | `self.logic = lambda _: True` | 
| Angry Aztec | On Llama Temple - back |  | `(l.jetpack and l.diddy) or l.CanMoonkick()` | 
| Angry Aztec | On Llama Temple |  | `(l.jetpack and l.diddy) or l.CanMoonkick()` | 
| Angry Aztec | Near Quicksand Tunnel Shop |  | `self.logic = lambda _: True` | 
| Angry Aztec | On 5-Door Temple |  | `(l.jetpack and l.diddy) or l.CanMoonkick()` | 
| Angry Aztec | Near Strong Kong Warp |  | `self.logic = lambda _: True` | 
| Angry Aztec | Near Vulture Cage |  | `((l.can_use_vines or l.CanMoonkick()) and l.climbing) or (l.jetpack and l.diddy)` | 
| Angry Aztec | Under Vulture Cage |  | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Vulture cage shop |  | `self.logic = lambda _: True` | 
| Angry Aztec | Behind Gong tower |  | `self.logic = lambda _: True` | 
| Angry Aztec | Left of Gong tower |  | `self.logic = lambda _: True` | 
| Angry Aztec | Near Gong Tower |  | `self.logic = lambda _: True` | 
| Angry Aztec | Sealed Quicksand Tunnel |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Tunnel Warp 1 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Oasis Warp 2 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Totem Warp 2 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Totem Warp 5 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Totem Warp 3 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Oasis Warp 1 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Totem Warp 4 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Tunnel Warp 3 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Funky Warp 4 |  | `self.logic = lambda _: True` | 
| Angry Aztec | Vanilla Tunnel Warp 5 |  | `self.logic = lambda _: True` | 
| Aztec Donkey5DTemple | Donkey 5DT: Dead End |  | `self.logic = lambda _: True` | 
| Aztec Diddy5DTemple | Diddy 5DT: Dead End |  | `(l.peanut and l.isdiddy) or l.CanPhase()` | 
| Aztec Lanky5DTemple | Lanky 5DT: Dead End |  | `(l.grape and l.islanky) or l.CanPhase()` | 
| Aztec Lanky5DTemple | Lanky 5DT: Right side |  | `self.logic = lambda _: True` | 
| Aztec Tiny5DTemple | Tiny 5DT: Dead End |  | `(l.feather and l.istiny) or l.CanPhase(), group=7` | 
| Aztec Chunky5DTemple | Chunky 5DT: Right side |  | `self.logic = lambda _: True` | 
| Aztec Chunky5DTemple | Chunky 5DT: Left side |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Llama Right |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Entrance |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Next to Llama Right |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Next to Llama Left |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Llama Left |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Matching Room |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Vanilla Close Warp 1 |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Vanilla Far Warp 1 |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Vanilla Lava Warp 2 |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Vanilla Close Warp 2 |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | In the Water | CrownPad, DirtPatch, Bananaport | `Events.AztecLlamaSpit in l.Events and l.HasGun(Kongs.any) and l.swim and l.scope and ((l.istiny and l.isKrushaAdjacent(Kongs.tiny)) or (not l.istiny))` | 
| Aztec Llama Temple | Llama Temple: DK Switch |  | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple: Lava Room |  | `self.logic = lambda _: True` | 

# Frantic Factory
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Frantic Factory | Under R&D Grate | MelonCrate, Bananaport | `(l.grab and l.donkey) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Dark Room |  | `((l.punch and l.chunky) or l.CanPhase())` | 
| Frantic Factory | On Foyer Carpet |  | `self.logic = lambda _: True` | 
| Frantic Factory | Near Foyer carpet |  | `self.logic = lambda _: True` | 
| Frantic Factory | Clock-in room left |  | `self.logic = lambda _: True` | 
| Frantic Factory | Clock-in room right |  | `self.logic = lambda _: True` | 
| Frantic Factory | Near Hatch |  | `self.logic = lambda _: True` | 
| Frantic Factory | Hatch Pole Center |  | `self.logic = lambda _: True` | 
| Frantic Factory | Hatch Pole Bottom |  | `self.logic = lambda _: True` | 
| Frantic Factory | Tunnel to production room |  | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room Lower Section |  | `self.logic = lambda _: True` | 
| Frantic Factory | Under High Conveyors |  | `self.logic = lambda _: True` | 
| Frantic Factory | Past Tiny Production Bonus |  | `l.twirl and l.tiny` | 
| Frantic Factory | Vent platform near elevators |  | `self.logic = lambda _: True` | 
| Frantic Factory | Storage Room Corner |  | `self.logic = lambda _: True` | 
| Frantic Factory | Near left storage shop | MelonCrate | `self.logic = lambda _: True` | 
| Frantic Factory | Near right storage shop |  | `self.logic = lambda _: True` | 
| Frantic Factory | Dark Room Corner |  | `(l.punch and l.chunky) or l.phasewalk` | 
| Frantic Factory | Arcade Room Bench |  | `self.logic = lambda _: True` | 
| Frantic Factory | Next to DK Arcade |  | `self.logic = lambda _: True` | 
| Frantic Factory | Near Snide |  | `self.logic = lambda _: True` | 
| Frantic Factory | Near Snide (hidden) |  | `self.logic = lambda _: True` | 
| Frantic Factory | Right Corridor |  | `self.logic = lambda _: True` | 
| Frantic Factory | Number Game |  | `self.logic = lambda _: True` | 
| Frantic Factory | Under Block Tower Stairs |  | `self.logic = lambda _: True` | 
| Frantic Factory | On the Block Tower | CrownPad | `(l.spring or l.CanMoonkick() or l.CanMoontail())` | 
| Frantic Factory | Under Testing barrel |  | `self.logic = lambda _: True` | 
| Frantic Factory | Testing shop entrance left | MelonCrate | `self.logic = lambda _: True` | 
| Frantic Factory | Testing shop left |  | `self.logic = lambda _: True` | 
| Frantic Factory | Testing shop right |  | `self.logic = lambda _: True` | 
| Frantic Factory | Testing shop entrance right |  | `self.logic = lambda _: True` | 
| Frantic Factory | Piano Room left corner | CrownPad, Bananaport | `(l.trombone and l.lanky) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Piano Room right | CrownPad, Bananaport | `((l.trombone and l.islanky) or l.CanAccessRNDRoom())` | 
| Frantic Factory | Diddy R&D corner | CrownPad, Bananaport | `(l.guitar and l.diddy) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Diddy R&D | CrownPad, Bananaport | `((l.guitar and l.isdiddy) or l.CanAccessRNDRoom())` | 
| Frantic Factory | Chunky R&D | CrownPad, Bananaport | `(l.triangle and l.climbing and l.chunky and l.punch) or l.CanAccessRNDRoom()` | 
| Frantic Factory | In front of toy monster room | CrownPad, Bananaport | `((l.punch and l.climbing and l.ischunky) or l.CanAccessRNDRoom())` | 
| Frantic Factory | Car Race room |  | `(l.mini and l.istiny) or l.phasewalk` | 
| Frantic Factory | Also car race room |  | `((l.mini and l.istiny) or l.CanPhase())` | 
| Frantic Factory | R&D lever room |  | `self.logic = lambda _: True` | 
| Frantic Factory | Under second R&D Grate | MelonCrate, Bananaport | `(l.grab and l.donkey) or l.CanPhase() or l.generalclips` | 
| Frantic Factory | Vanilla Foyer Warp 2 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Foyer Warp 3 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla R&D Warp 2 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Snide Warp 3 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla High Warp 4 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Low Warp 4 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Testing Warp 5 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Foyer Warp 1 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Storage Warp 1 |  | `self.logic = lambda _: True` | 
| Frantic Factory | Vanilla Arcade Warp 5 |  | `self.logic = lambda _: True` | 
| Factory Crusher | Crusher: Central Safehaven |  | `(l.strongKong and l.isdonkey) or l.CanPhase() or l.generalclips` | 
| Factory Power Hut | Power Hut: Corner |  | `self.logic = lambda _: True` | 

# Gloomy Galleon
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Gloomy Galleon | Under cavern shop |  | `(l.punch and l.chunky) or l.CanPhase() or l.CanSkew(False, False)` | 
| Galleon Lighthouse | Lighthouse: Interior Rear |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Cactus | DirtPatch, CrownPad, Bananaport | `self.logic = lambda _: True` | 
| Gloomy Galleon | Front of cannonball |  | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Behind the cannonball |  | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Next to cannonball cannon |  | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Entrance tunnel crossing |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Tunnel to chests far |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Tunnel to chests close |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Chests tunnel alcove |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Chests room |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind Punch GB Chest |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind the cannon wreck |  | `self.logic = lambda _: True` | 
| Galleon2DShip | Lanky 2DS: Inside Chest | CrownPad, DirtPatch, Bananaport | `self.logic = lambda _: True` | 
| Gloomy Galleon | Left of cavern shop |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Front of cavern shop |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Bridge Warp 3 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near the Rocketbarrel |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near the Baboon Blast |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Lighthouse ladder |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Under lighthouse Enguarde box | CrownPad, DirtPatch, Bananaport | `Events.LighthouseEnguarde in l.Events` | 
| Gloomy Galleon | In Enguarde Alcove | CrownPad, DirtPatch, Bananaport | `Events.LighthouseEnguarde in l.Events` | 
| Gloomy Galleon | In Front of Mermaid Palace | CrownPad, DirtPatch, Bananaport | `Events.LighthouseEnguarde in l.Events` | 
| Gloomy Galleon | On Rocketbarrel platform |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Lighthouse Alcove | MelonCrate | `Events.WaterLowered in l.Events` | 
| Gloomy Galleon | Behind lighthouse shop | CrownPad, Bananaport | `self.logic = lambda _: True` | 
| Gloomy Galleon | On the submarine | CrownPad, DirtPatch, Bananaport | `Events.ShipyardEnguarde in l.Events` | 
| Gloomy Galleon | In the Shipwreck with Replenishables | CrownPad, DirtPatch, Bananaport | `Events.ShipyardEnguarde in l.Events` | 
| Gloomy Galleon | Behind Musical Cactus | CrownPad, DirtPatch, Bananaport | `Events.ShipyardEnguarde in l.Events` | 
| Gloomy Galleon | On Top of Mechfish Grate | DirtPatch, CrownPad, Bananaport | `Events.ShipyardEnguarde in l.Events` | 
| Gloomy Galleon | On Gold Tower | Bananaport | `((l.balloon and l.islanky) and Events.WaterRaised in l.Events or (Events.ShipyardTreasureRoomOpened in l.Events and l.monkey_maneuvers)) or l.CanMoonkick()` | 
| Gloomy Galleon | Treasure Room UnderWater | CrownPad, DirtPatch, Bananaport | `Events.ShipyardTreasureRoomOpened in l.Events` | 
| Gloomy Galleon | Vanilla Floating Warp 5 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Lighthouse Warp 1 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Alcove Warp 3 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Lighthouse Warp 5 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Cavern Warp 2 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Bridge Warp 3 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Floating Warp 2 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Gold Tower Warp 4 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Cavern Warp 1 |  | `self.logic = lambda _: True` | 
| Gloomy Galleon | Vanilla Floating Warp 4 |  | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick Ship: Left of Cannon |  | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick Ship: Entrance |  | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick Ship: Right of Cannon |  | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick Ship: Back left corner |  | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick Ship: Behind the non-alcoholic tower |  | `((l.punch and l.ischunky) or l.CanPhase())` | 
| Galleon Sick Bay | Seasick Ship: Behind Spinning Barrels |  | `(l.punch and l.ischunky) or l.CanPhase()` | 
| Galleon Lighthouse | Lighthouse: Bottom Left |  | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse: Back Right |  | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse: Behind Whomp's Fortress floor 2 |  | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse: On top of Whomp's Fortress |  | `self.logic = lambda _: True` | 

# Fungi Forest
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Fungi Forest | Giant Mushroom High Ladder Platform |  | `self.logic = lambda _: True` | 
| Fungi Forest | Front of Beanstalk |  | `self.logic = lambda _: True` | 
| Fungi Forest | Mill Grass | Bananaport | `self.logic = lambda _: True` | 
| Fungi Forest | Near Well | DirtPatch, Bananaport | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Clock |  | `self.logic = lambda _: True` | 
| Fungi Forest | In front of Clock |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Blue Tunnel |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Mills shop |  | `(l.TimeAccess(Regions.MillArea, Time.Day))` | 
| Fungi Forest | Behind rafters barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Left of rafters barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Diddy Pad |  | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Dark Attic |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Mill Tag |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Well Exit |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Winch |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Mill Punch Door |  | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Crusher Output |  | `self.logic = lambda _: True` | 
| Fungi Forest | En route to DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Right of DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Far Right of DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Behind DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Far Left of DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near DK Barn |  | `self.logic = lambda _: True` | 
| Fungi Forest | Alcove near the apple |  | `(l.TimeAccess(Regions.WormArea, Time.Night) or l.CanPhase())` | 
| Fungi Forest | On the Tomato Field |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near beanstalk shop |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Beanstalk Area Entrance |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Beanstalk |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Beanstalk Mini Monkey |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Giant Mushroom |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Yellow Tunnel | DirtPatch, Bananaport | `self.logic = lambda _: True` | 
| Fungi Forest | Near Lower Baboon Blast Ladder |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Baboon Blast |  | `self.logic = lambda _: True` | 
| Fungi Forest | Above Upper Baboon Blast Ladder |  | `self.logic = lambda _: True` | 
| Fungi Forest | Highest Giant Mushroom Platform |  | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Rabbit |  | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Rabbit's house |  | `self.logic = lambda _: True` | 
| Fungi Forest | Under Owl Tree |  | `self.logic = lambda _: True` | 
| Fungi Forest | Under the Owl Tree |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Owl Tree |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Owl Rocketbarrel |  | `self.logic = lambda _: True` | 
| Fungi Forest | Grass Near Owl Rocketbarrel | DirtPatch, Bananaport | `self.logic = lambda _: True` | 
| Fungi Forest | Top of Owl Tree |  | `((l.jetpack and l.isdiddy) or l.CanMoonkick())` | 
| Fungi Forest | On Mill |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Clock Warp 1 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Mill Warp 1 | MelonCrate | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Clock Warp 2 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Beanstalk Warp 2 | MelonCrate | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Clock Warp 3 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Clock Warp 4 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Owl Tree Warp 4 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Lower Warp 5 |  | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Upper Warp 5 | MelonCrate | `self.logic = lambda _: True` | 
| Fungi Forest | Vanilla Mushroom Warp 3 | MelonCrate | `self.logic = lambda _: True` | 
| Forest Anthill | Anthill: Orange Platform |  | `self.logic = lambda _: True` | 
| Forest Winch Room | Winch Room: Opposite Entrance |  | `self.logic = lambda _: True` | 
| Fungi Forest | Near Thornvine Barn |  | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK Barn: Near Entrance |  | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK Barn: Near Ladder |  | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK Barn: Next to ladder |  | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK Barn: back left |  | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill Front: Near Conveyor |  | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill Front: Near Mini Monkey |  | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill front: Near levers |  | `self.logic = lambda _: True` | 
| Forest Mill Back | Mill Back: near Chunky's coins |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: Near Tiny Bonus |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: Near Gun Switches |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: Near Bottom Cannon |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: Near vines |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: Next to a cannon |  | `((l.istiny and l.twirl) or (l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey))))` | 
| Forest Giant Mushroom | Giant Mushroom: Cannon below night door |  | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom: On Top Viney Platform |  | `self.logic = lambda _: True` | 
| Forest Mill Attic | Mill Attic: Near Box |  | `self.logic = lambda _: True` | 
| Forest Lanky Zingers Room | Mushroom Zingers: Opposite Entrance |  | `self.logic = lambda _: True` | 
| Forest Lanky Mushrooms Room | Mushroom Slam: Opposite Entrance |  | `self.logic = lambda _: True` | 
| Forest Chunky Face Room | Face Puzzle: Near Puzzle |  | `self.logic = lambda _: True` | 
| Forest Mill Back | Mill Back: Near Thatch |  | `self.logic = lambda _: True` | 
| Forest Spider | Spider: Opposite Entrance |  | `self.logic = lambda _: True` | 

# Crystal Caves
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Caves Rotating Cabin | Rotating cabin: wall |  | `l.Slam and l.isdonkey` | 
| Crystal Caves | Giant Kosha Room |  | `self.logic = lambda _: True` | 
| Crystal Caves | In Monkeyport igloo |  | `((Events.CavesMonkeyportAccess in l.Events or l.CanPhaseswim()))` | 
| Crystal Caves | In breakable igloo |  | `Events.CavesLargeBoulderButton in l.Events or l.CanPhaseswim() or l.generalclips` | 
| Crystal Caves | On igloo Pillar | MelonCrate | `(l.jetpack and l.isdiddy) or (l.twirl and l.istiny and (not l.isKrushaAdjacent(Kongs.tiny)))` | 
| Crystal Caves | On top of the Igloo | CrownPad, MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves | Under tag barrel near igloo | MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves | In front of Igloo | CrownPad, DirtPatch, Bananaport | `(l.HasGun(Kongs.any) and ((l.istiny and l.isKrushaAdjacent(Kongs.tiny)) or (not l.istiny))) or l.Slam` | 
| Crystal Caves | In the mini cave |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near ice wall to boulder |  | `self.logic = lambda _: True` | 
| Crystal Caves | In Giant Boulder Room |  | `self.logic = lambda _: True` | 
| Crystal Caves | In front of Cranky | MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves | Below Ice Castle (yellow) |  | `self.logic = lambda _: True` | 
| Crystal Caves | Below Ice castle (blue) |  | `self.logic = lambda _: True` | 
| Crystal Caves | Ice Castle Tag barrel |  | `self.logic = lambda _: True` | 
| Crystal Caves | Next to Ice Castle |  | `self.logic = lambda _: True` | 
| Crystal Caves | On Ice Castle |  | `(l.balloon and l.islanky) or (l.jetpack and l.isdiddy) or l.monkey_maneuvers` | 
| Crystal Caves | Near Small Boulder |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near ice wall to shop |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near cave shop |  | `self.logic = lambda _: True` | 
| Crystal Caves | Under Small Boulder | DirtPatch, MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves | Near ice wall to Gone room |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Gorilla Gone Room |  | `self.logic = lambda _: True` | 
| Crystal Caves | In Gorilla Gone Room |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Kasplat Spire |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Funky's |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Funky under Rocketbarrel |  | `self.logic = lambda _: True` | 
| Crystal Caves | Mini Monkeyport cave |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near headphones |  | `self.logic = lambda _: True` | 
| Crystal Caves | Headphones ledge |  | `self.logic = lambda _: True` | 
| Crystal Caves | Next to Lanky cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Left of rotating cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Next to rotating cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Right of rotating cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Kasplat Pillar | MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves | Near cabins Rocketbarrel |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Tiny cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near cabins Tag barrel |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Diddy Upper cabin |  | `self.logic = lambda _: True` | 
| Crystal Caves | Near Diddy upper Cabin door |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Close Warp 1 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Close Warp 2 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Igloo Warp 1 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Cabins Warp 2 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Pillar Warp 5 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Hidden Warp 3 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Igloo Warp 3 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Hidden Warp 4 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Spire Warp 4 |  | `self.logic = lambda _: True` | 
| Crystal Caves | Vanilla Cabin Warp 5 |  | `self.logic = lambda _: True` | 
| Caves Diddy Igloo | Diddy igloo: Center | CrownPad | `self.logic = lambda _: True` | 
| Caves Donkey Igloo | DK igloo: Behind Maze |  | `self.logic = lambda _: True` | 
| Caves Lanky Igloo | Lanky igloo: High Platform |  | `((l.balloon or l.monkey_maneuvers) and l.islanky) or (l.monkey_maneuvers and (l.isdiddy or l.istiny))` | 
| Caves Tiny Igloo | Tiny igloo: Opposite Entrance |  | `self.logic = lambda _: True` | 
| Caves Lanky Cabin | Lanky cabin: Carpet |  | `self.logic = lambda _: True` | 
| Caves Chunky Cabin | Chunky cabin: Back Left Corner | CrownPad | `self.logic = lambda _: True` | 
| Caves Diddy Upper Cabin | Diddy Upper cabin: Right |  | `self.logic = lambda _: True` | 
| Caves Donkey Cabin | Donkey cabin: Opposite Entrance |  | `self.logic = lambda _: True` | 
| Caves Frozen Castle | Ice Castle: Left of puzzle |  | `self.logic = lambda _: True` | 
| Caves Frozen Castle | Ice Castle: Right of puzzle |  | `self.logic = lambda _: True` | 
| Caves Tiny Cabin | Tiny Cabin: Interior |  | `l.oranges` | 

# Creepy Castle
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Castle Greenhouse | Greenhouse: Center | DirtPatch | `l.islanky or l.settings.free_trade_items` | 
| Creepy Castle | Top of Castle near shop |  | `self.logic = lambda _: True` | 
| Castle Greenhouse | Greenhouse: GB area | DirtPatch | `self.logic = lambda _: True` | 
| Creepy Castle | Near the Tree |  | `self.logic = lambda _: True` | 
| Creepy Castle | Next to lowest tree |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near lower entrance - right |  | `self.logic = lambda _: True` | 
| Creepy Castle | Lowest ledge near ladder |  | `self.logic = lambda _: True` | 
| Creepy Castle | Graveyard behind stone |  | `self.logic = lambda _: True` | 
| Creepy Castle | Lowest ledge towards Tiny Kasplat |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near the lower door |  | `self.logic = lambda _: True` | 
| Creepy Castle | Upper Gravestone |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Dungeon Tunnel Steps |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Dungeon Tunnel |  | `self.logic = lambda _: True` | 
| Creepy Castle | On square stone |  | `self.logic = lambda _: True` | 
| Creepy Castle | Next to the drawbridge |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Lower Rocketbarrel |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Lower Tag Barrel |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Headphones |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Drawbridge Exit |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near middle shop |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Shed |  | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Greenhouse |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near Wind Tower |  | `self.logic = lambda _: True` | 
| Creepy Castle | Top of Castle near fence |  | `self.logic = lambda _: True` | 
| Creepy Castle | Near top shop |  | `self.logic = lambda _: True` | 
| Creepy Castle | On Wind Tower |  | `l.jetpack and l.isdiddy` | 
| Creepy Castle | Vanilla Overhang Warp 2 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Top Warp 5 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Moat Warp 1 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Moat Warp 5 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Back Warp 1 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Moat Warp 3 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Moat Warp 2 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Moat Warp 4 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Shop Warp 3 |  | `self.logic = lambda _: True` | 
| Creepy Castle | Vanilla Shed Warp 4 |  | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom: Near Left Candle |  | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom: Near Right Candle |  | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom: Back Left |  | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom: Back Right |  | `self.logic = lambda _: True` | 
| Castle Dungeon | Dungeon: Near Diddy Room |  | `self.logic = lambda _: True` | 
| Castle Dungeon | Dungeon: Donkey Room |  | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.donkey) or l.CanPhase()` | 
| Castle Dungeon | Dungeon: Behind punch gate |  | `((l.punch and l.ischunky) or l.CanPhase())` | 
| Castle Shed | Shed: Near Entrance |  | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower cave: Lower Portion |  | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower cave: Also Behind Mausoleum |  | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower cave: Near shop |  | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower cave: Behind Mausoleum |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: entrance |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Near Chunky Coffin |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Near Diddy Coffin |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Far Warp 1 |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Close Warp 1 |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Close Warp 2 |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Close Warp 3 |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Far Warp 3 |  | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt: Vanilla Far Warp 2 |  | `self.logic = lambda _: True` | 
| Castle Mausoleum | Mausoleum: entrance |  | `self.logic = lambda _: True` | 
| Castle Mausoleum | Mausoleum: Lanky Tunnel |  | `self.logic = lambda _: True` | 
| Castle Upper Cave | Upper cave: Near Pit |  | `self.logic = lambda _: True` | 
| Castle Upper Cave | Upper cave: Near shop |  | `self.logic = lambda _: True` | 
| Castle Library | Library: Enemy Gauntlet Room | CrownPad | `self.logic = lambda _: True` | 
| Castle Library | Library: Flying Book Room |  | `self.logic = lambda _: True` | 
| Castle Museum | Museum: Near Race |  | `self.logic = lambda _: True` | 
| Castle Museum | Museum: Pillar Front |  | `((l.monkeyport and l.istiny) or l.CanPhase())` | 
| Castle Museum | Museum: Pillar Back Right |  | `((l.monkeyport and l.istiny) or l.CanPhase())` | 
| Castle Museum | Museum: Behind Pillar |  | `(l.monkeyport and l.istiny) or l.CanPhase()` | 
| Castle Museum | Museum: Pillar Back Left |  | `((l.monkeyport and l.istiny) or l.CanPhase())` | 
| Castle Museum | Museum: Main Room |  | `self.logic = lambda _: True` | 
| Castle Trash Can | Trash Can: Near Cheese |  | `self.logic = lambda _: True` | 
| Castle Tree | Tree: Starting Room |  | `self.logic = lambda _: True` | 

# DK Isles
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Isles Snide Room | Snide's Room: Under Rock |  | `l.chunky and l.barrels` | 
| Fungi Forest Lobby | Fungi Lobby: Gorilla Gone Box |  | `l.CanOpenForestLobbyGoneDoor() and l.chunky and l.gorillaGone` | 
| Isles | Front of Fungi Building |  | `self.logic = lambda _: True` | 
| Isles | On Aztec Building |  | `self.logic = lambda _: True` | 
| Isles | Under Caves Lobby Entrance |  | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby: Center |  | `((l.chunky and l.balloon and l.islanky and l.barrels) or l.CanMoonkick() or (l.monkey_maneuvers and l.istiny and l.twirl and (not l.isKrushaAdjacent(Kongs.tiny))))` | 
| Training Grounds | Training Grounds: Banana Hoard |  | `(l.can_use_vines or l.CanMoonkick()) and l.climbing` | 
| Training Grounds | Training Grounds: Rear Tunnel |  | `self.logic = lambda _: True` | 
| KLumsy | Prison: Back |  | `self.logic = lambda _: True` | 
| Isles | Behind Fungi Building |  | `self.logic = lambda _: True` | 
| Isles | Fungi floating island |  | `self.logic = lambda _: True` | 
| Isles | Waterfall Platform |  | `self.logic = lambda _: True` | 
| Isles | Down Near Caves Lobby Tree |  | `self.logic = lambda _: True` | 
| Isles | Near K. Rool |  | `self.logic = lambda _: True` | 
| Isles | Near Fungi Cannon |  | `self.logic = lambda _: True` | 
| Isles | In Fungi cannon rock |  | `(l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events or l.CanPhase())` | 
| Isles | Next to Caves Lobby Tree |  | `self.logic = lambda _: True` | 
| Isles | Isles Boulders |  | `self.logic = lambda _: True` | 
| Isles | Front of Aztec Building |  | `self.logic = lambda _: True` | 
| Isles | Behind Aztec Building |  | `self.logic = lambda _: True` | 
| Isles | Outside K. Lumsy |  | `self.logic = lambda _: True` | 
| Isles | Near Monkeyport pad |  | `self.logic = lambda _: True` | 
| Isles | Back of Krem Isle |  | `self.logic = lambda _: True` | 
| Isles | Under DK Caged GB |  | `self.logic = lambda _: True` | 
| Isles | Back of Krem Isle (Lower) |  | `self.logic = lambda _: True` | 
| Isles | Behind Factory Lobby Entrance |  | `self.logic = lambda _: True` | 
| Isles | Right of Factory Lobby Entrance |  | `self.logic = lambda _: True` | 
| Isles | Behind Helm Lobby Entrance |  | `self.logic = lambda _: True` | 
| Isles | Left Krem Isle Arm (side) |  | `self.logic = lambda _: True` | 
| Isles | Left Krem Isle Arm |  | `self.logic = lambda _: True` | 
| Isles | Right Krem Isle Arm |  | `self.logic = lambda _: True` | 
| Isles | Fairy Isle |  | `self.logic = lambda _: True` | 
| Isles | Behind Fairy Isle |  | `logic=lambda _: True` | 
| Isles | Small Island |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Ring Warp 1 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla K. Lumsy Warp 1 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Ring Warp 2 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Upper Warp 2 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Waterfall Warp 3 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Ring Warp 5 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Ring Warp 3 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Ring Warp 4 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Krem Warp 4 |  | `self.logic = lambda _: True` | 
| Isles | Vanilla Island Warp 5 |  | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby: Near Tag Barrel |  | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby: Near Portal |  | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby: Front of Door |  | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby: back room right |  | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Angry Aztec Lobby | Aztec Lobby: back room left |  | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Frantic Factory Lobby | Factory Lobby: Near Lever |  | `self.logic = lambda _: True` | 
| Frantic Factory Lobby | Factory Lobby: High Platform |  | `((l.grab and l.isdonkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Frantic Factory Lobby | Factory Lobby: Above Portal |  | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Gloomy Galleon Lobby | Galleon Lobby: Right of Portal |  | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby: Left of Portal |  | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby: Mini room | CrownPad | `((l.mini and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.istiny and l.chunky and l.swim) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
| Fungi Forest Lobby | Forest Lobby: On Tag Crate | MelonCrate | `self.logic = lambda _: True` | 
| Crystal Caves Lobby | Caves Lobby: On the Lava | CrownPad | `((l.punch and l.strongKong and l.isdonkey) or l.CanPhase() or l.ledgeclip)` | 
| Crystal Caves Lobby | Caves Lobby: Right of Portal |  | `self.logic = lambda _: True` | 
| Crystal Caves Lobby | Caves Lobby: Diddy ledge |  | `(l.jetpack and l.isdiddy) or l.CanMoonkick()` | 
| Crystal Caves Lobby | Caves Lobby: boulder room |  | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Creepy Castle Lobby | Castle Lobby: Behind the entrance |  | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby: Right of Entrance |  | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby: Left of Portal |  | `self.logic = lambda _: True` | 
| Hideout Helm Lobby | Helm Lobby: Next to Tag Barrel |  | `self.logic = lambda _: True` | 
| Hideout Helm Lobby | Helm Lobby: Bonus Platform |  | `(l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone, False) and l.can_use_vines) or (l.monkey_maneuvers and l.istiny and l.twirl)` | 
| Hideout Helm Lobby | Helm Lobby: Kasplat island |  | `((l.coconut and l.scope) or (l.twirl and l.istiny and l.monkey_maneuvers))` | 
| Training Grounds | Training Grounds: Far Mountain |  | `l.climbing` | 
| Training Grounds | Training Grounds: On the rear hill |  | `l.climbing` | 
| Training Grounds | Training Grounds: On the entrance hill |  | `l.climbing and ((l.twirl and l.istiny) or (l.monkey_maneuvers and l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey))))` | 
| Training Grounds | Training Grounds: Near Mountain |  | `l.climbing and ((l.twirl and l.istiny) or (l.monkey_maneuvers and l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey))))` | 
| Training Grounds | Training Grounds: Rear Cave |  | `self.logic = lambda _: True` | 
| Training Grounds | Training Grounds: Banana Hoard (back) |  | `(l.can_use_vines or l.CanMoonkick()) and l.climbing` | 
| Training Grounds | Training Grounds: Underwater | CrownPad, DirtPatch | `l.HasGun(Kongs.any) and ((l.istiny and l.isKrushaAdjacent(Kongs.tiny)) or (not l.istiny)) and l.swim and l.scope` | 
| Training Grounds | Training Grounds: Near Pool |  | `self.logic = lambda _: True` | 
| Treehouse | Treehouse: back |  | `self.logic = lambda _: True` | 
| Banana Fairy Room | Banana Fairy Room: Right of Queen |  | `self.logic = lambda _: True` | 
| Banana Fairy Room | Banana Fairy Room: Behind Queen |  | `self.logic = lambda _: True` | 
| Banana Fairy Room | Banana Fairy Room: Behind Fairy Chair |  | `self.logic = lambda _: True` | 
| Banana Fairy Room | Banana Fairy Room: Rareware room |  | `self.logic = lambda _: True` | 
| Banana Fairy Room | Banana Fairy Room: Rareware Room right |  | `self.logic = lambda _: True` | 
| Isles Snide Room | Snide's Room: Next to Snide's |  | `self.logic = lambda _: True` | 
| KLumsy | Prison: Back Right |  | `self.logic = lambda _: True` | 
| KLumsy | Prison: Near Left |  | `self.logic = lambda _: True` | 
| KLumsy | Prison: Under K. Lumsy |  | `(l.IsKLumsyFree() or l.CanPhase())` | 

# Hideout Helm
| Map | Name | Banned Types | Logic |
| --- | ---- | ------------ | ----- |
| Hideout Helm | Metal grate by Mini Monkey barrel | MelonCrate | `self.logic = lambda _: True` | 
| Hideout Helm | Mini Monkey room right side | MelonCrate | `self.logic = lambda _: True` | 
| Hideout Helm | Pineapple switch room in ammo alcove | MelonCrate | `self.logic = lambda _: True` | 
| Hideout Helm | First room left of Tag barrel | MelonCrate | `self.logic = lambda _: True` | 
| Hideout Helm | Top of Blast-o-Matic |  | `l.jetpack and l.isdiddy` | 
| Hideout Helm | Blast-o-Matic platform left side |  | `self.logic = lambda _: True` | 
| Hideout Helm | Blast-o-Matic platform right side |  | `self.logic = lambda _: True` | 
| Hideout Helm | Under K. Rool door |  | `self.logic = lambda _: True` | 
| Hideout Helm | Navigation room near terminals |  | `self.logic = lambda _: True` | 
| Hideout Helm | Navigation room near left window |  | `self.logic = lambda _: True` | 
| Hideout Helm | Navigation room near right window |  | `self.logic = lambda _: True` | 
| Hideout Helm | K. Rool room near kong faces |  | `self.logic = lambda _: True` | 
| Hideout Helm | K. Rool room in front of chair |  | `self.logic = lambda _: True` | 
