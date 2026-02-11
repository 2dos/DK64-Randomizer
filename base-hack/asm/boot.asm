.definelabel dataStart, 0x01FED020
.definelabel dataRDRAM, 0x807FF800
.definelabel musicInfo, 0x01FFF000
.definelabel itemROM, 0x01FF3000
.definelabel codeEnd, 0x805FAE00
.definelabel itemdatasize, 0x30

START:
	displacedBootCode:
		// Load Variable Space
		lui $a0, hi(dataStart)
		lui $a1, hi(dataStart + 0x200)
		addiu $a1, $a1, lo(dataStart + 0x200)
		addiu $a0, $a0, lo(dataStart)
		lui $a2, 0x807F
		jal dmaFileTransfer
		ori $a2, $a2, 0xF800 //RAM location to copy to
		
		// Load item data
		lui $a0, hi(itemROM)
		lui $a1, hi(itemROM + itemdatasize)
		addiu $a1, $a1, lo(itemROM + itemdatasize)
		addiu $a0, $a0, lo(itemROM)
		lui $a2, hi(APName)
		jal dmaFileTransfer
		addiu $a2, $a2, lo(APName)
    
		//
		lui $v0, 0x8001
		addiu $v0, $v0, 0xDCC4

		lui $t3, 0
		lui $t4, 1
		lui $t5, static_code_upper
		lui $t9, static_data_upper
		lui $t8, multi_code_upper
		j 0x80000784
		lui $t6, multi_data_upper
		//end of boot code
		/////////////////////////////////////////////////////

LobbyReplaceCode1:
	lui $t7, hi(ReplacementLobbiesArray)
	addiu $t7, $t7, lo(ReplacementLobbiesArray)
LobbyReplaceCode2:
	lui $a0, hi(ReplacementLobbiesArray)
	lhu $a0, lo(ReplacementLobbiesArray) ($a0)

loadExtraHooks:	
	lui $t3, hi(LobbyReplaceCode1)
	lw $t3, lo(LobbyReplaceCode1) ($t3)
	lui $t4, 0x8069
	sw $t3, 0xABE8 ($t4)
	lui $t3, hi(LobbyReplaceCode1)
	addiu $t3, $t3, 4
	lw $t3, lo(LobbyReplaceCode1) ($t3)
	sw $t3, 0xABEC ($t4)

	lui $t3, hi(LobbyReplaceCode2)
	lw $t3, lo(LobbyReplaceCode2) ($t3)
	lui $t4, 0x8060
	sw $t3, 0x0058 ($t4)
	lui $t3, hi(LobbyReplaceCode2)
	addiu $t3, $t3, 4
	lw $t3, lo(LobbyReplaceCode2) ($t3)
	sw $t3, 0x006C ($t4)

	jr $ra
	nop
	
.align 0x10
END: