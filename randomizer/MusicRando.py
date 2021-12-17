"""Randomize Music passed from Misc options."""
import json
import random

import js
from pyodide import to_js

from randomizer.Enums.SongType import SongType
from randomizer.Patcher import ROM
from randomizer.Settings import Settings
from randomizer.Songs import song_data


def randomize_music(settings: Settings):
    """Randomize music passed from the misc music settings.

    Args:
        settings (Settings): Settings object from the windows form.
    """
    # Check if we have anything beyond default set for BGM
    if settings.music_bgm != "default":
        # If the user selected standard rando
        if settings.music_bgm == "randomized":
            # Generate the list of BGM songs
            song_list = []
            for song in song_data:
                if song.type == SongType.BGM:
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Copy the existing list of songs and shuffle it
            shuffled_music = song_list.copy()
            random.shuffle(shuffled_music)

            # For each song in the shuffled list, randomize it into the pool using the shuffled list as a base
            for song in shuffled_music:
                ROM().seek(song["pointing_to"])
                stored_data = ROM().readBytes(song["compressed_size"])
                ROM().seek(song_list[shuffled_music.index(song)]["pointing_to"])
                ROM().writeBytes(stored_data)
        # If the user was a poor sap and selected chaos put DK rap for everything
        elif settings.music_bgm == "chaos":
            # Find the DK rap in the list
            rap = js.pointer_addresses[0]["entries"][
                song_data.index(next((x for x in song_data if x.name == "DK Rap"), None))
            ]
            # Find all BGM songs
            song_list = []
            for song in song_data:
                if song.type == SongType.BGM:
                    song_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])

            # Load the DK Rap song data
            ROM().seek(rap["pointing_to"])
            stored_data = ROM().readBytes(rap["compressed_size"])

            # Replace all songs as the DK rap
            for song in song_list:
                ROM().seek(song["pointing_to"])
                ROM().writeBytes(stored_data)
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

            # Replace all the fanfare songs with our new order
            for song in shuffled_music:
                ROM().seek(song["pointing_to"])
                stored_data = ROM().readBytes(song["compressed_size"])
                ROM().seek(fanfare_list[shuffled_music.index(song)]["pointing_to"])
                ROM().writeBytes(stored_data)
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

            # Replace all the event songs with our new order
            for song in shuffled_music:
                ROM().seek(song["pointing_to"])
                stored_data = ROM().readBytes(song["compressed_size"])
                ROM().seek(event_list[shuffled_music.index(song)]["pointing_to"])
                ROM().writeBytes(stored_data)
