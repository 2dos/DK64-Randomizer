.align
// Open Rareware + Nintendo Coin door (Give both coins)
OpenCoinDoor:
    SW      ra, @ReturnAddress
    LA      a0, CoinDoorOption
    LBU     a0, 0x0 (a0)
    BEQZ    a0, OpenCoinDoor_Finish
    NOP
    JAL     CodedSetPermFlag
    LI      a0, 0x84
    JAL     CodedSetPermFlag
    LI      a0, 0x17B
    JAL     CodedSetPermFlag
    LI      a0, 0x303

    OpenCoinDoor_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
CoinDoorOption:
    .byte 1