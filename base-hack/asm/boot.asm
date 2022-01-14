.definelabel dataStart, 0x01FED020
.definelabel dataRDRAM, 0x807FF800

START:
	displacedBootCode:
		// Load Variable Space
		LUI a0, hi(dataStart)
		LUI a1, hi(dataStart + 0x100)
		ADDIU a1, a1, lo(dataStart + 0x100)
		ADDIU a0, a0, lo(dataStart)
		LUI a2, 0x807F
		JAL dmaFileTransfer
		ORI a2, a2, 0xF800 //RAM location to copy to
		//
		LUI v0, 0x8001
		ADDIU v0, v0, 0xDCC4
		// Write LZ Update
		//LUI t3, 0x2406
		//ADDIU t3, t3, 1
		//LUI t4, 0x8073
		//SW t3, 0xE764 (t4)

		LUI t3, 0x8075
		SB r0, 0x8E2A (t3)

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

loadExtraHooks:
	LUI t3, hi(NinWarpHook)
	LW t3, lo(NinWarpHook) (t3)
	LUI t4, 0x8071
	SW t3, 0x32BC (t4) // Store Hook
	SW r0, 0x32C0 (t4) // Store NOP

	LUI t3, hi(InstanceScriptHook)
	LW t3, lo(InstanceScriptHook) (t3)
	LUI t4, 0x8064
	SW t3, 0xEE08 (t4) // Store Hook
	SW r0, 0xEE0C (t4) // Store NOP

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