ObjectRotate:
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x288
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x90
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x18D
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x13C
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDE
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xE0
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xE1
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDD
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0xDF
    BEQ     v0, at, ObjectRotate_ApplyRotate
    NOP
    J       0x80637150
    NOP

    ObjectRotate_ApplyRotate:
        J       0x80637160
        NOP
        