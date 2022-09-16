#include "../../include/common.h"

#define WARPLEVELCOUNT 8 // # 9 if you included Helm warps

static const short warpflags_japes[] = {
	FLAG_WARP_JAPES_W1_PORTAL,
	FLAG_WARP_JAPES_W1_FAR,
	FLAG_WARP_JAPES_W2_HIGH,
	FLAG_WARP_JAPES_W2_LOW,
	FLAG_WARP_JAPES_W3_RIGHT,
	FLAG_WARP_JAPES_W3_LEFT,
	FLAG_WARP_JAPES_W4_CLOSE,
	FLAG_WARP_JAPES_W4_CRANKY,
	FLAG_WARP_JAPES_W5_SHELLHIVE,
	FLAG_WARP_JAPES_W5_TOP,
};
static const short warpflags_aztec[] = {
	FLAG_WARP_AZTEC_W1_PORTAL,
	FLAG_WARP_AZTEC_W1_CANDY,
	FLAG_WARP_AZTEC_W2_TEMPLE,
	FLAG_WARP_AZTEC_W2_TOTEM,
	FLAG_WARP_AZTEC_W3_CRANKY,
	FLAG_WARP_AZTEC_W3_TOTEM,
	FLAG_WARP_AZTEC_W4_TOTEM,
	FLAG_WARP_AZTEC_W4_FUNKY,
	FLAG_WARP_AZTEC_W5_TOTEM,
	AZTEC_SNOOPW5, // Custom Flag
	FLAG_WARP_LLAMA_W1_HIGH,
	FLAG_WARP_LLAMA_W1_LOW,
	FLAG_WARP_LLAMA_W2_FAR,
	FLAG_WARP_LLAMA_W2_LOW,
};
static const short warpflags_factory[] = {
	FLAG_WARP_FACTORY_W1_FOYER,
	FLAG_WARP_FACTORY_W1_STORAGE,
	FLAG_WARP_FACTORY_W2_FOYER,
	FLAG_WARP_FACTORY_W2_RND,
	FLAG_WARP_FACTORY_W3_FOYER,
	FLAG_WARP_FACTORY_W3_SNIDE,
	FLAG_WARP_FACTORY_W4_TOP,
	FLAG_WARP_FACTORY_W4_BOTTOM,
	FLAG_WARP_FACTORY_W5_FUNKY,
	FLAG_WARP_FACTORY_W5_ARCADE,
};
static const short warpflags_galleon[] = {
	FLAG_WARP_GALLEON_W1_LIGHTHOUSE,
	FLAG_WARP_GALLEON_W1_CRANKY,
	FLAG_WARP_GALLEON_W2_2DS,
	FLAG_WARP_GALLEON_W2_CRANKY,
	FLAG_WARP_GALLEON_W3_SNIDE,
	FLAG_WARP_GALLEON_W3_CRANKY,
	FLAG_WARP_GALLEON_W4_SEAL,
	GALLEON_TOWERW4, // Activating the gold tower warp despawns Diddy's GB
	FLAG_WARP_GALLEON_W5_5DS,
	FLAG_WARP_GALLEON_W5_LIGHTHOUSE,
};
static const short warpflags_fungi[] = {
	FLAG_WARP_FUNGI_W1_MILL,
	FLAG_WARP_FUNGI_W1_CLOCK,
	FLAG_WARP_FUNGI_W2_CLOCK,
	FLAG_WARP_FUNGI_W2_FUNKY,
	FLAG_WARP_FUNGI_W3_CLOCK,
	FLAG_WARP_FUNGI_W3_MUSH,
	FLAG_WARP_FUNGI_W4_CLOCK,
	FLAG_WARP_FUNGI_W4_OWL,
	FLAG_WARP_FUNGI_W5_LOW,
	FLAG_WARP_FUNGI_W5_HIGH,
};
static const short warpflags_caves[] = {
	FLAG_WARP_CAVES_W1_5DI,
	FLAG_WARP_CAVES_W1_PORTAL,
	FLAG_WARP_CAVES_W2_PORTAL,
	FLAG_WARP_CAVES_W2_FAR,
	FLAG_WARP_CAVES_W3_5DI,
	CAVES_HIDDENW3,
	FLAG_WARP_CAVES_W4_FAR,
	FLAG_WARP_CAVES_W4_5DI,
	FLAG_WARP_CAVES_W5_5DC,
	FLAG_WARP_CAVES_W5_PILLAR,
};
static const short warpflags_castle[] = {
	FLAG_WARP_CASTLE_W1_HUB,
	FLAG_WARP_CASTLE_W1_FAR,
	FLAG_WARP_CASTLE_W2_HUB,
	FLAG_WARP_CASTLE_W2_HIGH,
	FLAG_WARP_CASTLE_W3_HUB,
	FLAG_WARP_CASTLE_W3_HIGH,
	FLAG_WARP_CASTLE_W4_HUB,
	FLAG_WARP_CASTLE_W4_HIGH,
	FLAG_WARP_CASTLE_W5_HUB,
	FLAG_WARP_CASTLE_W5_HIGH,
	FLAG_WARP_CRYPT_W1_CLOSE,
	FLAG_WARP_CRYPT_W1_FAR,
	FLAG_WARP_CRYPT_W2_CLOSE,
	FLAG_WARP_CRYPT_W2_FAR,
	FLAG_WARP_CRYPT_W3_CLOSE,
	FLAG_WARP_CRYPT_W3_FAR,
};
// static const short warpflags_helm[] = {
// 	FLAG_WARP_HELM_W1_NEAR,
// 	FLAG_WARP_HELM_W1_FAR
// };
static const short warpflags_isles[] = {
	FLAG_WARP_ISLES_W1_RING,
	FLAG_WARP_ISLES_W1_FAR,
	FLAG_WARP_ISLES_W2_RING,
	FLAG_WARP_ISLES_W2_FAR,
	FLAG_WARP_ISLES_W3_RING,
	FLAG_WARP_ISLES_W3_FAR,
	FLAG_WARP_ISLES_W4_RING,
	FLAG_WARP_ISLES_W4_HIGH,
	FLAG_WARP_ISLES_W5_RING,
	FLAG_WARP_ISLES_W5_FAR,
	//FLAG_WARP_LOBBY_W1_NEAR, # Helm lobby still requires Gorilla Gone
	//FLAG_WARP_LOBBY_W1_FAR,
};

static const short* warpflags_list[WARPLEVELCOUNT] = {
	warpflags_japes,
	warpflags_aztec,
	warpflags_factory,
	warpflags_galleon,
	warpflags_fungi,
	warpflags_caves,
	warpflags_castle,
	// warpflags_helm, # Activating Helm warps would circumvent Helm door settings
	warpflags_isles,
};

static const char warpflags_count[WARPLEVELCOUNT] = {
	10,14,10,10,10,10,16, /*2,*/ 10
};

void toggleWarpLevel(int levelIndex) {
    int count = warpflags_count[levelIndex];
    for (int i = 0; i < count; i++) {
        setPermFlag(warpflags_list[levelIndex][i]);
    }
}

void activateBananaports(void) {
    if (Rando.activate_all_bananaports == 1) {
        for (int i = 0; i < WARPLEVELCOUNT; i++) {
            toggleWarpLevel(i);
        }
    } else if (Rando.activate_all_bananaports == 2) {
		toggleWarpLevel(7);
	}
}