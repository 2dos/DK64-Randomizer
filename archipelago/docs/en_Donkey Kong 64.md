# Donkey Kong 64

## Where is the settings page?

The [player settings page for this game](../player-settings) contains all the options you need to configure and export a config file.

## What does randomization do to this game?

Items which the player would normally acquire throughout the game have been moved around. Logic remains, so the game is
always able to be completed, but because of the item shuffle the player may need to access certain areas before they
would in the vanilla game.

In addition, the level entrances from DK Isles have been swapped around. This means that you may find Creepy Castle where the entrance for Jungle Japes normally is, and so on.

Due to some technical constraints brought on by the Archipelago framework, a number of changes have been made from the regular Donkey Kong 64 randomizer logic, including:
- Tag Anywhere / freely switching Kongs is considered in logic
- Purchases from shopkeepers (Cranky/Funky/Candy) are free
- B. Lockers costs are 0 Golden Bananas for all levels, except Hideout Helm which needs 60 Golden Bananas
- Banana Medal checks are sent after collecting 40 of the same colored bananas in a world, down from 75

These restrictions may be changed in future updates to this APWorld.

## What is the goal of Donkey Kong 64 when randomized?

Currently, two goals can be selected:

- Defeat King K. Rool
- Find all the Keys for K. Lumsy's cage

## What items and locations get shuffled?

### Items

- Playable Kongs
- Golden Bananas
- Banana Fairies
- Banana Medals
- All Keys for K. Lumsy's cage, except Key 8
- Blast-o-Matic blueprints
- Instruments, guns and respective upgrades
- Training Grounds moves
- Cranky's Lab moves/potions
- The Banana Fairy Camera
- The Bean in Fungi Forest
- The Pearls in Gloomy Galleon

### Locations
- Golden Banana / Banana Fairy Locations
- Banana Medal rewards
- Cranky's Lab / Funky's Armoury / Candy's Music Shop rewards
- Rainbow Coin dirt patches
- Kasplat item drops
- DK Arcade / Jetpac rewards
- Boss rewards

## Which items can be in another player's world?

All of the major items listed above can be randomized into other games. In addition, there are filler items that refill your health or consumable "ammo" for certain moves, including gun ammo, Orange Grenades, Crystal Coconuts, Banana Camera film, and instrument energy. Traps are also available in the item pool, but trap spawning can be reduced or disabled entirely in your YAML settings.

Due to current technical restraints, the rewards for returning the Blast-o-Matic blueprints to Snide will always be Golden Bananas.

## What does another world's item look like in Donkey Kong 64?

Items from other games will appear as an Archipelago icon. When you collect them, a message will appear on screen showing the item's name and who it is for.

## When the player receives an item, what happens?

A message will appear on screen showing what item you received and who sent it.
