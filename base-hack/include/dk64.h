//functions
extern void setFlag(int flagIndex, int value, flagtypes flagType);
extern int checkFlag(int flagIndex, flagtypes flagType);
extern int getFlagIndex(int startFlag, int level, int kong);
extern void* dk_malloc(int size);
extern void dk_free(void* mallocPtr);
extern void playSound(short soundIndex, int unk0, float unk1, float unk2, int unk3, int unk4);
extern void initiateTransition(maps map, int exit);
extern void initiateTransition_0(maps map, int exit, int unk0, int unk1);
extern void WarpToParent(void);
extern void ExitFromBonus(void);
extern void ExitRace(void);
extern void ExitFromLevel(void);
extern int* getFlagBlockAddress(char flagType);
extern int isAddressActor(void* address);
extern unsigned long long getTimestamp(void);
extern void dmaFileTransfer(int romStart, int romEnd, int ramStart);
extern void deleteActor(void* actor);
extern int spawnActor(int actorID, int actorBehaviour);
extern void* spawnActorSpawnerContainer(short actor, int x, int y, int z, int unk0, int unk1, int unk2, void* unk3);
extern void spawnTextOverlay(int style, int x, int y, char* string, int timer1, int timer2, unsigned char effect, unsigned char speed);
extern float dk_sqrt(float __x);
extern float dk_cos(float __x);
extern float dk_sin(float __x);
extern void dk_strFormat(char* destination, char* source, ...);
extern void dk_multiply(double val1, double val2, int unk1, int unk2);
extern double convertTimestamp(double unk0, double unk1, unsigned int unk2, unsigned int unk3);
extern void resetMap();
extern void prepKongColoring();
extern int getTimestampDiff(unsigned int major, unsigned int minor);
extern void patchHook(unsigned int hook_rdram_location, int offset_in_hook_list, char hook_byte_size);
extern void* dk_memcpy(void* _dest, void* _src, int size);
extern void getTimestampDiffInTicks(unsigned int major, unsigned int minor);
extern int timestampDiffToMilliseconds(unsigned int major, unsigned int minor);
extern void timestampAdd(int* timestamp1, int* timestamp2);
extern int SaveToGlobal();
extern int SaveToUnk();
extern int DetectGameOver();
extern int DetectAdventure();
extern void displaySprite(void* control_pointer, void* sprite, int x, int y, float scale, int gif_updatefrequency, int movement_style);
extern int* getOtherSpritePointer();
extern void alterSize(void* object, int size);
extern void unkSizeFunction(void* object);
extern void spawnRocketbarrel(void* object, int unk);
extern void* getObjectArrayAddr(void* init_address, int common_object_size, int index);
extern short getFloatUpper(float value);
extern void playSong(songs songIndex, float volume);
extern void playLevelMusic(void);
extern void loadExtraHooks();
extern void playCutscene(void* actor, int cutscene_index, int cutscene_type);
extern void playBonusCutsceneWrapper(void* actor, int unk0, int cutscene_index, int unk1);
extern int isCutsceneActive(void);
extern void setHUDItemAsInfinite(int item_index, int player_index, char isInfinite);
extern void resetCoconutHUD(void);
extern void osWritebackDCacheAll();
extern void copyFromROM(int rom_start, void* write_location, void* file_size_location, int unk1, int unk2, int unk3, int unk4);
extern int getActorSpawnerID(void* actor);
extern void textOverlayCode(void);
extern void spawnTransferredActor(void);
extern void resolveMovementBox(void* spawner);
extern void wipeMemory(void* location, int size);
extern void wipeMallocSpace(void* pointer);
extern void setArcadeTextXY(int x, int y);
extern void spawnArcadeText(void* write_location, void* text_pointer);
extern void setArcadeTextColor(int red, int green, int blue, int alpha);
extern int arcadeGetObjIndexOfType(int obj_type);
extern int arcadeGetNextVacantSlot(void);
extern void setArcadeSong(int songIndex);
extern void sendToHiScorePage(void);
extern void sendToNextMap(void);
extern void hideHUD(void);
extern void tagKong(int kong_actor_index);
extern void clearGun(void* player);
extern void playAnimation(void* player, int anim_index);
extern void clearTagSlide(void* player);
extern void initiateTransitionFade(maps map, int cutscene, int gamemode);
extern void __osInvalICache(void* write_location, int size);
extern void __osInvalDCache(void* write_location, int size);
extern void __osWritebackDCache(void* write_location, int size);
extern void __osCreateMesgQueue(void* queue, void* message, int unk);
extern void __osRecvMesg(void* queue, void* message, int os_state);
extern void __osEPiStartDMA(void* unk, void* iomessage, int os_state);
extern void __osPiRawReadIo(int a0, void* a1);
extern int __osGetThreadId(OSThread* thread);
extern int __osDisableInt();
extern void __osRestoreInt(int mask);
extern int __osEepromProbe(void* unk0);
extern void __osViSwapContext(void);
extern void* __osVirtualToPhysical(void* data);
extern int cstring_strlen(char* str);
extern void copyFunc(int rom_offset, int size, void* write_location);
extern void* getMapData(data_indexes data_idx, int _index, char compressbyte0, char compressbyte1);
extern void loadSetup(void* setup_file, int unk0, int unk1);
extern int getParentDataIndex(int map);
extern void WarpToDKTV(void);
extern void initHelmTimer(void);
extern void LoadGameOver(void);
extern int getActorSpawnerIDFromTiedActor(void* actor);
extern void deleteActorContainer(void* actor);
extern void renderActor(void* actor, int unk0);
extern void initCharSpawnerActor(void);
extern void cutsceneKongGenericCode(void);
extern void DisplayTextFlagCheck(short text_file, char text_index, short flag);
extern void handleCutsceneKong(void* actor, int index);
extern void addToHandState(void* actor, int index);
extern void removeFromHandState(void* actor, int index);
extern int playGunSFX(void* actor);
extern void playTagActorAnimation(void* actor, void* paad, int index);
extern void alterCutsceneKongProperties(void);
extern void displaySpriteAttachedToActor(void* sprite, float scale, void* actor, int bone, int info_type);
extern void spawnCutsceneKongText(int text_index, int text_file, int unk0);
extern void unkCutsceneKongFunction_0(int unk0, int unk1);
extern void changeActorColor(int red, int green, int blue, int alpha);
extern void unkCutsceneKongFunction_1(int unk0);
extern float getAnimationTimer(void* actor);
extern int getPadGravity(void* actor);
extern void BananaMedalGet(void);
extern void CrownGet(void);
extern void updateModel(void* data);
extern void bounceObjectCode(int convert_to_model_two);

extern int callFunc(void* func);

extern void cancelMusic(int song, int unk0);
extern void removeGorillaGone(void* actor);
extern void resetActorDL(void* actor);
extern int getActorModelIndex(void* actor);

extern void spawnTextOverlayWrapper(int style, int x, int y, char* str, int unk0, int unk1, int unk2, int unk3);

extern void regularFrameLoop(void);
extern void handleMusicTransition(void);

extern void loadJetpacSprites(void);
extern void updateGBCountHUD(int player);
extern void initHUDItem(float x, float y, float* unk0, float* unk1, float* unk2);

extern void wipeStoredSetup(void* setup);
extern void complex_free(void* ptr);
extern void createCollision(int type, void* player, collision_types subtype, int map, int exit, int x, int y, int z);
extern void setScriptRunState(void* behaviour_pointer, enum_script_runstate destination_state, int unk0);

extern void unkObjFunction0(int id, int unk0, int unk1);
extern void unkObjFunction1(int id, int unk0, int unk1);
extern void unkObjFunction2(int id, int unk0, int unk1);
extern int unkObjFunction3(int unk0, int unk1, int unk2, int unk3, int unk4, int unk5, int unk6);
extern void unkObjFunction4(int behav_38, int unk0);
extern void unkObjFunction5(int behav_38, int unk0);
extern void unkObjFunction6(int behav_38, int unk0);
extern void unkObjFunction7(int id, int unk0, int unk1);
extern int unkObjFunction8(int id, int unk0);
extern void unkObjFunction9(int id, int unk0, int unk1);
extern void unkObjFunction10(int id, int unk0, int unk1, int unk2);
extern void unkObjFunction11(int id, int unk0);
extern int unkObjFunction12(int id, int unk0, int unk1, int unk2, int unk3, float unk4, int unk5);
extern void unkObjFunction13(int unk0, int unk1, int unk2);
extern void unkObjFunction14(int unk0);
extern void unkObjFunction15(int unk0, int x, int y, int z);
extern void unkObjFunction16(int unk0, int unk1, short* unk2, float* unk3, char* unk4);
extern void unkObjFunction17(int id, int unk0, int unk1);
extern int checkLeverAngle(void);

extern int touchingModel2Object(int id);
extern int GetKongUnlockedFlag(int actor_type, int kong_index);
extern void setNextTransitionType(int type);
extern int isPlayerInRangeOfObject(int distance);
extern int getPlayerObjectDistance(void);
extern void spawnWrinkly(behaviour_data* behaviour, int index, int door_kong_index, int unk0);
extern int isWrinklySpawned(void);
extern void setAction(int action, void* actor, int player_index);
extern void exitPortalPath(behaviour_data* behaviour, int index, int unk0, int unk1);
extern int getInteractionOfContactActor(int contact_actor);
extern void enterPortal(void* player);
extern void drawBossDoorNumber(behaviour_data* behaviour, int index, int unk0, int unk1);
extern void displayShopIcon(behaviour_data* behaviour_data, int id, int image_index, int unk0);
extern void hideShop(behaviour_data* behaviour_data, int id, int unk0, int unk1);

extern Gfx* initDisplayList(Gfx* dl);
extern Gfx* initDisplayList_0(Gfx* dl);
extern int getTextStyleHeight(int style);
extern Gfx* displayText(Gfx* dl, int style, int x, int y, void* text_pointer, char unk0);
extern Gfx* displayImage(Gfx* dl, int texture_index, int unk3, codecs codec_index, int width, int height, int x, int y, float xScale, float yScale, int unk11, float unk12);
extern void getScreenPosition(float x, float y, float z, float* x_store, float* y_store, int unk8, float scale, char player_index);
extern Gfx* textDraw(Gfx* dl, int style, int x, int y, char* str);
extern void* getPtr14Texture(int texture);
extern void renderImage_Internal(Gfx* dl, void* texture, int unk0, int width, int height, int unk1, int unk1_copy, int unk2, int unk2_copy, float width_f, float height_f, float x_center, float y_center, int unk3);
extern Gfx* displayChunk(Gfx* dl, int chunk_index, int shift);

extern void cancelPausedCutscene(void);
extern void pauseCutscene(void);
extern void getTextPointer_0(void* actor, int text_file, int text_index);

extern int hasTurnedInEnoughCBs(void);
extern int getWorld(maps map, int lobby_is_isles);
extern void displayImageOnObject(int obj_id, int position, int image_index, int unk4);
extern void displayCountOnTeeth(int count);
extern void drawNumberObject(int model, int unk2, int image_index, int unk4);
extern int isLobby(maps map);
extern float determineXRatioMovement(unsigned int unk);
extern float determineZRatioMovement(unsigned int unk);
extern int countFlagArray(int starting_flag, int count, int flagType);
extern int canHitSwitch(void);
extern void setSomeTimer(int model2_type);
extern int indexOfNextObj(int id);
extern int playSFXFromObject(int object_index, short sfx, char unk0, char unk1, char unk2, char unk3, float unk4);
extern int playSFXAtXYZ(float x, float y, float z, int sfx, int unk0, int unk1, int unk2, int unk3, float unk4);

extern void unkMultiplayerWarpFunction(void* actor, int player_index);
extern void renderScreenTransition(int transition_type);

extern int inDKTV(void);
extern void handleGamemodes(void);

extern void setWaterHeight(int chunk, float height, float unk2);
extern void loadObjectForScripting(void* unk0, int unk1);
extern void updateObjectScript(void* behaviour_pointer);
extern void executeBehaviourScript(void* behaviour_pointer, int unk0);
extern void* loadCounterFontTexture(int texture_base, void* write_location, int position, int texture_offset, int width);
extern void delayedObjectModel2Change(maps map, int model2_id, int state);
extern int isObjectLoadedInMap(maps map, int model2_id, int state);
extern int cycleRNG(void);
extern void voidWarp(void);
extern void setToeTexture(void* actor, int data);
extern void applyFootDamage(void* actor, int unk0, int unk1, int unk2);
extern void modifyCharSpawnerAttributes(int unk0, int unk1, int unk2);
extern void modifyObjectState(int object_id, int dest_state);
extern void spawnPianoKremling(int kremling_index, int unk0);
extern void setAcceptablePianoKey(int id, int key, int unk0);
extern int checkContactSublocation(void* behaviour_pointer, int id, int key, int unk0);
extern void PlayCutsceneFromModelTwoScript(void* behavior_pointer, int cutscene, int unk0, int unk1);
extern void handleGuardDetection(float offset, float radius);
extern int guardShouldMove(void);
extern void guardUnkFunction(int unk0);
extern void generalActorHandle(int control_state, int x, int z, int unk0, float unk1);
extern void handleGuardDefaultAnimation(int unk0);
extern void setActorSpeed(void* actor, short speed);
extern void playActorAnimation(void* actor, int animation);
extern void actorUnkFunction(void);
extern int getRNGLower31(void);
extern float getRNGAsFloat(void);
extern void setActorAnimation(int animation);
extern void actorUnkFunction_0(int control_state, int unk0);
extern void spawnSparkles(float x, float y, float z, int size);
extern void spawnEnemyDrops_Vanilla(void* actor);
extern void spawnActorWithFlag(int object, float x, float y, float z, int unk0, int cutscene, int flag, int unk1);
extern void spawnObjectAtActor(int object, int flag);
extern void spawnSpiderSilk(void);
extern void* isActorLoaded(int actor_type);
extern void beaverControlSwitchCase(int unk0, int unk1, int unk2);
extern void BonusBarrelCode(void);
extern void DisplayExplosionSprite(void);
extern void displayWarpSparkles(behaviour_data* behaviour, int index, int unk0, int unk1);
extern void setObjectScriptState(int id, int state, int offset);

extern void updateActorProjectileInfo(void* actor, int unk0);
extern void spawnProjectile(short object, short subtype, float speed, float x, float y, float z, float unk0, void* actor);
extern void controlStateControl(int unk0);
extern void save(void);
extern void getObjectPosition(int index, int unk0, int unk1, void* x, void* y, void* z);

extern void setActorModel(void* actor, int index);
extern void spawn3DActor(spawnerPacket* packet);
extern int getChunk(float x, float y, float z, int unk0);
extern void spawnKey(short flag, int x, int y, int z, short unk0, short unk1);
extern void spawnTimer(int x, int y, int timer);
extern void initTimer(void* actor);
extern void mushroomBounce(void);

extern int crystalsUnlocked(int kong);
extern void setMovesForAllKongs(shop_paad* paad, int is_bitfield);
extern void setMoveProgressive(shop_paad* paad, int kong);
extern void setMoveBitfield(shop_paad* paad, int kong);
extern void refillHealth(int player_index);
extern void changeCollectableCount(int item, int player_index, int change);
extern void save(void);
extern void* getSpawnerTiedActor(short target_trigger, short props_change);

extern void bananaslip(void);
extern void setAnimalYAccel(void);

extern void _guScaleF(void* mtx, int x, int y, int z);
extern void _guTranslateF(void* mtx, float x, float y, float z);
extern void _guMtxCatF(void* mtx, void* unk0, void* unk1);
extern void _guMtxF2L(void* mtx, void* unk0);
extern void _guMtxXFML(void* unk0, int unk1, int unk2, int unk3, float* x, float* y, float* z);
extern void _guMtxXFMF(void* unk0, int unk1, int unk2, int unk3, float* x, float* y, float* z);
extern void* getTextPointer(int file, int text_index, int unk0);
extern void addDLToOverlay(void* code, void* actor, int delay);
extern int groundContactCheck(void);
extern void groundContactSet(void);
extern int getRefillCount(int item, int player);
extern int doAllKongsHaveMove(shop_paad* paad, int unk0);
extern void getSequentialPurchase(shop_paad* paad, KongBase* movedata);
extern int ReadFile(int data, int kong, int level, int file);
extern void SaveToFile(int data, int kong, int level, int file, int value);
extern Gfx* printText(Gfx* dl, short x, short y, float scale, char* str);
extern Gfx* printOutOfCounter(int x, int y, int top, int bottom, Gfx* dl, int unk0, int scale);

extern void assessFlagMapping(int map, int id);
extern void coinCBCollectHandle(int player, int obj, int is_homing);
extern void standardCrateHandle(int player_index, int id, void* player, int obj_type);
extern void bunchHandle(int player_index, int id, void* player);
extern void displayItemOnHUD(int item, int unk0, int unk1);
extern int getCollectableOffset(int item, int obj, int homing);
extern void GoldenBananaCode(void);

extern void unkSpriteRenderFunc(int unk0);
extern void unkSpriteRenderFunc_0(void);
extern void unkSpriteRenderFunc_1(int unk0);
extern void unkSpriteRenderFunc_2(int unk0);
extern void unkSpriteRenderFunc_3(int unk0);
extern void attachSpriteToBone(void* sprite, float scale, void* actor, int bone, int unk0);
extern void loadSpriteFunction(int func);
extern sprite_struct* displaySpriteAtXYZ(void* sprite, float scale, float x, float y, float z);
extern void* getHUDSprite(int item);
extern void updateMenuController(void* actor, void* paad, int unk0);
extern void lockInput(int unk0);
extern void fileStart(int file);
extern int isFileEmpty(int file);
extern void initMenuBackground(void* paad, int unk0);
extern int calculateFilePercentage(void);
extern void displayMenuSprite(void* paad, void* sprite_address, int x, int y, float scale, int unk0, int unk1);
extern void loadFile(int file, int restock_inventory);
extern void loadEndSeq(int mode);
extern void checkGlobalProgress(int flag);
extern void updateCutscene(void);
extern void loadDKTVData(void);
extern void clearActorList(void);
extern void updateModelScales(void* actor, int size);
extern void WipeFile(int file, int will_save);
extern void WipeImageCache(void);
extern void calculateScreenPosition(float x, float y, float z, float* x_store, float* y_store, int unk0, float unk1, int unk2);
extern int getNewSaveTime(void);
extern void unkBonusFunction(actorData* actor);
extern void internalKasplatCode(int has_bp);
extern void drawRetroSprite(void* unk0, int x, int y);

extern void spriteActorGenericCode(float unk0);
extern void assignGIFToActor(void* paad, void* sprite, float scale);
extern int loadSetupNew(int map);
extern int getParentIndex(int map);
extern void getParentMap(int* map, int* exit);
extern void updateCollisionDimensions(int player, int x_f, int y_f, int z_f, float scale);
extern void parseCheats(int unk0);

extern void wipeTextureSlot(void* location);
extern void copyImage(void* location, void* image, int width);
extern void blink(void* actor, int unk0, int unk1);
extern void unkPaletteFunc(void* actor, int unk0, int unk1);
extern void applyImageToActor(void* actor, int unk0, int unk1);
extern void adjustColorPalette(void* actor, int unk0, int palette, float unk1);
extern void retextureZone(void* actor, int index, int palette);
extern void writeImageSlotToActor(void* actor, int unk0, int unk1, void* location);
extern void spriteControlCode(sprite_struct* sprite, char* render);
extern int getPauseWheelRotationProgress(int unk0, int unk1);
extern void updateFilePercentage(void);
extern int getKong(int player_index);
extern int spawnModelTwo(int type, float x, float y, float z, float scale, int id);
extern void refreshItemVisibility(void);

extern void getPathPosition(int path_index, float* x, float* y, float* z);
extern void updateGBCountHUD(int player);

extern void* getActorModel(void* actor, int model_index, int unk0);

extern int isBalloonOrPatch(int actor_type);
extern void getModel2AndActorInfo(void* setup, int** model2_write, int** actor_write);
extern int isSingleOrBunch(int object_type);
extern void enableComplexFree(void);
extern void complexFreeWrapper(void* addr);
extern void trapPlayer(void);
extern int applyDamage(int player, int damage);
extern void damage(void);
extern int checkDeathAction(void* player);
extern int isObjectTangible(int id);
extern int getCenterOffset(int style, char* str);

extern void unkLightFunc_0(actorData* actor, int unk0, char unk1, char unk2, unsigned char unk3, unsigned char unk4, float unk5, char unk6); //80604cbc
extern void kongFollowingLightFunc(unsigned int unk0, unsigned short height_variance, float payerX, float PlayerY, float PlayerZ, unsigned short unk2, float unk3, float movement_speed, unsigned int unk4); //8072a920
extern void lightShiningLightFunc(void); //806c6530
extern int getAngleBetweenPoints(float x1, float z1, float x2, float z2);

extern void unkCollisionFunc_0(int id, int unk0);
extern collected_item_struct* addNewCollectedObject(item_collision* item);
extern void writeDynamicFlagItemToFile(int flag, int data, int world);

extern void* deleteModelTwo(int index, int id_of_next);
extern void spawnModelTwoWithDelay(int type, int x, int y, int z, int delay);

extern int printDebugText(char* string, int v1, int v2, int v3, int v4);
extern void dumpReturns(void* info);
extern void updateBones(bonedata* bone, int force_update);
extern void resetKongVars(void);
extern void handleAnimation(void* actor);

extern int CanDive(void);
extern void unkTextFunction(void* actor);
extern void homing_code(int bitfield, void* actor, int unk0, int unk1);
extern int madeContact(void);
extern int madeGroundContact(void);
extern void unkProjectileCode_0(void* actor, float unk0);
extern void unkProjectileCode_1(void* actor, float x, float y, float z, float scale, int unk4);
extern void allocateBone(void* actor, int unk0, int unk1, int unk2, int unk3);
extern void unkProjectileCode_2(void* actor);
extern void unkProjectileCode_3(void* actor, int unk0);
extern void playSFXFromActor(void* actor, int sfx, int unk0, int unk1, int unk2);
extern int unkGunFunction(int unk0);

extern void wipeGlobalFlags(void);
extern void setIntroStoryPlaying(int value);

extern void alterSFXVolume(int channel, int volume);
extern void alterMusicVolume(int channel);
extern void adjustSFXType_Internal(int subtype);

extern void runAnimFrame(actorData* actor, int anim, int unk0, float unk1);
extern int getTrackChannel(int song);
extern int getSongWriteSlot(int song);
extern void loadSongIntoMemory(int write_slot, int song, float volume);
extern void cseqpScheduleMetaEventCheck(int seq_player);
extern int cspGetState(int* seqp);
extern void handleTextScrolling(void* menu_aad, float x1, float y1, float* x2, float* y2, int unk0, int unk1, float unk2);

extern void handlePoleGrabbing(void* actor, int player_index, int allow_vines);
extern void handleLedgeGrabbing(void);
extern void unkCutsceneFunction(void* actor);
extern void loadMapChunkLighting(int chunk_index);
extern void loadChunks(void* data);
extern void genericKongCode(void* actor, int kongType);
extern void renderLight(float x, float y, float z, float src_x, float src_y, float src_z, float radius, int unk0, int red, int green, int blue);
extern int getTotalGBs(void);
extern void displayPauseSpriteNumber(void* handler, int x, int y, int unk0, int unk1, int count, int unk2, int unk3);
extern void headphonesCode(int unused, int enable); // Note: Only has parameters for *if* we're passing in an enabled state for the headphones fix qol change

extern int getSpawnerIndexOfResolvedBonus(void* unk0, int unk1, int* map_storage);
extern void resolveBonus(short unk0, int unk1, int unk2, float unk3);
extern void failBonus(int unk0, int unk1);
extern void winBonus(int unk0, int unk1);
extern void getBonePosition(void* actor, int bone, float* x, float* y, float* z);
extern void spawnFireballExplosion(float x, float y, float z, float scale, char unk0, char unk1);
extern void setChunkLighting(float red, float green, float blue, int chunk);
extern void unkLoadingZoneControllerFunction(short exit);

extern void crankyCode(void);
extern void funkyCode(void);
extern void candyCode(void);
extern void snideCode(void);
extern void trashCanBugCode(void);
extern void flyingEnemyHandler(void* func, int anim_0, int anim_1, int anim_2);

extern int getLetterCount(char* str);
extern int getCharacterWidth(int style, char* byte_char);
extern Gfx* styleSpecificDLStuff(Gfx* dl, int style, int file);
extern void recolorVertBlockText(void* vert_block, int unk0, int bitfield);

extern void unkWallFunc(void* actor, int unk0);
extern void unkWallFunc_0(void* actor, int unk0);
extern void adjustProjectileSpawnPosition(float x, float y, float z);
extern void reduceShadowIntensity(int delta);
extern void unkActorFunc(int unk0, int anim_0, int anim_1);
extern void unkActorFunc_0(void* actor, int unk0);
extern int unkCollisionFunc(void* unk0, int unk1);

extern void collisionStuff(void* actor);
extern void unkActorHandler(void* actor);
extern short getScreenDist(short x, short y);
extern int getDistanceCap(short input_dist);

extern void customDamageCode(void);

//vanilla data
extern OSThread* __osActiveQueue;
extern float TransitionSpeed;
extern char CutsceneWillPlay;
extern char KRoolRound;
extern KongBase MovesBase[6];
extern int PlayerOneColor;
extern char** PauseTextPointer;
extern char** LevelNamesPointer;
extern char Mode;
extern char TBVoidByte;
extern maps CurrentMap;
extern short PreviousMap;
extern maps DestMap;
extern int DestExit;
extern char StorySkip;
extern char HelmTimerShown;
extern char TempFlagBlock[0x10];
extern submapInfo SubmapData[0x12];
extern char HelmTimerPaused;
extern int LagBoost;
extern int FrameLag;
extern int FrameReal;
extern int RNG;
extern char BetaNinRWSkip;
extern char LogosDestMap;
extern char LogosDestMode;
extern char Gamemode;
extern ModelTwoData* ObjectModel2Pointer;
extern int ObjectModel2Timer;
extern int ObjectModel2Count;
extern int ObjectModel2Count_Dupe;
extern short CutsceneIndex;
extern char CutsceneActive;
extern short CutsceneTimer;
extern cutsceneType* CutsceneTypePointer;
extern short PreviousCameraState;
extern short CurrentCameraState;
extern short CameraStateChangeTimer;
extern unsigned short CutsceneStateBitfield;
extern AutowalkData* AutowalkPointer;
extern char IsAutowalking;
extern WarpInfo PositionWarpInfo;
extern short PositionWarpBitfield;
extern float PositionFloatWarps[3];
extern unsigned short PositionFacingAngle;
extern char ChimpyCam;
extern char ScreenRatio;
extern char SoundType;
extern actorData* LastSpawnedActor;
extern char LoadedActorCount;
extern loadedActorArr LoadedActorArray[64];
extern SpawnerMasterInfo SpawnerMasterData;
extern unsigned char MenuSkyTopRGB[3];
extern unsigned char MenuSkyRGB[3];
extern skybox_blend_struct SkyboxBlends[8];
extern int* ActorArray[];
extern short ActorCount;
extern short ButtonsEnabledBitfield;
extern char JoystickEnabledX;
extern char JoystickEnabledY;
extern char MapState;
extern Controller ControllerInput;
extern Controller NewlyPressedControllerInput;
extern Controller PreviouslyPressedButtons;
extern playerData* Player;
extern SwapObjectData* SwapObject;
extern char Character;
extern short KongIndex;
extern cameraData* Camera;
extern char ISGActive;
extern unsigned int ISGTimestampMajor;
extern unsigned int ISGTimestampMinor;
extern char ISGPreviousFadeout;
extern unsigned int CurrentTimestampMajor;
extern unsigned int CurrentTimestampMinor;
extern ISGFadeoutData ISGFadeoutArray[];
extern InventoryBase CollectableBase;
extern char ModelTwoTouchCount;
extern short ModelTwoTouchArray[4];
extern char TransitionProgress;
extern Controller BackgroundHeldInput;
extern unsigned int PauseTimestampMajor;
extern unsigned int PauseTimestampMinor;
extern unsigned int HelmStartTimestampMajor;
extern unsigned int HelmStartTimestampMinor;
extern int HelmStartTime;
extern int HelmCurrentTime;
extern short HelmMinigameFlags[10];
extern short p1PressedButtons;
extern short p1HeldButtons;
extern char player_count;
extern char FocusedPlayerIndex;
extern int* sprite_table[0xAF];
extern char sprite_translucency;
extern int* bbbandit_array[4];
extern char StoredDamage;
extern actorSpawnerData* ActorSpawnerPointer;
extern char DebugInfoOn;
extern char CutsceneFadeActive;
extern short CutsceneFadeIndex;
extern heap* heap_pointer;
extern char stickX_magnitude;
extern char stickY_magnitude;
extern float phasewalk_stickmagnitude;
extern fairyInfo fairy_data;
extern short transferredActorType;
extern charSpawnerData characterSpawnerActors[0x71];
extern unsigned char levelIndexMapping[216];
extern char stickX_interpretted;
extern char stickY_interpretted;
extern char preventSongPlaying;
extern int parentDataCount;
extern parentMaps parentData[17];
extern void* SetupFilePointer;
extern int* focusedParentDataSetup[17];
extern hudData* HUD;
extern text_struct textData[7];
extern text_char_info* textCharData[7];
extern char* textUnkData[7];
extern float LZFadeoutProgress;
extern int* mapFloorPointer;
extern int mapFloorBlockCount;
extern int displayListCount;
extern char TransitionType;
extern char DKTVKong;
extern cutsceneType CutsceneBanks[2];
extern queued_cutscene_function* QueuedCutsceneFunctions;
extern int ActorTimer;
extern int EEPROMType;
extern unsigned char ReverseMillLeverOrder[5];
extern unsigned char ReverseCryptLeverOrder[3];

extern map_properties_bitfield MapProperties;

extern short MapVoid_MinX;
extern short MapVoid_MinZ;
extern short MapVoid_MaxX;
extern short MapVoid_MaxZ;

extern float LeaveWaterVelocity[7];
extern float unkGravity[7];
extern float GroundAttackSpeedThreshold[7];

extern bonus_vanilla_info BonusBarrelData[54];
extern short ArenaScore;

extern short screenCenterX;
extern short screenCenterY;
extern float collisionPos[3];
extern char FileIndex;
extern int LockStackCount;
extern char CutsceneBarState;

extern void* ActorFunctions[345];
extern unsigned char ActorMasterType[345];
extern short* ActorPaadDefs[345];
extern collision_data_struct ActorCollisionArray[345];
extern health_damage_struct ActorHealthArray[345];
extern short ActorInteractionArray[345];

extern trigger* TriggerArray;
extern short TriggerSize;
extern cannon* CastleCannonPointer;
extern short TroffNScoffReqArray[8]; // u16 item size
extern unsigned short TroffNScoffTurnedArray[8]; // u16 item size
extern short BLockerDefaultArray[8]; // u16 item size
extern blocker_cheat BLockerCheatArray[8]; // u16 item size, [u8 - GB, u8 - Kong]
extern short CheckmarkKeyArray[8]; // u16 item size
extern short KongFlagArray[4];
extern main_menu_moves_struct MainMenuMoves[8];
extern char DataIsCompressed[32];
extern char KutOutKongArray[5];
extern enemy_drop_struct EnemyDropsTable[27];
extern short scriptLoadedArray[0x46];
extern short scriptsLoaded;
extern unsigned char scriptLoadsAttempted;
extern int MenuDarkness;

extern purchase_struct CrankyMoves[5][7];
extern purchase_struct CandyMoves[5][7];
extern purchase_struct FunkyMoves[5][7];

extern short LobbiesArray[9]; // Should be 8, but dk64lol
extern short WorldArray[8];
extern short WorldExitArray[8];
extern short WorldCutsceneArray[8];
extern race_exit_struct RaceExitArray[8];

extern short BossMapArray[8];
extern char BossKongArray[16];

extern void* CutsceneModelJumpTable[136];

extern char KongUnlockedMenuArray[5];
extern char FilePercentage; // Unsigned is technically correct, but -124% is more fun
extern int FileGBCount;
extern float FileScreenDLOffset;
extern short CBTurnedInArray[8];
extern short songData[SONG_COUNT];
extern short songVolumes[SONG_COUNT];
extern int* compactSequencePlayers[4];
extern unsigned int DKTVData[5];

extern void* ExitPointer;
extern unsigned char ExitCount;

extern charspawner_flagstruct charspawnerflags[0x1F];
extern GBDictItem GBDictionary[113];
extern actorData* CurrentActorPointer_0;
extern short MusicTrackChannels[12];
extern float BoatSpeeds[2];
extern short textParameter;

extern unsigned char collisionType;
extern unsigned char collisionActive;
extern actorData* PlayerPointer_0;
extern SpawnerInfo* currentCharSpawner;
extern short EnemiesKilledCounter;
extern model2_collision_info ModelTwoCollisionArray[42];
extern unsigned char MelonArray[6];
extern int IGT;
extern unsigned int LevelStateBitfield;

extern float menuHeadX[5];
extern float menuHeadY[5];
extern float menuHeadScale[5];
extern image_cache_struct ImageCache[32];

extern short* AnimationTable1;
extern short* AnimationTable2;
extern short* AnimationTable3;
extern SpawnerInfo* TiedCharacterSpawner;
extern kong_model_struct KongModelData[8];
extern tag_model_struct TagModelData[5];
extern short RollingSpeeds[7];
extern int KongTagNames[9];
extern short KrazyKKModels[6];
extern short ChargeVelocities_0[7];
extern short ChargeVelocities_1[7];
extern short ChargeDeceleration[7];
extern char* KongTextNames[8];

extern actor_behaviour_def ActorBehaviourTable[128];
extern float LedgeHangY[7];
extern float LedgeHangY_0[7];

extern unsigned char ViewedPauseItem;
extern unsigned char NextViewedPauseItem;
extern unsigned char MenuActivatedItems[16];
extern unsigned char ItemsInWheel;
extern short RotationPerItem;
extern short FileVariables[8];

extern char ToeSet1[24];
extern char ToeSet2[24];

extern float CannonArcSize[7];
extern unsigned short PotionAnimations[6];
extern char ArcadeBackgrounds[4];
extern unsigned char ArcadeExited;
extern unsigned char ArcadeStoryMode;
extern unsigned char ArcadeMap;
extern unsigned char ArcadeEnableReward;
extern int ArcadeScores[5];
extern int ArcadeCurrentScore;

extern unsigned char CharSpawnerActorSubtypes[113];
extern charSpawnerActorInfo CharSpawnerActorData[113];

extern unsigned short balloonPatchCounts[221];
extern unsigned short coloredBananaCounts[8];

extern collected_item_struct* CollectedObjects;
extern collected_item_struct* LatestCollectedObject;

extern char SelectedDLIndex;

extern stack_trace_address_struct StackTraceAddresses[19];

extern char* ReasonExceptions[20];
extern unsigned char ReasonCode;
extern int ReasonValues[3];

extern int StackTraceX;
extern int StackTraceY;
extern int StackTraceSize;
extern int StackTraceStartX;

extern weather_struct WeatherData[6];
extern hitbox_master_struct* ModelTwoHitboxPointer;
extern item_collision* MiscHitboxPointer;
extern rgb BlueprintLargeImageColors[16];

extern char SFXVolume;
extern char MusicVolume;

extern Border BorderInformation[22];
extern void* JetpacEnemyFunctions[8];
extern SurfaceInfo SurfaceTypeInformation[9];

extern float* ChunkLighting_Red;
extern float* ChunkLighting_Green;
extern float* ChunkLighting_Blue;
extern int chunk_count;
extern Chunk* chunkArray;
extern unsigned char unkSoundIndex;
extern short unkSoundArray[0x10];

extern char RambiArenaComboTimer;
extern char RambiArenaComboSize;
extern char RambiArenaComboChain[16];

extern char* AnimationPointer;
extern unsigned short StoredOrangeCount;
extern path_data_struct* PathData[32];
extern fence_collective_struct* FenceInformation;
extern rgba KongRGBA[5];
extern char_spawner_paad* ActorPaad;
extern float unkFloatArray[7];
extern float BackflipVelArray[7];

//hack data
extern int TestVariable;
extern char LoadedHooks;
extern varspace Rando;
extern short StoredLag;
extern short ReplacementLobbiesArray[9];
extern short ReplacementLobbyExitsArray[9];
extern unsigned char DamageMultiplier;
extern char LobbiesOpen;
extern char* PauseSlot3TextPointer;
extern char ExpandPauseMenu;
extern unsigned short InitialPauseHeight;
extern cc_effects* CCEffectData;
extern short style128Mtx[0x10];
extern short style6Mtx[0x10];
extern short style2Mtx[0x10];
extern purchase_struct CrankyMoves_New[5][8];
extern purchase_struct CandyMoves_New[5][8];
extern purchase_struct FunkyMoves_New[5][8];
extern purchase_struct TrainingMoves_New[4];
extern purchase_struct BFIMove_New;
extern purchase_struct FirstMove_New;
extern settingsData StoredSettings;
extern char preventTagSpawn;
extern char bonusAutocomplete;
extern void* StoredCounterTextures[7];
extern char TextHoldOn;
extern unsigned char PauseText;
extern unsigned char ShorterBosses;
extern char ForceStandardAmmo;
extern char KKOPhaseRandoOn;
extern char KKOPhaseOrder[3];
extern unsigned short MultiBunchCount;
extern char QueueHelmTimer;
extern char ToggleAmmoOn;
extern void* WarpData;
extern unsigned char InvertedControls;
extern unsigned char WinCondition;
extern unsigned char ChunkyModel;
extern unsigned char EnemyInView;
extern unsigned char ItemRandoOn;
extern short ItemRando_FLUT[0x320];
extern arbitrary_overlay TextOverlayData;
extern unsigned char KasplatSpawnBitfield;
extern char KrushaSlot;
extern unsigned char TextItemName;
extern unsigned char RandomSwitches;
extern unsigned char SwitchLevel[7];
extern int ExtraSaveData[0x100];
extern char* DisplayedSongNamePointer;
extern unsigned char RandomizerVersion;