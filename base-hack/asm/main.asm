.n64 // Let armips know we're coding for the N64 architecture
.open "rom/dk64-randomizer-base.z64", "rom/dk64-randomizer-base-dev.z64", 0 // Open the ROM file
.include "asm/symbols.asm" // Include dk64.asm to tell armips' linker where to find the game's function(s)
.orga 0x3154 ; ROM
.org 0x80002554 ; RDRAM
NOP ; CRC Patch
.include "asm/bootPatch.asm" //patch boot routine to DMA our code from ROM
.include "asm/header.asm"
.include "asm/boot.asm" //include modified boot code
.include "asm/hookcode.asm" // Hook code
.include "asm/objects.asm"
.close // Close the ROM file