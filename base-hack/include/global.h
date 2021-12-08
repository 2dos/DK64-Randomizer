#include "vars.h"

extern void playSFX(short sfxIndex);
extern void setPermFlag(short flagIndex);
extern int convertIDToIndex(short obj_index);
extern void* findActorWithType(int search_actor_type);
extern int isRDRAM(void* address);
extern void customHideHUD(void);
extern void setWarpPosition(float x, float y, float z);
extern void initHack(void);

extern void level_order_rando_funcs(void);
extern void unlockKongs(void);
extern void unlockMoves(void);
extern void tagAnywhere(void);
extern void islesSpawn(void);
extern void applyFastStart(void);
extern void fixCastleAutowalk(void);
extern void openCrownDoor(void);
extern void openCoinDoor(void);
extern void qualityOfLife_fixes(void);
extern void qualityOfLife_shorteners(void);