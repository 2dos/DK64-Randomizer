"""Randomize Music passed from Misc options."""
import gzip
import json
import random
from ast import And

import js
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.Settings import MusicCosmetics
from randomizer.Enums.SongType import SongType
from randomizer.Lists.Songs import Song, SongGroup, song_data
from randomizer.Patching.Patcher import ROM
from randomizer.Settings import Settings
from randomizer.Spoiler import Spoiler


def insertUploaded(uploaded_songs: list, uploaded_song_names: list, target_type: SongType):
    """Insert uploaded songs into ROM."""
    added_songs = list(zip(uploaded_songs, uploaded_song_names))
    random.shuffle(added_songs)
    all_target_songs = [song for song in song_data if song.type == target_type]
    songs_to_be_replaced = random.sample(all_target_songs, len(added_songs))
    for index, song in enumerate(songs_to_be_replaced):
        song_idx = song_data.index(song)
        song_data[song_idx].output_name = added_songs[index][1]
        entry_data = js.pointer_addresses[0]["entries"][song_idx]
        ROM().seek(entry_data["pointing_to"])
        zipped_data = gzip.compress(bytes(added_songs[index][0]), compresslevel=9)
        ROM().writeBytes(zipped_data)


def randomize_music(spoiler: Spoiler):
    """Randomize music passed from the misc music settings.

    Args:
        settings (Settings): Settings object from the windows form.
    """
    settings: Settings = spoiler.settings
    if js.document.getElementById("override_cosmetics").checked:
        if js.document.getElementById("random_music").checked:
            spoiler.settings.music_bgm = MusicCosmetics.randomized
            spoiler.settings.music_fanfares = MusicCosmetics.randomized
            spoiler.settings.music_events = MusicCosmetics.randomized
        else:
            spoiler.settings.music_bgm = MusicCosmetics[js.document.getElementById("music_bgm").value]
            spoiler.settings.music_fanfares = MusicCosmetics[js.document.getElementById("music_fanfares").value]
            spoiler.settings.music_events = MusicCosmetics[js.document.getElementById("music_events").value]
    else:
        if spoiler.settings.random_music:
            spoiler.settings.music_bgm = MusicCosmetics.randomized
            spoiler.settings.music_fanfares = MusicCosmetics.randomized
            spoiler.settings.music_events = MusicCosmetics.randomized
    if spoiler.settings.music_bgm != MusicCosmetics.default or spoiler.settings.music_events != MusicCosmetics.default or spoiler.settings.music_fanfares != MusicCosmetics.default:
        sav = spoiler.settings.rom_data
        ROM().seek(sav + 0x12E)
        ROM().write(1)
    for song in song_data:
        song.Reset()
    # Check if we have anything beyond default set for BGM
    if spoiler.settings.music_bgm != MusicCosmetics.default:
        # If the user selected standard rando
        if spoiler.settings.music_bgm in (MusicCosmetics.randomized, MusicCosmetics.uploaded):
            if spoiler.settings.music_bgm == MusicCosmetics.uploaded and js.cosmetics is not None and js.cosmetic_names is not None:
                # If uploaded, replace some songs with the uploaded songs
                insertUploaded(list(js.cosmetics.bgm), list(js.cosmetic_names.bgm), SongType.BGM)
            # Generate the list of BGM songs
            song_list = []
            for channel_index in range(12):
                song_list.append([])
            for song in song_data:
                if song.type == SongType.BGM:
                    # For testing, flip these two lines
                    # song_list.append(pointer_addresses[0]["entries"][song_data.index(song)])
                    song_list[song.channel - 1].append(js.pointer_addresses[0]["entries"][song_data.index(song)])
            # ShuffleMusicWithSizeCheck(spoiler, song_list)
            for channel_index in range(12):
                shuffled_music = song_list[channel_index].copy()
                random.shuffle(shuffled_music)
                shuffle_music(spoiler, song_list[channel_index].copy(), shuffled_music)
        # If the user was a poor sap and selected chaos put DK rap for everything
        elif spoiler.settings.music_bgm == MusicCosmetics.chaos:
            # Find the DK rap in the list
            rap = js.pointer_addresses[0]["entries"][song_data.index(next((x for x in song_data if x.name == "DK Rap"), None))]
            # Find all BGM songs
            song_list = []
            for song in song_data:
                if song.type == SongType.BGM:
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Load the DK Rap song data
            ROM().seek(rap["pointing_to"])
            stored_data = ROM().readBytes(rap["compressed_size"])
            uncompressed_data_table = js.pointer_addresses[26]["entries"][0]
            # Replace all songs as the DK rap
            for song in song_list:
                ROM().seek(song["pointing_to"])
                ROM().writeBytes(stored_data)
                # Update the uncompressed data table to have our new size.
                ROM().seek(uncompressed_data_table["pointing_to"] + (4 * song_list.index(song)))
                new_bytes = ROM().readBytes(4)
                ROM().seek(uncompressed_data_table["pointing_to"] + (4 * song_list.index(rap)))
                ROM().writeBytes(new_bytes)
                # Update data
                ROM().seek(0x1FFF000 + (song["index"] * 2))
                ROM().writeMultipleBytes(song_data[rap["index"]].memory, 2)
    # If the user wants to randomize fanfares
    if spoiler.settings.music_fanfares != MusicCosmetics.default:
        # Check if our setting is just rando
        if spoiler.settings.music_fanfares in (MusicCosmetics.randomized, MusicCosmetics.uploaded):
            if spoiler.settings.music_fanfares == MusicCosmetics.uploaded and js.cosmetics is not None and js.cosmetic_names is not None:
                # If uploaded, replace some songs with the uploaded songs
                insertUploaded(list(js.cosmetics.fanfares), list(js.cosmetic_names.fanfares), SongType.Fanfare)
            # Load the list of fanfares
            fanfare_list = []
            for song in song_data:
                if song.type == SongType.Fanfare:
                    fanfare_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])
            # Shuffle the fanfare list
            # ShuffleMusicWithSizeCheck(spoiler, fanfare_list)
            shuffled_music = fanfare_list.copy()
            random.shuffle(shuffled_music)
            shuffle_music(spoiler, fanfare_list.copy(), shuffled_music)

    # If the user wants to randomize events
    if spoiler.settings.music_events != MusicCosmetics.default:
        # Check if our setting is just rando
        if spoiler.settings.music_events in (MusicCosmetics.randomized, MusicCosmetics.uploaded):
            if spoiler.settings.music_events == MusicCosmetics.uploaded and js.cosmetics is not None and js.cosmetic_names is not None:
                # If uploaded, replace some songs with the uploaded songs
                insertUploaded(list(js.cosmetics.events), list(js.cosmetic_names.events), SongType.Event)
            # Load the list of events
            event_list = []
            for song in song_data:
                if song.type == SongType.Event:
                    event_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Shuffle the event list
            duped_song_list = event_list.copy()
            random.shuffle(duped_song_list)
            shuffle_music(spoiler, event_list.copy(), duped_song_list)


def shuffle_music(spoiler: Spoiler, pool_to_shuffle, shuffled_list):
    """Shuffle the music pool based on the OG list and the shuffled list.

    Args:
        pool_to_shuffle (list): Original pool to shuffle.
        shuffled_list (list): Shuffled order list.
    """
    uncompressed_data_table = js.pointer_addresses[26]["entries"][0]
    stored_song_data = {}
    stored_song_sizes = {}
    # For each song in the shuffled list, randomize it into the pool using the shuffled list as a base
    # First loop over all songs to read data from ROM
    for song in pool_to_shuffle:
        ROM().seek(song["pointing_to"])
        stored_data = ROM().readBytes(song["compressed_size"])
        stored_song_data[song["index"]] = stored_data
        # Update the uncompressed data table to have our new size.
        ROM().seek(uncompressed_data_table["pointing_to"] + (4 * song["index"]))
        new_bytes = ROM().readBytes(4)
        stored_song_sizes[song["index"]] = new_bytes

    # Second loop over all songs to write data into ROM
    # test0 = []
    # test1 = []
    # for x in range(len(pool_to_shuffle)):
    #     test0.append({
    #         "vanilla": pool_to_shuffle[x]["index"],
    #         "shuffled": shuffled_list[x]["index"]
    #     })
    # print(test0)

    for song in pool_to_shuffle:
        shuffled_song = shuffled_list[pool_to_shuffle.index(song)]
        songs = stored_song_data[shuffled_song["index"]]
        ROM().seek(song["pointing_to"])
        ROM().writeBytes(songs)
        # Update the uncompressed data table to have our new size.
        song_size = stored_song_sizes[shuffled_song["index"]]
        ROM().seek(uncompressed_data_table["pointing_to"] + (4 * song["index"]))
        ROM().writeBytes(song_size)
        originalIndex = song["index"]
        shuffledIndex = shuffled_song["index"]
        memory = song_data[shuffledIndex].memory
        ROM().seek(0x1FFF000 + 2 * originalIndex)
        ROM().writeMultipleBytes(memory, 2)
        if song_data[originalIndex].type == SongType.BGM:
            spoiler.music_bgm_data[song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.Fanfare:
            spoiler.music_fanfare_data[song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.Event:
            spoiler.music_event_data[song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        # print(f"Vanilla Index {originalIndex}: Song {shuffledIndex}")
