#include "../../include/common.h"

int curseRemoved(void) {
	return checkFlag(FLAG_MODIFIER_HELMBOM,0); // BoM turned off
}

int hasPermaLossGrace(void) {
	return (CurrentMap == 0x11) || (CurrentMap == 0xAA);
}

int determineKongUnlock(int actorType, int kong_index) {
	int unlock_flag = GetKongUnlockedFlag(actorType,kong_index);
	int kong_freed = checkFlag(unlock_flag,0);
	if (!Rando.perma_lose_kongs) {
		return kong_freed;
	}
	if (hasPermaLossGrace()) {
		return kong_freed;
	}
	if (curseRemoved()) {
		return kong_freed;
	}
	int kong_locked = checkFlag(KONG_LOCKED_START + kong_index,0);
	if (kong_locked || (!kong_freed)) {
		return 0;
	} else {
		return 1;
	}
}

void unlockKongPermaLoss(int actorType, int kong_index) {
	int unlock_flag = GetKongUnlockedFlag(actorType,kong_index);
	int kong_locked = checkFlag(KONG_LOCKED_START + kong_index,0);
	if (Rando.perma_lose_kongs) {
		if (kong_locked && (!curseRemoved())) {
			return;
		}
	}
	setPermFlag(unlock_flag);
}

void giveKongMoves(int kong_index) {
	MovesBase[kong_index].special_moves = 7; // All 3 cranky moves
	MovesBase[kong_index].weapon_bitfield |= 1; // Gun
	MovesBase[kong_index].instrument_bitfield |= 1; // Instrument
}

int isDeathState(int control_state) {
	return (control_state == 0x36) || (control_state == 0x3B) || (control_state == 0x39);
}

void kong_has_died(void) {
	if (Rando.perma_lose_kongs) {
		if (getWorld(CurrentMap,0) != 8) { // Not in Helm
			if (!curseRemoved()) {
				if (Player) {
					int control_state = Player->control_state;
					if (isDeathState(control_state)) {
						if (TransitionSpeed > 0.0f) {
							if (LZFadeoutProgress == 30.0f) {
								int init_kong = Character;
								setPermFlag(KONG_LOCKED_START + init_kong);
								int new_kong = (init_kong + 1) % 5;
								int pass = 1;
								int counter = 0;
								while (pass) {
									int kong_locked = checkFlag(KONG_LOCKED_START + new_kong,0);
									int unlock_flag = GetKongUnlockedFlag(Player->characterID,new_kong);
									int kong_freed = checkFlag(unlock_flag,0);
									if ((!kong_freed) || (kong_locked)) {
										new_kong = (new_kong + 1) % 5;
										counter += 1;
										if (counter >= 5) {
											setFlag(KONG_LOCKED_START + init_kong,0,0);
											pass = 0;
											resetMap(); // Resets parent chain to prevent SirSmack causing memes
											Gamemode = 7; // Loading Game Over
											Mode = 7;
											return;
										}
									} else {
										pass = 0;
										Character = new_kong;
										giveKongMoves(init_kong);
										return;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}

void determineStartKong_PermaLossMode(void) {
	if (Rando.perma_lose_kongs) {
		if (!curseRemoved()) {
			for (int i = 0; i < 5; i++) {
				int kong_locked = checkFlag(KONG_LOCKED_START + i,0);
				int unlock_flag = GetKongUnlockedFlag(2 + i,i);
				int kong_freed = checkFlag(unlock_flag,0);
				if ((kong_freed) && (!kong_locked)) {
					Character = i;
					return;
				}
			}
		}
	}
}

void transitionKong(void) {
	if (!curseRemoved()) {
		if (checkFlag(KONG_LOCKED_START + Character,0)) {
			int new_kong = (Character + 1) % 5;
			int pass = 1;
			int counter = 0;
			while (pass) {
				int kong_locked = checkFlag(KONG_LOCKED_START + new_kong,0);
				int unlock_flag = GetKongUnlockedFlag(Player->characterID,new_kong);
				int kong_freed = checkFlag(unlock_flag,0);
				if ((!kong_freed) || (kong_locked)) {
					new_kong = (new_kong + 1) % 5;
					counter += 1;
					if (counter >= 5) {
						pass = 0;
						return;
					}
				} else {
					pass = 0;
					Character = new_kong;
					return;
				}
			}
		}
	}
}

void changeKongOnTransition_Permaloss(void) {
	if (TransitionSpeed > 0.0f) {
		if (Player) {
			int control_state = Player->control_state;
			if (isDeathState(control_state)) {
				transitionKong();
			}
		}
	}
}

void forceBossKong(void) {
	if (Rando.perma_lose_kongs) {
		if (CurrentMap == 0x2A) {
			int transitioning_to_boss = 0;
			for (int i = 0; i < 7; i++) {
				if (BossMapArray[i] == DestMap) {
					transitioning_to_boss = 1;
				}
			}
			if (transitioning_to_boss) {
				if (TransitionSpeed > 0.0f) {
					if (LZFadeoutProgress == 30.0f) {
						if (Player) {
							int world = getWorld(CurrentMap, 0);
							Character = BossKongArray[world];
						}
					}
				}
			}
		}
	}
}

void preventBossCheese(void) {
	if (Rando.perma_lose_kongs) {
		int in_boss = 0;
		for (int i = 0; i < 7; i++) {
			if (BossMapArray[i] == CurrentMap) {
				in_boss = 1;
			}
		}
		if (in_boss) {
			changeKongOnTransition_Permaloss();
		}
	}
}