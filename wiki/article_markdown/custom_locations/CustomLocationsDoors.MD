
# Jungle Japes
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Jungle Japes Lobby | Japes Lobby - Middle Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Far Left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Close Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Far Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Close Left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel Cave | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Near Painting Room | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Rambi Boulder Cave | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Diddy Cage - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Alcove Above Stormy Tunnel - right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Alcove Above Stormy Tunnel - left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Minecart Exit - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Across From Minecart Exit | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Hive Tunnel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Hive Area - Next to Hive - far left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Hive Area - Next to Hive - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Rambi Pool - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Rambi Pool - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Top of Lanky Useless Slope - left | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Top of Lanky Useless Slope - right | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | River by Tag Barrel | Boss, Wrinkly | `l.swim` | 
| Jungle Japes | River by Chunky Underground | Boss, Wrinkly | `l.swim` | 
| Jungle Japes | Low Hill Shop - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Painting Hill - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Painting Hill - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel Switch - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel Switch - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel - back left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | First Tunnel - Near River Exit | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Tunnel - Near Pit River Side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Tunnel - River Side | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Tunnel Threeway crossing | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Tunnel - Crossroad | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - front right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - center left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - center right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - back left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Stormy Area - back right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Tiny Hive | Hive Room 2 - left | Wrinkly | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips` | 
| Japes Tiny Hive | Hive Room 2 - right | Wrinkly | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips` | 
| Japes Lanky Cave | Painting Room - Next to the Entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Mountain | Diddy Mountain - Next to Conveyor Controls | Wrinkly | `(l.charge and l.isdiddy) or l.CanPhase()` | 
| Japes Mountain | Diddy Mountain - between River and GB switch | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Japes Mountain | Diddy Mountain - between River and Peanut Switch | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Japes Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Mountain | Diddy Mountain - Next to the slam switch | Boss, Dk_Portal, Wrinkly | `l.peanut and l.isdiddy` | 
| Japes Mountain | Diddy Mountain - River grate 1 | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Mountain | Diddy Mountain - River grate 2 | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Mountain | Diddy Mountain - Minecart room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Lanky Cave | Painting room - Left of painting | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Lanky Cave | Painting room - Right of painting | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Under Ground | Chunky underground - left wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Under Ground | Chunky underground - right wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Under Ground | Chunky underground - Kasplat platform | Wrinkly | `l.can_use_vines and l.pineapple and l.ischunky` | 
| Jungle Japes | Next to the baboon blast pad | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Entrance door switch | Boss, Dk_Portal, Wrinkly | `l.can_use_vines and l.climbing` | 
| Jungle Japes | Next to level entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Against the mountain | Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 

# Angry Aztec
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Angry Aztec Lobby | Aztec Lobby - Pillar Wall | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby - Lower Right | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby - Left of Portal | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby - Right of Portal | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec Lobby | Aztec Lobby - Back Room | Wrinkly | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Angry Aztec | Near Quicksand Tunnel Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Tunnel Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Oasis Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Vulture Cage Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Behind 5DT | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Oasis Shop - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Under Tiny Temple Peanut Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Tiny Temple Pineapple Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Tiny Temple Feather Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Tiny Temple Grape Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Gong Tower Stairs - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tag Barrel near Vulture Cage | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Under the Vulture Cage | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5 Door Temple's 6th Door | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Hunky Barrel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Hunky Barrel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Snake Road - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Snake Road - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5 Door Temple Staircase - front | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5 Door Temple Staircase - back | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | First Tunnel - next to DK Door | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | First Tunnel - Near Oasis | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | In the sealed quicksand tunnel | Wrinkly | `l.isdonkey and l.strongKong` | 
| Angry Aztec | Far Back Triple Stairs Quicksand | Wrinkly | `l.isdonkey and l.strongKong` | 
| Aztec Llama Temple | Llama Temple Matching Room - right | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple Matching Room - left | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - back left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Oasis - Next to Tunnel - far left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Oasis - Next to Tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Far Back Triple Stairs Wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Llama Temple - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Llama Temple's switchless side | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Main Room - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Main Room - back | Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Across from KONG Room - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Across from KONG Room - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Next to Opening to Underwater Room | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Across from Opening to Underwater Room | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Llama Temple Stairs - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Llama Temple Stairs - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Entrance Staircase - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Entrance Staircase - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Across from the Spit Gate | Wrinkly | `Events.AztecLlamaSpit in l.Events and l.swim` | 
| Angry Aztec | Aztec Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Donkey5DTemple | Donkey 5DT - First right branch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Diddy5DTemple | Diddy 5DT - Second right branch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Lanky5DTemple | Lanky 5DT - Left side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Lanky5DTemple | Lanky 5DT - Right side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny5DTemple | Tiny 5DT - Left side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny5DTemple | Tiny 5DT - Second center tunnel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Chunky5DTemple | Chunky 5DT - Intersection | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Chunky5DTemple | Chunky 5DT - Left side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Down the stairs - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Down the stairs - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Near top stairs - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Near top stairs - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Center torch below entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Llama Temple | Llama Temple - Next to mini tunnel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Behind the guitar pad | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Little alcove above mini barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Next to triangle pad | Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Vulture room back wall | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Tiny room right wall | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Tiny room - on the K | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Behind the llama cage | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | In the quicksand near 5-door temple | Wrinkly | `l.strongKong and l.isdonkey` | 
| Angry Aztec | On top of llama temple | Wrinkly | `l.jetpack and l.diddy` | 
| Aztec Tiny Race | Behind the start of beetle race | Wrinkly | `self.logic = lambda _: True` | 

# Frantic Factory
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Frantic Factory Lobby | Factory Lobby - Low Left | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory Lobby | Factory Lobby - Top Left | Wrinkly | `(l.grab and l.donkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.istiny or l.isdiddy))` | 
| Frantic Factory Lobby | Factory Lobby - Top Center | Wrinkly | `(l.grab and l.donkey) or l.CanMoonkick() or l.monkey_maneuvers` | 
| Frantic Factory Lobby | Factory Lobby - Top Right | Wrinkly | `(l.grab and l.donkey) or l.CanMoonkick() or (l.monkey_maneuvers and (l.istiny or l.isdiddy))` | 
| Frantic Factory Lobby | Factory Lobby - Low Right | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Arcade Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Storage Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Behind Toy Monster Box | Wrinkly | `(l.ischunky and l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Next to Hatch - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Next to Hatch - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Bottom of the Hatch Pole | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room - Under Conveyors | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Storage Room - Behind Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Under Left Storage Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Under Right Storage Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Next to Number Game | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D - Next to Tunnel to Car Race | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Under Tunnel to Shop | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D - Dead End | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D - Blind Corner Next to Tunnel to Car Race | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Shop Room Left Wall | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Air Vent Under Arcade Window | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Under Arcade Window - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Behind Tag Barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D - Next to Diddy's Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D - Tiny's Race Entry Area | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Storage Room - Next to Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room - in Alcove Next to Tiny's Barrel | Wrinkly | `l.istiny and l.twirl` | 
| Frantic Factory | Production Room - Next to Diddy's Switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Arcade Room - Corner | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Next to Mini Barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Testing Area - Base of the Block Tower | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Foyer - Under Clock | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Frantic Factory | Foyer - front left | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Foyer - back left | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Foyer - front right | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Storage Room - Top of Orangstand Pipe | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Frantic Factory | Diddy R&D Room - front-right | Wrinkly | `(l.isdiddy and l.guitar) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Lanky Piano Room - right | Wrinkly | `(l.islanky and l.trombone) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Lanky Piano Room - left | Wrinkly | `(l.islanky and l.trombone) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Dark Room | Wrinkly, Boss | `(l.chunky and l.punch) or l.CanPhase() or l.generalclips` | 
| Factory Crusher | Crusher Room - start | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Factory Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Factory Power Hut | In the power hut | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 

# Gloomy Galleon
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Gloomy Galleon Lobby | Galleon Lobby - Far Left | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby - Far Right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby - Close Right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby - Near DK Portal | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon Lobby | Galleon Lobby - Close Left | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cavern Alcove Past Planks | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Deep Hole | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind 2DS | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind Enguarde Door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Tunnel to Shipyard - Tiny switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Tunnel to Shipyard - Lanky switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Tunnel to Punch Chests | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Under Baboon Blast pad | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Under RocketBarrel barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Cannonball game | Boss, Wrinkly | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Next to Lighthouse Gate switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Entrance Tunnel - near entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Shipyard Gate switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus - bottom back left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus - bottom front left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus - bottom back right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus - bottom front right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | On top of Seal cage | Wrinkly | `l.isdiddy and l.jetpack` | 
| Gloomy Galleon | Treasure Chest Exterior | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cavern Mast Top | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Punch Chests Room - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Punch Under Cavern Shop | Boss, Wrinkly | `(l.ischunky and l.punch) or l.CanPhase()` | 
| Gloomy Galleon | Low water alcove in lighthouse area | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind boxes near Cavern Wreck | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mechfish Gate - far left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mechfish Gate - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mechfish Gate - middle | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mechfish Gate - right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mechfish Gate - far right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cannonball Room Exit | Boss, Wrinkly | `l.swim` | 
| Gloomy Galleon | 2DS secret 3rd door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - Under Tag Barrel | Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Up the ledge | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Back | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mermaid Room | In Mermaid's Palace | Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip DKTiny | Tiny 5DS | Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip Diddy Lanky Chunky | Lanky 5DS | Wrinkly | `self.logic = lambda _: True` | 
| Galleon2DShip | Lanky 2DS | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Galleon Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cannonball gate tunnel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cannonball gate tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - start left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - start right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons front right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons center | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mechafish | Mechfish - Left wall | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mechafish | Mechfish - Right wall | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip Diddy Lanky Chunky | Chunky 5DS - Against a chest | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip DKTiny | Donkey 5DS - Next to the left cell bed | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | On top of the lighthouse | Wrinkly | `l.jetpack and l.isdiddy` | 

# Fungi Forest
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Fungi Forest Lobby | Forest Lobby - On High Box | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest Lobby | Forest Lobby - Near Gorilla Gone Door | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest Lobby | Forest Lobby - Opposite Gorilla Gone Door | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest Lobby | Forest Lobby - Near B. Locker | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest Lobby | Forest Lobby - Near Entrance | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Thornvine Barn | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Beanstalk Area Alcove | Boss, Wrinkly | `Events.Night in l.Events` | 
| Fungi Forest | Near Mills Shop | Boss, Wrinkly | `Events.Day in l.Events` | 
| Fungi Forest | Top of Giant Mushroom | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Owl Area Clearing | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | On top of Mill Crusher Output | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mill front side - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mill right side - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mill right side - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mill Roof - tower | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Boxes outside of Rafters Barn | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Night Thorns - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Behind Night Thorns - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Outside Thornvine Barn | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Rabbit's House | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Owl Area - Near Rocketbarrel Barrel - far left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Beanstalk Area - Behind Beanstalk right | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Tag Barrel near Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Rocketbarrel Barrel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Rocketbarrel Barrel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Center - Next to Pink Tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Center - Next to Pink Tunnel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Clock - left | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Clock - right | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Beanstalk Area - Behind Beanstalk left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Beanstalk Area - Behind Beanstalk | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom - All Kong Gun Switch - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom - All Kong Gun Switch - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom - halfway along the Dead End | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant Mushroom - Vine Mesh Wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Chunky Face Room | Chunky's Face Puzzle | Wrinkly | `self.logic = lambda _: True` | 
| Forest Lanky Zingers Room | Lanky's Zinger Bounce Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill - front side - Levers Area | Wrinkly | `(l.isdonkey and l.CanSlamSwitch(Levels.FungiForest, 2)) or l.CanPhase() or l.generalclips` | 
| Forest Mill Back | Mill - back side - Left Wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Winch Room | Winch Room - on the Winch | Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Attic | Lanky's Attic | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK's Barn - Between 2 Barrels near Switch | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Forest Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill - front side - Next to entrance | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill - front side - In the hay | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Front | Mill - front side - Above the switch crate | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Back | Mill - back side - In the hay | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Back | Mill - back side - Crates near spider entrance | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Giant mushroom - Top towards tag barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Night door in the owl tree | Boss, Wrinkly | `l.TimeAccess(Regions.HollowTreeArea, Time.Night) and l.jetpack and l.isdiddy` | 
| Forest Lanky Mushrooms Room | Lanky's colored mushrooms room | Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Thornvine Barn | DK's Barn - Second floor | Boss, Wrinkly | `self.logic = lambda _: True` | 

# Crystal Caves
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Crystal Caves Lobby | Caves Lobby - Far Left | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves Lobby | Caves Lobby - Top Ledge | Wrinkly | `(l.isdiddy and l.jetpack) or l.CanMoonkick()` | 
| Crystal Caves Lobby | Caves Lobby - Near Left | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves Lobby | Caves Lobby - Far Right | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves Lobby | Caves Lobby - Near Right | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | On Rotating Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Ice Cave Near Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Giant Boulder Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | On Lanky Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Near Igloo | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Lanky Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Chunky Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Diddy Lower Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Diddy Upper Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Under the Waterfall (Cabins Area) | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Cabins Useless Ledge | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Between DK and Diddy Igloos | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | Between Diddy and Tiny Igloos | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | Between Tiny and Chunky Igloos | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | Between Chunky and Lanky Igloos | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | Between Lanky and DK Igloos | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | Beneath Igloo bongo pad | Boss | `l.swim` | 
| Crystal Caves | Beneath Igloo guitar pad | Boss | `l.swim` | 
| Crystal Caves | Beneath Igloo saxophone pad | Boss | `l.swim` | 
| Crystal Caves | Beneath Igloo triangle pad | Boss | `l.swim` | 
| Crystal Caves | Beneath Igloo trombone pad | Boss | `l.swim` | 
| Crystal Caves | Near the small Boulder Switch | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Beneath Ice Castle - on land | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Beneath Ice Castle - underwater | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water under Blast pillar - right | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water under Blast pillar - left | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Under Bridge to Shop near Igloo | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Bottom of the Slope - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Mini Monkey Ledge | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Across from Ice Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Left of Mini Bonus Cave | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Level Entrance - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Level Entrance - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Igloo Area - left of entrance | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - Behind Tag Barrel Island | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - Behind Lone Platform | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - right of entrance | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water Under Shop Near Cabins Area | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water Under Mini Monkey Ledge | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water Under Mini-Rocket Bridge - left | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water Under Mini-Rocket Bridge - center | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Water Under Mini-Rocket Bridge - right | Wrinkly, Boss | `l.swim` | 
| Caves Frozen Castle | Tomato Game Room - left | Wrinkly | `self.logic = lambda _: True` | 
| Caves Frozen Castle | Tomato Game Room - right | Wrinkly | `self.logic = lambda _: True` | 
| Caves Chunky Cabin | Chunky Cabin - Bookshelf | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Area - Near Shop - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Area - Near Shop - far right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Tiny Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Near Cabin Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Bottom of the Slope - left | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Caves Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Wall between Donkey cabin and waterfall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Donkey Cabin | Donkey cabin - Right of entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Donkey Cabin | Donkey cabin - Back wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Diddy Upper Cabin | Diddy upper cabin - Near right corner | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Diddy Upper Cabin | Diddy upper cabin - Far right corner | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Diddy Upper Cabin | Diddy upper cabin - Back bookshelf | Wrinkly | `self.logic = lambda _: True` | 
| Caves Tiny Cabin | Tiny cabin - Near corner | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Tiny Cabin | Tiny cabin - Far corner | Wrinkly | `self.logic = lambda _: True` | 
| Caves Chunky Cabin | Chunky cabin - Near corner | Wrinkly | `self.logic = lambda _: True` | 
| Caves Chunky Cabin | Chunky cabin - Back shelf | Wrinkly | `self.logic = lambda _: True` | 
| Caves Donkey Igloo | Donkey igloo - Under the swords | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Tiny Igloo | Tiny igloo - Back wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Near ice castle tag barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Behind giant boulder ice wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Behind gorilla gone ice wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Lanky Race | Starting room of beetle race | Wrinkly | `self.logic = lambda _: True` | 

# Creepy Castle
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Creepy Castle Lobby | Castle Lobby - Central Pillar (1) | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby - Central Pillar (2) | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby - Central Pillar (3) | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby - Central Pillar (4) | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle Lobby | Castle Lobby - Central Pillar (5) | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Near Greenhouse | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Rocketbarrel Overhang | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Lowest ledge near tree | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Near Lower Cave Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Near Upper Cave Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Near Sewer Grate | Boss | `self.logic = lambda _: True` | 
| Creepy Castle | Against the Big Tree | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Moat Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Middle Shop | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Outside Lanky's Greenhouse | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | On Stairs to Moat Tag Barrel | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Between Moat and Cliff | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Top Shop Battlement - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Top Shop Battlement - center | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Top Shop Battlement - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Stairs to Drawbridge | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Rocketbarrel Battlement - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Rocketbarrel Battlement - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Moat Underwater by RocketBarrel | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat Under Drawbridge | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Next to Moat Door - left | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Next to Moat Door - right | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat Next to Ladder - left | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat Next to Ladder - right | Wrinkly, Boss | `l.swim` | 
| Castle Tree | Tree - First Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Room with Big Books - left | Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Room with big Books - back | Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Next to Exit - left | Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Next to Exit - right | Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Left Candle - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Left Candle - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Back Candle - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Back Candle - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Right Candle - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - Right Candle - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Trash Can | Trash Can - Cheese | Wrinkly | `self.logic = lambda _: True` | 
| Castle Shed | Inside the Shed | Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower Cave - Crypt skull left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower Cave - Crypt skull right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Mausoleum | Mausoleum - Under Grape Switch | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Castle Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Tower | Lanky wind tower - Right of Entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Tower | Lanky wind tower - Left of Entrance | Wrinkly | `self.logic = lambda _: True` | 
| Castle Greenhouse | Greenhouse - Dead end | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Castle Greenhouse | Greenhouse - Also dead end | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Castle Ballroom | Ballroom - In Front of Monkeyport Pad | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Museum | Museum - Far Left Side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Museum | Museum - Far Right Side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Museum | Museum - Tiny side - near the statue | Boss, Wrinkly | `l.monkeyport` | 
| Castle Museum | Museum - Tiny side - on the factory | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Castle Tree | Tree - Near Coconut Gate | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Tree | Tree - Past Punch Gate | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Strong Kong Alcove | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Library | Library - Left wing | Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Chunky crypt - between right coffins | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Chunky crypt - between left coffins | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Donkey crypt - behind the levers | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Diddy crypt - right of the tomb | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Diddy crypt - left of the tomb | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Crypt | Crypt - Second intersection | Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Near the crypt staircase | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Behind the mausoleum | Wrinkly | `self.logic = lambda _: True` | 
| Castle Mausoleum | Mausoleum - sprint corridor | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Dungeon | Dungeon - Lanky side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Dungeon | Dungeon - Diddy side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Dungeon | Dungeon - DK side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Upper Cave Shop Intersection | Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Next to dungeon door | Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Next to the chasm | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Tombstone near lower door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Behind the shed | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
