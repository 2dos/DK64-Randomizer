tns_pad_height_patch:
    lhu $t7, 0x46C0 ($t7)
    beql $t7, $zero, tns_pad_height_patch_finish
    addiu $t7, $zero, 1

    tns_pad_height_patch_finish:
        j 0x8064D8E8
        lui $at, 0x4F80

tns_pad_height_patch_0:
    lhu $t7, 0x46C0 ($t7)
    beql $t7, $zero, tns_pad_height_patch_0_finish
    addiu $t7, $zero, 1

    tns_pad_height_patch_0_finish:
        j 0x8064D9E0
        lh $a0, 0x3E ($sp)

scoff_patch:
    lhu $t9, 0x46C0 ($t9)
    beql $t9, $zero, scoff_patch_finish
    addiu $t9, $zero, 1

    scoff_patch_finish:
        j 0x806BE104
        lui $at, 0x4F80