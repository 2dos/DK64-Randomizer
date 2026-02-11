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
	
.align 0x10
END: