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