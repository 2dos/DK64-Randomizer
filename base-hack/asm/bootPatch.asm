//DMA our custom code from ROM to RAM, run code we overwrote with hook, then run our custom code on boot
.definelabel bootStart, 0x02000000

.headersize 0x7FFFF400
.org 0x80000764
LUI a0, hi(bootStart) //start of ROM copy
LUI a1, hi(bootStart + 0x20000)
ADDIU a1, a1, lo(bootStart + 0x20000)
ADDIU a0, a0, lo(bootStart)
LUI a2, 0x805D
JAL dmaFileTransfer
ORI a2, a2, 0xAE00 //RAM location to copy to
J displacedBootCode
NOP