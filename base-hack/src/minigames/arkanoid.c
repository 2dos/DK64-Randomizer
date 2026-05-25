// minigame: arkanoid
#include "minigame_defs.h"

typedef enum gameStates {
    GAMESTATE_INIT,
    GAMESTATE_TITLE,
    GAMESTATE_NORMAL,
    GAMESTATE_WIN,
} gameStates;

typedef enum powerUpState {
    POWERUP_NONE,
    POWERUP_LASER, // Fires dual lasers
    POWERUP_ENLARGE, // Grows paddle
    POWERUP_CATCH, // Ball sticks to paddle
    POWERUP_SLOW, // Slow ball velocity
    POWERUP_DISRUPTION, // Splits ball into 3
} powerUpState;

typedef struct BallStruct {
    short x;
    short y;
    short xVel;
    short yVel;
    unsigned char attached_to_paddle;
    unsigned char active;
    unsigned char width;
    unsigned char height;
    unsigned char colliding;
    unsigned char collision_polarity;
} BallStruct;

typedef struct PowerUpStruct {
    short x;
    short y;
    unsigned char power_up;
    unsigned char active;
    unsigned char width;
    unsigned char height;
    unsigned char frame;
} PowerUpStruct;

typedef struct ColliderStruct {
    short x;
    short y;
    unsigned short width;
    unsigned short height;
    unsigned char has_color;
    unsigned char active;
    rgb color;
    unsigned char can_kill;
    unsigned char health;
    unsigned char black_ended;
    unsigned char required_for_win;
    unsigned char points;
} ColliderStruct;

typedef struct CollisionPacketStruct {
    short collision_x;
    short collision_y;
    unsigned char colliding;
} CollisionPacketStruct;

#define BOARD_Y_OFFSET 0x25
#define BOARD_BORDER 8
#define BOARD_X_INSET 48
#define ROW_ELEMENTS 13
#define COL_ELEMENTS 6
#define EL_WIDTH 15
#define EL_HEIGHT 7
#define EL_Y_START 60
#define PADDLE_Y 200
#define KILL_PLANE 230
#define COLLIDER_BUFFER_SIZE 100
#define BALL_BUFFER_SIZE 5
#define POWER_UP_BUFFER_SIZE 5
#define PADDLE_ENDS_WIDTH 8
#define BALL_WIDTH 4

ROM_RODATA_NUM static const unsigned char power_up_table[] = {
    POWERUP_LASER,
    POWERUP_LASER,
    POWERUP_LASER,
    POWERUP_LASER,

    POWERUP_ENLARGE,
    POWERUP_ENLARGE,
    POWERUP_ENLARGE,
    POWERUP_CATCH,

    POWERUP_CATCH,
    POWERUP_CATCH,
    POWERUP_SLOW,
    POWERUP_SLOW,

    POWERUP_DISRUPTION, 
    POWERUP_DISRUPTION,
    POWERUP_DISRUPTION,
    POWERUP_DISRUPTION,
};
ROM_DATA static gameStates game_state = GAMESTATE_INIT;
ROM_DATA static ColliderStruct paddle = {
    .x = 170 - PADDLE_ENDS_WIDTH,
    .y = PADDLE_Y,
    .width = 16 + (2 * PADDLE_ENDS_WIDTH),
    .height = 8,
    .active = 1,
    .has_color = 0,
    .can_kill = 0,
};
ROM_DATA static unsigned short points = 0;
ROM_DATA static unsigned char level = 0;
ROM_DATA static unsigned char current_power_up = POWERUP_NONE;
ROM_DATA static BallStruct balls[BALL_BUFFER_SIZE] = {};
ROM_DATA static ColliderStruct colliders[COLLIDER_BUFFER_SIZE] = {};
ROM_DATA static PowerUpStruct power_ups[POWER_UP_BUFFER_SIZE] = {};
// ROM_RODATA_NUM static const char paddle_left[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/arkanoid/paddle_left.png", "IA8");
// ROM_RODATA_NUM static const char paddle_right[] = __LOAD_SPRITE("assets/arcade_jetpac/minigames/arkanoid/paddle_right.png", "IA8");

ROM_RODATA_NUM static const rgb paddle_color = {.red = 0xFF, .green = 0xD7, .blue = 0x00};
ROM_RODATA_NUM static const rgb element_colors[] = {
    {.red = 0x9D, .green = 0x9D, .blue = 0x9D},
    {.red = 0xFF, .green = 0x00, .blue = 0x00},
    {.red = 0xFF, .green = 0xFF, .blue = 0x00},
    {.red = 0x00, .green = 0x00, .blue = 0xFF},
    {.red = 0xFF, .green = 0x00, .blue = 0xFF},
    {.red = 0x00, .green = 0xFF, .blue = 0x00},
};

#define POWERUP_COLOR_STRENGTH 0x9D
ROM_RODATA_NUM static const rgb powerup_colors[] = {
    {.red = POWERUP_COLOR_STRENGTH, .green = 0x00, .blue = 0x00}, // POWERUP_LASER
    {.red = 0x00, .green = 0x00, .blue = POWERUP_COLOR_STRENGTH}, // POWERUP_ENLARGE
    {.red = 0x00, .green = POWERUP_COLOR_STRENGTH, .blue = 0x00}, // POWERUP_CATCH
    {.red = POWERUP_COLOR_STRENGTH, .green = POWERUP_COLOR_STRENGTH >> 1, .blue = 0x00}, // POWERUP_SLOW
    {.red = 0x00, .green = POWERUP_COLOR_STRENGTH, .blue = POWERUP_COLOR_STRENGTH}, // POWERUP_DISRUPTION
};
ROM_RODATA_PTR static const char *powerup_letters[] = {
    "L", // POWERUP_LASER
    "E", // POWERUP_ENLARGE
    "C", // POWERUP_CATCH
    "S", // POWERUP_SLOW
    "D", // POWERUP_DISRUPTION
};

int getVacantCollider(void) {
    for (int i = 0; i < COLLIDER_BUFFER_SIZE; i++) {
        if (!colliders[i].active) {
            return i;
        }
    }
    return -1;
}

BallStruct *spawnBall(int x, int y, int attach_to_paddle) {
    for (int i = 0; i < BALL_BUFFER_SIZE; i++) {
        BallStruct *ball = &balls[i];
        if (!ball->active) {
            ball->active = 1;
            ball->attached_to_paddle = attach_to_paddle;
            ball->xVel = 1;
            ball->yVel = -1;
            if (attach_to_paddle) {
                ball->x = paddle.x + ((paddle.width - BALL_WIDTH) >> 1);
                ball->y = paddle.y - BALL_WIDTH;
            } else {
                ball->x = x;
                ball->y = y;
            }
            ball->width = BALL_WIDTH;
            ball->height = BALL_WIDTH;
            return ball;
        }
    }
    return 0;
}

void resetGame(void) {
    paddle.x = 170 - PADDLE_ENDS_WIDTH;
    paddle.width = 16 + (2 * PADDLE_ENDS_WIDTH);
    points = 0;
    level = 0;
    
    for (int i = 0; i < COLLIDER_BUFFER_SIZE; i++) {
        // Make all colliders inactive
        colliders[i].active = 0;
        colliders[i].required_for_win = 0;
        colliders[i].points = 0;
    }
    // Walls - Always use 0-2
    for (int i = 0; i < 3; i++) {
        // General
        colliders[i].active = 1;
        colliders[i].can_kill = 0;
        colliders[i].has_color = 0;
        colliders[i].y = 0;
    }
    colliders[0].x = 0;
    colliders[0].width = BOARD_X_INSET + BOARD_BORDER;
    colliders[0].height = 240;
    colliders[1].x = 0;
    colliders[1].width = 320;
    colliders[1].height = BOARD_Y_OFFSET + BOARD_BORDER;
    colliders[2].x = 320 - (BOARD_X_INSET + BOARD_BORDER);
    colliders[2].width = BOARD_X_INSET + BOARD_BORDER;
    colliders[2].height = 240;
    // Tiles
    for (int x = 0; x < ROW_ELEMENTS; x++) {
        int x_start = BOARD_X_INSET + BOARD_BORDER + ((EL_WIDTH + 1) * x);
        for (int y = 0; y < COL_ELEMENTS; y++) {
            const rgb *color = &element_colors[y];
            int y_start = EL_Y_START + ((EL_HEIGHT + 1) * y);
            int next_collider = getVacantCollider();
            if (next_collider > -1) {
                ColliderStruct *tile = &colliders[next_collider];
                tile->x = x_start;
                tile->y = y_start;
                tile->width = EL_WIDTH;
                tile->height = EL_HEIGHT;
                tile->black_ended = 1;
                tile->has_color = 1;
                tile->active = 1;
                tile->can_kill = 1;
                tile->required_for_win = 1;
                tile->health = y == 0 ? 2 : 1;
                if (y == 0) {
                    tile->points = 50 * level;
                } else {
                    tile->points = 100 - (10 * y);
                }
                tile->color.red = color->red;
                tile->color.green = color->green;
                tile->color.blue = color->blue;
            }
        }
    }
    // Balls
    for (int i = 0; i < BALL_BUFFER_SIZE; i++) {
        if (i == 0) {
            spawnBall(0, 0, 1);
        } else {
            balls[i].active = 0;
        }
    }
}

int allWinTilesDestroyed(void) {
    for (int i = 0; i < 100; i++) {
        ColliderStruct *col = &colliders[i];
        if (col->active && col->required_for_win) {
            return 0;
        }
    }
    return 1;
}

void spawnPowerup(int x, int y, powerUpState power_up) {
    for (int i = 0; i < POWER_UP_BUFFER_SIZE; i++) {
        PowerUpStruct *pu = &power_ups[i];
        if (!pu->active) {
            pu->active = 1;
            pu->x = x;
            pu->y = y;
            pu->height = 8;
            pu->width = 16;
            pu->frame = 0;
            pu->power_up = power_up;
            return;
        }
    }
}

void collectPowerUp(PowerUpStruct *pu) {
    pu->active = 0;
    current_power_up = pu->power_up;
    if (pu->power_up == POWERUP_DISRUPTION) {
        for (int i = 0; i < BALL_BUFFER_SIZE; i++) {
            BallStruct *ball = &balls[i];
            if (ball->active) {
                BallStruct *ball_0 = spawnBall(ball->x, ball->y, 0);
                if (ball_0) {
                    ball_0->xVel = 0;
                }
                BallStruct *ball_1 = spawnBall(ball->x, ball->y, 0);
                if (ball_1) {
                    ball_1->xVel = -ball->xVel;
                }
                break;
            }
        }
    }
}

void destroyBall(BallStruct *ball) {
    ball->active = 0;
    int active_count = 0;
    for (int i = 0; i < BALL_BUFFER_SIZE; i++) {
        if (balls[i].active) {
            active_count++;
        }
    }
    if ((active_count < 2) && (current_power_up == POWERUP_DISRUPTION)) {
        current_power_up = POWERUP_NONE;
    }
}

int powerUpColliding(PowerUpStruct *pu, ColliderStruct *pdl) {
    if ((pu->y < (pdl->y + pdl->height)) && ((pu->y + pu->height) > pdl->y)) {
        if ((pu->x + pu->width) < pdl->x) {
            return 0;
        }
        if (pu->x > (pdl->x + pdl->width)) {
            return 0;
        }
        return 1;
    }
    return 0;
}

void renderPowerUp(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (int i = 0; i < POWER_UP_BUFFER_SIZE; i++) {
        PowerUpStruct *pu = &power_ups[i];
        if (pu->active) {
            const rgb *color = &powerup_colors[pu->power_up - 1];
            dl = setFillColor(dl, color->red, color->green, color->blue);
            gDPFillRectangle(dl++, pu->x, pu->y, pu->x + pu->width, pu->y + pu->height);
        }
    }
    *dl_ptr = dl;
}

void renderPowerUpText(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    for (int i = 0; i < POWER_UP_BUFFER_SIZE; i++) {
        PowerUpStruct *pu = &power_ups[i];
        if (pu->active) {
            gDPSetScissor(dl++, G_SC_NON_INTERLACE, pu->x, pu->y, pu->x + pu->width, pu->y + pu->height);
            renderText(&dl, pu->x + 4, pu->y - 8 + pu->frame, 0xFF, 0xD7, 0x00, 0xFF, powerup_letters[pu->power_up - 1]);
        }
    }
    gDPSetScissor(dl++, G_SC_NON_INTERLACE, 0, 0, 319, 239);
    *dl_ptr = dl;
}

void handlePowerUpItems(void) {
    for (int i = 0; i < POWER_UP_BUFFER_SIZE; i++) {
        PowerUpStruct *pu = &power_ups[i];
        if (pu->active) {
            pu->y++;
            if (powerUpColliding(pu, &paddle)) {
                collectPowerUp(pu);
            } else if (pu->y > KILL_PLANE) {
                pu->active = 0;
            } else {
                pu->frame++;
                if (pu->frame > 16) {
                    pu->frame = 0;
                }
            }
        }
    }
}

void powerUpHandler(void) {
    // Paddle Length
    if (current_power_up == POWERUP_ENLARGE) {
        if (paddle.width < (32 + (2 * PADDLE_ENDS_WIDTH))) {
            paddle.width++;
        }
    } else {
        if (paddle.width > (16 + (2 * PADDLE_ENDS_WIDTH))) {
            paddle.width--;
        }
    }
}

void tileDestroyCode(ColliderStruct *tile) {
    if (!tile->can_kill) {
        return;
    }
    if (tile->health >= 2) {
        tile->health--;
        return;
    }
    // Make inactive
    tile->active = 0;
    points += tile->points;
    if (allWinTilesDestroyed()) {
        gameVictory();
        return;
    }
    if (current_power_up == POWERUP_DISRUPTION) {
        return;
    }
    int rng = getRNGLower31();
    if ((rng & 7) == 0) {
        rng = getRNGLower31() & 0xF;
        powerUpState pu = power_up_table[rng];
        spawnPowerup(tile->x + (tile->width >> 1), tile->y + tile->height, pu);
    }
}

void handleState_init(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    game_state = GAMESTATE_TITLE;
    gameInit();
    resetGame();
    *dl_ptr = dl;
}

void handleState_title(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    game_state = GAMESTATE_NORMAL;
    
    *dl_ptr = dl;
}

void renderDecals(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    // Top header
    renderText(&dl, 0x48, 0x13, 0xFF, 0x00, 0x00, 0xFF, "1UP");
    renderText(&dl, 0x48, 0x1B, 0xFF, 0xFF, 0xFF, 0xFF, "00");
    renderText(&dl, 0x78, 0x13, 0xFF, 0x00, 0x00, 0xFF, "HIGH SCORE");
    renderText(&dl, 0x78, 0x1B, 0xFF, 0xFF, 0xFF, 0xFF, "50000");
    // Paddle Ends
    *dl_ptr = dl;
}

void checkCollision(BallStruct *ball, ColliderStruct *col, CollisionPacketStruct *pkt) {
    pkt->colliding = 0;

    int t_enter_num = 0;
    int t_enter_den = 1;
    int t_exit_num  = 1;
    int t_exit_den  = 1;

    int hit_axis = -1; // 0 = X, 1 = Y

    // --- X axis ---
    if (ball->xVel == 0) {
        if ((ball->x + ball->width) < col->x || ball->x > (col->x + col->width)) {
            return; // no collision possible
        }
    } else {
        int tx1_num = col->x - (ball->x + ball->width); // left of collider minus right of ball
        int tx2_num = (col->x + col->width) - ball->x;  // right of collider minus left of ball
        int tx_den  = ball->xVel;

        if (tx_den < 0) {
            tx_den = -tx_den;
            tx1_num = -tx1_num;
            tx2_num = -tx2_num;
        }

        int tmin_num = tx1_num < tx2_num ? tx1_num : tx2_num;
        int tmax_num = tx1_num > tx2_num ? tx1_num : tx2_num;

        if ((tmin_num * t_enter_den) > (t_enter_num * tx_den)) {
            t_enter_num = tmin_num;
            t_enter_den = tx_den;
            hit_axis = 0;
        }

        if ((tmax_num * t_exit_den) < (t_exit_num * tx_den)) {
            t_exit_num = tmax_num;
            t_exit_den = tx_den;
        }
    }

    // --- Y axis ---
    if (ball->yVel == 0) {
        if ((ball->y + ball->height) < col->y || ball->y > (col->y + col->height)) {
            return; // no collision possible
        }
    } else {
        int ty1_num = col->y - (ball->y + ball->height); // top of collider minus bottom of ball
        int ty2_num = (col->y + col->height) - ball->y;  // bottom of collider minus top of ball
        int ty_den  = ball->yVel;

        if (ty_den < 0) {
            ty_den = -ty_den;
            ty1_num = -ty1_num;
            ty2_num = -ty2_num;
        }

        int tmin_num = ty1_num < ty2_num ? ty1_num : ty2_num;
        int tmax_num = ty1_num > ty2_num ? ty1_num : ty2_num;

        if ((tmin_num * t_enter_den) > (t_enter_num * ty_den)) {
            t_enter_num = tmin_num;
            t_enter_den = ty_den;
            hit_axis = 1;
        }

        if ((tmax_num * t_exit_den) < (t_exit_num * ty_den)) {
            t_exit_num = tmax_num;
            t_exit_den = ty_den;
        }
    }

    // --- No overlap ---
    if ((t_enter_num * t_exit_den) > (t_exit_num * t_enter_den)) {
        return;
    }

    // t_enter must be within [0,1]
    if (t_enter_num < 0 || t_enter_num > t_enter_den) {
        return;
    }

    // --- Collision point ---
    pkt->collision_x = ball->x + (ball->xVel * t_enter_num) / t_enter_den;
    pkt->collision_y = ball->y + (ball->yVel * t_enter_num) / t_enter_den;
    pkt->colliding = 1;

    // --- Reflect velocity ---
    if (hit_axis == 0) {
        ball->xVel = -ball->xVel;
    } else if (hit_axis == 1) {
        ball->yVel = -ball->yVel;
    }
}


void renderBalls(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    // Collision
    for (int b = 0; b < BALL_BUFFER_SIZE; b++) {
        BallStruct *ball = &balls[b];
        if (ball->active) {
            if (!ball->attached_to_paddle) {
                CollisionPacketStruct packet;
                ColliderStruct *colliding_object = 0;
                for (int i = 0; i < COLLIDER_BUFFER_SIZE + 1; i++) {
                    ColliderStruct *data = &paddle; // Player always checked first
                    if (i > 0) {
                        data = &colliders[i - 1]; // Then check other colliders
                    }
                    if (data->active) {
                        checkCollision(ball, data, &packet);
                        if (packet.colliding) {
                            // Now is colliding with object
                            colliding_object = data;
                            break;
                        }
                    }
                }
                if ((colliding_object) && (!ball->colliding)) {
                    ball->x = packet.collision_x;
                    ball->y = packet.collision_y;
                    ball->colliding = 1;
                    tileDestroyCode(colliding_object);
                    ball->collision_polarity ^= 1;
                    playSFXWrapper(159 + ball->collision_polarity);
                } else {
                    ball->x += ball->xVel;
                    ball->y += ball->yVel;
                    ball->colliding = 0;
                }
                if (ball->y > KILL_PLANE) {
                    destroyBall(ball);
                }
            }
            // Rendering
            dl = setFillColor(dl, 50, 168, 157);
            gDPFillRectangle(dl++, ball->x, ball->y, ball->x + BALL_WIDTH, ball->y + BALL_WIDTH);
        }
    }
    *dl_ptr = dl;
}

void renderBoard(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    // All Colliders
    for (int i = 0; i < COLLIDER_BUFFER_SIZE; i++) {
        ColliderStruct *col = &colliders[i];
        if (col->active) {
            if (col->has_color) {
                int inset = 0;
                if (col->black_ended) {
                    inset = 1;
                    dl = setFillColor(dl, 0, 0, 0);
                    gDPFillRectangle(dl++, col->x, col->y, col->x + col->width, col->y + col->height);
                }
                dl = setFillColor(dl, col->color.red, col->color.green, col->color.blue);
                gDPFillRectangle(dl++, col->x, col->y, col->x + col->width - inset, col->y + col->height - inset);
            }
        }
    }
    renderBalls(&dl);
    handlePowerUpItems();
    powerUpHandler();
    renderPowerUp(&dl);
    // Paddle
	// gDPSetPrimColor(dl++, 0, 0, 0, 0xFF - paddle_color.red, 0xFF - paddle_color.green, 0xFF - paddle_color.blue);
    // dl = displayImageCustom(dl, &paddle_left, 3, IA8, 8, 8, (paddle.x + 8) - 8, paddle.y, 1.0f, 1.0f, 0, 0.0f);
    // dl = displayImageCustom(dl, &paddle_right, 3, IA8, 8, 8, (paddle.x + 8) + (paddle.width - 16), paddle.y, 1.0f, 1.0f, 0, 0.0f);
    //
    dl = setFillColor(dl, (paddle_color.red * 3) >> 2, (paddle_color.green * 3) >> 2, (paddle_color.blue * 3) >> 2);
    gDPFillRectangle(dl++,
        paddle.x + PADDLE_ENDS_WIDTH,
        paddle.y,
        paddle.x + paddle.width - PADDLE_ENDS_WIDTH,
        paddle.y + 7
    );
    dl = setFillColor(dl, (paddle_color.red * 9) / 10, (paddle_color.green * 9) / 10, (paddle_color.blue * 9) / 10);
    gDPFillRectangle(dl++,
        paddle.x + PADDLE_ENDS_WIDTH,
        paddle.y + 1,
        paddle.x + paddle.width - PADDLE_ENDS_WIDTH,
        paddle.y + 5
    );
    dl = setFillColor(dl, (paddle_color.red * 9) / 10, (paddle_color.green * 9) / 10, (paddle_color.blue * 9) / 10);
    gDPFillRectangle(dl++,
        paddle.x + PADDLE_ENDS_WIDTH,
        paddle.y + 2,
        paddle.x + paddle.width - PADDLE_ENDS_WIDTH,
        paddle.y + 3
    );
    dl = setFillColor(dl, 0xFF, 0xFF, 0xFF);
    gDPFillRectangle(dl++,
        paddle.x + PADDLE_ENDS_WIDTH,
        paddle.y + 3,
        paddle.x + paddle.width - PADDLE_ENDS_WIDTH,
        paddle.y + 4
    );
    renderDecals(&dl);
    renderPowerUpText(&dl);
    *dl_ptr = dl;
}

void handleState_normal(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    int ball_delta = 0;
    if ((MinigameInput->stickX < -0x20) || MinigameInput->Buttons.d_left) {
        paddle.x  -= 2;
        int lim = BOARD_X_INSET + BOARD_BORDER;
        if (paddle.x < lim) {
            paddle.x = lim;
        } else {
            ball_delta = -2;
        }
    } else if ((MinigameInput->stickX > 0x20) || MinigameInput->Buttons.d_right) {
        paddle.x += 2;
        int lim2 = 320 - (BOARD_X_INSET + BOARD_BORDER + paddle.width - (2 * PADDLE_ENDS_WIDTH));
        if (paddle.x > lim2) {
            paddle.x = lim2;
        } else {
            ball_delta = 2;
        }
    }
    for (int i = 0; i < BALL_BUFFER_SIZE; i++) {
        if (balls[i].active && balls[i].attached_to_paddle) {
            balls[i].x += ball_delta;
            if (p1PressedButtons & A_BUTTON) {
                balls[i].attached_to_paddle = 0;
            }
        }
    }
    renderBoard(&dl);
    *dl_ptr = dl;
}

void loop(Gfx **dl_ptr) {
    Gfx *dl = *dl_ptr;
    if (game_state != GAMESTATE_INIT) {
        dl = minigame_dl_init(dl, 0, 0, 0, 0);
        dl = setFillColor(dl, 143, 143, 143);
        gDPFillRectangle(dl++, BOARD_X_INSET, BOARD_Y_OFFSET, 319 - BOARD_X_INSET, 239);
        dl = setFillColor(dl, 0, 0, 174);
        gDPFillRectangle(dl++, BOARD_BORDER + BOARD_X_INSET, BOARD_Y_OFFSET + BOARD_BORDER, 319 - (BOARD_BORDER + BOARD_X_INSET), 239);
    }
    switch(game_state) {
        case GAMESTATE_INIT:
            handleState_init(&dl);
            break;
        case GAMESTATE_TITLE:
            handleState_title(&dl);
            break;
        case GAMESTATE_NORMAL:
            handleState_normal(&dl);
            break;
        default:
            break;
    }
    *dl_ptr = dl;
}