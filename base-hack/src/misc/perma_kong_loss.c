#include "../../include/common.h"

int curseRemoved(void) {
	return checkFlag(770,0); // BoM turned off
}

int determineKongUnlock(int actorType, int kong_index) {
	int unlock_flag = GetKongUnlockedFlag(actorType,kong_index);
	int kong_freed = checkFlag(unlock_flag,0);
	if (!Rando.perma_lose_kongs) {
		return kong_freed;
	}
	if (CurrentMap == 0x11) {
		return kong_freed;
	}
	if (CurrentMap == 0x2A) {
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

void kong_has_died(void) {
	if (Rando.perma_lose_kongs) {
		if (getWorld(CurrentMap,0) != 8) { // Not in Helm
			if (!curseRemoved()) {
				if (Player) {
					int control_state = Player->control_state;
					if ((control_state == 0x36) || (control_state == 0x3B)) {
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
											Gamemode = 7; // Loading Game Over
											Mode = 7;
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

void changeKongOnTransition_Permaloss(void) {
	if (TransitionSpeed > 0.0f) {
		if (Player) {
			int control_state = Player->control_state;
			if ((control_state != 0x36) && (control_state != 0x3B)) {
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
		}
	}
}

void preventBossCheese(void) {
	if (Rando.perma_lose_kongs) {
		if (CurrentMap == 0xC7) { // King Kut Out
			changeKongOnTransition_Permaloss();
		}
	}
}