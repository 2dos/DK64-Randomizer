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