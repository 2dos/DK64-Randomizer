"""Randomize Music passed from Misc options."""
import gzip
import random

import js
import math
from io import BytesIO
from zipfile import ZipFile
from randomizer.Enums.SongType import SongType
from randomizer.Lists.Songs import song_data
from randomizer.Patching.Patcher import ROM
from randomizer.Settings import Settings

storage_banks = {
    0: 0x8000,
    1: 0x11B6,
    2: 0x07B6,
    3: 0x0156,
}

class GroupData:
    """Class to store information regarding groups."""

    def __init__(self, name: str, setting: bool, files: list, names: list, extensions: list, song_type: SongType):
        self.name = name
        self.setting = setting
        self.files = files
        self.names = names
        self.extensions = extensions
        self.song_type = song_type

def doesSongLoop(data: bytes) -> bool:
    """Check if song loops."""
    byte_list = [x for xi, x in enumerate(data) if xi >= 0x44]  # Get byte list, exclude header
    for ps in range(len(byte_list) - 3):
        if byte_list[ps] == 0xFF and byte_list[ps + 1] == 0x2E and byte_list[ps + 2] == 0x00 and byte_list[ps + 3] == 0xFF:
            return True
    return False

def isValidSong(data: bytes, extension: str) -> bool:
    """Check if song is a valid bin."""
    if extension == ".candy":
        return True # TODO: Check from ZIP
    byte_list = [x for xi, x in enumerate(data) if xi < 4]
    return byte_list[0] == 0 and byte_list[1] == 0 and byte_list[2] == 0 and byte_list[3] == 0x44

class UploadInfo:
    """Class to store information regarding an uploaded song."""

    def __init__(self, push_array: list):
        """Initialize with given variables."""
        self.raw_input = push_array[0]
        self.name = push_array[1]
        self.extension = push_array[2]
        self.song_file = self.raw_input
        self.zip_file = None
        if self.extension == ".candy":
            self.zip_file = ZipFile(BytesIO(bytes(self.raw_input)))
            self.song_file = self.zip_file.open("song.bin").read()
        self.tags = []
        self.filter = self.extension == ".candy"
        self.acceptable = isValidSong(self.song_file, self.extension)

def insertUploaded(settings: Settings, uploaded_songs: list, uploaded_song_names: list, uploaded_song_extensions: list, target_type: SongType):
    """Insert uploaded songs into ROM."""
    # Initial Variables
    temp_push = [UploadInfo(x) for x in list(zip(uploaded_songs, uploaded_song_names, uploaded_song_extensions))]
    added_songs = [x for x in temp_push if x.acceptable]
    all_target_songs = [song for song in song_data if song.type == target_type]
    # Calculate Proportion, add songs if necessary
    proportion = settings.custom_music_proportion / 100
    if proportion < 0:
        proportion = 0
    elif proportion > 1:
        proportion = 1
    if settings.fill_with_custom_music:
        if len(added_songs) > 0 and len(all_target_songs) > 0:
            duplication_count = math.ceil((len(all_target_songs) * proportion) / len(added_songs))
            if duplication_count > 1: # Not enough songs to fill all slots
                initial_songs = added_songs.copy()
                for _ in range(duplication_count - 1):
                    added_songs.extend(initial_songs)
    # Shuffle
    random.shuffle(added_songs)
    swap_amount = len(added_songs)
    # Calculate Cap
    cap = int(len(all_target_songs) * proportion)
    if swap_amount > cap:
        swap_amount = cap
    # Place Songs
    songs_to_be_replaced = random.sample(all_target_songs, swap_amount)
    ROM_COPY = ROM()
    for index, song in enumerate(songs_to_be_replaced):
        selected_bank = None
        selected_cap = 0xFFFFFF
        new_song_data = bytes(added_songs[index].song_file)
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
            song_data[song_idx].output_name = added_songs[index].name
            entry_data = js.pointer_addresses[0]["entries"][song_idx]
            ROM_COPY.seek(entry_data["pointing_to"])
            zipped_data = gzip.compress(new_song_data, compresslevel=9)
            ROM_COPY.writeBytes(zipped_data)


ENABLE_CHAOS = False  # Enable DK Rap everywhere
TYPE_ARRAY = 0x1FEE200
TYPE_VALUES = [SongType.BGM, SongType.Event, SongType.MajorItem, SongType.MinorItem]

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
    ROM_COPY = ROM()

    NON_BGM_DATA = [
        # Minor Items
            GroupData("Minor Items", settings.music_minoritems_randomized, None, None, None, SongType.MinorItem),
            # Major Items
            GroupData("Major Items", settings.music_majoritems_randomized, None, None, None, SongType.MajorItem),
            # Events
            GroupData("Events", settings.music_events_randomized, None, None, None, SongType.Event),
    ]
    if js.cosmetics is not None and js.cosmetic_names is not None and js.cosmetic_extensions is not None:
        NON_BGM_DATA = [
            # Minor Items
            GroupData("Minor Items", settings.music_minoritems_randomized, js.cosmetics.minoritems, js.cosmetic_names.minoritems, js.cosmetic_extensions.minoritems, SongType.MinorItem),
            # Major Items
            GroupData("Major Items", settings.music_majoritems_randomized, js.cosmetics.majoritems, js.cosmetic_names.majoritems, js.cosmetic_extensions.majoritems, SongType.MajorItem),
            # Events
            GroupData("Events", settings.music_events_randomized, js.cosmetics.events, js.cosmetic_names.events, js.cosmetic_extensions.events, SongType.Event),
        ]


    if settings.music_bgm_randomized or settings.music_events_randomized or settings.music_majoritems_randomized or settings.music_minoritems_randomized:
        sav = settings.rom_data
        ROM_COPY.seek(sav + 0x12E)
        ROM_COPY.write(1)

    for index, song in enumerate(song_data):
        song.Reset()
        ROM_COPY.seek(TYPE_ARRAY + index)
        if song.type in TYPE_VALUES:
            ROM_COPY.write(TYPE_VALUES.index(song.type))
        else:
            ROM_COPY.write(255)
    # Check if we have anything beyond default set for BGM
    if settings.music_bgm_randomized:
        # If the user selected standard rando
        if not ENABLE_CHAOS:
            if js.cosmetics is not None and js.cosmetic_names is not None and js.cosmetic_extensions is not None:
                # If uploaded, replace some songs with the uploaded songs
                insertUploaded(settings, list(js.cosmetics.bgm), list(js.cosmetic_names.bgm), list(js.cosmetic_extensions.bgm), SongType.BGM)
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
            ROM_COPY.seek(rap["pointing_to"])
            stored_data = ROM_COPY.readBytes(rap["compressed_size"])
            uncompressed_data_table = js.pointer_addresses[26]["entries"][0]
            # Replace all songs as the DK rap
            for song in song_list:
                ROM_COPY.seek(song["pointing_to"])
                ROM_COPY.writeBytes(stored_data)
                # Update the uncompressed data table to have our new size.
                ROM_COPY.seek(uncompressed_data_table["pointing_to"] + (4 * song_list.index(song)))
                new_bytes = ROM_COPY.readBytes(4)
                ROM_COPY.seek(uncompressed_data_table["pointing_to"] + (4 * song_list.index(rap)))
                ROM_COPY.writeBytes(new_bytes)
                # Update data
                ROM_COPY.seek(0x1FFF000 + (song["index"] * 2))
                ROM_COPY.writeMultipleBytes(song_data[rap["index"]].memory, 2)

    for type_data in NON_BGM_DATA:
        if type_data.setting: # If the user wants to randomize the group
            if js.cosmetics is not None and js.cosmetic_names is not None and js.cosmetic_extensions is not None:
                # If uploaded, replace some songs with the uploaded songs
                insertUploaded(settings, list(type_data.files), list(type_data.names), list(type_data.extensions), type_data.song_type)
            # Load the list of items in that group
            group_items = []
            for song in song_data:
                if song.type == type_data.song_type:
                    group_items.append(js.pointer_addresses[0]["entries"][song_data.index(song)])
            # Shuffle the group list
            shuffled_music = group_items.copy()
            random.shuffle(shuffled_music)
            shuffle_music(music_data, group_items.copy(), shuffled_music)
    
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
    ROM_COPY = ROM()
    for song in pool_to_shuffle:
        ROM_COPY.seek(song["pointing_to"])
        stored_data = ROM_COPY.readBytes(song["compressed_size"])
        stored_song_data[song["index"]] = stored_data
        # Update the uncompressed data table to have our new size.
        ROM_COPY.seek(uncompressed_data_table["pointing_to"] + (4 * song["index"]))
        new_bytes = ROM_COPY.readBytes(4)
        stored_song_sizes[song["index"]] = new_bytes

    for song in pool_to_shuffle:
        shuffled_song = shuffled_list[pool_to_shuffle.index(song)]
        songs = stored_song_data[shuffled_song["index"]]
        ROM_COPY.seek(song["pointing_to"])
        ROM_COPY.writeBytes(songs)
        # Update the uncompressed data table to have our new size.
        song_size = stored_song_sizes[shuffled_song["index"]]
        ROM_COPY.seek(uncompressed_data_table["pointing_to"] + (4 * song["index"]))
        ROM_COPY.writeBytes(song_size)
        originalIndex = song["index"]
        shuffledIndex = shuffled_song["index"]
        memory = song_data[shuffledIndex].memory
        ROM_COPY.seek(0x1FFF000 + 2 * originalIndex)
        ROM_COPY.writeMultipleBytes(memory, 2)
        if song_data[originalIndex].type == SongType.BGM:
            music_data["music_bgm_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.MajorItem:
            music_data["music_majoritem_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.MinorItem:
            music_data["music_minoritem_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
        elif song_data[originalIndex].type == SongType.Event:
            music_data["music_event_data"][song_data[originalIndex].name] = song_data[shuffledIndex].output_name
