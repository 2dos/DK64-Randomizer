permaLossTagCheck:
    JAL 		determineKongUnlock
    LW 			a0, 0x58 (t5)
    J 			0x80682F48
    NOP

permaLossTagSet:
    JAL	 		unlockKongPermaLoss
    LW 			a0, 0x58 (t9)
    J 			0x80683640
    NOP

permaLossTagDisplayCheck:
    JAL 		determineKongUnlock
    OR 			a1, s0, r0
    J 			0x806840e0
    NOP