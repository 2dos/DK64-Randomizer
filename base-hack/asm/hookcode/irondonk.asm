permaLossTagCheck:
    jal determineKongUnlock
    lw $a0, 0x58 ($t5)
    j 0x80682F48
    nop

permaLossTagSet:
    jal unlockKongPermaLoss
    lw $a0, 0x58 ($t9)
    j 0x80683640
    nop

permaLossTagDisplayCheck:
    jal determineKongUnlock
    or $a1, $s0, $zero
    j 0x806840e0
    nop