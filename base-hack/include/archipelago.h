#define ARCHIPELAGO_FLAG_START 0x320+static_expansion_size
#define ARCHIPELAGO_FLAG_SIZE 400

typedef enum archipelago_items {
    /* 0x000 */ TRANSFER_ITEM_NULL,
    /* 0x001 */ TRANSFER_ITEM_GB,
    /* 0x002 */ TRANSFER_ITEM_CROWN,
    /* 0x003 */ TRANSFER_ITEM_BP,
    /* 0x004 */ TRANSFER_ITEM_KEY1,
    /* 0x005 */ TRANSFER_ITEM_KEY2,
    /* 0x006 */ TRANSFER_ITEM_KEY3,
    /* 0x007 */ TRANSFER_ITEM_KEY4,
    /* 0x008 */ TRANSFER_ITEM_KEY5,
    /* 0x009 */ TRANSFER_ITEM_KEY6,
    /* 0x00A */ TRANSFER_ITEM_KEY7,
    /* 0x00B */ TRANSFER_ITEM_KEY8,
    /* 0x00C */ TRANSFER_ITEM_MEDAL,
    /* 0x00D */ TRANSFER_ITEM_NINTENDOCOIN,
    /* 0x00E */ TRANSFER_ITEM_RAREWARECOIN,
    /* 0x00F */ TRANSFER_ITEM_DK,
    /* 0x010 */ TRANSFER_ITEM_DIDDY,
    /* 0x011 */ TRANSFER_ITEM_LANKY,
    /* 0x012 */ TRANSFER_ITEM_TINY,
    /* 0x013 */ TRANSFER_ITEM_CHUNKY,
    /* 0x014 */ TRANSFER_ITEM_FAIRY,
    /* 0x015 */ TRANSFER_ITEM_RAINBOWCOIN,
    /* 0x016 */ TRANSFER_ITEM_BEAN,
    /* 0x017 */ TRANSFER_ITEM_PEARL,
    /* 0x018 */ TRANSFER_ITEM_FAKEITEM,
    /* 0x019 */ TRANSFER_ITEM_JUNKITEM,
    /* 0x01A */ TRANSFER_ITEM_BABOONBLAST,
    /* 0x01B */ TRANSFER_ITEM_STRONGKONG,
    /* 0x01C */ TRANSFER_ITEM_GORILLAGRAB,
    /* 0x01D */ TRANSFER_ITEM_CHIMPYCHARGE,
    /* 0x01E */ TRANSFER_ITEM_ROCKETBARREL,
    /* 0x01F */ TRANSFER_ITEM_SIMIANSPRING,
    /* 0x020 */ TRANSFER_ITEM_ORANGSTAND,
    /* 0x021 */ TRANSFER_ITEM_BABOONBALLOON,
    /* 0x022 */ TRANSFER_ITEM_ORANGSTANDSPRINT,
    /* 0x023 */ TRANSFER_ITEM_MINIMONKEY,
    /* 0x024 */ TRANSFER_ITEM_TWIRL,
    /* 0x025 */ TRANSFER_ITEM_MONKEYPORT,
    /* 0x026 */ TRANSFER_ITEM_HUNKYCHUNKY,
    /* 0x027 */ TRANSFER_ITEM_PRIMATEPUNCH,
    /* 0x028 */ TRANSFER_ITEM_GORILLAGONE,
    /* 0x029 */ TRANSFER_ITEM_BONGOS,
    /* 0x02A */ TRANSFER_ITEM_GUITAR,
    /* 0x02B */ TRANSFER_ITEM_TROMBONE,
    /* 0x02C */ TRANSFER_ITEM_SAX,
    /* 0x02D */ TRANSFER_ITEM_TRIANGLE,
    /* 0x02E */ TRANSFER_ITEM_COCONUT,
    /* 0x02F */ TRANSFER_ITEM_PEANUT,
    /* 0x030 */ TRANSFER_ITEM_GRAPE,
    /* 0x031 */ TRANSFER_ITEM_FEATHER,
    /* 0x032 */ TRANSFER_ITEM_PINEAPPLE,
    /* 0x033 */ TRANSFER_ITEM_SLAMUPGRADE,
    /* 0x034 */ TRANSFER_ITEM_HOMING,
    /* 0x035 */ TRANSFER_ITEM_SNIPER,
    /* 0x036 */ TRANSFER_ITEM_BELTUPGRADE,
    /* 0x037 */ TRANSFER_ITEM_INSTRUMENTUPGRADE,
    /* 0x038 */ TRANSFER_ITEM_CAMERA,
    /* 0x039 */ TRANSFER_ITEM_SHOCKWAVE,
    /* 0x03A */ TRANSFER_ITEM_CAMERASHOCKWAVECOMBO,
    /* 0x03B */ TRANSFER_ITEM_DIVE,
    /* 0x03C */ TRANSFER_ITEM_ORANGE,
    /* 0x03D */ TRANSFER_ITEM_BARREL,
    /* 0x03E */ TRANSFER_ITEM_VINE,
    /* 0x03F */ TRANSFER_ITEM_CLIMBING,
    /* 0x040 */ TRANSFER_ITEM_FAKEITEM_SLOW,
    /* 0x041 */ TRANSFER_ITEM_FAKEITEM_REVERSE,
} archipelago_items;

typedef struct archipelago_data {
    /* 0x000 */ unsigned short counter;
    /* 0x002 */ unsigned short start_flag;
    /* 0x004 */ archipelago_items fed_item;
    /* 0x008 */ char fed_string[0x21]; // 0x20 characters followed by null terminator
    /* 0x029 */ unsigned char connection;
    /* 0x02A */ unsigned char safety_text_timer; // Timer for when it's *safe* to send another string in
    /* 0x02B */ char fed_subtitle[0x21]; // 0x20 characters followed by null terminator
    /* 0x04C */ char slot_name[0x10];
    /* 0x05C */ char send_death; // If donk player dies. Set this back to 0 upon receiving that the donk player has died
    /* 0x05D */ char receive_death; // If someone else dies, this will kill the donk player
    /* 0x05E */ char can_die; // If death is received, the game will queue the death until this is 1. It's generally a good idea to not send a death to the donk player if this is zero 
    /* 0x05F */ unsigned char text_timer;
    /* 0x060 */ char tag_kong; // Byte to set the current kong to this. Check can_tag before setting this if you want safety
    /* 0x061 */ unsigned char can_tag;
} archipelago_data;

extern archipelago_data *APData;
extern void handleArchipelagoFeed(void);
extern int isFlagAPItem(int flag);
extern void initAP(void);
extern void initAPCounter(void);
extern void saveAPCounter(void);
extern int isAPEnabled(void);
extern void sendDeath(void);
extern Gfx *displayAPConnection(Gfx *dl);