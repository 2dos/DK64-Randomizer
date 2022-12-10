Jump_RemoveKrazyKKLagImpact:
    j RemoveKrazyKKLagImpact
    nop

PatchBonusCode:
    lui $t3, hi(Jump_RemoveKrazyKKLagImpact)
    lw $t3, lo(Jump_RemoveKrazyKKLagImpact) ($t3)
    lui $t4, 0x8003
    sw $t3, 0x95D4 ($t4)
    jr ra
    sw $zero, 0x95D8 ($t4)

RemoveKrazyKKLagImpact:
    lh $t4, 0x0 ($t0)
    lui $t5, hi(StoredLag)
    lhu $t5, lo(StoredLag) ($t5)
    j 0x800295DC
    subu $t5, $t4, $t5