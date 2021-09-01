.align
// Enable Tag Anywhere - OPTIONAL
TagAnywhere:
    SW      ra, @ReturnAddress
    LA      a0, TagAnywhereOn
    LBU     a0, 0x0 (a0)
    BEQZ    a0, TagAnywhere_Finish
    NOP
    LBU     a0, @Character
    SLTIU   a0, a0, 5
    BEQZ    a0, TagAnywhere_Finish
    NOP
    LH      a1, @NewlyPressedControllerInput
    ANDI    a2, a1, @D_Left
    BNEZ    a2, TagAnywhere_CheckHUD
    LI      t0, -1
    ANDI    a2, a1, @D_Right
    BNEZ    a2, TagAnywhere_CheckHUD
    LI      t0, 1
    B       TagAnywhere_Finish
    NOP

    TagAnywhere_CheckHUD:
        LW      a0, @HUDPointer
        BEQZ    a0, TagAnywhere_Finish
        NOP
        LW      a1, 0x20 (a0) // CB
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x50 (a0) // Coins
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x1A0 (a0) // GB Count (Not Bottom)
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x200 (a0) // Medals 
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x260 (a0) // Blueprint
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x290 (a0) // CB?
        BNEZ    a1, TagAnywhere_Finish
        NOP
        LW      a1, 0x2C0 (a0) // Coins?
        BNEZ    a1, TagAnywhere_Finish
        NOP

    TagAnywhere_CheckBullets:
        LHU     a0, @LoadedActorCount
        BEQZ    a0, TagAnywhere_Finish
        NOP
        LI      a1, @LoadedActorArray

    TagAnywhere_CheckBullet_Loop:
        LW      t3, 0x0 (a1)
        LW      a2, 0x58 (t3)
        LI      a3, 36 // Peanut
        BEQ     a2, a3, TagAnywhere_CheckBullet_Stuck
        LI      a3, 38 // Pineapple
        BEQ     a2, a3, TagAnywhere_CheckBullet_Stuck
        LI      a3, 42 // Grape
        BEQ     a2, a3, TagAnywhere_CheckBullet_Stuck
        LI      a3, 43 // Feather
        BEQ     a2, a3, TagAnywhere_CheckBullet_Stuck
        LI      a3, 48 // Coconut
        BEQ     a2, a3, TagAnywhere_CheckBullet_Stuck
        NOP
        B       TagAnywhere_CheckBullet_Next
        NOP

    TagAnywhere_CheckBullet_Stuck:
        LBU     a2, 0x154 (t3)
        BEQZ    a2, TagAnywhere_Finish // Bullet hasn't touched object (feathers)
        NOP

    TagAnywhere_CheckBullet_Next:
        ADDI    a0, a0, -1
        BEQZ    a0, TagAnywhere_ChangeCharacter // All items checked
        NOP
        B       TagAnywhere_CheckBullet_Loop
        ADDIU   a1, a1, 8

    TagAnywhere_ChangeCharacter:
        LW      a0, @CurrentMap
        LA      t3, TagAnywhereBan

    TagAnywhere_MapLoop:
        LBU     a2, 0x0 (t3)
        BEQZ    a2, TagAnywhere_IsChanging
        NOP
        BEQ     a0, a2, TagAnywhere_Finish
        NOP
        B       TagAnywhere_MapLoop
        ADDIU   t3, t3, 1

    TagAnywhere_IsChanging:
        LBU     a2, @Character
        LI      a3, 5

    TagAnywhere_CharacterLoop:
        LI      t3, 1
        BEQ     t0, t3, TagAnywhere_Add // Inc Kong
        NOP
        BEQZ    a2, WrapAround_Neg
        NOP
        B       UnlockCheck
        ADDI    a2, a2, -1

    TagAnywhere_Add:
        SLTIU   t8, a2, 4
        BEQZ    t8, WrapAround_Pos
        NOP
        B       UnlockCheck
        ADDIU   a2, a2, 1 // New Character Value

    WrapAround_Neg:
        B       UnlockCheck
        LI      a2, 4

    WrapAround_Pos:
        LI      a2, 0

    UnlockCheck:
        LA      a0, KongTagAnywhereFlags
        SLL     t3, a2, 1
        ADD     a0, a0, t3
        LI      a1, 0
        LH      a0, 0x0 (a0)
        SW      t0, @VarStorage0
        SW      a3, @VarStorage1
        SW      a2, @VarStorage2
        JAL     @CheckFlag
        NOP
        LW      a2, @VarStorage2
        LW      a3, @VarStorage1
        LW      t0, @VarStorage0
        ADDIU   a0, v0, 0
        ADDI    a3, a3, -1
        SW      a3, @TestVariable
        BEQZ    a3, TagAnywhere_Finish
        NOP
        BEQZ    a0, TagAnywhere_CharacterLoop
        NOP

    GunCheck:
        LW      a1, @Player
        BEQZ    a1, TagAnywhere_Finish // If player isn't in RDRAM, cancel
        NOP
        LA      a3, GunBitfields
        SLL     t3, a2, 2 // new_kong x 4
        ADD     a3, t3, a3
        LW      a3, 0x0 (a3)
        LBU     t9, 0x0 (a3) // Get gun bitfield for kong
        ANDI    t9, t9, 1 // Has gun
        BEQZ    t9, RetractGun
        NOP
        LBU     t9, 0x20C(a1) // Was gun out
        BEQZ    t9, RetractGun
        NOP

    PullOutGun:
        LA      t9, HandStatesGun
        ADD     t9, t9, a2
        LBU     t9, 0x0 (t9)
        SB      t9, 0x147 (a1) // Set Hand State
        LI      t9, 1
        B       ChangeCharacter
        SB      t9, 0x20C (a1) // Set Gun State

    RetractGun:
        LA      t9, HandStatesNoGun
        ADD     t9, t9, a2
        LBU     t9, 0x0 (t9)
        SB      t9, 0x147 (a1) // Set Hand State
        SB      r0, 0x20C (a1) // Set Gun State

    ChangeCharacter:
        LW      a1, @Player
        BEQZ    a1, TagAnywhere_Finish // If player isn't in RDRAM, cancel
        ADDIU   a2, a2, 2
        SB      a2, 0x36F (a1)
        LW      a1, @SwapObject
        BEQZ    a1, TagAnywhere_Finish // If swap object isn't in RDRAM, cancel
        LI      a2, 0x3B
        SH      a2, 0x29C (a1) // Initiate Swap

    TagAnywhere_Finish:
        LW      ra, @ReturnAddress
        JR      ra
        NOP

.align
TagAnywhereBan:
// Credit: Isotarge
// Tag Anywhere Dedicated Mod: https://pastebin.com/m82XBvYm
    .byte 1 // Funky's Store
    .byte 2 // DK Arcade
    .byte 3 // K. Rool Barrel: Lanky's Maze
    .byte 5 // Cranky's Lab
    .byte 6 // Jungle Japes: Minecart
    .byte 9 // Jetpac
    .byte 10 // Kremling Kosh! (very easy)
    .byte 14 // Angry Aztec: Beetle Race // Note: Softlock at the end if enabled?
    .byte 15 // Snide's H.Q.
    .byte 18 // Teetering Turtle Trouble! (very easy)
    .byte 25 // Candy's Music Shop
    .byte 27 // Frantic Factory: Car Race
    .byte 31 // Gloomy Galleon: K. Rool's Ship // TODO: Test
    .byte 32 // Batty Barrel Bandit! (easy)
    .byte 35 // K. Rool Barrel: DK's Target Game
    .byte 37 // Jungle Japes: Barrel Blast // Note: The barrels don't work as other kongs so not much point enabling it on this map
    .byte 41 // Angry Aztec: Barrel Blast
    .byte 42 // Troff 'n' Scoff
    .byte 50 // K. Rool Barrel: Tiny's Mushroom Game
    .byte 54 // Gloomy Galleon: Barrel Blast
    .byte 55 // Fungi Forest: Minecart
    .byte 76 // DK Rap
    .byte 77 // Minecart Mayhem! (easy)
    .byte 78 // Busy Barrel Barrage! (easy)
    .byte 79 // Busy Barrel Barrage! (normal)
    .byte 80 // Main Menu
    .byte 82 // Crystal Caves: Beetle Race
    .byte 83 // Fungi Forest: Dogadon
    .byte 101 // Krazy Kong Klamour! (easy) // Note: Broken with switch kong
    .byte 102 // Big Bug Bash! (very easy) // Note: Broken with switch kong
    .byte 103 // Searchlight Seek! (very easy) // Note: Broken with switch kong
    .byte 104 // Beaver Bother! (easy) // Note: Broken with switch kong
    .byte 106 // Creepy Castle: Minecart
    .byte 110 // Frantic Factory: Barrel Blast
    .byte 111 // Gloomy Galleon: Pufftoss
    .byte 115 // Kremling Kosh! (easy)
    .byte 116 // Kremling Kosh! (normal)
    .byte 117 // Kremling Kosh! (hard)
    .byte 118 // Teetering Turtle Trouble! (easy)
    .byte 119 // Teetering Turtle Trouble! (normal)
    .byte 120 // Teetering Turtle Trouble! (hard)
    .byte 121 // Batty Barrel Bandit! (easy)
    .byte 122 // Batty Barrel Bandit! (normal)
    .byte 123 // Batty Barrel Bandit! (hard)
    .byte 131 // Busy Barrel Barrage! (hard)
    .byte 136 // Beaver Bother! (normal)
    .byte 137 // Beaver Bother! (hard)
    .byte 138 // Searchlight Seek! (easy)
    .byte 139 // Searchlight Seek! (normal)
    .byte 140 // Searchlight Seek! (hard)
    .byte 141 // Krazy Kong Klamour! (normal)
    .byte 142 // Krazy Kong Klamour! (hard)
    .byte 143 // Krazy Kong Klamour! (insane)
    .byte 144 // Peril Path Panic! (very easy) // Note: Broken with switch kong
    .byte 145 // Peril Path Panic! (easy)
    .byte 146 // Peril Path Panic! (normal)
    .byte 147 // Peril Path Panic! (hard)
    .byte 148 // Big Bug Bash! (easy)
    .byte 149 // Big Bug Bash! (normal)
    .byte 150 // Big Bug Bash! (hard)
    .byte 165 // K. Rool Barrel: Diddy's Kremling Game
    .byte 185 // Enguarde Arena // Note: Handled by character check
    .byte 186 // Creepy Castle: Car Race
    .byte 187 // Crystal Caves: Barrel Blast
    .byte 188 // Creepy Castle: Barrel Blast
    .byte 189 // Fungi Forest: Barrel Blast
    .byte 190 // Kong Battle: Arena 2 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
    .byte 191 // Rambi Arena // Note: Handled by character check
    .byte 192 // Kong Battle: Arena 3 // TODO: Would be really cool to get multiplayer working, currently just voids you out when activated
    .byte 198 // Training Grounds (End Sequence) // Note: Handled by cutscene check
    .byte 199 // Creepy Castle: King Kut Out // Note: Doesn't break the kong order but since this fight is explicitly about tagging we might as well disable
    .byte 201 // K. Rool Barrel: Diddy's Rocketbarrel Game
    .byte 202 // K. Rool Barrel: Lanky's Shooting Game
    .byte 203 // K. Rool Fight: DK Phase // Note: Enabling here breaks the fight and may cause softlocks
    .byte 204 // K. Rool Fight: Diddy Phase // Note: Enabling here breaks the fight and may cause softlocks
    .byte 205 // K. Rool Fight: Lanky Phase // Note: Enabling here breaks the fight and may cause softlocks
    .byte 206 // K. Rool Fight: Tiny Phase // Note: Enabling here breaks the fight and may cause softlocks
    .byte 207 // K. Rool Fight: Chunky Phase // Note: Enabling here breaks the fight and may cause softlocks
    .byte 208 // Bloopers Ending // Note: Handled by cutscene check
    .byte 209 // K. Rool Barrel: Chunky's Hidden Kremling Game
    .byte 210 // K. Rool Barrel: Tiny's Pony Tail Twirl Game
    .byte 211 // K. Rool Barrel: Chunky's Shooting Game
    .byte 212 // K. Rool Barrel: DK's Rambi Game
    .byte 213 // K. Lumsy Ending // Note: Handled by cutscene check
    .byte 214 // K. Rool's Shoe
    .byte 215 // K. Rool's Arena // Note: Handled by cutscene check?
    .byte 0 // NULL TERMINATOR (ends loop)

.align
TagAnywhereOn:
    .byte 1