.align
// Open Crown door
OpenCrownDoor:
    SW      ra, @ReturnAddress
    LA      a0, CrownDoorOption
    LBU     a0, 0x0 (a0)
    BEQZ    a0, OpenCrownDoor_Finish
    NOP
    
    JAL     CodedSetPermFlag
    LI      a0, 0x304
    
    OpenCrownDoor_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
CrownDoorOption:
    .byte 1