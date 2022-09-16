START_HOOK:
	NinWarpCode:
		JAL 	checkNinWarp
		NOP
		J 		0x807132CC
		NOP

	Jump_AlwaysCandyInstrument:
		J 		AlwaysCandyInstrument
		NOP
	Jump_CrankyDecouple:
		J 		CrankyDecouple
		NOP
	Jump_ForceToBuyMoveInOneLevel:
		J 		ForceToBuyMoveInOneLevel
		NOP
	Jump_MoveShow0:
		J 		FixInvisibleText_0
		NOP
	Jump_MoveShow1:
		J 		FixInvisibleText_1
		NOP
	Jump_PriceKongStore:
		J 		PriceKongStore
		NOP
	Jump_CharacterCollectableBaseModify:
		J 		CharacterCollectableBaseModify
		NOP
	Jump_SetMoveBaseBitfield:
		J 		SetMoveBaseBitfield
		NOP
	Jump_SetMoveBaseProgressive:
		J 		SetMoveBaseProgressive
		NOP
		
	PatchCrankyCode:
		LUI t3, hi(Jump_CrankyDecouple)
		LW t3, lo(Jump_CrankyDecouple) (t3)
		LUI t4, 0x8002
		SW t3, 0x60E0 (t4) // Store Hook
		SW r0, 0x60E4 (t4) // Store NOP

		LUI t3, hi(Jump_ForceToBuyMoveInOneLevel)
		LW t3, lo(Jump_ForceToBuyMoveInOneLevel) (t3)
		LUI t4, 0x8002
		SW 	t3, 0x60A8 (t4) // Store Hook
		SW 	r0, 0x60AC (t4) // Store NOP
		SW 	r0, 0x6160 (t4) // Store NOP to prevent loop

		LUI t3, hi(Jump_PriceKongStore)
		LW t3, lo(Jump_PriceKongStore) (t3)
		LUI t4, 0x8002
		SW t3, 0x6140(t4) // Store Hook
		SW r0, 0x6144 (t4) // Store NOP

		LUI t3, hi(Jump_CharacterCollectableBaseModify)
		LW t3, lo(Jump_CharacterCollectableBaseModify) (t3)
		LUI t4, 0x8002
		SW t3, 0x5FC0(t4) // Store Hook
		SW r0, 0x5FC4 (t4) // Store NOP

		LUI t3, hi(Jump_SetMoveBaseBitfield)
		LW t3, lo(Jump_SetMoveBaseBitfield) (t3)
		LUI t4, 0x8002
		SW t3, 0x60F0(t4) // Store Hook
		SW r0, 0x60F4 (t4) // Store NOP

		LUI t3, hi(Jump_SetMoveBaseProgressive)
		LW t3, lo(Jump_SetMoveBaseProgressive) (t3)
		LUI t4, 0x8002
		SW t3, 0x611C(t4) // Store Hook
		SW r0, 0x6120 (t4) // Store NOP

		LUI t3, hi(CurrentMap)
		LW 	t3, lo(CurrentMap) (t3)
		ADDIU t4, r0, 0x5
		BEQ t3, t4, PatchCrankyCode_Cranky
		NOP

		LUI t3, hi(Jump_MoveShow0)
		LW t3, lo(Jump_MoveShow0) (t3)
		LUI t4, 0x8002
		SW 	t3, 0x7AE8 (t4) // Store Hook
		SW 	r0, 0x7AEC (t4) // Store NOP

		LUI t3, hi(Jump_MoveShow1)
		LW t3, lo(Jump_MoveShow1) (t3)
		LUI t4, 0x8002
		SW 	t3, 0x7B30 (t4) // Store Hook
		SW 	r0, 0x7B34 (t4) // Store NOP

		B 	PatchCrankyCode_More
		NOP

		PatchCrankyCode_Cranky:
			LUI 	t3, 0x8002
			ADDIU 	t4, r0, 300
			SH 		t4, 0x7B72 (t3)
			SH 		t4, 0x7BCA (t3)
			SH 		t4, 0x7BFA (t3)

		PatchCrankyCode_More:
			LUI 	t4, hi(Jump_AlwaysCandyInstrument)
			LW 		t4, lo(Jump_AlwaysCandyInstrument) (t4)
			LUI 	t3, 0x8002
			SW 		t4, 0x6924 (t3)
			SW 		r0, 0x6928 (t3)

			LUI t3, 0x8002
			ADDIU t4, r0, hi(CrankyMoves_New)
			SH t4, 0x6072 (t3)
			ADDIU t4, r0, lo(CrankyMoves_New)
			SH t4, 0x607A (t3)
			ADDIU t4, r0, hi(CandyMoves_New)
			SH t4, 0x607E (t3)
			ADDIU t4, r0, lo(CandyMoves_New)
			SH t4, 0x6086 (t3)
			ADDIU t4, r0, hi(FunkyMoves_New)
			SH t4, 0x608A (t3)
			ADDIU t4, r0, lo(FunkyMoves_New)
			SH t4, 0x608E (t3)

		JR 		ra
		NOP

	CrankyDecouple:
		BEQ		a0, t0, CrankyDecouple_Bitfield
		OR 		v1, a0, r0
		BEQZ 	a0, CrankyDecouple_Bitfield
		NOP

		CrankyDecouple_Progessive:
			J 		0x800260E8
			NOP

		CrankyDecouple_Bitfield:
			J 		0x800260F0
			NOP

	ForceToBuyMoveInOneLevel:
		ADDU 	t3, t3, t9
		SLL 	t3, t3, 1
		LBU 	t2, 0xC (s2) // Current Level
		SLTIU 	t1, t2, 7
		BEQZ 	t1, ForceToBuyMoveInOneLevel_Skip // If level < 7 (In one of the main 7 levels, progress. Otherwise skip)
		NOP
		SLL 	t1, t2, 2
		SUBU 	t1, t1, t2
		SLL 	t1, t1, 1 // Current Level * 6
		J 		0x800260B4
		ADDU 	v1, v1, t1

		ForceToBuyMoveInOneLevel_Skip:
			LUI 	s1, 0x8002
			SW 		r0, 0x6194 (s1)
			J 		0x80026168
			ADDIU 	s1, r0, 0

	AlwaysCandyInstrument:
		// Candy
		LUI 	at, 0x8080
		LW 		at, 0xBB40 (at)
		LW 		t9, 0x58 (at)
		ADDIU 	at, r0, 191
		BEQ 	t9, at, AlwaysCandyInstrument_IsCandy
		ADDIU 	t9, r0, 4
		// Funky
		LUI 	at, 0x8080
		LW 		at, 0xBB40 (at)
		LW 		t9, 0x58 (at)
		ADDIU 	at, r0, 190
		BEQ 	t9, at, AlwaysCandyInstrument_IsCandy
		ADDIU 	t9, r0, 2
		// Cranky
		LUI 	at, 0x8080
		LW 		at, 0xBB40 (at)
		LW 		t9, 0x58 (at)
		ADDIU 	at, r0, 189
		BEQ 	t9, at, AlwaysCandyInstrument_IsCandy
		ADDIU 	t9, r0, 0
		// Default
		LBU 	t9, 0xB (s0)
		
		AlwaysCandyInstrument_IsCandy:
			J 		0x8002692C
			SLTIU 	at, t9, 0x5

	FixInvisibleText_0:
		LW 		a0, 0xC4 (sp)
		ADDIU 	t8, r0, 0x82
		SW 		t8, 0x90 (a0)
		ADDIU 	a0, sp, 0x3C
		J 		0x80027AF0
		SLL 	t8, t7, 5

	FixInvisibleText_1:
		LW  	v0, 0xC4 (sp)
		ADDIU 	a1, r0, 0x82
		SW 		a1, 0x90 (v0)
		OR 		v0, r0, r0
		J 		0x80027B38
		ADDIU 	a1, sp, 0x3C

	PriceKongStore:
		// Stores price & kong correctly
		// 0x80026140
		LH 		v0, 0x4 (a1)
		SH 		v0, 0x4 (s2)
		ANDI 	t8, v0, 0xFF
		J 		0x8002614C
		SH 		t8, 0x0 (t2)

	CharacterCollectableBaseModify:
		// Replaces param2 with the start of the character collectable base
		// 0x80025FC0
		OR 		s2, a0, r0
		LUI 	a1, hi(MovesBase)
		ADDIU	a1, a1, lo(MovesBase)
		J 		0x80025FC8
		OR 		s3, a1, r0

	SetMoveBaseBitfield:
		// Sets the move base to the correct kong (Bitfield)
		// 0x800260F0
		LH 		t4, 0x2 (a1)
		ADDU 	t8, s3, a0
		LBU 	t9, 0x4 (a1)
		ADDIU 	t6, r0, 0x5E
		MULT 	t9, t6
		MFLO 	t9
		J 		0x800260F8
		ADDU 	t8, t8, t9

	SetMoveBaseProgressive:
		// Sets the move base to the correct kong (Progressive)
		// 0x8002611C
		LBU 	t6, 0x4 (a1)
		ADDIU 	t5, r0, 0x5E
		MULT 	t6, t5
		MFLO	t6
		ADDU 	t4, t4, t6
		LBU 	t6, 0x0 (t4)
		J 		0x80026124
		LH 		t5, 0x2 (a1)

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

	KongUnlockCorrectCode:
		ADDIU 	s0, s0, 0x3805
		JAL 	correctKongFaces
		ADDIU 	s2, s2, 0x5B2
		J 		0x800298DC
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

	BarrelMovesFixes:
		LBU 	t0, 0x4238 (t0) // Load Barrel Moves Array Slot
		ADDI 	t0, t0, -1 // Reduce move_value by 1
		ADDIU 	v1, r0, 1
		SLLV 	t0, v1, t0 // Get bitfield value
		AND  	v1, t0, t9
		BEQZ 	v1, BarrelMovesFixes_Finish
		NOP
		ADDIU 	v1, r0, 1

		BarrelMovesFixes_Finish:
			J 		0x806F6EB4
			NOP

	ChimpyChargeFix:
		ANDI 	t6, t6, 1
		LUI	 	v1, 0x8080
		J 		0x806E4938
		ADDIU 	v1, v1, 0xBB40

	OStandFix:
		LBU 	t2, 0xCA0C (t2)
		ANDI 	t2, t2, 1
		J 		0x806E48B4
		ADDIU 	a0, r0, 0x25

	HunkyChunkyFix2:
		BNEL 	v1, at, HunkyChunkyFix2_Finish
		LI 		at, 4
		ANDI 	a2, a0, 1
		BLEZL 	a2, HunkyChunkyFix2_Finish
		LI 		at, 4
		J 		0x8067ECC8
		NOP

		HunkyChunkyFix2_Finish:
			J 		0x8067ECD0
			nop

	EarlyFrameCode:
		JAL 	earlyFrame
		NOP
		JAL 	0x805FC668
		NOP
		J 		0x805FC404
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

	damageMultiplerCode:
		BGEZ 	a3, damageMultiplerCode_Finish
		LB 		t9, 0x2FD (v0)
		SUBU 	t2, r0, a3
		SLTI 	t2, t2, 12
		BEQZ 	t2, damageMultiplerCode_Finish
		NOP
		LUI 	t2, hi(DamageMultiplier)
		LBU 	t2, lo(DamageMultiplier) (t2)
		MULTU 	a3, t2
		MFLO 	a3

		damageMultiplerCode_Finish:
			J 		0x806C9A84
			ADDU 	t0, t9, a3

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
		ADDIU 	a0, r0, 0x22
		JAL 	0x805FF378 // Init Map Change
		ADDIU 	a1, r0, 0
		JAL 	resetMapContainer
		NOP
		J 		0x806A8A20
		ADDIU 	at, r0, 2
		
		PauseExtraSlotCustomCode_Finish:
			J 		0x806A880C
			ADDIU 	at, r0, 2

	FileScreenDLCode_Jump:
		J 		FileScreenDLCode
		NOP
	FileSelectDLCode_Jump:
		J 		FileSelectDLCode
		NOP
	Jump_MenuUnlock:
		J 		KongUnlockCorrectCode
		NOP

	FileScreenDLCode_Write:
		LUI t3, hi(FileScreenDLCode_Jump)
		LW t3, lo(FileScreenDLCode_Jump) (t3)
		LUI t4, 0x8003
		SW t3, 0x937C (t4) // Store Hook
		SW r0, 0x9380 (t4) // Store NOP

		LUI t3, hi(Jump_MenuUnlock)
		LW t3, lo(Jump_MenuUnlock) (t3)
		LUI t4, 0x8003
		SW t3, 0x98B8 (t4) // Store Hook
		SW r0, 0x98BC (t4) // Store NOP

		LUI t3, hi(FileSelectDLCode_Jump)
		LW t3, lo(FileSelectDLCode_Jump) (t3)
		LUI t4, 0x8003
		SW t3, 0x8E90 (t4) // Store Hook
		SW r0, 0x8E94 (t4) // Store NOP

		LUI t3, 0x8003
		ADDIU t3, t3, 0x37DC
		ADDIU t4, r0, 0xFF
		SB 	t4, 0x0 (t3)
		SB 	t4, 0x3 (t3)
		ADDIU t4, r0, 0xD7
		SB 	t4, 0x1 (t3)
		SB 	r0, 0x2 (t3)
		JR 	ra
		NOP

	FileScreenDLCode:
		ADDIU 	s0, t4, -0x140
		JAL 	display_text
		ADDIU 	a0, s2, 8
		J 		0x80029690
		ADDIU 	s2, v0, 0

	AutowalkFix:
		// Free Variables
		// at, t2, a0, t7, t8
		LUI 	a0, hi(TransitionSpeed)
		LHU 	a0, lo(TransitionSpeed) (a0)
		ANDI 	a0, a0, 0x8000 // Get sign
		BEQZ 	a0, AutowalkFix_Vanilla // No transition exit
		NOP
		LUI 	t7, hi(DestMap)
		LW 		t7, lo(DestMap) (t7)
		LUI 	t8, hi(DestExit)
		LW 		t8, lo(DestExit) (t8)
		ADDIU 	t2, r0, 0x22
		BNE 	t7, t2, AutowalkFix_NotAztecDoor
		ADDIU 	a0, r0, 3
		BEQ 	t8, a0, AutowalkFix_Finish
		LUI 	at, 0x44F2

		AutowalkFix_NotAztecDoor:
			ADDIU 	t2, r0, 0x1A
			BNE 	t7, t2, AutowalkFix_NotCrusher
			ADDIU 	a0, r0, 8
			LUI 	at, 0x4536
			BEQ 	t8, a0, AutowalkFix_Finish
			ADDIU 	at, at, 0x4000

		AutowalkFix_NotCrusher:
			ADDIU 	t2, r0, 0x57
			BNE 	t7, t2, AutowalkFix_NotCastle
			ADDIU 	a0, r0, 15
			LUI 	at, 0x452F
			BEQ 	t8, a0, AutowalkFix_Finish // Castle Tree
			ADDIU 	at, at, 0x9000
			ADDIU 	a0, r0, 11
			LUI 	at, 0x4552
			BEQ 	t8, a0, AutowalkFix_Finish // Castle Ballroom
			ADDIU 	at, at, 0x4000
			ADDIU 	a0, r0, 21
			LUI 	at, 0x45FD
			BEQ 	t8, a0, AutowalkFix_Finish // Castle Entry (Cancel Autowalk)
			ADDIU 	at, at, 0x2000

		AutowalkFix_NotCastle:
			ADDIU 	t2, r0, 0x70
			BNE  	t7, t2, AutowalkFix_Vanilla
			ADDIU 	a0, r0, 1
			BEQ 	t8, a0, AutowalkFix_Finish
			LUI 	at, 0x4361

		AutowalkFix_Vanilla:
			LUI 	at, 0x42C8

		AutowalkFix_Finish:
			J 		0x806F3E7C
			OR 		t2, r0, r0

	FileSelectDLCode:
		JAL 		0x806ABB98
		SRA 		a2, t3, 0x10
		ADDIU 		a0, v0, 0
		LWC1		f6, 0xF8 (sp)
		LUI 		a1, 0x4080
		MTC1 		a1, f0
		MUL.S 		f6, f6, f0
		TRUNC.W.S 	f6, f6
		JAL 		displayHash
		MFC1 		a1, f6
		J 			0x80028E98
		NOP

	DynamicCodeFixes:
		JAL 		decouple_moves_fixes
		NOP
		LUI 		a1, 0x8074
		J 			0x80610950
		LUI 		t1, 0x8074

	danceSkip0:
		LUI 		a1, hi(SkipDance)
		LBU 		a1, lo(SkipDance) (a1)
		BNEZ 		a1, danceSkip0_Skip
		NOP
		JAL 		0x80614E78
		ADDIU 		a1, r0, 0x5B
		J 			0x806EFB90
		NOP

		danceSkip0_Skip:
			LUI 	t1, 0x8080
			J 		0x806EFBAC
			LUI 	t2, 0x8080

	danceSkip1:
		LUI 		t4, hi(SkipDance)
		LBU 		t4, lo(SkipDance) (t4)
		BNEZ 		t4, danceSkip1_Skip
		NOP
		LW 			t4, 0x0 (s0)
		SH 			v0, 0xE6 (t4)

		danceSkip1_Skip:
			J 		0x806EFC10
			NOP

	danceSkip2:
		LUI 		a3, hi(SkipDance)
		LBU 		a3, lo(SkipDance) (a3)
		BNEZ 		a3, danceSkip2_Skip
		NOP
		JAL 		0x80627948
		ADDIU 		a3, r0, 5

		danceSkip2_Skip:
			J 		0x806EFC24
			NOP

	permaLossTagCheck:
		JAL 		determineKongUnlock
		LW 			a0, 0x58 (t5)
		J 			0x80682F48
		NOP

	permaLossTagSet:
		JAL	 		unlockKongPermaLoss
		LW 			a0, 0x58 (t9)
		J 			0x80683640
		NOP

	permaLossTagDisplayCheck:
		JAL 		determineKongUnlock
		OR 			a1, s0, r0
		J 			0x806840e0
		NOP

	tagPreventCode:
		LUI 		a1, hi(preventTagSpawn)
		LBU 		a1, lo(preventTagSpawn) (a1)
		BEQZ 		a1, tagPreventCode_Vanilla
		NOP
		LH 			a1, 0x0 (s1)
		ADDIU 		a1, a1, 0x10
		ADDIU 		t8, r0, 98
		BEQ 		a1, t8, tagPreventCode_Prevent
		NOP
		ADDIU 		t8, r0, 136
		BEQ 		a1, t8, tagPreventCode_Prevent
		NOP
		ADDIU 		t8, r0, 137
		BEQ 		a1, t8, tagPreventCode_Prevent
		NOP

		tagPreventCode_Vanilla:
			LH 		a1, 0x0 (s1)
			J 		0x8068953C
			SUBU 	t3, t3, r0

		tagPreventCode_Prevent:
			J 		0x8068968C
			NOP

	destroyAllBarrelsCode:
		LW 			t6, 0x0 (s1)
		SB 			v0, 0x131 (t6)
		LUI 		a0, hi(Gamemode)
		LBU 		a0, lo(Gamemode) (a0)
		ADDIU 		t0, r0, 3
		BEQ 		a0, t0, destroyAllBarrelsCode_Finish
		NOP
		LUI 		a0, hi(bonusAutocomplete)
		LBU 		a0, lo(bonusAutocomplete) (a0)
		ANDI 		t0, a0, 1
		BEQZ 		t0, destroyAllBarrelsCode_Helm
		NOP
		LW 			t0, 0x58 (t6)
		ADDIU 		v0, r0, 0x1C
		BNE 		t0, v0, destroyAllBarrelsCode_Helm
		NOP
		ADDIU 		t0, r0, 0xC
		SB 			t0, 0x154 (t6)
		SB 			r0, 0x155 (t6)
		ADDIU 		t0, r0, 3
		SB 			t0, 0x185 (t6)

		destroyAllBarrelsCode_Helm:
		ANDI 		t0, a0, 2
		BEQZ  		t0, destroyAllBarrelsCode_Finish
		NOP
		LW 			t0, 0x58 (t6)
		ADDIU 		v0, r0, 0x6B
		BNE 		t0, v0, destroyAllBarrelsCode_Finish
		NOP
		ADDIU 		t0, r0, 0xC
		SB 			t0, 0x154 (t6)
		SB 			r0, 0x155 (t6)
		ADDIU 		t0, r0, 3
		SB 			t0, 0x185 (t6)

		destroyAllBarrelsCode_Finish:
		J 			0x80680D18
		NOP

	initCode:
		JAL 		0x80609140
		SW 			r0, 0x14 (sp)
		JAL 		fixMusicRando
		NOP
		JAL 		quickInit
		NOP
		J 			0x805FBDF4
		NOP

	KeyCompressionCode:
		SRA 		s5, t7, 0x10
		ADDIU 		t5, r0, 1
		SB 			t5, 0x154 (t4)
		J 			0x806BD330
		SH 			t5, 0x146 (t4)

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
		LUI 		t2, hi(QoLOn)
		LBU 		t2, lo(QoLOn) (t2)
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

	DKCollectableFix:
		LHU 		v0, 0x4A (s0)
		ADDIU 		t8, r0, 0xD // CB Single
		BEQ 		v0, t8, DKCollectableFix_IsCollectable
		NOP
		ADDIU 		t8, r0, 0x2B // CB Bunch
		BEQ 		v0, t8, DKCollectableFix_IsCollectable
		NOP
		ADDIU 		t8, r0, 0x1D // Coin
		BEQ 		v0, t8, DKCollectableFix_IsCollectable
		NOP
		SRA 		t8, a0, 0x10
		J 			0x806324CC
		OR 			a0, t8, r0

		DKCollectableFix_IsCollectable:
			J 		0x806324CC
			ADDIU 	a0, r0, 385

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
		JAL 	setFlag
		OR 		a2, r0, r0
		JAL 	0x8060DEC8
		NOP
		J 		0x80031380
		NOP

	Jump_RemoveKrazyKKLagImpact:
		J 			RemoveKrazyKKLagImpact
		NOP

	PatchBonusCode:
		LUI 		t3, hi(Jump_RemoveKrazyKKLagImpact)
		LW 			t3, lo(Jump_RemoveKrazyKKLagImpact) (t3)
		LUI 		t4, 0x8003
		SW 			t3, 0x95D4 (t4)
		JR 			ra
		SW 			r0, 0x95D8 (t4)

	RemoveKrazyKKLagImpact:
		LH 			t4, 0x0 (t0)
		LUI 		t5, hi(StoredLag)
		LHU 		t5, lo(StoredLag) (t5)
		J 			0x800295DC
		SUBU 		t5, t4, t5

	CannonForceCode:
		LUI 		a0, hi(CurrentMap)
		LW 			a0, lo(CurrentMap) (a0)
		ADDIU 		v0, r0, 0x22
		BEQ 		a0, v0, CannonForceCode_IsIsles
		NOP
		J 			0x8067B694
		NOP

		CannonForceCode_CheckFlag:
			JAL 	0x8067B450
			OR 		a0, s0, r0
			J 		0x8067B68C
			NOP

		CannonForceCode_IsIsles:
			LUI 	a0, hi(LobbiesOpen)
			LBU		a0, lo(LobbiesOpen) (a0)
			BEQZ 	a0, CannonForceCode_CheckFlag
			NOP
			J 		0x8067B6CC
			NOP

	GuardAutoclear:
		// Check Overlay
		LUI 		a1, 0x8080
		LW 			a1, 0xBB64 (a1)
		ANDI 		a0, a1, 0x4000
		BNEZ 		a0, GuardAutoclear_IsSnoop
		NOP
		SRA 		a1, a1, 16
		ANDI 		a0, a1, 0x10
		BNEZ		a0, GuardAutoclear_IsSnoop
		NOP

		GuardAutoclear_NotSnoop:
			JAL 	guardCatch // Void Warp
			NOP
			B 		GuardAutoclear_Finish
			NOP

		GuardAutoclear_IsSnoop:
			ADDIU 	a0, r0, 0x43
			JAL 	0x806EB0C0
			LW 		a1, 0x0 (s0)

		GuardAutoclear_Finish:
			J 		0x806AE564
			NOP

	GuardDeathHandle:
		JAL 	newGuardCode
		NOP
		LUI 	v1, 0x8080
		LW 		s0, 0xBB40 (v1)
		J 		0x806AF754
		NOP

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

	ShopImageHandler:
		JAL 	0x807149B8
		ADDIU 	a0, r0, 1
		LH 		v0, 0x4A (sp)
		LW 		t2, 0x44 (sp)
		ADDIU 	at, r0, 0x90
		MULTU 	t2, at
		MFLO 	at
		LUI 	t2, hi(ObjectModel2Pointer)
		LW 		t2, lo(ObjectModel2Pointer) (t2)
		ADDU 	t2, t2, at
		LHU		t2, 0x84 (t2) // Object Type
		ADDIU 	at, r0, 0x73
		BEQ 	t2, at, ShopImageHandler_IsCranky
		NOP
		ADDIU 	at, r0, 0x7A
		BEQ 	t2, at, ShopImageHandler_IsFunky
		NOP
		ADDIU 	at, r0, 0x124
		BEQ 	t2, at, ShopImageHandler_IsCandy
		NOP
		ADDIU 	at, r0, 0x79
		BEQ 	t2, at, ShopImageHandler_IsSnide
		NOP
		B 		ShopImageHandler_Finish
		NOP

		ShopImageHandler_IsCranky:
			B 		ShopImageHandler_Finish
			ADDIU 	v0, r0, 1
			
		ShopImageHandler_IsFunky:
			B 		ShopImageHandler_Finish
			ADDIU 	v0, r0, 2

		ShopImageHandler_IsCandy:
			B 		ShopImageHandler_Finish
			ADDIU 	v0, r0, 0

		ShopImageHandler_IsSnide:
			ADDIU 	v0, r0, 3

		ShopImageHandler_Finish:
			J 		0x80648370
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

	GiveItemPointerToMulti:
		LUI 	t8, hi(MultiBunchCount)
		ADDIU 	t8, t8, lo(MultiBunchCount)
		SW 		t8, 0x0 (s0)
		J 		0x806F8618
		SW 		t6, 0xC (s0)

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
.align 0x10
END_HOOK: