//functions
.definelabel setFlag, 0x8073129C
.definelabel checkFlag, 0x8073110C
.definelabel dk_malloc, 0x80610FE8
.definelabel dk_free, 0x80611408
.definelabel playSound, 0x80609140
.definelabel initiateTransition, 0x805FF378
.definelabel initiateTransition_0, 0x805FF9AC
.definelabel getFlagBlockAddress, 0x8060E25C
.definelabel isAddressActor, 0x8067AF44
.definelabel getTimestamp, 0x800060B0
.definelabel dmaFileTransfer, 0x80000450
.definelabel deleteActor, 0x806785D4
.definelabel spawnActor, 0x80677FA8
.definelabel spawnTextOverlay, 0x8069D0F8
.definelabel dk_sqrt, 0x8000AC60
.definelabel dk_cos, 0x8000A930
.definelabel dk_sin, 0x8000AAA0
.definelabel dk_strFormat, 0x800031E0
.definelabel dk_multiply, 0x80005918
.definelabel convertTimestamp, 0x80005818
.definelabel resetMap, 0x805FFFC8
.definelabel prepKongColoring, 0x8068A508
.definelabel dk_memcpy, 0x80003000
.definelabel SaveToGlobal, 0x8060DEA8
.definelabel DetectGameOver, 0x80714394
.definelabel DetectAdventure, 0x8071432C
.definelabel displaySprite, 0x806AB4EC
.definelabel alterSize, 0x806D0468
.definelabel unkSizeFunction, 0x806CFF9C
.definelabel spawnRocketbarrel, 0x806C7BAC
.definelabel playSong, 0x80602A94
.definelabel playCutscene, 0x8061CC40
.definelabel setHUDItemAsInfinite, 0x806FB370
.definelabel osWritebackDCacheAll, 0x800052E0
.definelabel copyFromROM, 0x8060B140
.definelabel getActorSpawnerIDFromTiedActor, 0x80688E68
.definelabel textOverlayCode, 0x8069DA54
.definelabel spawnTransferredActor, 0x806C80E4
.definelabel resolveMovementBox, 0x8072827C
.definelabel wipeMemory, 0x800051C0
.definelabel hideHUD, 0x806FB218
.definelabel tagKong, 0x806C8E58
.definelabel clearGun, 0x806F0C18
.definelabel playAnimation, 0x80614E78
.definelabel clearTagSlide, 0x806CFF9C
.definelabel initiateTransitionFade, 0x807124B8
.definelabel __osInvalICache, 0x80005260
.definelabel __osInvalDCache, 0x80004520
.definelabel __osWritebackDCache, 0x80005670
.definelabel __osCreateMesgQueue, 0x80004950
.definelabel __osRecvMesg, 0x800046C0
.definelabel __osEPiStartDMA, 0x80006F10
.definelabel __osPiRawReadIo, 0x800045D0
.definelabel __osDisableInt, 0x80009020
.definelabel __osRestoreInt, 0x80009040
.definelabel __osEepromProbe, 0x80007D20
.definelabel copyFunc, 0x805FB750
.definelabel getMapData, 0x8066B0F8
.definelabel loadSetup, 0x806886E0
.definelabel getParentDataIndex, 0x80688D64
.definelabel getScreenPosition, 0x80626F8C
.definelabel WarpToDKTV, 0x807131BC
.definelabel textDraw, 0x806FD490
.definelabel wipeStoredSetup, 0x80611614
.definelabel complex_free, 0x8061130C
.definelabel createCollision, 0x8067ABC0
.definelabel setScriptRunState, 0x8064199C
.definelabel deleteActorContainer, 0x806782C0
.definelabel initCharSpawnerActor, 0x80729B00
.definelabel cutsceneKongGenericCode, 0x806BFBF4
.definelabel DisplayTextFlagCheck, 0x806C151C
.definelabel handleCutsceneKong, 0x806F09F0
.definelabel alterCutsceneKongProperties, 0x806C15E8
.definelabel unkCutsceneKongFunction, 0x80714C08
.definelabel spawnCutsceneKongText, 0x806C10A0
.definelabel unkCutsceneKongFunction_0, 0x80724CA4
.definelabel changeActorColor, 0x807149C8
.definelabel unkCutsceneKongFunction_1, 0x80724E48
.definelabel getAnimationTimer, 0x80614A54
.definelabel playSFXFromObject, 0x806085DC

.definelabel unkObjFunction0, 0x80650BBC
.definelabel unkObjFunction1, 0x80650A04
.definelabel unkObjFunction2, 0x806508B4
.definelabel unkObjFunction3, 0x80723020
.definelabel unkObjFunction4, 0x80723320
.definelabel unkObjFunction5, 0x8072334C
.definelabel unkObjFunction6, 0x80723284
.definelabel touchingModel2Object, 0x806F70A8
.definelabel GetKongUnlockedFlag, 0x805FF018
.definelabel setNextTransitionType, 0x805FF158

.definelabel unkMultiplayerWarpFunction, 0x8061EB04
.definelabel renderScreenTransition, 0x806291B4

.definelabel initDisplayList, 0x807132DC
.definelabel getTextStyleHeight, 0x806FD894
.definelabel displayText, 0x806FC530
.definelabel displayImage, 0x8068C5A8
.definelabel determineXRatioMovement, 0x80612794

.definelabel getWorld, 0x805FF030
.definelabel displayImageOnObject, 0x80635018
.definelabel drawNumberObject, 0x80635098
.definelabel isLobby, 0x805FEF74
.definelabel canHitSwitch, 0x806419F8
.definelabel setSomeTimer, 0x80641724
.definelabel indexOfNextObj, 0x80659470
.definelabel renderActor, 0x806319C4

.definelabel cancelPausedCutscene, 0x8061CB08
.definelabel pauseCutscene, 0x8061CAD8
.definelabel hasTurnedInEnoughCBs, 0x805FF0C8
.definelabel getTextPointer_0, 0x8070D8C0
.definelabel BonusBarrelCode, 0x806809F0
.definelabel DisplayExplosionSprite, 0x8067DCC0

.definelabel setArcadeTextXY, 0x80024508
.definelabel spawnArcadeText, 0x8002451C
.definelabel setArcadeTextColor, 0x800244E4
.definelabel arcadeGetObjIndexOfType, 0x80024860
.definelabel arcadeGetNextVacantSlot, 0x800247B8
.definelabel setArcadeSong, 0x800252A4

.definelabel countFlagArray, 0x80731AA8
.definelabel setWaterHeight, 0x80661398
.definelabel loadObjectForScripting, 0x8063B4C0
.definelabel updateObjectScript, 0x8063E078
.definelabel executeBehaviourScript, 0x8063E0D4
.definelabel loadCounterFontTexture, 0x8069DC80
.definelabel delayedObjectModel2Change, 0x8063DB3C
.definelabel cycleRNG, 0x806119A0
.definelabel voidWarp, 0x805FF1B0
.definelabel setToeTexture, 0x8002FC48
.definelabel applyFootDamage, 0x8002FC98
.definelabel modifyCharSpawnerAttributes, 0x8072B79C
.definelabel modifyObjectState, 0x8063DA40
.definelabel spawnPianoKremling, 0x80641874
.definelabel setAcceptablePianoKey, 0x806508B4
.definelabel checkContactSublocation, 0x8064AB1C
.definelabel PlayCutsceneFromModelTwoScript, 0x80641DA0
.definelabel handleGuardDetection, 0x806AE394
.definelabel guardShouldMove, 0x8072E54C
.definelabel guardUnkFunction, 0x80724E48
.definelabel generalActorHandle, 0x8072AB74
.definelabel handleGuardDefaultAnimation, 0x8072B7CC
.definelabel setActorSpeed, 0x8072B324
.definelabel playActorAnimation, 0x80614EBC
.definelabel actorUnkFunction, 0x8072A450
.definelabel getRNGLower31, 0x80611A44
.definelabel setActorAnimation, 0x8072DE44
.definelabel actorUnkFunction_0, 0x8072D13C
.definelabel spawnSparkles, 0x80686E40
.definelabel spawnEnemyDrops, 0x806A5C60
.definelabel isActorLoaded, 0x8067ADB4
.definelabel beaverControlSwitchCase, 0x806AD260
.definelabel spawnProjectile, 0x80690A28
.definelabel updateActorProjectileInfo, 0x80690814
.definelabel controlStateControl, 0x806DF6D4
.definelabel save, 0x8060DEC8
.definelabel displayItemOnHUD, 0x806F8BC4
.definelabel assessFlagMapping, 0x807314F4
.definelabel coinCBCollectHandle, 0x806F54E0

.definelabel unkSpriteRenderFunc, 0x807149FC
.definelabel unkSpriteRenderFunc_0, 0x8071495C
.definelabel loadSpriteFunction, 0x8071498C
.definelabel displaySpriteAtXYZ, 0x80714CC0
.definelabel getHUDSprite, 0x806FACE8

//vanilla data
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
.definelabel LagBoost, 0x80744478 // u32
.definelabel FrameLag, 0x8076AF10
.definelabel FrameReal, 0x80767CC4
.definelabel RNG, 0x80746A40 // u32
.definelabel BetaNinRWSkip, 0x80755324 // u8
.definelabel LogosDestMap, 0x807132BF // u8
.definelabel LogosDestMode, 0x807132CB // u8
.definelabel Gamemode, 0x80755314 // u8
.definelabel ObjectModel2Pointer, 0x807F6000
.definelabel ObjectModel2Timer, 0x8076A064
.definelabel ObjectModel2Count, 0x807F6004
.definelabel ObjectModel2Count_Dupe, 0x80747D70
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
.definelabel CurrentActorPointer, 0x807FBB44
.definelabel CurrentActorPointer_0, 0x807FBB40
.definelabel LoadedActorCount, 0x807FBB35
.definelabel LoadedActorArray, 0x807FB930
.definelabel SpawnerMasterData, 0x807FDC88
.definelabel MenuSkyTopRGB, 0x80754F4C
.definelabel MenuSkyRGB, 0x80754F4F
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
.definelabel ModelTwoTouchCount, 0x807FD798 // u8
.definelabel ModelTwoTouchArray, 0x807FD790 // u16 array
.definelabel TransitionProgress, 0x807ECC60 // u8
.definelabel BackgroundHeldInput, 0x807ECD40 // u32
.definelabel PauseTimestampMajor, 0x807445C0 // u32
.definelabel PauseTimestampMinor, 0x807445C4 // u32
.definelabel HelmStartTimestampMajor, 0x80755340 // u32
.definelabel HelmStartTimestampMinor, 0x80755344 // u32
.definelabel HelmStartTime, 0x8075534C // u32
.definelabel p1PressedButtons, 0x807ECD48
.definelabel p1HeldButtons, 0x807ECD58
.definelabel player_count, 0x807FC928
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
.definelabel LZFadeoutProgress, 0x807FD888
.definelabel mapFloorPointer, 0x807F9514
.definelabel mapFloorBlockCount, 0x807F9518
.definelabel displayListCount, 0x8076A088
.definelabel TransitionType, 0x8076AEE0
.definelabel DKTVKong, 0x80755328
.definelabel CutsceneBanks, 0x807F5B10
.definelabel EEPROMType, 0x807EDEAC

.definelabel screenCenterX, 0x80744490
.definelabel screenCenterY, 0x80744494
.definelabel collisionPos, 0x807F621C
.definelabel FileIndex, 0x807467C8
.definelabel LockStackCount, 0x807F5A68
.definelabel CutsceneBarState, 0x8076A0B3

.definelabel TriggerArray, 0x807FDCB4
.definelabel TriggerSize, 0x807FDCB0
.definelabel CastleCannonPointer, 0x807F5BE8
.definelabel TroffNScoffReqArray, 0x807446C0 // u16 item size
.definelabel TroffNScoffTurnedArray, 0x807FC930 // u16 item size
.definelabel BLockerDefaultArray, 0x807446D0 // u16 item size
.definelabel BLockerCheatArray, 0x807446E0 // u16 item size, [u8 - GB, u8 - Kong]
.definelabel CheckmarkKeyArray, 0x80744710 // u16 item size
.definelabel KongFlagArray, 0x807505B0
.definelabel MainMenuMoves, 0x80033938
.definelabel DataIsCompressed, 0x80748E18
.definelabel CrankyMoves, 0x80033260
.definelabel CandyMoves, 0x80033334
.definelabel FunkyMoves, 0x80033408
.definelabel WorldArray, 0x8074809C
.definelabel WorldExitArray, 0x807480AC
.definelabel LobbiesArray, 0x80744734
.definelabel RaceExitArray, 0x807447A0
.definelabel BossMapArray, 0x80744700
.definelabel BossKongArray, 0x807446F0
.definelabel KutOutKongArray, 0x80035B44
.definelabel EnemyDropsTable, 0x80750400
.definelabel scriptLoadedArray, 0x807F60B0
.definelabel scriptsLoaded, 0x807F60A8
.definelabel scriptLoadsAttempted, 0x807F7140

.definelabel KongUnlockedMenuArray, 0x80033804
.definelabel FilePercentage, 0x80033F51
.definelabel FileGBCount, 0x8003380C
.definelabel FileScreenDLOffset, 0x80033F4C
.definelabel GBDictionary, 0x80755A20
.definelabel DKTVData, 0x8075E5C0

.definelabel CBTurnedInArray, 0x807FC930
.definelabel charspawnerflags, 0x80755DA8
.definelabel songData, 0x80745658
.definelabel MusicTrackChannels, 0x807458DC
.definelabel BoatSpeeds, 0x8075A04C
.definelabel textParameter, 0x80750AC8

.definelabel collisionType, 0x807FBD70
.definelabel collisionActive, 0x807FBB85
.definelabel PlayerPointer_0, 0x807FDC94
.definelabel currentCharSpawner, 0x807FDC9C
.definelabel EnemiesKilledCounter, 0x80744508

.definelabel getXRatioMovement, 0x80612794
.definelabel getZRatioMovement, 0x80612790
.definelabel ModelTwoCollisionArray, 0x80753EF0
.definelabel IGT, 0x80750AB0
.definelabel LatestCollectedObject, 0x807FD734

//hack data
.definelabel TestVariable, 0x807FFFFC
.definelabel StoredLag, 0x807FFFFA // 0x2
.definelabel DamageMultiplier, 0x807FFFF9 // u8
.definelabel ExpandPauseMenu, 0x807FFFF8
.definelabel InitialPauseHeight, 0x807FFFF6
.definelabel LoadedHooks, 0x807FFFEF // u8
.definelabel WarpToIslesEnabled, 0x807FFFEE // u8
.definelabel SkipDance, 0x807FFFED // u8
.definelabel permaLossMode, 0x807FFFEC // u8
.definelabel preventTagSpawn, 0x807FFFEA // u8
.definelabel bonusAutocomplete, 0x807FFFE9 // u8
.definelabel QoLOn, 0x807FFFE8 // u8
.definelabel LobbiesOpen, 0x807FFFE7 // u8
.definelabel Rando, 0x807FF800 // 0x200
.definelabel InstanceScriptParams, 0x807FFFB4 // 0x8
.definelabel PauseSlot3TextPointer, 0x807FFFBC // ptr
.definelabel ReplacementLobbiesArray, 0x807FFFC0 // 0x12
.definelabel style2Mtx, 0x807FFF90
.definelabel style6Mtx, 0x807FFF70
.definelabel style128Mtx, 0x807FFF50
.definelabel StoredSettings, 0x807ED5A0
.definelabel ReplacementLobbyExitsArray, 0x807FFF3E // 0x12
.definelabel StoredCounterTextures, 0x807FFF30
.definelabel PauseText, 0x807FFFE6
.definelabel ShorterBosses, 0x807FFFE5
.definelabel ForceStandardAmmo, 0x807FFFE4
.definelabel KKOPhaseRandoOn, 0x807FFFE0
.definelabel KKOPhaseOrder, 0x807FFFE1
.definelabel MultiBunchCount, 0x807FFFDE

.definelabel CrankyMoves_New, 0x807FF400
.definelabel CandyMoves_New, 0x807FF4F0
.definelabel FunkyMoves_New, 0x807FF5E0