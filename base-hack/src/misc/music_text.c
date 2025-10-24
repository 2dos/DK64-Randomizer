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

void detectSongChange(void) {
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

// 480k (default) / 1.5
#define SPEED_UP_TEMPO 320000

void SpeedUpMusic(void) {
    if (!Rando.song_speed_near_win) {
        return;
    }
    if (!isGamemode(GAMEMODE_ADVENTURE, 1)) {
        return;
    }
    win_conditions win_con = Rando.win_condition;
    if (win_con == GOAL_KROOLS_CHALLENGE) {
        if (!canAccessKroolsChallenge()) {
            return;
        }
    } else {
        requirement_item win_con_item = Rando.win_condition_extra.item;
        int win_con_count = Rando.win_condition_extra.count;
        // Checking items
        if (win_con == GOAL_KROOL) {
            win_con_item = REQITEM_KEY;
            win_con_count = 9; // Triggers upon picking up the 8th key
        } else if (win_con != GOAL_CUSTOMITEM) {
            // Goal is ineligible for speed up
            return;
        }
        if (win_con_count < 2) {
            // Doesn't work for 1-item win conditions
            return;
        }
        int item_count = getItemCountReq(win_con_item);
        if (item_count != (win_con_count - 1)) {
            return;
        }
    }
    for (int i = 0; i < 4; i++) {
        songs song = SongInWriteSlot[i];
        if ((music_types[song] == SONGTYPE_BGM) && (song != SONG_BABOONBALLOON)) {
            int existing_tempo = getSongTempo(compactSequencePlayers[i]);
            float current_inverse_division = compactSequencePlayers[i]->target->qnpt;
            float target_inverse_division = (1.0f / musicStorage[i]->division / 1.5f);
            if (current_inverse_division != target_inverse_division) {
                compactSequencePlayers[i]->target->qnpt = target_inverse_division;
                alCSPSetTempo(compactSequencePlayers[i], existing_tempo);
            }
        }
    }
}

void initSongDisplay(int song) {
    if (song == SONG_SILENCE) {
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
        _guTranslateF(&mtx1, 80.0f, 800.0f + (i * 30.0f), 0.0f);
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

void fixBrokenVoices(ALSeqPlayer* seq_p) {
    if(SongInWriteSlot[2] != 0x2B || MusicTrackChannels[8] == 0x12){
        seq_p->state = 1;
        return;
    }
    PVoice* pVoice = (PVoice*) 0x8076D714;
    int* samples = *(int*) 0x8076D724;
    int delta = * samples;
    while(pVoice != 0){
        // if stop voice update didn't come through
        if (pVoice->debug1 == 0x01){
            if(postSynUpdate(pVoice, (pVoice->delay + samples), 0xF) == 1){
                pVoice->debug1 = 0;
            }
        }
        // if stop voice update came through, but free voice update didn't come through
        if (pVoice->debug1 == 0 && pVoice->debug2 == 0x02){
            if(postSynUpdate(pVoice, (pVoice->delay + samples), 0) == 1){
                pVoice->debug1 = 0;
                pVoice->debug2 = 0;
            }
        }
        pVoice = (PVoice*) (int*) pVoice->node.next;
    }

    // finally set the sequence player's state to 1 (playing), which is the code that this function overwrites
    seq_p->state = 1;
}

char postSynUpdate(PVoice* pVoice, int delta, short type){
    if(pVoice){
        ALParam* param = getNextFreeSynthUpdate();
        if(param != 0){
            param->delta = delta;
            param->updateType = type;
            param->pitch = (int*) pVoice;
            SetParam(pVoice, 3, param);
            return 1;
        }
    }
    return 0;
}