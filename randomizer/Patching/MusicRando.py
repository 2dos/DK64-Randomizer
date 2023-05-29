"""Randomize Music passed from Misc options."""
import gzip
import random

import js
import randomizer.Lists.Exceptions as Ex
from randomizer.Enums.SongType import SongType
from randomizer.Lists.Songs import Song, song_data
from randomizer.Patching.Patcher import ROM
from randomizer.Settings import Settings

storage_banks = {
    0: 0x8000,
    1: 0x11C0,
    2: 0x07C0,
    3: 0x0160,
}


def doesSongLoop(data: bytes) -> bool:
    """Check if song loops."""
    byte_list = [x for xi, x in enumerate(data) if xi >= 0x44]  # Get byte list, exclude header
    for ps in range(len(byte_list) - 3):
        if byte_list[ps] == 0xFF and byte_list[ps + 1] == 0x2E and byte_list[ps + 2] == 0x00 and byte_list[ps + 3] == 0xFF:
            return True
    return False


def insertUploaded(uploaded_songs: list, uploaded_song_names: list, target_type: SongType):
    """Insert uploaded songs into ROM."""
    added_songs = list(zip(uploaded_songs, uploaded_song_names))
    random.shuffle(added_songs)
    all_target_songs = [song for song in song_data if song.type == target_type]
    swap_amount = len(added_songs)
    if swap_amount > len(all_target_songs):
        swap_amount = len(all_target_songs)
    songs_to_be_replaced = random.sample(all_target_songs, swap_amount)
    for index, song in enumerate(songs_to_be_replaced):
        selected_bank = None
        selected_cap = 0xFFFFFF
        new_song_data = bytes(added_songs[index][0])
        for bank in storage_banks:
            if len(new_song_data) <= storage_banks[bank]:  # Song can fit in bank
                if selected_cap > storage_banks[bank]:  # Bank size is new lowest that fits
                    selected_bank = bank
                    selected_cap = storage_banks[bank]
        if selected_bank is not None:
            song_idx = song_data.index(song)
            old_bank = (song_data[song_idx].memory >> 1) & 3
            if old_bank < selected_bank:
                selected_bank = old_bank  # If vanilla bank is bigger, use the vanilla bank
            # Construct new memory data based on variables
            song_data[song_idx].memory &= 0xFEF9
            song_data[song_idx].memory |= (selected_bank & 3) << 1
            loop = doesSongLoop(new_song_data)
            loop_val = 0
            if loop:
                loop_val = 1
            song_data[song_idx].memory |= loop_val << 8
            # Write Song
            song_data[song_idx].output_name = added_songs[index][1]
            entry_data = js.pointer_addresses[0]["entries"][song_idx]
            ROM().seek(entry_data["pointing_to"])
            zipped_data = gzip.compress(new_song_data, compresslevel=9)
            ROM().writeBytes(zipped_data)


ENABLE_CHAOS = False  # Enable DK Rap everywhere


def randomize_music(settings: Settings):
    """Randomize music passed from the misc music settings.

    Args:
        settings (Settings): Settings object from the windows form.
    """
    music_data = {"music_bgm_data": {}, "music_majoritem_data": {}, "music_minoritem_data": {}, "music_event_data": {}}
    if js.document.getElementById("override_cosmetics").checked or True:
        if js.document.getElementById("random_music").checked:
            settings.music_bgm_randomized = True
            settings.music_majoritems_randomized = True
            settings.music_minoritems_randomized = True
            settings.music_events_randomized = True
        else:
            settings.music_bgm_randomized = js.document.getElementById("music_bgm_randomized").checked
            settings.music_majoritems_randomized = js.document.getElementById("music_majoritems_randomized").checked
            settings.music_majoritems_randomized = js.document.getElementById("music_majoritems_randomized").checked
            settings.music_minoritems_randomized = js.document.getElementById("music_minoritems_randomized").checked
            settings.music_events_randomized = js.document.getElementById("music_events_randomized").checked
    else:
        if settings.random_music:
            settings.music_bgm_randomized = True
            settings.music_majoritems_randomized = True
            settings.music_minoritems_randomized = True
            settings.music_events_randomized = True
    if settings.music_bgm_randomized or settings.music_events_randomized or settings.music_majoritems_randomized or settings.music_minoritems_randomized:
        sav = settings.rom_data
        ROM().seek(sav + 0x12E)
        ROM().write(1)
    for song in song_data:
        song.Reset()
    # Check if we have anything beyond default set for BGM
    if settings.music_bgm_randomized:
        # If the user selected standard rando
        if not ENABLE_CHAOS:
            if js.cosmetics is not None and js.cosmetic_names is not None:
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
            # ShuffleMusicWithSizeCheck(music_data, song_list)
            for channel_index in range(12):
                shuffled_music = song_list[channel_index].copy()
                random.shuffle(shuffled_music)
                shuffle_music(music_data, song_list[channel_index].copy(), shuffled_music)
        # If the user was a poor sap and selected chaos put DK rap for everything
        else:
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
    # If the user wants to randomize major items
    if settings.music_majoritems_randomized:
        if js.cosmetics is not None and js.cosmetic_names is not None:
            # If uploaded, replace some songs with the uploaded songs
            insertUploaded(list(js.cosmetics.majoritems), list(js.cosmetic_names.majoritems), SongType.MajorItem)
        # Load the list of majoritems
        majoritem_list = []
        for song in song_data:
            if song.type == SongType.MajorItem:
                majoritem_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])
        # Shuffle the majoritem list
        # ShuffleMusicWithSizeCheck(music_data, majoritem_list)
        shuffled_music = majoritem_list.copy()
        random.shuffle(shuffled_music)
        shuffle_music(music_data, majoritem_list.copy(), shuffled_music)
    # If the user wants to randomize minor items
    if settings.music_minoritems_randomized:
        if js.cosmetics is not None and js.cosmetic_names is not None:
            # If uploaded, replace some songs with the uploaded songs
            insertUploaded(list(js.cosmetics.minoritems), list(js.cosmetic_names.minoritems), SongType.MinorItem)
        # Load the list of minoritems
        minoritem_list = []
        for song in song_data:
            if song.type == SongType.MinorItem:
                minoritem_list.append(js.pointer_addresses[0]["entries"][song_data.index(song)])
        # Shuffle the minoritem list
        # ShuffleMusicWithSizeCheck(music_data, minoritem_list)
        shuffled_music = minoritem_list.copy()
        random.shuffle(shuffled_music)
        shuffle_music(music_data, minoritem_list.copy(), shuffled_music)

    # If the user wants to randomize events
    if settings.music_events_randomized:
        if js.cosmetics is not None and js.cosmetic_names is not None:
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
        shuffle_music(music_data, event_list.copy(), duped_song_list)
    return music_data


def shuffle_music(music_data, pool_to_shuffle, shuffled_list):
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
            music_data["music_bgm_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.MajorItem:
            music_data["music_majoritem_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.MinorItem:
            music_data["music_minoritem_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.Event:
            music_data["music_event_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
