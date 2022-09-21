FileScreenDLCode_Jump:
    J 		FileScreenDLCode
    NOP
FileSelectDLCode_Jump:
    J 		FileSelectDLCode
    NOP

FileScreenDLCode_Write:
    LUI t3, hi(FileScreenDLCode_Jump)
    LW t3, lo(FileScreenDLCode_Jump) (t3)
    LUI t4, 0x8003
    SW t3, 0x937C (t4) // Store Hook
    SW r0, 0x9380 (t4) // Store NOP

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