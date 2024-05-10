/**
 * @file switches.c
 * @author Ballaam
 * @brief Functions related to switches
 * @version 0.1
 * @date 2023-10-23
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#include "../../include/common.h"

int getPressedRandoSwitch(behaviour_data* behaviour_pointer, int setting, int vanilla_bullet_type, int ID) {
	int bullet = vanilla_bullet_type;
	if (setting != 0) {
		bullet = kong_pellets[setting - 1];
	}
	return getPressedSwitch(behaviour_pointer, bullet, ID);
}

typedef struct SwitchInfo {
	/* 0x000 */ unsigned char* setting_address;
	/* 0x004 */ kongs vanilla_kong;
} SwitchInfo;

static const SwitchInfo switch_data[] = {
	{.setting_address = &Rando.switchsanity.isles.aztec_lobby_feather, .vanilla_kong=KONG_TINY},
	{.setting_address = &Rando.switchsanity.isles.fungi_lobby_feather, .vanilla_kong=KONG_TINY},
	{.setting_address = &Rando.switchsanity.japes.feather, .vanilla_kong=KONG_TINY},
	{.setting_address = &Rando.switchsanity.japes.rambi, .vanilla_kong=KONG_DK},
	{.setting_address = &Rando.switchsanity.japes.diddy_cave, .vanilla_kong=KONG_DIDDY},
	{.setting_address = &Rando.switchsanity.japes.painting, .vanilla_kong=KONG_DIDDY},
	{.setting_address = &Rando.switchsanity.aztec.bp_door, .vanilla_kong=KONG_DK},
	{.setting_address = &Rando.switchsanity.aztec.llama_switches[0], .vanilla_kong=KONG_DK},
	{.setting_address = &Rando.switchsanity.aztec.llama_switches[1], .vanilla_kong=KONG_LANKY},
	{.setting_address = &Rando.switchsanity.aztec.llama_switches[2], .vanilla_kong=KONG_TINY},
	{.setting_address = &Rando.switchsanity.galleon.lighthouse, .vanilla_kong=KONG_DK},
	{.setting_address = &Rando.switchsanity.galleon.shipwreck, .vanilla_kong=KONG_DIDDY},
	{.setting_address = &Rando.switchsanity.galleon.cannongame, .vanilla_kong=KONG_CHUNKY},
	{.setting_address = &Rando.switchsanity.fungi.yellow, .vanilla_kong=KONG_LANKY},
	{.setting_address = &Rando.switchsanity.fungi.green_feather, .vanilla_kong=KONG_TINY},
	{.setting_address = &Rando.switchsanity.fungi.green_pineapple, .vanilla_kong=KONG_CHUNKY},
};

static const SwitchInfo pad_data[] = {
	{.setting_address = &Rando.switchsanity.isles.spawn_rocketbarrel, .vanilla_kong=KONG_LANKY},
	{.setting_address = &Rando.switchsanity.aztec.guitar, .vanilla_kong=KONG_DIDDY},
	{.setting_address = &Rando.switchsanity.aztec.snoop_switch, .vanilla_kong=KONG_DK},
};

int randomGunSwitchGenericCode(behaviour_data* behaviour_pointer, int index, int switch_index) {
	int vanilla_kong = switch_data[switch_index].vanilla_kong;
	int setting = 0;
	if (switch_data[switch_index].setting_address) {
		setting = *switch_data[switch_index].setting_address;
	}
	return getPressedRandoSwitch(behaviour_pointer, setting, kong_pellets[vanilla_kong], index);
}

int randomInstrumentGenericCode(behaviour_data* behaviour_pointer, int index, int pad_index) {
	int referenced_kong = pad_data[pad_index].vanilla_kong;
	int setting = 0;
	if (pad_data[pad_index].setting_address) {
		setting = *pad_data[pad_index].setting_address;
	}
	if (setting != 0) {
		referenced_kong = setting - 1;
	}
	return Player->characterID == referenced_kong + 2;
}

int hasChunkyPhaseSlam(void) {
	return MovesBase[KONG_CHUNKY].simian_slam >= Rando.chunky_phase_krool_slam_req;
}