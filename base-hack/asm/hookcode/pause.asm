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

PauseCounterCap:
    ANDI    t4, s4, 0xFF
    ADDIU   t8, r0, 4
    BNE     t8, s3, PauseCounterCap_Finish
    NOP
    ADDIU   s3, r0, 3

    PauseCounterCap_Finish:
        J       0x806A98A0
        OR      t8, t6, s2

PauseControl_Control:
    // 806A86FC
    BEQ     a1, at, PauseControl_Control_Finish
    LUI     t8, 0x8080
    ADDIU   at, r0, 4
    BEQ     a1, at, PauseControl_Control_Finish
    NOP
    J       0x806A8704
    NOP

    PauseControl_Control_Finish:
        J       0x806A8D08
        NOP

PauseControl_Sprite:
    // 806AA414
    BEQ     v0, at, PauseControl_Sprite_Finish
    OR      s0, r0, r0
    ADDIU   at, r0, 4
    BEQ     v0, at, PauseControl_Sprite_Finish
    NOP
    J       0x806AA41C
    NOP

    PauseControl_Sprite_Finish:
        J       0x806AB2C0
        NOP