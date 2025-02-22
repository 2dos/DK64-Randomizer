/**
 * @file quality_fixes.c
 * @author Ballaam
 * @brief Quality of life fixes to the game
 * @version 0.1
 * @date 2021-12-07
 * 
 * @copyright Copyright (c) 2021
 * 
 */
#include "../../include/common.h"

#define MODE_DKTV 3

void qualityOfLife_fixes(void) {
	/**
	 * @brief Quality of life fixes to the game
	 */
	if (Rando.quality_of_life.vanilla_fixes) {
		// Prevent a bug where detransforming from Rambi shortly before getting hit will keep you locked as Rambi
		if (CurrentMap == MAP_JAPES) {
			if (Player) {
				if (Character == 6) { // Rambi
					if (Player->detransform_timer == 0) {
						Player->rambi_enabled = 1;
					}
				}
			}
		} else if (CurrentMap == MAP_CAVESROTATINGROOM) {
			if (Player) {
				if (Player->yPos < 50.0f) {
					Player->xPos = 317.0f;
					Player->yPos = 124.0f;
					Player->zPos = 295.0f;
					displaySpriteAtXYZ(sprite_table[19], 1.0f, Player->xPos, Player->yPos, Player->zPos);
				}
			}
		} else {
			int is_beaver_bother = CurrentMap == MAP_BBOTHER_EASY ||
				CurrentMap == MAP_BBOTHER_HARD ||
				CurrentMap == MAP_BBOTHER_NORMAL;
			if (is_beaver_bother) {
				if (Player) {
					int control_state = Player->control_state;
					int good_state = control_state == 0x7D || // Klaptrap
						control_state == 0x73 || // Failure
						control_state == 0x74; // Victory
					if (!good_state) {
						Player->control_state = 0x7D;
					}
				}
			}
		}
	}
}

int force_enable_diving_timer = 0;

void dropWrapper(void* actor) {
	clearTagSlide(actor);
	force_enable_diving_timer = ObjectModel2Timer;
}

int CanDive_WithCheck(void) {
	if (ObjectModel2Timer < 5) {
		return 1;
	}
	if (ObjectModel2Timer >= force_enable_diving_timer) {
		if ((ObjectModel2Timer - force_enable_diving_timer) < 2) {
			return 1;
		}
	}
	if (isGlobalCutscenePlaying(29)) {
		return 1;
	}
	return CanDive();
}

void playTransformationSong(songs song, float volume) {
	if (CurrentMap == MAP_FUNGI) {
		if (song == SONG_SPRINT) {
			return;
		}
	}
	playSong(song, volume);
}

static unsigned short previous_total_cbs = 0xFFFF;
static unsigned char previous_world = 0xFF;

#define SPRITE_ALPHA_OUT 8
#define SPRITE_ALPHA_IN 44
#define SPRITE_ALPHA_END 52

static unsigned char ding_sprite_timer = 0;

int hasEnoughCBs(void) {
	int world = getWorld(CurrentMap, 1);
	if (world < 7) {
		int total_cbs = getTotalCBCount();
		int req_cbs = TroffNScoffReqArray[world];
		return total_cbs >= req_cbs;
	}
	return 0;
}

int shouldDing(void) {
	int world = getWorld(CurrentMap, 1);
	if (world < 7) {
		int req_cbs = TroffNScoffReqArray[world];
		if ((previous_total_cbs < req_cbs) && (hasEnoughCBs()) && (previous_world == world) && (CurrentMap != MAP_TROFFNSCOFF)) { // Ban in T&S because of delayed update to turn in array
			if (!checkFlag(tnsportal_flags[world],FLAGTYPE_PERMANENT)) {
				return 1;
			}
		}
	}
	return 0;
}

Gfx* renderIndicatorSprite(Gfx* dl, int sprite, int dim, unsigned char* timer, int width, int height, codecs codec) {
	if (*timer == 0) {
		return dl;
	}
	int timer_value = *timer - 1;
	*timer = timer_value;
	int offset = 0;
	if (timer_value > SPRITE_ALPHA_IN) {
		offset = timer_value - SPRITE_ALPHA_IN;
	} else if (timer_value < SPRITE_ALPHA_OUT) {
		offset = SPRITE_ALPHA_OUT - timer_value;
	}
	float alpha = 0xFF;
	if (dim) {
		alpha = 0x80;
	}
	alpha *= (SPRITE_ALPHA_OUT - offset);
	alpha /= SPRITE_ALPHA_OUT;
	int y = 825 + (offset * 5);
	int alpha_i = alpha;
	if (alpha_i > 255) {
		alpha_i = 255;
	} else if (alpha_i < 0) {
		return dl;
	}
	dl = initDisplayList(dl);
	gDPSetRenderMode(dl++, G_RM_XLU_SURF, G_RM_XLU_SURF2);
	gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, alpha_i);
	gDPSetCombineLERP(dl++, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0);
	gDPSetTextureFilter(dl++, G_TF_POINT);
	int p2 = 0;
	if (codec == IA8) {
		p2 = 3;
	}
	return displayImage(dl++, sprite, p2, codec, width, height, 900, y, 2.0f, 2.0f, 0, 0.0f);
}

Gfx* renderDingSprite(Gfx* dl) {
	return renderIndicatorSprite(dl, 114, !hasEnoughCBs(), &ding_sprite_timer, 48, 42, RGBA16);
}

void initDingSprite(void) {
	ding_sprite_timer = SPRITE_ALPHA_END;
}

int getHomingCountWithAbilityCheck(item_ids item, int player) {
	if (!(MovesBase[0].weapon_bitfield & 2)) {
		return 0;
	}
	return getItemCount(item, player);
}

void playCBDing(void) {
	/**
	 * @brief Play Bell Ding sound effect
	 */
	playSFX(Bell);
	initDingSprite();
}

void CBDing(void) {
	/**
	 * @brief Check if T&S Threshold has been met
	 */
	if (Rando.quality_of_life.cb_indicator) {
		int world = getWorld(CurrentMap, 1);
		if (shouldDing()) {
			playCBDing();
		}
		previous_world = world;
		previous_total_cbs = getTotalCBCount();
	}
}

void fixRBSlowTurn(void) {
	/**
	 * @brief Fix the Rocketbarrel Slow Turn glitch
	 * This occurs if you standing ground attack before jumping into a Rocketbarrel Barrel
	 */
	controlStateControl(0x1B);
	if (Player) {
		Player->turn_speed = 0x190;
	}
}

void postKRoolSaveCheck(void) {
	/**
	 * @brief Prevent the game saving on the transition from Chunky Phase to the K. Rool launch cutscene
	 */
	if ((CurrentMap != MAP_ISLES) || (!CutsceneFadeActive) || (CutsceneFadeIndex != 29)) {
		save();
	}
}

void tagBarrelBackgroundKong(int kong_actor) {
	/**
	 * @brief Alter the tag function to also change the background kong.
	 * This prevents a bug with tagging from a tag barrel where it doesn't update the background kong.
	 * This can result in a weird tag when getting caught by a guard or other situations
	 */
	tagKong(kong_actor);
	Player->new_kong = kong_actor;
}

void updateMultibunchCount(void) {
	/**
	 * @brief Get the total amount of colored bananas for a level.
	 * Used in the multibunch display
	 */
	int count = getTotalCBCount();
	MultiBunchCount = count;
	if (HUD) {
		HUD->item[ITEMID_MULTIBUNCH].visual_item_count = count;
	}
}

typedef struct balloon_paad {
	/* 0x000 */ char unk0;
	/* 0x001 */ char speed;
	/* 0x002 */ char local_path_index;
	/* 0x003 */ char unk3;
	/* 0x004 */ short unk4;
	/* 0x006 */ short flag;
} balloon_paad;

void RabbitRaceInfiniteCode(void) {
	/**
	 * @brief Change Rabbit Race so that upon starting the race, you get infinite Crystal Coconuts
	 * This only applies to Round 2, and will end the infinite coconuts upon the race finishing
	 */
	initCharSpawnerActor();
	if (checkFlag(FLAG_RABBIT_ROUND1,FLAGTYPE_PERMANENT)) {
		int control_state = CurrentActorPointer_0->control_state;
		if (control_state == 0x1F) {
			if (CurrentActorPointer_0->control_state_progress == 2) {
				// Start
				setHUDItemAsInfinite(ITEMID_CRYSTALS,0,1);
			}
		} else if ((control_state == 0x28) || (control_state == 0x1E)) {
			if (CurrentActorPointer_0->control_state_progress == 0) {
				// End
				resetCoconutHUD();
			}
		}
	}
}

int fixDilloTNTPads(void* actor) {
	/**
	 * @brief Fix a bug where grabbing a TNT Barrel with Tiny, then throwing it can cause the TNT Barrel to go under the pad.
	 * This exposes behaviour where the TNT spawn pad can move if it's riding another object.
	 * To fix this, we change the behaviour of the TNT Spawn pad so that it won't obey gravity and will be locked in place.
	 * The unfortunate side effect is that if the ground ripples in Army Dillo, the pad won't move with the ripple.
	 * 
	 * @param actor TNT Spawn Pad actor address
	 * 
	 * @return Does actor obey gravity
	 */
	if ((CurrentMap == MAP_JAPESDILLO) || (CurrentMap == MAP_CAVESDILLO)) {
		return 0;
	}
	return getPadGravity(actor);
}

int canPlayJetpac(void) {
	/**
	 * @brief Determine whether the player can play Jetpac.
	 * We will only enable the player to attempt Jetpac upon not having the Jetpac Reward
	 * 
	 * @return Amount of medals the player has. Set to 0 if you have the Jetpac Reward
	 */
	if (checkFlag(FLAG_COLLECTABLE_RAREWARECOIN, FLAGTYPE_PERMANENT)) {
		return 0;
	} else {
		return getMedalCount();
	}
}

void fixCrownEntrySKong(playerData* player, int animation) {
	player->strong_kong_ostand_bitfield &= 0xFFFFFFEF;
	playAnimation(player, animation);
}

void reduceTrapBubbleLife(void) {
	Player->trap_bubble_timer -= 5;
	if (Player->trap_bubble_timer < 1) {
		Player->trap_bubble_timer = 1;
	}
}

void exitTrapBubbleController(void) {
	int x = stickX_interpretted;
	int y = stickY_interpretted;
	int threshold = 0x28;
	if (((x > threshold) || (y > threshold)) && (Player->unk_288 != 0.0f)) {
		Player->unk_288 = 1.0f;
		reduceTrapBubbleLife();
		return;
	}
	if (((x < -threshold) || (y < -threshold)) && (Player->unk_288 == 0.0f)) {
		Player->unk_288 = 0.0f;
		reduceTrapBubbleLife();
		return;
	}
	if (NewlyPressedControllerInput.Buttons.a) {
		// Perform reduction twice to counteract that this can be done once per two frames
		reduceTrapBubbleLife();
		reduceTrapBubbleLife();
		return;
	}
}

void fixChimpyCamBug(void) {
	/**
	 * @brief Things to be reset upon first boot of the game on PJ64 (Because PJ64 is weird)
	 */
	wipeGlobalFlags();
	SaveToFile(DATA_CAMERATYPE, 0, 0, 0, Rando.default_camera_type);
	SaveToFile(DATA_LANGUAGE, 0, 0, 0, Rando.default_camera_type);
	SaveToFile(DATA_SOUNDTYPE, 0, 0, 0, Rando.default_sound_type);
	wipeFileStats();
	SaveToGlobal();
}

void movePelletWrapper(actorData* actor) {
	if (!(CurrentActorPointer_0->obj_props_bitfield & 0x10)) {
		if ((Player->control_state == 2) && (Player->was_gun_out == 1)) {
			int dist = getScreenDist(screenCenterX >> 1, screenCenterY >> 1);
			int cap = getDistanceCap(dist);
			if ((cap == 0) || (cap == 996)) {
				// Lets not get into a div-by-0 mess
				unkProjectileCode_2(actor);
				return;
			}
			float dxz = CurrentActorPointer_0->hSpeed * 0.025f;
			float dy = CurrentActorPointer_0->yVelocity * 0.025f;
			float cap_f = cap;
			float d_one_frame = dk_sqrt((dxz * dxz) + (dy * dy));
			float ratio = cap_f / d_one_frame;
			int rotation = CurrentActorPointer_0->rot_y_copy;
			float dxz_ratio = dxz * ratio;

			CurrentActorPointer_0->xPos += (dxz_ratio * determineXRatioMovement(rotation));
			CurrentActorPointer_0->yPos += (dy * ratio);
			CurrentActorPointer_0->zPos += (dxz_ratio * determineZRatioMovement(rotation));
			return;
		}
	}
	unkProjectileCode_2(actor);
}

static unsigned char good_gamemode_list[] = {
	GAMEMODE_ADVENTURE,
	GAMEMODE_RAP,
	GAMEMODE_SNIDEGAMES,
};

void fixHelmTimerDisable(void) {
	if (inU8List(Gamemode, &good_gamemode_list, 3)) {
		return;
	}
	HelmTimerShown = 0;
}

// Segment framebuffer
// Should help with framebuffer crashes

// #define FB_SEGMENTATION 16
// #define FB_HEIGHT_PER_SEG (240 / 16)
// #define FB_WIDTH 320

// typedef struct framebuffer_info {
// 	/* 0x000 */ short* segment[FB_SEGMENTATION];
// } framebuffer_info;

// void* framebufferMalloc(void) {
// 	framebuffer_info* data = dk_malloc(sizeof(framebuffer_info));
// 	for (int i = 0; i = FB_SEGMENTATION; i++) {
// 		data->segment[i] = dk_malloc(FB_WIDTH * FB_HEIGHT_PER_SEG * 2);
// 	}
// 	return data;
// }

// void storeFramebufferNew(framebuffer_info* dest, short* src) {
// 	int global_px = 0;
// 	for (int i = 0; i < FB_SEGMENTATION; i++) {
// 		int local_px = 0;
// 		for (int y = 0; y < FB_HEIGHT_PER_SEG; y++) {
// 			for (int x = 0; x < FB_WIDTH; x++) {
// 				dest->segment[i][local_px] = src[global_px] | 1;
// 				local_px++;
// 				global_px++;
// 			}
// 		}
// 	}
// }