#include "vars.h"

extern void playSFX(short sfxIndex);
extern void setPermFlag(short flagIndex);
extern int convertIDToIndex(short obj_index);
extern void* findActorWithType(int search_actor_type);
extern int isRDRAM(void* address);
extern void customHideHUD(void);
extern void setWarpPosition(float x, float y, float z);
extern void initHack(void);
extern void callParentMapFilter(void);
extern void shiftBrokenJapesPortal(void);

extern void level_order_rando_funcs(void);
extern void unlockKongs(void);
extern void unlockMoves(void);
extern void tagAnywhere(int prev_crystals);
extern void islesSpawn(void);
extern void applyFastStart(void);
extern void fixCastleAutowalk(void);
extern void openCrownDoor(void);
extern void openCoinDoor(void);
extern void qualityOfLife_fixes(void);
extern void qualityOfLife_shorteners(void);
extern void decouple_moves_fixes(void);
extern void price_rando(void);
extern void determine_krool_order(void);
extern void replace_zones(int init_flag);
extern void randomize_bosses(void);
extern void alter_boss_key_flags(void);
extern void displayNumberOnTns(void);
extern void replace_moves(void);
extern void updateProgressive(void);
extern void moveTransplant(void);
extern void priceTransplant(void);

extern void changeCharSpawnerFlag(int map, int spawner_id, int new_flag);
extern void changeHelmLZ(void);

extern void PatchCrankyCode(void);
extern void PatchKRoolCode(void);
extern void PatchBonusCode(void);
extern void FileScreenDLCode_Write(void);
extern void write_kutoutorder(void);
extern void remove_blockers(void);
extern void disable_krool_health_refills(void);
extern void pre_turn_keys(void);
extern void handle_WTI(void);
extern void no_enemy_drops(void);
extern void cancelMoveSoftlock(void);
extern void adjust_galleon_water(void);

extern int convertSubIDToIndex(short obj_index);
extern int change_object_scripts(behaviour_data* behaviour_pointer, int id, int index, int param2);
extern void setCrusher(void);
extern void createCollisionObjInstance(collision_types subtype, int map, int exit);
extern int spawnCannonWrapper(void);
extern void fixkey8(void);
extern void alterGBKong(int map, int id, int new_kong);
extern void fixDKFreeSoftlock(void);

extern void preventBossCheese(void);
extern void determineStartKong_PermaLossMode(void);
extern void kong_has_died(void);
extern int curseRemoved(void);
extern void forceBossKong(void);
extern int hasPermaLossGrace(void);

extern void writeJetpacMedalReq(void);
extern void resetMapContainer(void);
extern void correctDKPortal(void);

extern int* drawTri(int* dl, short x1, short y1, short x2, short y2, short x3, short y3, int red, int green, int blue, int alpha);
extern int* drawImage(int* dl, int text_index, codecs codec_index, int img_width, int img_height, int x, int y, float xScale, float yScale, int opacity);
extern int* drawPixelText(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha);
extern int* drawPixelTextContainer(int* dl, int x, int y, char* str, int red, int green, int blue, int alpha, int offset);
extern int* drawScreenRect(int* dl, int x1, int y1, int x2, int y2, int red, int green, int blue, int alpha);
extern int* drawTextContainer(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity, int background);
extern int* drawText(int* dl, int style, float x, float y, char* str, int red, int green, int blue, int opacity);
extern void correctKongFaces(void);

extern void displayNumberOnObject(int id, int param2, int imageindex, int param4, int subtype);
extern void recolorKongControl(void);
extern void newCounterCode(void);
extern void writeCoinRequirements(int source);
extern void colorMenuSky(void);
extern void getMoveHint(actorData* actor, int text_file, int text_index);
extern void cutsceneDKCode(void);
//extern void getRandoNextMovePurchase(shop_paad* shop_info, KongBase* moves);