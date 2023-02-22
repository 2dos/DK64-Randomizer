.definelabel dataStart, 0x01FED020
.definelabel dataRDRAM, 0x807FF800
.definelabel musicInfo, 0x01FFF000
.definelabel itemROM, 0x01FF2000
.definelabel codeEnd, 0x805FAE00
.definelabel itemdatasize, 0x640

START:
	displacedBootCode:
		// Load Variable Space
		LUI a0, hi(dataStart)
		LUI a1, hi(dataStart + 0x200)
		ADDIU a1, a1, lo(dataStart + 0x200)
		ADDIU a0, a0, lo(dataStart)
		LUI a2, 0x807F
		JAL dmaFileTransfer
		ORI a2, a2, 0xF800 //RAM location to copy to
		// Boot image
		// LUI a0, 0x8060
		// JAL 0x805FB7E4 // Render Nintendo Logo
		// SW r0, 0xBBCC (a0)
		// Load item data
		LUI a0, hi(itemROM)
		LUI a1, hi(itemROM + itemdatasize)
		ADDIU a1, a1, lo(itemROM + itemdatasize)
		ADDIU a0, a0, lo(itemROM)
		LUI a2, hi(codeEnd - itemdatasize)
		JAL dmaFileTransfer
		ADDIU a2, a2, lo(codeEnd - itemdatasize)
		//
		LUI v0, 0x8001
		ADDIU v0, v0, 0xDCC4
		// Bypass Setup Checks
		//LUI t3, 0x8075
		//ADDIU t4, r0, 1
		//SB t4, 0x00B0 (t3)
		//LUI t3, 0x8074
		//SB t4, 0x7D78 (t3)
		// Write LZ Update
		LUI t3, 0x8075
		SB r0, 0x8E21 (t3) // Setup
		SB r0, 0x8E22 (t3) // M2 Scripts
		SB r0, 0x8E24 (t3) // Text
		SB r0, 0x8E2A (t3) // Loading Zones
		SB r0, 0x8E28 (t3) // Character Spawners

		LUI t3, 0x2407
		ADDIU t3, t3, 1
		LUI t4, 0x8073
		SW t3, 0xE76C (t4)
		//write per frame hook
		//
		LUI t3, hi(mainASMFunctionJump)
		LW t3, lo(mainASMFunctionJump) (t3)
		LUI t4, 0x8060
		SW t3, 0xC164 (t4) //store per frame hook
		// Write Init Hook
		LUI t3, hi(initHook)
		LW t3, lo(initHook) (t3)
		LUI t4, 0x8060
		SW t3, 0xBDEC (t4) // Store Hook
		SW r0, 0xBDF0 (t4) // Store NOP

		LUI t3, 0
		LUI t4, 1
		LUI t5, 1
		LUI t9, 0xD
		LUI t8, 0xD
		J 0x80000784
		LUI t6, 0x000D
		//end of boot code
		/////////////////////////////////////////////////////

mainASMFunction:
	JAL	0x805FC2B0
	NOP
	JAL cFuncLoop
	NOP
	NOP
	J 0x805FC16C
	NOP

mainASMFunctionJump:
	J mainASMFunction //instruction copied and used as a hook
	NOP

mainASMFunctionVanilla:
	JAL	0x805FC2B0
	NOP

NinWarpHook:
	J 	NinWarpCode
	NOP
InstanceScriptHook:
	J 	InstanceScriptCheck
	NOP
SaveToFileFixesHook:
	J 	SaveToFileFixes
	NOP
BarrelMovesFixesHook:
	J 	BarrelMovesFixes
	NOP
ChimpyChargeFixHook:
	J 	ChimpyChargeFix
	NOP
OStandFixHook:
	J 	OStandFix
	NOP
HunkyChunkyFix2Hook:
	J 	HunkyChunkyFix2
	NOP
EarlyFrameHook:
	J 	EarlyFrameCode
	NOP
DisplayListHook:
	J 	displayListCode
	NOP
LobbyExitHook:
	J 	getLobbyExit
	NOP
LobbyReplaceCode1:
	LUI t7, hi(ReplacementLobbiesArray)
	ADDIU t7, t7, lo(ReplacementLobbiesArray)

LobbyReplaceCode2:
	LUI a0, hi(ReplacementLobbiesArray)
	LHU a0, lo(ReplacementLobbiesArray) (a0)
damageMultiplerHook:
	J 	damageMultiplerCode
	NOP
PauseExtraSlotHook:
	J 	PauseExtraSlotCode
	NOP
PauseExtraHeightHook:
	J 	PauseExtraHeight
	NOP
PauseExtraSlotClamp0Hook:
	J 	PauseExtraSlotClamp0
	NOP
PauseExtraSlotClamp1Hook:
	J 	PauseExtraSlotClamp1
	NOP
PauseExtraSlotCustomHook:
	J 	PauseExtraSlotCustomCode
	NOP
AutowalkFixHook:
	J 	AutowalkFix
	NOP
LoadCodeReplacements:
	J 	DynamicCodeFixes
	NOP
TagPermaLossCheckHook:
	J 	permaLossTagCheck
	NOP
TagPermaLossSetHook:
	J 	permaLossTagSet
	NOP
TagPermaLossDisplayHook:
	J 	permaLossTagDisplayCheck
	NOP
TagPreventHook:
	J 	tagPreventCode
	NOP
BonusAutocompleteHook:
	J 	destroyAllBarrelsCode
	NOP
initHook:
	J 	initCode
	NOP
KeyCompressionHook:
	J 	KeyCompressionCode
	NOP
HUDDisplayHook:
	J 	HUDDisplayCode
	NOP
HomingDisableHook:
	J 	HomingDisable
	NOP
HomingHUDHandleHook:
	J 	HomingHUDHandle
	NOP
DKCollectableFixHook:
	J 	DKCollectableFix
	NOP
CannonForceHook:
	J 	CannonForceCode
	NOP
GuardAutoclearHook:
	J 	GuardAutoclear
	NOP
TextHandlerHook:
	J 	TextHandler
	NOP
GuardDeathHandleHook:
	J 	GuardDeathHandle
	NOP
ShopImageHandlerHook:
	J 	ShopImageHandler
	NOP
FixPufftossInvalidWallCollisionHook:
	J 	FixPufftossInvalidWallCollision
	NOP
GiveItemPointerToMultiHook:
	J 	GiveItemPointerToMulti
	NOP
CoinHUDRepositionHook:
	J 	CoinHUDReposition
	NOP
SaveHelmHurryCheckHook:
	J 	SaveHelmHurryCheck
	NOP
InvertCameraControlsHook:
	J 	InvertCameraControls
	NOP
VineCodeHook:
	J 	VineCode
	NOP
VineShowHook:
	J 	VineShowCode
	NOP
SkipCutscenePansHook:
	J 	SkipCutscenePans
	NOP
ModifyCameraColorHook:
	J 	ModifyCameraColor
	NOP

PlayCutsceneVelocityHook:
	J 	PlayCutsceneVelocity
	NOP
ItemRandoFlagCheckHook:
	J 	checkFlag_ItemRando
	NOP
ItemRandoFlagSetHook:
	J 	setFlag_ItemRando
	NOP
ObjectRotateHook:
	J 	ObjectRotate
	NOP
SpriteFixHook:
	J 	SpriteFix
	NOP
PauseCounterCapHook:
	J 	PauseCounterCap
	NOP
PauseControlHook:
	J 	PauseControl_Control
	NOP
PauseSpriteHook:
	J 	PauseControl_Sprite
	NOP
HandleSlamCheckHook:
	J 	HandleSlamCheck
	NOP

loadExtraHooks:
	LUI t3, hi(InstanceScriptHook)
	LW t3, lo(InstanceScriptHook) (t3)
	LUI t4, 0x8064
	SW t3, 0xEE08 (t4) // Store Hook
	SW r0, 0xEE0C (t4) // Store NOP
	
	LUI t3, hi(ItemRandoFlagCheckHook)
	LW t3, lo(ItemRandoFlagCheckHook) (t3)
	LUI t4, 0x8073
	SW t3, 0x1168 (t4) // Store Hook
	SW r0, 0x116C (t4) // Store NOP
	
	LUI t3, hi(ItemRandoFlagSetHook)
	LW t3, lo(ItemRandoFlagSetHook) (t3)
	LUI t4, 0x8073
	SW t3, 0x12F8 (t4) // Store Hook
	SW r0, 0x12FC (t4) // Store NOP
	
	LUI t3, hi(VineCodeHook)
	LW t3, lo(VineCodeHook) (t3)
	LUI t4, 0x806A
	SW t3, 0x840C (t4) // Store Hook
	SW r0, 0x8410 (t4) // Store NOP
	
	LUI t3, hi(VineShowHook)
	LW t3, lo(VineShowHook) (t3)
	LUI t4, 0x806A
	SW t3, 0x8420 (t4) // Store Hook
	SW r0, 0x8424 (t4) // Store NOP
	
	LUI t3, hi(HandleSlamCheckHook)
	LW t3, lo(HandleSlamCheckHook) (t3)
	LUI t4, 0x8064
	SW t3, 0xED7C (t4) // Store Hook
	SW r0, 0xED80 (t4) // Store NOP
	
	LUI t3, hi(ModifyCameraColorHook)
	LW t3, lo(ModifyCameraColorHook) (t3)
	LUI t4, 0x8070
	SW t3, 0xF384 (t4) // Store Hook
	SW r0, 0xF388 (t4) // Store NOP
	
	LUI t3, hi(SkipCutscenePansHook)
	LW t3, lo(SkipCutscenePansHook) (t3)
	LUI t4, 0x8062
	SW t3, 0xE684 (t4) // Store Hook
	SW r0, 0xE688 (t4) // Store NOP

	LUI t3, hi(ShopImageHandlerHook)
	LW t3, lo(ShopImageHandlerHook) (t3)
	LUI t4, 0x8065
	SW t3, 0x8364 (t4) // Store Hook
	SW r0, 0x8368 (t4) // Store NOP
	
	LUI t3, hi(InvertCameraControlsHook)
	LW t3, lo(InvertCameraControlsHook) (t3)
	LUI t4, 0x806F
	SW t3, 0xA70C (t4) // Store Hook
	SW r0, 0xA710 (t4) // Store NOP
	
	LUI t3, hi(PlayCutsceneVelocityHook)
	LW t3, lo(PlayCutsceneVelocityHook) (t3)
	LUI t4, 0x8062
	SW t3, 0xCE38 (t4) // Store Hook
	SW r0, 0xCE3C (t4) // Store NOP

	LUI t3, hi(FixPufftossInvalidWallCollisionHook)
	LW t3, lo(FixPufftossInvalidWallCollisionHook) (t3)
	LUI t4, 0x8067
	SW t3, 0x7C14 (t4) // Store Hook
	SW r0, 0x7C18 (t4) // Store NOP

	LUI t3, hi(SaveToFileFixesHook)
	LW t3, lo(SaveToFileFixesHook) (t3)
	LUI t4, 0x8061
	SW t3, 0xDFF4 (t4) // Store Hook
	SW r0, 0xDFF8 (t4) // Store NOP

	LUI t3, hi(BarrelMovesFixesHook)
	LW t3, lo(BarrelMovesFixesHook) (t3)
	LUI t4, 0x806F
	SW t3, 0x6EA0 (t4) // Store Hook
	SW r0, 0x6EA4 (t4) // Store NOP

	LUI t3, hi(ChimpyChargeFixHook)
	LW t3, lo(ChimpyChargeFixHook) (t3)
	LUI t4, 0x806E
	SW t3, 0x4930 (t4) // Store Hook
	SW r0, 0x4934 (t4) // Store NOP

	LUI t3, hi(OStandFixHook)
	LW t3, lo(OStandFixHook) (t3)
	LUI t4, 0x806E
	SW t3, 0x48AC (t4) // Store Hook
	SW r0, 0x48B0 (t4) // Store NOP

	LUI t3, hi(HunkyChunkyFix2Hook)
	LW t3, lo(HunkyChunkyFix2Hook) (t3)
	LUI t4, 0x8068
	SW t3, 0xECB8 (t4) // Store Hook
	SW r0, 0xECBC (t4) // Store NOP

	LUI t3, hi(EarlyFrameHook)
	LW t3, lo(EarlyFrameHook) (t3)
	LUI t4, 0x8060
	SW t3, 0xC3FC (t4) // Store Hook
	SW r0, 0xC400 (t4) // Store NOP

	LUI t3, hi(DisplayListHook)
	LW t3, lo(DisplayListHook) (t3)
	LUI t4, 0x8071
	SW t3, 0x417C (t4) // Store Hook
	SW r0, 0x4180 (t4) // Store NOP

	LUI t3, hi(GiveItemPointerToMultiHook)
	LW t3, lo(GiveItemPointerToMultiHook) (t3)
	LUI t4, 0x8070
	SW t3, 0x8610 (t4) // Store Hook
	SW r0, 0x8614 (t4) // Store NOP
	
	LUI t3, hi(CoinHUDRepositionHook)
	LW t3, lo(CoinHUDRepositionHook) (t3)
	LUI t4, 0x8070
	SW t3, 0x88C8 (t4) // Store Hook
	SW r0, 0x88CC (t4) // Store NOP

	LUI t3, hi(LobbyExitHook)
	LW t3, lo(LobbyExitHook) (t3)
	LUI t4, 0x8060
	SW t3, 0x005C (t4) // Store Hook
	SW r0, 0x0060 (t4) // Store NOP

	LUI t3, hi(LobbyReplaceCode1)
	LW t3, lo(LobbyReplaceCode1) (t3)
	LUI t4, 0x8069
	SW t3, 0xABE8 (t4)
	LUI t3, hi(LobbyReplaceCode1)
	ADDIU t3, t3, 4
	LW t3, lo(LobbyReplaceCode1) (t3)
	SW t3, 0xABEC (t4)

	LUI t3, hi(LobbyReplaceCode2)
	LW t3, lo(LobbyReplaceCode2) (t3)
	LUI t4, 0x8060
	SW t3, 0x0058 (t4)
	LUI t3, hi(LobbyReplaceCode2)
	ADDIU t3, t3, 4
	LW t3, lo(LobbyReplaceCode2) (t3)
	SW t3, 0x006C (t4)

	LUI t3, hi(damageMultiplerHook)
	LW t3, lo(damageMultiplerHook) (t3)
	LUI t4, 0x806D
	SW t3, 0x9A7C (t4) // Store Hook
	SW r0, 0x9A80 (t4) // Store NOP
	
	LUI t3, hi(SaveHelmHurryCheckHook)
	LW t3, lo(SaveHelmHurryCheckHook) (t3)
	LUI t4, 0x8061
	SW t3, 0xDEF4 (t4) // Store Hook
	SW r0, 0xDEF8 (t4) // Store NOP

	LUI t3, hi(WarpToIslesEnabled)
	LBU t3, lo(WarpToIslesEnabled) (t3)
	BEQZ t3, loadExtraHooks_0
	NOP

	LUI t3, hi(PauseExtraSlotHook)
	LW t3, lo(PauseExtraSlotHook) (t3)
	LUI t4, 0x806B
	SW t3, 0x995C (t4) // Store Hook
	SW r0, 0x9960 (t4) // Store NOP

	LUI t3, hi(PauseExtraHeightHook)
	LW t3, lo(PauseExtraHeightHook) (t3)
	LUI t4, 0x806B
	SW t3, 0x9818 (t4) // Store Hook
	SW r0, 0x981C (t4) // Store NOP

	LUI t3, hi(PauseExtraSlotClamp0Hook)
	LW t3, lo(PauseExtraSlotClamp0Hook) (t3)
	LUI t4, 0x806B
	SW t3, 0x87BC (t4) // Store Hook
	SW r0, 0x87C0 (t4) // Store NOP

	LUI t3, hi(PauseExtraSlotClamp1Hook)
	LW t3, lo(PauseExtraSlotClamp1Hook) (t3)
	LUI t4, 0x806B
	SW t3, 0x8760 (t4) // Store Hook
	SW r0, 0x8764 (t4) // Store NOP

	LUI t3, hi(PauseExtraSlotCustomHook)
	LW t3, lo(PauseExtraSlotCustomHook) (t3)
	LUI t4, 0x806B
	SW t3, 0x8804 (t4) // Store Hook
	SW r0, 0x8808 (t4) // Store NOP
	
	LUI t3, hi(PauseCounterCapHook)
	LW t3, lo(PauseCounterCapHook) (t3)
	LUI t4, 0x806B
	SW t3, 0x9898 (t4) // Store Hook
	SW r0, 0x989C (t4) // Store NOP

	loadExtraHooks_0:
	LUI t3, hi(AutowalkFixHook)
	LW t3, lo(AutowalkFixHook) (t3)
	LUI t4, 0x806F
	SW t3, 0x3E74 (t4) // Store Hook
	SW r0, 0x3E78 (t4) // Store NOP

	LUI t3, hi(LoadCodeReplacements)
	LW t3, lo(LoadCodeReplacements) (t3)
	LUI t4, 0x8061
	SW t3, 0x0948 (t4) // Store Hook
	SW r0, 0x094C (t4) // Store NOP

	LUI t3, hi(permaLossMode)
	LBU t3, lo(permaLossMode) (t3)
	BEQZ t3, loadExtraHooks_1
	NOP

	LUI t3, hi(TagPermaLossCheckHook)
	LW t3, lo(TagPermaLossCheckHook) (t3)
	LUI t4, 0x8068
	SW t3, 0x2F2C (t4) // Store Hook
	SW r0, 0x2F30 (t4) // Store NOP

	LUI t3, hi(TagPermaLossSetHook)
	LW t3, lo(TagPermaLossSetHook) (t3)
	LUI t4, 0x8068
	SW t3, 0x3620 (t4) // Store Hook
	SW r0, 0x3624 (t4) // Store NOP

	LUI t3, hi(TagPermaLossDisplayHook)
	LW t3, lo(TagPermaLossDisplayHook) (t3)
	LUI t4, 0x8068
	SW t3, 0x40C4 (t4) // Store Hook
	SW r0, 0x40C8 (t4) // Store NOP

	loadExtraHooks_1:
	LUI t3, hi(TagPreventHook)
	LW t3, lo(TagPreventHook) (t3)
	LUI t4, 0x8069
	SW t3, 0x9534 (t4) // Store Hook
	SW r0, 0x9538 (t4) // Store NOP

	LUI t3, hi(bonusAutocomplete)
	LBU t3, lo(bonusAutocomplete) (t3)
	BEQZ t3, loadExtraHooks_2
	NOP

	//LUI t3, hi(BonusAutocompleteHook)
	//LW t3, lo(BonusAutocompleteHook) (t3)
	//LUI t4, 0x8068
	//SW t3, 0x0D10 (t4) // Store Hook
	//SW r0, 0x0D14 (t4) // Store NOP

	loadExtraHooks_2:
	LUI t3, hi(KeyCompressionHook)
	LW t3, lo(KeyCompressionHook) (t3)
	LUI t4, 0x806C
	SW t3, 0xD328 (t4) // Store Hook
	SW r0, 0xD32C (t4) // Store NOP

	LUI t3, hi(CannonForceHook)
	LW t3, lo(CannonForceHook) (t3)
	LUI t4, 0x8068
	SW t3, 0xB684 (t4) // Store Hook
	SW r0, 0xB688 (t4) // Store NOP

	LUI t3, hi(HUDDisplayHook)
	LW t3, lo(HUDDisplayHook) (t3)
	LUI t4, 0x8070
	SW t3, 0x9F88 (t4) // Store Hook
	SW r0, 0x9F8C (t4) // Store NOP

	LUI t3, hi(HomingDisableHook)
	LW t3, lo(HomingDisableHook) (t3)
	LUI t4, 0x806E
	SW t3, 0x22B0 (t4) // Store Hook
	SW r0, 0x22B4 (t4) // Store NOP

	LUI t3, hi(HomingHUDHandleHook)
	LW t3, lo(HomingHUDHandleHook) (t3)
	LUI t4, 0x806F
	SW t3, 0xB574 (t4) // Store Hook
	SW r0, 0xB578 (t4) // Store NOP

	LUI t3, hi(DKCollectableFixHook)
	LW t3, lo(DKCollectableFixHook) (t3)
	LUI t4, 0x8063
	SW t3, 0x24C4 (t4) // Store Hook
	SW r0, 0x24C8 (t4) // Store NOP

	LUI t3, hi(GuardDeathHandleHook)
	LW t3, lo(GuardDeathHandleHook) (t3)
	LUI t4, 0x806B
	SW t3, 0xF70C (t4) // Store Hook
	SW r0, 0xF710 (t4) // Store NOP
	
	LUI t3, hi(NinWarpHook)
	LW t3, lo(NinWarpHook) (t3)
	LUI t4, 0x8071
	SW t3, 0x32BC (t4) // Store Hook
	SW r0, 0x32C0 (t4) // Store NOP

	LUI t3, hi(TextHoldOn)
	LBU t3, lo(TextHoldOn) (t3)
	BEQZ t3, loadExtraHooks_3
	NOP

	LUI t3, hi(TextHandlerHook)
	LW t3, lo(TextHandlerHook) (t3)
	LUI t4, 0x8071
	SW t3, 0xE83C (t4) // Store Hook
	SW r0, 0xE840 (t4) // Store NOP

	loadExtraHooks_3:
	LUI t3, hi(GuardAutoclearHook)
	LW t3, lo(GuardAutoclearHook) (t3)
	LUI t4, 0x806B
	SW t3, 0xE55C (t4) // Store Hook
	SW r0, 0xE560 (t4) // Store NOP

	LUI t3, hi(ItemRandoOn)
	LBU t3, lo(ItemRandoOn) (t3)
	BEQZ t3, loadExtraHooks_4
	NOP

	LUI t3, hi(ObjectRotateHook)
	LW t3, lo(ObjectRotateHook) (t3)
	LUI t4, 0x8063
	SW t3, 0x7148 (t4) // Store Hook
	SW r0, 0x714C (t4) // Store NOP
	
	LUI t3, hi(SpriteFixHook)
	LW t3, lo(SpriteFixHook) (t3)
	LUI t4, 0x806A
	SW t3, 0x6708 (t4) // Store Hook
	SW r0, 0x670C (t4) // Store NOP
	
	LUI t3, hi(PauseControlHook)
	LW t3, lo(PauseControlHook) (t3)
	LUI t4, 0x806B
	SW t3, 0x86FC (t4) // Store Hook
	SW r0, 0x8700 (t4) // Store NOP
	
	LUI t3, hi(PauseSpriteHook)
	LW t3, lo(PauseSpriteHook) (t3)
	LUI t4, 0x806B
	SW t3, 0xA414 (t4) // Store Hook
	SW r0, 0xA418 (t4) // Store NOP

	loadExtraHooks_4:
	JR ra
	NOP

getObjectArrayAddr:
	// a0 = initial address
	// a1 = common object size
	// a2 = index
	MULTU 	a1, a2
	MFLO	a1
	JR 		ra
	ADD 	v0, a0, a1
	
.align 0x10
END: