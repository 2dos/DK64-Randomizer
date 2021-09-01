.org 0x8000DE88 // 0x00DE88 > 0x00EDDA. EDD1 seems the safe limit before overwriting data.

Start:
    // Run the code we replaced
    JAL     0x805FC2B0
    NOP
    LW      a0, @CurrentMap
    LI      a1, 0x50 // Main Menu
    BNE     a0, a1, Finish
    NOP
    LBU     a0, @CutsceneActive
    LI      a1, 6
    BNE     a0, a1, Finish
    NOP
    LI      a0, 0x346 // CB far OoB in Japes
    JAL     @CheckFlag
    LI      a1, 0
    ADDIU   a0, v0, 0
    BNEZ    a0, Finish // Flag is set, moves given
    NOP
    LI      a0, 0x346
    LI      a1, 1
    JAL     @SetFlag
    LI      a2, 0
    JAL     ApplyFastStart
    NOP

    Finish:
        J       0x805FC15C // retroben's hook but up a few functions
        NOP

