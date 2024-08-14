.include "asm/functions/actor.asm"
.include "asm/functions/arcade.asm"
.include "asm/functions/graphics.asm"
.include "asm/functions/items.asm"
.include "asm/functions/math.asm"
.include "asm/functions/media.asm"
.include "asm/functions/modeltwo.asm"
.include "asm/functions/sprite.asm"
.include "asm/functions/system.asm"
.include "asm/functions/warp.asm"

.include "asm/variables/actor.asm"
.include "asm/variables/hack.asm"
.include "asm/variables/heap.asm"
.include "asm/variables/modeltwo.asm"
.include "asm/variables/static.asm"

//vanilla data
.definelabel __osActiveQueue, 0x800100EC
.definelabel TransitionSpeed, 0x807FD88C
.definelabel CutsceneWillPlay, 0x8075533B
.definelabel KRoolRound, 0x80750AD4
.definelabel MovesBase, 0x807FC950 // End: 0x807FCB28
.definelabel PlayerOneColor, 0x807552F4
.definelabel Mode, 0x80755318
.definelabel TBVoidByte, 0x807FBB63
.definelabel CurrentMap, 0x8076A0A8
.definelabel PreviousMap, 0x8076AEF2
.definelabel DestMap, 0x807444E4
.definelabel DestExit, 0x807444E8
.definelabel StorySkip, 0x8074452C
.definelabel HelmTimerShown, 0x80755350 // u8
.definelabel TempFlagBlock, 0x807FDD90
.definelabel SubmapData, 0x8076A160
.definelabel HelmTimerPaused, 0x80713C9B // u8
.definelabel PauseTextPointer, 0x807FC7E0
.definelabel LevelNamesPointer, 0x807FC7E8
.definelabel LagBoost, 0x80744478 // u32
.definelabel FrameLag, 0x8076AF10
.definelabel FrameReal, 0x80767CC4
.definelabel RNG, 0x80746A40 // u32
.definelabel BetaNinRWSkip, 0x80755324 // u8
.definelabel LogosDestMap, 0x807132BF // u8
.definelabel LogosDestMode, 0x807132CB // u8
.definelabel Gamemode, 0x80755314 // u8

.definelabel MapVoid_MinX, 0x807F5FE4
.definelabel MapVoid_MinZ, 0x807F5FE6
.definelabel MapVoid_MaxX, 0x807F5FE8
.definelabel MapVoid_MaxZ, 0x807F5FEA
.definelabel CutsceneIndex, 0x807476F4
.definelabel CutsceneActive, 0x807444EC
.definelabel CutsceneTimer, 0x807476F0
.definelabel CutsceneTypePointer, 0x807476FC
.definelabel PreviousCameraState, 0x807F5CF0
.definelabel CurrentCameraState, 0x807F5CF2
.definelabel CameraStateChangeTimer, 0x807F5CEC
.definelabel CutsceneStateBitfield, 0x807F5CF4
.definelabel AutowalkPointer, 0x807FD70C
.definelabel IsAutowalking, 0x807463B8
.definelabel PositionWarpInfo, 0x807FC918 // WarpInfo Struct
.definelabel PositionWarpBitfield, 0x8076AEE2
.definelabel PositionFloatWarps, 0x8076AEE4 // f32 x 3
.definelabel PositionFacingAngle, 0x8076AEF0 // u16
.definelabel ChimpyCam, 0x80744530
.definelabel ScreenRatio, 0x807444C0
.definelabel SoundType, 0x80745844
.definelabel LastSpawnedActor, 0x807FBB44
.definelabel CurrentActorPointer_0, 0x807FBB40
.definelabel LoadedActorCount, 0x807FBB35
.definelabel LoadedActorArray, 0x807FB930
.definelabel SpawnerMasterData, 0x807FDC88
.definelabel MenuSkyTopRGB, 0x80754F4C
.definelabel MenuSkyRGB, 0x80754F4F
.definelabel SkyboxBlends, 0x80754EF8
.definelabel ActorArray, 0x807FBFF0
.definelabel ActorCount, 0x807FC3F0
.definelabel ButtonsEnabledBitfield, 0x80755308
.definelabel JoystickEnabledX, 0x8075530C
.definelabel JoystickEnabledY, 0x80755310
.definelabel MapState, 0x8076A0B1
.definelabel ControllerInput, 0x80014DC4
.definelabel NewlyPressedControllerInput, 0x807ECD66
.definelabel Player, 0x807FBB4C
.definelabel SwapObject, 0x807FC924
.definelabel Character, 0x8074E77C
.definelabel Camera, 0x807FB968
.definelabel ISGActive, 0x80755070
.definelabel ISGTimestampMajor, 0x807F5CE0
.definelabel ISGTimestampMinor, 0x807F5CE4
.definelabel ISGPreviousFadeout, 0x807F5D14
.definelabel CurrentTimestampMajor, 0x80014FE0
.definelabel CurrentTimestampMinor, 0x80014FE4
.definelabel ISGFadeoutArray, 0x80747708
.definelabel CollectableBase, 0x807FCC40
.definelabel TransitionProgress, 0x807ECC60 // u8
.definelabel BackgroundHeldInput, 0x807ECD40 // u32
.definelabel PauseTimestampMajor, 0x807445C0 // u32
.definelabel PauseTimestampMinor, 0x807445C4 // u32
.definelabel HelmStartTimestampMajor, 0x80755340 // u32
.definelabel HelmStartTimestampMinor, 0x80755344 // u32
.definelabel HelmStartTime, 0x8075534C // u32
.definelabel HelmCurrentTime, 0x80755348 // u32
.definelabel p1PressedButtons, 0x807ECD48
.definelabel p1HeldButtons, 0x807ECD58
.definelabel player_count, 0x807FC928
.definelabel FocusedPlayerIndex, 0x807FC929
.definelabel sprite_table, 0x80755390
.definelabel sprite_translucency, 0x807FC80F
.definelabel bbbandit_array, 0x8002DB80
.definelabel StoredDamage, 0x807FCC4D // s8
.definelabel ActorSpawnerPointer, 0x807FC400 // u32 ptr
.definelabel DebugInfoOn, 0x807563B4 // u8
.definelabel CutsceneFadeActive, 0x8075533B // u8
.definelabel CutsceneFadeIndex, 0x8075533E // u16
.definelabel PreviouslyPressedButtons, 0x807ECD60 // u32
.definelabel heap_pointer, 0x807F0990 // ptr
.definelabel stickX_magnitude, 0x807FD640 // u8
.definelabel stickY_magnitude, 0x807FD641 // u8
.definelabel phasewalk_stickmagnitude, 0x807FD614 // f32
.definelabel fairy_data, 0x807FD802
.definelabel transferredActorType, 0x807FD570 // u16
.definelabel characterSpawnerActors, 0x8075EB80 // array with struct
.definelabel levelIndexMapping, 0x807445E0
.definelabel stickX_interpretted, 0x807FD63E
.definelabel stickY_interpretted, 0x807FD63F
.definelabel preventSongPlaying, 0x80745650
.definelabel parentDataCount, 0x807F5A68
.definelabel parentData, 0x8076A160
.definelabel SetupFilePointer, 0x807F6010
.definelabel focusedParentDataSetup, 0x807F5A70
.definelabel HUD, 0x80754280
.definelabel HelmMinigameFlags, 0x8074E7E0
.definelabel textData, 0x80754A34
.definelabel textCharData, 0x80754A18
.definelabel textUnkData, 0x807549FC
.definelabel LZFadeoutProgress, 0x807FD888
.definelabel mapFloorPointer, 0x807F9514
.definelabel mapFloorBlockCount, 0x807F9518
.definelabel displayListCount, 0x8076A088
.definelabel TransitionType, 0x8076AEE0
.definelabel DKTVKong, 0x80755328
.definelabel CutsceneBanks, 0x807F5B10
.definelabel QueuedCutsceneFunctions, 0x807452A0
.definelabel ActorTimer, 0x8076A068
.definelabel EEPROMType, 0x807EDEAC

.definelabel ExitPointer, 0x807FC900
.definelabel ExitCount, 0x807FC904

.definelabel screenCenterX, 0x80744490
.definelabel screenCenterY, 0x80744494
.definelabel collisionPos, 0x807F621C
.definelabel FileIndex, 0x807467C8
.definelabel LockStackCount, 0x807F5A68
.definelabel CutsceneBarState, 0x8076A0B3

.definelabel PathData, 0x807FDBF8
.definelabel MapProperties, 0x807FBB64

.definelabel TriggerArray, 0x807FDCB4
.definelabel TriggerSize, 0x807FDCB0
.definelabel CastleCannonPointer, 0x807F5BE8
.definelabel KongFlagArray, 0x807505B0
.definelabel MainMenuMoves, 0x80033938
.definelabel DataIsCompressed, 0x80748E18
.definelabel WorldArray, 0x8074809C
.definelabel WorldExitArray, 0x807480AC
.definelabel WorldCutsceneArray, 0x807480BC
.definelabel LobbiesArray, 0x80744734
.definelabel RaceExitArray, 0x807447A0
.definelabel BossMapArray, 0x80744700
.definelabel BossKongArray, 0x807446F0
.definelabel KutOutKongArray, 0x80035B44
.definelabel EnemyDropsTable, 0x80750400
.definelabel scriptLoadedArray, 0x807F60B0
.definelabel scriptsLoaded, 0x807F60A8
.definelabel scriptLoadsAttempted, 0x807F7140
.definelabel BonusBarrelData, 0x80755F4C
.definelabel ArenaScore, 0x80744518

.definelabel KongUnlockedMenuArray, 0x80033804
.definelabel FilePercentage, 0x80033F51
.definelabel FileGBCount, 0x8003380C
.definelabel FileScreenDLOffset, 0x80033F4C
.definelabel GBDictionary, 0x80755A20
.definelabel DKTVData, 0x8075E5C0
.definelabel KongModelData, 0x8075C410
.definelabel TagModelData, 0x8074E814
.definelabel RollingSpeeds, 0x80753568
.definelabel KongTagNames, 0x8074E85C
.definelabel KrazyKKModels, 0x8002D8C8
.definelabel ChargeVelocities_0, 0x8075380C
.definelabel ChargeVelocities_1, 0x8075381C
.definelabel ChargeDeceleration, 0x8075382C
.definelabel KongTextNames, 0x8074E780

.definelabel CBTurnedInArray, 0x807FC930
.definelabel charspawnerflags, 0x80755DA8
.definelabel songData, 0x80745658
.definelabel songVolumes, 0x807454F0
.definelabel MusicTrackChannels, 0x807458DC
.definelabel BoatSpeeds, 0x8075A04C
.definelabel textParameter, 0x80750AC8

.definelabel collisionType, 0x807FBD70
.definelabel collisionActive, 0x807FBB85
.definelabel PlayerPointer_0, 0x807FDC94
.definelabel TiedCharacterSpawner, 0x807FDC98
.definelabel currentCharSpawner, 0x807FDC9C
.definelabel EnemiesKilledCounter, 0x80744508

.definelabel MelonArray, 0x800334DC
.definelabel IGT, 0x80750AB0
.definelabel LevelStateBitfield, 0x807FBB60

.definelabel menuHeadX, 0x80033F68
.definelabel menuHeadY, 0x80033F80
.definelabel menuHeadScale, 0x80033F98
.definelabel ImageCache, 0x807FC690
.definelabel ViewedPauseItem, 0x807FC80C
.definelabel NextViewedPauseItem, 0x807FC80D
.definelabel MenuActivatedItems, 0x807FC818
.definelabel ItemsInWheel, 0x807FC83C
.definelabel RotationPerItem, 0x807FC83A
.definelabel FileVariables, 0x807FC828

.definelabel ToeSet1, 0x80036950
.definelabel ToeSet2, 0x80036968

.definelabel CannonArcSize, 0x80753CD0
.definelabel PotionAnimations, 0x8075D380
.definelabel ArcadeBackgrounds, 0x8004A788
.definelabel ArcadeExited, 0x8004A73C
.definelabel ArcadeStoryMode, 0x8004A740
.definelabel ArcadeMap, 0x8004C723
.definelabel ArcadeEnableReward, 0x8004A770
.definelabel ArcadeScores, 0x8004A74C
.definelabel ArcadeCurrentScore, 0x8004A748

.definelabel CharSpawnerActorSubtypes, 0x80755698
.definelabel CharSpawnerActorData, 0x8075EB80

.definelabel SelectedDLIndex, 0x807444FC

.definelabel balloonPatchCounts, 0x807FC408
.definelabel coloredBananaCounts, 0x807F6150

.definelabel StackTraceAddresses, 0x807FEF80
.definelabel StackTraceX, 0x807FEF70
.definelabel StackTraceY, 0x807FEF74
.definelabel StackTraceSize, 0x807FEF78
.definelabel StackTraceStartX, 0x807FEF7C

.definelabel ChunkLighting_Red, 0x8076A0B4
.definelabel ChunkLighting_Green, 0x8076A0B8
.definelabel ChunkLighting_Blue, 0x8076A0BC
.definelabel chunk_count, 0x807F6C28
.definelabel chunkArray, 0x807F6C18

.definelabel BlueprintLargeImageColors, 0x80033228

.definelabel SFXVolume, 0x8074583C
.definelabel MusicVolume, 0x80745840
.definelabel BorderInformation, 0x80750840

.definelabel RambiArenaComboTimer, 0x8002D930
.definelabel RambiArenaComboSize, 0x8002D92C
.definelabel RambiArenaComboChain, 0x8002DEF0

.definelabel StoredOrangeCount, 0x80029FA4