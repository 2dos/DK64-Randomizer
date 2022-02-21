"""Randomize Music passed from Misc options."""
import gzip
import json
import random

import js
from randomizer.Spoiler import Spoiler
from randomizer.Enums.SongType import SongType
from randomizer.Lists.Songs import Song, song_data
from randomizer.Patcher import ROM
from randomizer.Settings import Settings


def randomize_music(spoiler:Spoiler):
    """Randomize music passed from the misc music settings.

    Args:
        settings (Settings): Settings object from the windows form.
    """
    settings:Settings = spoiler.settings
    # Check if we have anything beyond default set for BGM
    if settings.music_bgm != "default":
        # If the user selected standard rando
        if settings.music_bgm == "randomized":
            
            # These lines exist for testing only
            # file = open('static/patches/pointer_addresses.json')
            # pointer_addresses = json.load(file)

            # Generate the list of BGM songs
            song_list = []
            for song in song_data:
                if song.type == SongType.BGM:
                    # For testing, flip these two lines
                    # song_list.append(pointer_addresses[0]["entries"][song_data.index(song)])
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Copy the existing list of songs and shuffle it
            shuffled_music = song_list.copy()
            random.shuffle(shuffled_music)
            # For testing, comment out shuffle_music
            shuffle_music(song_list, shuffled_music)
            for i, song_item in enumerate(song_list):
                shuffled_song_item = shuffled_music[i]
                vanillaSong:Song = song_data[song_item["index"]]
                newSong:Song = song_data[shuffled_song_item["index"]]
                spoiler.music_bgm_data[vanillaSong.name] = newSong.name

        # If the user was a poor sap and selected chaos put DK rap for everything
        elif settings.music_bgm == "chaos":
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
        elif settings.music_bgm == "uploaded":
            # Generate the list of BGM songs
            song_list = []
            for song in song_data:
                if song.type == SongType.BGM:
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Load our BGM data and just shuffle it around
            added_bgm = list(js.cosmetics.bgm)
            random.shuffle(added_bgm)

            already_modified = []
            for item in added_bgm:

                def check_song():
                    random_song = random.choice(song_list)
                    # Exit loop for recursion
                    if len(already_modified) >= len(song_list):
                        return
                    if random_song not in already_modified:
                        ROM().seek(random_song["pointing_to"])
                        ROM().writeBytes(gzip.compress(bytes(item), compresslevel=9))
                        already_modified.append(random_song)
                    else:
                        check_song()

                check_song()
            duped_song_list = song_list.copy()
            random.shuffle(duped_song_list)
            shuffle_music(song_list, duped_song_list)
    # If the user wants to randomize fanfares
    if settings.music_fanfares != "default":
        # Check if our setting is just rando
        if settings.music_fanfares == "randomized":
            # Load the list of fanfares
            fanfare_list = []
            for song in song_data:
                if song.type == SongType.Fanfare:
                    fanfare_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Shuffle the fanfare list
            shuffled_music = fanfare_list.copy()
            random.shuffle(shuffled_music)
            shuffle_music(fanfare_list, shuffled_music)
        elif settings.music_fanfares == "uploaded":
            # Generate the list of fanfares songs
            song_list = []
            for song in song_data:
                if song.type == SongType.Fanfare:
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Load our fanfares data and just shuffle it around
            added_fanfares = list(js.cosmetics.fanfares)
            random.shuffle(added_fanfares)

            already_modified = []
            for item in added_fanfares:

                def check_song():
                    random_song = random.choice(song_list)
                    # Exit loop for recursion
                    if len(already_modified) >= len(song_list):
                        return
                    if random_song not in already_modified:
                        ROM().seek(random_song["pointing_to"])
                        ROM().writeBytes(gzip.compress(bytes(item), compresslevel=9))
                        already_modified.append(random_song)
                    else:
                        check_song()

                check_song()
            duped_song_list = song_list.copy()
            random.shuffle(duped_song_list)
            shuffle_music(song_list, duped_song_list)

    # If the user wants to randomize events
    if settings.music_events != "default":
        # Check if our setting is just rando
        if settings.music_events == "randomized":
            # Load the list of events
            event_list = []
            for song in song_data:
                if song.type == SongType.Event:
                    event_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Shuffle the event list
            shuffled_music = event_list.copy()
            random.shuffle(shuffled_music)

            shuffle_music(event_list, shuffled_music)


def shuffle_music(pool_to_shuffle, shuffled_list):
    """Shuffle the music pool based on the OG list and the shuffled list.

    Args:
        pool_to_shuffle (list): Original pool to shuffle.
        shuffled_list (list): Shuffled order list.
    """
    uncompressed_data_table = js.pointer_addresses[26]["entries"][0]
    # For each song in the shuffled list, randomize it into the pool using the shuffled list as a base
    for song in pool_to_shuffle:
        ROM().seek(song["pointing_to"])
        stored_data = ROM().readBytes(song["compressed_size"])
        ROM().seek(shuffled_list[pool_to_shuffle.index(song)]["pointing_to"])
        ROM().writeBytes(stored_data)
        # Update the uncompressed data table to have our new size.
        ROM().seek(uncompressed_data_table["pointing_to"] + (4 * shuffled_list.index(song)))
        new_bytes = ROM().readBytes(4)
        ROM().seek(uncompressed_data_table["pointing_to"] + (4 * pool_to_shuffle.index(song)))
        ROM().writeBytes(new_bytes)
