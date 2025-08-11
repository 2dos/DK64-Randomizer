
# Jungle Japes
| Map | Name | Logic |
| --- | ---- | ----- |
| Jungle Japes | Japes Kasplat: Behind Rambi Wall | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Top of mountain | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Beehive Area | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Hive Tunnel Lower | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Hive Tunnel Upper | `self.additional_logic = lambda _: True` | 
| Japes Under Ground | Japes Kasplat: Underground | `(l.can_use_vines and l.pineapple and l.ischunky)` | 
| Jungle Japes | Japes Kasplat: By Lanky Slope Bonus | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Near Painting Room | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Inside Tiny's Cage | `((Events.JapesTinySwitch in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(False)) and l.tiny)` | 
| Jungle Japes | Japes Kasplat: Starting Area | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Diddy Peanut Cave | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: In the river | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Jungle Japes | Japes Kasplat: Rambi Water Pool | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Jungle Japes | Japes Kasplat: Near Cranky's | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Hillside Alcove | `self.additional_logic = lambda _: True` | 
| Japes Mountain | Japes Kasplat: Inside the Mountain | `self.additional_logic = lambda _: True` | 
| Japes Tiny Hive | Japes Kasplat: Inside the Shell | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Painting Room Hill | `self.additional_logic = lambda _: True` | 
| Jungle Japes | Japes Kasplat: Minecart Exit | `self.additional_logic = lambda _: True` | 

# Angry Aztec
| Map | Name | Logic |
| --- | ---- | ----- |
| Angry Aztec | Aztec Kasplat: DK Quicksand Tunnel | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: On the Oasis | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: On Llama Cage | `((l.can_use_vines or (l.jetpack and l.isdiddy)) and l.climbing) or (l.monkey_maneuvers and (l.istiny or l.isdiddy)) or l.CanMoonkick()` | 
| Angry Aztec | Aztec Kasplat: Near giant boulder | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: Behind DK Stone Door | `l.CanPhase() or (l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny)))` | 
| Aztec Llama Temple | Aztec Kasplat: Llama Temple Lava | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: Hunky Chunky Barrel | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: On Tiny Temple | `l.jetpack and l.isdiddy and l.climbing` | 
| Angry Aztec | Aztec Kasplat: In Vase Room | `(l.chunky and l.pineapple) or l.CanPhase()` | 
| Angry Aztec | Aztec Kasplat: Behind 5-Door Temple | `self.additional_logic = lambda _: True` | 
| Angry Aztec | Aztec Kasplat: Near Snide's | `self.additional_logic = lambda _: True` | 
| Aztec Llama Temple | Aztec Kasplat: By the Llama in his Temple | `self.additional_logic = lambda _: True` | 
| Aztec Tiny Temple | Aztec Kasplat: Free Tiny Room | `self.additional_logic = lambda _: True` | 
| Aztec Chunky5DTemple | Aztec Kasplat: Chunky 5-Door Temple | `(l.pineapple and l.ischunky) or l.CanPhase()` | 
| Angry Aztec | Aztec Kasplat: Behind the Beetle Race | `self.additional_logic = lambda _: True` | 
| Aztec Llama Temple | Aztec Kasplat: Lanky Matching Game | `self.additional_logic = lambda _: True` | 
| Aztec Tiny Temple | Aztec Kasplat: Tiny Temple Mini Monkey | `self.additional_logic = lambda _: True` | 
| Aztec Donkey5DTemple | Aztec Kasplat: Donkey 5-Door Temple | `(l.coconut or l.CanPhase()) and l.isdonkey` | 

# Frantic Factory
| Map | Name | Logic |
| --- | ---- | ----- |
| Frantic Factory | Factory Kasplat: Starting Area | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Near Power Hut | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Down the Hatch Pole | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Dark Room | `(l.punch and l.chunky) or l.CanPhase()` | 
| Frantic Factory | Factory Kasplat: Lowest Production Platform | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Upper Production Pipe | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Base of Production | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: R&D | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Pole to Arcade | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Block Tower | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Near Snide's | `self.additional_logic = lambda _: True` | 
| Factory Power Hut | Factory Kasplat: Power Hut | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: By Car Race | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Tiny Shooting Game | `l.mini or l.CanPhase()` | 
| Factory Crusher | Factory Kasplat: Crusher Room | `self.additional_logic = lambda _: True` | 
| Frantic Factory | Factory Kasplat: Upper Production Twirl | `l.twirl` | 
| Frantic Factory | Factory Kasplat: Lanky Piano Game | `l.trombone or l.CanAccessRNDRoom()` | 

# Gloomy Galleon
| Map | Name | Logic |
| --- | ---- | ----- |
| Gloomy Galleon | Galleon Kasplat: Lighthouse Platform | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Diddy Gold Tower | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Lighthouse Alcove | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Cannon Game Room | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Galleon Kasplat: Past Vines | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Musical Cactus | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: On the Crown Pad | `(l.punch and l.chunky) or l.CanPhase() or l.CanSkew(False, False)` | 
| Gloomy Galleon | Galleon Kasplat: Next to Cranky's | `self.additional_logic = lambda _: True` | 
| Galleon Lighthouse | Galleon Kasplat: Atop Whomp's Lighthouse | `self.additional_logic = lambda _: True` | 
| Galleon Mechafish | Galleon Kasplat: In the Mechfish | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Lanky Gold Tower | `(Events.WaterRaised in l.Events or (Events.ShipyardEnguarde in l.Events and Events.ShipyardTreasureRoomOpened in l.Events and l.monkey_maneuvers)) and l.balloon` | 
| Galleon Sick Bay | Galleon Kasplat: Sickbay | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Middle Deck of Shipwreck | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Starting Area | `self.additional_logic = lambda _: True` | 
| Gloomy Galleon | Galleon Kasplat: Inside Punchable Chest | `l.punch and l.chunky` | 
| Gloomy Galleon | Galleon Kasplat: Also Musical Cactus | `self.additional_logic = lambda _: True` | 

# Fungi Forest
| Map | Name | Logic |
| --- | ---- | ----- |
| Fungi Forest | Forest Kasplat: Behind Diddy Barn | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Behind beanstalk | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: By Giant Mushroom Rocketbarrel | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Top Floor | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Near the Rabbit | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Owl Tree Troff | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Behind DK's Barn | `self.additional_logic = lambda _: True` | 
| Forest Giant Mushroom | Forest Kasplat: Inside Giant Mushroom | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Under Owl Tree | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Low Mushroom Exterior | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Mushroom Night Door | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Behind Cuckoo Clock | `self.additional_logic = lambda _: True` | 
| Forest Mill Front | Forest Kasplat: Grinder Room | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Moat | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Fungi Forest | Forest Kasplat: Giant Mushroom Peak | `l.jetpack or l.handstand` | 
| Fungi Forest | Forest Kasplat: On Mill Roof | `self.additional_logic = lambda _: True` | 
| Fungi Forest | Forest Kasplat: Minecart Exit Well | `self.additional_logic = lambda _: True` | 
| Forest Lanky Mushrooms Room | Forest Kasplat: Lanky Mushroom Slam Room | `self.additional_logic = lambda _: True` | 
| Forest Spider | Forest Kasplat: Spider Boss | `self.additional_logic = lambda _: True` | 
| Forest Winch Room | Forest Kasplat: Winch Room | `self.additional_logic = lambda _: True` | 
| Forest Chunky Face Room | Forest Kasplat: Face Shooting Room | `self.additional_logic = lambda _: True` | 

# Crystal Caves
| Map | Name | Logic |
| --- | ---- | ----- |
| Crystal Caves | Caves Kasplat: Near Snide's | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Bonus Barrel Cave | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Inside Ice Shield | `Events.CavesLargeBoulderButton in l.Events or (l.generalclips and l.ischunky)` | 
| Crystal Caves | Caves Kasplat: On 5-Door Cabin | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Across river from Candy | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Giant Boulder Room | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Near Ice Castle | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Mini Room by Funky | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: On the Pillar | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: By the Far Warp 2 | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: On 5-Door Igloo | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Water by Blast Pad | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Tied to the Bananaport Spire | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Between Funky and Castle | `self.additional_logic = lambda _: True` | 
| Caves Lanky Race | Caves Kasplat: In the Beetle Race | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: With the Giant Kosha | `self.additional_logic = lambda _: True` | 
| Caves Diddy Igloo | Caves Kasplat: In Diddy Igloo | `self.additional_logic = lambda _: True` | 
| Caves Donkey Cabin | Caves Kasplat: DK Shooting Cabin | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Gorilla Gone Cave | `self.additional_logic = lambda _: True` | 
| Crystal Caves | Caves Kasplat: Starting Area | `self.additional_logic = lambda _: True` | 

# Creepy Castle
| Map | Name | Logic |
| --- | ---- | ----- |
| Castle Lower Cave | Castle Kasplat: Behind the Mausoleum | `self.additional_logic = lambda _: True` | 
| Castle Dungeon | Castle Kasplat: Dungeon Center | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: Back of Castle Troff | `self.additional_logic = lambda _: True` | 
| Castle Ballroom | Castle Kasplat: Ballroom | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: Castle Top Level | `self.additional_logic = lambda _: True` | 
| Castle Tree | Castle Kasplat: Inside the Tree | `(l.coconut or l.CanPhase() or l.generalclips) and l.isdonkey` | 
| Castle Lower Cave | Castle Kasplat: Lower Cave Center | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: Near Upper Warp 2 | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: On a lone platform | `self.additional_logic = lambda _: True` | 
| Castle Upper Cave | Castle Kasplat: Near Candy's | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: Tree Pond | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
| Creepy Castle | Castle Kasplat: Near Cranky's Hut | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: Lower Rocketbarrel | `self.additional_logic = lambda _: True` | 
| Castle Greenhouse | Castle Kasplat: Greenhouse | `self.additional_logic = lambda _: True` | 
| Castle Museum | Castle Kasplat: Museum Mysterious Pedestal | `l.monkeyport or l.CanPhase()` | 
| Castle Dungeon | Castle Kasplat: Caged in the Dungeon | `l.punch or l.CanPhase()` | 
| Castle Crypt | Castle Kasplat: Entrance to Minecart | `self.additional_logic = lambda _: True` | 
| Castle Library | Castle Kasplat: Library | `self.additional_logic = lambda _: True` | 
| Creepy Castle | Castle Kasplat: In the Clouds | `l.jetpack` | 

# DK Isles
| Map | Name | Logic |
| --- | ---- | ----- |
| Isles | Isles Kasplat: Beaver Beach | `self.additional_logic = lambda _: True` | 
| Frantic Factory Lobby | Isles Kasplat: Factory Lobby above Portal | `(l.grab and l.donkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.istiny or l.isdiddy))` | 
| Hideout Helm Lobby | Isles Kasplat: Helm Lobby | `(l.scope and l.coconut) or (l.twirl and l.tiny and l.monkey_maneuvers)` | 
| Creepy Castle Lobby | Isles Kasplat: Castle Lobby | `(l.coconut and l.donkey) or l.CanPhase()` | 
| Crystal Caves Lobby | Isles Kasplat: Caves Lobby Punch | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Frantic Factory Lobby | Isles Kasplat: Factory Lobby Box | `l.punch and l.chunky` | 
| Gloomy Galleon Lobby | Isles Kasplat: Galleon Lobby | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Inside Big Rock | `Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky` | 
| Isles | Isles Kasplat: Back of Kroc Isle Middle | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Big X Platform | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Back of Cabin Isle | `self.additional_logic = lambda _: True` | 
| Crystal Caves Lobby | Isles Kasplat: Caves Lobby Platform | `l.jetpack` | 
| Angry Aztec Lobby | Isles Kasplat: Aztec Lobby Feather Gate | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| KLumsy | Isles Kasplat: Prison Sprint Cage | `(l.sprint and l.lanky) or l.CanPhase()` | 
| Jungle Japes Lobby | Isles Kasplat: Japes Lobby | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Upper Monkeyport | `self.additional_logic = lambda _: True` | 
| Isles Snide Room | Isles Kasplat: Near Snide's | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Aztec Lobby Roof | `self.additional_logic = lambda _: True` | 
| Isles | Isles Kasplat: Waterfall Pool | `l.swim and (l.oranges or l.HasGun(Kongs.any) or l.HasInstrument(Kongs.any))` | 
