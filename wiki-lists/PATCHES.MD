# Patches 

## DK Isles
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Isles | DK Isles: On Aztec Building | ((Events.IslesDiddyBarrelSpawn in l.Events and l.jetpack and l.isdiddy) or (l.twirl and l.istiny and l.advanced_platforming)) and l.shockwave | 
| Isles | DK Isles: Under Caves Lobby Entrance | l.shockwave | 
| Isles | DK Isles: Front of Fungi Building | l.shockwave | 
| Training Grounds | DK Isles - Training Grounds: Banana Hoard | (l.vines or l.CanMoonkick()) and l.shockwave | 
| Training Grounds | DK Isles - Training Grounds: Rear Inside Tunnel | l.shockwave | 
| KLumsy | DK Isles - K Lumsy: Inside K. Lumsy's Cage | l.shockwave | 
| Creepy Castle Lobby | DK Isles - Creepy Castle Lobby: Castle Lobby | ((l.chunky and l.barrels and l.balloon and l.islanky) or l.CanMoonkick()) and l.shockwave | 
| Isles | DK Isles: Isles Boulders | l.shockwave | 
| Isles | DK Isles: Behind BFI | l.shockwave) | 
| Isles | DK Isles: Back of Kroc Isle (Lower) | l.shockwave | 
| Isles | DK Isles: Back of Kroc Isle (Middle) | l.shockwave | 
| Isles | DK Isles: Kroc Isle Left Arm | l.shockwave | 
| Isles | DK Isles: In Fungi Boulder | (l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events or l.phasewalk) and l.shockwave | 
| Isles | DK Isles: Behind Fungi Building | l.shockwave | 
| Isles | DK Isles: Behind Aztec Building | l.shockwave | 
| Banana Fairy Room | DK Isles - Banana Fairy Room: Behind Fairy Chair | l.shockwave | 
| Banana Fairy Room | DK Isles - Banana Fairy Room: Behind the Rareware Door | l.BananaFairies >= l.settings.rareware_gb_fairies and l.shockwave | 
| KLumsy | DK Isles - K Lumsy: Under K. Lumsy | (l.CanAccessKRool() or l.phasewalk) and l.shockwave | 
| Hideout Helm Lobby | DK Isles - Hideout Helm Lobby: Next to Tag Barrel | l.shockwave | 
| Hideout Helm Lobby | DK Isles - Hideout Helm Lobby: Blueprint Platform | ((l.coconut and l.scope) or (l.twirl and l.istiny and l.advanced_platforming)) and l.shockwave | 
| Jungle Japes Lobby | DK Isles - Jungle Japes Lobby: Near Tag Barrel | l.shockwave | 
| Angry Aztec Lobby | DK Isles - Angry Aztec Lobby: Behind Feather Door | l.feather and l.shockwave | 
| Frantic Factory Lobby | DK Isles - Frantic Factory Lobby: High Platform | ((l.grab and l.isdonkey) or l.CanMoonkick() or (l.advanced_platforming and (l.isdiddy or l.istiny or l.ischunky))) and l.shockwave | 
| Gloomy Galleon Lobby | DK Isles - Gloomy Galleon Lobby: Behind Mini Monkey Gate | ((l.mini and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.istiny and l.chunky) or l.CanPhaseswim()) and l.shockwave | 
| Fungi Forest Lobby | DK Isles - Fungi Forest Lobby: On Tag Crate | l.shockwave | 
| Crystal Caves Lobby | DK Isles - Crystal Caves Lobby: On the Lava | ((l.punch and l.strongKong and l.isdonkey) or l.phasewalk or l.ledgeclip) and l.shockwave | 
| Creepy Castle Lobby | DK Isles - Creepy Castle Lobby: Behind the entrance | l.shockwave | 
| Isles Snide Room | DK Isles - Isles Snide Room: Next to Snides | l.shockwave | 
| Training Grounds | DK Isles - Training Grounds: On the entrance hill | ((l.twirl and l.istiny) or (l.advanced_platforming and l.isdonkey)) and l.shockwave | 
| Training Grounds | DK Isles - Training Grounds: On the rear hill | l.shockwave | 
| Treehouse | DK Isles - Treehouse: Back of the treehouse | l.shockwave | 
</details>

## Jungle Japes
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Jungle Japes | Jungle Japes: On Painting Hill | ((l.handstand and l.islanky) or (l.twirl and l.istiny) or l.CanMoonkick() or ((l.phasewalk or l.generalclips) and (l.istiny or l.isdiddy))) and l.shockwave | 
| Jungle Japes | Jungle Japes: Inside Diddy's Cavern | l.shockwave | 
| Jungle Japes | Jungle Japes: Near Cannon to Diddy-freeing cage | l.shockwave | 
| Jungle Japes | Jungle Japes: Near the Vine Pit | l.shockwave | 
| Jungle Japes | Jungle Japes: On the useless Lanky ramp | (l.handstand and l.islanky) and l.shockwave | 
| Jungle Japes | Jungle Japes: Cranky-tunnel Crossing | l.shockwave | 
| Jungle Japes | Jungle Japes: Directly behind Cranky | l.shockwave | 
| Jungle Japes | Jungle Japes: Next to topright's hut | l.shockwave | 
| Jungle Japes | Jungle Japes: Behind Chunky Boulder | l.shockwave | 
| Jungle Japes | Jungle Japes: Inside the first tunnel - later half | l.shockwave | 
| Jungle Japes | Jungle Japes: Next to level entrance | l.shockwave | 
| Jungle Japes | Jungle Japes: Next to first tunnel entrance | l.shockwave | 
| Jungle Japes | Jungle Japes: Behind Diddy's Mountain | l.shockwave | 
</details>

## Angry Aztec
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Angry Aztec | Angry Aztec: Oasis | l.shockwave | 
| Aztec Chunky5DTemple | Angry Aztec - Aztec Chunky5D Temple: Chunky 5DT | ((l.pineapple and l.ischunky) or l.phasewalk) and l.shockwave | 
| Angry Aztec | Angry Aztec: Behind Chunky Cage | l.shockwave | 
| Angry Aztec | Angry Aztec: Entrance tunnel - near DK door | l.shockwave | 
| Angry Aztec | Angry Aztec: Next to Tiny Temple - left | l.shockwave | 
| Angry Aztec | Angry Aztec: Next to Tiny Temple - right | l.shockwave | 
| Angry Aztec | Angry Aztec: Behind Llama Cage | l.shockwave | 
| Aztec Tiny Temple | Angry Aztec - Aztec Tiny Temple: Main room back-left | l.shockwave | 
| Aztec Tiny Temple | Angry Aztec - Aztec Tiny Temple: Next to Tiny cage | l.shockwave | 
| Angry Aztec | Angry Aztec: Next to Llama Temple | l.shockwave | 
| Angry Aztec | Angry Aztec: Next to Snide | l.shockwave | 
| Angry Aztec | Angry Aztec: Behind Gong-tower | l.shockwave | 
| Angry Aztec | Angry Aztec: Left of Gong-tower | l.shockwave | 
| Aztec Llama Temple | Angry Aztec - Aztec Llama Temple: Next to Llama Left | l.shockwave | 
| Aztec Llama Temple | Angry Aztec - Aztec Llama Temple: Next to Llama Right | l.shockwave | 
</details>

## Frantic Factory
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Frantic Factory | Frantic Factory: Dark Room | ((l.punch and l.chunky) or l.phasewalk) and l.shockwave | 
| Frantic Factory | Frantic Factory: Middle of Entrance Room | l.shockwave | 
| Frantic Factory | Frantic Factory: Clock-in room left | l.shockwave | 
| Frantic Factory | Frantic Factory: Clock-in room right | l.shockwave | 
| Frantic Factory | Frantic Factory: Halfway the hatch near entrance - next to the window - Tiny's 10 CB | l.shockwave | 
| Frantic Factory | Frantic Factory: Tunnel to production room | l.shockwave | 
| Frantic Factory | Frantic Factory: Next to DK Arcade | l.shockwave | 
| Frantic Factory | Frantic Factory: Near Snide | l.shockwave | 
| Frantic Factory | Frantic Factory: On Diddy's Block Tower | (l.spring or l.CanMoonkick()) and l.shockwave | 
| Frantic Factory | Frantic Factory: In Lanky's Piano Room | ((l.trombone and l.islanky) or l.CanAccessRNDRoom()) and l.shockwave | 
| Frantic Factory | Frantic Factory: In Diddy's Pincode enemies room | ((l.guitar and l.isdiddy) or l.CanAccessRNDRoom()) and l.shockwave | 
| Frantic Factory | Frantic Factory: In front of Chunky's toy boss room | ((l.punch and l.ischunky) or l.CanAccessRNDRoom()) and l.shockwave | 
| Frantic Factory | Frantic Factory: Near Funky | l.shockwave | 
| Frantic Factory | Frantic Factory: Tiny race entry area | ((l.mini and l.istiny) or l.phasewalk) and l.shockwave | 
| Frantic Factory | Frantic Factory: R&D lever room - by Tiny's barrel | l.shockwave | 
</details>

## Gloomy Galleon
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Galleon Lighthouse | Gloomy Galleon - Galleon Lighthouse: Interior Rear | l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: On the ship near Cranky | l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Next to cannon in cannonball room | (Events.WaterSwitch in l.Events or (l.advanced_platforming and (l.islanky or l.ischunky))) and l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Entrance tunnel - under tag barrel | l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Next to Lighthouse ladder | l.shockwave | 
| Galleon Lighthouse | Gloomy Galleon - Galleon Lighthouse: Behind Whomp's Fortress floor 2 | l.shockwave | 
| Galleon Lighthouse | Gloomy Galleon - Galleon Lighthouse: On top of Whomp's Fortress | l.shockwave | 
| Galleon Sick Bay | Gloomy Galleon - Galleon Sick Bay: Chunky ship entrance | l.shockwave | 
| Galleon Sick Bay | Gloomy Galleon - Galleon Sick Bay: Chunky ship - backleft corner | l.shockwave | 
| Galleon Sick Bay | Gloomy Galleon - Galleon Sick Bay: Chunky ship - behind the non-alcoholic tower | ((l.punch and l.ischunky) or l.phasewalk) and l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Next to Cannonball - in front | (Events.WaterSwitch in l.Events or (l.advanced_platforming and (l.ischunky or l.islanky))) and l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Next to Cannonball - behind | (Events.WaterSwitch in l.Events or (l.advanced_platforming and (l.ischunky or l.islanky))) and l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Behind Chunky's Big GB Chest | l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: Behind the ship you shoot onto with the cannon | l.shockwave | 
| Gloomy Galleon | Gloomy Galleon: In front of Cranky | l.shockwave | 
</details>

## Fungi Forest
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Fungi Forest | Fungi Forest: Beanstalk | l.shockwave | 
| Fungi Forest | Fungi Forest: Mill Grass | l.shockwave | 
| Fungi Forest | Fungi Forest: Top of Owl Tree | ((l.jetpack and l.isdiddy) or l.CanMoonkick()) and l.shockwave | 
| Fungi Forest | Fungi Forest: Near BBlast | l.shockwave | 
| Fungi Forest | Fungi Forest: Under the Owl Tree | l.shockwave | 
| Fungi Forest | Fungi Forest: Next to Rabbit's house | l.shockwave | 
| Forest Mill Front | Fungi Forest - Forest Mill Front: Inside the water mill - near DK's levers | l.shockwave | 
| Forest Mill Back | Fungi Forest - Forest Mill Back: Inside the water mill - near Chunky's coins (Chunky's punch door) | l.shockwave | 
| Fungi Forest | Fungi Forest: Next to Diddy Pad | l.shockwave | 
| Forest Thornvine Barn | Fungi Forest - Forest Thornvine Barn: Next to ladder | l.shockwave | 
| Forest Giant Mushroom | Fungi Forest - Forest Giant Mushroom: Next to a cannon | ((l.istiny and l.twirl) or l.isdonkey) and l.shockwave | 
| Forest Giant Mushroom | Fungi Forest - Forest Giant Mushroom: Next to the cannon below the night door | l.vines and l.shockwave | 
| Fungi Forest | Fungi Forest: Next to Crusher Output | l.shockwave | 
| Fungi Forest | Fungi Forest: On the Tomato Field | l.shockwave | 
| Fungi Forest | Fungi Forest: Near Funky with the fenced in Chunky coins | l.TimeAccess(Regions.WormArea, Time.Night) and l.shockwave | 
</details>

## Crystal Caves
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Crystal Caves | Crystal Caves: Giant Kosha Room | l.shockwave | 
| Crystal Caves | Crystal Caves: Near lanky's 1DC - lower | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Funky under Diddy's barrel | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Diddy's top 5D Cabin door | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Tag barrel at 5D Cabin | l.shockwave | 
| Crystal Caves | Crystal Caves: Next to Ice Castle | l.shockwave | 
| Crystal Caves | Crystal Caves: Next to Lanky's 1DC - upper | l.shockwave | 
| Crystal Caves | Crystal Caves: Next to Donkey's 1DC - left | l.shockwave | 
| Caves Frozen Castle | Crystal Caves - Caves Frozen Castle: Next to Slam Puzzle - left | l.shockwave | 
| Caves Frozen Castle | Crystal Caves - Caves Frozen Castle: Next to Slam Puzzle - right | l.shockwave | 
| Crystal Caves | Crystal Caves: On top of the Igloo | l.shockwave | 
| Crystal Caves | Crystal Caves: Under tag barrel near igloo | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Primate Punch wall opposite cranky | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Primate Punch wall near entrance | l.shockwave | 
| Crystal Caves | Crystal Caves: Near Primate Punch wall near snide | l.shockwave | 
</details>

## Creepy Castle
<details>
<summary>Dirt Patch Locations</summary>

| Map | Name | Logic |
| --- | ---- | ----- |
| Creepy Castle | Creepy Castle: Top of Castle near shop | l.shockwave | 
| Creepy Castle | Creepy Castle: Near the Catacombs Door | l.shockwave | 
| Creepy Castle | Creepy Castle: Upper Gravestone | l.shockwave | 
| Creepy Castle | Creepy Castle: Top of Castle near fence | l.shockwave | 
| Castle Ballroom | Creepy Castle - Castle Ballroom: Ballroom - Back Left | l.shockwave | 
| Castle Ballroom | Creepy Castle - Castle Ballroom: Ballroom - Back Right | l.shockwave | 
| Castle Museum | Creepy Castle - Castle Museum: Museum - Pillar Front | ((l.monkeyport and l.istiny) or l.phasewalk) and l.shockwave | 
| Castle Museum | Creepy Castle - Castle Museum: Museum - Pillar Back Right | ((l.monkeyport and l.istiny) or l.phasewalk) and l.shockwave | 
| Castle Museum | Creepy Castle - Castle Museum: Museum - Pillar Back Left | ((l.monkeyport and l.istiny) or l.phasewalk) and l.shockwave | 
| Creepy Castle | Creepy Castle: Next to Greenhouse | l.shockwave | 
| Castle Crypt | Creepy Castle - Castle Crypt: 3Kong crypt entrance | l.shockwave | 
| Castle Mausoleum | Creepy Castle - Castle Mausoleum: 2kong crypt entrance | l.shockwave | 
| Creepy Castle | Creepy Castle: Between the catacombs door and Tiny Kasplat | l.shockwave | 
| Creepy Castle | Creepy Castle: Next to the Drawing Drawbridge | l.shockwave | 
| Creepy Castle | Creepy Castle: Next to Lanky coin tree (near catacombs door) | l.shockwave | 
| Castle Dungeon | Creepy Castle - Castle Dungeon: Under the chunky balloon without coins | ((l.punch and l.ischunky) or l.phasewalk) and l.shockwave | 
</details>
