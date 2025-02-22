/**
 * @file dk_free_softlock.c
 * @author Ballaam
 * @brief Fixes the softlock when freeing DK from a cage
 * @version 0.1
 * @date 2022-04-13
 * 
 * @copyright Copyright (c) 2022
 * 
 */

#include "../../include/common.h"

void freeDK(void) {
	/**
	 * @brief Cancel the softlocked cutscene
	 */
	cancelCutscene(0); // Cancel cutscene
	// Delete cutscene DK
	actorData* cutscene_dk = (actorData*)findActorWithType(196);
	SpawnerInfo* spawner = cutscene_dk->tied_character_spawner;
	spawner->spawn_state = 0;
	deleteActorContainer(cutscene_dk);
}

static char jumping_started = 0; // Global variable indicating that the jumping sequence has started

void cutsceneDKCode(void) {
	/**
	 * @brief Actor code for cutscene DK
	 */
	initCharSpawnerActor(); // Initialize Char Spawner
	if ((CurrentActorPointer_0->obj_props_bitfield & 0x10) == 0) {
		// Initialization of the actor
		jumping_started = 0;
		alterCutsceneKongProperties();
		if (CurrentMap == MAP_DKRAP) {
			CurrentActorPointer_0->render->scale_x *= 0.8f;
			CurrentActorPointer_0->render->scale_y *= 0.8f;
			CurrentActorPointer_0->render->scale_z *= 0.8f;
		}
		unkCutsceneKongFunction_0(2,1);
		updateActorHandStates(CurrentActorPointer_0,CurrentActorPointer_0->actorType);
	}
	int obj_props = CurrentActorPointer_0->obj_props_bitfield;
	if ((obj_props << 3) < 0) {
		cutsceneKongGenericCode();
		if (CurrentActorPointer_0->render->sub->unk_10 == 0x1a4) {
			*(char*)(0x807FDB18) = 1;
			changeActorColor(0x96,0xFF,0xFF,0xFF);
			displaySpriteAttachedToActor((void*)0x8071FBA0,0.7f,CurrentActorPointer_0,5,0);
		}
		int iVar2 = 7;
		if (*(int*)(0x807FBB4C) == *(int*)(0x807FDC94)) {
			iVar2 = 5;
		}
		unkCutsceneKongFunction_1(iVar2);
	} else {
		int temp_flag = 0x7F;
		int animation = 89; // Japes Intro jumping for GB
		spawnCutsceneKongText(2,0x18,animation);
		unkCutsceneKongFunction_1(0);
		DisplayTextFlagCheck(6,1,temp_flag);
	}
	// Define jump as having an animation timer > 80.0f
	int anim_timer = getAnimationTimer(CurrentActorPointer_0);
	if (anim_timer > 80.0f) {
		jumping_started = 1;
	}
	if (jumping_started) {
		// If no textbox is present, cancel cutscene
		int found_actor = 0;
		for (int i = 0; i < ActorCount; i++) {
			actorData* _actor_ = (actorData*)ActorArray[i];
			if (_actor_->actorType == 299) {
				found_actor = (int)_actor_;
			}
		}
		if (found_actor == 0) {
			freeDK();
		}
	}
	renderActor(CurrentActorPointer_0,0);
}