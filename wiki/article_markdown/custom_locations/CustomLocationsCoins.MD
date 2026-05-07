
# DK Isles
## Training Grounds
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around tree by training barrels | 4 | `self.logic = lambda _: True` | 
| On left treetop by Cranky's | 2 | `l.climbing` | 
| On right treetop by Cranky's | 2 | `l.climbing` | 
| On cliff top by Cranky's | 3 | `l.climbing` | 
| Bottom of the pool | 3 | `l.swim` | 
| Banana hoard | 4 | `(l.can_use_vines or l.CanMoonkick()) and l.climbing` | 
| Rear Tunnel | 3 | `self.logic = lambda _: True` | 
## Treehouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In tire in DK's house | 2 | `self.logic = lambda _: True` | 
| By the door in DK's house | 3 | `self.logic = lambda _: True` | 
## Isles
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On beach, in corner by path to Aztec lobby | 3 | `self.logic = lambda _: True` | 
| In water below waterfall | 5 | `l.swim` | 
| On top of tree between Japes Lobby and Fungi cannon | 3 | `l.climbing` | 
| On slope on path to Aztec lobby | 3 | `self.logic = lambda _: True` | 
| At the bottom of Aztec steps | 5 | `self.logic = lambda _: True` | 
| In little alcove in DK's ear in front of Aztec lobby | 3 | `self.logic = lambda _: True` | 
| On top of Aztec lobby | 4 | `self.logic = lambda _: True` | 
| On top of K. Lumsy's prison | 4 | `( (l.hasMoveSwitchsanity(Switches.IslesMonkeyport) and ((l.istiny and l.twirl) or (l.settings.damage_amount != DamageAmount.ohko and not l.IsHardFallDamage()))) or ((l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events) and Events.IslesDiddyBarrelSpawn in l.Events and l.isdiddy and l.jetpack) or ( (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events) and ((l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey)) and l.settings.damage_amount != DamageAmount.ohko and not l.IsHardFallDamage()) or (l.istiny and l.twirl)) ) )` | 
| On top of Fungi lobby | 3 | `self.logic = lambda _: True` | 
| Hanging off the edge behind Fungi lobby | 3 | `self.logic = lambda _: True` | 
| Around palm tree on lone fairy island | 5 | `self.logic = lambda _: True` | 
| By main warps | 5 | `self.logic = lambda _: True` | 
| Back of Fairy Isle | 3 | `self.logic = lambda _: True` | 
| Back of Krem Isle, near propellors | 3 | `self.logic = lambda _: True` | 
| Behind pillar on path to Factory lobby | 3 | `self.logic = lambda _: True` | 
| Around pillar behind Factory lobby | 5 | `self.logic = lambda _: True` | 
| To the right of the staircase to Factory lobby | 3 | `self.logic = lambda _: True` | 
| Around Saxophone pad | 4 | `self.logic = lambda _: True` | 
## Banana Fairy Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On lilypads in front pools | 4 | `self.logic = lambda _: True` | 
| On lilypads in back pools | 4 | `self.logic = lambda _: True` | 
## Isles Snide Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| To the right of Snide's | 3 | `self.logic = lambda _: True` | 
| To the left of Snide's | 3 | `self.logic = lambda _: True` | 
## KLumsy
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around a candle to the left | 4 | `self.logic = lambda _: True` | 
| Around a candle to the right | 4 | `self.logic = lambda _: True` | 
## Jungle Japes Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to Japes lobby entrance | 3 | `self.logic = lambda _: True` | 
| Next to a torch on the left | 3 | `self.logic = lambda _: True` | 
## Angry Aztec Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the front pillar | 4 | `self.logic = lambda _: True` | 
| Around the back pillar | 4 | `self.logic = lambda _: True` | 
| On the left stairs | 3 | `self.logic = lambda _: True` | 
| In the back room (left) | 3 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| In the back room (right) | 3 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
## Frantic Factory Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In tag barrel corner | 3 | `self.logic = lambda _: True` | 
| On top level in corner | 3 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| On top level at the end | 3 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
## Gloomy Galleon Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In water on left side | 3 | `self.logic = lambda _: True` | 
| On left side | 3 | `self.logic = lambda _: True` | 
| On right side | 3 | `self.logic = lambda _: True` | 
| Around golden banana | 3 | `l.swim and ((l.mini and l.twirl and l.tiny and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.chunky) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
## Fungi Forest Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On wooden box | 3 | `self.logic = lambda _: True` | 
| On flour bag | 2 | `self.logic = lambda _: True` | 
| On metal box | 3 | `self.logic = lambda _: True` | 
| In corner by B. Locker | 3 | `self.logic = lambda _: True` | 
## Crystal Caves Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around blue switch | 4 | `self.logic = lambda _: True` | 
| Beyond wall to lava GB | 3 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Around Lanky blueprint room | 5 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Near left ledge | 3 | `self.logic = lambda _: True` | 
## Creepy Castle Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around entrance | 5 | `self.logic = lambda _: True` | 
| In alcove to the right | 2 | `self.logic = lambda _: True` | 
| In alcove to the left | 2 | `self.logic = lambda _: True` | 
| On top of center piece | 3 | `l.chunky and l.barrels and l.islanky and l.balloon` | 
| On wooden posts | 2 | `self.logic = lambda _: True` | 
## Hideout Helm Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around Gorilla Gone pad | 4 | `self.logic = lambda _: True` | 

# Jungle Japes
## Jungle Japes
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to the DK portal | 3 | `self.logic = lambda _: True` | 
| Next to the bush to the right | 3 | `self.logic = lambda _: True` | 
| Next to the bush to the left | 3 | `self.logic = lambda _: True` | 
| In the first tunnel to the left | 3 | `self.logic = lambda _: True` | 
| In the Diddy GB cave room around a torch | 3 | `self.logic = lambda _: True` | 
| In the first tunnel past peanut gate to the left | 3 | `self.logic = lambda _: True` | 
| Around far W1 | 3 | `self.logic = lambda _: True` | 
| Around low W2 | 3 | `self.logic = lambda _: True` | 
| Against wall near W1 and W2 | 3 | `self.logic = lambda _: True` | 
| Against wall between W1W2 and underground | 3 | `self.logic = lambda _: True` | 
| Around Chunky underground entrance | 4 | `self.logic = lambda _: True` | 
| In corner behind W3 beehive side | 3 | `self.logic = lambda _: True` | 
| Against wall across from DK's kasplat alcove | 3 | `self.logic = lambda _: True` | 
| Against wall across from Tiny's kasplat alcove | 3 | `self.logic = lambda _: True` | 
| In front of each feather switch | 2 | `self.logic = lambda _: True` | 
| Around W5 in beehive area | 4 | `self.logic = lambda _: True` | 
| On left log in beehive area | 5 | `self.logic = lambda _: True` | 
| On right log in beehive area | 5 | `self.logic = lambda _: True` | 
| To the right of the beehive | 3 | `self.logic = lambda _: True` | 
| To the left of the beehive | 3 | `self.logic = lambda _: True` | 
| Beehive area around front big tree | 4 | `self.logic = lambda _: True` | 
| Beehive area around left big tree | 4 | `self.logic = lambda _: True` | 
| Beehive area around back big tree | 4 | `self.logic = lambda _: True` | 
| Beehive area around right big tree | 4 | `self.logic = lambda _: True` | 
| On riverbed near tag barrel | 3 | `l.swim` | 
| In front of Tiny's caged GB | 3 | `self.logic = lambda _: True` | 
| Against wall to the right near Painting room | 3 | `self.logic = lambda _: True` | 
| In corner behind W3 painting room side | 3 | `self.logic = lambda _: True` | 
| Around middle tree tag barrel side | 4 | `self.logic = lambda _: True` | 
| In front of Diddy's caged GB | 3 | `self.logic = lambda _: True` | 
| Around tree in front of Snide's | 4 | `self.logic = lambda _: True` | 
| In front of Chunky's caged GB | 3 | `self.logic = lambda _: True` | 
| On slope between Snide's and mountain | 5 | `self.logic = lambda _: True` | 
| Behind melon crate | 3 | `self.logic = lambda _: True` | 
| On slope between mountain and Diddy cage | 3 | `self.logic = lambda _: True` | 
| Around tree in front of Diddy's cage | 4 | `self.logic = lambda _: True` | 
| In front of T&S portal near Diddy kasplat | 3 | `self.logic = lambda _: True` | 
| In pit near Diddy kasplat | 3 | `self.logic = lambda _: True` | 
| Around tunnel W4 | 3 | `self.logic = lambda _: True` | 
| Around small torch in W4 tunnel | 4 | `self.logic = lambda _: True` | 
| Around small torch near Lanky kasplat | 3 | `self.logic = lambda _: True` | 
| Against right wall in Lanky kasplat room | 3 | `self.logic = lambda _: True` | 
| Against left wall in Lanky kasplat room | 3 | `self.logic = lambda _: True` | 
| On top of right slippery slope | 3 | `self.logic = lambda _: True` | 
| Around Tiny hut | 4 | `self.logic = lambda _: True` | 
| Around Lanky hut | 4 | `self.logic = lambda _: True` | 
| Around Donkey hut | 4 | `self.logic = lambda _: True` | 
| Around Diddy hut | 4 | `self.logic = lambda _: True` | 
| Around Cranky W4 | 3 | `self.logic = lambda _: True` | 
| Around far tree in Cranky area | 4 | `self.logic = lambda _: True` | 
| In front of Rambi gate | 4 | `self.logic = lambda _: True` | 
| Around melon crate in boulder room | 3 | `self.logic = lambda _: True` | 
| Around torch near fairy room | 3 | `self.logic = lambda _: True` | 
| Around torch in fairy room | 3 | `self.logic = lambda _: True` | 
| Left side of fairy room | 4 | `self.logic = lambda _: True` | 
| Right side of fairy room | 3 | `self.logic = lambda _: True` | 
| Around torch in the middle of fairy room on water surface | 4 | `self.logic = lambda _: True` | 
| Near entrance portal | 3 | `self.logic = lambda _: True` | 
| Main Area Underwater (1) | 3 | `l.swim` | 
| Around the Baboon Blast Pad | 3 | `self.logic = lambda _: True` | 
| Start of first tunnel | 3 | `self.logic = lambda _: True` | 
| Diddy Cavern (1) | 3 | `self.logic = lambda _: True` | 
| Fairy Pool | 5 | `l.swim` | 
| Near Rambi Box | 3 | `l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.CanPhase()` | 
| Diddy Cavern (2) | 3 | `self.logic = lambda _: True` | 
| Near Diddy Kasplat | 3 | `self.logic = lambda _: True` | 
| Near Tiny Kasplat | 3 | `self.logic = lambda _: True` | 
| In between the vines near Diddy Kasplat | 1 | `l.can_use_vines` | 
| Near DK Kasplat | 3 | `self.logic = lambda _: True` | 
| Cannon Path | 2 | `self.logic = lambda _: True` | 
| Near Lanky Kasplat | 3 | `self.logic = lambda _: True` | 
| Main Area Underwater (2) | 2 | `l.swim` | 
| Main Area Underwater (3) | 3 | `l.swim` | 
| Behind the stump | 3 | `self.logic = lambda _: True` | 
| On top of the mountain | 5 | `self.logic = lambda _: True` | 
| Near Snide's HQ | 5 | `self.logic = lambda _: True` | 
## Japes Under Ground
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Right side towards the end of the cave | 3 | `self.logic = lambda _: True` | 
| Left side towards the end of the cave | 3 | `self.logic = lambda _: True` | 
| Around center platform | 3 | `self.logic = lambda _: True` | 
| Behind Entrance Cannon | 3 | `self.logic = lambda _: True` | 
| Near Underground Reward | 3 | `(l.can_use_vines and l.pineapple and l.ischunky) or l.CanPhase()` | 
## Japes Lanky Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to entrance | 3 | `self.logic = lambda _: True` | 
| On Pegs | 2 | `self.logic = lambda _: True` | 
## Japes Mountain
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On right minecart near entrance | 3 | `self.logic = lambda _: True` | 
| In treadmills room front left corner | 2 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()` | 
| On coal pile in second room | 1 | `self.logic = lambda _: True` | 
| Behind a barrel near the HI-LO Machine | 1 | `(l.charge and l.isdiddy) or l.CanPhase()` | 
| Under the Conveyors | 1 | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and l.isdiddy) or l.CanPhase()` | 
| On the bridge | 1 | `l.peanut or l.monkey_maneuvers` | 
| On a coal stack | 1 | `self.logic = lambda _: True` | 
## Japes Tiny Hive
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind Door 1 | 2 | `self.logic = lambda _: True` | 
| Around final room | 4 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase() or l.generalclips` | 
| Behind Door 2 | 2 | `((l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) or l.CanPhase() or l.generalclips) and l.istiny` | 
## Japes Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Between cannons in the Baboon Blast Course | 2 | `self.logic = lambda _: True` | 

# Angry Aztec
## Angry Aztec
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In front of Chunky vase room door | 3 | `self.logic = lambda _: True` | 
| In front of Donkey kasplat room door | 3 | `self.logic = lambda _: True` | 
| Left side across the sand from Candy's store | 3 | `self.logic = lambda _: True` | 
| Right side of Candy's store | 3 | `self.logic = lambda _: True` | 
| Next to quicksand close to llama cage | 3 | `self.logic = lambda _: True` | 
| On gentle slope of llama cage | 4 | `self.logic = lambda _: True` | 
| Around Oasis W1 | 3 | `self.logic = lambda _: True` | 
| Each side of Tiny Temple stairs | 4 | `self.logic = lambda _: True` | 
| Behind guitar door | 2 | `self.logic = lambda _: True` | 
| On boulder switch | 4 | `self.logic = lambda _: True` | 
| Right side of Cranky's | 2 | `self.logic = lambda _: True` | 
| Against wall near Chunky bonus GB | 3 | `self.logic = lambda _: True` | 
| In shady corner to the right of Llama temple | 3 | `self.logic = lambda _: True` | 
| Around W4 by other warps | 3 | `self.logic = lambda _: True` | 
| Around W3 by warps | 3 | `self.logic = lambda _: True` | 
| Around rocketbarrel | 4 | `self.logic = lambda _: True` | 
| By quicksand near tower | 3 | `self.logic = lambda _: True` | 
| Behind tower | 3 | `self.logic = lambda _: True` | 
| On ramps on stairs leading to tower | 4 | `self.logic = lambda _: True` | 
| Middle of Snide's platform | 3 | `self.logic = lambda _: True` | 
| On corner of path near Snide's tag barrel | 3 | `self.logic = lambda _: True` | 
| Left wall by Funky's | 4 | `self.logic = lambda _: True` | 
| Left corner near quicksand by Llama temple | 3 | `self.logic = lambda _: True` | 
| Left of Llama temple stairs | 3 | `self.logic = lambda _: True` | 
| Right of Llama temple stairs | 3 | `self.logic = lambda _: True` | 
| Front of 5 door temple | 3 | `self.logic = lambda _: True` | 
| Top of 5 door temple side stairs | 2 | `self.logic = lambda _: True` | 
| On roof of 5 door temple | 3 | `l.jetpack` | 
| On roof of Llama Temple | 4 | `l.jetpack` | 
| Around far W5 | 4 | `self.logic = lambda _: True` | 
| Near Cranky's Lab | 4 | `self.logic = lambda _: True` | 
| Outside Funky's | 5 | `self.logic = lambda _: True` | 
| Around Oasis Warp 2 | 5 | `self.logic = lambda _: True` | 
| Under Snide's HQ Tag Barrel | 3 | `self.logic = lambda _: True` | 
| On posts near Llama | 2 | `self.logic = lambda _: True` | 
| At the end of the quicksand tunnel | 4 | `self.logic = lambda _: True` | 
| Around the Giant Boulder | 3 | `self.logic = lambda _: True` | 
| Around the Bonus Barrel Cage | 4 | `self.logic = lambda _: True` | 
| Vines near Snide's HQ | 4 | `(l.can_use_vines and l.climbing) or (l.jetpack and l.isdiddy)` | 
| Around Hunky Chunky Barrel | 3 | `self.logic = lambda _: True` | 
| Behind 5-Door Temple | 3 | `self.logic = lambda _: True` | 
| Under Oasis Tag | 4 | `self.logic = lambda _: True` | 
| Around Totem W5 | 5 | `self.logic = lambda _: True` | 
| Around Tiny Temple | 4 | `self.logic = lambda _: True` | 
| Blueprint Cavern | 3 | `(l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) or l.CanPhase()) and ((l.strongKong and l.isdonkey) or (l.twirl and l.istiny))` | 
## Aztec Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Baboon Blast Course | 3 | `self.logic = lambda _: True` | 
## Aztec Chunky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| First Switch | 1 | `self.logic = lambda _: True` | 
| On torches | 2 | `self.logic = lambda _: True` | 
| On stairs | 3 | `self.logic = lambda _: True` | 
| Around the temple | 2 | `self.logic = lambda _: True` | 
| Around the temple | 2 | `(l.pineapple and l.ischunky) or l.CanPhase()` | 
## Aztec Diddy5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind some pillars | 3 | `(l.peanut and l.isdiddy) or l.CanPhase()` | 
| Behind some pillars | 1 | `self.logic = lambda _: True` | 
| Dead Ends | 1 | `(l.peanut and l.isdiddy) or l.CanPhase()` | 
| Dead Ends | 1 | `self.logic = lambda _: True` | 
## Aztec Donkey5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Final pathway | 4 | `(l.coconut and l.isdonkey) or l.CanPhase()` | 
| Near 2nd Switch | 2 | `(l.coconut and l.isdonkey) or l.CanPhase()` | 
## Aztec Lanky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Starting Staircase | 2 | `self.logic = lambda _: True` | 
| Final Corridors | 2 | `(l.grape and l.islanky) or l.CanPhase()` | 
## Aztec Tiny5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Fairy Side Room | 4 | `(l.istiny and l.mini) or l.CanPhase()` | 
| Other Side Room | 4 | `(l.istiny and l.mini) or l.CanPhase()` | 
| Under Feather Switches and at Dead Ends | 1 | `self.logic = lambda _: True` | 
| Under Feather Switches and at Dead Ends | 1 | `self.logic = lambda _: True` | 
| Under Feather Switches and at Dead Ends | 1 | `(l.feather and l.istiny) or l.CanPhase()` | 
## Aztec Llama Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Left Bannister | 5 | `self.logic = lambda _: True` | 
| Right Bannister | 5 | `self.logic = lambda _: True` | 
| Matching Game Room | 3 | `self.logic = lambda _: True` | 
| Around the right lava room platform | 4 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.monkey_maneuvers)) and l.istiny` | 
| Around the left lava room platform | 4 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.monkey_maneuvers)) and l.istiny` | 
| Around Instrument Pad | 5 | `self.logic = lambda _: True` | 
| Near Tag Barrel | 3 | `self.logic = lambda _: True` | 
| Matching Game Room Vines | 2 | `l.can_use_vines` | 
## Aztec Tiny Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the torch in the starting area | 4 | `self.logic = lambda _: True` | 
| Around Lanky Pedestal | 8 | `self.logic = lambda _: True` | 
| On KONG Letters | 4 | `self.logic = lambda _: True` | 
| Underwater tunnels | 3 | `self.logic = lambda _: True` | 
| On Diddy's Guitar Pad | 1 | `self.logic = lambda _: True` | 
| Around the Upper Lanky Pedestal | 4 | `self.logic = lambda _: True` | 
| Starting Corner (1) | 3 | `self.logic = lambda _: True` | 
| Starting Corner (2) | 3 | `self.logic = lambda _: True` | 
| Near Kong Cage | 5 | `self.logic = lambda _: True` | 

# Frantic Factory
## Frantic Factory
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near Portal | 4 | `self.logic = lambda _: True` | 
| Behind Lobby W1 | 2 | `self.logic = lambda _: True` | 
| Behind Lobby W2 | 2 | `self.logic = lambda _: True` | 
| On the Clock | 3 | `self.logic = lambda _: True` | 
| Around Lobby W3 | 3 | `self.logic = lambda _: True` | 
| Around the doorways in the Lobby | 4 | `self.logic = lambda _: True` | 
| Top window to Production Room | 3 | `self.logic = lambda _: True` | 
| Down Hatch | 3 | `self.logic = lambda _: True` | 
| Bottom of the Hatch Pole | 3 | `self.logic = lambda _: True` | 
| Corner of tunnel to Production Room | 3 | `self.logic = lambda _: True` | 
| On low boxes in lower Production Room | 4 | `self.logic = lambda _: True` | 
| On a pipe in lower Production Room | 3 | `self.logic = lambda _: True` | 
| On the spinning section in Lower Production Room | 4 | `l.climbing` | 
| On the boxes at the top of production Room | 2 | `self.logic = lambda _: True` | 
| Around the production room Simian Spring pad | 4 | `self.logic = lambda _: True` | 
| On various boxes around Production Room | 4 | `self.logic = lambda _: True` | 
| On the archway to Storage Room | 3 | `self.logic = lambda _: True` | 
| Around the BBlast pad | 4 | `self.logic = lambda _: True` | 
| Inbetween the storage room boxes | 2 | `self.logic = lambda _: True` | 
| Behind a storage room box | 1 | `self.logic = lambda _: True` | 
| On boxes near Cranky's Lab | 3 | `self.logic = lambda _: True` | 
| On boxes near Candy's Music Shop | 2 | `self.logic = lambda _: True` | 
| Behind some boxes near Cranky's | 1 | `self.logic = lambda _: True` | 
| Around the top of the pole to Arcade | 6 | `self.logic = lambda _: True` | 
| Arcade Room Poles | 4 | `self.logic = lambda _: True` | 
| On top of the Arcade Machine | 2 | `self.logic = lambda _: True` | 
| Snide Window | 3 | `self.logic = lambda _: True` | 
| Above the pole to Block Tower Room | 6 | `self.logic = lambda _: True` | 
| Behind some elevator blocks (1) | 3 | `self.logic = lambda _: True` | 
| On a box in Testing Room | 2 | `self.logic = lambda _: True` | 
| On some boxes near Funky's | 3 | `self.logic = lambda _: True` | 
| On block tower (1) | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy)` | 
| On block tower (2) | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy)` | 
| Near dartboard entry | 5 | `self.logic = lambda _: True` | 
| In Dartboard Mini Tunnel | 2 | `(l.istiny and l.mini) or l.CanPhase()` | 
| In Dartboard Room | 4 | `(l.istiny and l.mini) or l.CanPhase()` | 
| On the archway to R&D | 3 | `(l.balloon or l.monkey_maneuvers) and l.islanky` | 
| On the number game board | 4 | `self.logic = lambda _: True` | 
| Behind some elevator blocks (2) | 3 | `self.logic = lambda _: True` | 
| Around a light in R&D | 3 | `self.logic = lambda _: True` | 
| On a ledge in R&D | 4 | `self.logic = lambda _: True` | 
| In Piano Room | 3 | `(l.trombone and l.islanky) or l.CanAccessRNDRoom()` | 
| In Diddy R&D Room | 3 | `(l.guitar and l.isdiddy) or l.CanAccessRNDRoom()` | 
| In Chunky R&D Room | 4 | `(l.punch and l.triangle and l.ischunky) or l.CanAccessRNDRoom()` | 
| In Car Race Lobby | 6 | `self.logic = lambda _: True` | 
| On Power Shed Platform | 5 | `self.logic = lambda _: True` | 
| On spring small ledge | 3 | `((l.spring or l.CanMoontail()) and l.isdiddy) or l.CanPhase()` | 
| Around Snide's HQ W3 | 3 | `self.logic = lambda _: True` | 
| On steps near Block Tower | 3 | `self.logic = lambda _: True` | 
| Outside R&D Window | 3 | `self.logic = lambda _: True` | 
| Around Storage W1 | 5 | `self.logic = lambda _: True` | 
| Lower Production Room Window | 3 | `self.logic = lambda _: True` | 
| Above chute to Power Shed | 5 | `self.logic = lambda _: True` | 
| Around Hatch | 5 | `self.logic = lambda _: True` | 
| Around Tiny's Kasplat | 5 | `self.logic = lambda _: True` | 
| Around pole to Block Tower Room | 5 | `self.logic = lambda _: True` | 
| Above pole to Snide's HQ | 5 | `self.logic = lambda _: True` | 
| Around high W4 | 5 | `self.logic = lambda _: True` | 
| Below pole to R&D | 5 | `self.logic = lambda _: True` | 
| Above pole to R&D | 5 | `self.logic = lambda _: True` | 
| On elevators to upper production room | 2 | `self.logic = lambda _: True` | 
| On elevators to upper production room | 1 | `self.logic = lambda _: True` | 
| Behind a box in Block Tower room | 4 | `self.logic = lambda _: True` | 
| Alcoves in Block Tower Room | 4 | `logic=lambda _: True` | 
| Around the spinning section in Production Room | 4 | `self.logic = lambda _: True` | 
| Under a grate in R&D | 4 | `(l.grab and l.donkey) or l.CanAccessRNDRoom()` | 
| Near Number Game | 3 | `self.logic = lambda _: True` | 
| Around Arcade Tunnel Bonus | 3 | `(l.punch and l.ischunky) or l.CanPhase()` | 
| On boxes to Candy and Cranky | 3 | `self.logic = lambda _: True` | 
| Near Tiny Twirl Bonus | 3 | `l.istiny and l.twirl` | 
## Factory Tiny Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In Car Race | 3 | `self.logic = lambda _: True` | 
## Factory Crusher
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the Crusher Room near the GB | 4 | `(l.strongKong and l.isdonkey) or l.generalclips` | 
| Crusher Start | 3 | `self.logic = lambda _: True` | 
## Factory Power Hut
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Power Hut | 3 | `self.logic = lambda _: True` | 
| On top of doorway | 1 | `self.logic = lambda _: True` | 

# Gloomy Galleon
## Gloomy Galleon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of Lanky Slam Switch | 3 | `self.logic = lambda _: True` | 
| Around near W1 | 4 | `self.logic = lambda _: True` | 
| Around near W2 | 4 | `self.logic = lambda _: True` | 
| On top of GB Chest | 3 | `self.logic = lambda _: True` | 
| On top of headphones chest | 3 | `self.logic = lambda _: True` | 
| On top of fairy chest | 3 | `self.logic = lambda _: True` | 
| Around crossroads tag barrel | 4 | `self.logic = lambda _: True` | 
| On broken ship near Cranky's | 5 | `self.logic = lambda _: True` | 
| On Broken Ship railings | 6 | `self.logic = lambda _: True` | 
| Around Tiny's Kasplat | 6 | `self.logic = lambda _: True` | 
| Around the T&S Portal near Cranky | 2 | `self.logic = lambda _: True` | 
| Underneath Cranky's | 5 | `(l.punch and l.chunky) or l.CanPhase() or l.CanSkew(False, False)` | 
| In the corner of the main room | 3 | `self.logic = lambda _: True` | 
| Near Tiny's Slam Switch | 3 | `self.logic = lambda _: True` | 
| Around 5-Door Ship Exterior | 4 | `self.logic = lambda _: True` | 
| Above W4 Platform | 4 | `self.logic = lambda _: True` | 
| Near the 2-Door Ship | 2 | `self.logic = lambda _: True` | 
| Above Candy's Platform | 4 | `self.logic = lambda _: True` | 
| Seal Race Entrance | 2 | `Events.WaterRaised in l.Events` | 
| Mech Fish Grate | 4 | `self.logic = lambda _: True` | 
| Near BBlast Pad | 4 | `self.logic = lambda _: True` | 
| Around DK's slam switch | 4 | `self.logic = lambda _: True` | 
| Around Lighthouse W5 | 4 | `self.logic = lambda _: True` | 
| Snide Alcove Edge | 5 | `self.logic = lambda _: True` | 
| Blueprint Water Alcove | 5 | `self.logic = lambda _: True` | 
| Lighthouse Underwater corner (Circle) | 3 | `self.logic = lambda _: True` | 
| Lighthouse Underwater corner (Stack) | 4 | `logic=lambda _: True` | 
| Mermaid Palace Roof | 2 | `self.logic = lambda _: True` | 
| On Mermaid Palace Shells | 5 | `self.logic = lambda _: True` | 
| Behind Enguarde Door | 3 | `self.logic = lambda _: True` | 
| On Rafter near Funky's | 4 | `Events.WaterRaised in l.Events or l.CanMoonkick()` | 
| Around Cranky's Lab | 5 | `self.logic = lambda _: True` | 
| Tunnel to Chests Area | 3 | `self.logic = lambda _: True` | 
| Around Cactus | 4 | `self.logic = lambda _: True` | 
| On Seal Cage | 3 | `l.jetpack and l.isdiddy` | 
| Around Lighthouse W1 | 3 | `self.logic = lambda _: True` | 
| Behind Cannon Game Room gate | 3 | `self.logic = lambda _: True` | 
| Under Lighthouse Enguarde Crate | 3 | `self.logic = lambda _: True` | 
| Cannon Game Room Corner | 3 | `self.logic = lambda _: True` | 
| Inside Shipyard Chest (1) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (2) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (3) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Inside Shipyard Chest (4) | 3 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Around Cactus Top | 5 | `self.logic = lambda _: True` | 
| Under Mermaid Tag Barrel | 5 | `self.logic = lambda _: True` | 
| Down the deep hole | 3 | `self.logic = lambda _: True` | 
## Galleon Sick Bay
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the Cannon | 1 | `self.logic = lambda _: True` | 
| In the corner before the grate | 3 | `self.logic = lambda _: True` | 
| On Barrels near the spinning totem | 3 | `(l.punch and l.ischunky) or l.CanPhase()` | 
## Galleon Lighthouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Lighthouse Entry | 4 | `self.logic = lambda _: True` | 
| Lighthouse Climb (1) | 3 | `self.logic = lambda _: True` | 
| Lighthouse Climb (2) | 3 | `self.logic = lambda _: True` | 
| Top of Lighthouse | 2 | `self.logic = lambda _: True` | 
## Galleon Mechafish
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near Pillars | 6 | `self.logic = lambda _: True` | 
## Galleon Mermaid Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On fork in Mermaid Room | 1 | `self.logic = lambda _: True` | 
| In the corner | 3 | `self.logic = lambda _: True` | 
## Galleon Seal Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Seal Race Start | 2 | `self.logic = lambda _: True` | 
## Galleon5DShip Diddy Lanky Chunky
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Above Diddy Cannons | 2 | `self.logic = lambda _: True` | 
| On Diddy Barrel | 2 | `self.logic = lambda _: True` | 
| On Lanky Barrel | 2 | `self.logic = lambda _: True` | 
| On Lanky Bench | 2 | `self.logic = lambda _: True` | 
| Near Chunky Boxes | 3 | `self.logic = lambda _: True` | 
| Under Lanky Bench | 3 | `self.logic = lambda _: True` | 
| Near Chunky Treasure Chest | 3 | `self.logic = lambda _: True` | 
## Galleon5DShip DKTiny
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of DK Bonus Room | 3 | `self.logic = lambda _: True` | 
| Bed in DK Ship | 3 | `self.logic = lambda _: True` | 
| On boxes near bed | 2 | `self.logic = lambda _: True` | 
| At a dead end | 3 | `self.logic = lambda _: True` | 
## Galleon2DShip
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Corner of Tiny Entrance | 3 | `self.logic = lambda _: True` | 
| Corners of Tiny's Main Room | 3 | `self.logic = lambda _: True` | 
| Start of Lanky's Room | 2 | `self.logic = lambda _: True` | 
| In various chests | 4 | `self.logic = lambda _: True` | 
## Galleon Submarine
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the desk | 3 | `self.logic = lambda _: True` | 
| In the corner | 3 | `self.logic = lambda _: True` | 
## Galleon Treasure Chest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the keyhole | 4 | `self.logic = lambda _: True` | 
| On the coin floor | 4 | `self.logic = lambda _: True` | 
## Galleon Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the Baboon Blast Course | 2 | `self.logic = lambda _: True` | 

# Fungi Forest
## Fungi Forest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Left of Green Tunnel | 3 | `self.logic = lambda _: True` | 
| Around apple dropoff zone | 6 | `self.logic = lambda _: True` | 
| Right of blue tunnel entry | 3 | `self.logic = lambda _: True` | 
| Around well stump | 4 | `self.logic = lambda _: True` | 
| On well roof edges | 3 | `(l.climbing and (l.can_use_vines or l.CanMoonkick())) or (l.jetpack and l.isdiddy)` | 
| Mushroom Stem | 4 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On Clock Pendulum | 3 | `l.climbing` | 
| On Clock Torches | 2 | `self.logic = lambda _: True` | 
| Level Entry | 3 | `self.logic = lambda _: True` | 
| On bouncy mushroom in clock area | 3 | `self.logic = lambda _: True` | 
| Left of pink tunnel | 1 | `self.logic = lambda _: True` | 
| Near bouncy mushroom tag in the Giant Mushroom area | 3 | `self.logic = lambda _: True` | 
| Around a torch in the outer Giant Mushroom area | 3 | `self.logic = lambda _: True` | 
| Above a patch of grass in the Giant Mushroom area | 3 | `self.logic = lambda _: True` | 
| On the pink tunnel rim on the Giant Mushroom side | 3 | `l.jetpack and l.isdiddy` | 
| Behind the lowest ladder in the Giant Mushroom area | 2 | `self.logic = lambda _: True` | 
| Around the lower platform in the Giant Mushroom Area | 6 | `self.logic = lambda _: True` | 
| Behind the second lowest ladder in the Giant Mushroom Area | 2 | `self.logic = lambda _: True` | 
| Above the second lowest ladder in the Giant Mushroom Area | 2 | `self.logic = lambda _: True` | 
| On the entryways to the 3 top rooms in the Giant Mushroom Area | 3 | `self.logic = lambda _: True` | 
| On the Giant Mushroom top | 12 | `logic=lambda _: True` | 
| On the Rabbit Race roof | 5 | `self.logic = lambda _: True` | 
| Around the Saxophone pad | 4 | `self.logic = lambda _: True` | 
| On the stump at the start of the hollow tree area | 2 | `self.logic = lambda _: True` | 
| Around the shop in the Worm area | 4 | `self.logic = lambda _: True` | 
| Beanstalk Fence | 4 | `self.logic = lambda _: True` | 
| On the Green Tunnel Roof | 3 | `l.twirl and l.istiny` | 
| On a mushroom in the Worm Area | 4 | `self.logic = lambda _: True` | 
| On the waterwheel | 5 | `self.logic = lambda _: True` | 
| In the Snide's area | 4 | `(l.TimeAccess(Regions.MillArea, Time.Day))` | 
| Near the entrance to the Dark Rafters | 4 | `self.logic = lambda _: True` | 
| Hanging off the mill roof | 3 | `self.logic = lambda _: True` | 
| In front of the mill in the air | 3 | `l.balloon and l.islanky` | 
| Behind the well exit | 3 | `self.logic = lambda _: True` | 
| Near the thornvine barn | 3 | `self.logic = lambda _: True` | 
| On Thorny Hedge | 3 | `l.isdonkey and l.strongKong` | 
| Around BBlast Pad | 3 | `self.logic = lambda _: True` | 
| Behind Clock | 3 | `self.logic = lambda _: True` | 
| On Mushroom near Mill far tag | 3 | `l.climbing` | 
| Around Crown Pad | 3 | `self.logic = lambda _: True` | 
| Around Tiny Kasplat | 5 | `self.logic = lambda _: True` | 
| On Mushroom near Dark Rafters Barn | 3 | `l.climbing` | 
| Behind Giant Mushroom | 3 | `self.logic = lambda _: True` | 
| Under Hollow Tree | 3 | `self.logic = lambda _: True` | 
| On Well | 3 | `((l.can_use_vines or l.CanMoonkick()) and l.climbing) or (l.jetpack and l.isdiddy)` | 
| On Archway to Giant Mushroom Area | 3 | `(l.twirl and l.istiny) or l.monkey_maneuvers` | 
| Inside Hollow Tree night fence | 4 | `l.jetpack and l.isdiddy and l.TimeAccess(Regions.HollowTreeArea, Time.Night)` | 
| Near Beanstalk Mini Monkey Barrel | 3 | `self.logic = lambda _: True` | 
| On Mushroom near Mill Well Exit | 3 | `l.climbing` | 
| Behind Night Door in the Apple Area | 3 | `l.TimeAccess(Regions.WormArea, Time.Night)` | 
| On switch to face puzzle | 3 | `self.logic = lambda _: True` | 
| Behind Well Entrance | 3 | `self.logic = lambda _: True` | 
## Forest Anthill
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the cannon | 4 | `self.logic = lambda _: True` | 
## Forest Winch Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On flour bags | 3 | `self.logic = lambda _: True` | 
| Near the winch machine | 2 | `self.logic = lambda _: True` | 
## Forest Rafters
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the torch at the start | 1 | `self.logic = lambda _: True` | 
| On various rafters | 4 | `l.guitar and l.isdiddy` | 
## Forest Thornvine Barn
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the fence | 3 | `self.logic = lambda _: True` | 
| Behind some boxes | 3 | `self.logic = lambda _: True` | 
| Inside the trough | 3 | `self.logic = lambda _: True` | 
## Forest Mill Front
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the levers | 3 | `l.isdonkey and (l.CanSlamSwitch(Levels.FungiForest, 2) or l.CanPhase() or l.generalclips)` | 
| In front of the keg painting | 1 | `self.logic = lambda _: True` | 
| On support beams | 2 | `self.logic = lambda _: True` | 
| In the corner near the tag barrel | 3 | `self.logic = lambda _: True` | 
| In front of the Mini Monkey Hole | 3 | `self.logic = lambda _: True` | 
## Forest Giant Mushroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| At the bottom of ramps | 4 | `self.logic = lambda _: True` | 
| At the dead ends at the bottom | 2 | `self.logic = lambda _: True` | 
| Under a pathway | 3 | `self.logic = lambda _: True` | 
## Forest Mill Attic
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind the starting box | 2 | `self.logic = lambda _: True` | 
| Behind a box | 3 | `self.logic = lambda _: True` | 
## Forest Lanky Zingers Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the shadows | 3 | `self.logic = lambda _: True` | 
## Forest Mill Back
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the question mark box | 4 | `self.logic = lambda _: True` | 
| Inside a keg | 1 | `l.barrels` | 
| On boxes near spider | 3 | `self.logic = lambda _: True` | 
| On various boxes | 3 | `self.logic = lambda _: True` | 

# Crystal Caves
## Crystal Caves
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near the DK Portal | 4 | `self.logic = lambda _: True` | 
| Crystal near level entry | 3 | `self.logic = lambda _: True` | 
| Behind the first ice wall | 2 | `self.logic = lambda _: True` | 
| Around the lower thick pillar near Ice Castle | 5 | `self.logic = lambda _: True` | 
| Around Ice Castle Tag | 6 | `self.logic = lambda _: True` | 
| Ice Castle Battlements (1) | 4 | `l.isdiddy or (l.islanky and (l.balloon or l.monkey_maneuvers)) or l.istiny` | 
| Ice Castle Battlements (2) | 4 | `l.isdiddy or (l.islanky and (l.balloon or l.monkey_maneuvers)) or l.istiny` | 
| On stumps near Ice Castle | 3 | `self.logic = lambda _: True` | 
| Near the small boulder | 4 | `self.logic = lambda _: True` | 
| Under the bridge near the small boulder | 2 | `l.jetpack and l.isdiddy` | 
| Near DK's Kasplat | 4 | `self.logic = lambda _: True` | 
| Hanging off the ledge near Blueprint Cave | 6 | `self.logic = lambda _: True` | 
| Fences near Ice Castle | 4 | `self.logic = lambda _: True` | 
| Steps up to Cranky's Lab | 3 | `self.logic = lambda _: True` | 
| Around Giant Boulder Shield | 8 | `self.logic = lambda _: True` | 
| On a stalagmite | 1 | `self.logic = lambda _: True` | 
| Around a pillar in the boulder cave | 4 | `self.logic = lambda _: True` | 
| On a stalagmite in the bonus cave | 1 | `self.logic = lambda _: True` | 
| Around the entrance to the bonus cave | 4 | `self.logic = lambda _: True` | 
| On the 5-Door Igloo (Entrances) | 5 | `self.logic = lambda _: True` | 
| On the 5-Door Igloo (Center) | 6 | `self.logic = lambda _: True` | 
| Around the thin bananaport pillar | 4 | `self.logic = lambda _: True` | 
| Around the thick bananaport pillar | 4 | `self.logic = lambda _: True` | 
| On boxes near the 5-Door Cabin (1) | 3 | `self.logic = lambda _: True` | 
| On boxes near the 5-Door Cabin (2) | 3 | `self.logic = lambda _: True` | 
| Near the waterfall | 5 | `self.logic = lambda _: True` | 
| On the doorway to Rotating Room | 2 | `self.logic = lambda _: True` | 
| Outside the Sprint Cabin | 3 | `self.logic = lambda _: True` | 
| Near the Sprint Cabin Headphones | 5 | `self.logic = lambda _: True` | 
| On stalactite in the Giant Kosha area | 2 | `self.logic = lambda _: True` | 
| Back of Bonus Cave | 5 | `Events.CavesW3bTagged in l.Events` | 
| Gorilla Gone Cavern | 3 | `self.logic = lambda _: True` | 
| Giant Boulder Cavern | 3 | `self.logic = lambda _: True` | 
| Giant Kosha Room | 3 | `self.logic = lambda _: True` | 
| In Snide's Cavern | 3 | `self.logic = lambda _: True` | 
| On Ice Castle | 4 | `((l.balloon or l.monkey_maneuvers) and l.islanky) or l.isdiddy or l.istiny` | 
| Near Cabin Waterfall | 3 | `self.logic = lambda _: True` | 
| Behind Igloo Tag Barrel | 3 | `self.logic = lambda _: True` | 
| On Slope to Cranky | 3 | `self.logic = lambda _: True` | 
| Behind Spike near Igloo Area | 3 | `self.logic = lambda _: True` | 
| Near Headphones | 3 | `self.logic = lambda _: True` | 
| In water near Funky's | 3 | `self.logic = lambda _: True` | 
| Pillar near Ice Castle | 2 | `(l.isdiddy and l.jetpack) or (l.istiny and l.twirl)` | 
| Behind Caves Igloo W1 | 3 | `self.logic = lambda _: True` | 
| Entrance to Blueprint Cave | 3 | `self.logic = lambda _: True` | 
## Caves Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the path to the first hoop | 3 | `self.logic = lambda _: True` | 
| In Baboon Blast Course | 3 | `logic=lambda _: True` | 
## Caves Lanky Race
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the torches at the start of the beetle race | 3 | `self.logic = lambda _: True` | 
| In the window in the Caves Beetle Race | 1 | `self.logic = lambda _: True` | 
## Caves Frozen Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near the Ice Tomato chair | 2 | `self.logic = lambda _: True` | 
| On Board | 2 | `self.logic = lambda _: True` | 
## Caves Chunky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Chunky Igloo TNT | 1 | `self.logic = lambda _: True` | 
## Caves Diddy Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the barrels in Diddy Igloo | 6 | `self.logic = lambda _: True` | 
## Caves Donkey Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| At the back of Donkey Igloo | 4 | `self.logic = lambda _: True` | 
## Caves Lanky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On some platforms in Lanky Igloo | 2 | `self.logic = lambda _: True` | 
## Caves Tiny Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the swords in Tiny Igloo | 2 | `self.logic = lambda _: True` | 
## Caves Lanky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near books in Lanky Cabin | 2 | `self.logic = lambda _: True` | 
## Caves Rotating Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the corners of Rotating Room | 4 | `self.logic = lambda _: True` | 
## Caves Chunky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the targets in Chunky Cabin | 3 | `self.logic = lambda _: True` | 
## Caves Diddy Lower Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the corners of the center platform in Diddy Lower Cabin | 4 | `l.jetpack or l.monkey_maneuvers` | 
| In Corner Platforms | 4 | `l.jetpack or l.monkey_maneuvers` | 
## Caves Diddy Upper Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In front of the pictures in Diddy Upper Cabin | 3 | `l.jetpack and (l.guitar or l.oranges) and l.isdiddy and (l.spring or l.CanMoontail())` | 
## Caves Donkey Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In between the holes in Donkey Cabin | 3 | `self.logic = lambda _: True` | 
| Above holes | 2 | `self.logic = lambda _: True` | 
## Caves Tiny Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around Tiny Cabin Interior | 3 | `self.logic = lambda _: True` | 

# Creepy Castle
## Creepy Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near DK Portal | 4 | `self.logic = lambda _: True` | 
| Starting pool | 3 | `self.logic = lambda _: True` | 
| Near Low Tag Barrel | 4 | `self.logic = lambda _: True` | 
| High tree at the back of Castle | 4 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Above a gravestone near lower tunnel entry | 3 | `self.logic = lambda _: True` | 
| Outside lower tunnel entry | 4 | `self.logic = lambda _: True` | 
| Above retracting platforms | 2 | `self.logic = lambda _: True` | 
| On a post near the upper tunnel rear entry | 3 | `l.jetpack and l.isdiddy` | 
| On a series of posts near upper Warp 2 | 4 | `self.logic = lambda _: True` | 
| Near the wobbly bridge near upper Warp 2 | 2 | `self.logic = lambda _: True` | 
| Hanging off the edge near Cranky's | 4 | `self.logic = lambda _: True` | 
| Near Museum Entrance | 2 | `self.logic = lambda _: True` | 
| Near Trash Can | 2 | `self.logic = lambda _: True` | 
| On the library cloud | 3 | `self.logic = lambda _: True` | 
| Around the edge near Library entrance | 8 | `self.logic = lambda _: True` | 
| Top of Castle | 2 | `self.logic = lambda _: True` | 
| Under Museum Entrance Platform | 2 | `self.logic = lambda _: True` | 
| Outside Greenhouse | 3 | `self.logic = lambda _: True` | 
| Around Castle Tree exterior | 3 | `l.jetpack and l.isdiddy` | 
| Around Tiny Kasplat | 3 | `self.logic = lambda _: True` | 
| Around upper W2 | 3 | `self.logic = lambda _: True` | 
| On thin tree near the Tree entrance | 2 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Behind Grave (1) | 3 | `self.logic = lambda _: True` | 
| Hanging off ledge near Castle Tree entrance | 3 | `self.logic = lambda _: True` | 
| Behind Grave (2) | 3 | `self.logic = lambda _: True` | 
| On tree near Crypt Entrance | 2 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On Drawbridge | 4 | `l.jetpack and l.isdiddy` | 
| Above Window | 2 | `l.jetpack and l.isdiddy` | 
## Castle Ballroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Ballroom Wall Torches | 2 | `self.logic = lambda _: True` | 
| Ballroom Post Torches | 4 | `self.logic = lambda _: True` | 
| Around the tiled Ballroom floor | 4 | `self.logic = lambda _: True` | 
| Ballroom K. Rool Banners | 6 | `l.jetpack and l.isdiddy` | 
| Around Monkeyport Pad | 3 | `self.logic = lambda _: True` | 
## Castle Dungeon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Dungeon Buckets | 3 | `self.logic = lambda _: True` | 
| Dungeon - Behind Gate (1) | 2 | `l.punch and l.chunky or l.CanPhase()` | 
| Dungeon - Behind Gate (2) | 2 | `l.punch and l.chunky or l.CanPhase()` | 
| Dungeon - Behind Gate (3) | 2 | `l.punch and l.chunky or l.CanPhase()` | 
| Donkey's Dungeon Room | 4 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| Diddy's Dungeon Room | 4 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.scope and l.peanut and l.can_use_vines` | 
| Around Donkey Switch | 4 | `self.logic = lambda _: True` | 
| Inside punchable grate | 3 | `(l.punch and l.chunky) or l.CanPhase()` | 
| Above the acid in Lanky's Room | 3 | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.islanky and l.trombone and l.balloon` | 
## Castle Shed
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Shed Interior Corners | 4 | `self.logic = lambda _: True` | 
| Around punch box | 4 | `self.logic = lambda _: True` | 
## Castle Lower Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Lower Cave hallway start | 4 | `self.logic = lambda _: True` | 
| Lower Cave Melon Crate | 4 | `self.logic = lambda _: True` | 
| Lower Cave Torch Pillar | 1 | `self.logic = lambda _: True` | 
| Near Funky | 2 | `self.logic = lambda _: True` | 
| Near Crypt Entrance | 4 | `self.logic = lambda _: True` | 
| On Crypt Skull | 1 | `self.logic = lambda _: True` | 
| Around the mausoleum entrance | 4 | `self.logic = lambda _: True` | 
| Near the Crypt Staircase | 3 | `self.logic = lambda _: True` | 
## Castle Crypt
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Wall Torch | 2 | `self.logic = lambda _: True` | 
| On Diddy Coffin | 4 | `self.logic = lambda _: True` | 
| On incorrect Minecart levers | 3 | `self.logic = lambda _: True` | 
| Inside Chunky's Coffin | 4 | `(l.Slam or l.CanPhase()) and l.ischunky` | 
| Inside Chunky Coffins | 3 | `(l.ischunky and l.punch) or l.CanPhase() or l.generalclips` | 
| Inside Diddy Coffins | 3 | `(l.isdiddy and l.charge) or l.CanPhase() or l.generalclips` | 
## Castle Mausoleum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Goo Hands | 6 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.istiny and l.twirl` | 
| Between Mausoleum Vines | 6 | `((l.grape and l.sprint) or l.generalclips or l.CanPhase()) and l.islanky and l.trombone and l.can_use_vines` | 
| Around Tiny Slam Pad | 2 | `(l.twirl or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.tiny))) or l.CanPhase()) and l.istiny` | 
| Around Lanky Reward | 3 | `((l.grape and l.sprint) or l.generalclips or l.CanPhase()) and ((l.trombone and l.can_use_vines) or l.monkey_maneuvers) and l.islanky` | 
## Castle Upper Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Tunnel behind torch | 3 | `self.logic = lambda _: True` | 
| Tunnel Rear Entry | 2 | `self.logic = lambda _: True` | 
| Over pit | 3 | `l.twirl and l.istiny` | 
| Near Candy's Shop | 3 | `self.logic = lambda _: True` | 
| Outside Dungeon Entrance | 3 | `self.logic = lambda _: True` | 
## Castle Greenhouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Greenhouse Exit Corner | 3 | `self.logic = lambda _: True` | 
| Greenhouse Dead End | 3 | `self.logic = lambda _: True` | 
| At a dead end | 3 | `logic=lambda _: True` | 
## Castle Library
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Library Wall Torch | 3 | `self.logic = lambda _: True` | 
| Library inside enemy gauntlet room | 4 | `self.logic = lambda _: True` | 
| Library Strong Kong Alcove | 2 | `self.logic = lambda _: True` | 
## Castle Museum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Museum around second skull | 7 | `self.logic = lambda _: True` | 
| Museum entryway to main room | 4 | `self.logic = lambda _: True` | 
| Car Race Building Chimney stack | 6 | `self.logic = lambda _: True` | 
| Car Race Second Chimney stack | 1 | `self.logic = lambda _: True` | 
| Around mystery Museum Pillar | 7 | `(l.monkeyport or l.CanPhase()) and l.istiny` | 
| On mystery Museum Pillar | 3 | `(l.monkeyport or l.CanPhase()) and l.istiny` | 
| In front of shields | 3 | `self.logic = lambda _: True` | 
## Castle Tower
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Wall Torches | 3 | `l.balloon and l.islanky` | 
## Castle Trash Can
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around trash can cheese | 3 | `self.logic = lambda _: True` | 
| Off the ledge of the trash can cheese | 3 | `self.logic = lambda _: True` | 
| On the long sides of the cheese | 2 | `self.logic = lambda _: True` | 
## Castle Tree
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Underwater in the DK Tree area | 4 | `l.swim and ((l.coconut) or l.generalclips or l.CanPhase()) and l.isdonkey` | 
| In Chunky's Tree area | 4 | `self.logic = lambda _: True` | 
| On pathway to Chunky Bonus | 3 | `self.logic = lambda _: True` | 
## Castle Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside the Baboon Blast Course | 5 | `self.logic = lambda _: True` | 
