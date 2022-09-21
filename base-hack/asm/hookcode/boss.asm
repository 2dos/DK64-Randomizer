Jump_KRoolLankyPhaseFix:
    J 			KRoolLankyPhaseFix
    NOP
Jump_KKOPhaseHandler:
    J 			KKOPhaseHandler
    NOP
Jump_KKOInitPhase:
    J 			KKOInitPhase
    NOP
Jump_MadJackShort:
    J 			MadJackShort
    NOP
Jump_PufftossShort:
    J 			PufftossShort
    NOP
Jump_DogadonRematchShort:
    J 			DogadonRematchShort
    NOP
Jump_DilloRematchShort:
    J 			DilloRematchShort
    NOP
Jump_DKPhaseShort:
    J 			DKPhaseShort
    NOP
Jump_ChunkyPhaseShort:
    J 			ChunkyPhaseShort
    NOP
Jump_TinyPhaseShort:
    J 			TinyPhaseShort
    NOP
Jump_ChunkyPhaseAddedSave:
    J 			ChunkyPhaseAddedSave
    NOP
    

PatchKRoolCode:
    LUI 		t3, hi(Jump_KRoolLankyPhaseFix)
    LW 			t3, lo(Jump_KRoolLankyPhaseFix) (t3)
    LUI 		t4, 0x8003
    SW 			t3, 0x8CCC (t4)
    SW 			r0, 0x8CD0 (t4)

    LUI 		t3, hi(KKOPhaseRandoOn)
    LBU 		t3, lo(KKOPhaseRandoOn) (t3)
    BEQZ 		t3, PatchKRoolCode_0
    NOP

    LUI 		t3, hi(Jump_KKOPhaseHandler)
    LW 			t3, lo(Jump_KKOPhaseHandler) (t3)
    LUI 		t4, 0x8003
    SW 			t3, 0x2570 (t4)
    SW 			r0, 0x2574 (t4)

    LUI 		t3, hi(Jump_KKOInitPhase)
    LW 			t3, lo(Jump_KKOInitPhase) (t3)
    LUI 		t4, 0x8003
    SW 			t3, 0x1B2C (t4)
    SW 			r0, 0x1B30 (t4)

    // KKO Last Phase Check
    LUI 		t3, 0x8003
    ADDIU 		t4, r0, 4
    SH 			t4, 0x259A (t3)

    // KKO Enemy Check
    LUI 		t3, hi(KKOPhaseOrder + 1)
    LBU 		t3, lo(KKOPhaseOrder + 1) (t3)
    LUI 		t4, 0x8003
    SH 			t3, 0x2566 (t4)

    PatchKRoolCode_0:
        LUI 		t3, hi(ShorterBosses)
        LBU 		t3, lo(ShorterBosses) (t3)
        BEQZ 		t3, PatchKRoolCode_1
        NOP

        LUI 		t3, hi(Jump_MadJackShort)
        LW 			t3, lo(Jump_MadJackShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0x5120 (t4)
        SW 			r0, 0x5124 (t4)

        // Mad Jack Cutscene Memery
        LUI 		t3, 0x8003
        ADDIU 		t4, r0, 2
        SH 			t4, 0x50D2 (t3)

        LUI 		t3, hi(Jump_PufftossShort)
        LW 			t3, lo(Jump_PufftossShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0x9AAC (t4)
        SW 			r0, 0x9AB0 (t4)

        LUI 		t3, hi(Jump_DogadonRematchShort)
        LW 			t3, lo(Jump_DogadonRematchShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0xACB0 (t4)
        SW 			r0, 0xACB4 (t4)

        LUI 		t3, hi(Jump_DilloRematchShort)
        LW 			t3, lo(Jump_DilloRematchShort) (t3)
        LUI 		t4, 0x8002
        SW 			t3, 0x57CC (t4)
        SW 			r0, 0x57D0 (t4)

        // KKO Phase Hit Limit
        LUI 		t3, 0x8003
        ADDIU 		t4, r0, 2
        SH 			t4, 0x22BA (t3)

        LUI 		t3, hi(Jump_DKPhaseShort)
        LW 			t3, lo(Jump_DKPhaseShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0xDB10 (t4)
        SW 			r0, 0xDB14 (t4)

        // Diddy Phase Hit Count
        LUI 		t3, 0x8003
        ADDIU 		t4, r0, 2
        SH 			t4, 0xE52A (t3)

        // Lanky Phase Hit Count
        LUI 		t3, 0x8003
        ADDIU 		t4, r0, 2
        SH 			t4, 0xEF02 (t3)

        LUI 		t3, hi(Jump_TinyPhaseShort)
        LW 			t3, lo(Jump_TinyPhaseShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0x0370 (t4)
        SW 			r0, 0x0374 (t4)

        LUI 		t3, hi(Jump_ChunkyPhaseShort)
        LW 			t3, lo(Jump_ChunkyPhaseShort) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0x14B4 (t4)
        SW 			r0, 0x14B8 (t4)

    PatchKRoolCode_1:
        LUI 		t3, hi(Jump_ChunkyPhaseAddedSave)
        LW 			t3, lo(Jump_ChunkyPhaseAddedSave) (t3)
        LUI 		t4, 0x8003
        SW 			t3, 0x1378 (t4)
        SW 			r0, 0x137C (t4)


        JR 			ra
        NOP

KRoolLankyPhaseFix:
    LUI 		a1, 0x8003
    LBU 		a2, 0x43 (sp)
    SLL 		a2, a2, 1
    ADDU 		a1, a1, a2
    J 			0x80028CD4
    LH 			a1, 0x59A0 (a1)

KKOPhaseHandler:
    LUI 		v0, hi(KKOPhaseOrder)
    ADDIU 		v0, v0, lo(KKOPhaseOrder)
    LB 			a0, 0x0 (v0)
    BNE 		t7, a0, KKOPhaseHandler_Slot2
    NOP
    B 			KKOPhaseHandler_Finish
    LB 			t8, 0x1 (v0)

    KKOPhaseHandler_Slot2:
        LB 		a0, 0x1 (v0)
        BNE 	t7, a0, KKOPhaseHandler_Slot3
        NOP
        B 		KKOPhaseHandler_Finish
        LB 		t8, 0x2 (v0)

    KKOPhaseHandler_Slot3:
        LB 		a0, 0x2 (v0)
        BNE 	t7, a0, KKOPhaseHandler_Finish
        NOP
        B 		KKOPhaseHandler_Finish
        ADDIU 	t8, r0, 4

    KKOPhaseHandler_Finish:
        SB 		t8, 0x12 (s0)
        J 		0x80032578
        LB 		v0, 0x12 (s0)

KKOInitPhase:
    LUI 		at, hi(KKOPhaseOrder)
    LB 			at, lo(KKOPhaseOrder) (at)
    SB 			at, 0x12 (s0)
    J 			0x80031B34
    LUI 		at, 0x8003

MadJackShort:
    ADDIU 		t1, r0, 1 // Phase 2
    BEQ 		t1, t8, MadJackShort_Skip
    NOP
    ADDIU 		t1, r0, 3 // Phase 4
    BNE 		t1, t8, MadJackShort_Finish
    NOP

    MadJackShort_Skip:
        ADDIU 		t8, t8, 1

    MadJackShort_Finish:
        ANDI 		t1, t8, 0xFF
        J 			0x80035128
        SLL 		t0, t1, 2

PufftossShort:
    ADDIU 		t6, r0, 1 // Phase 2
    BEQ 		t5, t6, PufftossShort_Skip
    NOP
    ADDIU 		t6, r0, 3 // Phase 4
    BNE 		t5, t6, PufftossShort_Finish
    NOP

    PufftossShort_Skip:
        ADDIU 		t5, t5, 1

    PufftossShort_Finish:
        ANDI 		t6, t5, 0xFF
        J 			0x80029AB4
        SLL 		t7, t6, 2

DogadonRematchShort:
    ADDIU 		v0, r0, 0x53 // Dogadon 2 Map
    LUI 		t1, hi(CurrentMap)
    LW 			t1, lo(CurrentMap) (t1)
    BNE 		v0, t1, DogadonRematchShort_Finish
    NOP
    ADDIU 		v0, r0, 1 // Phase 2
    BNE 		t0, v0, DogadonRematchShort_Finish
    NOP
    ADDIU 		t0, t0, 1

    DogadonRematchShort_Finish:
        ANDI 	v0, t0, 0xFF
        J 		0x8002ACB8
        SLL 	t1, v0, 2

DilloRematchShort:
    ADDIU 		t4, t3, 1
    ADDIU 		t5, r0, 0xC4 // Dillo 2 Map
    LUI 		at, hi(CurrentMap)
    LW 			at, lo(CurrentMap) (at)
    BNE 		t5, at, DilloRematchShort_Finish
    NOP
    ADDIU 		t5, r0, 1 // Phase 2
    BNE 		t5, t4, DilloRematchShort_Finish
    NOP
    ADDIU 		t4, t4, 1

    DilloRematchShort_Finish:
        J 		0x800257D4
        LUI 	t5, 0x8077

DKPhaseShort:
    ADDIU 		t4, r0, 2 // Phase 3
    BNE 		t4, t3, DKPhaseShort_Finish
    NOP
    ADDIU 		t3, t3, 1

    DKPhaseShort_Finish:
        ANDI 	t4, t3, 0xFF
        J 		0x8002DB18
        SLL 	t5, t4, 2

TinyPhaseShort:
    JAL 		handleFootProgress
    OR 			a0, s0, r0
    J 			0x800303DC
    NOP

ChunkyPhaseShort:
    ADDIU 		t6, r0, 2 // Phase 3
    BNE 		t6, t5, ChunkyPhaseShort_Finish
    NOP
    ADDIU 		t5, t5, 1

    ChunkyPhaseShort_Finish:
        ANDI 	t6, t5, 0xFF
        J 		0x800314BC
        SLL 	t7, t6, 2

ChunkyPhaseAddedSave:
    LUI 		a2, hi(WinCondition)
    LBU 		a2, lo(WinCondition) (a2)
    BNEZ 		a2, ChunkyPhaseAddedSave_Finish
    NOP
    JAL 		setFlag
    OR 			a2, r0, r0

    ChunkyPhaseAddedSave_Finish:
        JAL 	0x8060DEC8
        NOP
        J 		0x80031380
        NOP

FixPufftossInvalidWallCollision:
    LW 		s0, 0x8C (s6)
    BEQZ 	s0, FixPufftossInvalidWallCollision_Invalid
    NOP
    SRA 	t9, s0, 16
    SLTIU 	t9, t9, 0x8000 // 1 if < 0x80000000
    BNEZ 	t9, FixPufftossInvalidWallCollision_Invalid
    NOP
    SRA 	t9, s0, 16
    SLTIU 	t9, t9, 0x8080 // 0 if > 0x80800000
    BEQZ 	t9, FixPufftossInvalidWallCollision_Invalid
    NOP
    J 		0x80677C20
    NOP

    FixPufftossInvalidWallCollision_Invalid:
        J 	0x80677C78
        NOP