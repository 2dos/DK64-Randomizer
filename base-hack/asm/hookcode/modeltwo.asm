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
    ADDIU   at, r0, 0x48
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x28F
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x5B
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F2
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F3
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F5
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x1F6
    BEQ     v0, at, ObjectRotate_ApplyRotate
    ADDIU   at, r0, 0x59
    BEQ     v0, at, ObjectRotate_ApplyRotate
    NOP
    J       0x80637150
    NOP

    ObjectRotate_ApplyRotate:
        J       0x80637160
        NOP