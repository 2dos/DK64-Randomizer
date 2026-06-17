.n64 // Let armips know we're coding for the N64 architecture
.open "minigame/dummy.bin", "minigame/hexagon.bin", 0 // Open the ROM file
.include "asm/symbols.asm" // Include dk64.asm to tell armips' linker where to find the game's function(s)
.headersize 0x80024390
.org 0x80024390
.include "asm/hookcode/displayImageCustom.asm"
.include "asm/minigames/hexagon/objects.asm"
.close // Close the ROM file
