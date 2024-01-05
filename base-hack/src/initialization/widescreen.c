/**
 * @file widescreen.c
 * @author Gamemasterplc, Ballaam
 * @brief Ported from the Widescreen DK64 Hack by Gamemasterplc (https://patch.wedarobi.com/dk_widescreen)
 * @version 0.1
 * @date 2023-06-25
 * 
 * @copyright Copyright (c) 2023
 * 
 */
#include "../../include/common.h"

static double pos_center_4x = SCREEN_WD_FLOAT * 2;
static double pos_center = SCREEN_WD_FLOAT / 2;
#define ZIPPER_COLOR_VALUE 0xFFFF

/*
    FIX LIST
    - fairy calculation grid
    - race coin counter
    - fix n64 not working (vc doesn't render anything)
    - Loading bar
    - fix various hud items
    - fix jetpac and arcade
    - Krazy KK/PPP Melon HUD
    - BP screen
    - BBBandit A Button
    - are you sure quit
*/

#define NINTENDO_LOGO_WIDTH 256

void ws_2d(void) {
    // loadSingularHook(0x8070F308, &arcadeRepositionY);
    float base_x = 0.25f;
    float base_y = 0.25f;
    base_y *= (SCREEN_HD_FLOAT / 240.0f);
    *(short*)(0x8070F322) = *(short*)(&base_x);
    *(short*)(0x8070F366) = *(short*)(&base_y);
}

void ws_fileentry(int map, int exit) {
    setNextTransitionType(2);
    initiateTransition(map, exit);
}

void ws_ninPos(void) {
    *(short*)(0x805FB8A6) = getUpper(SCREEN_WD*SCREEN_HD*2);
    *(int*)(0x805FB8A8) = 0x08000000 | ((((int)(&fixNintendoLogoPosition)) & 0xFFFFFF) >> 2);
    *(short*)(0x805FB8AE) = getLower(SCREEN_WD*SCREEN_HD*2);
}

void ws_boot(void) {
    int framebuffer_clear = SCREEN_WD * SCREEN_HD;
    int framebuffer_size = framebuffer_clear << 2;
    *(int*)(0x80610378) = 0x3C0F0000 | ((framebuffer_size >> 16) & 0xFFFF); //Load Size of Framebuffer 
    *(int*)(0x8061037C) = 0x35EF0000 | (framebuffer_size & 0xFFFF); //Load Size of Framebuffer
    *(short*)(0x80610956) = (framebuffer_clear >> 16) & 0xFFFF; //Upper Half of Framebuffer Clear Length
    *(short*)(0x80610962) = framebuffer_clear & 0xFFFF; //Lower Half of Framebuffer Clear Length
    // Nintendo Logo
    *(short*)(0x805FB902) = (SCREEN_WD - NINTENDO_LOGO_WIDTH) * 2; //Line Pixel Advance for Nintendo Logo
    ws_ninPos();
}

void ws_hud(void) {
    float medal_x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x80687CAA) = *(short*)(&medal_x); // Medal Reward
    float medal_y = SCREEN_HD_FLOAT / 2;
    *(short*)(0x80687CAE) = *(short*)(&medal_y); // Medal Reward

    float circle_scale = SCREEN_WD_FLOAT / 63.0f;
    *(short*)(0x806FFBA6) = *(short*)(&circle_scale); // Fix Camera Transition
    *(short*)(0x806FFBBA) = SCREEN_WD / 2; // X Position of Circle Transition
    *(short*)(0x806FFBBE) = SCREEN_HD / 2; // Y Position of Circle Transition
    *(short*)(0x806FEFBA) = *(short*)(&circle_scale); // Fix cannon game reticle
}

void ws_crashdebugger(void) {
    // *(int*)(0x80731C04) = 0x24190000 | 160; // Force crash debugger width
    // *(int*)(0x80731CE0) = 0x240F0000 | 160; // Force crash debugger width
}

void ws_timer(int* x_write) {
    spawnActor(0xB0, 0);
    int x = *x_write & 0x7FFF;
    if (x >= 0x78) {
        if (x < 0xC8) {
            *x_write = *x_write + ((SCREEN_WD / 2) - 160);
        } else {
            *x_write = *x_write + (SCREEN_WD - 320);
        }
    }
}

#define ZIPPER_IS_WIDESCREEN 1

void ws_transitions(void) {
    if (WS_REMOVE_ZIPPER) {
        writeFunction(0x8071456C, &ws_fileentry);
    }
    *(short*)(0x80629292) = SCREEN_WD - 10; //X Position of Transition from Right
    *(short*)(0x806292A2) = SCREEN_WD / 2; //X Position of Double Transition
    *(short*)(0x80629902) = SCREEN_WD - 9; // Maximum X Position of Transition 0
    *(short*)(0x806299EE) = SCREEN_WD - 15; // Maximum X Position of Transition 1
    *(short*)(0x80629C9E) = SCREEN_WD - 15; // Maximum X Position of Transition 2
    *(short*)(0x80629D5E) = SCREEN_WD - 9; // Maximum X Position of Transition 3
    float temp = (SCREEN_WD_FLOAT / 2) + 10.0f;
    *(short*)(0x80629E6E) = *(short*)(&temp); // Maximum X Position of Transition 4
    temp = SCREEN_WD + 30.0f;
    *(short*)(0x80629F96) = *(short*)(&temp); // Maximum X Position of Transition 5
    *(short*)(0x8062A09E) = *(short*)(&temp); // Maximum X Position of Transition 6

    temp = SCREEN_WD;
    *(short*)(0x80629E26) = *(short*)(&temp); // Width of Transitions 4
    *(short*)(0x80629F4E) = *(short*)(&temp); // Width of Transitions 5
    *(short*)(0x8062A00E) = *(short*)(&temp); // Width of Transitions 6
    temp = SCREEN_HD - 1;
    *(short*)(0x80629962) = *(short*)(&temp); // Height of Transitions 0
    *(short*)(0x8062997E) = temp; // Height of Transitions 0
    *(short*)(0x80629A0A) = *(short*)(&temp); // Height of Transitions 0
    *(short*)(0x80629A12) = temp; // Height of Transitions 0

    *(short*)(0x806296C6) = *(short*)(&temp); // Height of Transitions 1
    *(short*)(0x806296D6) = temp; // Height of Transitions 1

    *(short*)(0x806297AA) = *(short*)(&temp); // Height of Transitions 2
    *(short*)(0x806297C2) = temp; // Height of Transitions 2
    *(short*)(0x80629866) = *(short*)(&temp); // Height of Transitions 2
    *(short*)(0x80629872) = temp; // Height of Transitions 2
    
    *(short*)(0x80629B0E) = *(short*)(&temp); // Height of Transitions 3
    *(short*)(0x80629B26) = temp; // Height of Transitions 3
    *(short*)(0x80629B6E) = *(short*)(&temp); // Height of Transitions 3
    *(short*)(0x80629B82) = temp; // Height of Transitions 3
    *(short*)(0x80629C16) = *(short*)(&temp); // Height of Transitions 3
    *(short*)(0x80629C22) = temp; // Height of Transitions 3
    *(short*)(0x80629CBA) = *(short*)(&temp); // Height of Transitions 3
    *(short*)(0x80629CC2) = temp; // Height of Transitions 3

    *(short*)(0x80629E2E) = *(short*)(&temp); // Height of Transitions 4
    *(short*)(0x80629DEA) = temp; // Height of Transitions 4

    *(short*)(0x80629F56) = *(short*)(&temp); // Height of Transitions 5
    *(short*)(0x80629F12) = temp; // Height of Transitions 5

    *(short*)(0x8062A01E) = *(short*)(&temp); // Height of Transitions 6
    *(short*)(0x8062A03E) = temp; // Height of Transitions 6

    *(short*)(0x806295F6) = *(short*)(&temp); // Height of Transitions 7
    *(short*)(0x8062960A) = temp; // Height of Transitions 7

    float zipper_aspect_ratio = SCREEN_WD_FLOAT / SCREEN_HD_FLOAT;
    int zipper_aspect_ratio_int = *(int*)(&zipper_aspect_ratio);
    *(short*)(0x8070ADC6) = (zipper_aspect_ratio_int >> 16) & 0xFFFF;
    *(short*)(0x8070ADCA) = zipper_aspect_ratio_int & 0xFFFF;

    int zipper_scissor = 0;
    int framebuffer_upperleft = (SCREEN_WD / 8) - 2;
    int framebuffer_lowerright = (SCREEN_WD / 8) + 2;
    if (ZIPPER_IS_WIDESCREEN) {
        int interpolation_mode = 0;
        int zipper_lower_right = ((SCREEN_WD - 11) << 2);
        int zipper_lower_right_h = ((SCREEN_HD - 11) << 2);
        zipper_scissor = (interpolation_mode << 0x18) | (zipper_lower_right << 12) | zipper_lower_right_h;
        *(int*)(0x807095F4) = 0x24030140; //Force Zipper Transition Width
    } else {
        zipper_scissor = ((SCREEN_WD - 11) << 14) | ((SCREEN_HD - 11) << 2);
        *(int*)(0x807095F4) = 0x24030140; //Force Zipper Transition Width
    }
    *(short*)(0x8070BFA6) = 0xE400 | framebuffer_lowerright; //Zipper Right Edge X Position
    *(short*)(0x8070C07E) = framebuffer_upperleft; //Zipper Left Edge X Position
    *(short*)(0x8070AE02) = getUpper(zipper_scissor); //Upper Part of Zipper Transition Scissor
    *(short*)(0x8070AE0E) = getLower(zipper_scissor); //Lower Part of Zipper Transition Scissor
}

void ws_pause(void) {
    float out_of_y = (4 * SCREEN_HD_FLOAT) - 180.0f;
    *(short*)(0x806A9C92) = *(short*)(&out_of_y);
    *(short*)(0x806A9CD2) = *(short*)(&out_of_y);
    *(short*)(0x806A9E66) = *(short*)(&out_of_y);
    *(short*)(0x806A9E9E) = *(short*)(&out_of_y);
    *(short*)(0x806A9FBA) = (SCREEN_HD << 2) - 132;
}

void left_to_yconvert(void) {
    *(int*)(0x806FD4C4) = 0x25D00000 | (((SCREEN_WD / 2) - 160) & 0xFFFF); // X Offset of Text
    *(short*)(0x806A94AE) = SCREEN_WD; //Max X Position of UI Elements
    *(int*)(0x8070F308) = 0x08000000 | ((((int)(fixTilePosition)) & 0xFFFFFF) >> 2);
    *(short*)(0x807098D2) = 0xE08; //Double a Structure Size for Zipper
    *(short*)(0x80709F5E) = SCREEN_WD - 1; //Width of Zipper Fade Texture
    *(short*)(0x80700012) = ((SCREEN_WD / 2) - 80) * 2; //Source Offset for Camera Picture Copy
}

void ws_text(void) {
    *(short*)(0x8069FCAA) = SCREEN_WD; //Screen Width for Large Words
    float temp = SCREEN_WD >> 1;
    *(short*)(0x8069D9F6) = *(short*)(&temp); // X Position of Bending Text
    *(short*)(0x8069DA2A) = *(short*)(&temp); // X Position of Bending Text 2
    *(short*)(0x806C7852) = *(short*)(&temp); //X Position of Top Credits
    *(short*)(0x806C7882) = *(short*)(&temp); //X Position of Bottom Credits
    temp = SCREEN_HD >> 1;
    *(short*)(0x806C78CA) = *(short*)(&temp); //Y Position of Left Credits
    *(short*)(0x806C7912) = *(short*)(&temp); //Y Position of Right Credits

    temp = SCREEN_WD << 1;
    *(short*)(0x8069FF5E) = *(short*)(&temp); // X Position of Round Number
    temp = (SCREEN_HD_FLOAT / 2) - 40.0f;
    *(short*)(0x8069FF52) = *(short*)(&temp); // Y Position of Round Number
}

void ws_static(void) {
    ws_hud();
    ws_crashdebugger();

    *(int*)(0x806A2A34) = 0x0C000000 | ((((int)(&ws_timer)) & 0xFFFFFF) >> 2); // Timer Reposition
    *(int*)(0x806A2A2C) = 0x27A40018;

    *(short*)(0x805FB982) = 1; // Disable High Resolution for MAP_NINTENDOLOGO
    
    *(short*)(0x807075EE) = (SCREEN_WD / 128) + 2; //Number of Tiles Rendered in Main Menu Background

    ws_transitions();
    ws_pause();
    left_to_yconvert();
    ws_text();
    ws_2d();

    *(int*)(0x806AC3E4) = 0x3C010000 | getHi(&pos_center_4x); //Load High Half of pos_center_4x
    *(int*)(0x806AC3E8) = 0xD4280000 | getLo(&pos_center_4x); //Load pos_center_4x
    *(int*)(0x806AC3EC) = 0x46020102; //Run Replaced Instruction

    float width = (SCREEN_WD_FLOAT * 460) / 320;
    *(short*)(0x80706D26) = *(short*)(&width); // Background Width in Snide Race
    float height = (SCREEN_HD_FLOAT * 380) / 240;
    *(short*)(0x80706D3E) = *(short*)(&height); // Background Height in Snide Race

    *(short*)(0x8070FCA6) = SCREEN_WD; //Max X Position of Reset Banana in Storm
    *(short*)(0x80712112) = SCREEN_WD; //Screen Range of Banana Storm
    int transition_scissor = ((SCREEN_WD - 11) << 14) | ((SCREEN_HD - 11) << 2);
    *(short*)(0x8071331E) = (transition_scissor >> 16) & 0xFFFF; //Upper Part of Transition Scissor
    *(short*)(0x8071334A) = transition_scissor & 0xFFFF; //Lower Part of Transition Scissor
    *(short*)(0x8071390A) = SCREEN_WD - 11; //Viewport Width of Transitions
    *(short*)(0x807138F2) = SCREEN_HD - 11; //Viewport Height of Transitions
    *(short*)(0x80713C46) = SCREEN_WD << 1; //X Position of Game Over Text
    *(int*)(0x80714B58) = 0x24190000 | (SCREEN_WD-11); //Scissor Width of UI
    *(int*)(0x80714B6C) = 0x24080000 | (SCREEN_HD-11); //Scissor Height of UI
   
    // Got up to here

    float d_x = (SCREEN_WD_FLOAT*2)-190;
    int d_x_int = *(int*)(&d_x);
    *(int*)(0x80728E08) = 0x3C0D0000 | ((d_x_int >> 16) & 0xFFFF); //X Position of D Letter in Intro
    *(int*)(0x80728E0C) = 0x35AD0000 | (d_x_int & 0xFFFF); //X Position of D Letter in Intro
    *(int*)(0x80728E1C) = 0xAD8D007C; //Write X Position of D Letter in Intro

    d_x = (SCREEN_WD_FLOAT*2)+180;
    d_x_int = *(int*)(&d_x);
    *(int*)(0x80728E38) = 0x3C190000 | ((d_x_int >> 16) & 0xFFFF); //X Position of K Letter in Intro
    *(int*)(0x80728E3C) = 0x37390000 | (d_x_int & 0xFFFF); //X Position of K Letter in Intro
    *(int*)(0x80728E4C) = 0xAF19007C; //Write X Position of K Letter in Intro
    d_x = (SCREEN_WD * 2) - 140;
    *(int*)(0x80728E88) = 0x3C0F0000 | *(short*)(&d_x); //X Position of Round Text
    *(int*)(0x80728EA0) = 0xADCF007C; //Write X Position of Round Text

    *(short*)(0x8062A8C8) = 0x1000; // Disable Anamorphic Widescreens

    *(short*)(0x806A965A) = (SCREEN_WD*2); // X Position of Melons
    *(short*)(0x806A993A) = (SCREEN_WD*2); // X Position of Pause Menu Options
    *(short*)(0x806A9836) = (SCREEN_WD*2); // X Position of Are You Sure Text
    *(short*)(0x806A99D2) = (SCREEN_HD * 2) - 220; // Y Position of Are You Sure Text
    *(short*)(0x806A9A0A) = (SCREEN_WD*2); // X Position of Pause Menu Yes Option
    *(short*)(0x806A9A12) = (SCREEN_HD * 2) - 120; // Y Position of Pause Menu Yes Option
    *(short*)(0x806A9A42) = (SCREEN_WD*2); // X Position of Pause Menu No Option
    *(short*)(0x806A9A46) = (SCREEN_HD * 2) + 80; // Y Position of Pause Menu Yes Option
    
    // Not touched this block
    *(short*)(0x806A9B6A) = (SCREEN_WD*2); //X Position of DK Isles Icons
    *(short*)(0x806A9CA6) = ((SCREEN_WD*2)+40); //X Position of Banana Count
    *(short*)(0x806A9ED6) = ((SCREEN_WD*2)+48); //X Position of Banana Count
    *(short*)(0x806A9F6A) = (SCREEN_WD*2); //X Position of Golden Bananas Text
    *(short*)(0x806A9F92) = (SCREEN_WD*2); //X Position of Totals Text
    *(short*)(0x806A9FB6) = (SCREEN_WD*2); //X Position of Total Golden Banana Count

    *(short*)(0x806AA6AA) = (SCREEN_WD-30); //X Position of Coin Counter
    *(short*)(0x806AA6DE) = (SCREEN_WD-30); //X Position of Coin Icon
    *(short*)(0x806AA6F6) = (SCREEN_WD-30); //X Position of Drum Counter
    *(short*)(0x806AA752) = (SCREEN_WD-30); //X Position of Drum Icon
    *(short*)(0x806AA796) = (SCREEN_WD-30); //X Position of Film Reel Counter
    *(short*)(0x806AA7CA) = (SCREEN_WD-30); //X Position of Film Reel Icon
    *(short*)(0x806AA7E6) = ((SCREEN_WD/2)-15); //X Position of Golden Banana Counter
    *(short*)(0x806AA832) = ((SCREEN_WD/2)-15); //X Position of Golden Banana Icon
    *(short*)(0x806AAACE) = ((SCREEN_WD/2)-15); //X Position of Golden Banana Icon
    *(short*)(0x806AAC1E) = (SCREEN_WD/2); //X Position of Analog Stick on Character Wheel
    *(short*)(0x806AAFA6) = (SCREEN_WD/2); //X Position of Crown
    *(short*)(0x806AB036) = (SCREEN_WD-60); //X Position of Fairy 2 on Kongs Screen
    *(short*)(0x806AB1B2) = (SCREEN_WD-60); //X Position of Fairy 3 on Maps
    *(short*)(0x806AB1EE) = (SCREEN_WD-70); //X Position of Fairy 4 on Maps
    *(short*)(0x806AB22A) = ((SCREEN_WD/2)-15); //X Position of Golden Banana Icon
    *(short*)(0x806AB42E) = (SCREEN_WD/2); //X Position of Totals Screen X Position
    *(short*)(0x806AB4BE) = (SCREEN_WD-45); //X Position of R Button

    float wheel_center_y = SCREEN_HD_FLOAT * 2;
    *(short*)(0x806A9ADE) = *(short*)(&wheel_center_y);

    d_x = SCREEN_WD_FLOAT * 2;
    *(short*)(0x806AB682) = *(short*)(&d_x); //Max X Position of UI Icon Slide Out
    *(short*)(0x806AB916) = *(short*)(&d_x); //Max X Position of UI Slide Out
    *(short*)(0x806ABB12) = SCREEN_WD * 2; //X Position of Level Name
    *(short*)(0x806ABB42) = SCREEN_WD * 2; //X Position of Level Icon
}

void ws_staticdata(void) {
    *(float*)(0x807444BC) = SCREEN_WD_FLOAT / SCREEN_HD_FLOAT; //Aspect Ratio of Help Text
    *(double*)(0x8075ACD0) = (SCREEN_WD_FLOAT * 2) - 40; //X Position of Up C Button
    *(double*)(0x8075ACD8) = (SCREEN_WD_FLOAT * 2) + 40; //X Position of Down C Button
    *(double*)(0x8075C3F8) = SCREEN_HD_FLOAT + 55; //Y Offset of Player Names for Credits Bottom
    *(double*)(0x8075C408) = SCREEN_WD_FLOAT + 70; //X Offset of Player Names for Credits Right
    *(int*)(0x80747B30) = SCREEN_WD; //Blurring size X
    *(int*)(0x80747B34) = SCREEN_HD; //Blurring size Y

    /*
    Not needed for Rando (Multiplayer)
    *(short*)(0x80750878) = (SCREEN_WD-1); //Right Edge of Blackness in Border 5
    *(short*)(0x8075088C) = (SCREEN_WD-13); //Left Edge of Blackness in Border 7
    *(short*)(0x80750890) = (SCREEN_WD-1); //Right Edge of Blackness in Border 7
    *(short*)(0x8075089C) = (SCREEN_WD-13); //Right Edge of Blackness in Border 8
    *(short*)(0x807508A8) = (SCREEN_WD-14); //Right Edge of Blackness in Border 9
    *(short*)(0x807508B0) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 10
    *(short*)(0x807508B4) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 11
    *(short*)(0x807508BC) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 12
    *(short*)(0x807508C0) = (SCREEN_WD-14); //Right Edge of Blackness in Border 12
    *(short*)(0x807508CC) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 13
    *(short*)(0x807508D8) = SCREEN_WD; //Right Edge of Blackness in Border 14
    *(short*)(0x807508E0) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 15
    *(short*)(0x807508E4) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 15
    *(short*)(0x807508EC) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 16
    *(short*)(0x807508F0) = (SCREEN_WD-14); //Right Edge of Blackness in Border 16
    *(short*)(0x807508F8) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 17
    *(short*)(0x807508FC) = (SCREEN_WD-14); //Right Edge of Blackness in Border 17
    *(short*)(0x80750904) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 18
    *(short*)(0x80750908) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 18
    *(short*)(0x80750914) = (SCREEN_WD-14); //Left Edge of Blackness in Border 19
    *(short*)(0x8075091C) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 20
    *(short*)(0x80750920) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 20
    *(short*)(0x8075092C) = (SCREEN_WD-14); //Left Edge of Blackness in Border 21
    *(short*)(0x80750934) = ((SCREEN_WD/2)-1); //Left Edge of Blackness in Border 22
    *(short*)(0x80750938) = ((SCREEN_WD/2)+1); //Right Edge of Blackness in Border 22
    */

    /*
    Not needed for Rando (multiplayer)
    *(short*)(0x80750968) = (SCREEN_WD-13); //Right Edge of Viewport Setup 3
    *(short*)(0x80750974) = (SCREEN_WD-13); //Right Edge of Viewport Setup 4
    *(short*)(0x80750980) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 5
    *(short*)(0x80750988) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 6
    *(short*)(0x8075098C) = (SCREEN_WD-13); //Right Edge of Viewport Setup 6
    *(short*)(0x80750998) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 7
    *(short*)(0x807509A0) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 8
    *(short*)(0x807509A4) = (SCREEN_WD-13); //Right Edge of Viewport Setup 8
    *(short*)(0x807509B0) = (SCREEN_WD-13); //Right Edge of Viewport Setup 9
    *(short*)(0x807509BC) = (SCREEN_WD-13); //Right Edge of Viewport Setup 10
    *(short*)(0x807509C8) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 11
    *(short*)(0x807509D0) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 12
    *(short*)(0x807509D4) = (SCREEN_WD-13); //Right Edge of Viewport Setup 12
    *(short*)(0x807509E0) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 13
    *(short*)(0x807509EC) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 14
    *(short*)(0x807509F4) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 15
    *(short*)(0x807509F8) = (SCREEN_WD-13); //Right Edge of Viewport Setup 15
    *(short*)(0x80750A00) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 16
    *(short*)(0x80750A04) = (SCREEN_WD-13); //Right Edge of Viewport Setup 16
    *(short*)(0x80750A10) = (SCREEN_WD-13); //Right Edge of Viewport Setup 17
    *(short*)(0x80750A1C) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 18
    *(short*)(0x80750A24) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 19
    *(short*)(0x80750A28) = (SCREEN_WD-13); //Right Edge of Viewport Setup 19
    *(short*)(0x80750A34) = (SCREEN_WD-13); //Right Edge of Viewport Setup 20
    *(short*)(0x80750A40) = (SCREEN_WD-13); //Right Edge of Viewport Setup 21
    *(short*)(0x80750A4C) = (SCREEN_WD-13); //Right Edge of Viewport Setup 22
    *(short*)(0x80750A58) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 23
    *(short*)(0x80750A60) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 24
    *(short*)(0x80750A64) = (SCREEN_WD-13); //Right Edge of Viewport Setup 24
    *(short*)(0x80750A70) = ((SCREEN_WD/2)-1); //Right Edge of Viewport Setup 25
    *(short*)(0x80750A78) = ((SCREEN_WD/2)+1); //Left Edge of Viewport Setup 26
    *(short*)(0x80750A7C) = (SCREEN_WD-13); //Right Edge of Viewport Setup 26
    *(short*)(0x80750A88) = (SCREEN_WD-13); //Right Edge of Viewport Setup 27
    *(short*)(0x80750A94) = (SCREEN_WD-13); //Right Edge of Viewport Setup 28
    *(short*)(0x80750AA0) = (SCREEN_WD-13); //Right Edge of Viewport Setup 29
    *(short*)(0x80750AAC) = (SCREEN_WD-13); //Right Edge of Viewport Setup 30
    */
    *(short*)(0x80754C08) = -((SCREEN_WD*128)/320); //Position of Vertex 1 of Transition
    *(short*)(0x80754C0A) = -((SCREEN_WD*128)/320); //Position of Vertex 1 of Transition
    *(short*)(0x80754C18) = ((SCREEN_WD*128)/320); //Position of Vertex 2 of Transition
    *(short*)(0x80754C1A) = -((SCREEN_WD*128)/320); //Position of Vertex 2 of Transition
    *(short*)(0x80754C28) = ((SCREEN_WD*128)/320); //Position of Vertex 3 of Transition
    *(short*)(0x80754C2A) = ((SCREEN_WD*128)/320); //Position of Vertex 3 of Transition
    *(short*)(0x80754C38) = -((SCREEN_WD*128)/320); //Position of Vertex 4 of Transition
    *(short*)(0x80754C3A) = ((SCREEN_WD*128)/320); //Position of Vertex 4 of Transition
    *(float*)(0x8075E4D8) = SCREEN_WD - 5.0f; //Max X Position of Banana in Storm    
}

int* ws_textDraw(int* dl, int style, int x, int y, char* str) {
    float y_f = y;
    y_f *= (SCREEN_HD_FLOAT / 240.0f);
    return textDraw(dl, style, x, y_f, str);
}

// void ws_sprite(void* unk0, int x, int y) {
//     float y_f = y;
//     y_f *= (SCREEN_HD_FLOAT / 240.0f);
//     drawRetroSprite(unk0, x, y_f);
// }

void ws_arcade(void) {
    int clear_rect_instruction = 0xF6000000 | ((SCREEN_WD-1) << 14) | ((SCREEN_HD-1) << 2); // Clear Rectangle for DK Arcade
    *(short*)(0x800242E6) = (clear_rect_instruction >> 16) & 0xFFFF;
    *(short*)(0x800242EA) = clear_rect_instruction & 0xFFFF;
    int scissor = ((SCREEN_WD - 48) << 14)|((SCREEN_HD - 8) << 2);
    *(short*)(0x80025B16) = getUpper(scissor); // Scissor Higher Half for DK Arcade
    *(short*)(0x80025B22) = getLower(scissor); //Scissor Lower Half for DK Arcade
    int scissor_rect = (SCREEN_WD << 14) | (SCREEN_HD << 2); // Scissor Rectangle for DK Arcade
    *(short*)(0x800319E6) = getUpper(scissor_rect);
    *(short*)(0x800319EA) = getLower(scissor_rect);
    //
    writeFunction(0x80024620, &ws_textDraw);
    // loadSingularHook(0x80025C64, &arcadeYRescale);
    // *(short*)(0x80025B1A) = 0x10; // Expand DL
    // loadSingularHook(0x80025b2c, &arcadeRescale);
}

void ws_jetpac(void) {
    int clear_rect_instruction = 0xF6000000 | ((SCREEN_WD-1) << 14) | ((SCREEN_HD-1) << 2);
    *(short*)(0x800242CE) = (clear_rect_instruction >> 16) & 0xFFFF; //Clear Rectangle for Jetpac High Half
    *(short*)(0x800242EA) = clear_rect_instruction & 0xFFFF; //Clear Rectangle for Jetpac Low Half
    int scissor = ((SCREEN_WD - 32) << 14) | ((SCREEN_HD - 24) << 2);
    *(short*)(0x800255F2) = (scissor >> 16) & 0xFFFF; // Scissor Higher Half for Jetpac
    *(short*)(0x800255FE) = scissor & 0xFFFF; //Scissor Lower Half for Jetpac
    //
    writeFunction(0x8002B06C, &ws_textDraw);
}

void ws_menu(void) {
    float x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x80028726) = getUpper(*(int*)(&x)); //X Position of Mode Name Text
    // Fix option text position
    *(int*)(0x8002FA28) = 0x3C010000 | getHi(&pos_center);
    *(int*)(0x8002FA2C) = 0xD42A0000 | getLo(&pos_center);
    // FILE SELECT
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x80028DA2) = getUpper(*(int*)(&x)); //X Position of File Names
    // FILE PROGRESS
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x800296D2) = *(short*)(&x); // X Position of Game 1 Text
    float delta_x = 45.0f * (SCREEN_HD_FLOAT / 240.0f);
    x = (SCREEN_WD_FLOAT / 2) - (2 * delta_x) + 8.0f;
    *(short*)(0x800291D6) = *(short*)(&x); // X Position of File Head Icons
    *(short*)(0x800291E2) = *(short*)(&delta_x); // Delta X of File Head Icons
    float y = 85.0f * (SCREEN_HD_FLOAT / 240.0f);
    *(short*)(0x800291FA) = *(short*)(&y); // Y Position of File Head Icons
    *(double*)(0x80033D48) = SCREEN_HD_FLOAT / 240.0f; // Head base scale
    // SELECT DELETE FILE
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x80029C02) = getUpper(*(int*)(&x)); //X Position of Erase Text
    // Multiplayer Type
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002A646) = getUpper(*(int*)(&x)); //X Position of Center of Battle Select Screen
    *(int*)(0x8002A83C) = 0x4600A6A1; //Fix X Position of Battle Icons
    *(short*)(0x8002ABCA) = SCREEN_WD - 30; //X Position of A Button
    *(short*)(0x8002AC32) = SCREEN_WD / 2; //X Position of Analog Stick
    // Delete Confirm
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002A0CE) = getUpper(*(int*)(&x)); //X Position of Erase Game 1 Text
    *(short*)(0x8002A20E) = getUpper(*(int*)(&x)); //X Position of Are You Sure
    x = (SCREEN_WD_FLOAT / 2) - 80;
    *(short*)(0x8002A296) = getUpper(*(int*)(&x)); //X Position of No/Yes Text
    y = (SCREEN_HD_FLOAT / 2) - 40.0f;
    *(short*)(0x8002A212) = *(short*)(&y); // Y Position of Are you sure
    y = SCREEN_HD_FLOAT / 2;
    *(short*)(0x8002A29A) = *(short*)(&y); // Y Position of No/Yes Text

    // Multiplayer Join
    x = (SCREEN_WD_FLOAT/2)+50;
    *(short*)(0x8002B756) = *(short*)(&x); //X Position of P2 Question Mark
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002B7EE) = *(short*)(&x); //X Position of P3 Question Mark
    x = (SCREEN_WD_FLOAT / 2) - 50;
    *(short*)(0x8002B886) = *(short*)(&x); //X Position of P4 Question Mark
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002B94A) = *(short*)(&x); //X Position of Battle Arena Text
    *(short*)(0x8002BA92) = SCREEN_WD * 2; //X Position of Game Type Text
    *(short*)(0x8002BB4A) = getHi(&pos_center);  //Load High Half of Game Mode X Position
    *(int*)(0x8002BB4C) = 0xD4240000 | getLo(&pos_center); //Load X Position of Game Mode
    *(int*)(0x8002BC18) = 0x3C010000 | getHi(&pos_center); //Load High Half of Game Type Value X Position
    *(int*)(0x8002BC1C) = 0xD4280000 | getLo(&pos_center); //Load X Position of Game Type Value
    *(short*)(0x8002BED6) = SCREEN_WD * 2; //X Position of Screen Type Text
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002BF16) = *(short*)(&x);
    // Sound
    *(short*)(0x8002D5B2) = SCREEN_WD * 2; //X Position of Sound
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002D646) = *(short*)(&x); //Base X Position of Sound Options
    y = (SCREEN_HD_FLOAT / 2) + 25.0f;
    *(short*)(0x8002D64A) = *(short*)(&y); // Base Y Position of Sound Options
    *(short*)(0x8002D826) = SCREEN_HD - 30; // Y Position of B Button
    *(short*)(0x8002D85A) = SCREEN_WD / 2; // X Position of Sound Analog Stick
    *(short*)(0x8002D85E) = (SCREEN_HD / 2) + 5; // Y Position of Sound Analog Stick
    *(short*)(0x8002D88E) = SCREEN_WD / 2; // X Position of Sound Z Button
    *(short*)(0x8002D892) = SCREEN_HD - 40; // Y Position of Sound Z Button
    *(short*)(0x8002D79A) = SCREEN_HD / 2; // Y Offset of music/sfx volume
    // Options
    *(short*)(0x8002DC7A) = SCREEN_WD * 2; // X Position of Options Text
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002DD0A) = *(short*)(&x); // Base X Position of Options Values
    y = (SCREEN_HD_FLOAT / 2) + 25.0f;
    *(short*)(0x8002DD0E) = *(short*)(&y); // Base Y Position of Options Values
    *(short*)(0x8002DF22) = SCREEN_HD - 30; //X Position of Options B Button
    *(short*)(0x8002DF56) = SCREEN_WD / 2; //X Position of Options Analog Stick
    *(short*)(0x8002DF5A) = (SCREEN_HD / 2) + 5; //Y Position of Options Analog Stick
    *(short*)(0x8002DF8A) = SCREEN_WD / 2; //X Position of Options Z Button
    *(short*)(0x8002DF8E) = SCREEN_HD - 40; //Y Position of Options Z Button
    // Mystery Menu
    *(short*)(0x8002E4B2) = SCREEN_WD * 2; //X Position of Mystery Text
    *(short*)(0x8002E576) = (SCREEN_WD * 2) + 40; //X Position of Mystery Menu Number
    x = SCREEN_WD_FLOAT / 2;
    *(int*)(0x8002E59C) = 0x3C050000 | *(short*)(&x); //X Position of Cheat Name
    *(short*)(0x8002E96E) = SCREEN_WD / 2; //X Position of Mystery Menu Analog Stick
    *(short*)(0x8002E9A2) = (SCREEN_WD / 2) - 40; //X Position of Mystery Menu Fairy
    *(short*)(0x8002E9D6) = SCREEN_WD - 35; //X Position of Mystery Menu Z Button
    *(short*)(0x8002EA0A) = SCREEN_WD - 35; //X Position of Mystery Menu A Button
    *(short*)(0x8002E93A) = SCREEN_HD - 30; //Y Position of Mystery Menu B Button
    *(short*)(0x8002E972) = SCREEN_HD / 2; //Y Position of Mystery Menu Analog Stick
    *(short*)(0x8002E9A6) = (SCREEN_HD / 2) - 0x28; //Y Position of Mystery Menu Fairy
    *(short*)(0x8002E9DA) = SCREEN_HD - 30; //Y Position of Mystery Menu Z Button
    *(short*)(0x8002EA0E) = SCREEN_HD - 30; //Y Position of Mystery Menu A Button
    // Multiplayer Kong Code
    x = SCREEN_WD_FLOAT / 2;
    *(short*)(0x8002CD72) = *(short*)(&x); //Base X Position of Players on Player Setup Screen

    float temp = SCREEN_WD_FLOAT * 2;
    *(short*)(0x800309A2) = *(short*)(&temp); //X Position of Final X Position of Buttons
    *(short*)(0x80030E0A) = (SCREEN_WD / 2) - 40; //Fix Clipping of Item Circle Entering Barrel
    *(short*)(0x80030E12) = (SCREEN_WD / 2) + 40; //Fix Clipping of Item Circle Leaving Barrel
    *(int*)(0x80030FC8) = 0x3C010000 | getHi(&pos_center_4x); //Load High Half of pos_center_4x
    *(int*)(0x80030FCC) = 0xD4200000 | getLo(&pos_center_4x); //Load pos_center_4x
    //
    temp = (SCREEN_WD_FLOAT*2)+320;
    *(short*)(0x80030F3E) = *(short*)(&temp); //Max X Position of Yes Orange
    temp = (SCREEN_WD_FLOAT*2)-320;
    *(short*)(0x80030F8A) = *(short*)(&temp); //Min X Position of No Orange
    temp = SCREEN_WD_FLOAT * 2;
    *(short*)(0x8003177A) = *(short*)(&temp); // X Position of Menu Options in Circle
    temp = SCREEN_WD_FLOAT / 2;
    *(short*)(0x80031386) = *(short*)(&temp); // X Position of File Icons
    *(short*)(0x800317EA) = *(short*)(&temp); // Base X Position of Text
    *(short*)(0x8003191A) = *(short*)(&temp); // Center X Position of Text
    *(short*)(0x80031DA6) = *(short*)(&temp); // X Position of Explosion
    *(short*)(0x80031E26) = *(short*)(&temp); // X Position of Barrel Shards
    temp = SCREEN_HD_FLOAT / 2;
    *(short*)(0x800313A6) = *(short*)(&temp); // Y Position of File Icons
    temp = 60.0f * (SCREEN_HD_FLOAT / 240.0f);
    *(short*)(0x800312D2) = *(short*)(&temp); // Turning Radius of File Icons
}

void loadWidescreen(overlays loaded_overlay) {
    if (Rando.true_widescreen) {
        if (loaded_overlay == OVERLAY_BOOT) {
            ws_static();
            ws_staticdata();
            ws_boot();
        } else if (loaded_overlay == OVERLAY_ARCADE) {
            ws_arcade();
        } else if (loaded_overlay == OVERLAY_JETPAC) {
            ws_jetpac();
        } else if (loaded_overlay == OVERLAY_MENU) {
            ws_menu();
        }
    }
}

/*
    maybe not needed
    .org 0x80000BD4
    lui a0, hi(NOEXP_CFB1_ADDR) //Address for Framebuffer 1 Cache Invalidation

    .org 0x80000CEC
    li v1, NOEXP_CFB1_ADDR+(SCREEN_WD*240*2) //End Address of First Framebuffer Clear for Loading
    lui v0, hi(NOEXP_CFB1_ADDR) //Start Address of First Framebuffer Clear for Loading

    .org 0x80000D74
    lui a0, hi(NOEXP_CFB1_ADDR) //Address of Framebuffer for No Expansion Pak Screen Text

    .org 0x80000B38
    li a0, NOEXP_CFB1_ADDR+(SCREEN_WD*240*2) //End Address of First Framebuffer for No Expansion Pak Screen

    .org 0x80000B44
    lui v0, hi(NOEXP_CFB1_ADDR) //Start Address of First Framebuffer for No Expansion Pak Screen

    .org 0x80000B74
    li a2, NOEXP_CFB1_ADDR+(SCREEN_WD*60*2) //Start Address of No Expansion Pak Image

    .org 0x80000BB4
    sh t2, (((SCREEN_WD/2)-33)*2)(v1) //Write Offset for No Expansion Pak Image

    *(int*)(0x8000ED10) = NOEXP_CFB1_ADDR; //Address of Framebuffer for No Expansion Pak Screen

    .org 0x80000EBC
    li a1, (SCREEN_WD*240*2) //Invalidation Size for Text Framebuffer


    .org 0x806FF7AC
    jal 0x806FF140 //Call Border Render Function
    addu a0, v0, r0 //Send GBI Pointer to Border Render Function
    j 0x806FFA24 //Skip Over Some Code
    addu s0, v0, r0 //Set Next GBI Address

    .org 0x8002D91C
    skip_widescreen_page:
    //Get Pointer to Options Instance
    lb a2, 0x17(a1) //Get Page of Options
    bnez a2, @@skip //Skip Over Code if Not on Options Page
    lui at, 0x8003 //Load Upper Half of Scroll Speed Address
    lw a3, 0x3F44(at) //Get Scroll Speed
    bnez a3, @@left //Assume Right Scroll if Non-Zero
    addiu t0, r0, 1 //Move to Story Skip Page
    j @@skip //Return to Game
    sb t0, 0x17(a0) //Set Options Page Number
    @@left:
    lb t0, 0x38FC(at) //Get Max Pages
    addiu t0, t0, -1 //Get Last Page
    sb t0, 0x17(a0) //Set Page Number
    @@skip:
    j 0x8002DB78 //Return to Game 
    lw a0, 0x30(sp) //Execute Replaced Instruction

    .org 0x8002DB70
    j 0x8002D91C //Jump to Code to Skip Screen Mode Page

    .org 0x8002DF00
    addiu t1, r0, 0x1 //Default Page Number of Options Menu
    sb t1, 0x17(a0) //Set Page Number of Options Menu

    .org 0x8002DF2C
    sw at, 0x10(sp) //Set Parameter 5 to func_80030894

    .org 0x8002FA28
    j fix_option_pos //Fix X Position of Options
    nop //Skip Load of Option X Position
*/

/*
    needs adjustment
    .org 0x806A2A18
    j fix_timer_pos //Fix Timer X Position

    .org 0x8074685C
        .area 0x1B0
        fix_nintendo_logo_pos:
        lui at, hi(((SCREEN_WD*96)+((SCREEN_WD/2)-96))*2) //Upper Half of Nintendo Logo Write Position
        j 0x805FB8B0 //Return to Game
        addiu at, at, lo(((SCREEN_WD*96)+((SCREEN_WD/2)-96))*2) //Lower Half of Nintendo Logo Write Position
        fix_timer_pos:
        andi t0, a0, 0x7FFF //Get Lower Half of Timer X Position
        slti at, t0, 0x78 //Check if Timer is on the Left
        bnez at, @@skip //Skip Realignment for Left Aligned Timers
        nop
        slti at, t0, 0xC8 //Check if TImer is on the Right
        bnez at, @@skip2 //Right Align Timer if On Right
        nop
        addiu a0, a0, (SCREEN_WD-320) //Move Timer to Right Edge
        j 0x806A2A20 //Return to Caller
        sw a0, 0x18(sp) //Execute Replaced Instruction
        @@skip2:
        addiu a0, a0, ((SCREEN_WD/2)-160) //Move Timer to Center
        @@skip:
        j 0x806A2A20 //Return to Caller
        sw a0, 0x18(sp) //Execute Replaced Instruction
        fix_option_pos:
        //Check for Options Menu Caller
        lw t6, 0x2C(sp)
        li at, 0x8002DCDC
        bne t6, at, @@skip //Skip if Caller isnt Options Menu
        nop
        bnez v1, @@skip //Check if Rendering Page 0
        nop
        addiu v1, r0, 1 //Render Page 1 Instead of Page 0
        @@skip:
        lui at, hi(pos_center) //Load High Half for Option Base Position
        j 0x8002FA30 //Return to Caller
        ldc1 f10, lo(pos_center)(at) //Load Option Base Position
        .align 8 //Align Double
        pos_center:
        .double (SCREEN_WD_FLOAT/2)
        pos_center_4x:
        .double (SCREEN_WD_FLOAT*2)
        fill_zipper_white:
        addiu a2, r0, 0 //Initialize i
        li a3, (SCREEN_WD*240) //Number of Pixels to Clear
        @@L1:
        addiu t0, r0, 0xFFFF //Pixel Clear Value
        sh t0, 0(a0) //Write Pixel
        addiu a2, a2, 1 //Increment Pixel Number
        sltu at, a2, a3 //Check for Last Pixel
        bnez at, @@L1 // Loop Until Last Pixel
        addiu a0, a0, 2 //Increment Pixel Pointer
        jr ra //Return to Game
        nop //Delay Slot
        .endarea

    .org 0x800293AC
    addiu a2, r0, (SCREEN_WD*2) //X Position of Percentage

    .org 0x800293FC
    addiu a2, r0, (SCREEN_WD*2) //X Position of Banana Count

    .org 0x80029454
    addiu a2, r0, (SCREEN_WD*2) //X Position of File Time

    .org 0x800294F0
    li.u at, ((SCREEN_WD_FLOAT/2)-75) //X Position of Clock Background

    .org 0x80029584
    li.u at, ((SCREEN_WD_FLOAT*2)-300) //X Position of Clock Hands


    .org 0x8002980C
    addiu a2, r0, (SCREEN_WD-30) //X Position of File Confirm A Button

    .org 0x8002986C
    addiu a2, r0, ((SCREEN_WD/2)-42) //X Position of File Confirm Banana

    
*/