#include "../../include/common.h"

typedef struct drop_item {
    /* 0x000 */ short source_object;
    /* 0x002 */ short dropped_object;
    /* 0x004 */ unsigned char drop_music;
    /* 0x005 */ unsigned char drop_count;
} drop_item;

static drop_item drops[29] = {};

int addItemDrop(int source_object, int drop_object, int drop_music, int drop_count, int drop_total) {
    if (Rando.disable_drops) {
        if (source_object != 0) {
            if ((drop_object == 0x2F) || (drop_object == 0x34) || (drop_object == 0x33)) {
                source_object = 3;
            }
        }
    }
    drops[drop_total].source_object = source_object;
    drops[drop_total].dropped_object = drop_object;
    drops[drop_total].drop_music = drop_music;
    drops[drop_total].drop_count = drop_count;
    return drop_total + 1;
}

void buildItemDrops(void) {
    int drop_total = 0;
    drop_total = addItemDrop(0xB2,0x2F,0x2F,1,drop_total); // Beaver (Blue)
    drop_total = addItemDrop(0xD4,0x2F,0x2F,2,drop_total); // Beaver (Gold)
    drop_total = addItemDrop(0xCD,0x2F,0x2F,1,drop_total); // Green Klaptrap
    drop_total = addItemDrop(0xD0,0x34,0x00,3,drop_total); // Purple Klaptrap
    drop_total = addItemDrop(0xD1,0x33,0x00,1,drop_total); // Red Klaptrap
    drop_total = addItemDrop(0x03,0x35,0x00,3,drop_total); // Diddy
    drop_total = addItemDrop(0xF1,0x4E,0x4C,1,drop_total); // Kasplat (DK)
    drop_total = addItemDrop(0xF2,0x4B,0x4C,1,drop_total); // Kasplat (Diddy)
    drop_total = addItemDrop(0xF3,0x4D,0x4C,1,drop_total); // Kasplat (Lanky)
    drop_total = addItemDrop(0xF4,0x4F,0x4C,1,drop_total); // Kasplat (Tiny)
    drop_total = addItemDrop(0xF5,0x4C,0x4C,1,drop_total); // Kasplat (Chunky)
    drop_total = addItemDrop(0xBB,0x34,0x00,3,drop_total); // Klump
    drop_total = addItemDrop(0xEE,0x2F,0x2F,1,drop_total); // Kremling
    drop_total = addItemDrop(0xEB,0x2F,0x2F,2,drop_total); // Robo Kremling
    drop_total = addItemDrop(0x123,0x2F,0x2F,2,drop_total); // Kosha
    drop_total = addItemDrop(0xB7,0x2F,0x2F,1,drop_total); // Zinger
    drop_total = addItemDrop(0xCE,0x2F,0x2F,1,drop_total); // Zinger
    drop_total = addItemDrop(0x105,0x2F,0x2F,1,drop_total); // Robo-Zinger
    drop_total = addItemDrop(0x11D,0x2F,0x2F,1,drop_total); // Bat
    drop_total = addItemDrop(0x10F,0x2F,0x2F,1,drop_total); // Mr. Dice
    drop_total = addItemDrop(0x10E,0x2F,0x2F,1,drop_total); // Sir Domino
    drop_total = addItemDrop(0x10D,0x2F,0x2F,1,drop_total); // Mr. Dice
    drop_total = addItemDrop(0xE0,0x2F,0x2F,1,drop_total); // Mushroom Man
    drop_total = addItemDrop(0x106,0x2F,0x2F,1,drop_total); // Krossbones
    drop_total = addItemDrop(0x121,0x2F,0x2F,1,drop_total); // Ghost
    drop_total = addItemDrop(0xB6,0x2F,0x2F,1,drop_total); // Klobber
    drop_total = addItemDrop(0xAF,0x2F,0x2F,1,drop_total); // Kaboom
    drop_total = addItemDrop(0x103,0x33,0x0,1,drop_total); // Guard
    drop_total = addItemDrop(0,0,0,0,drop_total);
}

int getLo(void* addr) {
    return ((int)addr) & 0xFFFF;
}

int getHi(void* addr) {
    int addr_0 = (int)addr;
    int hi = (addr_0 >> 16) & 0xFFFF;
    int lo = getLo(addr);
    if (lo & 0x8000) {
        hi += 1;
    }
    return hi;
}

void initItemDropTable(void) {
    buildItemDrops();
    *(short*)(0x806A5CA6) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CB6) = getLo(&drops[0].source_object);

    *(short*)(0x806A5CBA) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CBE) = getLo(&drops[0].source_object);

    *(short*)(0x806A5CD2) = getHi(&drops[0].source_object);
    *(short*)(0x806A5CD6) = getLo(&drops[0].source_object);
}