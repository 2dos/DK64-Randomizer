
# DK Isles
## Training Grounds
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around tree by training barrels | 4 |  | 
| On left treetop by Cranky's | 2 | `l.climbing` | 
| On right treetop by Cranky's | 2 | `l.climbing` | 
| On cliff top by Cranky's | 3 | `l.climbing` | 
| Bottom of the pool | 3 | `l.swim` | 
| Banana hoard | 4 | `(l.can_use_vines or l.CanMoonkick()) and l.climbing` | 
| Rear Tunnel | 3 |  | 
## Treehouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In tire in DK's house | 2 |  | 
| By the door in DK's house | 3 |  | 
## Isles
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On beach, in corner by path to Aztec lobby | 3 |  | 
| In water below waterfall | 5 | `l.swim` | 
| On top of tree between Japes Lobby and Fungi cannon | 3 | `l.climbing` | 
| On slope on path to Aztec lobby | 3 |  | 
| At the bottom of Aztec steps | 5 |  | 
| In little alcove in DK's ear in front of Aztec lobby | 3 |  | 
| On top of Aztec lobby | 4 |  | 
| On top of K. Lumsy's prison | 4 | `( (l.hasMoveSwitchsanity(Switches.IslesMonkeyport) and ((l.istiny and l.twirl) or (l.settings.damage_amount != DamageAmount.ohko and not l.IsHardFallDamage()))) or ((l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events) and Events.IslesDiddyBarrelSpawn in l.Events and l.isdiddy and l.jetpack) or ( (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events) and ((l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey)) and l.settings.damage_amount != DamageAmount.ohko and not l.IsHardFallDamage()) or (l.istiny and l.twirl)) ) )` | 
| On top of Fungi lobby | 3 |  | 
| Hanging off the edge behind Fungi lobby | 3 |  | 
| Around palm tree on lone fairy island | 5 |  | 
| By main warps | 5 |  | 
| Back of Fairy Isle | 3 |  | 
| Back of Krem Isle, near propellors | 3 |  | 
| Behind pillar on path to Factory lobby | 3 |  | 
| Around pillar behind Factory lobby | 5 |  | 
| To the right of the staircase to Factory lobby | 3 |  | 
| Around Saxophone pad | 4 |  | 
## Banana Fairy Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On lilypads in front pools | 4 |  | 
| On lilypads in back pools | 4 |  | 
## Isles Snide Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| To the right of Snide's | 3 |  | 
| To the left of Snide's | 3 |  | 
## KLumsy
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around a candle to the left | 4 |  | 
| Around a candle to the right | 4 |  | 
## Jungle Japes Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to Japes lobby entrance | 3 |  | 
| Next to a torch on the left | 3 |  | 
## Angry Aztec Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the front pillar | 4 |  | 
| Around the back pillar | 4 |  | 
| On the left stairs | 3 |  | 
| In the back room (left) | 3 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.phasewalk` | 
| In the back room (right) | 3 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.phasewalk` | 
## Frantic Factory Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In tag barrel corner | 3 |  | 
| On top level in corner | 3 | `((l.grab and l.donkey) or (l.advanced_platforming and (l.isdiddy or l.istiny)))` | 
| On top level at the end | 3 | `((l.grab and l.donkey) or (l.advanced_platforming and (l.isdiddy or l.istiny)))` | 
## Gloomy Galleon Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In water on left side | 3 |  | 
| On left side | 3 |  | 
| On right side | 3 |  | 
| Around golden banana | 3 | `l.swim and ((l.mini and l.twirl and l.tiny and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.chunky) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
## Fungi Forest Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On wooden box | 3 |  | 
| On flour bag | 2 |  | 
| On metal box | 3 |  | 
| In corner by B. Locker | 3 |  | 
## Crystal Caves Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around blue switch | 4 |  | 
| Beyond wall to lava GB | 3 | `(l.punch and l.chunky) or l.phasewalk or l.ledgeclip` | 
| Around Lanky blueprint room | 5 | `(l.punch and l.chunky) or l.phasewalk or l.ledgeclip` | 
| Near left ledge | 3 |  | 
## Creepy Castle Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around entrance | 5 |  | 
| In alcove to the right | 2 |  | 
| In alcove to the left | 2 |  | 
| On top of center piece | 3 | `l.chunky and l.barrels and l.islanky and l.balloon` | 
| On wooden posts | 2 |  | 
## Hideout Helm Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around Gorilla Gone pad | 4 |  | 

# Jungle Japes
## Jungle Japes
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to the DK portal | 3 |  | 
| Next to the bush to the right | 3 |  | 
| Next to the bush to the left | 3 |  | 
| In the first tunnel to the left | 3 |  | 
| In the Diddy GB cave room around a torch | 3 |  | 
| In the first tunnel past peanut gate to the left | 3 |  | 
| Around far W1 | 3 |  | 
| Around low W2 | 3 |  | 
| Against wall near W1 and W2 | 3 |  | 
| Against wall between W1W2 and underground | 3 |  | 
| Around Chunky underground entrance | 4 |  | 
| In corner behind W3 beehive side | 3 |  | 
| Against wall across from DK's kasplat alcove | 3 |  | 
| Against wall across from Tiny's kasplat alcove | 3 |  | 
| In front of each feather switch | 2 |  | 
| Around W5 in beehive area | 4 |  | 
| On left log in beehive area | 5 |  | 
| On right log in beehive area | 5 |  | 
| To the right of the beehive | 3 |  | 
| To the left of the beehive | 3 |  | 
| Beehive area around front big tree | 4 |  | 
| Beehive area around left big tree | 4 |  | 
| Beehive area around back big tree | 4 |  | 
| Beehive area around right big tree | 4 |  | 
| On riverbed near tag barrel | 3 | `l.swim` | 
| In front of Tiny's caged GB | 3 |  | 
| Against wall to the right near Painting room | 3 |  | 
| In corner behind W3 painting room side | 3 |  | 
| Around middle tree tag barrel side | 4 |  | 
| In front of Diddy's caged GB | 3 |  | 
| Around tree in front of Snide's | 4 |  | 
| In front of Chunky's caged GB | 3 |  | 
| On slope between Snide's and mountain | 5 |  | 
| Behind melon crate | 3 |  | 
| On slope between mountain and Diddy cage | 3 |  | 
| Around tree in front of Diddy's cage | 4 |  | 
| In front of T&S portal near Diddy kasplat | 3 |  | 
| In pit near Diddy kasplat | 3 |  | 
| Around tunnel W4 | 3 |  | 
| Around small torch in W4 tunnel | 4 |  | 
| Around small torch near Lanky kasplat | 3 |  | 
| Against right wall in Lanky kasplat room | 3 |  | 
| Against left wall in Lanky kasplat room | 3 |  | 
| On top of right slippery slope | 3 | `l.handstand` | 
| Around Tiny hut | 4 |  | 
| Around Lanky hut | 4 |  | 
| Around Donkey hut | 4 |  | 
| Around Diddy hut | 4 |  | 
| Around Cranky W4 | 3 |  | 
| Around far tree in Cranky area | 4 |  | 
| In front of Rambi gate | 4 |  | 
| Around melon crate in boulder room | 3 |  | 
| Around torch near fairy room | 3 |  | 
| Around torch in fairy room | 3 |  | 
| Left side of fairy room | 4 |  | 
| Right side of fairy room | 3 |  | 
| Around torch in the middle of fairy room on water surface | 4 |  | 
| Near entrance portal | 3 |  | 
| Main Area Underwater (1) | 3 | `l.swim` | 
| Around the Baboon Blast Pad | 3 | `(l.can_use_vines or l.CanMoonkick()) and l.climbing` | 
| Start of first tunnel | 3 |  | 
| Diddy Cavern (1) | 3 |  | 
| Fairy Pool | 5 | `l.swim` | 
| Near Rambi Box | 3 | `l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.phasewalk` | 
| Diddy Cavern (2) | 3 |  | 
| Near Diddy Kasplat | 3 |  | 
| Near Tiny Kasplat | 3 |  | 
| In between the vines near Diddy Kasplat | 1 | `l.can_use_vines` | 
| Near DK Kasplat | 3 |  | 
| Cannon Path | 2 |  | 
| Near Lanky Kasplat | 3 |  | 
| Main Area Underwater (2) | 2 | `l.swim` | 
| Main Area Underwater (3) | 3 | `l.swim` | 
| Behind the stump | 3 |  | 
| On top of the mountain | 5 |  | 
| Near Snide's HQ | 5 |  | 
## Japes Under Ground
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Right side towards the end of the cave | 3 |  | 
| Left side towards the end of the cave | 3 |  | 
| Around center platform | 3 |  | 
| Behind Entrance Cannon | 3 |  | 
| Near Underground Reward | 3 | `(l.can_use_vines and l.pineapple and l.ischunky) or l.phasewalk` | 
## Japes Lanky Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to entrance | 3 |  | 
| On Pegs | 2 |  | 
## Japes Mountain
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On right minecart near entrance | 3 |  | 
| In treadmills room front left corner | 2 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.phasewalk` | 
| On coal pile in second room | 1 |  | 
| Behind a barrel near the HI-LO Machine | 1 | `(l.charge and l.isdiddy) or l.phasewalk` | 
| Under the Conveyors | 1 | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.phasewalk` | 
| On the bridge | 1 | `l.peanut or l.advanced_platforming` | 
| On a coal stack | 1 |  | 
## Japes Tiny Hive
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind Door 1 | 2 |  | 
| Around final room | 4 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.phasewalk or l.generalclips` | 
| Behind Door 2 | 2 | `((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.phasewalk or l.generalclips) and l.istiny` | 
## Japes Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Between cannons in the Baboon Blast Course | 2 |  | 

# Angry Aztec
## Angry Aztec
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In front of Chunky vase room door | 3 |  | 
| In front of Donkey kasplat room door | 3 |  | 
| Left side across the sand from Candy's store | 3 |  | 
| Right side of Candy's store | 3 |  | 
| Next to quicksand close to llama cage | 3 |  | 
| On gentle slope of llama cage | 4 |  | 
| Around Oasis W1 | 3 |  | 
| Each side of Tiny Temple stairs | 4 |  | 
| Behind guitar door | 2 |  | 
| On boulder switch | 4 |  | 
| Right side of Cranky's | 2 |  | 
| Against wall near Chunky bonus GB | 3 |  | 
| In shady corner to the right of Llama temple | 3 |  | 
| Around W4 by other warps | 3 |  | 
| Around W3 by warps | 3 |  | 
| Around rocketbarrel | 4 |  | 
| By quicksand near tower | 3 |  | 
| Behind tower | 3 |  | 
| On ramps on stairs leading to tower | 4 |  | 
| Middle of Snide's platform | 3 |  | 
| On corner of path near Snide's tag barrel | 3 |  | 
| Left wall by Funky's | 4 |  | 
| Left corner near quicksand by Llama temple | 3 |  | 
| Left of Llama temple stairs | 3 |  | 
| Right of Llama temple stairs | 3 |  | 
| Front of 5 door temple | 3 |  | 
| Top of 5 door temple side stairs | 2 |  | 
| On roof of 5 door temple | 3 | `l.jetpack` | 
| On roof of Llama Temple | 4 | `l.jetpack` | 
| Around far W5 | 4 |  | 
| Near Cranky's Lab | 4 |  | 
| Outside Funky's | 5 |  | 
| Around Oasis Warp 2 | 5 |  | 
| Under Snide's HQ Tag Barrel | 3 |  | 
| On posts near Llama | 2 |  | 
| At the end of the quicksand tunnel | 4 |  | 
| Around the Giant Boulder | 3 |  | 
| Around the Bonus Barrel Cage | 4 |  | 
| Vines near Snide's HQ | 4 | `l.can_use_vines and l.climbing` | 
| Around Hunky Chunky Barrel | 3 |  | 
| Behind 5-Door Temple | 3 |  | 
| Under Oasis Tag | 4 |  | 
| Around Totem W5 | 5 |  | 
| Around Tiny Temple | 4 |  | 
| Blueprint Cavern | 3 | `(l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) or l.phasewalk) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny))` | 
## Aztec Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Baboon Blast Course | 3 |  | 
## Aztec Chunky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| First Switch | 1 |  | 
| On torches | 2 | `(l.pineapple and l.ischunky) or l.phasewalk` | 
| On stairs | 3 | `(l.pineapple and l.ischunky) or l.phasewalk` | 
| Around the temple | 4 | `(l.pineapple and l.ischunky) or l.phasewalk` | 
## Aztec Diddy5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind some pillars | 4 | `(l.peanut and l.isdiddy) or l.phasewalk` | 
| Dead Ends | 2 | `(l.peanut and l.isdiddy) or l.phasewalk` | 
## Aztec Donkey5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Final pathway | 4 | `(l.coconut and l.isdonkey) or l.phasewalk` | 
| Near 2nd Switch | 2 | `(l.coconut and l.isdonkey) or l.phasewalk` | 
## Aztec Lanky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Starting Staircase | 2 | `(l.grape and l.islanky) or l.phasewalk` | 
| Final Corridors | 2 | `(l.grape and l.islanky) or l.phasewalk` | 
## Aztec Tiny5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Fairy Side Room | 4 | `(l.feather and l.istiny and l.mini) or l.phasewalk` | 
| Other Side Room | 4 | `(l.feather and l.istiny and l.mini) or l.phasewalk` | 
| Under Feather Switches and at Dead Ends | 1 |  | 
| Under Feather Switches and at Dead Ends | 2 | `(l.feather and l.istiny) or l.phasewalk` | 
## Aztec Llama Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Left Bannister | 5 |  | 
| Right Bannister | 5 |  | 
| Matching Game Room | 3 | `(l.grape and l.islanky) or l.phasewalk` | 
| Around the right lava room platform | 4 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.advanced_platforming)) and l.istiny` | 
| Around the left lava room platform | 4 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.advanced_platforming)) and l.istiny` | 
| Around Instrument Pad | 5 |  | 
| Near Tag Barrel | 3 |  | 
| Matching Game Room Vines | 2 | `((l.grape and l.islanky) or l.phasewalk) and l.can_use_vines` | 
## Aztec Tiny Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the torch in the starting area | 4 |  | 
| On frog ledge | 2 |  | 
| Around Lanky Pedestal | 8 |  | 
| On KONG Letters | 4 |  | 
| Underwater tunnels | 3 |  | 
| On Diddy's Guitar Pad | 1 | `l.CanSlamSwitch(Levels.AngryAztec, 1) and l.isdiddy and l.peanut` | 
| Around the Upper Lanky Pedestal | 4 |  | 
| Starting Corner (1) | 3 |  | 
| Starting Corner (2) | 3 |  | 
| Near Kong Cage | 5 |  | 

# Frantic Factory
## Frantic Factory
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near Portal | 4 |  | 
| Behind Lobby W1 | 2 |  | 
| Behind Lobby W2 | 2 |  | 
| On the Clock | 3 |  | 
| Around Lobby W3 | 3 |  | 
| Around the doorways in the Lobby | 4 |  | 
| Top window to Production Room | 3 |  | 
| Down Hatch | 3 |  | 
| Bottom of the Hatch Pole | 3 |  | 
| Corner of tunnel to Production Room | 3 |  | 
| On low boxes in lower Production Room | 4 |  | 
| On a pipe in lower Production Room | 3 |  | 
| On the spinning section in Lower Production Room | 4 | `l.climbing` | 
| On the boxes at the top of production Room | 2 |  | 
| Around the production room Simian Spring pad | 4 |  | 
| On various boxes around Production Room | 4 |  | 
| On the archway to Storage Room | 3 |  | 
| Around the BBlast pad | 4 |  | 
| Inbetween the storage room boxes | 2 |  | 
| Behind a storage room box | 1 |  | 
| On boxes near Cranky's Lab | 3 |  | 
| On boxes near Candy's Music Shop | 2 |  | 
| Behind some boxes near Cranky's | 1 |  | 
| Around the top of the pole to Arcade | 6 |  | 
| Arcade Room Poles | 4 |  | 
| On top of the Arcade Machine | 2 |  | 
| Snide Window | 3 |  | 
| Above the pole to Block Tower Room | 6 |  | 
| Behind some elevator blocks (1) | 3 |  | 
| On a box in Testing Room | 2 |  | 
| On some boxes near Funky's | 3 |  | 
| On block tower (1) | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy)` | 
| On block tower (2) | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy)` | 
| Near dartboard entry | 5 |  | 
| In Dartboard Mini Tunnel | 2 | `(l.istiny and l.mini) or l.phasewalk` | 
| In Dartboard Room | 4 | `(l.istiny and l.mini) or l.phasewalk` | 
| On the archway to R&D | 3 | `(l.balloon or l.advanced_platforming) and l.islanky` | 
| On the number game board | 4 |  | 
| Behind some elevator blocks (2) | 3 |  | 
| Around a light in R&D | 3 |  | 
| On a ledge in R&D | 4 |  | 
| In Piano Room | 3 | `(l.trombone and l.islanky) or l.CanAccessRNDRoom()` | 
| In Diddy R&D Room | 3 | `(l.guitar and l.isdiddy) or l.CanAccessRNDRoom()` | 
| In Chunky R&D Room | 4 | `(l.punch and l.triangle and l.ischunky) or l.CanAccessRNDRoom()` | 
| In Car Race Lobby | 6 |  | 
| On Power Shed Platform | 5 |  | 
| On spring small ledge | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy) or l.phasewalk` | 
| Around Snide's HQ W3 | 3 |  | 
| On steps near Block Tower | 3 |  | 
| Outside R&D Window | 3 |  | 
| Around Storage W1 | 5 |  | 
| Lower Production Room Window | 3 |  | 
| Above chute to Power Shed | 5 |  | 
| Around Hatch | 5 |  | 
| Around Tiny's Kasplat | 5 |  | 
| Around pole to Block Tower Room | 5 |  | 
| Above pole to Snide's HQ | 5 |  | 
| Around high W4 | 5 |  | 
| Below pole to R&D | 5 |  | 
| Above pole to R&D | 5 |  | 
| On elevators to upper production room | 2 |  | 
| On elevators to upper production room | 1 |  | 
| Behind a box in Block Tower room | 4 |  | 
| Alcoves in Block Tower Room | 4 |  | 
| Around the spinning section in Production Room | 4 |  | 
| Under a grate in R&D | 4 | `(l.grab and l.donkey) or l.CanAccessRNDRoom()` | 
| Near Number Game | 3 |  | 
| Around Arcade Tunnel Bonus | 3 | `(l.punch and l.ischunky) or l.phasewalk` | 
| On boxes to Candy and Cranky | 3 |  | 
| Near Tiny Twirl Bonus | 3 | `l.istiny and l.twirl` | 
## Factory Tiny Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In Car Race | 3 |  | 
## Factory Crusher
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the Crusher Room near the GB | 4 | `(l.strongKong and l.isdonkey) or l.generalclips` | 
| Crusher Start | 3 |  | 
## Factory Power Hut
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Power Hut | 3 |  | 
| On top of doorway | 1 |  | 

# Gloomy Galleon
## Gloomy Galleon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of Lanky Slam Switch | 3 |  | 
| Around near W1 | 4 |  | 
| Around near W2 | 4 |  | 
| On top of GB Chest | 3 |  | 
| On top of headphones chest | 3 |  | 
| On top of fairy chest | 3 |  | 
| Around crossroads tag barrel | 4 |  | 
| On broken ship near Cranky's | 5 |  | 
| On Broken Ship railings | 6 |  | 
| Around Tiny's Kasplat | 6 |  | 
| Around the T&S Portal near Cranky | 2 |  | 
| Underneath Cranky's | 5 | `(l.punch and l.chunky) or l.phasewalk or l.CanSkew(False)` | 
| In the corner of the main room | 3 |  | 
| Near Tiny's Slam Switch | 3 |  | 
| Around 5-Door Ship Exterior | 4 |  | 
| Above W4 Platform | 4 |  | 
| Near the 2-Door Ship | 2 |  | 
| Above Candy's Platform | 4 |  | 
| Seal Race Entrance | 2 | `Events.WaterRaised in l.Events` | 
| Mech Fish Grate | 4 |  | 
| Near BBlast Pad | 4 |  | 
| Around DK's slam switch | 4 |  | 
| Around Lighthouse W5 | 4 |  | 
| Snide Alcove Edge | 5 |  | 
| Blueprint Water Alcove | 5 |  | 
| Lighthouse Underwater corner (Circle) | 3 |  | 
| Lighthouse Underwater corner (Stack) | 4 |  | 
| Mermaid Palace Roof | 2 |  | 
| On Mermaid Palace Shells | 5 |  | 
| Behind Enguarde Door | 3 | `Events.LighthouseEnguarde in l.Events or l.CanPhaseswim()` | 
| On Rafter near Funky's | 4 | `Events.WaterRaised in l.Events or l.CanMoonkick()` | 
| Around Cranky's Lab | 5 |  | 
| Tunnel to Chests Area | 3 |  | 
| Around Cactus | 4 |  | 
| On Seal Cage | 3 | `l.jetpack and l.isdiddy` | 
| Around Lighthouse W1 | 3 |  | 
| Behind Cannon Game Room gate | 3 |  | 
| Under Lighthouse Enguarde Crate | 3 |  | 
| Cannon Game Room Corner | 3 |  | 
| Inside Shipyard Chest (1) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (2) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (3) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (4) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Around Cactus Top | 5 |  | 
| Under Mermaid Tag Barrel | 5 |  | 
| Down the deep hole | 3 |  | 
## Galleon Sick Bay
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the Cannon | 1 |  | 
| In the corner before the grate | 3 |  | 
| On Barrels near the spinning totem | 3 | `(l.punch and l.ischunky) or l.phasewalk` | 
## Galleon Lighthouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Lighthouse Entry | 4 |  | 
| Lighthouse Climb (1) | 3 | `l.climbing` | 
| Lighthouse Climb (2) | 3 | `l.climbing` | 
| Top of Lighthouse | 2 | `l.climbing` | 
## Galleon Mechafish
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near Pillars | 6 |  | 
## Galleon Mermaid Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On fork in Mermaid Room | 1 |  | 
| In the corner | 3 |  | 
## Galleon Seal Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Seal Race Start | 2 |  | 
## Galleon5DShip Diddy Lanky Chunky
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Above Diddy Cannons | 2 |  | 
| On Diddy Barrel | 2 |  | 
| On Lanky Barrel | 2 |  | 
| On Lanky Bench | 2 |  | 
| Near Chunky Boxes | 3 |  | 
| Under Lanky Bench | 3 |  | 
| Near Chunky Treasure Chest | 3 |  | 
## Galleon5DShip DKTiny
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of DK Bonus Room | 3 |  | 
| Bed in DK Ship | 3 |  | 
| On boxes near bed | 2 |  | 
| At a dead end | 3 |  | 
## Galleon2DShip
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of Tiny Entrance | 3 |  | 
| Corners of Tiny's Main Room | 3 |  | 
| Start of Lanky's Room | 2 |  | 
| In various chests | 4 |  | 
## Galleon Submarine
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the desk | 3 |  | 
| In the corner | 3 |  | 
## Galleon Treasure Chest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the keyhole | 4 |  | 
| On the coin floor | 4 |  | 
## Galleon Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the Baboon Blast Course | 2 |  | 

# Fungi Forest
## Fungi Forest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Left of Green Tunnel | 3 |  | 
| Around apple dropoff zone | 6 |  | 
| Right of blue tunnel entry | 3 |  | 
| Around well stump | 4 |  | 
| On well roof edges | 3 | `(l.climbing and (l.can_use_vines or l.CanMoonkick())) or (l.jetpack and l.isdiddy)` | 
| Mushroom Stem | 4 | `l.climbing` | 
| On Clock Pendulum | 3 | `l.climbing` | 
| On Clock Torches | 2 |  | 
| Level Entry | 3 |  | 
| On bouncy mushroom in clock area | 3 |  | 
| Left of pink tunnel | 1 |  | 
| Near bouncy mushroom tag in the Giant Mushroom area | 3 |  | 
| Around a torch in the outer Giant Mushroom area | 3 |  | 
| Above a patch of grass in the Giant Mushroom area | 3 |  | 
| On the pink tunnel rim on the Giant Mushroom side | 3 | `l.jetpack and l.isdiddy` | 
| Behind the lowest ladder in the Giant Mushroom area | 2 |  | 
| Around the lower platform in the Giant Mushroom Area | 6 |  | 
| Behind the second lowest ladder in the Giant Mushroom Area | 2 | `l.climbing` | 
| Above the second lowest ladder in the Giant Mushroom Area | 2 |  | 
| On the entryways to the 3 top rooms in the Giant Mushroom Area | 3 |  | 
| On the Giant Mushroom top | 12 | `(l.jetpack and l.isdiddy) or (l.islanky and l.handstand)` | 
| On the Rabbit Race roof | 5 |  | 
| Around the Saxophone pad | 4 |  | 
| On the stump at the start of the hollow tree area | 2 |  | 
| Around the shop in the Worm area | 4 |  | 
| Beanstalk Fence | 4 |  | 
| On the Green Tunnel Roof | 3 | `l.twirl and l.istiny` | 
| On a mushroom in the Worm Area | 4 |  | 
| On the waterwheel | 5 |  | 
| In the Snide's area | 4 | `(l.TimeAccess(Regions.MillArea, Time.Day))` | 
| Near the entrance to the Dark Rafters | 4 |  | 
| Hanging off the mill roof | 3 |  | 
| In front of the mill in the air | 3 | `l.balloon and l.islanky` | 
| Behind the well exit | 3 |  | 
| Near the thornvine barn | 3 |  | 
| On Thorny Hedge | 3 | `l.isdonkey and l.strongKong` | 
| Around BBlast Pad | 3 | `l.climbing` | 
| Behind Clock | 3 |  | 
| On Mushroom near Mill far tag | 3 |  | 
| Around Crown Pad | 3 |  | 
| Around Tiny Kasplat | 5 |  | 
| On Mushroom near Dark Rafters Barn | 3 |  | 
| Behind Giant Mushroom | 3 |  | 
| Under Hollow Tree | 3 |  | 
| On Well | 3 | `((l.can_use_vines or l.CanMoonkick()) and l.climbing) or (l.jetpack and l.isdiddy)` | 
| On Archway to Giant Mushroom Area | 3 | `(l.twirl and l.istiny) or l.advanced_platforming` | 
| Inside Hollow Tree night fence | 4 | `l.jetpack and l.isdiddy and l.TimeAccess(Regions.HollowTreeArea, Time.Night)` | 
| Near Beanstalk Mini Monkey Barrel | 3 |  | 
| On Mushroom near Mill Well Exit | 3 |  | 
| Behind Night Door in the Apple Area | 3 | `l.TimeAccess(Regions.WormArea, Time.Night)` | 
| On switch to face puzzle | 3 |  | 
| Behind Well Entrance | 3 |  | 
## Forest Anthill
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the cannon | 4 |  | 
## Forest Winch Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On flour bags | 3 |  | 
| Near the winch machine | 2 |  | 
## Forest Rafters
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the torch at the start | 1 |  | 
| On various rafters | 4 | `l.guitar and l.isdiddy` | 
## Forest Thornvine Barn
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the fence | 3 |  | 
| Behind some boxes | 3 |  | 
| Inside the trough | 3 |  | 
## Forest Mill Front
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the levers | 3 | `l.isdonkey and (l.CanSlamSwitch(Levels.FungiForest, 2) or l.phasewalk or l.generalclips)` | 
| In front of the keg painting | 1 |  | 
| On support beams | 2 |  | 
| In the corner near the tag barrel | 3 |  | 
| In front of the Mini Monkey Hole | 3 |  | 
## Forest Giant Mushroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| At the bottom of ramps | 4 |  | 
| At the dead ends at the bottom | 2 |  | 
| Under a pathway | 3 |  | 
## Forest Mill Attic
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the starting box | 2 |  | 
| Behind a box | 3 |  | 
## Forest Lanky Zingers Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the shadows | 3 |  | 
## Forest Mill Back
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the question mark box | 4 |  | 
| Inside a keg | 1 | `l.barrels` | 
| On boxes near spider | 3 |  | 
| On various boxes | 3 |  | 

# Crystal Caves
## Crystal Caves
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near the DK Portal | 4 |  | 
| Crystal near level entry | 3 |  | 
| Behind the first ice wall | 2 | `(l.punch and l.chunky) or l.phasewalk or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)` | 
| Around the lower thick pillar near Ice Castle | 5 |  | 
| Around Ice Castle Tag | 6 |  | 
| Ice Castle Battlements (1) | 4 | `l.isdiddy or (l.islanky and (l.balloon or l.advanced_platforming)) or l.istiny` | 
| Ice Castle Battlements (2) | 4 | `l.isdiddy or (l.islanky and (l.balloon or l.advanced_platforming)) or l.istiny` | 
| On stumps near Ice Castle | 3 |  | 
| Near the small boulder | 4 |  | 
| Under the bridge near the small boulder | 2 | `l.jetpack and l.isdiddy` | 
| Near DK's Kasplat | 4 |  | 
| Hanging off the ledge near Blueprint Cave | 6 |  | 
| Fences near Ice Castle | 4 |  | 
| Steps up to Cranky's Lab | 3 |  | 
| Around Giant Boulder Shield | 8 |  | 
| On a stalagmite | 1 |  | 
| Around a pillar in the boulder cave | 4 |  | 
| On a stalagmite in the bonus cave | 1 |  | 
| Around the entrance to the bonus cave | 4 |  | 
| On the 5-Door Igloo (Entrances) | 5 |  | 
| On the 5-Door Igloo (Center) | 6 |  | 
| Around the thin bananaport pillar | 4 |  | 
| Around the thick bananaport pillar | 4 |  | 
| On boxes near the 5-Door Cabin (1) | 3 |  | 
| On boxes near the 5-Door Cabin (2) | 3 |  | 
| Near the waterfall | 5 |  | 
| On the doorway to Rotating Room | 2 |  | 
| Outside the Sprint Cabin | 3 |  | 
| Near the Sprint Cabin Headphones | 5 |  | 
| On stalactite in the Giant Kosha area | 2 |  | 
| Back of Bonus Cave | 5 | `Events.CavesW3bTagged in l.Events` | 
| Gorilla Gone Cavern | 3 | `(l.punch and l.chunky) or l.phasewalk or l.CanPhaseswim() or l.checkBarrier(RemovedBarriersSelected.caves_ice_walls)` | 
| Giant Boulder Cavern | 3 |  | 
| Giant Kosha Room | 3 |  | 
| In Snide's Cavern | 3 |  | 
| On Ice Castle | 4 | `((l.balloon or l.advanced_platforming) and l.islanky) or l.isdiddy or l.istiny` | 
| Near Cabin Waterfall | 3 |  | 
| Behind Igloo Tag Barrel | 3 |  | 
| On Slope to Cranky | 3 |  | 
| Behind Spike near Igloo Area | 3 |  | 
| Near Headphones | 3 |  | 
| In water near Funky's | 3 |  | 
| Pillar near Ice Castle | 2 | `(l.isdiddy and l.jetpack) or (l.istiny and l.twirl)` | 
| Behind Caves Igloo W1 | 3 |  | 
| Entrance to Blueprint Cave | 3 |  | 
## Caves Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the path to the first hoop | 3 |  | 
| In Baboon Blast Course | 3 |  | 
## Caves Lanky Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the torches at the start of the beetle race | 3 |  | 
| In the window in the Caves Beetle Race | 1 |  | 
## Caves Frozen Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near the Ice Tomato chair | 2 |  | 
| On Board | 2 |  | 
## Caves Chunky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Chunky Igloo TNT | 1 |  | 
## Caves Diddy Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the barrels in Diddy Igloo | 6 |  | 
## Caves Donkey Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| At the back of Donkey Igloo | 4 |  | 
## Caves Lanky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On some platforms in Lanky Igloo | 2 |  | 
## Caves Tiny Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the swords in Tiny Igloo | 2 |  | 
## Caves Lanky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near books in Lanky Cabin | 2 |  | 
## Caves Rotating Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the corners of Rotating Room | 4 |  | 
## Caves Chunky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the targets in Chunky Cabin | 3 |  | 
## Caves Diddy Lower Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the corners of the center platform in Diddy Lower Cabin | 4 | `l.jetpack or l.advanced_platforming` | 
| In Corner Platforms | 4 | `l.jetpack or l.advanced_platforming` | 
## Caves Diddy Upper Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In front of the pictures in Diddy Upper Cabin | 3 | `l.jetpack and (l.guitar or l.oranges) and l.isdiddy and (l.spring or l.CanMoontail())` | 
## Caves Donkey Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In between the holes in Donkey Cabin | 3 |  | 
| Above holes | 2 |  | 
## Caves Tiny Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around Tiny Cabin Interior | 3 |  | 

# Creepy Castle
## Creepy Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near DK Portal | 4 |  | 
| Starting pool | 3 |  | 
| Near Low Tag Barrel | 4 |  | 
| High tree at the back of Castle | 4 | `l.climbing` | 
| Above a gravestone near lower tunnel entry | 3 |  | 
| Outside lower tunnel entry | 4 |  | 
| Above retracting platforms | 2 |  | 
| On a post near the upper tunnel rear entry | 3 | `l.jetpack and l.isdiddy` | 
| On a series of posts near upper Warp 2 | 4 |  | 
| Near the wobbly bridge near upper Warp 2 | 2 |  | 
| Hanging off the edge near Cranky's | 4 |  | 
| Near Museum Entrance | 2 |  | 
| Near Trash Can | 2 |  | 
| On the library cloud | 3 |  | 
| Around the edge near Library entrance | 8 |  | 
| Top of Castle | 2 |  | 
| Under Museum Entrance Platform | 2 |  | 
| Outside Greenhouse | 3 |  | 
| Around Castle Tree exterior | 3 | `l.jetpack and l.isdiddy` | 
| Around Tiny Kasplat | 3 |  | 
| Around upper W2 | 3 |  | 
| On thin tree near the Tree entrance | 2 | `l.climbing` | 
| Behind Grave (1) | 3 |  | 
| Hanging off ledge near Castle Tree entrance | 3 |  | 
| Behind Grave (2) | 3 |  | 
| On tree near Crypt Entrance | 2 | `l.climbing` | 
| On Drawbridge | 4 | `l.jetpack and l.isdiddy` | 
| Above Window | 2 | `l.jetpack and l.isdiddy` | 
## Castle Ballroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Ballroom Wall Torches | 2 |  | 
| Ballroom Post Torches | 4 |  | 
| Around the tiled Ballroom floor | 4 |  | 
| Ballroom K. Rool Banners | 6 | `l.jetpack and l.isdiddy` | 
| Around Monkeyport Pad | 3 |  | 
## Castle Dungeon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Dungeon Buckets | 3 |  | 
| Dungeon - Behind Gate (1) | 2 | `l.punch and l.chunky or l.phasewalk` | 
| Dungeon - Behind Gate (2) | 2 | `l.punch and l.chunky or l.phasewalk` | 
| Dungeon - Behind Gate (3) | 2 | `l.punch and l.chunky or l.phasewalk` | 
| Donkey's Dungeon Room | 4 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.phasewalk` | 
| Diddy's Dungeon Room | 4 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.scope and l.peanut and l.can_use_vines` | 
| Around Donkey Switch | 4 |  | 
| Inside punchable grate | 3 | `(l.punch and l.chunky) or l.phasewalk` | 
| Above the acid in Lanky's Room | 3 | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.phasewalk) and l.islanky and l.trombone and l.balloon` | 
## Castle Shed
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Shed Interior Corners | 4 |  | 
| Around punch box | 4 |  | 
## Castle Lower Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Lower Cave hallway start | 4 |  | 
| Lower Cave Melon Crate | 4 |  | 
| Lower Cave Torch Pillar | 1 |  | 
| Near Funky | 2 |  | 
| Near Crypt Entrance | 4 |  | 
| On Crypt Skull | 1 |  | 
| Around the mausoleum entrance | 4 |  | 
| Near the Crypt Staircase | 3 |  | 
## Castle Crypt
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Wall Torch | 2 |  | 
| On Diddy Coffin | 4 | `(l.peanut or l.phasewalk or l.generalclips or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)) and l.isdiddy` | 
| On incorrect Minecart levers | 3 | `(l.coconut or l.phasewalk or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)) and l.isdonkey` | 
| Inside Chunky's Coffin | 4 | `(((l.pineapple or l.generalclips or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)) and l.Slam) or l.phasewalk) and l.ischunky` | 
| Inside Chunky Coffins | 3 | `((l.pineapple or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)) and l.ischunky and l.punch) or l.phasewalk or l.generalclips` | 
| Inside Diddy Coffins | 3 | `((l.peanut or l.checkBarrier(RemovedBarriersSelected.castle_crypt_doors)) and l.isdiddy and l.charge) or l.phasewalk or l.generalclips` | 
## Castle Mausoleum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Goo Hands | 6 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.istiny and l.twirl` | 
| Between Mausoleum Vines | 6 | `((l.grape and l.sprint) or l.generalclips or l.phasewalk) and l.islanky and l.trombone and l.can_use_vines` | 
| Around Tiny Slam Pad | 2 | `(l.twirl or (l.advanced_platforming and (not l.isKrushaAdjacent(Kongs.tiny))) or l.phasewalk) and l.istiny` | 
| Around Lanky Reward | 3 | `((l.grape and l.sprint) or l.generalclips or l.phasewalk) and ((l.trombone and l.can_use_vines) or l.advanced_platforming) and l.islanky` | 
## Castle Upper Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Tunnel behind torch | 3 |  | 
| Tunnel Rear Entry | 2 |  | 
| Over pit | 3 | `l.twirl and l.istiny` | 
| Near Candy's Shop | 3 |  | 
| Outside Dungeon Entrance | 3 |  | 
## Castle Greenhouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Greenhouse Exit Corner | 3 |  | 
| Greenhouse Dead End | 3 |  | 
| At a dead end | 3 |  | 
## Castle Library
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Library Wall Torch | 3 |  | 
| Library inside enemy gauntlet room | 4 |  | 
| Library Strong Kong Alcove | 2 |  | 
## Castle Museum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Museum around second skull | 7 |  | 
| Museum entryway to main room | 4 |  | 
| Car Race Building Chimney stack | 6 |  | 
| Car Race Second Chimney stack | 1 |  | 
| Around mystery Museum Pillar | 7 | `(l.monkeyport or l.phasewalk) and l.istiny` | 
| On mystery Museum Pillar | 3 | `(l.monkeyport or l.phasewalk) and l.istiny` | 
| In front of shields | 3 |  | 
## Castle Tower
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Wall Torches | 3 | `l.balloon and l.islanky` | 
## Castle Trash Can
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around trash can cheese | 3 |  | 
| Off the ledge of the trash can cheese | 3 |  | 
| On the long sides of the cheese | 2 |  | 
## Castle Tree
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Underwater in the DK Tree area | 4 | `l.swim and ((l.coconut) or l.generalclips or l.phasewalk) and l.isdonkey` | 
| In Chunky's Tree area | 4 | `(l.punch or l.phasewalk) and l.ischunky` | 
| On pathway to Chunky Bonus | 3 | `(l.punch or l.phasewalk) and l.ischunky` | 
## Castle Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Baboon Blast Course | 5 |  | 
