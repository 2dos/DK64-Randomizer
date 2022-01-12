START_HOOK:
	NinWarpCode:
		JAL 	checkNinWarp
		NOP
		J 		0x807132CC
		NOP

	Jump_CrankyDecouple:
		J 		CrankyDecouple
		NOP

	PatchCrankyCode:
		LUI t3, hi(Jump_CrankyDecouple)
		LW t3, lo(Jump_CrankyDecouple) (t3)
		LUI t4, 0x8002
		SW t3, 0x60E0 (t4) // Store Hook
		SW r0, 0x60E4 (t4) // Store NOP
		JR 		ra
		NOP

	CrankyDecouple:
		BEQ		a0, t0, CrankyDecouple_Bitfield
		OR 		v1, a0, r0
		BEQZ 	a0, CrankyDecouple_Bitfield
		NOP

		CrankyDecouple_Progessive:
			J 		0x8002611C
			NOP

		CrankyDecouple_Bitfield:
			J 		0x800260F0
			NOP

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

.align 0x10
END_HOOK: