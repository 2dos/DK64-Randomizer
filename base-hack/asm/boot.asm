.definelabel dataStart, 0x01FED020
.definelabel dataRDRAM, 0x807FF800
.definelabel musicInfo, 0x01FFF000
.definelabel itemROM, 0x01FF2000
.definelabel codeEnd, 0x805FAE00
.definelabel itemdatasize, 0xD00

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
		LUI a2, hi(ItemRando_FLUT)
		JAL dmaFileTransfer
		ADDIU a2, a2, lo(ItemRando_FLUT)
    
		//
		LUI v0, 0x8001
		ADDIU v0, v0, 0xDCC4

		LUI t3, 0x2407
		ADDIU t3, t3, 1
		LUI t4, 0x8073
		SW t3, 0xE76C (t4)

		// Write Init Hook
		LUI t3, hi(initHook)
		LW t3, lo(initHook) (t3)
		LUI t4, 0x8060
		SW t3, 0xBDEC (t4) // Store Hook
		SW r0, 0xBDF0 (t4) // Store NOP

		LUI t3, 0
		LUI t4, 1
		LUI t5, static_code_upper
		LUI t9, static_data_upper
		LUI t8, multi_code_upper
		J 0x80000784
		LUI t6, multi_data_upper
		//end of boot code
		/////////////////////////////////////////////////////

LobbyReplaceCode1:
	LUI t7, hi(ReplacementLobbiesArray)
	ADDIU t7, t7, lo(ReplacementLobbiesArray)
LobbyReplaceCode2:
	LUI a0, hi(ReplacementLobbiesArray)
	LHU a0, lo(ReplacementLobbiesArray) (a0)
initHook:
	J 	initCode
	NOP

loadExtraHooks:	
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

getFloatUpper:
	; f12 = Float Value
	mfc1 	$v0, $f12
	sra 	$v0, $v0, 16
	JR 		ra
	andi 	$v0, $v0, 0xFFFF

callFunc:
	addi $sp, $sp, -8
	sw $ra, 0x4 ($sp)
	jalr $a0
	nop
	lw $ra, 0x4 ($sp)
	jr $ra
	addiu $sp, $sp, 8

	
.align 0x10
END: