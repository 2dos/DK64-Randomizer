/**
 * @file music_text.c
 * @author Ballaam
 * @brief Display the name of a song on the bottom of the screen when played
 * @version 0.1
 * @date 2024-03-25
 * 
 * @copyright Copyright (c) 2024
 * 
 */

#include "../../include/common.h"

static unsigned char display_timer = 0;
static short displayed_text_offset = -1;
static short storedMusicTrackChannel[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
static char storedTrackState[12] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};

void resetDisplayedMusic(void) {
    DisplayedSongNamePointer = 0; // Uses a static address for autotrackers
}


void detectSongChange(){
    char loadedSongCanceled = 0;
    for(int i = 11; i >= 0; i--){
        if(storedMusicTrackChannel[i] != MusicTrackChannels[i]){
            // New song was requested to play on this channel
            initSongDisplay(MusicTrackChannels[i]);
            if(MusicTrackChannels[i] == 0 && music_types[storedMusicTrackChannel[i]] == SONGTYPE_BGM){
                loadedSongCanceled = 1;
            }
            storedMusicTrackChannel[i] = MusicTrackChannels[i];
        } else if(loadedSongCanceled){
            // An already playing BGM got canceled. This song might have been blocking songs on lower channels from playing
            // So next song in line that is a BGM will be played.
            if(music_types[MusicTrackChannels[i]] == SONGTYPE_BGM){
                initSongDisplay(MusicTrackChannels[i]);
                // And ignore songs in lower channels. The BGM filter should be enough to make it accurate
                loadedSongCanceled = 0;
            }
        }
        if(trackStateArray[i] != storedTrackState[i]){
            if(trackStateArray[i] == 2 && storedTrackState[i] == 1){
                // New song has loaded in and has now started
                // This call is so close to being obsolete, but it covers edge cases where
                // you enter a level in a location where one BGM has priority over another (Aztec/Galleon tunnel spawn)
                initSongDisplay(MusicTrackChannels[i]);
            }
            storedTrackState[i] = trackStateArray[i];
        }
    }
}

void initSongDisplay(int song) {
    if (song == 0) {
        return;
    }
    if (music_types[song] != SONGTYPE_BGM) {
        return;
    }
    if ((CurrentMap == MAP_ISLES) && (CutsceneActive == 1) && (CutsceneIndex == 29)) {
        // In K Rool gets launched cutscene
        return;
    }
    if (DisplayedSongNamePointer) {
        complex_free(DisplayedSongNamePointer);
    }
    DisplayedSongNamePointer = getTextPointer(46, song, 0);
    displayed_text_offset = -1;
    int text_length = cstring_strlen(DisplayedSongNamePointer);
    display_timer = 60;
    if (ObjectModel2Timer < 31) {
        display_timer += 31;
    }
    for (int i = 0; i < text_length; i++) {
        if (DisplayedSongNamePointer[i] == 0xA) {
            DisplayedSongNamePointer[i] = 0;
            displayed_text_offset = i + 1;
        }
    }
}

Gfx* displaySongNameHandler(Gfx* dl) {
    if ((!Rando.show_music_name) || (display_timer == 0)) {
        return dl;
    }
    if (display_timer > 0) {
        display_timer -= 1;
    }
    if (!DisplayedSongNamePointer) {
        return dl;
    }
    if (displayed_text_offset == -1) {
        return dl;
    }
    for (int i = 0; i < 2; i++) {
        mtx_item mtx0;
        mtx_item mtx1;
        _guScaleF(&mtx0, 0x3F19999A, 0x3F19999A, 0x3F800000);
        _guTranslateF(&mtx1, 50.0f, 800.0f + (i * 30.0f), 0.0f);
        _guMtxCatF(&mtx0, &mtx1, &mtx0);
        _guTranslateF(&mtx1, 0.0f, 48.0f, 0.0f);
        _guMtxCatF(&mtx0, &mtx1, &mtx0);
        _guMtxF2L(&mtx0, &static_mtx[20 + i]);

        gSPDisplayList(dl++, 0x01000118);
        gSPMatrix(dl++, 0x02000180, G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
        gDPPipeSync(dl++);
        gDPSetCombineLERP(dl++, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0, 0, 0, 0, TEXEL0, TEXEL0, 0, PRIMITIVE, 0);
        gDPSetPrimColor(dl++, 0, 0, 0xFF, 0xFF, 0xFF, 0xFF);
        gSPMatrix(dl++, (int)&static_mtx[20 + i], G_MTX_PUSH | G_MTX_LOAD | G_MTX_MODELVIEW);
        dl = displayText(dl,6,0,0,DisplayedSongNamePointer + (displayed_text_offset * i),0);
        gSPPopMatrix(dl++, G_MTX_MODELVIEW);
    }
    return dl;
}