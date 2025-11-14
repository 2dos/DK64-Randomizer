
# Jungle Japes
## Jungle Japes
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Starting area against outside wall | 10 | `self.logic = lambda _: True` | 
| Starting area treetops | 15 | `l.climbing` | 
| Pentagon around Diddy's Cave GB | 5 | `self.logic = lambda _: True` | 
| Bunch in front of Cave T&S | 5 | `self.logic = lambda _: True` | 
| Line in front of cave peanut gate | 5 | `self.logic = lambda _: True` | 
| Bunch on torch in cave tunnel | 5 | `self.logic = lambda _: True` | 
| W1 bunches | 10 | `self.logic = lambda _: True` | 
| W2 bunches | 10 | `self.logic = lambda _: True` | 
| Along the shoreline on Tag Barrel side of river | 15 | `self.logic = lambda _: True` | 
| Cannon to Diddy cage (2 bunches) | 10 | `self.logic = lambda _: True` | 
| Tops of solid bushes (TB side) | 10 | `self.logic = lambda _: True` | 
| Tops of bushes (Painting Room side) | 10 | `self.logic = lambda _: True` | 
| From Diddy BP to river side (7 custom, 3 Diddy) | 3 | `self.logic = lambda _: True` | 
| From Diddy BP to river side (7 custom, 3 Diddy) | 7 | `self.logic = lambda _: True` | 
| Bunch in Minecart exit | 5 | `self.logic = lambda _: True` | 
| Up the slope to painting room | 10 | `(l.handstand and l.islanky) or (l.twirl and l.istiny) or l.slope_resets` | 
| Leading up to and on BBlast pad | 5 | `l.can_use_vines or l.CanMoonkick()` | 
| Leading up to and on BBlast pad | 5 | `self.logic = lambda _: True` | 
| Up the vine to Funky's and lining the edge of Funky's area | 15 | `self.logic = lambda _: True` | 
| On the edge of cannon platform | 10 | `self.logic = lambda _: True` | 
| Bunches on torches by DK and Tiny BPs | 10 | `self.logic = lambda _: True` | 
| Singles in DK/Tiny BP tunnel (10 custom, 10 Chunky) | 20 | `self.logic = lambda _: True` | 
| W5 bunches and 5 singles around on mountain | 10 | `self.logic = lambda _: True` | 
| W5 bunches and 5 singles around on mountain | 5 | `self.logic = lambda _: True` | 
| Ring of singles around beehive area | 15 | `self.logic = lambda _: True` | 
| Beehive area inner platform ring (between trees) | 10 | `self.logic = lambda _: True` | 
| Bunch on stump (beehive area) | 5 | `self.logic = lambda _: True` | 
| Singles on steps leading to beehive | 10 | `self.logic = lambda _: True` | 
| From W4 to Cranky (1 custom, 9 Donkey) | 10 | `self.logic = lambda _: True` | 
| Bottom of pit near Diddy BP | 5 | `self.logic = lambda _: True` | 
| Bunches above water in fairy room | 10 | `self.logic = lambda _: True` | 
| Bunches on torches in boulder room | 10 | `self.logic = lambda _: True` | 
| W4 bunches | 10 | `self.logic = lambda _: True` | 
| Cranky trees (1 custom, 1 Lanky, 1 Tiny bunch) | 15 | `l.climbing` | 
| Outside ring around Cranky area | 20 | `self.logic = lambda _: True` | 
| Inside ring around Cranky's Lab | 10 | `self.logic = lambda _: True` | 
| Lanky's blueprint room (8 custom, 7 Lanky) | 11 | `self.logic = lambda _: True` | 
| Lanky's blueprint room (8 custom, 7 Lanky) | 2 | `l.handstand or l.slope_resets` | 
| Lanky's blueprint room (8 custom, 7 Lanky) | 2 | `self.logic = lambda _: True` | 
| 4 corners of Lanky BP room | 20 | `self.logic = lambda _: True` | 
| Slope to Painting room (2 custom, 3 Lanky) | 4 | `self.logic = lambda _: True` | 
| Slope to Painting room (2 custom, 3 Lanky) | 1 | `self.logic = lambda _: True` | 
| Riverbed (5 custom, 5 Lanky) | 10 | `l.swim` | 
| Riverbed bunches (on each end) | 10 | `l.swim` | 
| Ring around mountain (3 custom, 7 Diddy) | 10 | `self.logic = lambda _: True` | 
| First tunnel (10 custom, 5 Tiny) | 15 | `self.logic = lambda _: True` | 
| Slopes to Diddy's cage (4 custom, 6 Donkey) | 10 | `self.logic = lambda _: True` | 
| Rambi door to Fairy room (3 custom, 7 Tiny) | 5 | `self.logic = lambda _: True` | 
| Rambi door to Fairy room (3 custom, 7 Tiny) | 5 | `self.logic = lambda _: True` | 
| 3 bunches on riverbed | 15 | `l.swim` | 
| Next to Snide | 10 | `self.logic = lambda _: True` | 
| Diddy cave around exterior | 10 | `self.logic = lambda _: True` | 
| On the edge of Diddy's cage platform | 5 | `self.logic = lambda _: True` | 
| Tiny's caged GB | 10 | `((Events.JapesTinySwitch in l.Events or l.CanPhase() or l.CanPhaseswim() or l.CanSkew(False)) and l.tiny)` | 
| Lanky's caged GB | 10 | `((Events.JapesLankySwitch in l.Events or l.CanSkew(False)) and l.lanky) or (l.CanSkew(False) and l.settings.free_trade_items)` | 
| T&S above diddy BP (2 custom, 1 Donkey bunch) | 15 | `self.logic = lambda _: True` | 
| Diddy's Caged GB | 10 | `((Events.JapesDiddySwitch1 in l.Events or l.CanPhase() or l.generalclips or l.CanSkew(False)) and l.diddy)` | 
| Chunky's Caged GB | 10 | `((Events.JapesChunkySwitch in l.Events or l.CanPhase() or l.CanSkew(False)) and l.chunky) or ((l.CanPhase() or l.CanSkew(False)) and l.settings.free_trade_items)` | 
| between vines from funky to cannon | 10 | `l.can_use_vines` | 
| Behind stump in beehive area | 10 | `self.logic = lambda _: True` | 
| Above Melon Crate behind mountain | 5 | `self.logic = lambda _: True` | 
| Above melon crate behind boulder | 5 | `self.logic = lambda _: True` | 
| Inside Free Diddy cage | 5 | `Events.JapesFreeKongOpenGates in l.Events` | 
| Between starting vines (Donkey) | 5 | `l.climbing and (l.can_use_vines or (l.monkey_maneuvers and l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey))))` | 
| On top of slippery slope in BP cave (Lanky) | 5 | `self.logic = lambda _: True` | 
| W3 bunches (Donkey) | 10 | `self.logic = lambda _: True` | 
| Starting area (Diddy) | 5 | `self.logic = lambda _: True` | 
| On Funky's shop (Chunky) | 10 | `self.logic = lambda _: True` | 
| Under Lanky's bonus barrel in first cave (Lanky) | 5 | `l.grape or l.CanPhase() or l.generalclips` | 
| In Rambi hut (Lanky) | 5 | `Events.Rambi in l.Events` | 
| In Rambi hut (Donkey) | 5 | `Events.Rambi in l.Events` | 
| In Rambi hut (Diddy) | 5 | `Events.Rambi in l.Events` | 
| In Rambi hut (Tiny) | 5 | `Events.Rambi in l.Events` | 
| On treetops (Tag barrel side) (Diddy) | 10 | `l.climbing` | 
| Inside cage with Rambi Box (Donkey) | 5 | `l.hasMoveSwitchsanity(Switches.JapesRambi, False) or l.CanPhase()` | 
| On 4 trees in Beehive area (Chunky) | 20 | `l.climbing and l.hunkyChunky` | 
| On treetop by Funky (Donkey) | 5 | `l.climbing` | 
| On treetop by cannon (Donkey) | 5 | `l.climbing` | 
| Underwater bunches (Diddy) | 10 | `l.swim` | 
| On treetops (Painting room side) (Diddy) | 10 | `l.climbing` | 
| Beehive area, left stump (Tiny) | 15 | `l.mini or l.CanPhase()` | 
| Beehive area, right stump (Tiny) | 15 | `l.mini or l.CanPhase()` | 
| Diddy's cage treetop (Donkey) | 5 | `l.climbing` | 
| In front of beehive entrance (Tiny) | 5 | `self.logic = lambda _: True` | 
| Under Tiny's bonus barrel in first cave (Tiny) | 5 | `l.feather or l.CanPhase()` | 
| Around boulder past rambi gate (Lanky) | 5 | `self.logic = lambda _: True` | 
| Treetop by Snide's (Lanky) | 5 | `l.climbing` | 
| Around underground entrance (Chunky) | 5 | `self.logic = lambda _: True` | 
| On Cranky's Lab (Chunky) | 5 | `l.climbing` | 
| Bunch by Snide's (Lanky) | 5 | `self.logic = lambda _: True` | 
| Japes Rock bunch (Chunky) | 5 | `l.barrels` | 
| Above the bush push bush | 5 | `self.logic = lambda _: True` | 
| Start gate switch | 5 | `l.climbing and l.can_use_vines` | 
| Peanut gate switches | 10 | `self.logic = lambda _: True` | 
| Hive area gate switches | 10 | `self.logic = lambda _: True` | 
| Peanut cave T&S door frame | 5 | `self.logic = lambda _: True` | 
| On the peanut cave torches | 10 | `self.logic = lambda _: True` | 
| On the DK caged GB | 5 | `self.logic = lambda _: True` | 
| Bumps near the river | 10 | `self.logic = lambda _: True` | 
| Other bumps near the river | 10 | `self.logic = lambda _: True` | 
| River surface | 10 | `self.logic = lambda _: True` | 
| Around first tree near minecart exit | 10 | `self.logic = lambda _: True` | 
| Around second tree near minecart exit | 10 | `self.logic = lambda _: True` | 
| On minecart exit | 5 | `self.logic = lambda _: True` | 
| Baboon blasting off !! | 5 | `l.blast, locations=[[5, 1.0, 2460, 700, 1148]]` | 
| Around the cannon | 5 | `self.logic = lambda _: True` | 
| Hive area next to left hollow stump | 5 | `self.logic = lambda _: True` | 
| Hive area next to right hollow stump | 5 | `self.logic = lambda _: True` | 
| On the bouncy mushroom | 5 | `self.logic = lambda _: True` | 
| Twirl from Funky | 5 | `l.twirl` | 
| Across the river | 5 | `self.logic = lambda _: True` | 
| Orangstand-able slope to cannon | 5 | `l.handstand` | 
| Torch near Diddy kasplat | 5 | `self.logic = lambda _: True` | 
| Above upper big torch | 5 | `self.logic = lambda _: True` | 
| Above lower big torch | 5 | `self.logic = lambda _: True` | 
| Behind the Lanky slope bonus barrel | 5 | `l.handstand` | 
| Cranky area entrance sides | 10 | `self.logic = lambda _: True` | 
| Flower near Rambi cage | 5 | `self.logic = lambda _: True` | 
| Flower near Lanky hut | 5 | `self.logic = lambda _: True` | 
| Flower near DK hut | 5 | `self.logic = lambda _: True` | 
| Flower near Diddy hut | 5 | `self.logic = lambda _: True` | 
| Flower near Tiny hut | 5 | `self.logic = lambda _: True` | 
| High against the Rambi door | 5 | `self.logic = lambda _: True` | 
| Rambi lake Bouldertech | 5 | `l.chunky and l.barrels` | 
| Rambi lake shore | 5 | `self.logic = lambda _: True` | 
| Starting area lower (DK portal side) | Balloon | `self.logic = lambda _: True` | 
| Starting area lower (gate side) | Balloon | `self.logic = lambda _: True` | 
| Starting area upper (DK portal side) | Balloon | `self.logic = lambda _: True` | 
| Starting area upper (gate side) | Balloon | `self.logic = lambda _: True` | 
| First tunnel 1 (gate side) | Balloon | `self.logic = lambda _: True` | 
| First tunnel 2 (main area side) | Balloon | `self.logic = lambda _: True` | 
| Minecart exit | Balloon | `self.logic = lambda _: True` | 
| Painting room peanut switch | Balloon | `self.logic = lambda _: True` | 
| Over river by middle switch | Balloon | `self.logic = lambda _: True` | 
| T&S portal above Diddy BP | Balloon | `self.logic = lambda _: True` | 
| Around mountain | Balloon | `self.logic = lambda _: True` | 
| In front of Diddy's cage | Balloon | `self.logic = lambda _: True` | 
| Funky's Armory | Balloon | `self.logic = lambda _: True` | 
| Cannon to Diddy's cage | Balloon | `self.logic = lambda _: True` | 
| Tunnel near DK BP | Balloon | `self.logic = lambda _: True` | 
| Tunnel near Tiny BP | Balloon | `self.logic = lambda _: True` | 
| Near high W2 above river | Balloon | `self.logic = lambda _: True` | 
| Above river by tag barrel | Balloon | `self.logic = lambda _: True` | 
| Over river by big vine | Balloon | `self.logic = lambda _: True` | 
| Beehive area between trees | Balloon | `self.logic = lambda _: True` | 
| Above beehive | Balloon | `self.logic = lambda _: True` | 
| Above stump | Balloon | `self.logic = lambda _: True` | 
| Above vines next to BBlast | Balloon | `self.logic = lambda _: True` | 
| Between trees in front of painting room | Balloon | `self.logic = lambda _: True` | 
| Near main Tag Barrel | Balloon | `self.logic = lambda _: True` | 
| Above hole by Diddy BP (BP side) | Balloon | `self.logic = lambda _: True` | 
| Above hole by Diddy BP (wall side) | Balloon | `self.logic = lambda _: True` | 
| Between beaver and rambi door | Balloon | `self.logic = lambda _: True` | 
| Above slope to Cranky | Balloon | `self.logic = lambda _: True` | 
| In first cave (Diddy) | Balloon | `self.logic = lambda _: True` | 
| In front of Snide's (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In boulder cave 1 (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Behind Rambi hut (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Above mountain (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Under baboon blast pad (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In front of Cranky (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Behind Rambi hut (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In fairy room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In boulder cave 2 (Chunky) | Balloon | `self.logic = lambda _: True` | 
| In boulder cave 3 (Chunky) | Balloon | `self.logic = lambda _: True` | 
| In Lanky blueprint room (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Peanut cage | Balloon | `self.logic = lambda _: True` | 
| DK's caged GB | Balloon | `self.logic = lambda _: True` | 
| Hive tunnel coconut switch | Balloon | `self.logic = lambda _: True` | 
| Above the river near Funky | Balloon | `self.logic = lambda _: True` | 
| Hillside coconut switch | Balloon | `self.logic = lambda _: True` | 
| Between cannon and alcove | Balloon | `self.logic = lambda _: True` | 
| Above Diddy's cage | Balloon | `self.logic = lambda _: True` | 
| Up high near Snide | Balloon | `self.logic = lambda _: True` | 
| Hive area entrance | Balloon | `self.logic = lambda _: True` | 
| Stormy tunnel towards Cranky | Balloon | `self.logic = lambda _: True` | 
| Tree between DK and Diddy's huts | Balloon | `self.logic = lambda _: True` | 
| Above the Rambi cage | Balloon | `self.logic = lambda _: True` | 
| In the Rambi lake | Balloon | `self.logic = lambda _: True` | 
## Japes Lanky Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Each side of the painting | 10 | `self.logic = lambda _: True` | 
| On pillars (Lanky) | 10 | `self.logic = lambda _: True` | 
| On steps (Lanky) | 10 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| In painting room (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Around the painting | Balloon | `self.logic = lambda _: True` | 
## Japes Mountain
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Bunch on Diddy's switch | 5 | `l.peanut or l.monkey_maneuvers` | 
| Singles on path to switch | 5 | `self.logic = lambda _: True` | 
| Big upside down minecart | 5 | `self.logic = lambda _: True` | 
| 2 bunches on big barrel (with ammo) | 10 | `self.logic = lambda _: True` | 
| Bunches on piles of coal | 10 | `self.logic = lambda _: True` | 
| 2 bunches on steel kegs (2nd room) | 10 | `self.logic = lambda _: True` | 
| Dynamite box in chimpy charge switch room | 5 | `l.charge or l.CanPhase()` | 
| Bunches on staircase-shaped boxes | 10 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()` | 
| Conveyors | 10 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()` | 
| On box in corner of conveyor room (Diddy) | 5 | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()` | 
| In river (Diddy) | 5 | `self.logic = lambda _: True` | 
| On box by conveyors (Diddy) | 5 | `l.CanSlamSwitch(Levels.JungleJapes, 1)` | 
| In front of peanut switch (Diddy) | 5 | `self.logic = lambda _: True` | 
| Around the first post | 5 | `self.logic = lambda _: True` | 
| On the glitchy backflip spot | 5 | `self.logic = lambda _: True` | 
| On the curved rail | 5 | `self.logic = lambda _: True` | 
| Jumping on the rails | 10 | `self.logic = lambda _: True` | 
| Next to post near minecart entrance | 5 | `self.logic = lambda _: True` | 
| Around the conveyor gate switch | 5 | `self.logic = lambda _: True` | 
| First room above river | Balloon | `self.logic = lambda _: True` | 
| In conveyor room (Diddy) | Balloon | `l.CanSlamSwitch(Levels.JungleJapes, 1) or l.CanPhase()` | 
| Little tunnel | Balloon | `self.logic = lambda _: True` | 
| Around post under the minecart track | Balloon | `self.logic = lambda _: True` | 
## Japes Under Ground
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On path (15 custom, 5 Chunky) | 20 | `self.logic = lambda _: True` | 
| On blueprint platform | 5 | `l.pineapple and l.can_use_vines and l.ischunky` | 
| Bunches on path (Chunky) | 10 | `self.logic = lambda _: True` | 
| Entrance stalagmite | 5 | `self.logic = lambda _: True` | 
| Entrance flames | 10 | `self.logic = lambda _: True` | 
| Perilous jump above the void | 5 | `self.logic = lambda _: True` | 
| Left side | Balloon | `self.logic = lambda _: True` | 
| Right (inner) side | Balloon | `self.logic = lambda _: True` | 
## Japes Tiny Hive
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Paths to 1st & 2nd Switch | 10 | `l.CanSlamSwitch(Levels.JungleJapes, 1) and l.istiny` | 
| Around first switch room | 10 | `self.logic = lambda _: True` | 
| Behind 2nd hallway arch | 10 | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) and l.istiny` | 
| Rings on steps (12 custom, 8 Tiny) | 20 | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) and l.istiny` | 
| Around 2nd switch room | 10 | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) and l.istiny` | 
| Above the entrance | 5 | `self.logic = lambda _: True` | 
| White flower between doors 2 and 3 | 5 | `self.logic = lambda _: True` | 
| Around final room | Balloon | `(l.CanSlamSwitch(Levels.JungleJapes, 1) and (l.saxophone or l.oranges)) and l.istiny` | 
| In first room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Second room | Balloon | `self.logic = lambda _: True` | 
## Japes Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Baboon blast singles between barrels | 10 | `self.logic = lambda _: True` | 
| Japes Baboon Blast (Donkey) | 10 | `self.logic = lambda _: True` | 

# Angry Aztec
## Angry Aztec
| Name | Amount | Logic |
| ---- | ------ | ----- |
| At DK Portal before W1 | 5 | `l.can_use_vines` | 
| First tunnel (5 custom, 5 Chunky) | 9 | `self.logic = lambda _: True` | 
| First tunnel (5 custom, 5 Chunky) | 1 | `l.can_use_vines` | 
| On DK BP archway | 10 | `l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) and l.strongKong` | 
| First tunnel (5 custom, 5 Lanky) | 10 | `self.logic = lambda _: True` | 
| Singles all around oasis (17 custom, 3 Donkey) | 20 | `self.logic = lambda _: True` | 
| Singles on vines and bunch on guitar pad | 10 | `l.can_use_vines` | 
| Around llama cage (upper) | 10 | `self.logic = lambda _: True` | 
| Around llama cage (lower) | 15 | `self.logic = lambda _: True` | 
| Bunches on each side of the Tiny Temple door | 10 | `self.logic = lambda _: True` | 
| Around Tiny Temple (on temple) | 20 | `self.logic = lambda _: True` | 
| Singles around Diddy BP | 10 | `l.jetpack` | 
| 4 corners of top of Tiny Temple | 20 | `l.jetpack and l.isdiddy and l.climbing` | 
| In front of Candy's | 5 | `self.logic = lambda _: True` | 
| Bunches on W1 | 5 | `self.logic = lambda _: True` | 
| Bunches on W1 | 5 | `self.logic = lambda _: True` | 
| Second tunnel (5 custom, 5 Diddy) | 10 | `self.logic = lambda _: True` | 
| Bunch on boulder switch | 5 | `self.logic = lambda _: True` | 
| Snake path to Cranky (5 custom, 5 Lanky) | 10 | `self.logic = lambda _: True` | 
| Bunches next to Cranky (1 custom, 1 Lanky bunch) | 10 | `self.logic = lambda _: True` | 
| W2 bunches (1 custom, 1 Diddy) | 5 | `self.logic = lambda _: True` | 
| W2 bunches (1 custom, 1 Diddy) | 5 | `self.logic = lambda _: True` | 
| Bunches on W3 | 10 | `self.logic = lambda _: True` | 
| Second tunnel from boulder pad to Chunky BB (5 custom, 5 Tiny) | 10 | `self.logic = lambda _: True` | 
| Second tunnel from Chunky BB to far W2 (5 custom, 5 Tiny) | 10 | `self.logic = lambda _: True` | 
| Near far W2 (2 custom, 3 Diddy) | 5 | `self.logic = lambda _: True` | 
| Flying bunches around totem (scale up a bit) | 20 | `l.jetpack` | 
| Around totem Llama temple/5DT side (8 custom, 7 Chunky) | 15 | `self.logic = lambda _: True` | 
| Around totem Snide's side (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Top of ramps by tower | 10 | `self.logic = lambda _: True` | 
| Bunch on trees between Snide's and Beetle Race tower (1 custom, 2 Lanky bunches) | 15 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Around Snide's HQ platform edge | 5 | `self.logic = lambda _: True` | 
| To Diddy's Tower GB (4 custom, 6 Chunky) | 10 | `self.logic = lambda _: True` | 
| Near Beetle Race Tower (2 custom, 3 Diddy) | 5 | `self.logic = lambda _: True` | 
| 15 singles around Beetle Race Tower | 15 | `self.logic = lambda _: True` | 
| From Snide's Tag to W5 T&S (7 custom, 3 Donkey) | 10 | `self.logic = lambda _: True` | 
| Bunches around the feed me totem | 10 | `self.logic = lambda _: True` | 
| Bunches on W4 | 10 | `self.logic = lambda _: True` | 
| W5 bunches (1 custom, 1 Tiny bunch) | 5 | `self.logic = lambda _: True` | 
| W5 bunches (1 custom, 1 Tiny bunch) | 5 | `self.logic = lambda _: True` | 
| Around Llama temple | 15 | `self.logic = lambda _: True` | 
| Llama temple stairs (1 custom, 4 Donkey) | 5 | `self.logic = lambda _: True` | 
| On each side of the Llama temple stairs | 10 | `self.logic = lambda _: True` | 
| On top of Diddy's Feed me totem switch on 5DT | 5 | `l.jetpack` | 
| 5DT side (1 custom, 4 Diddy) | 5 | `self.logic = lambda _: True` | 
| Around 5DT bottom ledge | 20 | `self.logic = lambda _: True` | 
| Around 5DT top ledge | 15 | `self.logic = lambda _: True` | 
| Bunches on patch of sand between Llama temple and W2-3-4 (accessible by jumping from nearby tree) | 10 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Bunches on 4 corners of Chunky BB cage | 20 | `self.logic = lambda _: True` | 
| Bunches on top of Chunky BB cage | 10 | `self.logic = lambda _: True` | 
| Along the walls around Chunky BB cage | 15 | `self.logic = lambda _: True` | 
| Inside giant boulder | 5 | `l.chunky and l.hunkyChunky and l.barrels` | 
| Bunches on each side of Funky's | 10 | `self.logic = lambda _: True` | 
| Singles up the stairs between Funky and Llama temple | 10 | `self.logic = lambda _: True` | 
| Singles up the stairs between Llama Temple and W2 | 10 | `self.logic = lambda _: True` | 
| Around W5 near bonus barrel | 5 | `self.logic = lambda _: True` | 
| Under Mini Monkey Barrel by Beetle Race Tower (Tiny) | 5 | `self.logic = lambda _: True` | 
| On oasis treetops (Donkey) | 5 | `l.climbing` | 
| On oasis treetops (Donkey) | 5 | `l.climbing` | 
| On oasis treetops (Donkey) | 5 | `l.climbing` | 
| DK Sealed Quicksand Tunnel (Donkey) | 20 | `l.strongKong` | 
| DK Blueprint cave (Donkey) | 10 | `(l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False) or l.CanPhase()) and l.strongKong` | 
| On Melon crate on Llama Temple roof (Diddy) | 5 | `l.jetpack` | 
| In sun (Diddy) | 5 | `l.jetpack` | 
| On trees around Beetle race tower (Diddy) | 15 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Path to 5DT (Tiny) | 5 | `self.logic = lambda _: True` | 
| Trees around back of 5DT (Tiny) | 10 | `l.climbing or (l.twirl and l.istiny) or (l.jetpack and l.isdiddy)` | 
| Trees around front of 5DT (Tiny) | 15 | `l.climbing or (l.twirl and l.istiny) or (l.jetpack and l.isdiddy)` | 
| Trees between Llama Temple and 5DT (Lanky) | 15 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Around the outside of Llama Temple | 15 | `self.logic = lambda _: True` | 
| Vase room (Chunky) | 20 | `l.pineapple or l.CanPhase()` | 
| On Tiny Temple Staircase | 5 | `self.logic = lambda _: True` | 
| Entrance portal | 10 | `self.logic = lambda _: True` | 
| In front of the vases room | 5 | `self.logic = lambda _: True` | 
| Under the flames by vases room | 10 | `self.logic = lambda _: True` | 
| In front of the DK Kasplat room | 5 | `self.logic = lambda _: True` | 
| Under the flames by DK Kasplat room | 10 | `self.logic = lambda _: True` | 
| Around the oasis grass | 10 | `self.logic = lambda _: True` | 
| Around the rocketbarrel tree | 10 | `self.logic = lambda _: True` | 
| Right of Tiny temple stairs | 5 | `self.logic = lambda _: True` | 
| Left of Tiny temple stairs | 5 | `self.logic = lambda _: True` | 
| Between the Tiny temple switches | 10 | `self.logic = lambda _: True` | 
| In front of the guitar door | 10 | `self.logic = lambda _: True` | 
| High between the three oasis trees | 5 | `l.climbing` | 
| Start tunnel arch | 5 | `l.jetpack and l.climbing` | 
| Top center of Tiny temple | 5 | `l.jetpack and l.climbing` | 
| Guitar door arch | 5 | `l.jetpack and l.climbing` | 
| Around the giant boulder switch | 10 | `self.logic = lambda _: True` | 
| Under flames near Hunky barrel | 10 | `self.logic = lambda _: True` | 
| Odd wall between Hunky and boulder | 5 | `self.logic = lambda _: True` | 
| On the giant boulder | 5 | `self.logic = lambda _: True` | 
| Around the giant boulder | 10 | `self.logic = lambda _: True` | 
| Totem area entrance | 10 | `self.logic = lambda _: True` | 
| Between warp 3 and warp 4 | 5 | `self.logic = lambda _: True` | 
| Around trees towards Funky | 10 | `self.logic = lambda _: True` | 
| Around tree in front of Llama temple | 5 | `self.logic = lambda _: True` | 
| Around tree near rocketbarrel | 5 | `self.logic = lambda _: True` | 
| Around the gong tower | 15 | `self.logic = lambda _: True` | 
| Behind the two far gongs | 10 | `self.logic = lambda _: True` | 
| In the quicksand near rocketbarrel | 10 | `l.strongKong` | 
| Flower near Snide | 5 | `self.logic = lambda _: True` | 
| Around trees between rocketbarrel and warp 5 | 10 | `self.logic = lambda _: True` | 
| In front of the sealed quicksand tunnel | 5 | `l.strongKong` | 
| Flower near Funky | 5 | `self.logic = lambda _: True` | 
| 5DT upper front corners | 10 | `self.logic = lambda _: True` | 
| 5DT upper back corners | 10 | `self.logic = lambda _: True` | 
| Stairs to the baboon blast pad | 5 | `self.logic = lambda _: True` | 
| Left of Llama temple stairs | 5 | `self.logic = lambda _: True` | 
| Right of Llama temple stairs | 5 | `self.logic = lambda _: True` | 
| Vases room central platform | 10 | `(l.pineapple and l.chunky) or l.CanPhase()` | 
| Totem rocketbarrel liftoff !! | 10 | `l.jetpack` | 
| Orbit around the sun | 15 | `l.jetpack` | 
| Sun symbol above the vulture cage | 5 | `(l.climbing and l.can_use_vines) or (l.jetpack and l.isdiddy)` | 
| Llama temple roof ledges | 10 | `l.jetpack` | 
| Ridge between Llama temple and 5DT | 5 | `l.jetpack` | 
| On the roof of the 5DT | 5 | `l.jetpack` | 
| Around sealed quicksand tunnel warp 5 | 5 | `self.logic = lambda _: True` | 
| Chunky vase room back wall | Balloon | `l.pineapple` | 
| Chunky vase room right wall | Balloon | `l.pineapple` | 
| DK BP room over/under bridge | Balloon | `l.hasMoveSwitchsanity(Switches.AztecBlueprintDoor, False)` | 
| Oasis | Balloon | `self.logic = lambda _: True` | 
| In front of Candy | Balloon | `self.logic = lambda _: True` | 
| Behind Tiny Temple | Balloon | `self.logic = lambda _: True` | 
| Behind Llama cage high up | Balloon | `self.logic = lambda _: True` | 
| Rising from quicksand near oasis | Balloon | `self.logic = lambda _: True` | 
| Near Hunky Chunky barrel | Balloon | `self.logic = lambda _: True` | 
| Cranky snake path left side | Balloon | `self.logic = lambda _: True` | 
| Around giant boulder | Balloon | `self.logic = lambda _: True` | 
| Behind Beetle Race Tower high up | Balloon | `self.logic = lambda _: True` | 
| In front of Snide's | Balloon | `self.logic = lambda _: True` | 
| Around feed me totem | Balloon | `self.logic = lambda _: True` | 
| Right side of 5DT | Balloon | `self.logic = lambda _: True` | 
| Spiral around tree left side of 5DT | Balloon | `self.logic = lambda _: True` | 
| Near Cranky's lab (right side) (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In front of Tiny Temple (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Behind Llama Temple (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Near Cranky's Lab (left side) (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Sealed Quicksand Tunnel (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Between the quicksand pits | Balloon | `self.logic = lambda _: True` | 
| Oasis entrance | Balloon | `self.logic = lambda _: True` | 
| Quicksand near Candy | Balloon | `self.logic = lambda _: True` | 
| Around the llama's cage | Balloon | `self.logic = lambda _: True` | 
| Snake road | Balloon | `self.logic = lambda _: True` | 
| Around the Hunky cage | Balloon | `self.logic = lambda _: True` | 
| Near the vulture cage | Balloon | `self.logic = lambda _: True` | 
| Around warp 5 | Balloon | `self.logic = lambda _: True` | 
| Poking in and out of the sealed quicksand tunnel | Balloon | `self.logic = lambda _: True` | 
| Trees in front of 5DT | Balloon | `self.logic = lambda _: True` | 
| In front of Llama temple | Balloon | `self.logic = lambda _: True` | 
| Quicksand near Rocketbarrel | Balloon | `self.logic = lambda _: True` | 
## Aztec Donkey5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| First dead end | 10 | `self.logic = lambda _: True` | 
| Second dead end | 5 | `(l.coconut and l.isdonkey) or l.CanPhase()` | 
| Path to GB | 16 | `(l.coconut and l.isdonkey) or l.CanPhase()` | 
| Path to GB | 4 | `self.logic = lambda _: True` | 
| Dead end corners | 5 | `self.logic = lambda _: True` | 
| Dead end corners | 5 | `l.coconut` | 
| Stairs | 5 | `l.coconut` | 
| Near the GB | 5 | `l.coconut` | 
| First dead end | Balloon | `self.logic = lambda _: True` | 
| Path to the second coconut switch | Balloon | `self.logic = lambda _: True` | 
## Aztec Diddy5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Path to GB | 16 | `l.peanut` | 
| Path to GB | 4 | `self.logic = lambda _: True` | 
| Second dead end | 10 | `self.logic = lambda _: True` | 
| First dead end | 10 | `l.peanut or l.CanPhase()` | 
| Dead end corners | 5 | `l.peanut` | 
| Dead end corners | 5 | `self.logic = lambda _: True` | 
| Stairs | 5 | `l.peanut` | 
| Near the GB | 10 | `l.peanut` | 
| Right side (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Second peanut switch | Balloon | `self.logic = lambda _: True` | 
## Aztec Lanky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Path to GB | 19 | `self.logic = lambda _: True` | 
| Path to GB | 2 | `l.grape or l.CanPhase()` | 
| Path to GB | 4 | `self.logic = lambda _: True` | 
| Dead end | 5 | `l.grape` | 
| Inner walls of the loop | 10 | `self.logic = lambda _: True` | 
| Center stairs | 5 | `self.logic = lambda _: True` | 
| Near the GB | 10 | `l.grape` | 
| Dead end | Balloon | `self.logic = lambda _: True` | 
| Middle (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Next to the GB | Balloon | `self.logic = lambda _: True` | 
## Aztec Tiny5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Path to GB | 19 | `self.logic = lambda _: True` | 
| Path to GB | 2 | `l.feather or l.CanPhase()` | 
| Path to GB | 4 | `self.logic = lambda _: True` | 
| Dead end | 5 | `l.feather` | 
| Right side Mini Monkey room (scale 0.6) | 10 | `l.mini or l.CanPhase()` | 
| Useless Mini room | 5 | `l.mini, locations=[[5, 1.0, 230, 48, 608]]` | 
| Under the right Mini barrel | 5 | `self.logic = lambda _: True` | 
| Above the left Mini barrel | 5 | `self.logic = lambda _: True` | 
| Center stairs | 5 | `self.logic = lambda _: True` | 
| Near the GB | 10 | `l.feather` | 
| Dead end | Balloon | `self.logic = lambda _: True` | 
| Left side | Balloon | `self.logic = lambda _: True` | 
## Aztec Chunky5DTemple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Path to GB | 22 | `self.logic = lambda _: True` | 
| Path to GB | 4 | `l.pineapple or l.CanPhase()` | 
| Path to GB | 4 | `self.logic = lambda _: True` | 
| On both stairs | 5 | `self.logic = lambda _: True` | 
| Near the dirt patch | 5 | `self.logic = lambda _: True` | 
| Final pineapple switch stairs | 10 | `l.pineapple` | 
| Near the GB | 10 | `l.pineapple` | 
| Straight after the first stairs | 5 | `self.logic = lambda _: True` | 
| Left side (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Right side (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Kasplat room | Balloon | `self.logic = lambda _: True` | 
## Aztec Llama Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance stairs (9 custom, 6 Lanky) | 15 | `self.logic = lambda _: True` | 
| Around water/lava | 15 | `self.logic = lambda _: True` | 
| Bottom of stairs to Llama | 20 | `self.logic = lambda _: True` | 
| W2 in Llama temple | 5 | `self.logic = lambda _: True` | 
| W2 in Llama temple | 5 | `self.logic = lambda _: True` | 
| Bottom of stairs to W1 | 10 | `self.logic = lambda _: True` | 
| Leading to Trombone Tremor pad | 10 | `self.logic = lambda _: True` | 
| W1 (1 custom, 1 Lanky bunch) | 10 | `self.logic = lambda _: True` | 
| Behind and above llama | 10 | `self.logic = lambda _: True` | 
| All around Llama Temple (Donkey) | 15 | `self.logic = lambda _: True` | 
| Llama Temple Water Corners | 20 | `Events.AztecLlamaSpit in l.Events and l.swim` | 
| To lava room (Tiny) | 3 | `self.logic = lambda _: True` | 
| To lava room (Tiny) | 2 | `self.logic = lambda _: True` | 
| On Tiny switches in lava room (Tiny) | 10 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.monkey_maneuvers)) and l.istiny` | 
| On vines in Matching game room (Lanky) | 5 | `l.can_use_vines` | 
| Entrance sides | 10 | `self.logic = lambda _: True` | 
| Pool corners | 10 | `self.logic = lambda _: True` | 
| Around the melon crate | 10 | `self.logic = lambda _: True` | 
| Around the trombone pad | 5 | `self.logic = lambda _: True` | 
| On the extended dinosnakes | 10 | `l.handstand and l.trombone` | 
| Behind the bongo pad | 5 | `self.logic = lambda _: True` | 
| Surface of the pool | 10 | `Events.AztecLlamaSpit in l.Events` | 
| Surface of the pool but bigger | 10 | `Events.AztecLlamaSpit in l.Events` | 
| On the sealed quicksand tunnel switch | 5 | `self.logic = lambda _: True` | 
| On the llama's head | 5 | `self.logic = lambda _: True` | 
| Along the walls behind the llama | 10 | `self.logic = lambda _: True` | 
| In front of the matching game door | 5 | `self.logic = lambda _: True` | 
| Twirl above the llama | 5 | `l.twirl` | 
| Matching game switch | 5 | `self.logic = lambda _: True` | 
| Towards the matching game switch | 5 | `self.logic = lambda _: True` | 
| On the mini tunnel | 5 | `self.logic = lambda _: True` | 
| On the lava pedestals first switch | 5 | `self.logic = lambda _: True` | 
| Lower ledge of the pedestal switch platforms | 10 | `(l.CanSlamSwitch(Levels.AngryAztec, 1) or (l.twirl and l.monkey_maneuvers))` | 
| Passage towards Lanky's cage | 5 | `(((Events.AztecLlamaSpit in l.Events or (l.CanPhaseswim() and l.settings.damage_amount != DamageAmount.ohko) and l.swim)) or l.CanPhase())` | 
| In front of Lanky's cage | 5 | `(((Events.AztecLlamaSpit in l.Events or (l.CanPhaseswim() and l.settings.damage_amount != DamageAmount.ohko) and l.swim)) or l.CanPhase())` | 
| Matching game room right side | Balloon | `self.logic = lambda _: True` | 
| Above Llama | Balloon | `self.logic = lambda _: True` | 
| Lava room | Balloon | `self.logic = lambda _: True` | 
| Above lava/water (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In Lanky's room (Lanky) | Balloon | `(((Events.AztecLlamaSpit in l.Events or (l.CanPhaseswim() and l.settings.damage_amount != DamageAmount.ohko) and l.swim)) or l.CanPhase())` | 
| In Lanky's room (Lanky) | Balloon | `(((Events.AztecLlamaSpit in l.Events or (l.CanPhaseswim() and l.settings.damage_amount != DamageAmount.ohko) and l.swim)) or l.CanPhase())` | 
| Entrance stairs | Balloon | `self.logic = lambda _: True` | 
| Left side behind the llama | Balloon | `self.logic = lambda _: True` | 
| Right side behind the llama | Balloon | `self.logic = lambda _: True` | 
| Matching game | Balloon | `self.logic = lambda _: True` | 
| Mini tunnel room arch | Balloon | `self.logic = lambda _: True` | 
| Splashing in the lava room | Balloon | `self.logic = lambda _: True` | 
## Aztec Tiny Temple
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In Vulture room (1 custom, 9 Lanky) | 10 | `self.logic = lambda _: True` | 
| Underwater square room corners | 20 | `self.logic = lambda _: True` | 
| Monkey tongues (2 custom, 3 Diddy) | 5 | `l.CanSlamSwitch(Levels.AngryAztec, 1)` | 
| Path to Free Tiny (3 custom, 7 Diddy) | 10 | `self.logic = lambda _: True` | 
| Path to Chunky's room (1 custom, 4 Chunky) | 5 | `self.logic = lambda _: True` | 
| On vulture GB switch (Lanky) | 5 | `self.logic = lambda _: True` | 
| Long monkey tongue (Diddy) | 15 | `l.CanSlamSwitch(Levels.AngryAztec, 1) and l.peanut` | 
| Mini Monkey tunnel (Tiny) | 5 | `l.mini or l.CanPhaseswim()` | 
| In corner around torch (Chunky) | 25 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| Around the pool | 10 | `self.logic = lambda _: True` | 
| Stairs near Mini barrel | 5 | `self.logic = lambda _: True` | 
| Diddy switch | 5 | `self.logic = lambda _: True` | 
| Klaptrap room peek spot | 5 | `self.logic = lambda _: True` | 
| Middle of the underwater square room | 10 | `self.logic = lambda _: True` | 
| In the Tiny cage room | 15 | `self.logic = lambda _: True` | 
| In the O of KONG | 5 | `self.logic = lambda _: True` | 
| Mini Monkey alcove | Balloon | `self.logic = lambda _: True` | 
| Tiny's room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Tiny's room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Vulture room (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Near the Chunky klaptrap room | Balloon | `self.logic = lambda _: True` | 
| Above the pool | Balloon | `self.logic = lambda _: True` | 
| Vulture path | Balloon | `self.logic = lambda _: True` | 
| KONG above the cage | Balloon | `self.logic = lambda _: True` | 

# Frantic Factory
## Frantic Factory
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance on K. Rool mat | 5 | `self.logic = lambda _: True` | 
| Around hatch | 10 | `self.logic = lambda _: True` | 
| On Hatch switch | 5 | `self.logic = lambda _: True` | 
| Hatch switch room left wall | 5 | `self.logic = lambda _: True` | 
| Hatch switch room on console | 10 | `self.logic = lambda _: True` | 
| W3 (1 custom, 1 Chunky) | 5 | `self.logic = lambda _: True` | 
| W3 (1 custom, 1 Chunky) | 5 | `self.logic = lambda _: True` | 
| Snide room on metal boxes | 10 | `self.logic = lambda _: True` | 
| Pole from entrance to testing - upper room | 10 | `self.logic = lambda _: True` | 
| Tunnel to Snide room | 5 | `self.logic = lambda _: True` | 
| Snide room pole - upper room | 10 | `self.logic = lambda _: True` | 
| Block tower room under stairs with DK coins | 15 | `self.logic = lambda _: True` | 
| Block tower room on top of DK coins stairs in front of window | 5 | `self.logic = lambda _: True` | 
| On the floor at the base of block tower | 10 | `self.logic = lambda _: True` | 
| On corner block of Block tower | 5 | `self.logic = lambda _: True` | 
| Block tower room on box pile to tag barrel | 5 | `self.logic = lambda _: True` | 
| Block tower room on box by tag barrel | 5 | `self.logic = lambda _: True` | 
| Block tower room on grate between Mini Monkey and Tag barrel | 5 | `self.logic = lambda _: True` | 
| Block tower room by tunnel to spinning wheel (1 custom, 1 Tiny bunch) | 10 | `self.logic = lambda _: True` | 
| All around Block tower room | 20 | `self.logic = lambda _: True` | 
| Around numbers game | 10 | `self.logic = lambda _: True` | 
| Tunnel to numbers game (5 custom, 5 Donkey) | 10 | `self.logic = lambda _: True` | 
| Block tower (lower block towards R&D and tunnel to numbers game) | 5 | `((l.spring or l.CanMoontail()) and l.isdiddy) or (l.balloon and l.islanky)` | 
| Block tower (R block near top) | 5 | `l.spring or l.CanMoontail()` | 
| Block tower (middle D block on the right path up) | 5 | `l.spring or l.CanMoontail()` | 
| Pole to R&D - lower room | 10 | `self.logic = lambda _: True` | 
| R&D Pole | 5 | `self.logic = lambda _: True` | 
| R&D pole - upper room | 10 | `self.logic = lambda _: True` | 
| Tunnel from pole to R&D room | 5 | `self.logic = lambda _: True` | 
| Lower R&D pathway (10 custom, 5 Lanky) | 15 | `self.logic = lambda _: True` | 
| R&D in grate with 4 Chunky coins | 5 | `(l.grab and l.donkey) or l.CanPhase()` | 
| Tunnel from R&D room to above Power shed | 5 | `self.logic = lambda _: True` | 
| R&D corners of room with lever | 10 | `self.logic = lambda _: True` | 
| Corners of Car race room (right) | 10 | `l.mini or l.CanPhase()` | 
| Corners of Car race room (left) | 10 | `l.mini or l.CanPhase()` | 
| Diddy R&D room | 10 | `l.guitar or l.CanPhase()` | 
| Diddy R&D room in front of 4 buttons | 20 | `l.guitar or l.CanPhase()` | 
| Leading to Chunky R&D room | 2 | `l.punch and l.chunky and l.climbing` | 
| Leading to Chunky R&D room | 3 | `self.logic = lambda _: True` | 
| Chunky R&D room behind chest | 10 | `l.CanAccessRNDRoom() or (l.punch and l.triangle and l.climbing)` | 
| Lanky R&D room upper 3 barrels | 15 | `l.CanAccessRNDRoom() or l.trombone` | 
| Lanky R&D room lower 3 barrels | 15 | `l.CanAccessRNDRoom() or l.trombone` | 
| On F Key | 5 | `l.CanAccessRNDRoom() or l.trombone` | 
| Side walls of Lanky R&D room | 10 | `l.CanAccessRNDRoom() or l.trombone` | 
| In fall from the hatch to power shed | 5 | `self.logic = lambda _: True` | 
| In Dark room on box | 5 | `l.punch or l.CanPhase()` | 
| On Simian Spring ledge with coins | 10 | `((l.spring or l.CanMoontail()) and l.isdiddy) or l.CanPhase()` | 
| On box in stack of boxes to Candy/Cranky - left | 5 | `self.logic = lambda _: True` | 
| On box in stack of boxes to Candy/Cranky - right | 5 | `self.logic = lambda _: True` | 
| From BBlast pad to Tiny BP pole | 5 | `self.logic = lambda _: True` | 
| From Prod room to Chunky room (1 custom, 4 Donkey) | 5 | `self.logic = lambda _: True` | 
| Bottom of production room (3 custom, 12 Diddy) | 15 | `self.logic = lambda _: True` | 
| Prod room Chunky switch | 5 | `self.logic = lambda _: True` | 
| Prod room Diddy switch | 5 | `self.logic = lambda _: True` | 
| Prod room Lanky switch | 5 | `self.logic = lambda _: True` | 
| Prod room Tiny switch | 5 | `self.logic = lambda _: True` | 
| Prod room from elevator to center | 15 | `self.logic = lambda _: True` | 
| Prod room around center piece (lower floor) | 15 | `self.logic = lambda _: True` | 
| Prod room around center piece (higher floor) | 10 | `self.logic = lambda _: True` | 
| Prod room on spinning cylinder out from center piece | 5 | `self.logic = lambda _: True` | 
| Bunches on W4 | 5 | `self.logic = lambda _: True` | 
| Bunches on W4 | 5 | `self.logic = lambda _: True` | 
| Prod room upper level from elevators to spinning cylinders | 15 | `self.logic = lambda _: True` | 
| Prod room below Tiny conveyors | 10 | `self.logic = lambda _: True` | 
| Prod room on box-shaped vents below the upper level | 15 | `self.logic = lambda _: True` | 
| From long pole to prod room (4 custom, 6 Donkey) | 10 | `self.logic = lambda _: True` | 
| Bottom of long pole around room | 10 | `self.logic = lambda _: True` | 
| Pole room to arcade | 10 | `self.logic = lambda _: True` | 
| Pole room to arcade around pole | 10 | `self.logic = lambda _: True` | 
| Tunnel to Stash Snatch | 5 | `self.logic = lambda _: True` | 
| Stash Snatch room | 10 | `l.punch` | 
| Under W5 table | 5 | `self.logic = lambda _: True` | 
| Under table to Mini Monkey GB | 15 | `self.logic = lambda _: True` | 
| On table to Mini Monkey GB | 10 | `self.logic = lambda _: True` | 
| On DK Arcade | 5 | `self.logic = lambda _: True` | 
| Tunnel to DK Arcade (5 custom, 5 Diddy) | 10 | `self.logic = lambda _: True` | 
| Funky room boxes on left | 10 | `self.logic = lambda _: True` | 
| Funky room on high boxes | 5 | `self.logic = lambda _: True` | 
| Around Funky platform | 15 | `self.logic = lambda _: True` | 
| Funky's room boxes on right | 10 | `self.logic = lambda _: True` | 
| Tunnel to Funky's room (2 custom, 3 Diddy) | 5 | `self.logic = lambda _: True` | 
| Funky's room around Funky's platform | 10 | `self.logic = lambda _: True` | 
| Bunches around Funky's store | 15 | `self.logic = lambda _: True` | 
| Production room spinning arms, inside ring (Chunky) | 10 | `self.logic = lambda _: True` | 
| Production room spinning arms, outside ring (Chunky) | 10 | `self.logic = lambda _: True` | 
| Dark room above moving platforms (Chunky) | 15 | `l.punch` | 
| Tunnel from entrance to hatch (Donkey) | 5 | `self.logic = lambda _: True` | 
| Block tower (set of 3 bunches) (Diddy) | 15 | `l.spring or l.CanMoontail()` | 
| Block tower (set of 2 bunches) (Diddy) | 10 | `l.spring or l.CanMoontail()` | 
| W5 (Diddy) | 5 | `self.logic = lambda _: True` | 
| W5 (Diddy) | 5 | `self.logic = lambda _: True` | 
| Prod room rotating cylinders (Diddy) | 15 | `self.logic = lambda _: True` | 
| R&D upper walkway (Lanky) | 5 | `self.logic = lambda _: True` | 
| Path from stack of boxes to Candy & Cranky (Lanky) | 5 | `self.logic = lambda _: True` | 
| Pipe in corner of Chunky's room (Lanky) | 4 | `self.logic = lambda _: True` | 
| Pipe in corner of Chunky's room (Lanky) | 1 | `self.logic = lambda _: True` | 
| Pipe at the top of Prod room (Lanky) | 20 | `l.handstand or l.CanPhase()` | 
| Pipe at the top of Prod room (Lanky) | 5 | `self.logic = lambda _: True` | 
| Prod room on the middle steps between rotating cylinders and the spinning arms (Lanky) | 15 | `self.logic = lambda _: True` | 
| W2 (Lanky) | 5 | `self.logic = lambda _: True` | 
| W2 (Lanky) | 5 | `self.logic = lambda _: True` | 
| Tunnel from starting room towards Testing (2 custom, 3 Tiny) | 5 | `self.logic = lambda _: True` | 
| Tunnel from pole past blue switch gate to T junction (3 custom, 2 Tiny) | 5 | `self.logic = lambda _: True` | 
| Tunnel from T junction to block tower (Tiny) | 5 | `self.logic = lambda _: True` | 
| Tunnel to Car race (Tiny) | 10 | `self.logic = lambda _: True` | 
| Prod room on conveyors to bonus barrel (Tiny) | 20 | `self.logic = lambda _: True` | 
| Prod room on far platform past Bonus Barrel (Tiny) | 5 | `l.twirl` | 
| Arcade room, by Mini Monkey tunnel (Tiny) | 5 | `self.logic = lambda _: True` | 
| In Spinning wheel room (Tiny) | 5 | `l.mini or l.CanPhase()` | 
| By middle window outside of production room (Tiny) | 10 | `self.logic = lambda _: True` | 
| On pole down hatch (Chunky) | 10 | `Events.HatchOpened in l.Events` | 
| Chunky R&D room left side (Chunky) | 5 | `(l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()` | 
| Chunky R&D room right side (Chunky) | 5 | `(l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()` | 
| W1 (Chunky) | 5 | `self.logic = lambda _: True` | 
| W1 (Chunky) | 5 | `self.logic = lambda _: True` | 
| Entrance portal | 5 | `self.logic = lambda _: True` | 
| Lobby factory-map | 5 | `self.logic = lambda _: True` | 
| Krem Co. clock | 5 | `self.logic = lambda _: True` | 
| Windows of the hatch | 15 | `self.logic = lambda _: True` | 
| Production factory-map | 5 | `self.logic = lambda _: True` | 
| Production Reject line | 5 | `self.logic = lambda _: True` | 
| Production Accept line | 5 | `self.logic = lambda _: True` | 
| In front of the crusher entrance | 5 | `self.logic = lambda _: True` | 
| In the big piston | 5 | `Events.MainCoreActivated in l.Events` | 
| First elevator to upper production room | 5 | `self.logic = lambda _: True` | 
| Second elevator to upper production room | 5 | `self.logic = lambda _: True` | 
| Third elevator to upper production room | 5 | `self.logic = lambda _: True` | 
| Upper production tag barrel | 5 | `self.logic = lambda _: True` | 
| Spring jump in upper production | 5 | `l.spring, locations=[[5, 1.0, 585, 720, 1628]]` | 
| Twirl from Tiny's highest spot in production to a very cursed vent | 10 | `l.twirl` | 
| On the vent right under Lanky's pipe | 5 | `l.handstand` | 
| Storage factory-map | 5 | `self.logic = lambda _: True` | 
| On the door frame to arcade | 5 | `l.spring` | 
| Boxes near the storage pipe | 5 | `self.logic = lambda _: True` | 
| Storage metal support beam | 5 | `self.logic = lambda _: True` | 
| Among the storage boxes | 10 | `self.logic = lambda _: True` | 
| Between the storage shops | 5 | `self.logic = lambda _: True` | 
| Between boxes near the storage shops | 10 | `self.logic = lambda _: True` | 
| Dark room entrance | 5 | `l.chunky and l.punch` | 
| Box in a corner of dark room | 5 | `l.chunky and l.punch` | 
| On the table around warp 5 | 10 | `self.logic = lambda _: True` | 
| Lower step of Snide | 5 | `self.logic = lambda _: True` | 
| Testing factory-map | 5 | `self.logic = lambda _: True` | 
| Triangle shoot-blocks near arcade window | 15 | `self.logic = lambda _: True` | 
| Triangle shoot-blocks near number game | 15 | `self.logic = lambda _: True` | 
| Triangle shoot-block to Funky | 5 | `self.logic = lambda _: True` | 
| Mini-block steps up the block tower | 10 | `l.spring or l.CanMoontail()` | 
| Under testing tag barrel | 5 | `self.logic = lambda _: True` | 
| On the number game | 10 | `self.logic = lambda _: True` | 
| Lower tunnel to R&D | 5 | `self.logic = lambda _: True` | 
| Upper tunnel to R&D | 5 | `self.logic = lambda _: True` | 
| R&D factory-map | 5 | `self.logic = lambda _: True` | 
| Between the car race windows | 5 | `self.logic = lambda _: True` | 
| Toy sales board in the lever room | 5 | `self.logic = lambda _: True` | 
| On the R&D trombone pad | 5 | `self.logic = lambda _: True` | 
| On the R&D guitar pad | 5 | `self.logic = lambda _: True` | 
| On the R&D triangle pad | 5 | `l.chunky and l.punch and l.climbing` | 
| Power hut coconut switch | 5 | `self.logic = lambda _: True` | 
| First room left corner | Balloon | `self.logic = lambda _: True` | 
| First room right side | Balloon | `self.logic = lambda _: True` | 
| First room by robots left side | Balloon | `self.logic = lambda _: True` | 
| Tunnel by Snide's window | Balloon | `self.logic = lambda _: True` | 
| Pole to block tower lower room | Balloon | `self.logic = lambda _: True` | 
| Pole to block tower upper room | Balloon | `self.logic = lambda _: True` | 
| Tunnel between Snide's and block tower | Balloon | `self.logic = lambda _: True` | 
| Block tower room above arcade window | Balloon | `self.logic = lambda _: True` | 
| Block tower room above block tower | Balloon | `l.spring or l.CanMoontail()` | 
| Around bottom of block tower | Balloon | `self.logic = lambda _: True` | 
| Block tower room in front of numbers game window | Balloon | `self.logic = lambda _: True` | 
| Tunnel to numbers game | Balloon | `self.logic = lambda _: True` | 
| Block tower room by Mini Monkey barrel | Balloon | `self.logic = lambda _: True` | 
| Block tower room by tag barrel | Balloon | `self.logic = lambda _: True` | 
| Funky's room high and around room | Balloon | `self.logic = lambda _: True` | 
| In spinning wheel room | Balloon | `l.mini or l.CanPhase()` | 
| Pole to R&D lower room | Balloon | `self.logic = lambda _: True` | 
| Pole to R&D upper room | Balloon | `self.logic = lambda _: True` | 
| R&D left side | Balloon | `self.logic = lambda _: True` | 
| Piano game right side | Balloon | `l.trombone or l.CanAccessRNDRoom()` | 
| In window by car race Mini Monkey | Balloon | `self.logic = lambda _: True` | 
| Tunnel to car race | Balloon | `self.logic = lambda _: True` | 
| Chunky R&D room | Balloon | `(l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom()` | 
| Cranky/Candy room | Balloon | `self.logic = lambda _: True` | 
| Chunky room above blue switch | Balloon | `self.logic = lambda _: True` | 
| Chunky room above dark room entrance | Balloon | `self.logic = lambda _: True` | 
| Dark room | Balloon | `l.punch or l.CanPhase()` | 
| Arcade room | Balloon | `self.logic = lambda _: True` | 
| Production room very top | Balloon | `self.logic = lambda _: True` | 
| Production room near wall under Lanky pipe | Balloon | `self.logic = lambda _: True` | 
| Production room in front of middle window | Balloon | `self.logic = lambda _: True` | 
| Production room in front of high window | Balloon | `self.logic = lambda _: True` | 
| Around hatch (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Top of pole by Snide (Chunky) | Balloon | `self.logic = lambda _: True` | 
| In piano game room (Lanky) | Balloon | `(l.trombone or l.CanAccessRNDRoom())` | 
| In front of Snide (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In Diddy's R&D room (back) (Diddy) | Balloon | `l.guitar or l.CanAccessRNDRoom()` | 
| In Diddy's R&D room (front) (Diddy) | Balloon | `l.guitar or l.CanAccessRNDRoom()` | 
| In R&D above hatch to Chunky's room (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In front of Candy & Cranky (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Around numbers game (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In Diddy's R&D room (left) (Diddy) | Balloon | `l.guitar or l.CanAccessRNDRoom()` | 
| Prod room, by center (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In front of Funky (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Prod room, by highest tag barrel (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Chunky R&D room (Chunky) | Balloon | `((l.punch and l.triangle and l.climbing) or l.CanAccessRNDRoom())` | 
| Top of the hatch | Balloon | `self.logic = lambda _: True` | 
| Tunnel from hatch to production | Balloon | `self.logic = lambda _: True` | 
| Around the lower production pipe | Balloon | `self.logic = lambda _: True` | 
| Around the rotating pipe | Balloon | `self.logic = lambda _: True` | 
| Around the big piston | Balloon | `self.logic = lambda _: True` | 
| Around the Lanky pipe | Balloon | `self.logic = lambda _: True` | 
| Along the storage pipe | Balloon | `self.logic = lambda _: True` | 
| Above the headphones | Balloon | `self.logic = lambda _: True` | 
| Arcade machine | Balloon | `self.logic = lambda _: True` | 
| Window of the number game | Balloon | `self.logic = lambda _: True` | 
| Shoot at the moon | Balloon | `l.spring or l.CanMoontail()` | 
| Ceiling pipe towards Funky | Balloon | `self.logic = lambda _: True` | 
| Top of pole to R&D | Balloon | `self.logic = lambda _: True` | 
| R&D right side | Balloon | `self.logic = lambda _: True` | 
## Factory Power Hut
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On box-shaped vents | 10 | `self.logic = lambda _: True` | 
| On boxes in corners (Donkey) | 15 | `self.logic = lambda _: True` | 
## Factory Crusher
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On conveyors (Donkey) | 15 | `l.strongKong` | 
| In crusher room (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Under the last crusher | Balloon | `l.strongKong` | 
## Factory Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Baboon Blast group 1 (Donkey) | 10 | `self.logic = lambda _: True` | 
| Baboon Blast group 2 (Donkey) | 10 | `self.logic = lambda _: True` | 

# Gloomy Galleon
## Gloomy Galleon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance (5 custom, 5 Lanky) | 10 | `self.logic = lambda _: True` | 
| Tunnel to cannon game room | 5 | `self.logic = lambda _: True` | 
| Tunnels to Lighthouse and 5DS area (6 custom, 9 Tiny) | 15 | `self.logic = lambda _: True` | 
| To Cranky area (3 custom, 2 Chunky) | 5 | `self.logic = lambda _: True` | 
| Tunnel to Chests room (5 custom, 5 Chunky) | 10 | `self.logic = lambda _: True` | 
| Around Chunky chest room | 10 | `self.logic = lambda _: True` | 
| Inside middle chest with headphones | 5 | `l.punch` | 
| Inside left chest with Fairy | 5 | `l.punch` | 
| In alcove to chest room by Chunky coins | 10 | `self.logic = lambda _: True` | 
| On left side of ship to chests room | 5 | `self.logic = lambda _: True` | 
| On each side of Cranky's Lab ship at the bottom | 10 | `self.logic = lambda _: True` | 
| On wooden box (5DS side) | 10 | `self.logic = lambda _: True` | 
| Around battle arena pad | 5 | `l.punch or l.CanPhase()` | 
| Back wall of Cranky area at the bottom | 15 | `self.logic = lambda _: True` | 
| Between the two cannons in Cranky room | 5 | `self.logic = lambda _: True` | 
| Cranky room inside wall | 10 | `self.logic = lambda _: True` | 
| Stack of boxes by W2 | 5 | `self.logic = lambda _: True` | 
| On ship to chests room | 10 | `self.logic = lambda _: True` | 
| To Tiny BP (2 custom, 3 Tiny) | 5 | `self.logic = lambda _: True` | 
| Cranky's Room to T&S (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Cannon GB room boulder side | 10 | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Cannon GB room cannon side | 15 | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Cannon game room underwater | 10 | `l.swim` | 
| On top of stalactite near 2DS | 5 | `self.logic = lambda _: True` | 
| Under ship tunnel by 5DS (with oranges) | 15 | `self.logic = lambda _: True` | 
| In chest by 5DS (Chunky OoB coins) | 5 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| In chest by 5DS (Lanky coins) | 5 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Chest around 5DS (DK coins) | 5 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Chest around 5DS (Tiny coins) | 5 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| Chest near mech fish (Diddy coins) | 5 | `Events.ShipyardEnguarde in l.Events or l.CanPhaseswim()` | 
| From 5DS to Mech fish on sea floor | 5 | `self.logic = lambda _: True` | 
| From 5DS to 2DS on sea floor | 5 | `self.logic = lambda _: True` | 
| On underwater mast of 2DS | 5 | `self.logic = lambda _: True` | 
| Tunnel to gold tower room (4 custom, 6 Diddy) | 10 | `self.logic = lambda _: True` | 
| Seafloor around Lanky gold tower | 10 | `self.logic = lambda _: True` | 
| 4 corners of gold tower room | 20 | `self.logic = lambda _: True` | 
| On Lanky Gold Tower (5 custom, 5 Lanky) | 9 | `l.balloon and ((Events.WaterRaised in l.Events) or (Events.ShipyardEnguarde in l.Events and l.monkey_maneuvers))` | 
| On Lanky Gold Tower (5 custom, 5 Lanky) | 1 | `l.balloon and ((Events.WaterRaised in l.Events) or (Events.ShipyardEnguarde in l.Events and l.monkey_maneuvers))` | 
| On Diddy gold tower | 15 | `self.logic = lambda _: True` | 
| W4 | 5 | `self.logic = lambda _: True` | 
| W4 | 5 | `self.logic = lambda _: True` | 
| On wooden box (lighthouse side) | 10 | `self.logic = lambda _: True` | 
| Around Candy's Store | 20 | `self.logic = lambda _: True` | 
| By Seal race | 10 | `self.logic = lambda _: True` | 
| On ship part by Candy's store | 10 | `Events.WaterRaised in l.Events` | 
| By submarine entrance | 5 | `self.logic = lambda _: True` | 
| On seafloor from 5DS to submarine area | 10 | `self.logic = lambda _: True` | 
| On floating plank with 4 DK coins | 10 | `Events.WaterRaised in l.Events` | 
| Plank in front of Funky (Melon crate) | 10 | `Events.WaterRaised in l.Events` | 
| On stalactite between 5DS and mech fish | 5 | `self.logic = lambda _: True` | 
| Around Funky's store | 20 | `self.logic = lambda _: True` | 
| Cactus on guitar pad | 5 | `self.logic = lambda _: True` | 
| Cactus on bongo pad | 5 | `self.logic = lambda _: True` | 
| Cactus on saxophone pad | 5 | `self.logic = lambda _: True` | 
| Cactus on top | 5 | `self.logic = lambda _: True` | 
| Cactus on top between coins | 5 | `self.logic = lambda _: True` | 
| Bottom around cactus | 15 | `self.logic = lambda _: True` | 
| Bottom on stalactites around submarine | 20 | `self.logic = lambda _: True` | 
| In corner behind cactus above the water surface | 10 | `Events.WaterRaised in l.Events` | 
| Alcove behind Enguarde plank | 20 | `self.logic = lambda _: True` | 
| Around tag barrel near enguarde box (Lighthouse area) | 5 | `self.logic = lambda _: True` | 
| Bottom of water around chest between tag barrel and mermaid area | 15 | `self.logic = lambda _: True` | 
| Bottom of water near mermaid on seashells (Right) | 10 | `self.logic = lambda _: True` | 
| Bottom of water near mermaid on seashells (Center) | 15 | `self.logic = lambda _: True` | 
| Bottom of water near mermaid on seashells (Left) | 10 | `self.logic = lambda _: True` | 
| Bottom on each side of mermaid entrance | 10 | `self.logic = lambda _: True` | 
| Mermaid area top of pillars on each side | 10 | `self.logic = lambda _: True` | 
| Mermaid area just under tag barrel | 5 | `self.logic = lambda _: True` | 
| Bunches leading down to bottom T&S | 20 | `self.logic = lambda _: True` | 
| Bottom of Lighthouse area around T&S portal | 10 | `self.logic = lambda _: True` | 
| Around hole leading to bottom T&S | 10 | `self.logic = lambda _: True` | 
| In front of water lowering switch | 5 | `self.logic = lambda _: True` | 
| In front of water raising switch | 5 | `self.logic = lambda _: True` | 
| W1 | 5 | `self.logic = lambda _: True` | 
| W1 | 5 | `self.logic = lambda _: True` | 
| W5 | 5 | `self.logic = lambda _: True` | 
| W5 | 5 | `self.logic = lambda _: True` | 
| Lighthouse switch | 5 | `self.logic = lambda _: True` | 
| Baboon Blast pad | 5 | `self.logic = lambda _: True` | 
| Around lighthouse | 10 | `self.logic = lambda _: True` | 
| On triangle pad by Diddy's BP | 5 | `self.logic = lambda _: True` | 
| On seal cage | 10 | `l.jetpack` | 
| Guitar pad on top of lighthouse | 5 | `l.jetpack` | 
| Up the ladder into the lighthouse | 5 | `self.logic = lambda _: True` | 
| Around Diddy BP | 15 | `self.logic = lambda _: True` | 
| In alcove behind Enguarde box (Donkey) | 10 | `self.logic = lambda _: True` | 
| Under ship tunnel by 5DS (Donkey) | 15 | `self.logic = lambda _: True` | 
| On top of lighthouse (Diddy) | 10 | `l.jetpack` | 
| Around 2DS on seafloor (Diddy) | 10 | `self.logic = lambda _: True` | 
| In cannon path to Cranky (Diddy) | 10 | `self.logic = lambda _: True` | 
| On seafloor around mech fish (Diddy) | 20 | `self.logic = lambda _: True` | 
| On seafloor around enguarde chest in lighthouse area (Lanky) | 5 | `self.logic = lambda _: True` | 
| Under Enguarde box on 5DS (Lanky) | 5 | `self.logic = lambda _: True` | 
| On cactus trombone pad (Lanky) | 5 | `self.logic = lambda _: True` | 
| In chest right of Enguarde box (Lanky) | 5 | `(Events.LighthouseEnguarde in l.Events or l.CanPhaseswim())` | 
| In chest left of Enguarde box (Lanky) | 5 | `(Events.LighthouseEnguarde in l.Events or l.CanPhaseswim())` | 
| In chest close to mermaid (Lanky) | 5 | `(Events.LighthouseEnguarde in l.Events or l.CanPhaseswim())` | 
| In chest close to T&S hole (Lanky) | 5 | `(Events.LighthouseEnguarde in l.Events or l.CanPhaseswim())` | 
| W3 (Tiny) | 5 | `self.logic = lambda _: True` | 
| W3 (Tiny) | 5 | `self.logic = lambda _: True` | 
| In front of Tiny's treasure chest (Tiny) | 5 | `self.logic = lambda _: True` | 
| In cannon game room over planks (Tiny) | 15 | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| On seafloor around lighthouse (Chunky) | 10 | `self.logic = lambda _: True` | 
| W2 (Chunky) | 5 | `Events.WaterRaised in l.Events` | 
| W2 (Chunky) | 5 | `self.logic = lambda _: True` | 
| Under ship tunnel by 5DS (Chunky) | 15 | `self.logic = lambda _: True` | 
| Around poles in cannon game room | 10 | `Events.WaterLowered in l.Events or l.swim` | 
| On the cannon game cannon | 5 | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Where the lighthouse sign is pointing | 5 | `self.logic = lambda _: True` | 
| Torch above Lanky switch | 5 | `self.logic = lambda _: True` | 
| Torch above Tiny switch | 5 | `self.logic = lambda _: True` | 
| First cannon shot to the wreck | 5 | `self.logic = lambda _: True` | 
| Around the big pole of the caverns | 10 | `self.logic = lambda _: True` | 
| Bow of Cranky's wreck | 5 | `self.logic = lambda _: True` | 
| Klobber and Kaboom in the tunnel | 10 | `self.logic = lambda _: True` | 
| Front of the chests | 5 | `self.logic = lambda _: True` | 
| Twirl from the upper planks | 5 | `l.twirl` | 
| In the water around the lighthouse platform | 10 | `Events.WaterLowered in l.Events or l.swim` | 
| On Kevin's spot (lighthouse alcove) | 5 | `self.logic = lambda _: True` | 
| Ceiling of the Enguarde cave | 5 | `Events.WaterRaised in l.Events` | 
| Rocket around the lighthouse | 15 | `l.jetpack` | 
| Algae near Enguarde crate | 15 | `self.logic = lambda _: True` | 
| Algae near the pit | 20 | `self.logic = lambda _: True` | 
| Algae near the center pillar | 10 | `self.logic = lambda _: True` | 
| Algae near the intermediate chest | 10 | `self.logic = lambda _: True` | 
| Algae at the very bottom | 15 | `self.logic = lambda _: True` | 
| Seal race entrance | 5 | `Events.WaterRaised in l.Events` | 
| In the DK star | 5 | `Events.ShipyardEnguarde in l.Events and (Events.WaterRaised in l.Events or l.monkey_maneuvers)` | 
| Around the cactus trunk | 10 | `self.logic = lambda _: True` | 
| On big spike between 5DS and submarine | 5 | `self.logic = lambda _: True` | 
| Top of wreck under shipyard entrance | 5 | `self.logic = lambda _: True` | 
| Top of wreck under tunnel to treasure room | 5 | `self.logic = lambda _: True` | 
| Top of wreck towards Funky area | 10 | `self.logic = lambda _: True` | 
| Chunky 5DS entrance | 5 | `self.logic = lambda _: True` | 
| Top of the 2DS | 5 | `self.logic = lambda _: True` | 
| Railings on the 5DS | 10 | `self.logic = lambda _: True` | 
| Around the tunnel to treasure room | 10 | `self.logic = lambda _: True` | 
| Big spike near the mechfish cage | 5 | `self.logic = lambda _: True` | 
| Top of the Diddy gold tower | 10 | `self.logic = lambda _: True` | 
| Underwater against the Diddy gold tower | 5 | `self.logic = lambda _: True` | 
| Underwater against the Lanky gold tower | 5 | `self.logic = lambda _: True` | 
| Cannon game room | Balloon | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Between W2 and Tiny BP | Balloon | `self.logic = lambda _: True` | 
| Between left side of ship and T&S portal | Balloon | `self.logic = lambda _: True` | 
| Around Cranky | Balloon | `self.logic = lambda _: True` | 
| Around top of lighthouse | Balloon | `l.jetpack` | 
| In front of Funky's | Balloon | `self.logic = lambda _: True` | 
| In front of Candy's | Balloon | `self.logic = lambda _: True` | 
| High in gold tower room | Balloon | `self.logic = lambda _: True` | 
| Around cactus (Diddy) | Balloon | `self.logic = lambda _: True` | 
| By Diddy BP (Tiny) | Balloon | `Events.WaterLowered in l.Events` | 
| Above battle crown pad 1 (Lanky) | Balloon | `(l.punch and l.chunky) or l.CanPhase()` | 
| Above battle crown pad 2 (Lanky) | Balloon | `((l.punch and l.chunky) or l.CanPhase())` | 
| Around cactus (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Above seal cage (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Around lighthouse (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In chests room (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In gold tower room (Diddy) | Balloon | `self.logic = lambda _: True` | 
| By cannon in cannon game room (Chunky) | Balloon | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Above 2DS (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Above 5DS (Lanky) | Balloon | `self.logic = lambda _: True` | 
| In front of Snide (Tiny) | Balloon | `Events.WaterRaised in l.Events` | 
| In gold tower room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Around the cannonball | Balloon | `(Events.WaterRaised in l.Events or (l.monkey_maneuvers and ((l.islanky and not l.isKrushaAdjacent(Kongs.lanky)) or l.ischunky)))` | 
| Entrance tunnel | Balloon | `self.logic = lambda _: True` | 
| Tunnel to shipyard | Balloon | `self.logic = lambda _: True` | 
| Tunnel to lighthouse | Balloon | `self.logic = lambda _: True` | 
| Tunnel to chests | Balloon | `self.logic = lambda _: True` | 
| Near lighthouse warp 1 | Balloon | `self.logic = lambda _: True` | 
| Near shipyard warp 4 | Balloon | `self.logic = lambda _: True` | 
| Near shipyard warp 5 | Balloon | `self.logic = lambda _: True` | 
| Between the gold towers | Balloon | `self.logic = lambda _: True` | 
## Galleon Sick Bay
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Each side of cannon | 10 | `self.logic = lambda _: True` | 
| In main hallway (Chunky) | 20 | `self.logic = lambda _: True` | 
| In barrels room (Chunky) | 5 | `l.punch or l.CanPhase()` | 
| Spilled all over the seasick ship | 15 | `self.logic = lambda _: True` | 
| Corner | Balloon | `self.logic = lambda _: True` | 
| Above the cannons | Balloon | `self.logic = lambda _: True` | 
## Galleon Lighthouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Ladder at the bottom | 5 | `self.logic = lambda _: True` | 
| Around first floor platforms | 10 | `self.logic = lambda _: True` | 
| Around the top of the lighthouse | 5 | `self.logic = lambda _: True` | 
| Around the bottom of the lighthouse | 15 | `self.logic = lambda _: True` | 
| Group 1 up the lighthouse (Donkey) | 10 | `self.logic = lambda _: True` | 
| Group 2 up the lighthouse (Donkey) | 10 | `self.logic = lambda _: True` | 
| Entrance corners | 10 | `self.logic = lambda _: True` | 
| Cobwebs at the bottom | 10 | `self.logic = lambda _: True` | 
| First elevator platform | 5 | `self.logic = lambda _: True` | 
| Final elevator platforms | 10 | `self.logic = lambda _: True` | 
| Around top | Balloon | `self.logic = lambda _: True` | 
| Left side (Donkey) | Balloon | `self.logic = lambda _: True` | 
## Galleon Mechafish
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On planks | 10 | `self.logic = lambda _: True` | 
| Mechanical heart | Balloon | `self.logic = lambda _: True` | 
## Galleon Mermaid Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In the alcove | 5 | `self.logic = lambda _: True` | 
| Above the mermaid | 5 | `self.logic = lambda _: True` | 
| Mermaid's armrests | 10 | `self.logic = lambda _: True` | 
## Galleon5DShip Diddy Lanky Chunky
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance tunnel (1 custom, 4 Diddy) | 5 | `self.logic = lambda _: True` | 
| On a barrel and a box | 10 | `self.logic = lambda _: True` | 
| On barrel | 5 | `self.logic = lambda _: True` | 
| On stack of boxes | 5 | `self.logic = lambda _: True` | 
| On chests | 10 | `self.logic = lambda _: True` | 
| On Captain K. Rools Log Book | 5 | `self.logic = lambda _: True` | 
| On a barrel | 5 | `self.logic = lambda _: True` | 
| On a box in the corner | 5 | `self.logic = lambda _: True` | 
| Corners of Diddy's 5DS (Diddy) | 10 | `self.logic = lambda _: True` | 
| Close right corner of Lanky's 5DS (Lanky) | 5 | `self.logic = lambda _: True` | 
| Far left corner of Lanky's 5DS (Lanky) | 5 | `self.logic = lambda _: True` | 
| Far right corner of Lanky's 5DS (Lanky) | 5 | `self.logic = lambda _: True` | 
| Windows to Lanky's room | 10 | `self.logic = lambda _: True` | 
| Cannons | 10 | `self.logic = lambda _: True` | 
| Windows to Diddy's room | 10 | `self.logic = lambda _: True` | 
| Red carpet | 15 | `self.logic = lambda _: True` | 
| Pile o' gold | 10 | `self.logic = lambda _: True` | 
## Galleon5DShip DKTiny
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On stack of boxes on the right | 5 | `self.logic = lambda _: True` | 
| On box in right bedroom | 5 | `self.logic = lambda _: True` | 
| On algae on the left | 5 | `self.logic = lambda _: True` | 
| On boxes in bonus barrel room | 10 | `self.logic = lambda _: True` | 
| Singles in Tiny's 5DS (2 custom, 8 Tiny) | 10 | `self.logic = lambda _: True` | 
| On pillow in back bedroom | 5 | `self.logic = lambda _: True` | 
| Right side of Tiny's 5DS (Tiny) | 5 | `self.logic = lambda _: True` | 
| Singles in DK's 5DS (Donkey) | 10 | `self.logic = lambda _: True` | 
| Left side of Tiny's 5DS (Tiny) | 5 | `self.logic = lambda _: True` | 
| Skeleton in the main room | 5 | `self.logic = lambda _: True` | 
| Skeleton near the GB | 5 | `self.logic = lambda _: True` | 
| Locked fairy door | 10 | `self.logic = lambda _: True` | 
| Around the GB | 5 | `self.logic = lambda _: True` | 
## Galleon2DShip
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the right on Tiny's side | 10 | `self.logic = lambda _: True` | 
| In the chests | 15 | `self.logic = lambda _: True` | 
| In tunnel to GB | 10 | `self.logic = lambda _: True` | 
| On barrel in Tiny's 2DS (Tiny) | 5 | `self.logic = lambda _: True` | 
| On path to Enguarde box (Lanky) | 5 | `self.logic = lambda _: True` | 
| On chest in Tiny's 2DS (Tiny) | 5 | `self.logic = lambda _: True` | 
| At the end of tunnel to GB (Lanky) | 5 | `self.logic = lambda _: True` | 
| Above the entrance | 5 | `self.logic = lambda _: True` | 
| Wooden beam | 5 | `self.logic = lambda _: True` | 
| Through the hole | 5 | `self.logic = lambda _: True` | 
## Galleon Submarine
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Back of submarine | 5 | `self.logic = lambda _: True` | 
| On each side | 10 | `self.logic = lambda _: True` | 
| On console | 5 | `self.logic = lambda _: True` | 
## Galleon Treasure Chest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Along bottom on each side | 10 | `self.logic = lambda _: True` | 
| The smile of the center clam | 5 | `self.logic = lambda _: True` | 
## Galleon Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Baboon blast bunches (Donkey) | 15 | `self.logic = lambda _: True` | 

# Fungi Forest
## Fungi Forest
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Mushroom near DK portal | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Mushroom by pink tunnel | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Mushroom with vines leading to other mushroom | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Other mushroom whose vines lead to | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Mushroom with vines leading to minecart | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On vines between two shrooms | 10 | `(l.can_use_vines and l.climbing) or (l.jetpack and l.isdiddy)` | 
| Vines to minecart | 5 | `(l.can_use_vines and l.climbing) or (l.jetpack and l.isdiddy)` | 
| Around the roof of minecart | 10 | `((l.can_use_vines or l.CanMoonkick()) and l.climbing) or (l.jetpack and l.isdiddy)` | 
| Mushroom by blue tunnel | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Stumps leading to pendulum | 15 | `self.logic = lambda _: True` | 
| Up the pendulum | 5 | `self.logic = lambda _: True` | 
| Behind clock | 5 | `self.logic = lambda _: True` | 
| Cannon trajectory | 10 | `self.logic = lambda _: True` | 
| Under W2 Tag Barrel | 5 | `self.logic = lambda _: True` | 
| Bouncy shroom by pink tunnel | 5 | `self.logic = lambda _: True` | 
| On pink tunnel lip | 5 | `(l.jetpack and l.isdiddy) or l.ischunky or (l.twirl and l.istiny)` | 
| On blue tunnel lip | 5 | `(l.jetpack and l.isdiddy) or l.ischunky or (l.twirl and l.istiny)` | 
| Against the wall by the apple destination | 10 | `self.logic = lambda _: True` | 
| W3 to pink tunnel | 5 | `self.logic = lambda _: True` | 
| W4 to Minecart | 10 | `self.logic = lambda _: True` | 
| Stump to Minecart | 5 | `self.logic = lambda _: True` | 
| Mill area - Mushroom by blue tunnel | 5 | `l.climbing` | 
| Mushroom by Snide's | 5 | `l.climbing` | 
| Mushroom by Diddy's barn | 5 | `l.climbing` | 
| Mushroom by back tag barrel | 5 | `l.climbing` | 
| Mushroom by Minecart exit | 5 | `l.climbing` | 
| Top of Minecart exit | 10 | `l.istiny and l.twirl and l.climbing` | 
| Top of Mill (8 custom, 7 Lanky) | 1 | `l.climbing` | 
| Top of Mill (8 custom, 7 Lanky) | 10 | `self.logic = lambda _: True` | 
| Top of Mill (8 custom, 7 Lanky) | 4 | `self.logic = lambda _: True` | 
| Outside of conveyor belt (behind night gate) | 5 | `Events.Night in l.Events or l.CanPhase() or l.CanPhaseswim() or l.ledgeclip` | 
| W1 (1 custom, 1 Lanky bunch) | 5 | `self.logic = lambda _: True` | 
| W1 (1 custom, 1 Lanky bunch) | 5 | `self.logic = lambda _: True` | 
| Behind Diddy's Barn | 5 | `self.logic = lambda _: True` | 
| Leading to Diddy barn (2 custom, 3 Diddy) | 5 | `self.logic = lambda _: True` | 
| Against wall behind back tag barrel | 5 | `self.logic = lambda _: True` | 
| Around the outside of DK's barn | 20 | `self.logic = lambda _: True` | 
| Around the inside of DK's barn | 15 | `self.logic = lambda _: True` | 
| On thorns hedge | 15 | `l.strongKong` | 
| Behind leaf wall by DK BP | 10 | `self.logic = lambda _: True` | 
| Apple GB T&S behind night gate | 5 | `Events.Night in l.Events or l.CanPhase()` | 
| Around apple (1 custom, 9 Chunky) | 10 | `self.logic = lambda _: True` | 
| Below Mini Monkey barrel | 5 | `self.logic = lambda _: True` | 
| Inside fence around beanstalk | 10 | `self.logic = lambda _: True` | 
| Around the outside of the fence around beanstalk | 15 | `self.logic = lambda _: True` | 
| Below tag barrel on bouncy shroom around giant mushroom | 5 | `self.logic = lambda _: True` | 
| On mushroom near Cranky | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Mushroom near rocketbarrel | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Mushroom near yellow tunnel | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| In patch of grass near yellow tunnel | 10 | `self.logic = lambda _: True` | 
| In moat around giant mushroom | 10 | `l.swim` | 
| By middle exit of giant mushroom | 5 | `self.logic = lambda _: True` | 
| Around Tiny BP | 10 | `self.logic = lambda _: True` | 
| Behind ladder to BBlast | 5 | `self.logic = lambda _: True` | 
| Behind ladder leading to Giant Mushroom middle entrance | 10 | `self.logic = lambda _: True` | 
| Around baboon blast platform | 10 | `self.logic = lambda _: True` | 
| On BBlast pad | 5 | `self.logic = lambda _: True` | 
| On path to giant mushroom middle entrance | 15 | `self.logic = lambda _: True` | 
| Entrance of Colored Slam (bright side of the mushroom) | 5 | `self.logic = lambda _: True` | 
| Each side of back T&S on top of giant mushroom | 10 | `self.logic = lambda _: True` | 
| Just off the edge by Face Puzzle entrance | 5 | `self.logic = lambda _: True` | 
| Entrance of Zinger bounce (dark side of the mushroom) | 5 | `self.logic = lambda _: True` | 
| Behind night ladder on top of giant mushroom | 5 | `self.logic = lambda _: True` | 
| By battle arena on little outcrop | 5 | `self.logic = lambda _: True` | 
| Around battle crown platform | 10 | `self.logic = lambda _: True` | 
| Around Lanky switch on top of giant mushroom | 10 | `(l.handstand and l.islanky) or (l.jetpack and l.isdiddy)` | 
| Path to Rabbit race (2 custom, 3 Lanky) | 5 | `self.logic = lambda _: True` | 
| On Rabbit's home | 5 | `self.logic = lambda _: True` | 
| On Guitar pad in W4 area | 5 | `self.logic = lambda _: True` | 
| Saxophone pad in tree area | 5 | `self.logic = lambda _: True` | 
| On anthill around hole | 5 | `(l.jetpack and l.isdiddy) or (l.mini and l.saxophone and l.istiny)` | 
| Around anthill (2 custom, 8 Tiny) | 10 | `self.logic = lambda _: True` | 
| In owl alcove | 5 | `l.jetpack` | 
| Around rocketbarrel barrel | 5 | `self.logic = lambda _: True` | 
| Tree stumps rocketbarrel side | 10 | `self.logic = lambda _: True` | 
| Tree stumps rabbit side | 10 | `self.logic = lambda _: True` | 
| Stump at the entrance of tree area | 10 | `self.logic = lambda _: True` | 
| On top of yellow tunnel in tree area | 5 | `l.jetpack` | 
| Around patch of grass by melon crate | 10 | `self.logic = lambda _: True` | 
| Line under tree by Lanky BP | 10 | `self.logic = lambda _: True` | 
| In purple tunnel (Donkey) | 5 | `self.logic = lambda _: True` | 
| In blue tunnel (Donkey) | 5 | `self.logic = lambda _: True` | 
| Path to thornvine barn (Donkey) | 5 | `self.logic = lambda _: True` | 
| Path to Baboon Blast pad (Donkey) | 2 | `self.logic = lambda _: True` | 
| Path to Baboon Blast pad (Donkey) | 3 | `self.logic = lambda _: True` | 
| On thornvine barn switch (Donkey) | 5 | `l.strongKong` | 
| W5 (Donkey) | 5 | `self.logic = lambda _: True` | 
| W5 (Donkey) | 5 | `self.logic = lambda _: True` | 
| Around giant mushroom upper exterior (Diddy) | 10 | `self.logic = lambda _: True` | 
| Around tree (Diddy) | 10 | `self.logic = lambda _: True` | 
| Under starting area rocketbarrel (Diddy) | 10 | `self.logic = lambda _: True` | 
| Under giant mushroom rocketbarrel (Diddy) | 10 | `self.logic = lambda _: True` | 
| By entrance of rafters attic (Diddy) | 5 | `l.spring or l.CanMoontail()` | 
| On hollow tree (Diddy) | 5 | `l.jetpack` | 
| W4 (Diddy) | 5 | `self.logic = lambda _: True` | 
| W4 (Diddy) | 5 | `self.logic = lambda _: True` | 
| W3 (1 Lanky, 1 Tiny) | 5 | `self.logic = lambda _: True` | 
| W3 (1 Lanky, 1 Tiny) | 5 | `self.logic = lambda _: True` | 
| Yellow tunnel (Lanky) | 10 | `self.logic = lambda _: True` | 
| Around giant mushroom base (Lanky) | 10 | `self.logic = lambda _: True` | 
| In entrance to Lanky's attic (Lanky) | 5 | `Events.Night in l.Events` | 
| Over baboon balloon pad (Lanky) | 5 | `self.logic = lambda _: True` | 
| On Giant mushroom top switch (Lanky) | 5 | `(l.jetpack and l.isdiddy) or (l.handstand and l.islanky)` | 
| On Rabbit Race instrument pad (Lanky) | 5 | `self.logic = lambda _: True` | 
| Green tunnel (Tiny) | 1 | `self.logic = lambda _: True` | 
| Green tunnel (Tiny) | 4 | `l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False) or l.CanPhase() or l.CanPhaseswim()` | 
| On riverbed around mill (3 custom, 17 Tiny) | 20 | `l.swim` | 
| On mushrooms in beanstalk area (Tiny) | 15 | `l.climbing` | 
| On anthill (Tiny) | 5 | `(l.jetpack and l.isdiddy) or (l.istiny and (l.mini and l.saxophone))` | 
| W2 (Chunky) | 5 | `self.logic = lambda _: True` | 
| W2 (Chunky) | 5 | `self.logic = lambda _: True` | 
| On minecart entrance (Chunky) | 5 | `self.logic = lambda _: True` | 
| Around giant mushroom lower exterior | 10 | `self.logic = lambda _: True` | 
| From W1 to W2 | 5 | `self.logic = lambda _: True` | 
| From W2 to W3 | 5 | `self.logic = lambda _: True` | 
| From W3 to W4 | 5 | `self.logic = lambda _: True` | 
| From W4 to W1 | 5 | `self.logic = lambda _: True` | 
| On the green tunnel lip (center side) | 5 | `(l.jetpack and l.isdiddy) or l.ischunky or (l.twirl and l.istiny)` | 
| Under the pendulum | 5 | `self.logic = lambda _: True` | 
| The one branch of the clock tree | 5 | `l.jetpack` | 
| Day and night switches | 10 | `self.logic = lambda _: True` | 
| Grass between pink tunnel and minecart | 5 | `self.logic = lambda _: True` | 
| Grass near portal | 5 | `self.logic = lambda _: True` | 
| Grass near blue tunnel | 5 | `self.logic = lambda _: True` | 
| Grass near the apple destination | 5 | `self.logic = lambda _: True` | 
| On the apple | 5 | `self.logic = lambda _: True` | 
| Left and right of Funky | 10 | `self.logic = lambda _: True` | 
| Along the thorns | 10 | `self.logic = lambda _: True` | 
| Outer ledge between minecart exit and thorns | 10 | `self.logic = lambda _: True` | 
| Minecart exit well border | 5 | `self.logic = lambda _: True` | 
| Above the meme hidden dirt patch | 5 | `self.logic = lambda _: True` | 
| Outer ledge between the meme dirt patch and rafters barn | 5 | `self.logic = lambda _: True` | 
| Tag barrel near rafters barn | 10 | `self.logic = lambda _: True` | 
| On the blue tunnel lip (mills side) | 5 | `l.twirl and l.climbing` | 
| Cobblestone path to Snide | 5 | `self.logic = lambda _: True` | 
| Around the winch cage | 5 | `self.logic = lambda _: True` | 
| Near the breakable door of the mill | 10 | `self.logic = lambda _: True` | 
| Above the Diddy winch switch | 5 | `self.logic = lambda _: True` | 
| Thornvine area right side wall | 5 | `self.logic = lambda _: True` | 
| Thornvine area left side wall | 5 | `self.logic = lambda _: True` | 
| Jump over the river from mill to rafters | 5 | `self.logic = lambda _: True` | 
| Jump over the river from mill to thorns | 5 | `self.logic = lambda _: True` | 
| Glitchy dry water spot near warp 5 | 5 | `self.logic = lambda _: True` | 
| On the pink tunnel lip (mushroom side) | 5 | `l.jetpack` | 
| Grass near warp 5 | 10 | `self.logic = lambda _: True` | 
| On the yellow tunnel lip (mushroom side) | 5 | `(l.jetpack and l.isdiddy) or l.climbing` | 
| Grass near mushroom rocketbarrel | 10 | `self.logic = lambda _: True` | 
| Grass near Cranky | 10 | `self.logic = lambda _: True` | 
| Grass near the bouncy mushroom tag barrel | 10 | `self.logic = lambda _: True` | 
| Near the ladder before the blast course | 5 | `self.logic = lambda _: True` | 
| Near the ladder after the blast course | 5 | `self.logic = lambda _: True` | 
| Near the mushroom night door | 5 | `self.logic = lambda _: True` | 
| Top of mushroom to zinger bounce room | 5 | `l.handstand` | 
| Top of mushroom to colored slam room | 5 | `l.handstand` | 
| Mushroom rocketbarrel liftoff !! | 15 | `l.jetpack` | 
| Around the top of mushroom bonus barrel | 10 | `l.jetpack` | 
| Around the first stump in owl tree area | 10 | `self.logic = lambda _: True` | 
| RABBIT | 10 | `self.logic = lambda _: True` | 
| Grass near the rabbit's house | 10 | `self.logic = lambda _: True` | 
| Grass near the owl tree rocketbarrel | 10 | `self.logic = lambda _: True` | 
| Above apple GB | Balloon | `self.logic = lambda _: True` | 
| By blue wall near Minecart | Balloon | `self.logic = lambda _: True` | 
| Around roof of minecart | Balloon | `self.logic = lambda _: True` | 
| High against wall between pink tunnel and minecart | Balloon | `self.logic = lambda _: True` | 
| Behind clock | Balloon | `self.logic = lambda _: True` | 
| Near blue tunnel mill side | Balloon | `self.logic = lambda _: True` | 
| Next to conveyor GB box | Balloon | `self.logic = lambda _: True` | 
| Side of Mill where back entrance is | Balloon | `self.logic = lambda _: True` | 
| Above back tag barrel (Mill area) | Balloon | `self.logic = lambda _: True` | 
| Barn area right side | Balloon | `self.logic = lambda _: True` | 
| Barn area left side | Balloon | `self.logic = lambda _: True` | 
| Around beanstalk | Balloon | `self.logic = lambda _: True` | 
| At first giant mushroom level by rocketbarrel barrel | Balloon | `self.logic = lambda _: True` | 
| By second level entrance | Balloon | `self.logic = lambda _: True` | 
| By high W5 | Balloon | `self.logic = lambda _: True` | 
| By T&S on top of giant mushroom | Balloon | `self.logic = lambda _: True` | 
| By battle crown | Balloon | `self.logic = lambda _: True` | 
| By yellow tunnel tree side | Balloon | `self.logic = lambda _: True` | 
| Rabbit race | Balloon | `self.logic = lambda _: True` | 
| By T&S portal (tree area) | Balloon | `self.logic = lambda _: True` | 
| Above tree | Balloon | `l.jetpack` | 
| In front of Snide (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Above Tiny's blueprint (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Behind Diddy's barn (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Above Chunky's blueprint (Chunky) | Balloon | `self.logic = lambda _: True` | 
| By DK's blueprint (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Blue tunnel | Balloon | `self.logic = lambda _: True` | 
| Pink tunnel | Balloon | `self.logic = lambda _: True` | 
| Around the clock tree trunk | Balloon | `self.logic = lambda _: True` | 
| Cuckoo! Tweet tweet !! | Balloon | `self.logic = lambda _: True` | 
| Green tunnel | Balloon | `l.hasMoveSwitchsanity(Switches.FungiGreenFeather, False) or l.CanPhase() or l.CanPhaseswim()` | 
| Above the apple | Balloon | `self.logic = lambda _: True` | 
| Minecart well | Balloon | `self.logic = lambda _: True` | 
| Waterwheel | Balloon | `self.logic = lambda _: True` | 
| Minecart exit | Balloon | `self.logic = lambda _: True` | 
| Front mill front door to attic | Balloon | `self.logic = lambda _: True` | 
| In front of thornvine barn | Balloon | `self.logic = lambda _: True` | 
| Hopping the thorns behind thornvine barn | Balloon | `self.logic = lambda _: True` | 
| In front of the giant mushroom | Balloon | `self.logic = lambda _: True` | 
| Around mushroom near rocketbarrel (mushroom side) | Balloon | `self.logic = lambda _: True` | 
| Under the lower kasplat mushroom platform | Balloon | `self.logic = lambda _: True` | 
| Yellow tunnel | Balloon | `self.logic = lambda _: True` | 
| Around the anthill | Balloon | `self.logic = lambda _: True` | 
## Forest Anthill
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On outside islands | 10 | `self.logic = lambda _: True` | 
| Central platform | 20 | `self.logic = lambda _: True` | 
| Around the cannon | Balloon | `self.logic = lambda _: True` | 
## Forest Winch Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On boxes in winch room | 15 | `self.logic = lambda _: True` | 
| Winch rope | 5 | `self.logic = lambda _: True` | 
| On the broken switch | 5 | `self.logic = lambda _: True` | 
| In winch room (Diddy) | Balloon | `self.logic = lambda _: True` | 
## Forest Rafters
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On plank near entrance | 5 | `l.guitar` | 
| On long plank near GB | 10 | `l.guitar` | 
| Rafters Right side (Diddy) | 5 | `l.guitar` | 
| Rafters Left side (Diddy) | 5 | `l.guitar` | 
| Above the entrance | 5 | `self.logic = lambda _: True` | 
## Forest Thornvine Barn
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On barrel and box near entrance | 10 | `self.logic = lambda _: True` | 
| On boxes by switch and ladder | 10 | `self.logic = lambda _: True` | 
| On two barrels by switch | 10 | `self.logic = lambda _: True` | 
| Near melon crate in thornvine area | 5 | `self.logic = lambda _: True` | 
| On boxes on upper level | 10 | `self.logic = lambda _: True` | 
| On ladder | 5 | `self.logic = lambda _: True` | 
| On switch (Donkey) | 5 | `l.Slam and l.isdonkey` | 
| Near the trough | 10 | `self.logic = lambda _: True` | 
| In the fairy box | 5 | `l.Slam` | 
| Between vines to bonus barrel | 5 | `l.CanSlamSwitch(Levels.FungiForest, 1) and l.climbing and l.can_use_vines` | 
| Ladder side | Balloon | `self.logic = lambda _: True` | 
## Forest Mill Front
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On flour bag by Mini Monkey | 5 | `self.logic = lambda _: True` | 
| On conveyor belt | 5 | `self.logic = lambda _: True` | 
| On DK switch (Donkey) | 5 | `l.Slam` | 
| In the nooks in the rafters | 10 | `self.logic = lambda _: True` | 
| Keg Bouldertech above the entrance | 5 | `l.chunky and l.barrels` | 
| On the pile of boxes | 5 | `self.logic = lambda _: True` | 
| On the wooden wall | 5 | `l.chunky and l.barrels` | 
| Between the levers | 10 | `l.CanSlamSwitch(Levels.FungiForest, 2) or l.generalclips or l.CanPhase()` | 
| Near the boxes | 5 | `self.logic = lambda _: True` | 
| Middle of the room | Balloon | `self.logic = lambda _: True` | 
| In DK's lever room (Donkey) | Balloon | `(l.CanSlamSwitch(Levels.FungiForest, 2) or l.generalclips or l.CanPhase())` | 
| Wooden wall | Balloon | `self.logic = lambda _: True` | 
## Forest Giant Mushroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| By entrance near gun switches | 10 | `self.logic = lambda _: True` | 
| Up first ladder up each path | 10 | `self.logic = lambda _: True` | 
| On first island to Speedy Swing Sortie | 5 | `self.logic = lambda _: True` | 
| On vines leading to night gate | 5 | `l.can_use_vines` | 
| On floor with oranges | 10 | `self.logic = lambda _: True` | 
| Over gaps near top | 15 | `self.logic = lambda _: True` | 
| Between cannons (Donkey) | 15 | `Events.MushroomCannonsSpawned in l.Events` | 
| Around Diddy's blueprint (3 custom, 7 Diddy) | 10 | `self.logic = lambda _: True` | 
| On Tiny switch (Tiny) | 5 | `self.logic = lambda _: True` | 
| First ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Second ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Third ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Fourth ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Fifth ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Sixth ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Last ladder up mushroom (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Lowest bunch up mushroom (Chunky) | 5 | `self.logic = lambda _: True` | 
| Top of mushroom (Chunky) | 5 | `self.logic = lambda _: True` | 
| Bunch in middle of climb up mushroom (Chunky) | 5 | `self.logic = lambda _: True` | 
| Top of lower portion of mushroom (Chunky) | 5 | `self.logic = lambda _: True` | 
| By night gate (Chunky) | 5 | `self.logic = lambda _: True` | 
| Around the headphones pillar | 5 | `self.logic = lambda _: True` | 
| Pineapple switch of legends | 5 | `self.logic = lambda _: True` | 
| Coconut switch of legends | 5 | `self.logic = lambda _: True` | 
| Torch near Tiny's bonus barrel | 5 | `self.logic = lambda _: True` | 
| Near the u-turn ladder | 5 | `self.logic = lambda _: True` | 
| Near the vines to night door | 10 | `self.logic = lambda _: True` | 
| Near the one vine jump | 10 | `self.logic = lambda _: True` | 
| Top of mushroom dead end | 5 | `self.logic = lambda _: True` | 
| Twirl from the tippy top | 5 | `l.twirl` | 
| Diddy BP floor | Balloon | `self.logic = lambda _: True` | 
| Oranges level | Balloon | `self.logic = lambda _: True` | 
| Top of giant mushroom interior (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Bottom of giant mushroom (Lanky) | Balloon | `self.logic = lambda _: True` | 
| Around the vines to night door | Balloon | `self.logic = lambda _: True` | 
| Behind the highest ladder | Balloon | `self.logic = lambda _: True` | 
## Forest Mill Attic
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On boxes in Lanky attic | 10 | `self.logic = lambda _: True` | 
| Line behind boxes | 5 | `self.logic = lambda _: True` | 
| On box (Lanky) | 5 | `self.logic = lambda _: True` | 
| Flour bags | 10 | `self.logic = lambda _: True` | 
| Enemy hole | Balloon | `self.logic = lambda _: True` | 
## Forest Lanky Mushrooms Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On green mushroom | 5 | `self.logic = lambda _: True` | 
| On mushroom (Lanky) | 5 | `self.logic = lambda _: True` | 
| Kong faces | 5 | `self.logic = lambda _: True` | 
## Forest Mill Back
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On boxes by Mini Monkey barrels | 10 | `self.logic = lambda _: True` | 
| On boxes by spider room (Tiny) | 5 | `self.logic = lambda _: True` | 
| By Mini Monkey entrance to front mill (Tiny) | 5 | `self.logic = lambda _: True` | 
| Inside punchable box (Tiny) | 5 | `Events.MillBoxBroken in l.Events` | 
| On triangle pad (Chunky) | 5 | `Events.MillBoxBroken in l.Events` | 
| Flour bags | 10 | `self.logic = lambda _: True` | 
| Keg Bouldertech up the high wooden wall | 5 | `l.barrels` | 
| Box area near spider | 5 | `self.logic = lambda _: True` | 
| Middle of room | Balloon | `self.logic = lambda _: True` | 
| Back corner | Balloon | `self.logic = lambda _: True` | 
## Forest Spider
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around center web | 10 | `self.logic = lambda _: True` | 
| On entrance plank (Tiny) | 5 | `self.logic = lambda _: True` | 
## Forest Lanky Zingers Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Over bouncy shrooms (Lanky) | 10 | `self.logic = lambda _: True` | 
| Middle | 10 | `self.logic = lambda _: True` | 
| High up | Balloon | `self.logic = lambda _: True` | 
## Forest Chunky Face Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Chunky switch (Chunky) | 5 | `self.logic = lambda _: True` | 
| Towards the switch | 5 | `self.logic = lambda _: True` | 
| Chunky's face puzzle room (Chunky) | Balloon | `self.logic = lambda _: True` | 
## Forest Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In baboon blast course (Donkey) | 10 | `self.logic = lambda _: True` | 

# Crystal Caves
## Crystal Caves
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around DK portal | 10 | `self.logic = lambda _: True` | 
| Around room by ice wall to Gorilla Gone GB | 5 | `self.logic = lambda _: True` | 
| Gorilla Gone Tunnel (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Around Gorilla Gone room | 10 | `self.logic = lambda _: True` | 
| Left side of first warps up the path | 10 | `self.logic = lambda _: True` | 
| On crystals on each side of W4 Mini Monkey room | 10 | `self.logic = lambda _: True` | 
| On Mini Monkey barrel ledge | 10 | `self.logic = lambda _: True` | 
| Next to Funky's store | 10 | `self.logic = lambda _: True` | 
| On monkeyport pad by W4 | 5 | `self.logic = lambda _: True` | 
| Mini Monkey tunnel to W4 | 5 | `self.logic = lambda _: True` | 
| On crystal platforms to Funky | 5 | `self.logic = lambda _: True` | 
| On crystal platforms to Ice castle | 5 | `self.logic = lambda _: True` | 
| On ice tomato switch | 5 | `self.logic = lambda _: True` | 
| On Beetle Race switch | 5 | `self.logic = lambda _: True` | 
| On Baboon Balloon pads | 5 | `self.logic = lambda _: True` | 
| On Baboon Balloon pads | 5 | `l.isdiddy or l.istiny or (l.islanky and (l.balloon or l.monkey_maneuvers))` | 
| To and around boulder by ice castle | 10 | `self.logic = lambda _: True` | 
| Path from boulder to boulder switch (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| On plank to DK BP | 5 | `self.logic = lambda _: True` | 
| Warps to Cranky slope | 10 | `self.logic = lambda _: True` | 
| In front of Snide's (2 custom, 3 Chunky) | 5 | `self.logic = lambda _: True` | 
| Next to headphones by Snide's | 10 | `self.logic = lambda _: True` | 
| On slippery slope to Cranky | 10 | `self.logic = lambda _: True` | 
| Above Baboon Blast pad | 15 | `(l.jetpack and l.isdiddy) or (l.balloon and l.islanky)` | 
| From BBlast pad to Cranky | 5 | `self.logic = lambda _: True` | 
| On crystal platforms to ice castle (right side) | 10 | `self.logic = lambda _: True` | 
| Vertical lines in alcoves between ice castle and BBlast | 15 | `self.logic = lambda _: True` | 
| Vertical line in alcove between BBlast and Mini Monkey W3 | 10 | `self.logic = lambda _: True` | 
| In front of Mini Monkey W3 tunnel | 5 | `self.logic = lambda _: True` | 
| On path between BBlast and Mini Monkey W3 | 5 | `self.logic = lambda _: True` | 
| On path between ice castle and BBlast | 10 | `self.logic = lambda _: True` | 
| Around Mini Monkey W3 room | 10 | `self.logic = lambda _: True` | 
| In Mini Monkey W3 tunnel | 5 | `self.logic = lambda _: True` | 
| In water around 5DI | 10 | `self.logic = lambda _: True` | 
| Around W1 in 5DI area | 5 | `self.logic = lambda _: True` | 
| Around W3 in 5DI area | 5 | `self.logic = lambda _: True` | 
| Around Tag Barrel in 5DI area | 5 | `self.logic = lambda _: True` | 
| Singles on 5DI | 10 | `self.logic = lambda _: True` | 
| Bunch on 5DI | 5 | `self.logic = lambda _: True` | 
| On pointy pillar by Chunky igloo | 5 | `l.jetpack` | 
| In water around Chunky Igloo | 5 | `self.logic = lambda _: True` | 
| In water around Tiny Igloo | 5 | `self.logic = lambda _: True` | 
| On edge of useless platform on the right side of waterfall | 5 | `self.logic = lambda _: True` | 
| On other edge of useless platform on the right side of waterfall | 5 | `self.logic = lambda _: True` | 
| On baboon balloon pad by 1DC | 5 | `self.logic = lambda _: True` | 
| On Lanky 1DC | 5 | `self.logic = lambda _: True` | 
| Next to Lanky 1DC | 5 | `self.logic = lambda _: True` | 
| Plank to Lanky 1DC | 5 | `self.logic = lambda _: True` | 
| From Waterfall tag to W2 | 5 | `self.logic = lambda _: True` | 
| W2 to Tiny BP | 5 | `self.logic = lambda _: True` | 
| Each side of DK 1DC | 10 | `self.logic = lambda _: True` | 
| In front of the T&S on DK 1DC | 5 | `self.logic = lambda _: True` | 
| On crystal platform near waterfall RB | 5 | `self.logic = lambda _: True` | 
| Lower crystal platform to waterfall tag | 5 | `self.logic = lambda _: True` | 
| Around Tiny BP | 10 | `self.logic = lambda _: True` | 
| In the water between pickups below W4 Mini Monkey tunnel | 10 | `self.logic = lambda _: True` | 
| In river W1W2 to Waterfall | 15 | `self.logic = lambda _: True` | 
| In river in corner near Ice castle | 5 | `self.logic = lambda _: True` | 
| Path to big boulder (2 custom, 3 Donkey) | 5 | `self.logic = lambda _: True` | 
| Around giant boulder | 10 | `self.logic = lambda _: True` | 
| Behind pillar in giant boulder room | 5 | `self.logic = lambda _: True` | 
| Around pillar below DK 1DC | 10 | `self.logic = lambda _: True` | 
| Near ledge by waterfall | 5 | `self.logic = lambda _: True` | 
| Crystal platform at the end of fence in front of 5DC | 5 | `self.logic = lambda _: True` | 
| Lone small crystal platform close to 5DC | 5 | `self.logic = lambda _: True` | 
| Along fence in front of 5DC | 5 | `self.logic = lambda _: True` | 
| 5DC Triangle pad | 5 | `self.logic = lambda _: True` | 
| 5DC Saxophone pad | 5 | `self.logic = lambda _: True` | 
| 5DC Lower Guitar pad | 5 | `self.logic = lambda _: True` | 
| 5DC Upper Guitar pad | 5 | `self.logic = lambda _: True` | 
| W5 | 5 | `self.logic = lambda _: True` | 
| W5 | 5 | `self.logic = lambda _: True` | 
| Corner by W5 | 5 | `self.logic = lambda _: True` | 
| Line on middle floor of 5DC | 5 | `self.logic = lambda _: True` | 
| Line on upper floor of 5DC | 5 | `self.logic = lambda _: True` | 
| Bunch in front of window up high on 5DC | 5 | `l.jetpack` | 
| Blue lonely crystal platform by 5DC | 5 | `self.logic = lambda _: True` | 
| Crystal platform by 5DC | 5 | `self.logic = lambda _: True` | 
| 2 ends of the Giant Kosha area | 10 | `self.logic = lambda _: True` | 
| 2 other ends of the Giant Kosha area | 10 | `self.logic = lambda _: True` | 
| In Boulder igloo (4 custom, 6 Chunky) | 10 | `(l.chunky and l.barrels) or l.CanPhase()` | 
| In star above 5DI (Diddy) | 5 | `l.jetpack` | 
| In waterfall under bonus barrel (Diddy) | 5 | `l.jetpack` | 
| W2 (Chunky) | 10 | `self.logic = lambda _: True` | 
| Around 5DI (Donkey) | 5 | `self.logic = lambda _: True` | 
| Around baboon blast pad (Donkey) | 5 | `self.logic = lambda _: True` | 
| W1 (Donkey) | 10 | `self.logic = lambda _: True` | 
| On 5DC bongos pad (Donkey) | 5 | `self.logic = lambda _: True` | 
| On pillar by 5DI tag (Diddy) | 5 | `l.jetpack and l.isdiddy` | 
| Above baboon blast pad by Cranky (Lanky) | 15 | `(l.jetpack and l.isdiddy) or (l.balloon and l.islanky)` | 
| Inside tower to beetle race (Lanky) | 5 | `(l.balloon or l.monkey_maneuvers) and l.CanSlamSwitch(Levels.CrystalCaves, 2)` | 
| On trombone pad on Lanky cabin (Lanky) | 5 | `self.logic = lambda _: True` | 
| First path to warps (Lanky) | 5 | `self.logic = lambda _: True` | 
| Path from Funky to rocketbarrel (Diddy) | 5 | `self.logic = lambda _: True` | 
| W4 (Diddy) | 5 | `self.logic = lambda _: True` | 
| W4 (Diddy) | 5 | `self.logic = lambda _: True` | 
| Above Tiny and Chunky igloos (Diddy) | 10 | `l.jetpack` | 
| Around Diddy blueprint (Diddy) | 5 | `self.logic = lambda _: True` | 
| Chunky igloo (Chunky) | 5 | `Events.CavesLargeBoulderButton in l.Events or l.generalclips or l.CanPhaseswim()` | 
| On Gorilla Gone pad (Chunky) | 5 | `self.logic = lambda _: True` | 
| On small boulder switch (Chunky) | 5 | `self.logic = lambda _: True` | 
| Inside giant boulder (Chunky) | 5 | `Events.CavesSmallBoulderButton in l.Events and l.hunkyChunky and l.barrels` | 
| W3 (Tiny) | 5 | `self.logic = lambda _: True` | 
| W3 (Tiny) | 5 | `self.logic = lambda _: True` | 
| On riverbed to waterfall (Lanky) | 10 | `self.logic = lambda _: True` | 
| On W5 pillar (Lanky) | 20 | `self.logic = lambda _: True` | 
| On riverbed to igloo area (Tiny) | 10 | `self.logic = lambda _: True` | 
| In Monkeyport igloo (Tiny) | 5 | `Events.CavesMonkeyportAccess in l.Events or l.CanPhaseswim()` | 
| Inside small boulder (Chunky) | 5 | `l.barrels and l.chunky` | 
| Middle of Giant Kosha room (Tiny) | 20 | `self.logic = lambda _: True` | 
| Around small pillar near gorilla gone cave | 5 | `self.logic = lambda _: True` | 
| Missing fence near warps 1 and 2 | 5 | `self.logic = lambda _: True` | 
| Crystals near warp 1 | 5 | `self.logic = lambda _: True` | 
| Crystal near Snide cave | 5 | `self.logic = lambda _: True` | 
| Missing fence near Snide | 5 | `self.logic = lambda _: True` | 
| Next to Cranky | 5 | `self.logic = lambda _: True` | 
| Balloon to the mini monkey cave | 10 | `l.balloon` | 
| Balloon to the protruding wall | 10 | `l.balloon` | 
| Crystal near mini monkey cave | 5 | `self.logic = lambda _: True` | 
| Crystal near the giant boulder cave | 5 | `self.logic = lambda _: True` | 
| Near the steps to baboon blast | 5 | `self.logic = lambda _: True` | 
| Around the ice castle | 10 | `self.logic = lambda _: True` | 
| Big stalactite between ice castle and Funky | 5 | `(l.jetpack and l.isdiddy) or (l.balloon and l.islanky)` | 
| Near the small boulder switch | 5 | `self.logic = lambda _: True` | 
| Leftmost crystal platform below ice castle | 5 | `self.logic = lambda _: True` | 
| Leftmost crystal platform below Funky | 5 | `self.logic = lambda _: True` | 
| Corner ledge between Funky and ice castle | 5 | `self.logic = lambda _: True` | 
| Next to Funky | 5 | `self.logic = lambda _: True` | 
| Under the rocketbarrel by Funky | 10 | `self.logic = lambda _: True` | 
| Big window on the 5-door cabin | 5 | `self.logic = lambda _: True` | 
| Next to Candy | 5 | `self.logic = lambda _: True` | 
| Nice ledge grab spot near cabins warp 2 | 5 | `self.logic = lambda _: True` | 
| Around the platform near cabins rocketbarrel | 5 | `self.logic = lambda _: True` | 
| Plank to rotating cabin | 5 | `self.logic = lambda _: True` | 
| Up the cabins waterfall | 5 | `l.jetpack` | 
| On the headphones | 5 | `self.logic = lambda _: True` | 
| Crystals on the useless platform in cabins area | 5 | `self.logic = lambda _: True` | 
| Ice ground near 5-door cabin | 5 | `self.logic = lambda _: True` | 
| Around full pillar near igloo area entrance | 5 | `self.logic = lambda _: True` | 
| Around full pillar near igloo warps | 5 | `self.logic = lambda _: True` | 
| Around half-pillar near igloo | 5 | `self.logic = lambda _: True` | 
| Spire near the ice castle | 5 | `l.twirl` | 
| Twirl from the cabins pillar | 5 | `l.twirl` | 
| Balloon to the cabins waterfall | 5 | `l.balloon` | 
| Near pillar by DK portal | Balloon | `self.logic = lambda _: True` | 
| First room between DK portal and main level | Balloon | `self.logic = lambda _: True` | 
| Under bridge to W4 Mini Monkey | Balloon | `self.logic = lambda _: True` | 
| Around pillar of Lanky BP | Balloon | `self.logic = lambda _: True` | 
| Around Lanky BP (high) | Balloon | `self.logic = lambda _: True` | 
| Above W1 and W2 (Ice castle height) | Balloon | `self.logic = lambda _: True` | 
| Above small boulder | Balloon | `self.logic = lambda _: True` | 
| Around pillar near Cranky | Balloon | `self.logic = lambda _: True` | 
| Above river under bridge to small boulder | Balloon | `self.logic = lambda _: True` | 
| Beneath BBlast | Balloon | `self.logic = lambda _: True` | 
| Above area to Mini Monkey W3 room | Balloon | `self.logic = lambda _: True` | 
| Behind right pillar near 5DI | Balloon | `self.logic = lambda _: True` | 
| Above Monkeyport igloo | Balloon | `self.logic = lambda _: True` | 
| Between Tag barrel and W1 | Balloon | `self.logic = lambda _: True` | 
| Above Chunky igloo | Balloon | `self.logic = lambda _: True` | 
| In waterfall (Under bonus barrel) | Balloon | `self.logic = lambda _: True` | 
| In front of 5DC lower floor | Balloon | `self.logic = lambda _: True` | 
| Above 5DC middle floor | Balloon | `self.logic = lambda _: True` | 
| Above river close to waterfall 5DC side | Balloon | `self.logic = lambda _: True` | 
| Around Tiny BP pillar (low) | Balloon | `self.logic = lambda _: True` | 
| Above useless platform below Lanky 1DC | Balloon | `self.logic = lambda _: True` | 
| Above river at Lanky 1DC roof height | Balloon | `self.logic = lambda _: True` | 
| Above rocketbarrel area (between Rotating room and waterfall tag) | Balloon | `self.logic = lambda _: True` | 
| Above rotating room | Balloon | `self.logic = lambda _: True` | 
| In front of Candy | Balloon | `self.logic = lambda _: True` | 
| Around W4 pillar (Diddy) | Balloon | `self.logic = lambda _: True` | 
| In front of Snide (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Around Tiny blueprint (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Waterfall (Lanky) | Balloon | `self.logic = lambda _: True` | 
| In gorilla gone room (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Above 5DC (Diddy) | Balloon | `self.logic = lambda _: True` | 
| In bonus barrel cave (Chunky) | Balloon | `self.logic = lambda _: True` | 
| In Diddy BP room (Tiny) | Balloon | `self.logic = lambda _: True` | 
| In giant boulder room (Donkey) | Balloon | `self.logic = lambda _: True` | 
| Around the big ice castle pillar | Balloon | `self.logic = lambda _: True` | 
| Slope to Cranky | Balloon | `self.logic = lambda _: True` | 
| Bridge near Cranky | Balloon | `self.logic = lambda _: True` | 
| Igloo area entrance | Balloon | `self.logic = lambda _: True` | 
| Little spire near Chunky transparent igloo | Balloon | `self.logic = lambda _: True` | 
| Tall pillar near ice castle | Balloon | `self.logic = lambda _: True` | 
| Crystal platforms near Funky | Balloon | `self.logic = lambda _: True` | 
| Near Lanky cabin | Balloon | `self.logic = lambda _: True` | 
| Tall pillar near 5-door cabin | Balloon | `self.logic = lambda _: True` | 
## Caves Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Middle path first barrel | 5 | `self.logic = lambda _: True` | 
| Line that misses a barrel in slow path | 5 | `self.logic = lambda _: True` | 
| Line of singles through ring | 5 | `self.logic = lambda _: True` | 
| Long path (Donkey) | 15 | `self.logic = lambda _: True` | 
| Middle path (Donkey) | 5 | `self.logic = lambda _: True` | 
## Caves Frozen Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Each side walls | 10 | `self.logic = lambda _: True` | 
| Each side of the tomato's chair | 10 | `self.logic = lambda _: True` | 
| L on the board | 5 | `self.logic = lambda _: True` | 
| In frozen castle (Lanky) | Balloon | `self.logic = lambda _: True` | 
## Caves Chunky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the igloo | 10 | `self.logic = lambda _: True` | 
| Hey look, a rabbit !! | 10 | `self.logic = lambda _: True` | 
| In Chunky 5DI (Chunky) | Balloon | `self.logic = lambda _: True` | 
## Caves Diddy Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Numbers 1 5 6 | 15 | `self.logic = lambda _: True` | 
| Numbers 2 3 4 | 15 | `self.logic = lambda _: True` | 
| In Diddy 5DI (Diddy) | Balloon | `self.logic = lambda _: True` | 
## Caves Donkey Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Center of igloo group with 7 singles | 10 | `l.strongKong and l.isdonkey` | 
| Around maze | 10 | `self.logic = lambda _: True` | 
| On doorframe (Donkey) | 5 | `self.logic = lambda _: True` | 
| In DK 5DI (Donkey) | Balloon | `self.logic = lambda _: True` | 
## Caves Lanky Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On crystal tower | 10 | `self.logic = lambda _: True` | 
| Up the crystal tower (Lanky) | 5 | `l.balloon or l.monkey_maneuvers` | 
| Upper balloon pad | 5 | `l.balloon or l.monkey_maneuvers` | 
| Around crystal tower (lower) | Balloon | `self.logic = lambda _: True` | 
| In Lanky 5DI (Lanky) | Balloon | `self.logic = lambda _: True` | 
## Caves Tiny Igloo
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside Tiny's igloo room | 10 | `self.logic = lambda _: True` | 
| In middle (Tiny) | 5 | `self.logic = lambda _: True` | 
| In Tiny 5DI (Tiny) | Balloon | `self.logic = lambda _: True` | 
## Caves Lanky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Stack of books in entrance corner | 5 | `self.logic = lambda _: True` | 
| Stacks of books on shelves in Lanky's cabin | 10 | `self.logic = lambda _: True` | 
| Bunch on switch | 5 | `self.logic = lambda _: True` | 
| Around the balloon pad | 10 | `self.logic = lambda _: True` | 
| Across room in L pattern | Balloon | `self.logic = lambda _: True` | 
| GB hole | Balloon | `self.logic = lambda _: True` | 
## Caves Chunky Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Stacks of books on shelves in Chunky's cabin | 10 | `self.logic = lambda _: True` | 
| Books on floor and back shelf in Chunky's cabin | 10 | `self.logic = lambda _: True` | 
| In the middle of the room (Chunky) | 20 | `l.gorillaGone and l.Slam` | 
| Light path corners | 10 | `self.logic = lambda _: True` | 
| Middle of the room | Balloon | `self.logic = lambda _: True` | 
## Caves Diddy Upper Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Books on shelf near entrance in Diddy's upper cabin | 5 | `self.logic = lambda _: True` | 
| Books on shelf on back wall in Diddy's upper cabin | 5 | `self.logic = lambda _: True` | 
| On candles (Diddy) | 15 | `l.jetpack and (l.guitar or l.oranges) and l.isdiddy and (l.spring or l.CanMoontail())` | 
| On the GB cage | 5 | `self.logic = lambda _: True` | 
| Behind the back candle | 5 | `self.logic = lambda _: True` | 
| Cobwebs | 5 | `self.logic = lambda _: True` | 
| Above entrance high up in the room | Balloon | `(l.guitar or l.oranges) and (l.spring or (l.CanMoontail() and not l.cabinBarrelMoved())) and l.jetpack` | 
| Middle of the room | Balloon | `self.logic = lambda _: True` | 
## Caves Donkey Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On books on shelves in DK's cabin | 10 | `self.logic = lambda _: True` | 
| On a trapdoor (Donkey) | 5 | `self.logic = lambda _: True` | 
| Around the center trapdoor | 10 | `self.logic = lambda _: True` | 
| Backflip above the center trapdoor | 5 | `self.logic = lambda _: True` | 
| Around room | Balloon | `self.logic = lambda _: True` | 
| Front holes | Balloon | `self.logic = lambda _: True` | 
## Caves Rotating Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On puzzle (Donkey) | 5 | `self.logic = lambda _: True` | 
| Back wall | 5 | `self.logic = lambda _: True` | 
| Puzzles | Balloon | `self.logic = lambda _: True` | 
## Caves Diddy Lower Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around room (Diddy) | 5 | `self.logic = lambda _: True` | 
| On center pillar (Diddy) | 5 | `l.jetpack or l.monkey_maneuvers` | 
| Wall torches | 10 | `self.logic = lambda _: True` | 
| Rocket up around the room | 10 | `l.jetpack` | 
| Around room above platforms | Balloon | `self.logic = lambda _: True` | 
## Caves Tiny Cabin
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Bunches in cabin (Tiny) | 10 | `self.logic = lambda _: True` | 
| Lone side platform | 5 | `self.logic = lambda _: True` | 
| Lone corner platform | 5 | `self.logic = lambda _: True` | 
| Corner above the void | 5 | `self.logic = lambda _: True` | 
| In Tiny 5DC (Tiny) | Balloon | `self.logic = lambda _: True` | 

# Creepy Castle
## Creepy Castle
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around DK portal platform | 5 | `self.logic = lambda _: True` | 
| Center of DK portal platform | 5 | `self.logic = lambda _: True` | 
| Around small pool outside tree | 5 | `self.logic = lambda _: True` | 
| On tree by small pool outside big tree | 2 | `self.logic = lambda _: True` | 
| On tree by small pool outside big tree | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On steps to big tree | 5 | `self.logic = lambda _: True` | 
| On tree by big tree (Tiny coins) | 2 | `self.logic = lambda _: True` | 
| On tree by big tree (Tiny coins) | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On branch sticking out of big tree | 5 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On big tree | 5 | `l.jetpack` | 
| On BBlast pad | 5 | `self.logic = lambda _: True` | 
| On sewer pipe | 5 | `self.logic = lambda _: True` | 
| Around big tree platform | 10 | `self.logic = lambda _: True` | 
| Path from big tree to first moving platforms (5 custom, 5 Donkey) | 10 | `self.logic = lambda _: True` | 
| Path from first moving platforms to staircase (not including) (4 custom, 6 Donkey) | 10 | `self.logic = lambda _: True` | 
| Along side of staircase to W1 | 5 | `self.logic = lambda _: True` | 
| On staircase to W1 (1 custom, 4 Donkey) | 5 | `self.logic = lambda _: True` | 
| On stones on path from moving platforms to W1 | 15 | `self.logic = lambda _: True` | 
| On tree by staircase to W1 | 2 | `self.logic = lambda _: True` | 
| On tree by staircase to W1 | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On tree by low T&S portal (by Lanky coins) | 2 | `self.logic = lambda _: True` | 
| On tree by low T&S portal (by Lanky coins) | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| Path from crypt to low T&S portal | 10 | `self.logic = lambda _: True` | 
| On ladder from W1 stairs to crypt | 2 | `self.logic = lambda _: True` | 
| On ladder from W1 stairs to crypt | 3 | `self.logic = lambda _: True` | 
| Path from Crypt to Tiny BP | 20 | `self.logic = lambda _: True` | 
| On Tiny BP platform | 10 | `self.logic = lambda _: True` | 
| On ladder from past crypt to random platform below/past W1 | 2 | `self.logic = lambda _: True` | 
| On ladder from past crypt to random platform below/past W1 | 3 | `self.logic = lambda _: True` | 
| On pile of bricks on random platform past/below W1 | 5 | `self.logic = lambda _: True` | 
| Below moving platforms past W1 | 5 | `self.logic = lambda _: True` | 
| Around random platform past/below W1 | 10 | `self.logic = lambda _: True` | 
| W1 | 10 | `self.logic = lambda _: True` | 
| W2 | 10 | `self.logic = lambda _: True` | 
| W3 | 10 | `self.logic = lambda _: True` | 
| W4 | 10 | `self.logic = lambda _: True` | 
| W5 | 10 | `self.logic = lambda _: True` | 
| On tree on platform past/below W1 | 2 | `self.logic = lambda _: True` | 
| On tree on platform past/below W1 | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| On ladder next to Tiny BP | 2 | `self.logic = lambda _: True` | 
| On ladder next to Tiny BP | 3 | `self.logic = lambda _: True` | 
| Path from W1 to ladder (7 custom, 8 Donkey) | 15 | `self.logic = lambda _: True` | 
| On ladder towards W2 (4 custom, 1 Donkey) | 5 | `self.logic = lambda _: True` | 
| Stone path from drawbridge to wooden path (4 custom, 6 Donkey) | 10 | `self.logic = lambda _: True` | 
| On wooden path towards W2 (4 custom, 6 Donkey) | 10 | `self.logic = lambda _: True` | 
| On path near Lanky BP (5 custom, 5 Donkey) | 10 | `self.logic = lambda _: True` | 
| Near W2 (1 custom, 4 Donkey) | 5 | `self.logic = lambda _: True` | 
| On brick piles past W1 | 10 | `self.logic = lambda _: True` | 
| On tree past W1 | 2 | `self.logic = lambda _: True` | 
| On tree past W1 | 3 | `l.climbing or (l.jetpack and l.isdiddy)` | 
| In moat by warps | 10 | `l.swim` | 
| In moat by upper cave entrance | 10 | `l.swim` | 
| On steps of upper cave entrance (warps side) | 10 | `self.logic = lambda _: True` | 
| On ladder into moat by W3 | 5 | `self.logic = lambda _: True` | 
| Ladder from tree to warps | 5 | `self.logic = lambda _: True` | 
| Edge of warps platform by tag barrel | 10 | `self.logic = lambda _: True` | 
| Wood border around tag barrel by warps | 10 | `self.logic = lambda _: True` | 
| W2 to wooden bridge (2 custom, 3 Tiny) | 5 | `self.logic = lambda _: True` | 
| Wooden bridge (2 custom, 3 Tiny) | 5 | `self.logic = lambda _: True` | 
| Wooden portion past bridge (3 custom, 2 Tiny) | 5 | `self.logic = lambda _: True` | 
| In front of Cranky (6 custom, 4 Tiny) | 10 | `self.logic = lambda _: True` | 
| First octagonal platform (4 custom, 1 Tiny) | 5 | `self.logic = lambda _: True` | 
| Second octagonal platform (4 custom, 1 Tiny) | 5 | `self.logic = lambda _: True` | 
| On switch to Museum | 5 | `self.logic = lambda _: True` | 
| Wooden path from Museum to W4 (6 custom, 4 Tiny) | 10 | `self.logic = lambda _: True` | 
| On W4 platform (4 custom, 1 Tiny) | 5 | `self.logic = lambda _: True` | 
| Around back of shed + greenhouse | 10 | `self.logic = lambda _: True` | 
| On greenhouse roof | 10 | `self.logic = lambda _: True` | 
| In front of ballroom (6 custom, 4 Tiny) | 10 | `self.logic = lambda _: True` | 
| In front of Library entrance (5 custom, 5 Tiny) | 10 | `self.logic = lambda _: True` | 
| Around tower past library (2 custom, 3 Tiny) | 5 | `self.logic = lambda _: True` | 
| Path to W5 from Library switch (5 custom, 5 Tiny) | 10 | `self.logic = lambda _: True` | 
| Path to W5 (1 custom, 9 Tiny singles, 1 Tiny bunch) | 15 | `self.logic = lambda _: True` | 
| Around tower at top | 10 | `self.logic = lambda _: True` | 
| On Tower Lanky switch | 5 | `self.logic = lambda _: True` | 
| On tower battlements (left of W5) | 10 | `self.logic = lambda _: True` | 
| On tower battlements past Snide | 15 | `self.logic = lambda _: True` | 
| Between W5 and path to Snide | 5 | `self.logic = lambda _: True` | 
| To and around Snide | 10 | `self.logic = lambda _: True` | 
| Battlements around Snide | 15 | `self.logic = lambda _: True` | 
| On battlements at top of tower | 20 | `l.jetpack` | 
| Switch to Ballroom | 5 | `self.logic = lambda _: True` | 
| First bridge (Donkey) | 5 | `self.logic = lambda _: True` | 
| On cloud atop tower (Diddy) | 5 | `l.jetpack` | 
| On pole close to Cranky (Diddy) | 5 | `l.jetpack` | 
| Pool near portal | 10 | `self.logic = lambda _: True` | 
| Near the headphones | 5 | `self.logic = lambda _: True` | 
| On stones near staircase to back W1 | 15 | `self.logic = lambda _: True` | 
| Stone near back W1 | 5 | `self.logic = lambda _: True` | 
| Stone on the graveyard platform | 5 | `self.logic = lambda _: True` | 
| Gravestone in the graveyard | 5 | `self.logic = lambda _: True` | 
| Wooden post near lone kasplat platform | 5 | `self.logic = lambda _: True` | 
| Stone brick above lone kasplat platform | 5 | `self.logic = lambda _: True` | 
| Trees near rocketbarrel battlement | 10 | `self.logic = lambda _: True` | 
| Stairs of the rocketbarrel battlement | 5 | `self.logic = lambda _: True` | 
| Stones near staircase to warps | 10 | `self.logic = lambda _: True` | 
| Jump back to portal platform | 5 | `self.logic = lambda _: True` | 
| Stones near ladder after drawbridge | 10 | `self.logic = lambda _: True` | 
| Edge of the moat | 5 | `self.logic = lambda _: True` | 
| Staircase to warps | 10 | `self.logic = lambda _: True` | 
| Fences near the warps | 15 | `self.logic = lambda _: True` | 
| On the drawbridge wooden beams | 10 | `l.jetpack` | 
| End wall of the moat | 5 | `self.logic = lambda _: True` | 
| Fence near Lanky kasplat | 5 | `self.logic = lambda _: True` | 
| Under the warp 2 rocketbarrel overhang | 5 | `l.jetpack` | 
| Museum sign | 5 | `self.logic = lambda _: True` | 
| Ballroom sign | 5 | `self.logic = lambda _: True` | 
| Pole near upper warp 4 | 5 | `self.logic = lambda _: True` | 
| Against the tower | 10 | `self.logic = lambda _: True` | 
| Blind jump to the library switch | 5 | `self.logic = lambda _: True` | 
| Spiky fence at the top | 10 | `self.logic = lambda _: True` | 
| Warp 2 rocketbarrel liftoff !! | 15 | `l.jetpack` | 
| Under the warp 4 overhang near Lanky kasplat | 10 | `l.jetpack` | 
| Above Cranky | 5 | `l.jetpack, locations=[[5, 1.0, 234, 1311, 1412]]` | 
| On poles in the back above warp 1 | 10 | `l.jetpack` | 
| Twirl from the library | 5 | `l.twirl` | 
| Gravestones near the lower door | 10 | `self.logic = lambda _: True` | 
| Gravestone on the way to lower T&S | 5 | `self.logic = lambda _: True` | 
| Edge next to lower T&S | 5 | `self.logic = lambda _: True` | 
| Below first bridge | Balloon | `self.logic = lambda _: True` | 
| Around big tree | Balloon | `self.logic = lambda _: True` | 
| Above area near low T&S portal | Balloon | `self.logic = lambda _: True` | 
| Above empty area past W1 | Balloon | `self.logic = lambda _: True` | 
| Over and under moat bridge | Balloon | `self.logic = lambda _: True` | 
| Above moat tunnel entrance | Balloon | `self.logic = lambda _: True` | 
| Above headphones by warps tag | Balloon | `self.logic = lambda _: True` | 
| On right side of path to W2 (Diddy balloon on the left) | Balloon | `self.logic = lambda _: True` | 
| By Lanky blueprint | Balloon | `self.logic = lambda _: True` | 
| Above path from W2 to W3 (castle side) | Balloon | `self.logic = lambda _: True` | 
| Around Cranky's shop | Balloon | `self.logic = lambda _: True` | 
| Behind greenhouse | Balloon | `self.logic = lambda _: True` | 
| Near ballroom entrance | Balloon | `self.logic = lambda _: True` | 
| On path near W5 (castle side) | Balloon | `self.logic = lambda _: True` | 
| Around tower | Balloon | `self.logic = lambda _: True` | 
| Above tower | Balloon | `l.jetpack` | 
| Behind Snide's | Balloon | `self.logic = lambda _: True` | 
| Above W1 (Diddy) | Balloon | `self.logic = lambda _: True` | 
| From portal to lone kasplat | Balloon | `self.logic = lambda _: True` | 
| Near ladder to headphones | Balloon | `self.logic = lambda _: True` | 
| Around the lower T&S area | Balloon | `self.logic = lambda _: True` | 
| Rising from the graveyard | Balloon | `self.logic = lambda _: True` | 
| Near the lower door | Balloon | `self.logic = lambda _: True` | 
| Around tree in uneventful area just above the grayevard | Balloon | `self.logic = lambda _: True` | 
| Near museum platforms | Balloon | `self.logic = lambda _: True` | 
## Castle Ballroom
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Ballroom - Entrance path | 10 | `self.logic = lambda _: True` | 
| Carpeted ramps to main room | 10 | `self.logic = lambda _: True` | 
| Back two corners of ballroom floor | 10 | `self.logic = lambda _: True` | 
| On monkeyport pad (Tiny) | 5 | `self.logic = lambda _: True` | 
| On candles (Diddy) | 15 | `l.jetpack` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| Main room entrance | 10 | `self.logic = lambda _: True` | 
| Black spaces | 10 | `self.logic = lambda _: True` | 
| White spaces | 10 | `self.logic = lambda _: True` | 
| Near the monkeyport pad | 5 | `self.logic = lambda _: True` | 
| Chandelier | 15 | `l.jetpack` | 
| In back of the room | Balloon | `self.logic = lambda _: True` | 
| By bonus barrel (Diddy) | Balloon | `self.logic = lambda _: True` | 
| Above the back candle | Balloon | `l.jetpack` | 
## Castle Baboon Blast
| Name | Amount | Logic |
| ---- | ------ | ----- |
| In baboon blast course | 10 | `self.logic = lambda _: True` | 
## Castle Dungeon
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On buckets | 15 | `self.logic = lambda _: True` | 
| On DK switch | 5 | `self.logic = lambda _: True` | 
| On Lanky switch | 5 | `self.logic = lambda _: True` | 
| On Diddy switch | 5 | `self.logic = lambda _: True` | 
| Path between Diddy and Lanky switches | 10 | `self.logic = lambda _: True` | 
| In DK's room behind puzzle | 5 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| In Diddy's room between chains | 10 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| On BB pads | 15 | `(l.balloon and l.trombone and (l.CanSlamSwitch(Levels.CreepyCastle, 3)) or l.CanPhase())` | 
| On face puzzle (Donkey) | 5 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| In cages DK side (Diddy) | 10 | `l.punch or l.CanPhase()` | 
| In cages Lanky side (Diddy) | 10 | `l.punch or l.CanPhase()` | 
| Chained to the walls | 10 | `self.logic = lambda _: True` | 
| Entrance corners | 10 | `self.logic = lambda _: True` | 
| Circle on the DK puzzle | 10 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| Rotating throne | 5 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| Under the chain vines in Diddy's room | 5 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| Balloon backwards to the main dungeon | 5 | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.trombone and l.balloon` | 
| In Lanky's section | Balloon | `self.logic = lambda _: True` | 
| In Diddy's section | Balloon | `self.logic = lambda _: True` | 
| In DK's room | Balloon | `l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()` | 
| In Diddy's dungeon room (Diddy) | Balloon | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase())` | 
| Far in Lanky's dungeon room (Lanky) | Balloon | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase()) and l.trombone and l.balloon` | 
| In cage left side (Chunky) | Balloon | `(l.punch or l.CanPhase() or l.generalclips)` | 
| Close in Lanky's dungeon room (Lanky) | Balloon | `(l.CanSlamSwitch(Levels.CreepyCastle, 3) or l.CanPhase())` | 
| In cage right side (Chunky) | Balloon | `(l.punch or l.CanPhase() or l.generalclips)` | 
| Intersection | Balloon | `self.logic = lambda _: True` | 
## Castle Shed
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Shed - Around room | 15 | `self.logic = lambda _: True` | 
| On Gorilla Gone pad | 5 | `l.punch` | 
| On the box | 5 | `self.logic = lambda _: True` | 
| Back of the shed (Chunky) | Balloon | `self.logic = lambda _: True` | 
## Castle Lower Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Path to Crypt | 10 | `self.logic = lambda _: True` | 
| In front of crypt entrance | 5 | `self.logic = lambda _: True` | 
| To and around mausoleum | 10 | `self.logic = lambda _: True` | 
| Between homing ammo pickups next to Funky | 10 | `self.logic = lambda _: True` | 
| Singles from entrance to Funky (Lanky) | 5 | `self.logic = lambda _: True` | 
| Bunches from entrance to tag barrel (Lanky) | 10 | `self.logic = lambda _: True` | 
| Bunches from tag barrel to Funky (Lanky) | 15 | `self.logic = lambda _: True` | 
| Mausoleum door | 5 | `self.logic = lambda _: True` | 
| Behind the mausoleum | 5 | `self.logic = lambda _: True` | 
| Slope towards the crypt | 5 | `self.logic = lambda _: True` | 
| Jump behind the fence near crypt | 5 | `self.logic = lambda _: True` | 
| On top of the skull | 5 | `self.logic = lambda _: True` | 
| Crypt entrance | 5 | `self.logic = lambda _: True` | 
| Above pathway to crypt | Balloon | `self.logic = lambda _: True` | 
| Around mausoleum | Balloon | `self.logic = lambda _: True` | 
| In front of crypt (Diddy) | Balloon | `self.logic = lambda _: True` | 
| In front of Funky (Tiny) | Balloon | `self.logic = lambda _: True` | 
| Tunnel to Funky | Balloon | `self.logic = lambda _: True` | 
## Castle Crypt
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance stairs | 5 | `self.logic = lambda _: True` | 
| Crypt - W1 (1 custom, 1 Diddy) | 10 | `self.logic = lambda _: True` | 
| Crypt - W2 (1 custom, 1 Donkey) | 10 | `self.logic = lambda _: True` | 
| Crypt - W3 | 10 | `self.logic = lambda _: True` | 
| Crypt - Path from warps to T intersection | 5 | `self.logic = lambda _: True` | 
| Crypt - Path to W2 | 10 | `self.logic = lambda _: True` | 
| Crypt - Path to W1 | 15 | `self.logic = lambda _: True` | 
| Crypt - Path to W3 | 10 | `self.logic = lambda _: True` | 
| Back corners of DK's room | 10 | `self.logic = lambda _: True` | 
| Bunch on coffin with pentagon of singles around it | 10 | `self.logic = lambda _: True` | 
| In coffins (Chunky) | 10 | `l.punch or l.CanPhase() or l.generalclips` | 
| Wall of the warps | 10 | `self.logic = lambda _: True` | 
| Torch on Chunky's path | 5 | `self.logic = lambda _: True` | 
| Left torch on Diddy's path | 5 | `self.logic = lambda _: True` | 
| Right torch farther down Diddy's path | 5 | `self.logic = lambda _: True` | 
| Correct levers | 10 | `self.logic = lambda _: True` | 
| Back chimpy charge switches | 10 | `self.logic = lambda _: True` | 
| In the slam coffin | 10 | `l.Slam or l.CanPhase()` | 
| Above warps | Balloon | `self.logic = lambda _: True` | 
| Around coffin in Chunky's room | Balloon | `self.logic = lambda _: True` | 
| Around coffin in Diddy's room | Balloon | `self.logic = lambda _: True` | 
| In coffin in Diddy's room (Diddy) | Balloon | `l.charge or l.generalclips or l.CanPhase()` | 
| In DK's room (Donkey) | Balloon | `self.logic = lambda _: True` | 
| DK's path | Balloon | `self.logic = lambda _: True` | 
| Tilted pineapple switch | Balloon | `self.logic = lambda _: True` | 
## Castle Mausoleum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On Goo hands | 15 | `l.CanSlamSwitch(Levels.CreepyCastle, 3) and l.twirl` | 
| On torches on Tiny's path | 10 | `self.logic = lambda _: True` | 
| Path to Lanky's side | 20 | `self.logic = lambda _: True` | 
| On trombone pad | 5 | `l.grape and l.sprint` | 
| In green goo gap (Tiny) | 5 | `l.twirl or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.tiny)))` | 
| Grape switch | 5 | `self.logic = lambda _: True` | 
| Vines in the Lanky goo room | 5 | `((l.grape and l.sprint) or l.generalclips or l.CanPhase()) and l.trombone and l.can_use_vines` | 
| Slope down Tiny's path | 5 | `self.logic = lambda _: True` | 
| In and out of green goo pit | Balloon | `self.logic = lambda _: True` | 
| Above green goo room | Balloon | `l.twirl or (l.monkey_maneuvers and (not l.isKrushaAdjacent(Kongs.tiny)))` | 
| In Lanky's green goo room (Lanky) | Balloon | `l.sprint or l.generalclips or l.CanPhase()` | 
| Beginning of Lanky's path | Balloon | `self.logic = lambda _: True` | 
## Castle Upper Cave
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Behind Tiny's bonus barrel | 10 | `l.twirl or l.CanPhase()` | 
| Path from moat entrance to Candy (Chunky) | 10 | `self.logic = lambda _: True` | 
| Path from tag barrel to Candy (Chunky) | 15 | `self.logic = lambda _: True` | 
| Path from W1 entrance to tag barrel (Chunky) | 5 | `self.logic = lambda _: True` | 
| Near Candy | 10 | `self.logic = lambda _: True` | 
| Near moat entrance | Balloon | `self.logic = lambda _: True` | 
| Near Candy | Balloon | `self.logic = lambda _: True` | 
| Coming in and out of pit by Tiny's bonus barrel | Balloon | `self.logic = lambda _: True` | 
| Near the dungeon door | Balloon | `self.logic = lambda _: True` | 
## Castle Greenhouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Near osprint barrel | 5 | `self.logic = lambda _: True` | 
| Far dead end | 10 | `self.logic = lambda _: True` | 
| Corner dead end | 5 | `self.logic = lambda _: True` | 
| Group 1 along path (Lanky) | 15 | `self.logic = lambda _: True` | 
| Group 2 along path (Lanky) | 15 | `self.logic = lambda _: True` | 
| Dead end near the arena | Balloon | `self.logic = lambda _: True` | 
## Castle Library
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On switch on books | 5 | `self.logic = lambda _: True` | 
| Path from first room to book hallway | 15 | `self.logic = lambda _: True` | 
| In big books room (Donkey) | 5 | `self.logic = lambda _: True` | 
| In ghost book hallway (Donkey) | 10 | `l.strongKong` | 
| On the big books | 10 | `self.logic = lambda _: True` | 
| Flying books hallway | 10 | `l.strongKong` | 
| In switch room | Balloon | `self.logic = lambda _: True` | 
| In GB room | Balloon | `self.logic = lambda _: True` | 
| Among the flying books | Balloon | `self.logic = lambda _: True` | 
## Castle Museum
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On rock switch | 5 | `self.logic = lambda _: True` | 
| Museum - Path from entrance to main room | 15 | `self.logic = lambda _: True` | 
| Giant bunch on pedestal | 5 | `l.monkeyport` | 
| Pentagon around pedestal | 5 | `l.monkeyport` | 
| On chimneys of car race building | 10 | `self.logic = lambda _: True` | 
| On monkeyport pads on car race side (Tiny) | 10 | `self.logic = lambda _: True` | 
| On monkeyport pad on monument side (Tiny) | 5 | `l.monkeyport or l.CanPhase()` | 
| Inside boulder (Chunky) | 5 | `l.punch and l.barrels` | 
| Around the boulder switch | 10 | `self.logic = lambda _: True` | 
| Around the chimney of the little factory | 5 | `self.logic = lambda _: True` | 
| In hallway to main room | Balloon | `self.logic = lambda _: True` | 
| Around car race | Balloon | `self.logic = lambda _: True` | 
| In monument room (Tiny) | Balloon | `l.feather and (l.monkeyport or l.CanPhase())` | 
| Around middle (Chunky) | Balloon | `self.logic = lambda _: True` | 
| Through the glass | Balloon | `self.logic = lambda _: True` | 
## Castle Tower
| Name | Amount | Logic |
| ---- | ------ | ----- |
| By the entrance | 10 | `self.logic = lambda _: True` | 
| On baboon balloon pad | 5 | `self.logic = lambda _: True` | 
| Around the hole | 10 | `self.logic = lambda _: True` | 
| In tower (Lanky) | Balloon | `self.logic = lambda _: True` | 
## Castle Trash Can
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around trash can | 10 | `self.logic = lambda _: True` | 
| On cheese (Tiny) | 5 | `self.logic = lambda _: True` | 
| On the soda can | 5 | `self.logic = lambda _: True` | 
| Above the cheese | Balloon | `self.logic = lambda _: True` | 
## Castle Tree
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Big Tree - Middle of first room | 5 | `self.logic = lambda _: True` | 
| Around hole on DK's side | 10 | `l.coconut or l.CanPhase()` | 
| Path to Chunky's cage | 10 | `self.logic = lambda _: True` | 
| On plank in water (Donkey) | 5 | `l.coconut` | 
| By punchable wall (Chunky) | 5 | `self.logic = lambda _: True` | 
| First room | 5 | `self.logic = lambda _: True` | 
| Against the pineapple gate | 5 | `self.logic = lambda _: True` | 
| Coconut switch | 5 | `self.logic = lambda _: True` | 
| Underwater tunnel | 5 | `(l.coconut or l.generalclips or l.CanPhase()) and l.swim` | 
| First room | Balloon | `self.logic = lambda _: True` | 
| Above hole (Donkey) | Balloon | `self.logic = lambda _: True` | 
| In Chunky's room (Chunky) | Balloon | `self.logic = lambda _: True` | 

# DK Isles
## Treehouse
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Next to the Radio | 5 | `self.logic = lambda _: True` | 
| On the crate | 5 | `self.logic = lambda _: True` | 
| On the hammock | 5 | `self.logic = lambda _: True` | 
| Above the exit | 5 | `self.logic = lambda _: True` | 
| In DK's Treehouse | Balloon | `self.logic = lambda _: True` | 
## Training Grounds
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Treehouse balcony | 5 | `l.climbing` | 
| Windowsills | 10 | `l.climbing` | 
| Tree front of treehouse | 5 | `l.climbing` | 
| Tree right of treehouse | 5 | `l.climbing` | 
| Tree next to rear tunnel | 5 | `l.climbing` | 
| On exit ledge | 10 | `(l.istiny and l.twirl) and l.climbing` | 
| On rear ledge | 10 | `l.climbing` | 
| Path to Cranky | 10 | `self.logic = lambda _: True` | 
| Around Cranky | 5 | `self.logic = lambda _: True` | 
| Next to Cranky | 10 | `self.logic = lambda _: True` | 
| Path to training area | 5 | `self.logic = lambda _: True` | 
| In the lake | 15 | `l.swim` | 
| Behind the waterfall | 5 | `self.logic = lambda _: True` | 
| Banana hoard tunnel | 10 | `l.can_use_vines and l.climbing` | 
| Banana hoard room | 20 | `l.can_use_vines and l.climbing` | 
| Rear tunnel | 5 | `self.logic = lambda _: True` | 
| Around rear dirt patch | 10 | `self.logic = lambda _: True` | 
| Exit tunnel | 10 | `self.logic = lambda _: True` | 
| Tree in training area | 5 | `l.climbing and (l.istiny and l.twirl)` | 
| Around treehouse tree | 10 | `self.logic = lambda _: True` | 
| Training area | 5 | `self.logic = lambda _: True` | 
| On the signposts | 10 | `self.logic = lambda _: True` | 
| Above the lake | Balloon | `self.logic = lambda _: True` | 
| Banana hoard room | Balloon | `self.logic = lambda _: True` | 
| Around the treehouse | Balloon | `self.logic = lambda _: True` | 
| Above rear ledge | Balloon | `self.logic = lambda _: True` | 
| Above exit ledge | Balloon | `self.logic = lambda _: True` | 
| Next to Cranky | Balloon | `self.logic = lambda _: True` | 
| Training Area | Balloon | `self.logic = lambda _: True` | 
| Rear tunnel | Balloon | `self.logic = lambda _: True` | 
| Exit tunnel | Balloon | `self.logic = lambda _: True` | 
## Isles
| Name | Amount | Logic |
| ---- | ------ | ----- |
| W1 | 5 | `self.logic = lambda _: True` | 
| W2 | 5 | `self.logic = lambda _: True` | 
| W3 | 5 | `self.logic = lambda _: True` | 
| W4 | 5 | `self.logic = lambda _: True` | 
| W5 | 5 | `self.logic = lambda _: True` | 
| K.Lumsy W1 | 5 | `self.logic = lambda _: True` | 
| Aztec W2 | 5 | `self.logic = lambda _: True` | 
| Waterfall W3 | 5 | `self.logic = lambda _: True` | 
| Factory W4 | 5 | `self.logic = lambda _: True` | 
| Fairy Isle W5 | 5 | `self.logic = lambda _: True` | 
| Japes entrance | 5 | `self.logic = lambda _: True` | 
| Tree between tag barrel and Japes | 5 | `(l.climbing) or (Events.AirSpaceEntered in l.Events and l.isdiddy)` | 
| Tree between tag barrel and Japes | 5 | `self.logic = lambda _: True` | 
| Tree next to Japes | 5 | `(l.climbing) or (Events.AirSpaceEntered in l.Events and l.isdiddy)` | 
| Tree next to Japes | 5 | `self.logic = lambda _: True` | 
| Tree on beaver beach | 5 | `(l.climbing) or (Events.AirSpaceEntered in l.Events and l.isdiddy)` | 
| Tree on beaver beach | 5 | `self.logic = lambda _: True` | 
| Tree near W3 | 5 | `(l.climbing) or (Events.AirSpaceEntered in l.Events and l.isdiddy)` | 
| Tree near W3 | 5 | `self.logic = lambda _: True` | 
| Behind cannon to Forest | 5 | `self.logic = lambda _: True` | 
| Waterfall pond | 15 | `l.swim` | 
| Seafloor around the X platform | 10 | `l.swim` | 
| In the pineapple cage | 10 | `l.pineapple or l.CanSTS() or l.CanPhase()` | 
| Beach below Caves | 5 | `self.logic = lambda _: True` | 
| Tree below Caves | 5 | `self.logic = lambda _: True` | 
| Path below Caves | 5 | `self.logic = lambda _: True` | 
| Stairs near Aztec | 10 | `self.logic = lambda _: True` | 
| Behind Aztec lobby | 5 | `self.logic = lambda _: True` | 
| Aztec lobby roof | 20 | `self.logic = lambda _: True` | 
| On trombone boulder | 5 | `self.logic = lambda _: True` | 
| On triangle boulder | 5 | `self.logic = lambda _: True` | 
| Between DK Isle's nostrils | 5 | `self.logic = lambda _: True` | 
| Caves lobby ledge | 5 | `self.logic = lambda _: True` | 
| Above Caves lobby | 15 | `self.logic = lambda _: True` | 
| Forest lobby roof | 10 | `self.logic = lambda _: True` | 
| Flower sniffing near Forest | 5 | `self.logic = lambda _: True` | 
| In the peanut cage | 10 | `l.peanut` | 
| Waterfall upstream | 5 | `self.logic = lambda _: True` | 
| Flower next to peanut cage | 5 | `self.logic = lambda _: True` | 
| Waterfall freefall | 10 | `self.logic = lambda _: True` | 
| DK Isle peaks | 10 | `self.logic = lambda _: True` | 
| Above the Pound the X rock | 5 | `self.logic = lambda _: True` | 
| On DK Isle's ear above Aztec | 15 | `self.logic = lambda _: True` | 
| On DK Isle's eyebrows | 10 | `self.logic = lambda _: True` | 
| On Fairy Isle's banana peel hat right | 5 | `self.logic = lambda _: True` | 
| On Fairy Isle's banana peel hat left | 5 | `self.logic = lambda _: True` | 
| On top of Fairy Isle | 5 | `self.logic = lambda _: True` | 
| On Fairy Isle's wings | 10 | `self.logic = lambda _: True` | 
| On the fairy tree | 5 | `self.logic = lambda _: True` | 
| Around the fairy tree | 5 | `self.logic = lambda _: True` | 
| In the feather cage | 10 | `l.feather or l.CanSTS() or l.CanPhase()` | 
| Fairy Isle entrance | 5 | `self.logic = lambda _: True` | 
| In the Pound the X rock | 10 | `Events.IslesChunkyBarrelSpawn in l.Events and l.hunkyChunky and l.Slam and l.chunky` | 
| Tag barrel shore | 10 | `self.logic = lambda _: True` | 
| Around Fairy Isle | 10 | `self.logic = lambda _: True` | 
| Under K.Lumsy's prison | 5 | `l.swim` | 
| Around Castle cannon | 10 | `(l.settings.open_lobbies or Events.ForestKeyTurnedIn in l.Events)` | 
| On top of K.Lumsy's prison | 5 | `( (l.hasMoveSwitchsanity(Switches.IslesMonkeyport) and ((l.istiny and l.twirl) or (l.settings.damage_amount != DamageAmount.ohko))) or ((l.settings.open_lobbies or Events.GalleonKeyTurnedIn in l.Events) and Events.IslesDiddyBarrelSpawn in l.Events and l.isdiddy and l.jetpack) or ( (l.settings.open_lobbies or Events.AztecKeyTurnedIn in l.Events) and (l.isdonkey and (not l.isKrushaAdjacent(Kongs.donkey)) and (l.settings.damage_amount != DamageAmount.ohko)) or (l.istiny and l.twirl) ) )` | 
| On top of side pipes | 15 | `self.logic = lambda _: True` | 
| Lower Monkeyport pad | 5 | `self.logic = lambda _: True` | 
| Upper Monkeyport pad | 5 | `self.logic = lambda _: True` | 
| Saxophone pad | 5 | `self.logic = lambda _: True` | 
| On vines to Snide | 5 | `l.can_use_vines` | 
| On Krem Isle's right arm | 5 | `self.logic = lambda _: True` | 
| On Krem Isle's left arm | 5 | `self.logic = lambda _: True` | 
| Path to Factory | 15 | `self.logic = lambda _: True` | 
| Key 2 rising platform | 5 | `self.logic = lambda _: True` | 
| Underwater behind propellers | 10 | `l.swim` | 
| Under path to Factory | 10 | `self.logic = lambda _: True` | 
| Prison cable | 5 | `self.logic = lambda _: True` | 
| Back of Krem Isle | 10 | `self.logic = lambda _: True` | 
| Snide ledge | 5 | `self.logic = lambda _: True` | 
| In the coconut cage | 10 | `l.coconut` | 
| In the grape cage | 10 | `l.grape or l.CanPhaseswim() or l.CanPhase()` | 
| Around the tree below caves | 5 | `self.logic = lambda _: True` | 
| Butterflies near Japes | 5 | `self.logic = lambda _: True` | 
| Dry plant thing near Aztec | 5 | `self.logic = lambda _: True` | 
| Steps to Factory lobby | 5 | `self.logic = lambda _: True` | 
| Directly under Galleon lobby | 5 | `l.swim` | 
| Waterfall lower | Balloon | `self.logic = lambda _: True` | 
| Waterfall upper | Balloon | `self.logic = lambda _: True` | 
| Above bananaports | Balloon | `self.logic = lambda _: True` | 
| Japes shore | Balloon | `self.logic = lambda _: True` | 
| Beaver beach | Balloon | `self.logic = lambda _: True` | 
| Between pineapple cage and the X platform | Balloon | `self.logic = lambda _: True` | 
| Around the tree below caves | Balloon | `self.logic = lambda _: True` | 
| Near Aztec | Balloon | `self.logic = lambda _: True` | 
| In front of DK Isle's eyes | Balloon | `self.logic = lambda _: True` | 
| Around the fairy tree | Balloon | `self.logic = lambda _: True` | 
| Front of Fairy Isle | Balloon | `self.logic = lambda _: True` | 
| Top of Fairy Isle | Balloon | `self.logic = lambda _: True` | 
| Behind Aztec | Balloon | `self.logic = lambda _: True` | 
| Near Forest | Balloon | `self.logic = lambda _: True` | 
| Near the Krem Krown | Balloon | `self.logic = lambda _: True` | 
| Upper Factory Path | Balloon | `self.logic = lambda _: True` | 
| Big pipe in Krem Isle middle back | Balloon | `self.logic = lambda _: True` | 
## KLumsy
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Inside K.Lumsy's cage | 15 | `l.IsKLumsyFree()` | 
| Prison sprint cage | 10 | `(l.sprint and l.lanky)` | 
## Isles Snide Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the Snide boulder | 5 | `self.logic = lambda _: True` | 
| Above Snide's doorway | 5 | `(l.spring and l.diddy)` | 
| Around Snide | Balloon | `self.logic = lambda _: True` | 
## Jungle Japes Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| On the boulder | 5 | `self.logic = lambda _: True` | 
| Around the boulder | 5 | `self.logic = lambda _: True` | 
| Right torch | 5 | `self.logic = lambda _: True` | 
| Left torch | 5 | `self.logic = lambda _: True` | 
| Back left torch | 5 | `self.logic = lambda _: True` | 
| Lanky door | 5 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Tiny door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `self.logic = lambda _: True` | 
| Chunky door | 5 | `self.logic = lambda _: True` | 
| Middle path | 5 | `self.logic = lambda _: True` | 
| Around B.Locker | 5 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| Left side | Balloon | `self.logic = lambda _: True` | 
| Right side | Balloon | `self.logic = lambda _: True` | 
## Angry Aztec Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Right ramp | 5 | `self.logic = lambda _: True` | 
| Left ramp | 5 | `self.logic = lambda _: True` | 
| Ridge between the posts | 5 | `self.logic = lambda _: True` | 
| Between the Columns | 5 | `self.logic = lambda _: True` | 
| Around the barrel hole | 10 | `self.logic = lambda _: True` | 
| Also around the barrel hole | 10 | `self.logic = lambda _: True` | 
| Tunnel | 5 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Back room | 15 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Left post | 5 | `self.logic = lambda _: True` | 
| Right post | 5 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `self.logic = lambda _: True` | 
| Tiny door | 5 | `self.logic = lambda _: True` | 
| Lanky door | 5 | `self.logic = lambda _: True` | 
| Chunky door (back room wall) | 5 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| On the gongs | 10 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| Torch above Donkey door | 5 | `self.logic = lambda _: True` | 
| Back room torches | 10 | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
| Between columns | Balloon | `self.logic = lambda _: True` | 
| Above B.Locker | Balloon | `self.logic = lambda _: True` | 
| Back room | Balloon | `l.hasMoveSwitchsanity(Switches.IslesAztecLobbyFeather, False) or l.CanPhase()` | 
## Frantic Factory Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Entrance | 10 | `self.logic = lambda _: True` | 
| On the box | 5 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Chunky door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Tiny door | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Lanky door | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| On the lever | 5 | `self.logic = lambda _: True` | 
| Bongo pad | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Bridge | 10 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| In the box | 5 | `l.punch and l.chunky` | 
| Post after bridge | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Stairs | 5 | `((l.grab and l.donkey) or (l.monkey_maneuvers and (l.isdiddy or l.istiny)))` | 
| Towards doors | 10 | `self.logic = lambda _: True` | 
| Tag barrel | 5 | `self.logic = lambda _: True` | 
| Vents | Balloon | `self.logic = lambda _: True` | 
| Between pipes | Balloon | `self.logic = lambda _: True` | 
| Upper path | Balloon | `self.logic = lambda _: True` | 
## Gloomy Galleon Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Underwater entrance | 5 | `self.logic = lambda _: True` | 
| Under tag barrel | 5 | `self.logic = lambda _: True` | 
| Underwater along the wall | 10 | `self.logic = lambda _: True` | 
| Kasplat platform | 10 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Chunky door | 5 | `self.logic = lambda _: True` | 
| Tiny door | 5 | `self.logic = lambda _: True` | 
| Lanky door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `self.logic = lambda _: True` | 
| Chunky switch | 5 | `self.logic = lambda _: True` | 
| Right water torch | 5 | `self.logic = lambda _: True` | 
| Left water torch | 5 | `self.logic = lambda _: True` | 
| Right land torch | 5 | `self.logic = lambda _: True` | 
| Left land torch | 5 | `self.logic = lambda _: True` | 
| On the Tiny platform | 15 | `l.swim and ((l.mini and l.twirl and l.tiny and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.chunky) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
| Mini tunnel | 5 | `l.swim and ((l.mini and l.twirl and l.tiny and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.chunky) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
| Above water | Balloon | `self.logic = lambda _: True` | 
| Above land | Balloon | `self.logic = lambda _: True` | 
| In the Tiny room | Balloon | `l.swim and ((l.mini and l.twirl and l.tiny and l.CanSlamSwitch(Levels.GloomyGalleon, 2) and l.chunky) or l.CanPhaseswim()) and (not l.IsLavaWater() or l.Melons >= 3)` | 
## Fungi Forest Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Tiny door (back wall) | 5 | `self.logic = lambda _: True` | 
| Chunky door (right wall) | 5 | `self.logic = lambda _: True` | 
| Lanky door (right corner) | 5 | `self.logic = lambda _: True` | 
| Where the lever used to be | 5 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| Center line | 5 | `self.logic = lambda _: True` | 
| Gorilla Gone pad | 5 | `((l.coconut and l.donkey) and (l.peanut and l.diddy) and (l.grape and l.lanky) and (l.feather and l.tiny) and (l.pineapple and l.chunky) or l.CanPhase())` | 
| Crazy fairy balloon | Balloon | `self.logic = lambda _: True` | 
| Wrinkly wheel (back wall) | Balloon | `self.logic = lambda _: True` | 
## Crystal Caves Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Left path | 5 | `self.logic = lambda _: True` | 
| Right path | 5 | `self.logic = lambda _: True` | 
| Bridge | 10 | `self.logic = lambda _: True` | 
| Around the boulder | 10 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Path to boulder | 5 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Left side crystals | 15 | `self.logic = lambda _: True` | 
| Right side crystals | 10 | `self.logic = lambda _: True` | 
| Entrance | 10 | `self.logic = lambda _: True` | 
| On the boulder | 5 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Lanky door | 5 | `self.logic = lambda _: True` | 
| Chunky door | 5 | `self.logic = lambda _: True` | 
| Tiny door | 5 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `l.jetpack` | 
| Guitar pad | 5 | `l.jetpack` | 
| Behind the lava ice wall | 5 | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Lava room | 20 | `((l.punch and l.chunky) or l.CanPhase() or l.ledgeclip) and l.strongKong` | 
| In the air | 10 | `l.jetpack` | 
| In the lava | Balloon | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
| Around the bridge | Balloon | `self.logic = lambda _: True` | 
| Boulder room | Balloon | `(l.punch and l.chunky) or l.CanPhase() or l.ledgeclip` | 
## Creepy Castle Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Chunky door | 5 | `self.logic = lambda _: True` | 
| Donkey door | 5 | `self.logic = lambda _: True` | 
| Diddy door | 5 | `self.logic = lambda _: True` | 
| Lanky door | 5 | `self.logic = lambda _: True` | 
| Tiny door | 5 | `self.logic = lambda _: True` | 
| On the boulder | 5 | `self.logic = lambda _: True` | 
| Around the boulder | 5 | `self.logic = lambda _: True` | 
| Kasplat cage | 5 | `(l.coconut and l.donkey) or l.CanPhase()` | 
| Around the lobby | 15 | `self.logic = lambda _: True` | 
| Right torch | 5 | `l.chunky and l.barrels` | 
| Left torch | 5 | `l.chunky and l.barrels` | 
| Stairs | 5 | `self.logic = lambda _: True` | 
| Above the entrance hole | 5 | `self.logic = lambda _: True` | 
| Torch way up | 10 | `l.chunky and l.barrels and l.balloon` | 
| Wall windows | 20 | `l.chunky and l.barrels and l.balloon` | 
| Acid moat | Balloon | `self.logic = lambda _: True` | 
| Above center piece | Balloon | `self.logic = lambda _: True` | 
| Near B.Locker | Balloon | `self.logic = lambda _: True` | 
## Hideout Helm Lobby
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Chunky pad | 5 | `self.logic = lambda _: True` | 
| W1 | 5 | `self.logic = lambda _: True` | 
| Under bonus barrel | 5 | `l.hasMoveSwitchsanity(Switches.IslesHelmLobbyGone, False) and l.can_use_vines` | 
| Kasplat island | 5 | `l.scope and l.coconut` | 
| Right side | 5 | `self.logic = lambda _: True` | 
| Left side | 5 | `self.logic = lambda _: True` | 
| Far W1 | 5 | `self.logic = lambda _: True` | 
| Around Kasplat island | Balloon | `self.logic = lambda _: True` | 
| Left side | Balloon | `self.logic = lambda _: True` | 
## Banana Fairy Room
| Name | Amount | Logic |
| ---- | ------ | ----- |
| Around the fairy | 5 | `self.logic = lambda _: True` | 
| Front corner torches | 10 | `self.logic = lambda _: True` | 
| Back corner torches | 10 | `self.logic = lambda _: True` | 
| Front ramp | 5 | `self.logic = lambda _: True` | 
| Left ramp | 5 | `self.logic = lambda _: True` | 
| Right ramp | 5 | `self.logic = lambda _: True` | 
| Back ramp | 5 | `self.logic = lambda _: True` | 
| Throne | 5 | `self.logic = lambda _: True` | 
| Rareware GB room | 20 | `self.logic = lambda _: True` | 
| Rareware GB room | Balloon | `self.logic = lambda _: True` | 
| Around the fairy | Balloon | `self.logic = lambda _: True` | 
