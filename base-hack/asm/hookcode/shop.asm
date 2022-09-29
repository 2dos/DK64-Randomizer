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