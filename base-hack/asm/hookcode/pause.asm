PauseExtraHeight:
    LUI 	s1, hi(InitialPauseHeight)
    LHU 	s1, lo(InitialPauseHeight) (s1)
    J 		0x806A9820
    ADDIU 	s0, s0, 0x5CC

PauseExtraSlotCode:
    LUI 	t9, hi(InitialPauseHeight)
    LHU 	t9, lo(InitialPauseHeight) (t9)
    ADDIU 	t9, t9, 0xCC
    BNE 	s1, t9, PauseExtraSlotCode_Normal
    NOP
    LUI 	t9, hi(ExpandPauseMenu)
    LBU 	t9, lo(ExpandPauseMenu) (t9)
    BEQZ  	t9, PauseExtraSlotCode_Skip
    SRA 	t4, a2, 0x10
    SLL 	t6, t7, 2
    LUI 	t9, hi(PauseSlot3TextPointer)
    J 		0x806A996C
    ADDIU 	t8, t9, lo(PauseSlot3TextPointer)

    PauseExtraSlotCode_Skip:
        J 		0x806A9980
        NOP

    PauseExtraSlotCode_Normal:
        LW 		t9, 0x0 (s6)
        J 		0x806A9964
        SRA 	t4, a2, 0x10

PauseExtraSlotClamp0:
    LUI 	a2, 0x427C
    LUI 	t4, hi(ExpandPauseMenu)
    LBU 	t4, lo(ExpandPauseMenu) (t4)
    J 		0x806A87C4
    ADDIU 	t4, t4, 2

PauseExtraSlotClamp1:
    LUI 	a3, 0x3F80
    LUI 	at, hi(ExpandPauseMenu)
    LBU 	at, lo(ExpandPauseMenu) (at)
    SUBU 	at, t8, at
    J 		0x806A8768
    SLTI 	at, at, 0x3

PauseExtraSlotCustomCode:
    LB 		v0, 0x17 (s0) // Load Slot Position
    ADDIU 	at, r0, 3
    BNE 	at, v0, PauseExtraSlotCustomCode_Finish
    NOP
    JAL 	warpToIsles // Init Map Change
    NOP
    JAL 	resetMapContainer
    NOP
    J 		0x806A8A20
    ADDIU 	at, r0, 2
    
    PauseExtraSlotCustomCode_Finish:
        J 		0x806A880C
        ADDIU 	at, r0, 2