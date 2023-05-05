#define NULL 0

// Colors
#define SelectedRGB 0xFFD700 // CSS Gold
#define ReturnRGB 0xFF4500 // CSS OrangeRed
#define KoshaRGB_Frozen 0x008B8B // CSS DarkCyan
#define KoshaRGB_CancelRange 0xFFD700 // CSS Gold
#define KoshaRGB_Music 0xD2691E // CSS Chocolate
#define KoshaRGB_Tantrum 0x8B0000 // CSS DarkRed
#define ISGRGB_FadeoutPending 0xFF4500 // CSS OrangeRed
#define ISGRGB_Fading 0xFF0000 // CSS Red
#define AngleRGB_PhaseState 0xFF4500 // CSS OrangeRed
#define HeldObject_ObjectExists 0xFF4500 // CSS OrangeRed

// SFX Index
#define Banana 0x2A0
#define Okay 0x23C
#define UhOh 0x150
#define Bell 0x1F
#define KLumsy 0x31C
#define Wrong 0x98
#define Potion 0x214
#define AmmoPickup 0x157
#define Coin 0x1D1
#define BeepHigh 116
#define BeepLow 117
#define FeedMe 601
#define Bounce 458
#define TimerTock 143
#define ChunkyFallTooFar 197
#define Fire 234
#define MatchingSound 171
#define CameraPull 441
#define Quack 170
#define TagWarp 612
#define TakeWarp 230
#define Splat 22
#define Burp 530
#define ArcadeJump 65
#define ArcadeSpring 67
#define ArcadeFalling 68
#define ArcadeGrunt 83

// Other
#define MysteryWriteOffset 0x29C
#define CurrentCharacter 0x36C
#define MovesBaseSize 0x1D8
#define MaxMenuItems 20 // 32 (practice rom cap) - 8 (normal cap) - 4 (watch)
#define ErrorLength 180
#define WarpScreens 38
#define WatchCount 4
#define FileStatesROMStart 0x2022000
#define FileStateSize 0x340
#define flagMenuScreenCount 11
#define pointer_table_offset 0x101C50
#define static_expansion_size 0x100

#define ACTOR_VANILLA_LIMIT 345
#define COLLISION_LIMIT 60
#define DEFS_LIMIT 147
#define ACTOR_LIMIT 345 + NEWACTOR_TERMINATOR
#define CUSTOM_ACTORS_START 345

#define KONG_LOCKED_START 0x2E8
#define SNOOPDOOR_OPEN 0x2ED
#define DKJAPESCAGEGB_OPEN 0x2EF
#define JAPESMOUNTAINSPAWNED 0x2F0
#define FACTORYDIDDYPRODSPAWNED 0x2F1
#define FUNGICRUSHERON 0x2F2
#define CAVESBOULDERDOME_DESTROYED 0x2F3
#define CAVESGBDOME_DESTROYED 0x2F4
#define AZTEC_SNOOPW5 0x2F5
#define GALLEON_TOWERW4 0x2F6
#define CAVES_HIDDENW3 0x2F7
#define GALLEON_5DSOPEN_DK 0x2F8
#define GALLEON_5DSOPEN_DIDDY 0x2F9
#define GALLEON_5DSOPEN_LANKY 0x2FA
#define GALLEON_5DSOPEN_TINY 0x2FB
#define GALLEON_5DSOPEN_CHUNKY 0x2FC
#define FLAG_ABILITY_CAMERA 0x2FD // Decoupled from shockwave which uses regular flag
#define GALLEON_2DSOPEN_LANKY 0x2FE
#define GALLEON_2DSOPEN_TINY 0x2FF
#define FLAG_COLLECTABLE_BEAN 0x300
#define FLAG_PKMNSNAP_PICTURES 0x26B // 0x26B -> 0x28D (inc.) (35 flags)

#define FLAG_ITEM_SLAM_0 0x290
#define FLAG_ITEM_SLAM_1 0x291
#define FLAG_ITEM_BELT_0 0x292
#define FLAG_ITEM_BELT_1 0x293
#define FLAG_ITEM_INS_0 0x294
#define FLAG_ITEM_INS_1 0x295
#define FLAG_ITEM_INS_2 0x296
#define FLAG_SHOPMOVE_SLAM_0 0x297
#define FLAG_SHOPMOVE_SLAM_1 0x298
#define FLAG_SHOPMOVE_BELT_0 0x299
#define FLAG_SHOPMOVE_BELT_1 0x29A
#define FLAG_SHOPMOVE_INS_0 0x29B
#define FLAG_SHOPMOVE_INS_1 0x29C
#define FLAG_SHOPMOVE_INS_2 0x29D
#define FLAG_RAINBOWCOIN_0 0x29E // 0x29E -> 0x2AD (inc.) (16 flags)
#define FLAG_FAKEITEM 0x2AE // 0x2AE -> 0x2BD (inc.) (16 flags)
#define FLAG_JUNKITEM 0x320 // 0x320 -> 0x383 (inc.) (100 flags)
#define FLAG_WRINKLYVIEWED 0x384 // 0x384 -> 0x3A6 (inc.) (35 flags)
#define FLAG_KROOL_ENTERED 0x3A7 // 0x3A7 = DK, 0x3A8 = Diddy, 0x3A9 = Lanky, 0x3AA = Tiny, 0x3AB = Chunky

#define IMAGE_DPAD 187
#define IMAGE_AMMO_START 188
#define IMAGE_KONG_START 190
#define IMAGE_TRACKER 0xA1
#define LEVEL_COUNT 8
#define IGT_BITS 22
#define HELM_HURRY_BITS 16
#define STAT_BITS 16
#define LETTER_BITS 7

#define PURCHASE_MOVES 0
#define PURCHASE_SLAM 1
#define PURCHASE_GUN 2
#define PURCHASE_AMMOBELT 3
#define PURCHASE_INSTRUMENT 4
#define PURCHASE_FLAG 5
#define PURCHASE_GB 6
#define PURCHASE_NOTHING -1

// Move Bitfield Checks
#define MOVECHECK_BLAST 1
#define MOVECHECK_STRONG 2
#define MOVECHECK_GRAB 4
#define MOVECHECK_CHARGE 1
#define MOVECHECK_ROCKETBARREL 2
#define MOVECHECK_SPRING 4
#define MOVECHECK_OSTAND 1
#define MOVECHECK_BALLOON 2
#define MOVECHECK_OSPRINT 4
#define MOVECHECK_MINI 1
#define MOVECHECK_TWIRL 2
#define MOVECHECK_MONKEYPORT 4
#define MOVECHECK_HUNKY 1
#define MOVECHECK_PUNCH 2
#define MOVECHECK_GONE 4
#define MOVECHECK_HOMING 2
#define MOVECHECK_SNIPER 4
#define MOVECHECK_UPGRADE1 2
#define MOVECHECK_THIRDMELON 4
#define MOVECHECK_UPGRADE2 8