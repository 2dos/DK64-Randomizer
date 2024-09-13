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
extern int giveSlamLevel(void);
extern int isSlamFlag(int flag);
extern int isBeltFlag(int flag);
extern int isInstrumentUpgradeFlag(int flag);
extern int inBattleCrown(maps map);
extern int inTraining(maps map);
extern int inShop(maps map, int include_snide);
extern int inBossMap(maps map, int include_regular, int include_krool, int include_shoe);
extern int inMinigame(maps map);
extern int isGamemode(gamemodes target_mode, int force_both);
extern int has_key(int index);
extern overlays getOverlayFromMap(maps map);
extern void* malloc_wipe(int size);
extern int applyDamageMask(int player_index, int damage);
extern void* replaceWaterTexture(int table, int file, int unk0, int unk1);
extern void* replaceWaterTexture_spooky(int table, int file, int unk0, int unk1);
extern int isBounceObject(int object);

extern int getEnemyItem(int id);
extern int getEnemyFlag(int id);
extern void setEnemyDBPopulation(int value);
extern void populateEnemyMapData(void);

extern int getLo(void* addr);
extern int getHi(void* addr);

extern int hasChunkyPhaseSlam(void);
extern void fixKRoolKong(void);

extern void level_order_rando_funcs(void);
extern void unlockMoves(void);
extern void tagAnywhere(void);
extern void applyFastStart(void);
extern void openCrownDoor(void);
extern void openCoinDoor(void);
extern void qualityOfLife_fixes(void);
extern void qualityOfLife_shorteners(void);
extern void overlay_changes(void);
extern void handleKRoolSaveProgress(void);
extern void replace_zones(int init_flag);
extern void displayNumberOnTns(void);
extern void moveTransplant(void);
extern void priceTransplant(void);

extern void changeCharSpawnerFlag(maps map, int spawner_id, int new_flag);
extern void HelmBarrelCode(void);
extern void WarpHandle(void);

extern int correctRefillCap(int index, int player);
extern void cc_effect_handler(void);

extern void PatchCrankyCode(void);
extern void PatchKRoolCode(void);
extern void PatchBonusCode(void);
extern void kioskBugCode(void);
extern void FileScreenDLCode_Write(void);
extern void pre_turn_keys(void);
extern void auto_turn_keys(void);
extern void handle_WTI(void);
extern void warpToIsles(void);
extern void adjust_level_modifiers(void);
extern void handleTimeOfDay(time_of_day_calls call);

extern void initKongRando(void);

extern int getMedalCount(void);
extern int isMedalFlag(int flag);

extern int convertSubIDToIndex(short obj_index);
extern int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2);
extern void setCrusher(void);
extern void createCollisionObjInstance(collision_types subtype, int map, int exit);
extern int spawnCannonWrapper(void);
extern void disableDiddyRDDoors(void);
extern void fixkey8(void);
extern void alterGBKong(maps map, int id, int new_kong);

extern void preventBossCheese(void);
extern void determineStartKong_PermaLossMode(void);
extern void kong_has_died(void);
extern int curseRemoved(void);
extern void forceBossKong(void);
extern int hasPermaLossGrace(maps map);
extern void fixGraceCheese(void);

extern void resetMapContainer(void);
extern void correctDKPortal(void);
extern int canSaveHelmHurry(void);
extern void addHelmTime(helm_hurry_items item, int multiplier);
extern void saveHelmHurryTime(void);
extern void writeDefaultFilename(void);
extern void wipeFileStats(void);

extern int getHelmExit(void);

extern Gfx* drawTri(Gfx* dl, short x1, short y1, short x2, short y2, short x3, short y3, int red, int green, int blue, int alpha);
extern Gfx* drawImage(Gfx* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity);
extern Gfx* drawPixelText(Gfx* dl, int x, int y, char* str, int red, int green, int blue, int alpha);
extern Gfx* drawPixelTextContainer(Gfx* dl, int x, int y, char* str, int red, int green, int blue, int alpha, int offset);
extern Gfx* drawScreenRect(Gfx* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha);
extern Gfx* drawTextContainer(Gfx* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background);
extern Gfx* drawText(Gfx* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity);
extern Gfx* drawDPad(Gfx* dl);
extern Gfx* drawImageWithFilter(Gfx* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int red, int green, int blue, int opacity);
extern void correctKongFaces(void);

extern Gfx* display_file_images(Gfx* dl, int y_offset);
extern Gfx* drawTextPointers(Gfx* dl);
extern Gfx* displayCenteredText(Gfx* dl, int y, char* str, int offset);
extern void applyHintRecoloring(letter_data* data, int index, int bitfield, char* char_address);
extern void setCharacterRecoloring(int output, char* stored_str);
extern void setCharacterColor(int index, int value, int opacity);
extern void wipeTextColorData(void);

extern int getLo(void* addr);
extern int getHi(void* addr);

extern void displayNumberOnObject(int id, int param2, int imageindex, int param4, int subtype);
extern void newCounterCode(void);
extern void wipeCounterImageCache(void);
extern void getMoveHint(actorData* actor, int text_file, int text_index);
extern void cutsceneDKCode(void);

extern void fastWarp_playMusic(void* actor);
extern void fixCutsceneModels(void);
extern void updateActorHandStates(actorData* actor, int type);
extern void updateActorHandStates_gun(actorData* actor, int type);
extern void clearGunHandler(actorData* actor);

extern void guardCatch(void);
extern void guardCatchInternal(void);
extern void dummyGuardCode(void);
extern void catchWarpHandle(void);
extern void handleFootProgress(actorData* actor);
extern void cancelCutscene(int enable_movement);
extern void clearVultureCutscene(void);
extern void fastWarp(void* actor, int player_index);

extern int isKrushaAdjacentModel(int kong);
extern int isGlobalCutscenePlaying(int cutscene_index);
extern void adjustGunBone(playerData* player);

extern int getTagAnywhereKong(int direction);
extern int getTAState(void);
extern int hasAccessToKong(int kong);
extern void changeKong(int next_character);
extern void toggleStandardAmmo(void);
extern void initTagAnywhere(void);
extern void initItemDropTable(void);
extern void initCollectableCollision(void);
extern void initActorDefs(void);
extern void updateKopStat(void);
extern void newGuardCode(void);
extern void goldBeaverCode(void);
extern void ninCoinCode(void);
extern void rwCoinCode(void);
extern void medalCode(void);
extern void beanCode(void);
extern void pearlCode(void);
extern void NothingCode(void);
extern void fairyDuplicateCode(void);
extern void shopOwnerItemCode(void);
extern void FakeGBCode(void);
extern void beaverExtraHitHandle(void);
extern void CBDing(void);
extern Gfx* renderIndicatorSprite(Gfx* dl, int sprite, int dim, unsigned char* timer, int width, int height, codecs codec);
extern Gfx* renderDingSprite(Gfx* dl);
extern Gfx* renderProgressiveSprite(Gfx* dl);
extern int getHintGBRequirement(int slot);
extern void gbUpdateHandler(void);
extern void handleProgressiveIndicator(int delta);
extern int hasEnoughCBs(void);
extern void initDingSprite(void);
extern void fastWarpShockwaveFix(void);
extern void setPrevSaveMap(void);
extern int filterSong(int* song_write);
extern int getTotalCBCount(void);

extern void setLocationStatus(location_list location_index);
extern int getLocationStatus(location_list location_index);
extern void getNextMoveText(void);
extern Gfx* displayHeadTexture(Gfx* dl, int texture, float x, float y, float scale);

extern void* getFile(int size, int rom);

extern int CanDive_WithCheck(void);
extern void playTransformationSong(songs song, float volume);

extern void updateBarrierCounts(void);
extern void displayBarrierHUD(item_ids item, int persist);
extern void swap_ending_cutscene_model(void);

extern void tagBarrelBackgroundKong(int kong_actor);
extern void modifyCutscenePoint(int bank, int cutscene, int point, int new_item);
extern void modifyCutsceneItem(int bank, int item, int new_param1, int new_param2, int new_param3);
extern void modifyCutscenePanPoint(int bank, int item, int point_index, int x, int y, int z, int rot0, int rot1, int rot2, int zoom, int roll);
extern void modifyCutscenePointTime(int bank, int cutscene, int point, int new_time);
extern void modifyCutscenePointCount(int bank, int cutscene, int point_count);
extern void createCutscene(int bank, int cutscene, int point_count);
extern void HelmInit(int init_stage);
extern void handleSFXCache(void);
extern void preventMedalHUD(int item, int unk0, int unk1);
extern int getObjectCollectability(int id, int unk1, int model2_type);
extern void* getHUDSprite_HUD(int item);
extern void updateMultibunchCount(void);
extern void handleDPadFunctionality(void);
extern void file_progress_screen_code(actorData* actor, int buttons);
extern Gfx* displayTopText(Gfx* dl, short x, short y, float scale);
extern void FileProgressInit(actorData* menu_controller);
extern void checkTotalCache(void);
extern void checkSeedVictory(void);
extern void checkVictory_flaghook(int flag);
extern void FileProgressInitSub(int file, int shuffle);
extern void handleFileSelectSprites(void* paad, void* sprite, int x, int y, float scale, int unk0, int control);
extern void checkSkippableCutscene(void);
extern void updateSkippableCutscenes(void);
//extern void getRandoNextMovePurchase(shop_paad* shop_info, KongBase* moves);
extern void adjustAnimationTables(void);
extern void adaptKrushaZBAnimation_PunchOStand(int action, void* player, int player_index);
extern void adaptKrushaZBAnimation_Charge(actorData* actor, int anim);
extern void OrangeGunCode(void);
extern void changeFeatherToSprite(void);
extern void setActorDamage(int actor, int new_damage);
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
extern void pressSkipHandler(void* actor);
extern void clearSkipCache(void);
extern void updateSkipCheck(void);
extern void renderScreenTransitionCheck(int applied_transition);
extern void melonCrateItemHandler(behaviour_data* behaviour_pointer, int index, int p1, int p2);
extern int checkFlagDuplicate(short flag, flagtypes type);
extern void setFlagDuplicate(short flag, int set, flagtypes type);
extern void* updateFlag(flagtypes type, short* flag, void* fba, int source);
extern void spawnEnemyDrops(actorData* actor);
extern int countFlagsDuplicate(int start, int count, flagtypes type);
extern void* checkMove(short* flag, void* fba, int source, int vanilla_flag);
extern int hasMove(int flag);

extern void finalizeBeatGame(void);
extern void exitTrapBubbleController(void);

extern int getFlagIndex_Corrected(int start, int level);
extern int getFlagIndex_MedalCorrected(int start, int level);
extern int getBPItem(int index);
extern int getMedalItem(int index);
extern int getWrinklyItem(int index);
extern int getCrownItem(maps map);
extern int getKeyItem(int old_flag);
extern int getFairyModel(int flag);
extern int getRainbowCoinItem(int old_flag);
extern int getCrateItem(int old_flag);
extern Gfx* controlKeyText(Gfx* dl);
extern void keyGrabHook(int song, float vol);
extern int getKeyFlag(int index);
extern int getKongFlag(int kong_index);
extern void PotionCode(void);
extern void KongDropCode(void);
extern int getMoveProgressiveFlagType(int flag);
extern void getItem(int object_type);
extern void checkModelTwoItemCollision(item_collision* obj_collision, int player_index, player_collision_info* player_collision);
extern void CheckKasplatSpawnBitfield(void);
extern void initActor(int actor_index, int is_custom, void* func, int master_type, int health, int damage_given, int initial_interactions, int base);
extern void setCollisionAddress(int actor_index, int is_custom, void* collision_info, int subdata);
extern void refreshPads(pad_refresh_signals signal);

extern int stompHandler(void* unk0, playerData* player, int unk1);

extern void indicateCollectionStatus(void);
extern void fireballEnemyDeath(float x, float y, float z, float scale, char unk0, char unk1);
extern void rulerEnemyDeath(void);
extern int canSpawnEnemyReward(void);
extern void wipeEnemySpawnBitfield(void);
extern void setSpawnBitfield(int id, int state);
extern void setSpawnBitfieldFromFlag(int flag, int state);

extern Gfx* pauseScreen3And4ItemName(Gfx* dl, int x, int y, float scale, char* text);
extern void handleSpriteCode(int control_type);
extern void initPauseMenu(void);
extern void storeHintRegion(void);
extern void getHintRegionText(void);
extern void initCarousel_onPause(void);
extern void initCarousel_onBoot(void);
extern Gfx* drawHintScreen(Gfx* dl, int level_x);
extern Gfx* drawItemLocationScreen(Gfx* dl, int level_x);
extern void handleCShifting(char* value, char limit);
extern void initHints(void);
extern void initHintFlags(void);

extern void handleFilename(char* location, char* format, char* new_name);
extern void initItemDictionary(void);
extern void initActorExpansion(void);
extern void initTextChanges(void);
extern void giveGB(int kong, int level);
extern void giveRainbowCoin(void);
extern void giveAmmo(void);
extern void giveOrange(void);
extern void giveMelon(void);
extern void giveCrystal(void);
extern int inShortList(int target, short* list, int count);

extern int CrownDoorCheck(void);
extern int CoinDoorCheck(void);

extern void alterChunkData(void* data);
extern void shineLight(actorData* actor, int kongType);
extern void fallDamageWrapper(int action, void* actor, int player_index);
extern void transformBarrelImmunity(void);
extern void factoryShedFallImmunity(short exit);
extern void handleFallDamageImmunity(void);
extern void warpOutOfTraining(void);
extern Gfx* displayNoGeoChunk(Gfx* dl, int chunk_index, int shift);

extern void initIceTrap(void);
extern int isBannedTrapMap(maps map, ICE_TRAP_TYPES type);
extern void queueIceTrap(ICE_TRAP_TYPES trap_type);
extern void callIceTrap(void);
extern int getPatchWorld(int index);
extern int getCrateWorld(int index);
extern int getCrateFlag(int id);

extern void initItemRando(void);
extern void initQoL(void);
extern void initCosmetic(void);
extern void populatePatchItem(int id, int map, int index, int world);
extern void populateCrateItem(int id, int map, int index, int world);
extern int isObjectTangible_detailed(int id);

extern void insertROMMessages(void);
extern int isTBarrelFlag(int flag);
extern int isFairyFlag(int flag);
extern int isFlagInRange(int test_flag, int start_flag, int count);

extern void wipeHintCache(void);
extern void spawnWrinklyWrapper(behaviour_data* behaviour, int index, int kong, int unk0);

extern int initFile_hasGun(int kong);
extern int initFile_hasInstrument(int kong);
extern int initFile_getBeltLevel(int inc_training);
extern int initFile_getInsUpgradeLevel(int inc_training);
extern int initFile_getSlamLevel(int inc_training);
extern int initFile_getKongPotionBitfield(int kong);
extern int initFile_checkTraining(int type_check, int kong_check, int value_check);

extern void fixHelmTimerCorrection(void);
extern void exitBoss(void);

extern int changeStat(bonus_stat statistic, int delta);
extern int getStat(bonus_stat statistic);
extern void setStat(bonus_stat statistic, int amount);
extern void setKongIgt(void);
extern int ReadExtraData(extra_global_data data_type, int sub_index);
extern void SaveExtraData(extra_global_data data_type, int sub_index, int value);
extern void ResetExtraData(extra_global_data data_type, int sub_index);
extern void setKrushaAmmoColor(void);

extern void handleCannonGameReticle(void);

extern void cFuncLoop(void);
extern void overlay_mod_menu(void);
extern void overlay_mod_critter(void);
extern void overlay_mod_boss(void);
extern void overlay_mod_bonus(void);
extern void initJetpac(void);
extern void overlay_mod_race(void);

extern int getTrackerYOffset(void);

extern void hideObject(behaviour_data* behaviour_pointer);
extern void bananaportGenericCode(behaviour_data* behaviour, int index, int id);
extern void TNSPortalGenericCode(behaviour_data* behaviour, int index, int id);
extern void TNSIndicatorGenericCode(behaviour_data* behaviour, int index, int id);
extern void CrownPadGenericCode(behaviour_data* behaviour, int index, int id, int crown_level_index);
extern void MelonCrateGenericCode(behaviour_data* behaviour, int index, int id);
extern int isBonus(maps map);
extern int randomGunSwitchGenericCode(behaviour_data* behaviour_pointer, int index, int switch_index);
extern int randomInstrumentGenericCode(behaviour_data* behaviour_pointer, int index, int pad_index);
extern int checkControlState(int target_control_state);
extern int checkSlamLocation(int kong, int key, int id);
extern void playSFXContainer(int id, int vanilla_sfx, int new_sfx);
extern int getPressedSwitch(behaviour_data* behaviour_pointer, int bullet_type, int ID);
extern void getModelTwoItemFromActor(int actor, short* item, float* scale);
extern void IslesMonkeyportCode(behaviour_data* behaviour_pointer, int index);
extern void HelmLobbyGoneCode(behaviour_data* behaviour_pointer, int index);
extern void initSwitchsanityChanges(void);
extern void setObjectOpacity(behaviour_data* behaviour_pointer, int opacity);
extern int standingOnM2Object(int index);

extern int getItemCountReq(requirement_item item);
extern int isItemRequirementSatisfied(ItemRequirement* req);
extern dynamic_flag_icetrap_junk isIceTrapFlag(int flag);

extern int getGamePercentage(void);

extern void displayMedalOverlay(int flag, int item_type);

extern void handleCrownTimerInternal(void);

extern void initSongDisplay(int song);
extern void newSongIsLoading(int write_slot, int song, float volume);
extern Gfx* displaySongNameHandler(Gfx* dl);
extern void resetDisplayedMusic(void);

extern enum_bonus_skin getBarrelSkinIndex(int actor);
extern void crankyCodeHandler(void);
extern void funkyCodeHandler(void);
extern void candyCodeHandler(void);
extern void snideCodeHandler(void);

extern int canPlayerClimb(void);

extern purchase_struct* getShopData(vendors vendor, int kong, int level);
extern void playBalloonWhoosh(int path_index, float* x, float* y, float* z);

extern unsigned int cs_skip_db[432];
extern bonus_barrel_info bonus_data[BONUS_DATA_COUNT];
extern const short kong_flags[5];
extern const short normal_key_flags[8];
extern short tbarrel_flags[4];
extern short bfi_move_flags[2];
extern const short tnsportal_flags[7];
extern const unsigned short slam_flags[6];
extern const unsigned short belt_flags[4];
extern const unsigned short instrument_flags[6];
extern const unsigned char kong_pellets[5];
extern const rgb colorblind_colors[15];
extern const check_struct item_db[297];
extern const unsigned char crown_maps[10];
extern const unsigned char regular_boss_maps[7];
extern char* levels[10];
extern unsigned int dark_mode_colors[10];

extern sprite_data_struct bean_sprite;
extern sprite_data_struct pearl_sprite;
extern sprite_data_struct krool_sprite;
extern sprite_data_struct feather_gun_sprite;
extern sprite_data_struct fool_overlay_sprite;

extern void* actor_functions[ACTOR_LIMIT];
extern health_damage_struct actor_health_damage[ACTOR_LIMIT];
extern short actor_interactions[ACTOR_LIMIT];
extern unsigned char actor_master_types[ACTOR_LIMIT];
extern short* actor_extra_data_sizes[ACTOR_LIMIT];
extern collision_data_struct actor_collisions[ACTOR_LIMIT];
extern collision_info object_collisions[COLLISION_LIMIT];
extern unsigned char enemy_rewards_spawned[ENEMY_REWARD_CACHE_SIZE];

extern mtx_item static_mtx[22];
extern int hint_pointers[35];
extern char* itemloc_pointers[LOCATION_ITEM_COUNT];
extern char music_types[SONG_COUNT];
extern char filename[FILENAME_LENGTH + 1];
extern char grab_lock_timer;
extern char tag_locked;
extern char enable_skip_check;
extern int force_enable_diving_timer;

extern unsigned int base_text_color;
extern unsigned int emph_text_colors[10];
extern unsigned char HeadSize[MODEL_COUNT];
extern const char big_head_actors[MODEL_COUNT];

// Items we're extern-ing for usage with "ASMPatcher.py"
// DON'T REMOVE UNLESS YOU KNOW WHAT YOU'RE DOING
extern int balloon_path_pointers[PATH_CAP];
extern drop_item drops[DROP_COUNT];
extern int file_sprites[17];
extern short file_items[16];
extern short file_item_caps[16];
extern ICE_TRAP_TYPES ice_trap_queued;
extern const collision_tree_struct fixed_shockwave_collision[3];
extern const collision_tree_struct fixed_scarab_collision[4];
extern const collision_tree_struct fixed_dice_collision[12];
extern const collision_tree_struct fixed_klap_collision[8];
extern const collision_tree_struct fixed_bug_collision[2];
