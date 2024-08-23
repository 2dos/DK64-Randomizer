
# Jungle Japes
| Map | Name | Logic |
| --- | ---- | ----- |
| Jungle Japes | Japes Kasplat: Behind Rambi Wall |  | 
| Jungle Japes | Japes Kasplat: Top of mountain |  | 
| Jungle Japes | Japes Kasplat: Beehive Area |  | 
| Jungle Japes | Japes Kasplat: Hive Tunnel Lower |  | 
| Jungle Japes | Japes Kasplat: Hive Tunnel Upper |  | 
| Japes Under Ground | Japes Kasplat: Underground | `(l.can_use_vines and l.pineapple and l.ischunky)` | 
| Jungle Japes | Japes Kasplat: By Lanky Slope Bonus |  | 
| Jungle Japes | Japes Kasplat: Near Painting Room |  | 
| Jungle Japes | Japes Kasplat: Inside Tiny's Cage | `((Events.JapesTinySwitch in l.Events or l.phasewalk or l.CanPhaseswim() or l.CanSkew(False)) and l.tiny)` | 
| Jungle Japes | Japes Kasplat: Starting Area |  | 
| Jungle Japes | Japes Kasplat: Diddy Peanut Cave |  | 
| Jungle Japes | Japes Kasplat: In the river | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Jungle Japes | Japes Kasplat: Rambi Water Pool | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Jungle Japes | Japes Kasplat: Near Cranky's |  | 
| Jungle Japes | Japes Kasplat: Hillside Alcove |  | 
| Japes Mountain | Japes Kasplat: Inside the Mountain |  | 
| Japes Tiny Hive | Japes Kasplat: Inside the Shell |  | 
| Jungle Japes | Japes Kasplat: Painting Room Hill | `(l.lanky and l.handstand) or (l.tiny and l.twirl) or l.CanMoonkick() or ((l.phasewalk or l.generalclips) and (l.istiny or l.isdiddy))` | 
| Jungle Japes | Japes Kasplat: Minecart Exit |  | 

# Angry Aztec
| Map | Name | Logic |
| --- | ---- | ----- |
| Angry Aztec | Aztec Kasplat: DK Quicksand Tunnel |  | 
| Angry Aztec | Aztec Kasplat: On the Oasis |  | 
| Angry Aztec | Aztec Kasplat: On Llama Cage | `((l.can_use_vines or (l.jetpack and l.isdiddy)) and l.climbing) or (l.advanced_platforming and (l.istiny or l.isdiddy)) or l.CanMoonkick()` | 
| Angry Aztec | Aztec Kasplat: Near giant boulder |  | 
| Angry Aztec | Aztec Kasplat: Behind DK Stone Door | `l.phasewalk or (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny)))` | 
| Aztec Llama Temple | Aztec Kasplat: Llama Temple Lava |  | 
| Angry Aztec | Aztec Kasplat: Hunky Chunky Barrel |  | 
| Angry Aztec | Aztec Kasplat: On Tiny Temple | `l.jetpack and l.isdiddy and l.climbing` | 
| Angry Aztec | Aztec Kasplat: In Vase Room | `(l.chunky and l.pineapple) or l.phasewalk` | 
| Angry Aztec | Aztec Kasplat: Behind 5-Door Temple |  | 
| Angry Aztec | Aztec Kasplat: Near Snide's |  | 
| Aztec Llama Temple | Aztec Kasplat: By the Llama in his Temple |  | 
| Aztec Tiny Temple | Aztec Kasplat: Free Tiny Room |  | 
| Aztec Chunky5DTemple | Aztec Kasplat: Chunky 5-Door Temple | `(l.pineapple and l.ischunky) or l.phasewalk` | 
| Angry Aztec | Aztec Kasplat: Behind the Beetle Race |  | 
| Aztec Llama Temple | Aztec Kasplat: Lanky Matching Game | `l.grape or l.phasewalk` | 
| Aztec Tiny Temple | Aztec Kasplat: Tiny Temple Mini Monkey |  | 
| Aztec Donkey5DTemple | Aztec Kasplat: Donkey 5-Door Temple | `(l.coconut or l.phasewalk) and l.isdonkey` | 

# Frantic Factory
| Map | Name | Logic |
| --- | ---- | ----- |
| Frantic Factory | Factory Kasplat: Starting Area |  | 
| Frantic Factory | Factory Kasplat: Near Power Hut |  | 
| Frantic Factory | Factory Kasplat: Down the Hatch Pole |  | 
| Frantic Factory | Factory Kasplat: Dark Room | `(l.punch and l.chunky) or l.phasewalk` | 
| Frantic Factory | Factory Kasplat: Lowest Production Platform |  | 
| Frantic Factory | Factory Kasplat: Upper Production Pipe |  | 
| Frantic Factory | Factory Kasplat: Base of Production |  | 
| Frantic Factory | Factory Kasplat: Research and Development |  | 
| Frantic Factory | Factory Kasplat: Pole to Arcade |  | 
| Frantic Factory | Factory Kasplat: Block Tower |  | 
| Frantic Factory | Factory Kasplat: Near Snide's |  | 
| Factory Power Hut | Factory Kasplat: Power Hut |  | 
| Frantic Factory | Factory Kasplat: By Car Race |  | 
| Frantic Factory | Factory Kasplat: Tiny Shooting Game | `l.mini or l.phasewalk` | 
| Factory Crusher | Factory Kasplat: Crusher Room |  | 
| Frantic Factory | Factory Kasplat: Upper Production Twirl | `l.twirl` | 
| Frantic Factory | Factory Kasplat: Lanky Piano Game | `l.trombone or l.CanAccessRNDRoom()` | 

# Gloomy Galleon
| Map | Name | Logic |
| --- | ---- | ----- |
| Gloomy Galleon | Galleon Kasplat: Lighthouse Platform |  | 
| Gloomy Galleon | Galleon Kasplat: Diddy Gold Tower |  | 
| Gloomy Galleon | Galleon Kasplat: Lighthouse Alcove |  | 
| Gloomy Galleon | Galleon Kasplat: Cannon Game Room | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Galleon Kasplat: Past Vines |  | 
| Gloomy Galleon | Galleon Kasplat: Musical Cactus |  | 
| Gloomy Galleon | Galleon Kasplat: On the Crown Pad | `(l.punch and l.chunky) or l.phasewalk or l.CanSkew(False)` | 
| Gloomy Galleon | Galleon Kasplat: Next to Cranky's |  | 
| Galleon Lighthouse | Galleon Kasplat: Atop Whomp's Lighthouse | `l.climbing` | 
| Galleon Mechafish | Galleon Kasplat: In the Mechfish |  | 
| Gloomy Galleon | Galleon Kasplat: Lanky Gold Tower | `(Events.WaterRaised in l.Events or (Events.ShipyardEnguarde in l.Events and Events.ShipyardTreasureRoomOpened in l.Events and l.advanced_platforming))` | 
| Galleon Sick Bay | Galleon Kasplat: Sickbay |  | 
| Gloomy Galleon | Galleon Kasplat: Middle Deck of Shipwreck |  | 
| Gloomy Galleon | Galleon Kasplat: Starting Area |  | 
| Gloomy Galleon | Galleon Kasplat: Inside Punchable Chest | `l.punch and l.chunky` | 
| Gloomy Galleon | Galleon Kasplat: Also Musical Cactus |  | 

# Fungi Forest
| Map | Name | Logic |
| --- | ---- | ----- |
| Fungi Forest | Forest Kasplat: Behind Diddy Barn |  | 
| Fungi Forest | Forest Kasplat: Behind beanstalk |  | 
| Fungi Forest | Forest Kasplat: By Giant Mushroom Rocketbarrel |  | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Top Floor |  | 
| Fungi Forest | Forest Kasplat: Near the Rabbit |  | 
| Fungi Forest | Forest Kasplat: Owl Tree Troff |  | 
| Fungi Forest | Forest Kasplat: Behind DK's Barn |  | 
| Forest Giant Mushroom | Forest Kasplat: Inside Giant Mushroom |  | 
| Fungi Forest | Forest Kasplat: Under Owl Tree |  | 
| Fungi Forest | Forest Kasplat: Low Mushroom Exterior |  | 
| Fungi Forest | Forest Kasplat: Mushroom Night Door |  | 
| Fungi Forest | Forest Kasplat: Behind Cuckoo Clock |  | 
| Forest Mill Front | Forest Kasplat: Grinder Room |  | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Moat | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Peak | `l.jetpack or l.handstand` | 
| Fungi Forest | Forest Kasplat: On Mill Roof |  | 
| Fungi Forest | Forest Kasplat: Minecart Exit Well |  | 
| Forest Lanky Mushrooms Room | Forest Kasplat: Lanky Mushroom Slam Room |  | 
| Forest Spider | Forest Kasplat: Spider Boss |  | 
| Forest Winch Room | Forest Kasplat: Winch Room |  | 
| Forest Chunky Face Room | Forest Kasplat: Face Shooting Room |  | 

# Crystal Caves
| Map | Name | Logic |
| --- | ---- | ----- |
| Crystal Caves | Caves Kasplat: Near Snide's |  | 
| Crystal Caves | Caves Kasplat: Bonus Barrel Cave |  | 
| Crystal Caves | Caves Kasplat: Inside Ice Shield | `Events.CavesLargeBoulderButton in l.Events or (l.generalclips and l.ischunky)` | 
| Crystal Caves | Caves Kasplat: On 5-Door Cabin |  | 
| Crystal Caves | Caves Kasplat: Across river from Candy |  | 
| Crystal Caves | Caves Kasplat: Giant Boulder Room |  | 
| Crystal Caves | Caves Kasplat: Near Ice Castle |  | 
| Crystal Caves | Caves Kasplat: Mini Room by Funky |  | 
| Crystal Caves | Caves Kasplat: On the Pillar |  | 
| Crystal Caves | Caves Kasplat: By the Far Warp 2 |  | 
| Crystal Caves | Caves Kasplat: On 5-Door Igloo |  | 
| Crystal Caves | Caves Kasplat: Water by Blast Pad |  | 
| Crystal Caves | Caves Kasplat: Tied to the Bananaport Spire |  | 
| Crystal Caves | Caves Kasplat: Between Funky and Castle |  | 
| Caves Lanky Race | Caves Kasplat: In the Beetle Race |  | 
| Crystal Caves | Caves Kasplat: With the Giant Kosha |  | 
| Caves Diddy Igloo | Caves Kasplat: In Diddy Igloo |  | 
| Caves Donkey Cabin | Caves Kasplat: DK Shooting Cabin |  | 
| Crystal Caves | Caves Kasplat: Gorilla Gone Cave | `(l.punch and l.chunky) or l.phasewalk or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)` | 
| Crystal Caves | Caves Kasplat: Starting Area |  | 

# Creepy Castle
| Map | Name | Logic |
| --- | ---- | ----- |
| Castle Lower Cave | Castle Kasplat: Behind the Mausoleum |  | 
| Castle Dungeon | Castle Kasplat: Dungeon Center |  | 
| Creepy Castle | Castle Kasplat: Back of Castle Troff |  | 
| Castle Ballroom | Castle Kasplat: Ballroom |  | 
| Creepy Castle | Castle Kasplat: Castle Top Level |  | 
| Castle Tree | Castle Kasplat: Inside the Tree | `(l.coconut or l.phasewalk or l.generalclips) and l.isdonkey` | 
| Castle Lower Cave | Castle Kasplat: Lower Cave Center |  | 
| Creepy Castle | Castle Kasplat: Near Upper Warp 2 |  | 
| Creepy Castle | Castle Kasplat: On a lone platform |  | 
| Castle Upper Cave | Castle Kasplat: Near Candy's |  | 
| Creepy Castle | Castle Kasplat: Tree Pond | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Creepy Castle | Castle Kasplat: Near Cranky's Hut |  | 
| Creepy Castle | Castle Kasplat: Lower Rocketbarrel |  | 
| Castle Greenhouse | Castle Kasplat: Greenhouse |  | 
| Castle Museum | Castle Kasplat: Museum Mysterious Pedestal | `l.monkeyport or l.phasewalk` | 
| Castle Dungeon | Castle Kasplat: Caged in the Dungeon | `l.punch or l.phasewalk` | 
| Castle Crypt | Castle Kasplat: Entrance to Minecart | `l.coconut or l.phasewalk or l.generalclips or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)` | 
| Castle Library | Castle Kasplat: Library |  | 
| Creepy Castle | Castle Kasplat: In the Clouds | `l.jetpack` | 

# DK Isles
| Map | Name | Logic |
| --- | ---- | ----- |
| Isles | Isles Kasplat: Beaver Beach |  | 
| Frantic Factory Lobby | Isles Kasplat: Factory Lobby above Portal | `(l.grab and l.donkey) or l.CanMoonkick() or (l.advanced_platforming and (l.istiny or l.isdiddy))` | 
| Hideout Helm Lobby | Isles Kasplat: Helm Lobby | `(l.scope and l.coconut) or (l.twirl and l.tiny and l.advanced_platforming)` | 
| Creepy Castle Lobby | Isles Kasplat: Castle Lobby | `(l.coconut and l.donkey) or l.phasewalk` | 
| Crystal Caves Lobby | Isles Kasplat: Caves Lobby Punch | `(l.punch and l.chunky) or l.phasewalk or l.ledgeclip` | 
| Frantic Factory Lobby | Isles Kasplat: Factory Lobby Box | `l.punch and l.chunky` | 
| Gloomy Galleon Lobby | Isles Kasplat: Galleon Lobby |  | 
| Isles | Isles Kasplat: Inside Big Rock | `Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky` | 
| Isles | Isles Kasplat: Back of Kroc Isle Middle |  | 
| Isles | Isles Kasplat: Big X Platform |  | 
| Isles | Isles Kasplat: Back of Cabin Isle |  | 
| Crystal Caves Lobby | Isles Kasplat: Caves Lobby Platform | `l.jetpack` | 
| Angry Aztec Lobby | Isles Kasplat: Aztec Lobby Feather Gate | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.phasewalk` | 
| KLumsy | Isles Kasplat: Prison Sprint Cage | `(l.sprint and l.lanky) or l.phasewalk` | 
| Jungle Japes Lobby | Isles Kasplat: Japes Lobby |  | 
| Isles | Isles Kasplat: Upper Monkeyport |  | 
| Isles Snide Room | Isles Kasplat: Near Snide's |  | 
| Isles | Isles Kasplat: Aztec Lobby Roof |  | 
| Isles | Isles Kasplat: Waterfall Pool | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
