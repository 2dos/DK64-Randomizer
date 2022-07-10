#define NULL 0

// N64 Buttons
#define L_Button 0x0020
#define D_Up 0x0800
#define D_Down 0x0400
#define D_Left 0x0200
#define D_Right 0x0100
#define B_Button 0x4000
#define A_Button 0x8000
#define Z_Button 0x2000
#define R_Button 0x0010
#define Start_Button 0x1000
#define C_Up 0x0008
#define C_Down 0x0004
#define C_Left 0x0002
#define C_Right 0x0001

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

#define KONG_LOCKED_START 0x2E8
#define SNOOPDOOR_OPEN 0x2ED
#define DKJAPESCAGEGB_OPEN 0x2EF
#define JAPESMOUNTAINSPAWNED 0x2F0
#define FACTORYDIDDYPRODSPAWNED 0x2F1
#define FUNGICRUSHERON 0x2F2
#define CAVESBOULDERDOME_DESTROYED 0x2F3
#define CAVESGBDOME_DESTROYED 0x2F4