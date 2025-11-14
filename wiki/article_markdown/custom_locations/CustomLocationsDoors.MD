
# Jungle Japes
| Map | Name | Door types acceptable in location | Logic |
| --- | ---- | --------------------------------- | ----- |
| Jungle Japes Lobby | Japes Lobby - Middle Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Far Left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Close Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Far Right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes Lobby | Japes Lobby - Close Left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Diddy Cave | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Near Painting Room | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Fairy Cave | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Diddy Cage - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Alcove Above Diddy Tunnel - right | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Alcove Above Diddy Tunnel - left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Minecart Exit -right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Across From Minecart Exit | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Main Area - Next to Tunnel to Tiny Gate | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Beehive Area - Next to Beehive - far left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Beehive Area - Next to Beehive - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Behind Rambi Door - watery room - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Behind Rambi Door - watery room - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Top of Lanky's Useless Slope - left | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Top of Lanky's Useless Slope - right | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Underwater by Warp 2 | Boss, Wrinkly | `l.swim` | 
| Jungle Japes | Underwater by Chunky's underground | Boss, Wrinkly | `l.swim` | 
| Jungle Japes | Next to Funky - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Lanky's Painting Room - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Next to Lanky's Painting Room - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Outside Diddy Cave Switch - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Outside Diddy Cave Switch - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Entrance Tunnel - Near Diddy Cave - back left | Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Entrance Tunnel - Near Diddy Cave - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Entrance Tunnel - Near Warppad 1 and 2 | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Diddy Tunnel - next to hole - river side | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Diddy Tunnel - river side | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Near Warp 4 and Tunnel Threeway crossing | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Tunnel - Crossroad | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - front-right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - center left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - center right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - back left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Jungle Japes | Cranky Area - back right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Japes Tiny Hive | Beehive Room 2 - left | Wrinkly | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips` | 
| Japes Tiny Hive | Beehive Room 2 - right | Wrinkly | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips` | 
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
| Angry Aztec Lobby | Aztec Lobby - Behind Feather Door | Wrinkly | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Angry Aztec | Near Funky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Cranky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Candy's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Near Snide's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Behind 5DT | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Candy - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Under Diddy's Tiny Temple Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Chunky's Tiny Temple Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Tiny's Tiny Temple Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Under Lanky's Tiny Temple Switch | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Diddy Tower Stairs - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tag Barrel near Snides | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Under the Vulture Cage | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5Door Temple's 6th Door | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Cranky Tunnel - Near Chunky Barrel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Cranky Tunnel - Near Chunky Barrel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Cranky Tunnel - Near Road to Cranky - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Cranky Tunnel - Near Road to Cranky - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5Door Temple Staircase - front | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | 5Door Temple Staircase - back | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Entrance Tunnel - next to Coconut Switch | Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Entrance Tunnel - left (near the oasis end) | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | In the sealed quicksand tunnel | Wrinkly | `l.isdonkey and l.strongKong` | 
| Angry Aztec | Near Tag Barrel near Snides - strong kong | Wrinkly | `l.isdonkey and l.strongKong` | 
| Aztec Llama Temple | In Face Matching Game - right | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Aztec Llama Temple | In Face Matching Game - left | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Tiny Temple - back left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Oasis - Next to Tunnel - far left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Oasis - Next to Tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Between Snides and Diddy Gong Tower | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Next to Llama Temple - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Angry Aztec | Llama Temple's switchless side | Boss, Dk_Portal | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Main Room - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Main Room - back | Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Across from Slope to Tiny Cage - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Aztec Tiny Temple | Tiny Temple - Across from Slope to Tiny Cage - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
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
| Frantic Factory | Behind Chunky's Toy Box - big | Wrinkly | `(l.ischunky and l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Next to Hatch with Tall Pole - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Next to Hatch with Tall Pole - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Bottom of the Tall Pole | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room - Under Tiny Conveyors | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Kong Cage Room - Behind Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Under Cranky's Lab | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Under Candy's Store | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Next to DK's Count to 16 Puzzle | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D Room - Next to Tunnel to Car Race | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - Under Tunnel to Funky's | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D Room - Dead End | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D Room - Blind Corner Next to Tunnel to Car Race | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Funky's Room - Across from Melon Crate | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - Air Vent Under Arcade Window | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - Under Arcade Window - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - Behind Tag Barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | R&D Room - Next to Diddy's Pincode Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Tiny's Race Entry Area | Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Kong Cage Room - Next to Tag Barrel | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Production Room - in Alcove Next to Tiny's Barrel | Wrinkly | `l.istiny and l.twirl` | 
| Frantic Factory | Production Room - Next to Diddy's Switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Arcade Room - in a corner | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - Next to Tiny Barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Block Tower Room - at the Base of the Block Tower | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Frantic Factory | Clock Room - Under Clock | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Frantic Factory | Clock Room - front left | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Clock Room - back left | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Clock Room - front right | Wrinkly, Boss | `self.logic = lambda _: True` | 
| Frantic Factory | Top of Pipe Near Kong-freeing Switch | Wrinkly, Dk_Portal | `self.logic = lambda _: True` | 
| Frantic Factory | Pin Code Room - front-right | Wrinkly | `(l.isdiddy and l.guitar) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Lanky's Piano Room - right | Wrinkly | `(l.islanky and l.trombone) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Lanky's Piano Room - left | Wrinkly | `(l.islanky and l.trombone) or l.CanAccessRNDRoom()` | 
| Frantic Factory | Chunky's Dark Room | Wrinkly, Boss | `(l.chunky and l.punch) or l.CanPhase() or l.generalclips` | 
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
| Gloomy Galleon | Near Cranky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Deep Hole | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind 2DS | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind Enguarde Door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cactus | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | In hallway to Shipyard - Tiny switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | In hallway to Shipyard - Lanky switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | In hallway to Primate Punch Chests | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Under Baboon Blast pad | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Under RocketBarrel barrel | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Cannonball game | Boss, Wrinkly | `l.CanGetOnCannonGamePlatform()` | 
| Gloomy Galleon | Next to Coconut switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Entrance Tunnel - near entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Peanut switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Music Cactus - bottom back left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Music Cactus - bottom front left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Music Cactus - bottom back right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Music Cactus - bottom front right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | On top of Seal cage | Wrinkly | `l.isdiddy and l.jetpack` | 
| Gloomy Galleon | Treasure Chest Exterior | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Next to Warp 3 in Cranky's Area | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | In Primate Punch Chest Room - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind Chunky punch gate in Cranky Area | Boss, Wrinkly | `(l.ischunky and l.punch) or l.CanPhase()` | 
| Gloomy Galleon | Low water alcove in lighthouse area | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Behind boxes in Cranky Area | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mech Fish Gate - far left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mech Fish Gate - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mech Fish Gate - middle | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mech Fish Gate - right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Mech Fish Gate - far right | Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Cannonball Area Exit | Boss, Wrinkly | `l.swim` | 
| Gloomy Galleon | 2Dship's secret 3rd door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Near Mermaid's Palace - Under Tag Barrel | Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Up the ledge | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Lighthouse | Lighthouse - Back | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mermaid Room | In Mermaid's Palace | Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip DKTiny | Tiny's 5D ship | Wrinkly | `self.logic = lambda _: True` | 
| Galleon5DShip Diddy Lanky Chunky | Lanky's 5D ship | Wrinkly | `self.logic = lambda _: True` | 
| Galleon2DShip | Lanky's 2D ship | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Galleon Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Pineapple gate tunnel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Gloomy Galleon | Pineapple gate tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - start left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - start right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons front left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons front right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Sick Bay | Seasick ship - after cannons center | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mechafish | Left wall of Mech Fish | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Galleon Mechafish | Right wall of Mech Fish | Boss, Wrinkly | `self.logic = lambda _: True` | 
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
| Fungi Forest | Behind DK Barn | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Beanstalk Area | Boss, Wrinkly | `Events.Night in l.Events` | 
| Fungi Forest | Near Snide's | Boss, Wrinkly | `Events.Day in l.Events` | 
| Fungi Forest | Top of Giant Mushroom | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Owl Area | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | On top of Cage outside Conveyor Belt | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Watermill - front - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Watermill - right - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Watermill - right - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Watermill Roof - tower | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Boxes outside of Diddy's Barn | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Immediately Inside the Thornvine Area - right | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Immediately Inside the Thornvine Area - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Outside DK's Barn | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Next to Rabbit's House | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Owl Area - Near Rocketbarrel Barrel - far left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Funky Area - Near Tiny Coins | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Tag Barrel near Cranky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Rocketbarrel Barrel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Rocketbarrel Barrel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Mushroom Area - Next to Cranky | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Clock Area - Next to Purple Tunnel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Clock Area - Next to Purple Tunnel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Clock Area - Next to Clock - left | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Clock Area - Next to Clock - right | Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Funky Area - Near Beanstalk - left | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Fungi Forest | Funky Area - Near Beanstalk - back | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Inside the Mushroom - All Kong Gun Switch - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Inside the Mushroom - All Kong Gun Switch - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Inside the Mushroom - halfway along the Dead End | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Giant Mushroom | Inside the Mushroom - Along the Wall near Klump and Oranges | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Chunky Face Room | Chunky's Face Puzzle | Wrinkly | `self.logic = lambda _: True` | 
| Forest Lanky Zingers Room | Lanky's 2-Mushroom Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Forest Mill Front | DK Lever puzzle Area | Wrinkly | `(l.isdonkey and l.CanSlamSwitch(Levels.FungiForest, 2)) or l.CanPhase() or l.generalclips` | 
| Forest Mill Back | Mill - back side - Near Chunky Coins | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
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
| Crystal Caves | On Rotating Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Near Snide's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Giant Boulder Room | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | On Sprint Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Near 5DI | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Lanky's Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Chunky's Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Diddy's Lower Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Diddy's Upper Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Under the Waterfall (Cabin Area) | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Across from the 5Door Cabin | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - DK's right | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - Diddy's right | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - Tiny's right | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - Chunky's right | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - Lanky's right | Boss | `self.logic = lambda _: True` | 
| Crystal Caves | 5Door Igloo - DK's instrument pad | Boss | `l.swim` | 
| Crystal Caves | 5Door Igloo - Diddy's instrument pad | Boss | `l.swim` | 
| Crystal Caves | 5Door Igloo - Tiny's instrument pad | Boss | `l.swim` | 
| Crystal Caves | 5Door Igloo - Chunky's instrument pad | Boss | `l.swim` | 
| Crystal Caves | 5Door Igloo - Lanky's instrument pad | Boss | `l.swim` | 
| Crystal Caves | Ice Castle Area - Near Rock Switch | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Between Funky and Ice Castle - on land | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Between Funky and Ice Castle - underwater | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | In Water Near W4 Opposite Cranky - right | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | In Water Near W4 Opposite Cranky - left | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Under Bridge to Cranky | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Under Handstand Slope | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Mini Monkey Ledge | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Across from Snide | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Slope to Cranky with Mini Monkey Hole | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Level Entrance - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Level Entrance - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Igloo Area - left of entrance | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - Behind Tag Barrel Island | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - Behind Warp 1 | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Igloo Area - right of entrance | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Under Funky's Store | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | Next to Waterfall that's Next to Funky | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | In Water Under Funky - left | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | In Water Under Funky - center | Wrinkly, Boss | `l.swim` | 
| Crystal Caves | In Water Under Funky - right | Wrinkly, Boss | `l.swim` | 
| Caves Frozen Castle | Ice Castle Interior - left | Wrinkly | `self.logic = lambda _: True` | 
| Caves Frozen Castle | Ice Castle Interior - right | Wrinkly | `self.logic = lambda _: True` | 
| Caves Chunky Cabin | In Chunky's 5Door Cabin on a Book Shelf | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Area - Near Candy - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Area - Near Candy - far right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Outside Tiny's Cabin | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Cabin Area - Next to Tag Barrel on 2nd Floor | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Under Cranky Slope - small | Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Caves Vanilla Level Entry | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Crystal Caves | Wall between Donkey cabin and waterfall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Donkey Cabin | Donkey 5door cabin - Right of entrance | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Caves Donkey Cabin | Donkey 5door cabin - Back wall | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
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
| Crystal Caves | Near Cranky | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
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
| Creepy Castle | Small Plateau | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Back of Castle | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Near Funky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Near Candy's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Small Pool outside of the Big Tree | Boss | `self.logic = lambda _: True` | 
| Creepy Castle | Against the Big Tree | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Tag Barrel at the Warp Pad Hub | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Cranky's | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Outside Lanky's Greenhouse | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | On Stairs to Tag Barrel at the Warp Pad Hub | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Castle Moat - Above Tiny's Kasplat | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Snide's Battlement - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Snide's Battlement - center | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Snide's Battlement - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Next to Stairs to Drawing Drawbridge | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Battlement with Rocketbarrel Barrel - left | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Battlement with Rocketbarrel Barrel - right | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Moat - Underwater by Diddy Barrel | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat - Under Drawing Drawbridge | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat - Next to Tunnel Entrance - left | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat - Next to Tunnel Entrance - right | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat - Next to Ladder - left | Wrinkly, Boss | `l.swim` | 
| Creepy Castle | Moat - Next to Ladder - right | Wrinkly, Boss | `l.swim` | 
| Castle Tree | Inside the Tree | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
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
| Castle Shed | Inside Chunky's Shed | Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower Tunnel - Under Peanut Switch | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Lower Cave | Lower Tunnel - Under Coconut and Pineapple Switches | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
| Castle Mausoleum | Crypt - Under Lanky's Switch | Wrinkly | `self.logic = lambda _: True` | 
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
| Castle Upper Cave | Candy intersection | Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Next to dungeon door | Wrinkly | `self.logic = lambda _: True` | 
| Castle Upper Cave | Next to the chasm | Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Tombstone near lower door | Boss, Wrinkly | `self.logic = lambda _: True` | 
| Creepy Castle | Behind the shed | Boss, Dk_Portal, Wrinkly | `self.logic = lambda _: True` | 
