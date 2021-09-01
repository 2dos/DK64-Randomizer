.align
// Unlock All Moves
GiveMoves:
    SW      ra, @ReturnAddress
    LA      a0, UnlockAllMoves
    LBU     a0, 0x0 (a0)
    BEQZ    a0, GiveMoves_Finish
    NOP
    // Melons & Health
    LI      a0, 3
    SB      a0, @Melons
    LI      a0, 12
    SB      a0, @Health
    // Collectable counts
    LI      a0, 100
    SH      a0, @AmmoStandard
    LI      a0, 15
    SH      a0, @Oranges
    LI      a0, 1500 // Crystal = 150 * amount
    SH      a0, @Crystals
    LI      a0, 5
    SH      a0, @Film
    LA      a0, TrainingBarrelFlags
    JAL     SetAllFlags
    NOP
    LI      a0, 4
    LI      a1, @MovesBase
    WriteMoves:
        LI      t3, 0x0303
        SH      t3, 0x0 (a1) // Special | Slam Level
        LA      t3, SniperValue
        LBU     t3, 0x0 (t3)
        SB      t3, 0x2 (a1) // Gun Bitfield
        LI      t3, 0x2
        SB      t3, 0x3 (a1) // Ammo belt
        LI      t3, 15
        SB      t3, 0x4 (a1) // Instrument
        LI      t3, 12
        SH      t3, 0x8 (a1) // Instrument Energy
        BEQZ    a0, WriteMoveFlags
        ADDI    a0, a0, -1 // Decrement Value for next kong
        B       WriteMoves
        ADDIU   a1, a1, 0x5E // Next kong base
    
    WriteMoveFlags:
        JAL     CodedSetPermFlag
        LI      a0, 0x179 // BFI Camera

    GiveMoves_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
UnlockAllMoves:
    .byte 1

.align
SniperValue:
    .byte 0x3