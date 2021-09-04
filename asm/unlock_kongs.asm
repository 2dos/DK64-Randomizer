.align
// Unlock All Kongs
UnlockKongs:
    SW      ra, @ReturnAddress
    LA      a0, KongFlags
    JAL     SetAllFlags
    NOP
    LW      ra, @ReturnAddress
    JR      ra
    NOP

.align
KongFlags:
    .half 385
    .half 6
    .half 70
    .half 66
    .half 117
    .half 0