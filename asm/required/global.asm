// MIPS ASM
[ReturnAddress]: 0x807FFFE4
[ReturnAddress2]: 0x807FFFE8
[ReturnAddress3]: 0x807FFFEC
[VarStorage0]: 0x807FFFF0
[VarStorage1]: 0x807FFFF4
[VarStorage2]: 0x807FFFF8

// Custom Variables
[BackupParentMap]: 0x807FFFDF // u8

// Normal Variables
[TransitionSpeed]: 0x807FD88C
[MovesBase]:  0x807FC950
[Gamemode]: 0x80755318
[StorySkip]: 0x8074452C
[TempFlagBlock]: 0x807FDD90
[CastleCannonPointer]: 0x807F5BE8
[ObjectTimer]: 0x8076A064
[CurrentMap]: 0x8076A0A8
[TroffNScoffReqArray]: 0x807446C0 // u16 item size
[BLockerDefaultArray]: 0x807446D0 // u16 item size
[BLockerCheatArray]: 0x807446E0 // u16 item size, [u8 - GB, u8 - Kong]
[CheckmarkKeyArray]: 0x80744710 // u16 item size
[ControllerInput]: 0x80014DC4
[NewlyPressedControllerInput]: 0x807ECD66
[CutsceneIndex]: 0x807476F4
[CutsceneActive]: 0x807444EC
[CutsceneTimer]: 0x807476F0
[CutsceneType]: 0x807476FC
[ParentMap]: 0x8076A172
[ActorSpawnerArrayPointer]: 0x807FDC8C
[DestinationMap]: 0x807444E4
[DestinationExit]: 0x807444E8
[LevelIndexMapping]: 0x807445E0
[Health]: 0x807FCC4B // u8
[Melons]: 0x807FCC4C // u8
[AmmoStandard]: 0x807FCC40 // u16
[AmmoHoming]: 0x807FCC42 // u16
[Oranges]: 0x807FCC44 // u16
[Crystals]: 0x807FCC46 // u16
[Film]: 0x807FCC48 // u16
[IsAutowalking]: 0x807463B8
[HUDPointer]: 0x80754280
[LoadedActorArray]: 0x807FB930
[LoadedActorCount]: 0x807FBB34 // u16

// New Variables
[TestVariable]: 0x807FFFFC

// Model Two
[ModelTwoArray]: 0x807F6000
[ModelTwoArraySize]: 0x807F6004

// Functions
[SetFlag]: 0x8073129C
[CheckFlag]: 0x8073110C
[DMAFileTransfer]: 0x80000450

// Loading Zones
[LZArray]: 0x807FDCB4 // u32
[LZSize]: 0x807FDCB0 // u16

// Pointers
[Player]: 0x807FBB4C
[SwapObject]: 0x807FC924
[Character]: 0x8074E77C

// Buttons
[L_Button]: 0x0020
[D_Up]: 0x0800
[D_Down]: 0x0400
[D_Left]: 0x0200
[D_Right]: 0x0100
[B_Button]: 0x4000
[A_Button]: 0x8000
[Z_Button]: 0x2000
[R_Button]: 0x0010
[Start_Button]: 0x1000

.org 0x805FC164 // retroben's hook but up a few functions
J Start

.org 0x8000072C // Boot
J   LoadInAdditionalFile
NOP
.org 0x805DAE00
