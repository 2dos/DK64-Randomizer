CoinHUDReposition:
    ADDIU	t8, r0, 0x26
    LUI 	t7, hi(CurrentMap)
    LW 		t7, lo(CurrentMap) (t7)
    ADDIU 	a2, r0, 1
    BEQ 	t7, a2, CoinHUDReposition_Finish
    NOP
    ADDIU 	a2, r0, 5
    BEQ 	t7, a2, CoinHUDReposition_Finish
    NOP
    ADDIU 	a2, r0, 0x19
    BEQ 	t7, a2, CoinHUDReposition_Finish
    NOP

    CoinHUDReposition_Lower:
        ADDIU 	t8, r0, 0x4C

    CoinHUDReposition_Finish:
        J 	0x806F88D0
        ADDIU 	t7, r0, 0x122

GiveItemPointerToMulti:
    LUI 	t8, hi(MultiBunchCount)
    ADDIU 	t8, t8, lo(MultiBunchCount)
    SW 		t8, 0x0 (s0)
    J 		0x806F8618
    SW 		t6, 0xC (s0)

TextHandler:
    LUI 	t9, hi(PauseText)
    LBU 	t9, lo(PauseText) (t9)
    BEQZ 	t9, TextHandler_NoPause
    NOP

    TextHandler_Pause:
        J 	0x8070E8B8
        NOP

    TextHandler_NoPause:
        LW 	t9, 0x60 (a1)
        J 	0x8070E844
        LUI at, 0xFDFF

InvertCameraControls:
    ADDU 	t7, t7, t6
    LB 		t7, 0xD63F (t7)
    LUI 	a0, hi(InvertedControls)
    LBU 	a0, lo(InvertedControls) (a0)
    BEQZ 	a0, InvertCameraControls_Finish
    NOP
    SUB 	t7, r0, t7

    InvertCameraControls_Finish:
        J 	0x806EA714
        NOP

HUDDisplayCode:
    ADDIU 		a0, sp, 0x6C
    SW 			s0, 0x10 (sp)
    JAL 		writeHUDAmount
    LW 	 		a3, 0x78 (sp)
    J 			0x806F9F90
    OR 			s0, v0, r0

HomingDisable:
    LBU 		t1, 0x2 (t0)
    LUI			t2, hi(ForceStandardAmmo)
    LBU 		t2, lo(ForceStandardAmmo) (t2)
    BEQZ 		t2, HomingDisable_Finish
    NOP
    LUI 		t2, hi(ToggleAmmoOn)
    LBU 		t2, lo(ToggleAmmoOn) (t2)
    BEQZ 		t2, HomingDisable_Finish
    NOP
    ANDI 		t1, t1, 0xFFFD

    HomingDisable_Finish:
        J 		0x806E22B8
        ANDI 	t2, t1, 0x2

HomingHUDHandle:
    LUI 		a0, hi(ForceStandardAmmo)
    LBU 		a0, lo(ForceStandardAmmo) (a0)
    BEQZ 		a0, HomingHUDHandle_Finish
    NOP
    ADDIU 		a3, r0, 0x2

    HomingHUDHandle_Finish:
        OR 			a0, a3, r0
        J 			0x806EB57C
        OR 			a1, r0, r0

SkipCutscenePans:
    LUI         t1, hi(CutsceneActive)
    ADDIU       v0, r0, 1
    LBU         t1, lo(CutsceneActive) (t1)
    BNE         t1, v0, SkipCutscenePans_Persist
    NOP
    LUI         t1, hi(CutsceneIndex)
    LHU         t1, lo(CutsceneIndex) (t1)
    SLTIU       v0, t1, 64
    BEQZ        v0, SkipCutscenePans_Persist
    NOP
    LUI         t1, hi(CurrentMap)
    LW          t1, lo(CurrentMap) (t1)
    SLTIU       v0, t1, 216
    BEQZ        v0, SkipCutscenePans_Persist
    NOP
    LUI         t1, hi(CutsceneIndex)
    LHU         t1, lo(CutsceneIndex) (t1)
    ADDIU       t6, r0, 32
    SUBU        v0, t1, t6
    SLTIU       t1, t1, 32
    BEQZ        t1, SkipCutscenePans_PostShiftDetect
    ADDIU       t1, r0, 1
    LUI         t1, hi(CutsceneIndex)
    LHU         v0, lo(CutsceneIndex) (t1)
    ADDIU       t1, r0, 0

    SkipCutscenePans_PostShiftDetect:
        // t1 = offset, v0 = shift
        LUI         t6, hi(CurrentMap)
        LW          t6, lo(CurrentMap) (t6)
        SLL         t6, t6, 1
        ADDU        t6, t6, t1
        SLL         t6, t6, 2
        LUI         t1, hi(cs_skip_db)
        ADDIU       t1, t1, lo(cs_skip_db)
        ADDU        t6, t6, t1
        LW          t6, 0x0 (t6)
        ADDIU       t1, r0, 1
        SLLV        t1, t1, v0
        AND         t6, t6, t1
        BEQZ        t6, SkipCutscenePans_Persist
        NOP
        LUI         t6, hi(CutsceneStateBitfield)
        LHU         t6, lo(CutsceneStateBitfield) (t6)
        ANDI        t6, t6, 4
        BEQZ        t6, SkipCutscenePans_Skip
        NOP

    SkipCutscenePans_Persist:
        LW          t1, 0x0 (s1)
        J           0x8061E68C
        LUI         v0, 0x807F

    SkipCutscenePans_Skip:
        J           0x8061E8A4
        NOP

ModifyCameraColor:
    LUI         t0, hi(EnemyInView)
    LBU         t0, lo(EnemyInView) (t0)
    BEQZ        t0, ModifyCameraColor_Finish
    LI          t0, -1
    LUI         t0, 0xFF
    ADDIU       t0, t0, 0xFF

    ModifyCameraColor_Finish:
        J           0x806FF38C
        LUI         at, 0x3F00
    