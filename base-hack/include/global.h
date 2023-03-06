#include "vars.h"
#include "text_items.h"

extern void playSFX(short sfxIndex);
extern void setPermFlag(short flagIndex);
extern int convertIDToIndex(short obj_index);
extern void* findActorWithType(int search_actor_type);
extern int isRDRAM(void* address);
extern void customHideHUD(void);
extern void setWarpPosition(float x, float y, float z);
extern void initHack(int source);
extern void callParentMapFilter(void);
extern void shiftBrokenJapesPortal(void);
extern void quickInit(void);
extern int getCenter(int style, char* str);
extern int getActorIndex(int actor_input);
extern int getCustomActorIndex(new_custom_actors offset);
extern void spawnItemOverlay(int type, int kong, int index, int force);

extern int getWrinklyLevelIndex(void);
extern void initOptionScreen(void);
extern int getLo(void* addr);
extern int getHi(void* addr);

extern void level_order_rando_funcs(void);
extern void unlockKongs(void);
extern void unlockMoves(void);
extern void tagAnywhere(void);
extern void applyFastStart(void);
extern void openCrownDoor(void);
extern void openCoinDoor(void);
extern void qualityOfLife_fixes(void);
extern void qualityOfLife_shorteners(void);
extern void overlay_changes(void);
extern void determine_krool_order(void);
extern void replace_zones(int init_flag);
extern void randomize_bosses(void);
extern void alter_boss_key_flags(void);
extern void displayNumberOnTns(void);
extern void moveTransplant(void);
extern void priceTransplant(void);
extern void squawks_with_spotlight_actor_code(void);
extern void shine_light_at_kong(unsigned short height_variance, unsigned short min_follow_distance, unsigned short param_3);

extern void changeCharSpawnerFlag(int map, int spawner_id, int new_flag);
extern void changeHelmLZ(void);
extern void HelmBarrelCode(void);
extern void WarpHandle(void);

extern void PatchCrankyCode(void);
extern void PatchKRoolCode(void);
extern void PatchBonusCode(void);
extern void FileScreenDLCode_Write(void);
extern void write_kutoutorder(void);
extern void remove_blockers(void);
extern void disable_krool_health_refills(void);
extern void pre_turn_keys(void);
extern void auto_turn_keys(void);
extern void handle_WTI(void);
extern void warpToIsles(void);
extern void adjust_level_modifiers(void);

extern int canItemPersist(void);
extern void initKongRando(void);

extern int convertSubIDToIndex(short obj_index);
extern int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2);
extern void setCrusher(void);
extern void createCollisionObjInstance(collision_types subtype, int map, int exit);
extern int spawnCannonWrapper(void);
extern void disableDiddyRDDoors(void);
extern void fixkey8(void);
extern void alterGBKong(int map, int id, int new_kong);

extern void preventBossCheese(void);
extern void determineStartKong_PermaLossMode(void);
extern void kong_has_died(void);
extern int curseRemoved(void);
extern void forceBossKong(void);
extern int hasPermaLossGrace(int map);
extern void fixGraceCheese(void);

extern void writeJetpacMedalReq(void);
extern void resetMapContainer(void);
extern void correctDKPortal(void);
extern int canSaveHelmHurry(void);
extern int initHelmHurry(void);
extern void addHelmTime(helm_hurry_items item, int multiplier);

extern int* drawTri(int* dl, short x1, short y1, short x2, short y2, short x3, short y3, int red, int green, int blue, int alpha);
extern int* drawImage(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity);
extern int* drawPixelText(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha);
extern int* drawPixelTextContainer(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha, int offset);
extern int* drawScreenRect(int* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha);
extern int* drawTextContainer(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background);
extern int* drawText(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity);
extern int* drawDPad(int* dl);
extern int* drawImageWithFilter(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int red, int green, int blue, int opacity);
extern void correctKongFaces(void);
extern int* display_file_images(int* dl, int y_offset);

extern int getLo(void* addr);
extern int getHi(void* addr);

extern void displayNumberOnObject(int id, int param2, int imageindex, int param4, int subtype);
extern void newCounterCode(void);
extern void wipeCounterImageCache(void);
extern void writeCoinRequirements(int source);
extern void colorMenuSky(void);
extern void getMoveHint(actorData* actor, int text_file, int text_index);
extern void cutsceneDKCode(void);
extern void getNextMovePurchase(shop_paad* paad, KongBase* movedata);

extern void fastWarp_playMusic(void* actor);

extern void guardCatch(void);
extern void catchWarpHandle(void);
extern void handleFootProgress(actorData* actor);
extern void cancelCutscene(int enable_movement);
extern void clearVultureCutscene(void);
extern void fastWarp(void* actor, int player_index);
extern void activateBananaports(void);

extern int getTagAnywhereKong(int direction);
extern int getTAState(void);
extern void toggleStandardAmmo(void);
// extern void initTagAnywhere(void);
extern void initStackTrace(void);
extern void initItemDropTable(void);
extern void initCollectableCollision(void);
extern void initActorDefs(void);
extern void newGuardCode(void);
extern void goldBeaverCode(void);
extern void ninCoinCode(void);
extern void rwCoinCode(void);
extern void medalCode(void);
extern void beanCode(void);
extern void pearlCode(void);
extern void NothingCode(void);
extern void fairyDuplicateCode(void);
extern void FakeGBCode(void);
extern void beaverExtraHitHandle(void);
extern void CBDing(void);
extern void handleSpiderTrapCode(void);
extern void fastWarpShockwaveFix(void);
extern int fixDilloTNTPads(void* actor);
extern int canPlayJetpac(void);
extern void setPrevSaveMap(void);

extern move_block* getMoveBlock(void);
extern void setLocationStatus(location_list location_index);
extern int getLocationStatus(location_list location_index);
extern void fixTBarrelsAndBFI(int init);
extern void purchaseMove(shop_paad* paad);
extern void getNextMoveText(void);
extern void displayBFIMoveText(void);
extern void showPostMoveText(shop_paad* paad, KongBase* kong_base, int intro_flag);
extern void fixRBSlowTurn(void);
extern void postKRoolSaveCheck(void);
extern int* displayHeadTexture(int* dl, int texture, float x, float y, float scale);

extern void tagBarrelBackgroundKong(int kong_actor);
extern void tagAnywhereInit(int is_homing, int model2_id, int obj);
extern void tagAnywhereAmmo(int player, int obj, int is_homing);
extern void tagAnywhereBunch(int player, int obj, int player_index);
extern void modifyCutscenePoint(int bank, int cutscene, int point, int new_item);
extern void modifyCutsceneItem(int bank, int item, int new_param1, int new_param2, int new_param3);
extern void modifyCutscenePanPoint(int bank, int item, int point_index, int x, int y, int z, int rot0, int rot1, int rot2, int zoom, int roll);
extern void modifyCutscenePointTime(int bank, int cutscene, int point, int new_time);
extern void modifyCutscenePointCount(int bank, int cutscene, int point_count);
extern void createCutscene(int bank, int cutscene, int point_count);
extern void HelmInit(int init_stage);
extern void initKRool(int phase);
extern void handleSFXCache(void);
extern void preventMedalHUD(int item, int unk0, int unk1);
extern void initHUDDirection(placementData* hud_data, int item);
extern int getObjectCollectability(int id, int unk1, int model2_type);
extern void* getHUDSprite_HUD(int item);
extern void updateMultibunchCount(void);
extern void handleDPadFunctionality(void);
extern void file_progress_screen_code(actorData* actor, int buttons);
extern int* displayTopText(int* dl, short x, short y, float scale);
extern void FileProgressInit(actorData* menu_controller);
extern void checkTotalCache(void);
extern void checkSeedVictory(void);
extern void checkVictory_flaghook(int flag);
extern void FileProgressInitSub(int file, int shuffle);
extern void changeFileSelectAction(menu_controller_paad* paad, int cap, int buttons);
extern void changeFileSelectAction_0(menu_controller_paad* paad, int cap);
extern void checkSkippableCutscene(void);
extern void updateSkippableCutscenes(void);
extern void parseCutsceneData(void);
//extern void getRandoNextMovePurchase(shop_paad* shop_info, KongBase* moves);
extern void adjustAnimationTables(void);
extern void adaptKrushaZBAnimation_PunchOStand(int action, void* player, int player_index);
extern void adaptKrushaZBAnimation_Charge(actorData* actor, int anim);
extern void updateCutsceneModels(actorData* actor, int size);
extern void* DiddySwimFix(int ptr, int file, int c0, int c1);
extern void updateUnderwaterCollisions(actorData* player, int anim, int unk0, int unk1);
extern void MinecartJumpFix(void* player, int anim);
extern void MinecartJumpFix_0(void);
extern void initTracker(void);
extern void resetTracker(void);
extern void wipeFileMod(int file, int will_save);
extern void enterFileProgress(int sfx);
extern void pokemonSnapMode(void);
extern int isSnapEnemyInRange(void);
extern int getPkmnSnapData(int* frames, int* current, int* total);
extern void updateSkippableCutscenes(void);
extern void renderScreenTransitionCheck(int applied_transition);
extern int updateLevelIGT(void);
extern int* printLevelIGT(int* dl, int x, int y, float scale, char* str);
extern void RabbitRaceInfiniteCode(void);
extern void completeBonus(actorData* actor);
extern void KasplatIndicator(int has_bp);
extern void spawnBonusReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1);
extern void spawnCrownReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1);
extern void spawnBossReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1);
extern void spawnDirtPatchReward(int object, int x_f, int y_f, int z_f, int unk0, int cutscene, int flag, int unk1);
extern void spawnRewardAtActor(int object, int flag);
extern void spawnMinecartReward(int object, int flag);
extern int checkFlagDuplicate(short flag, int type);
extern void setFlagDuplicate(short flag, int set, int type);
extern void* updateFlag(int type, short* flag, void* fba, int source);
extern void spawnEnemyDrops(actorData* actor);
extern int countFlagsForKongFLUT(int startFlag, int start, int cap, int kong);
extern int countFlagsDuplicate(int start, int count, int type);
extern int getKongFromBonusFlag(int flag);
extern void banana_medal_acquisition(int flag);
extern void finalizeBeatGame(void);

extern int getFlagIndex_Corrected(int start, int level);
extern int getBPItem(int index);
extern int getMedalItem(int index);
extern int getCrownItem(int map);
extern int getKeyItem(int old_flag);
extern int getFairyModel(int flag);
extern int getRainbowCoinItem(int old_flag);
extern int* controlKeyText(int* dl);
extern void keyGrabHook(int song, int vol);
extern int itemGrabHook(int collectable_type, int obj_type, int is_homing);
extern int getKeyFlag(int index);
extern int getKongFlag(int kong_index);
extern void PotionCode(void);
extern void KongDropCode(void);
extern int getMoveProgressiveFlagType(int flag);
extern void getItem(int object_type);
extern void checkModelTwoItemCollision(item_collision* obj_collision, int player_index, player_collision_info* player_collision);
extern int setupHook(int map);
extern void CheckKasplatSpawnBitfield(void);
extern void initActor(int actor_index, int is_custom, void* func, int master_type, int health, int damage_given, int initial_interactions, int base);
extern void refreshPads(pad_refresh_signals signal);

extern int* pauseScreen3And4Header(int* dl);
extern int* pauseScreen3And4Counter(int x, int y, int top, int bottom, int* dl, int unk0, int scale);
extern void updatePauseScreenWheel(void* write_location, void* sprite, int x, int y, float scale, int local_index, int index);
extern int* pauseScreen3And4ItemName(int* dl, int x, int y, float scale, char* text);
extern void handleSpriteCode(int control_type);
extern int changeSelectedLevel(int unk0, int unk1);
extern void checkItemDB(void);
extern void initPauseMenu(void);
extern void changePauseScreen(void);

extern void handleDynamicItemText(char* location, char* format, int character);
extern void mermaidCheck(void);
extern void initItemDictionary(void);
extern void initActorExpansion(void);
extern void initTextChanges(void);
extern void giveGB(int kong, int level);
extern void giveRainbowCoin(void);
extern void giveAmmo(void);
extern void giveOrange(void);
extern void giveMelon(void);
extern void giveCrystal(void);

extern int CrownDoorCheck(void);
extern int CoinDoorCheck(void);

extern int fairyQueenCutsceneInit(int start, int count, int type);
extern void fairyQueenCutsceneCheck(void);
extern void spawnCharSpawnerActor(int actor, SpawnerInfo* spawner);
extern void giveFairyItem(int flag, int state, int type);
extern void SpawnBarrel(spawnerPacket* packet);
extern void initBarrelChange(void);

extern void initIceTrap(void);
extern void queueIceTrap(void);
extern void callIceTrap(void);
extern int getPatchWorld(int index);

extern void initItemRando(void);
extern void initFiles(void);
extern void initQoL(void);
extern void initCosmetic(void);
extern void populatePatchItem(int id, int map, int index, int world);
extern int isObjectTangible_detailed(int id);

extern void insertROMMessages(void);
extern void handleModelTwoOpacity(short object_type, unsigned char* unk0, short* opacity);
extern int isTBarrelFlag(int flag);
extern int isFairyFlag(int flag);
extern int isFlagInRange(int test_flag, int start_flag, int count);
extern void BalloonShoot(int item, int player, int change);
extern void fixCrownEntrySKong(playerData* player, int animation);

extern void wipeHintCache(void);
extern void spawnWrinklyWrapper(behaviour_data* behaviour, int index, int kong, int unk0);

extern item_collision* writeItemScale(int id);
extern item_collision* writeItemActorScale(void);

extern unsigned int cs_skip_db[432];
extern bonus_barrel_info bonus_data[95];
extern const short kong_flags[5];
extern const short normal_key_flags[8];
extern const check_struct item_db[292];

extern sprite_data_struct bean_sprite;
extern sprite_data_struct pearl_sprite;
extern sprite_data_struct krool_sprite;

extern void* actor_functions[ACTOR_LIMIT];
extern health_damage_struct actor_health_damage[ACTOR_LIMIT];
extern short actor_interactions[ACTOR_LIMIT];
extern unsigned char actor_master_types[ACTOR_LIMIT];
extern short* actor_extra_data_sizes[ACTOR_LIMIT];
extern collision_data_struct actor_collisions[ACTOR_LIMIT];
extern collision_info object_collisions[COLLISION_LIMIT];