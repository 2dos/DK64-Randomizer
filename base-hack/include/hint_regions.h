/*
	This file is automatically written to by build_hint_regions.py
	Don't directly modify this file, instead modify the script
	Otherwise your changes will be overwritten on next build

	Thanks,
		Ballaam
*/

typedef enum regions {
	/* 0x000 */ REGION_NULLREGION, // ???
	/* 0x001 */ REGION_SHOPISLES, // Isles Shops
	/* 0x002 */ REGION_SHOPJAPES, // Japes Shops
	/* 0x003 */ REGION_SHOPAZTEC, // Aztec Shops
	/* 0x004 */ REGION_SHOPFACTORY, // Factory Shops
	/* 0x005 */ REGION_SHOPGALLEON, // Galleon Shops
	/* 0x006 */ REGION_SHOPFUNGI, // Forest Shops
	/* 0x007 */ REGION_SHOPCAVES, // Caves Shops
	/* 0x008 */ REGION_SHOPCASTLE, // Castle Shops
	/* 0x009 */ REGION_JETPAC, // Jetpac Game
	/* 0x00A */ REGION_MEDALSISLES, // Isles Medal Rewards
	/* 0x00B */ REGION_MEDALSJAPES, // Japes Medal Rewards
	/* 0x00C */ REGION_MEDALSAZTEC, // Aztec Medal Rewards
	/* 0x00D */ REGION_MEDALSFACTORY, // Factory Medal Rewards
	/* 0x00E */ REGION_MEDALSGALLEON, // Galleon Medal Rewards
	/* 0x00F */ REGION_MEDALSFUNGI, // Forest Medal Rewards
	/* 0x010 */ REGION_MEDALSCAVES, // Caves Medal Rewards
	/* 0x011 */ REGION_MEDALSCASTLE, // Castle Medal Rewards
	/* 0x012 */ REGION_GAMESTART, // Game Start
	/* 0x013 */ REGION_CREDITS, // Credits
	/* 0x014 */ REGION_ISLESMAIN, // Main Isle
	/* 0x015 */ REGION_ISLESOUTER, // Outer Isles
	/* 0x016 */ REGION_ISLESKREM, // Krem Isle
	/* 0x017 */ REGION_ISLESRAREWARE, // Rareware Banana Room
	/* 0x018 */ REGION_ISLESLOBBIES0, // Japes - Forest Lobbies
	/* 0x019 */ REGION_ISLESLOBBIES1, // Caves - Helm Lobbies
	/* 0x01A */ REGION_ISLESKROOL, // K Rool Arena
	/* 0x01B */ REGION_JAPESLOW, // Japes Lowlands
	/* 0x01C */ REGION_JAPESHIGH, // Japes Hillside
	/* 0x01D */ REGION_JAPESSTORM, // Stormy Tunnel Area
	/* 0x01E */ REGION_JAPESHIVE, // Hive Tunnel Area
	/* 0x01F */ REGION_JAPESCAVERNS, // Japes Caves and Mines
	/* 0x020 */ REGION_AZTECOASISTOTEM, // Aztec Oasis and Totem Area
	/* 0x021 */ REGION_AZTECTINY, // Tiny Temple
	/* 0x022 */ REGION_AZTECGETOUT, // 5 Door Temple
	/* 0x023 */ REGION_AZTECLLAMA, // Llama Temple
	/* 0x024 */ REGION_AZTECTUNNELS, // Various Aztec Tunnels
	/* 0x025 */ REGION_FACTORYSTART, // Frantic Factory Start
	/* 0x026 */ REGION_FACTORYTESTING, // Testing Area
	/* 0x027 */ REGION_FACTORYRESEARCH, // Research and Development Area
	/* 0x028 */ REGION_FACTORYSTORAGE, // Storage and Arcade
	/* 0x029 */ REGION_FACTORYPROD, // Production Room
	/* 0x02A */ REGION_GALLEONCAVERNS, // Galleon Caverns
	/* 0x02B */ REGION_GALLEONLIGHTHOUSE, // Lighthouse Area
	/* 0x02C */ REGION_GALLEONSHIPYARD, // Shipyard Outskirts
	/* 0x02D */ REGION_GALLEONTREASURE, // Treasure Room
	/* 0x02E */ REGION_GALLEONSHIP, // 5 Door Ship
	/* 0x02F */ REGION_FORESTSTART, // Forest Center and Beanstalk
	/* 0x030 */ REGION_FORESTGMEXT, // Giant Mushroom Exterior
	/* 0x031 */ REGION_FORESTGMINT, // Giant Mushroom Insides
	/* 0x032 */ REGION_FORESTOWL, // Owl Tree
	/* 0x033 */ REGION_FORESTMILLS, // Forest Mills
	/* 0x034 */ REGION_CAVESMAIN, // Main Caves Area
	/* 0x035 */ REGION_CAVESIGLOO, // Igloo Area
	/* 0x036 */ REGION_CAVESCABINS, // Cabins Area
	/* 0x037 */ REGION_CASTLEEXT, // Castle Surroundings
	/* 0x038 */ REGION_CASTLEROOMS, // Castle Rooms
	/* 0x039 */ REGION_CASTLEUNDERGROUND, // Castle Underground
	/* 0x03A */ REGION_OTHERHELM, // Hideout Helm
	/* 0x03B */ REGION_OTHERTNS, // Troff n Scoff
	/* 0x03C */ REGION_ERROR, // This should not be hinted
} regions;
extern char* hint_region_names[61];extern char* unknown_hints[5];