.org 0x805DAE00
// Randomize Level Progression
RandoLevelOrder:
    LA      a0, RandoOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, FinishSettingLZs
    NOP
    // Grab LZ Array (Size: 0x3A, Type: 0x10_u16, DMap: 0x12_u16, DExit: 0x14_dexit)
    LW      a0, @LZArray
    BEQZ    a0, FinishSettingLZs
    NOP
    LW      a1, @ObjectTimer
    LI      a2, 3
    BNE     a1, a2, FinishSettingLZs
    NOP
    LHU     a1, @LZSize
    LW      a2, @CurrentMap

    RandoLoop:
        // Lobby Entrances
        LA      t6, Lobbies
        LI      a3, 0x22 // Isles
        BNE     a2, a3, Exit
        LI      a3, 9 // Type
        LHU     t9, 0x10 (a0)
        BNE     t9, a3, LoopControl
        LI      t3, 0

        EntranceSearch:
            LA      t6, Lobbies
            ADD     t6, t6, t3
            LBU     t6, 0x0 (t6)
            LHU     t9, 0x12 (a0)
            BEQ     t6, t9, EntranceFound // t3 = lobby index
            NOP
            LI      t9, 7
            BEQ     t3, t9, LoopControl // Lobby index not found
            NOP
            B       EntranceSearch
            ADDIU   t3, t3, 1

        EntranceFound:
            LA      t6, LevelOrder
            ADD     t6, t6, t3
            LBU     t6, 0x0 (t6) // New Index
            LA      t3, Lobbies
            ADD     t3, t3, t6
            LBU     t3, 0x0 (t3) // New Lobby
            B       LoopControl
            SH      t3, 0x12 (a0)

        // Lobby Exits
        Exit:
            LHU     t9, 0x12 (a0)
            LI      a3, 0x22 // Isles
            BNE     t9, a3, LoopControl
            LI      a3, 9 // Type
            LHU     t9, 0x10 (a0)
            BNE     t9, a3, LoopControl
            LI      t3, 0

        ExitSearch:
            LA      t6, Lobbies
            ADD     t6, t6, t3
            LBU     t6, 0x0 (t6)
            LW      t9, @CurrentMap
            BEQ     t6, t9, ExitFound // t3 = lobby index
            NOP
            LI      t9, 7
            BEQ     t3, t9, LoopControl // Lobby not found
            NOP
            ADDIU   t3, t3, 1
            B       ExitSearch
            NOP

        ExitFound:
            LI      t9, 0

        ExitFoundSearch:
            // t3 = Found Lobby
            // t9 = Index in Level Order
            LA      t6, LevelOrder
            ADD     t6, t6, t9
            LBU     t6, 0x0 (t6) // Source Index
            BEQ     t6, t3, ExitFoundIndexFound
            NOP
            LI      t6, 7
            BEQ     t9, t6, LoopControl // Index not found
            NOP
            ADDIU   t9, t9, 1
            B       ExitFoundSearch
            NOP

        ExitFoundIndexFound:
            LA      t3, LobbyExits
            ADD     t3, t3, t9
            LBU     t3, 0x0 (t3) // Found Exit Value
            SH      t3, 0x14 (a0)

        // Loop Control
        LoopControl:
            ADDI    a1, a1, -1
            BEQZ    a1, CastleCannon
            ADDIU   a0, a0, 0x3A
            B       RandoLoop
            NOP

    CastleCannon:
        LW      a0, @CurrentMap
        LI      a1, 0x22
        BNE     a0, a1, FinishSettingLZs
        NOP
        LW      a0, @CastleCannonPointer
        BEQZ    a0, FinishSettingLZs
        SRA     a1, a0, 16
        SLTIU   a2, a1, 0x8000
        BNEZ    a2, FinishSettingLZs
        SLTIU   a2, a1, 0x8080
        BEQZ    a2, FinishSettingLZs
        NOP
        LHU     a1, 0x376 (a0)
        LI      a2, 0x22
        BNE     a1, a2, FinishSettingLZs
        NOP
        LA      a1, LevelOrder
        LBU     a1, 0x6 (a1) // Castle Cannon Lobby Index
        LA      a2, Lobbies
        ADD     a2, a2, a1
        LBU     a2, 0x0 (a2) // Cannon Map
        SH      a2, 0x378 (a0)

    // We are going with randomized level lobby entrances
        // Values of lobby entrances
        // Values of lobby exits
        // Determine level order from randomized array in python script
            // Each level would need its B Locker value, T&S value and Key value adjusted to
            // what level number it is

    FinishSettingLZs:
        JR      ra
        NOP

// Swap B. Locker/Cheat Code/T&S counts
SwapRequirements:
    LA      a0, RandoOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, SwapRequirements_Finish
    NOP
    LBU     a0, @TransitionSpeed
    ANDI    a0, a0, 0x80
    BEQZ    a0, SwapRequirements_Finish
    NOP
    LW      t0, @CurrentMap
    LI      t3, @LevelIndexMapping
    ADD     t3, t3, t0
    LBU     t0, 0x0 (t3) // Level Index
    LI      t3, 7
    LA      a0, TroffNScoffAmounts
    LA      a1, BLockerDefaultAmounts
    LA      a2, BLockerCheatAmounts
    BEQ     t0, t3, SwapRequirements_InIsles
    NOP

    SwapRequirements_NotInIsles:
        LA      a3, KeyFlags_Normal
        LI      t3, 0
        B       SwapRequirements_Loop
        LI      t7, 8

    SwapRequirements_InIsles:
        LA      a3, KeyFlags
        LI      t3, 0
        LI      t7, 8

    SwapRequirements_Loop:
        // T&S
        LI      t9, @TroffNScoffReqArray
        SLL     t6, t3, 1
        ADD     t9, t9, t6
        LHU     t6, 0x0 (a0)
        SH      t6, 0x0 (t9)
        // B. Locker Default
        LI      t9, @BLockerDefaultArray
        SLL     t6, t3, 1
        ADD     t9, t9, t6
        LHU     t6, 0x0 (a1)
        SH      t6, 0x0 (t9)
        // B. Locker Cheat
        LI      t9, @BLockerCheatArray
        SLL     t6, t3, 1
        ADD     t9, t9, t6
        LHU     t6, 0x0 (a2)
        SB      t6, 0x0 (t9)
        // Keys - Boss Door
        SLTIU   t0, t7, 2
        BNEZ    t0, SwapRequirements_Increment
        NOP
        LI      t9, @CheckmarkKeyArray
        SLL     t6, t3, 1
        ADD     t9, t9, t6
        LHU     t6, 0x0 (a3)
        SH      t6, 0x0 (t9)

    SwapRequirements_Increment:
        // Loop
        ADDI    t7, t7 -1
        BEQZ    t7, SwapRequirements_Finish
        ADDIU   a0, a0, 2
        ADDIU   a1, a1, 2
        ADDIU   a2, a2, 2
        ADDIU   a3, a3, 2
        B       SwapRequirements_Loop
        ADDIU   t3, t3, 1

    SwapRequirements_Finish:
        JR      ra
        NOP