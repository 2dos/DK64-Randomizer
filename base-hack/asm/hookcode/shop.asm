Jump_AlwaysCandyInstrument:
    j AlwaysCandyInstrument
    nop
Jump_CrankyDecouple:
    j CrankyDecouple
    nop
Jump_ForceToBuyMoveInOneLevel:
    j ForceToBuyMoveInOneLevel
    nop
Jump_MoveShow0:
    j FixInvisibleText_0
    nop
Jump_MoveShow1:
    j FixInvisibleText_1
    nop
Jump_PriceKongStore:
    j PriceKongStore
    nop
Jump_CharacterCollectableBaseModify:
    j CharacterCollectableBaseModify
    nop
Jump_SetMoveBaseBitfield:
    j SetMoveBaseBitfield
    nop
Jump_SetMoveBaseProgressive:
    j SetMoveBaseProgressive
    nop
Jump_CrankyCoconutDonation:
    j CrankyCoconutDonation
    nop
    
PatchCrankyCode:
    lui $t3, hi(Jump_CrankyDecouple)
    lw $t3, lo(Jump_CrankyDecouple) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x60E0 ($t4) ; Store Hook
    sw $zero, 0x60E4 ($t4) ; Store NOP

    lui $t3, hi(Jump_ForceToBuyMoveInOneLevel)
    lw $t3, lo(Jump_ForceToBuyMoveInOneLevel) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x60A8 ($t4) ; Store Hook
    sw $zero, 0x60AC ($t4) ; Store NOP
    sw $zero, 0x6160 ($t4) ; Store NOP to prevent loop

    lui $t3, hi(Jump_PriceKongStore)
    lw $t3, lo(Jump_PriceKongStore) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x6140(t4) ; Store Hook
    sw $zero, 0x6144 ($t4) ; Store NOP

    lui $t3, hi(Jump_CharacterCollectableBaseModify)
    lw $t3, lo(Jump_CharacterCollectableBaseModify) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x5FC0(t4) ; Store Hook
    sw $zero, 0x5FC4 ($t4) ; Store NOP

    lui $t3, hi(Jump_SetMoveBaseBitfield)
    lw $t3, lo(Jump_SetMoveBaseBitfield) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x60F0(t4) ; Store Hook
    sw $zero, 0x60F4 ($t4) ; Store NOP

    lui $t3, hi(Jump_SetMoveBaseProgressive)
    lw $t3, lo(Jump_SetMoveBaseProgressive) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x611C(t4) ; Store Hook
    sw $zero, 0x6120 ($t4) ; Store NOP

    lui $t3, hi(CurrentMap)
    lw $t3, lo(CurrentMap) ($t3)
    addiu $t4, $zero, 0x5
    beq $t3, $t4, PatchCrankyCode_Cranky
    nop

    lui $t3, hi(Jump_MoveShow0)
    lw $t3, lo(Jump_MoveShow0) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x7AE8 ($t4) ; Store Hook
    sw $zero, 0x7AEC ($t4) ; Store NOP

    lui $t3, hi(Jump_MoveShow1)
    lw $t3, lo(Jump_MoveShow1) ($t3)
    lui $t4, 0x8002
    sw $t3, 0x7B30 ($t4) ; Store Hook
    sw $zero, 0x7B34 ($t4) ; Store NOP

    b PatchCrankyCode_More
    nop

    PatchCrankyCode_Cranky:
        lui $t3, 0x8002
        addiu $t4, $zero, 300
        sh $t4, 0x7B72 ($t3)
        sh $t4, 0x7BCA ($t3)
        sh $t4, 0x7BFA ($t3)

        lui $t4, hi(Jump_CrankyCoconutDonation)
        lw $t4, lo(Jump_CrankyCoconutDonation) ($t4)
        lui $t3, 0x8002
        sw $t4, 0x6EFC ($t3)
        sw $zero, 0x6F00 ($t3)

    PatchCrankyCode_More:
        lui $t4, hi(Jump_AlwaysCandyInstrument)
        lw $t4, lo(Jump_AlwaysCandyInstrument) ($t4)
        lui $t3, 0x8002
        sw $t4, 0x6924 ($t3)
        sw $zero, 0x6928 ($t3)

        lui $t3, 0x8002
        addiu $t4, $zero, hi(CrankyMoves_New)
        sh $t4, 0x6072 ($t3)
        addiu $t4, $zero, lo(CrankyMoves_New)
        sh $t4, 0x607A ($t3)
        addiu $t4, $zero, hi(CandyMoves_New)
        sh $t4, 0x607E ($t3)
        addiu $t4, $zero, lo(CandyMoves_New)
        sh $t4, 0x6086 ($t3)
        addiu $t4, $zero, hi(FunkyMoves_New)
        sh $t4, 0x608A ($t3)
        addiu $t4, $zero, lo(FunkyMoves_New)
        sh $t4, 0x608E ($t3)

    jr ra
    nop

CrankyDecouple:
    beq $a0, $t0, CrankyDecouple_Bitfield
    or v1, $a0, $zero
    beqz $a0, CrankyDecouple_Bitfield
    nop

    CrankyDecouple_Progessive:
        j 0x800260E8
        nop

    CrankyDecouple_Bitfield:
        j 0x800260F0
        nop

ForceToBuyMoveInOneLevel:
    addu $t3, $t3, $t9
    sll $t3, $t3, 1
    lbu $t2, 0xC ($s2) ; Current Level
    sltiu $t1, $t2, 7
    beqz $t1, ForceToBuyMoveInOneLevel_Skip ; If level < 7 (In one of the main 7 levels, progress. Otherwise skip)
    nop
    sll $t1, $t2, 2
    subu $t1, $t1, $t2
    sll $t1, $t1, 1 ; Current Level * 6
    j 0x800260B4
    addu v1, v1, $t1

    ForceToBuyMoveInOneLevel_Skip:
        lui $s1, 0x8002
        sw $zero, 0x6194 ($s1)
        j 0x80026168
        addiu $s1, $zero, 0

AlwaysCandyInstrument:
    ; Candy
    lui $at, 0x8080
    lw $at, 0xBB40 ($at)
    lw $t9, 0x58 ($at)
    addiu $at, $zero, 191
    beq $t9, $at, AlwaysCandyInstrument_IsCandy
    addiu $t9, $zero, 4
    ; Funky
    lui $at, 0x8080
    lw $at, 0xBB40 ($at)
    lw $t9, 0x58 ($at)
    addiu $at, $zero, 190
    beq $t9, $at, AlwaysCandyInstrument_IsCandy
    addiu $t9, $zero, 2
    ; Cranky
    lui $at, 0x8080
    lw $at, 0xBB40 ($at)
    lw $t9, 0x58 ($at)
    addiu $at, $zero, 189
    beq $t9, $at, AlwaysCandyInstrument_IsCandy
    addiu $t9, $zero, 0
    ; Default
    lbu $t9, 0xB ($s0)
    
    AlwaysCandyInstrument_IsCandy:
        j 0x8002692C
        sltiu $at, $t9, 0x5

FixInvisibleText_0:
    lw $a0, 0xC4 ($sp)
    addiu $t8, $zero, 0x82
    sw $t8, 0x90 ($a0)
    addiu $a0, $sp, 0x3C
    j 0x80027AF0
    sll $t8, $t7, 5

FixInvisibleText_1:
    lw v0, 0xC4 ($sp)
    addiu $a1, $zero, 0x82
    sw $a1, 0x90 (v0)
    or v0, $zero, $zero
    j 0x80027B38
    addiu $a1, $sp, 0x3C

PriceKongStore:
    ; Stores price & kong correctly
    ; 0x80026140
    lh v0, 0x4 ($a1)
    sh v0, 0x4 ($s2)
    andi $t8, v0, 0xFF
    j 0x8002614C
    sh $t8, 0x0 ($t2)

CharacterCollectableBaseModify:
    ; Replaces param2 with the start of the character collectable base
    ; 0x80025FC0
    or $s2, $a0, $zero
    lui $a1, hi(MovesBase)
    addiu $a1, $a1, lo(MovesBase)
    j 0x80025FC8
    or $s3, $a1, $zero

SetMoveBaseBitfield:
    ; Sets the move base to the correct kong (Bitfield)
    ; 0x800260F0
    lh $t4, 0x2 ($a1)
    addu $t8, $s3, $a0
    lbu $t9, 0x4 ($a1)
    addiu $t6, $zero, 0x5E
    mult $t9, $t6
    mflo $t9
    j 0x800260F8
    addu $t8, $t8, $t9

SetMoveBaseProgressive:
    ; Sets the move base to the correct kong (Progressive)
    ; 0x8002611C
    lbu $t6, 0x4 ($a1)
    addiu $t5, $zero, 0x5E
    mult $t6, $t5
    mflo $t6
    addu $t4, $t4, $t6
    lbu $t6, 0x0 ($t4)
    j 0x80026124
    lh $t5, 0x2 ($a1)

ShopImageHandler:
    jal 0x807149B8
    addiu $a0, $zero, 1
    lh v0, 0x4A ($sp)
    lw $t2, 0x44 ($sp)
    addiu $at, $zero, 0x90
    multu $t2, $at
    mflo $at
    lui $t2, hi(ObjectModel2Pointer)
    lw $t2, lo(ObjectModel2Pointer) ($t2)
    addu $t2, $t2, $at
    lhu $t2, 0x84 ($t2) ; Object Type
    addiu $at, $zero, 0x73
    beq $t2, $at, ShopImageHandler_IsCranky
    nop
    addiu $at, $zero, 0x7A
    beq $t2, $at, ShopImageHandler_IsFunky
    nop
    addiu $at, $zero, 0x124
    beq $t2, $at, ShopImageHandler_IsCandy
    nop
    addiu $at, $zero, 0x79
    beq $t2, $at, ShopImageHandler_IsSnide
    nop
    b ShopImageHandler_Finish
    nop

    ShopImageHandler_IsCranky:
        b ShopImageHandler_Finish
        addiu v0, $zero, 1
        
    ShopImageHandler_IsFunky:
        b ShopImageHandler_Finish
        addiu v0, $zero, 2

    ShopImageHandler_IsCandy:
        b ShopImageHandler_Finish
        addiu v0, $zero, 0

    ShopImageHandler_IsSnide:
        addiu v0, $zero, 3

    ShopImageHandler_Finish:
        j 0x80648370
        nop

CrankyCoconutDonation:
    beq $at, $v1, CrankyCoconutDonation_Funky
    addiu $t5, $zero, 0x2
    addiu $at, $zero, 0xBD ; Cranky Actor index
    bne $at, $v1, CrankyCoconutDonation_Candy ; Not Cranky Actor
    nop
    lw  $t6, 0x24 ($sp)
    addiu $t7, $zero, 5 ; Crystal Coconuts
    sw $t7, 0x24 ($sp)
    addiu $t7, $zero, 8 ; Text File
    addiu $t8, $zero, 0x24 ; Text Index 
    sw $t7, 0x2c ($sp)
    sw $t8, 0x28 ($sp) 
    j 0x80026F4C
    addiu $v0, $zero, 0 ; Move Type 0

    CrankyCoconutDonation_Candy:
        j 0x80026F08
        addiu $at, $zero, 0xBF

    CrankyCoconutDonation_Funky:
        j 0x80026F18
        addiu $t5, $zero, 0x2