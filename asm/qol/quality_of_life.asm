QOLChanges:
    SW      ra, @ReturnAddress
    LA      a0, QualityChangesOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, FinishQOL
    NOP

    // Remove DK Rap from startup
    FridgeHasBeenTaken:
        LI       a1, 0x50
        SB       a1, 0x807132BF // Set Destination Map after N/R Logos to Main Menu
        LI       a1, 5
        SB       a1, 0x807132CB // Set Gamemode after N/R Logos to Main Menu Mode

    // Story Skip set to "On" by default (not locked to On)
    StorySkip:
        LBU     a1, @Gamemode
        BNEZ    a1, QOLChanges_TrainingBarrels
        NOP
        LI      a1, 1
        SB      a1, @StorySkip

    // Training Barrels are pre spawned
    QOLChanges_TrainingBarrels:
        JAL     CodedSetPermFlag
        LI      a0, 0x309 // Cranky FTT
        JAL     CodedSetPermFlag
        LI      a0, 0x17F // Training Barrels Spawned

    FinishQOL:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

// QoL Changes that require the "Shorten Cutscenes" option to be on
QOLChangesShorten:
    SW          ra, @ReturnAddress
    LA          a0, QualityChangesOn
    LBU         a0, 0x0 (a0)
    BEQZ        a0, FinishQOLShorten
    NOP

    // Remove First Time Text
    NoFTT:
        LA      a0, FTTFlags
        JAL     SetAllFlags
        NOP

    NoDance:
        SW      r0, 0x806EFB9C // Movement Write
        SW      r0, 0x806EFC1C // CS Play
        SW      r0, 0x806EFB88 // Animation Write
        SW      r0, 0x806EFC0C // Change Rotation
        SW      r0, 0x806EFBA8 // Control State Progress

    // Remove First Time Boss Cutscenes
    ShortenBossCutscenes:
        LI      a1, @TempFlagBlock
        LI      a2, 0x803F // All Boss Cutscenes
        LHU     a3, 0xC (a1)
        OR      a2, a3, a2
        SH      a2, 0xC (a1)

    // Shorter Snides Cutscenes
    SnidesCutsceneCompression:
        // The cutscene the game chooses is based on the parent map (the method used to detect which Snide's H.Q. you're in)
        // The shortest contraption cutscene is chosen with parent map 0
        // So we swap out the original parent map with 0 at the right moment to get short cutscenes
        // Then swap the original value back in at the right moment so that the player isn't taken back to test map when exiting Snide's H.Q.
        LW      t0, @CurrentMap
        LI      t1, 0xF
        BNE     t0, t1, FinishQOLShorten
        NOP
        LHU     t0, @CutsceneIndex
        LI      t1, 5
        BEQ     t0, t1, SnidesCutsceneCompression_CS5
        NOP
        LI      t1, 2
        BEQ     t0, t1, SnidesCutsceneCompression_CS2
        NOP
        B       SnidesCutsceneCompression_TurnIn
        NOP

        SnidesCutsceneCompression_CS5:
            LHU     t0, @CutsceneTimer
            LI      t1, 199
            BEQ     t0, t1, SnidesCutsceneCompression_Time199
            NOP
            LI      t1, 200
            BEQ     t0, t1, SnidesCutsceneCompression_Time200
            NOP
            B       SnidesCutsceneCompression_TurnIn
            NOP

            SnidesCutsceneCompression_Time199:
                // Make a backup copy of the current parent map to restore later
                LHU     t2, @ParentMap
                SB      t2, @BackupParentMap
                B       SnidesCutsceneCompression_TurnIn
                NOP

            SnidesCutsceneCompression_Time200:
                // Set parent map to 0
                SH      r0, @ParentMap
                B       SnidesCutsceneCompression_TurnIn
                NOP

        SnidesCutsceneCompression_CS2:
            // Restore the backup copy of the parent map
            LBU     t2, @BackupParentMap
            SH      t2, @ParentMap

        SnidesCutsceneCompression_TurnIn:
            // Dereference the spawner array
            LW      t0, @ActorSpawnerArrayPointer
            BEQZ    t0, FinishQOLShorten // If there's no array loaded, don't bother
            NOP

            SnidesCutsceneCompression_TurnIn_Loop:
                // Find a snide entry (enemy type 7)
                LBU     t1, 0x0 (t0) // Get enemy type at slot 0
                LI      t2, 7 // Snide Enemy Type
                BNE     t1, t2, FinishQOLShorten
                NOP

                // Dereference the Snide Actor pointer from it
                LW      t0, 0x18 (t0)
                BEQZ    t0, FinishQOLShorten
                NOP

                // Read the turn count (Snide + 0x232)
                LBU     t1, 0x232 (t0)
                BEQZ    t1, FinishQOLShorten
                NOP
                LI      t2, 1
                SB      t2, 0x232 (t0)

    FinishQOLShorten:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
QualityChangesOn:
    .byte 1