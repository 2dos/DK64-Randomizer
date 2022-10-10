NinWarpCode:
    JAL 	checkNinWarp
    NOP
    J 		0x807132CC
    NOP

SaveToFileFixes:
    BNEZ 	s0, SaveToFileFixes_Not0
    ANDI 	a1, s3, 0xFF
    B 		SaveToFileFixes_Finish
    ADDIU  	a0, r0, 10 // Stores it in unused slot

    SaveToFileFixes_Not0:
        ADDIU 	a0, s0, 4

    SaveToFileFixes_Finish:
        J 		0x8060DFFC
        NOP

SaveHelmHurryCheck:
    SW 		s2, 0x28 (sp)
    JAL		canSaveHelmHurry
    SW 		s1, 0x24 (sp)
    OR 		t6, v0, r0
    J 		0x8060DEFC
    ADDIU 	at, r0, 1

initCode:
    JAL 		0x80609140
    SW 			r0, 0x14 (sp)
    JAL 		fixMusicRando
    NOP
    JAL 		quickInit
    NOP
    J 			0x805FBDF4
    NOP

displayListCode:
    JAL 	displayListModifiers
    OR 		a0, s0, r0
    OR 		s0, v0, r0
    LUI 	a0, 0x8075
    ADDIU 	a0, a0, 0x531C
    LHU 	v1, 0x0 (a0)
    LUI 	v0, 0x8075
    J 		0x80714184
    LBU 	v0, 0x5314 (v0)

updateLag:
    LUI 	t6, hi(FrameReal)
    LW 		a0, lo(FrameReal) (t6)
    LUI 	t6, hi(FrameLag)
    LW 		a1, lo(FrameLag) (t6)
    SUBU 	a1, a0, a1
    LUI 	t6, hi(StoredLag)
    SH 		a1, lo(StoredLag) (t6)
    LUI 	t6, 0x8077
    J 		0x8060067C
    LBU 	t6, 0xAF14 (t6)

InstanceScriptCheck:
    ADDIU 	t1, r0, 1
    ADDI 	t4, t4, -1 // Reduce move_index by 1
    SLLV 	t4, t1, t4 // 1 << move_index
    ADDIU 	t1, r0, 0
    AND 	at, t6, t4 // at = kong_moves & move_index
    BEQZ 	at, InstanceScriptCheck_Fail
    NOP

    InstanceScriptCheck_Success:
        J 	0x8063EE14
        NOP

    InstanceScriptCheck_Fail:
        J 	0x8063EE1C
        NOP

EarlyFrameCode:
    JAL 	earlyFrame
    NOP
    JAL 	0x805FC668
    NOP
    J 		0x805FC404
    NOP

DynamicCodeFixes:
    JAL 		decouple_moves_fixes
    NOP
    LUI 		a1, 0x8074
    J 			0x80610950
    LUI 		t1, 0x8074

getLobbyExit:
    LUI 	a1, hi(ReplacementLobbyExitsArray)
    SLL 	t7, t6, 1
    ADDU 	a1, a1, t7
    LHU 	a1, lo(ReplacementLobbyExitsArray) (a1)
    ADDU 	a0, a0, t7
    JAL 	0x805FF378
    LHU 	a0, lo(ReplacementLobbiesArray) (a0)
    JAL 	resetMapContainer
    NOP
    J 		0x80600070
    NOP

checkFlag_ItemRando:
    JAL     getFlagBlockAddress
    SH      a2, 0x22 (sp)
    LW      a0, 0x24 (sp)
    JAL     updateFlag
    ADDIU   a1, sp, 0x22
    J       0x80731170
    NOP

setFlag_ItemRando:
    JAL     getFlagBlockAddress
    SH      a3, 0x32 (sp)
    LW      a0, 0x38 (sp)
    JAL     updateFlag
    ADDIU   a1, sp, 0x32
    J       0x80731300
    NOP