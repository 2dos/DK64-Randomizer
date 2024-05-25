#include "../../include/common.h"

typedef struct delete_item_struct {
    /* 0x000 */ char active;
    /* 0x001 */ char is_model2;
    /* 0x002 */ short id;
} delete_item_struct;

typedef struct puppet {
    /* 0x000 */ unsigned char map;
    /* 0x001 */ unsigned char last_kong;
    /* 0x002 */ short x;
    /* 0x004 */ short y;
    /* 0x006 */ short z;
    /* 0x008 */ short animation;
    /* 0x00A */ char active;
    /* 0x00B */ unsigned char kong;
    /* 0x00C */ actorData* tied_actor;
    /* 0x010 */ short facing_angle;
    /* 0x012 */ unsigned char hand_state;
    /* 0x013 */ char pad;
    /* 0x014 */ delete_item_struct deleted_items[4];
} puppet;

static puppet puppets[3];
static short puppet_models[] = {4, 1, 6, 9, 0xC, 0xDA, 0x14, 0x18};
static delete_item_struct in_contact_items[4];

void wipeItemDestroyers(void) {
    for (int i = 0; i < 4; i++) {
        in_contact_items[i].active = 0;
    }
}

void handlePuppet(puppet* pp) {
    if (!pp->active) {
        return;
    }
    if (ObjectModel2Timer == 1) {
        pp->tied_actor = 0;
        return;
    }
    if (CurrentMap == pp->map) {
        // Handle Puppet
        if (!pp->tied_actor) {
            // Puppet hasn't been spawned
            spawnActor(1, puppet_models[pp->kong]);
            pp->tied_actor = LastSpawnedActor;
        }
        actorData* local_actor = pp->tied_actor;
        local_actor->xPos = pp->x;
        local_actor->yPos = pp->y;
        local_actor->zPos = pp->z;
        if (pp->last_kong != pp->kong) {
            // setActorModel(local_actor, puppet_models[pp->kong]);
        }
        pp->last_kong = pp->kong;
        local_actor->hand_state = pp->hand_state;
        local_actor->rot_y = pp->facing_angle;
        renderingParamsData* render = local_actor->render;
        if (render) {
            if (pp->animation != render->animation) {
                // playAnimation(local_actor, pp->animation);
            }
        }
        // Handle items which need to be deleted
        for (int i = 0; i < 4; i++) {
            delete_item_struct* dis = &pp->deleted_items[i];
            if (dis) {
                if (dis->active) {
                    if (dis->is_model2) {
                        deleteModelTwo(dis->id, 1);
                    } else {
                        actorSpawnerData* ptr = ActorSpawnerPointer;
                        while (1) {
                            if (!ptr) {
                                break;
                            }
                            if (ptr->id == dis->id) {
                                if (isAddressActor(ptr->tied_actor)) {
                                    deleteActorContainer(ptr->tied_actor);
                                    break;
                                }
                            }
                            ptr = ptr->next_spawner;
                        }
                    }
                    dis->active = 0;
                }
            }
        }
    } else {
        // Puppet isn't in map
        if (pp->tied_actor) {
            deleteActorContainer(pp->tied_actor);
            pp->tied_actor = 0;
        }
    }   
}

void puppetLoop(void) {
    *(int*)(0x807FF700) = (int)&puppets[0];
    *(int*)(0x807FF704) = (int)&in_contact_items[0];
    for (int i = 0; i < 3; i++) {
        handlePuppet(&puppets[i]);
    }
}

void puppetActor(void) {
    CurrentActorPointer_0->noclip_byte = 1;
    renderActor(CurrentActorPointer_0, 0);
}