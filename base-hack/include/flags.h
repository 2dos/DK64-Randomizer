#include "rom_version.h"

#if ROM_VERSION < 2
	// US/PAL

	#define FLAG_WATERFALL 0x17A // Waterfall Cutscene
	#define FLAG_ESCAPE 0x186 // Escape Cutscene
	
	// Kong FTTs
	#define FLAG_FTT_DIDDY 0x16F // Diddy FTT
	#define FLAG_FTT_LANKY 0x170 // Lanky FTT
	#define FLAG_FTT_TINY 0x171 // Tiny FTT
	#define FLAG_FTT_CHUNKY 0x172 // Chunky FTT

	#define FLAG_ABILITY_CAMERA 0x179 // Camera
	#define FLAG_ABILITY_SIMSLAM 0x180 // Cranky Sim Slam Acquired
	
	// Warp Flags
	#define FLAG_WARP_JAPES_W1_PORTAL 0x20
	#define FLAG_WARP_JAPES_W1_FAR 0x21
	#define FLAG_WARP_JAPES_W2_HIGH 0x22
	#define FLAG_WARP_JAPES_W2_LOW 0x23
	#define FLAG_WARP_JAPES_W3_RIGHT 0x24
	#define FLAG_WARP_JAPES_W3_LEFT 0x25
	#define FLAG_WARP_JAPES_W4_CLOSE 0x28
	#define FLAG_WARP_JAPES_W4_CRANKY 0x29
	#define FLAG_WARP_JAPES_W5_SHELLHIVE 0x26
	#define FLAG_WARP_JAPES_W5_TOP 0x27

	#define FLAG_WARP_AZTEC_W1_PORTAL 0x4F
	#define FLAG_WARP_AZTEC_W1_CANDY 0x50
	#define FLAG_WARP_AZTEC_W2_TEMPLE 0x51
	#define FLAG_WARP_AZTEC_W2_TOTEM 0x52
	#define FLAG_WARP_AZTEC_W3_CRANKY 0x53
	#define FLAG_WARP_AZTEC_W3_TOTEM 0x54
	#define FLAG_WARP_AZTEC_W4_TOTEM 0x55
	#define FLAG_WARP_AZTEC_W4_FUNKY 0x56
	#define FLAG_WARP_AZTEC_W5_TOTEM 0x57
	#define FLAG_WARP_AZTEC_W5_SNOOP 0x3E // GB Flag

	#define FLAG_WARP_LLAMA_W1_HIGH 0x58
	#define FLAG_WARP_LLAMA_W1_LOW 0x59
	#define FLAG_WARP_LLAMA_W2_FAR 0x5A
	#define FLAG_WARP_LLAMA_W2_LOW 0x5B	

	#define FLAG_WARP_FACTORY_W1_FOYER 0x8D
	#define FLAG_WARP_FACTORY_W1_STORAGE 0x8E
	#define FLAG_WARP_FACTORY_W2_FOYER 0x8F
	#define FLAG_WARP_FACTORY_W2_RND 0x90
	#define FLAG_WARP_FACTORY_W3_FOYER 0x91
	#define FLAG_WARP_FACTORY_W3_SNIDE 0x92
	#define FLAG_WARP_FACTORY_W4_TOP 0x93
	#define FLAG_WARP_FACTORY_W4_BOTTOM 0x94
	#define FLAG_WARP_FACTORY_W5_FUNKY 0x95
	#define FLAG_WARP_FACTORY_W5_ARCADE 0x96

	#define FLAG_WARP_GALLEON_W1_LIGHTHOUSE 0xB1
	#define FLAG_WARP_GALLEON_W1_CRANKY 0xB2
	#define FLAG_WARP_GALLEON_W2_2DS 0xAB
	#define FLAG_WARP_GALLEON_W2_CRANKY 0xAC
	#define FLAG_WARP_GALLEON_W3_SNIDE 0xAD
	#define FLAG_WARP_GALLEON_W3_CRANKY 0xAE
	#define FLAG_WARP_GALLEON_W4_SEAL 0xAF
	#define FLAG_WARP_GALLEON_W4_TOWER 0xA3 // GB Flag
	#define FLAG_WARP_GALLEON_W5_5DS 0xA9
	#define FLAG_WARP_GALLEON_W5_LIGHTHOUSE 0xAA

	#define FLAG_WARP_FUNGI_W1_MILL 0xED
	#define FLAG_WARP_FUNGI_W1_CLOCK 0xEE
	#define FLAG_WARP_FUNGI_W2_CLOCK 0xEF
	#define FLAG_WARP_FUNGI_W2_FUNKY 0xF0
	#define FLAG_WARP_FUNGI_W3_CLOCK 0xF1
	#define FLAG_WARP_FUNGI_W3_MUSH 0xF2
	#define FLAG_WARP_FUNGI_W4_CLOCK 0xF3
	#define FLAG_WARP_FUNGI_W4_OWL 0xF4
	#define FLAG_WARP_FUNGI_W5_LOW 0xF5
	#define FLAG_WARP_FUNGI_W5_HIGH 0xF6

	#define FLAG_WARP_CAVES_W1_5DI 0x11B
	#define FLAG_WARP_CAVES_W1_PORTAL 0x11C
	#define FLAG_WARP_CAVES_W2_PORTAL 0x11D
	#define FLAG_WARP_CAVES_W2_FAR 0x11E
	#define FLAG_WARP_CAVES_W3_5DI 0x123
	#define FLAG_WARP_CAVES_W3_CAVERN 0x127 // GB Flag
	#define FLAG_WARP_CAVES_W4_FAR 0x11F
	#define FLAG_WARP_CAVES_W4_5DI 0x120
	#define FLAG_WARP_CAVES_W5_5DC 0x121
	#define FLAG_WARP_CAVES_W5_PILLAR 0x122

	#define FLAG_WARP_CASTLE_W1_HUB 0x147
	#define FLAG_WARP_CASTLE_W1_FAR 0x148
	#define FLAG_WARP_CASTLE_W2_HUB 0x149
	#define FLAG_WARP_CASTLE_W2_HIGH 0x14A
	#define FLAG_WARP_CASTLE_W3_HUB 0x14B
	#define FLAG_WARP_CASTLE_W3_HIGH 0x14C
	#define FLAG_WARP_CASTLE_W4_HUB 0x14D
	#define FLAG_WARP_CASTLE_W4_HIGH 0x14E
	#define FLAG_WARP_CASTLE_W5_HUB 0x14F
	#define FLAG_WARP_CASTLE_W5_HIGH 0x150

	#define FLAG_WARP_CRYPT_W1_CLOSE 0x151
	#define FLAG_WARP_CRYPT_W1_FAR 0x152
	#define FLAG_WARP_CRYPT_W2_CLOSE 0x153
	#define FLAG_WARP_CRYPT_W2_FAR 0x154
	#define FLAG_WARP_CRYPT_W3_CLOSE 0x155
	#define FLAG_WARP_CRYPT_W3_FAR 0x156

	#define FLAG_WARP_LOBBY_W1_NEAR 0x1A1
	#define FLAG_WARP_LOBBY_W1_FAR 0x1A2

	#define FLAG_WARP_ISLES_W1_RING 0x1B1
	#define FLAG_WARP_ISLES_W1_FAR 0x1B2
	#define FLAG_WARP_ISLES_W2_RING 0x1B3
	#define FLAG_WARP_ISLES_W2_FAR 0x1B4
	#define FLAG_WARP_ISLES_W3_RING 0x1B5
	#define FLAG_WARP_ISLES_W3_FAR 0x1B6
	#define FLAG_WARP_ISLES_W4_RING 0x1B7
	#define FLAG_WARP_ISLES_W4_HIGH 0x1B8
	#define FLAG_WARP_ISLES_W5_RING 0x1BA
	#define FLAG_WARP_ISLES_W5_FAR 0x1B9

	#define FLAG_WARP_HELM_W1_NEAR 0x305
	#define FLAG_WARP_HELM_W1_FAR 0x306

	#define FLAG_CUTSCENE_DIDDYHELPME 0x2A // Diddy Help Me Cutscene
	#define FLAG_CUTSCENE_LLAMA 0x5C // Llama Cutscene
	#define FLAG_CUTSCENE_KOSHA 0x12B // GK Cutscene

	#define FLAG_FTT_BLOCKER 0x17E // B Locker FTT
	#define FLAG_FTT_BANANAPORT 0x163 // Bananaport FTT
	#define FLAG_FTT_CROWNPAD 0x166 // Crown Pad FTT

	// Barrel Ability FTTs
	#define FLAG_FTT_STRONGKONG 0x16B // SK FTT
	#define FLAG_FTT_ORANGSPRINT 0x16A // OSS FTT
	#define FLAG_FTT_MINIMONKEY 0x168 // MM FTT
	#define FLAG_FTT_HUNKYCHUNKY 0x169 // HC FTT

	// Keys in Possession
	#define FLAG_KEYHAVE_KEY1 0x1A // Key 1 Have
	#define FLAG_KEYHAVE_KEY2 0x4A // Key 2 Have
	#define FLAG_KEYHAVE_KEY3 0x8A // Key 3 Have
	#define FLAG_KEYHAVE_KEY4 0xA8 // Key 4 Have
	#define FLAG_KEYHAVE_KEY5 0xEC // Key 5 Have
	#define FLAG_KEYHAVE_KEY6 0x124 // Key 6 Have
	#define FLAG_KEYHAVE_KEY7 0x13D // Key 7 Have
	#define FLAG_KEYHAVE_KEY8 0x17C // Key 8 Have

	// Keys turned in/japes
	#define FLAG_KEYIN_JAPES 0x1BB // Japes Open
	#define FLAG_KEYIN_KEY1 0x1BC // Key 1 In
	#define FLAG_KEYIN_KEY2 0x1BD // Key 2 In
	#define FLAG_KEYIN_KEY3 0x1BE // Key 3 In
	#define FLAG_KEYIN_KEY4 0x1BF // Key 4 In
	#define FLAG_KEYIN_KEY5 0x1C0 // Key 5 In
	#define FLAG_KEYIN_KEY6 0x1C1 // Key 6 In
	#define FLAG_KEYIN_KEY7 0x1C2 // Key 7 In
	#define FLAG_KEYIN_KEY8 0x1C3 // Key 8 In

	// Kongs Freed
	#define FLAG_KONG_DK 0x181 // DK Free
	#define FLAG_KONG_DIDDY 0x6 // Diddy Free
	#define FLAG_KONG_LANKY 0x46 // Lanky Free
	#define FLAG_KONG_TINY 0x42 // Tiny Free
	#define FLAG_KONG_CHUNKY 0x75 // Chunky Free

	// Boss Intro Cutscenes
	#define FLAG_INTRO_ARMYDILLO1 0x68 // AD1
	#define FLAG_INTRO_DOGADON1 0x67 // Dog 1
	#define FLAG_INTRO_MADJACK 0x6A // MJ
	#define FLAG_INTRO_PUFFTOSS 0x6B // Puff
	#define FLAG_INTRO_DOGADON2 0x69 // Dog 2
	#define FLAG_INTRO_ARMYDILLO2 0x6D // AD2
	#define FLAG_INTRO_KINGKUTOUT 0x6C // KKO

	// Level Intros
	#define FLAG_INTRO_JAPES 0x1B // Japes
	#define FLAG_INTRO_AZTEC 0x5F // Aztec
	#define FLAG_INTRO_FACTORY 0x8C // Factory
	#define FLAG_INTRO_GALLEON 0xC2 // Galleon
	#define FLAG_INTRO_FUNGI 0x101 // Fungi
	#define FLAG_INTRO_CAVES 0x11A // Caves
	#define FLAG_INTRO_CASTLE 0x15D // Castle

	// Level T&S Portal Closed
	#define FLAG_PORTAL_JAPES 0x2E // Japes
	#define FLAG_PORTAL_AZTEC 0x6C // Aztec
	#define FLAG_PORTAL_FACTORY 0x98 // Factory
	#define FLAG_PORTAL_GALLEON 0xCB // Galleon
	#define FLAG_PORTAL_FUNGI 0x102 // Fungi
	#define FLAG_PORTAL_CAVES 0x12E // Caves
	#define FLAG_PORTAL_CASTLE 0x160// Castle

	#define FLAG_ARCADE_ROUND1 0x82 // Arcade R1 Beaten
	#define FLAG_RABBIT_ROUND1 0xF8 // Rabbit Race 1 Beaten

	#define FLAG_MODIFIER_PRODROOM 0x6F // Prod Room On
	#define FLAG_MODIFIER_GALLEONWATER 0xA0 // Galleon Water Raised
	#define FLAG_MODIFIER_GALLEONSHIP 0x9C // Galleon Ship
	#define FLAG_MODIFIER_FUNGINIGHT 0xCE // Fungi Time of Day
	#define FLAG_MODIFIER_KOSHADEAD 0x12C // Giant Kosha Dead
	#define FLAG_MODIFIER_HELMBOM 0x302 // Helm BoM Off

	// Training Barrel Flags
	#define FLAG_TBARREL_DIVE 0x182 // Dive
	#define FLAG_TBARREL_ORANGE 0x184 // Orange
	#define FLAG_TBARREL_BARREL 0x185 // Barrel
	#define FLAG_TBARREL_VINE 0x183 // Vine
	#define FLAG_TBARREL_COMPLETE 0x187 // Training Barrels Completed
	#define FLAG_TBARREL_SPAWNED 0x17F // Training Barrel Spawned

	#define FLAG_STORY_ARCADE 0x63 // Arcade Story
	#define FLAG_STORY_JETPAC 0x61 // Jetpac Story
	// Whatever Temp Flag 92 is
	// Map Warp Flags
#else
	// JP

	// Waterfall Cutscene
	// Escape Cutscene
	// Kong FTTs
	// Cranky Sim Slam Acquired
	// Warp Flags
	// Camera

	// Diddy Help Me Cutscene
	// Llama Cutscene
	// GK Cutscene

	// B Locker FTT
	// Bananaport FTT
	// Crown Pad FTT
	// Barrel Ability FTTs

	// Keys in Possession
	// Keys turned in
	// Japes Open

	// Kongs Freed

	// Boss Intro Cutscenes
	// Level Intros
	// Level T&S Portal Closed

	// Arcade R1 Beaten
	// Rabbit Race 1 Beaten

	// Prod Room On
	// Galleon Water Raised
	// Galleon Ship
	// Fungi Time of Day
	// Giant Kosha Dead
	// Helm BoM Off

	// Training Barrel Flags
	// Training Barrel Spawned

	// Arcade Story
	// Jetpac Story
	// Whatever Temp Flag 92 is
	// Map Warp Flags
#endif
