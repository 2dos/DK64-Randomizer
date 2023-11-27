"""Randomize Music passed from Misc options."""
import gzip
import random

import js
import json
from io import BytesIO
from zipfile import ZipFile
from randomizer.Enums.Songs import Songs
from randomizer.Enums.SongType import SongType
from randomizer.Enums.SongGroups import SongGroup
from randomizer.Lists.Songs import song_data, song_idx_list
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
        """Initialize with given parameters."""
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
        return True  # TODO: Check from ZIP
    if len(data) < 0x44:
        return False
    byte_list = [x for xi, x in enumerate(data) if xi < 4]
    return byte_list[0] == 0 and byte_list[1] == 0 and byte_list[2] == 0 and byte_list[3] == 0x44


def getAllAssignedVanillaSongs(settings: Settings):
    """Return a dictionary of user-assigned vanilla songs."""
    return settings.music_selection_dict["vanilla"] if settings.song_select_enabled else {}


def getAllAssignedCustomSongs(settings: Settings):
    """Return a dictionary of user-assigned custom songs."""
    return settings.music_selection_dict["custom"] if settings.song_select_enabled else {}


def getVanillaSongAssignedToLocation(settings: Settings, location: Songs):
    """Return the vanilla song assigned to the given location."""
    assigned_vanilla_songs = getAllAssignedVanillaSongs(settings)
    loc_str = str(location.value)
    if loc_str in assigned_vanilla_songs:
        return assigned_vanilla_songs[loc_str]
    else:
        return None


def getCustomSongAssignedToLocation(settings: Settings, location: Songs):
    """Return the custom song assigned to the given location."""
    assigned_custom_songs = getAllAssignedCustomSongs(settings)
    loc_str = str(location.value)
    if loc_str in assigned_custom_songs:
        return assigned_custom_songs[loc_str]
    else:
        return None


TAG_CONVERSION_TABLE = {
    # Arg0 = group, Arg1 = is location
    "Gloomy": [SongGroup.Gloomy, False],
    "Lobbies and Shops": [SongGroup.LobbyShop, True],
    "Minigames": [SongGroup.Minigames, True],
    "Spawning": [SongGroup.Spawning, True],
    "Fights": [SongGroup.Fight, True],
    "Happy": [SongGroup.Happy, False],
    "Collection": [SongGroup.Collection, True],
    "Calm": [SongGroup.Calm, False],
    "Interiors": [SongGroup.Interiors, True],
    "Exteriors": [SongGroup.Exteriors, True],
}


class UploadInfo:
    """Class to store information regarding an uploaded song."""

    def __init__(self, push_array: list):
        """Initialize with given variables."""
        self.raw_input = push_array[0]
        self.name = push_array[1]
        self.extension = push_array[2]
        self.song_file = self.raw_input
        self.zip_file = None
        self.song_length = 0
        self.referenced_index = None
        self.location_tags = []
        self.mood_tags = []
        if self.extension == ".candy":
            self.zip_file = ZipFile(BytesIO(bytes(self.raw_input)))
            self.song_file = self.zip_file.open("song.bin").read()
            data_json = json.loads(self.zip_file.open("data.json").read())
            needed_keys = ["game", "song", "converter", "length", "tags"]
            enable_json_data = True
            for key in needed_keys:
                if key not in list(data_json.keys()):
                    enable_json_data = False
            if enable_json_data:
                self.name = f"{data_json['game']} \"{data_json['song']}\" converted by {data_json['converter']}"
                self.song_length = data_json["length"]
                for tag in data_json["tags"]:
                    if tag in list(TAG_CONVERSION_TABLE.keys()):
                        if TAG_CONVERSION_TABLE[tag][1]:
                            # Location Tag
                            self.location_tags.append(TAG_CONVERSION_TABLE[tag][0])
                        else:
                            # Mood Tag
                            self.mood_tags.append(TAG_CONVERSION_TABLE[tag][0])
        if len(self.location_tags) == 0:
            self.location_tags = [
                SongGroup.Fight,
                SongGroup.LobbyShop,
                SongGroup.Interiors,
                SongGroup.Exteriors,
                SongGroup.Minigames,
                SongGroup.Spawning,
                SongGroup.Collection,
            ]
        self.filter = self.extension == ".candy"
        self.acceptable = isValidSong(self.song_file, self.extension)
        self.used = False


UNPLACED_SONGS = {}
MAX_LENGTH_DIFFERENCE = 0.4
MAX_LENGTH_OFFSET = 3
GLOBAL_SEARCH_INDEX = 0
USED_INDEXES = []


def pushSongToUnplaced(song: UploadInfo, ref_index: int):
    """Pushes song to unplaced song to the UNPLACED_SONGS dictionary."""
    global UNPLACED_SONGS

    song.referenced_index = ref_index
    for tag in song.location_tags:
        if tag not in list(UNPLACED_SONGS.keys()):
            UNPLACED_SONGS[tag] = []
        UNPLACED_SONGS[tag].append(song)


def isSongWithInLengthRange(vanilla_length: int, proposed_length: int) -> bool:
    """Determine whether song is within range of the vanilla length."""
    if vanilla_length == 0 or proposed_length == 0:
        return True
    min_value = vanilla_length * (1 - MAX_LENGTH_DIFFERENCE)
    max_value = ((1 + MAX_LENGTH_DIFFERENCE) * (vanilla_length + MAX_LENGTH_OFFSET)) - MAX_LENGTH_OFFSET
    if proposed_length > min_value and proposed_length < max_value:
        return True
    return False


def getAssignedCustomSong(file_data_array: list, song_name: str) -> UploadInfo:
    """Request a specific custom song from the list."""
    global USED_INDEXES

    MAX_SEARCH_LENGTH = len(file_data_array)
    # Because all of the user-assigned custom songs get moved to the back of
    # the list, it's faster to search through the list backwards.
    for i in reversed(range(MAX_SEARCH_LENGTH)):
        item = file_data_array[i]
        if song_name == item[1]:
            USED_INDEXES.append(i)
            return UploadInfo(item)
    # The requested song was not found. (This should never happen due to client-side
    # validation.)
    raise ValueError(f'Requested non-existent custom song "{song_name}".')


def requestNewSong(file_data_array: list, location_tags: list, location_length: int, song_type: SongType, check_unused: bool) -> UploadInfo:
    """Request new song from list."""
    global GLOBAL_SEARCH_INDEX, USED_INDEXES, UNPLACED_SONGS

    # First, filter through the unplaced songs dictionary and remove any used songs
    for tag in UNPLACED_SONGS:
        UNPLACED_SONGS[tag] = [x for x in UNPLACED_SONGS[tag] if not x.used]
    check_tag = song_type == SongType.BGM
    # Next, check songs that have already been gone through.
    # If one of them satisfies the conditions, then we can just use that one and pop it from the list
    if check_tag:
        # Tag-Based Search
        loc_tag_copy = location_tags.copy()
        random.shuffle(loc_tag_copy)
        for tag in loc_tag_copy:
            if tag in list(UNPLACED_SONGS.keys()):
                if len(UNPLACED_SONGS[tag]) > 0:
                    found_song = UNPLACED_SONGS[tag].pop(0)
                    found_song.used = check_unused
                    USED_INDEXES.append(found_song.referenced_index)
                    return found_song
    else:
        # Length-Based Search
        for tag in UNPLACED_SONGS:
            songs_in_tag = UNPLACED_SONGS[tag]
            if len(songs_in_tag) > 0:
                for si, song in enumerate(songs_in_tag):
                    if isSongWithInLengthRange(location_length, song.song_length):
                        found_song = UNPLACED_SONGS[tag].pop(si)
                        found_song.used = check_unused
                        USED_INDEXES.append(found_song.referenced_index)
                        return found_song
    # Otherwise, go through the list of ones we're yet to go through
    MAX_SEARCH_LENGTH = len(file_data_array)
    start_index = GLOBAL_SEARCH_INDEX
    for i in range(MAX_SEARCH_LENGTH):
        GLOBAL_SEARCH_INDEX = (start_index + i) % MAX_SEARCH_LENGTH
        referenced_index = GLOBAL_SEARCH_INDEX
        item = UploadInfo(file_data_array[GLOBAL_SEARCH_INDEX])
        GLOBAL_SEARCH_INDEX = (start_index + i + 1) % MAX_SEARCH_LENGTH  # Advance 1 just in case we return from this
        if referenced_index in USED_INDEXES and check_unused:
            continue
        if not item.filter:
            if item.acceptable:
                USED_INDEXES.append(referenced_index)
                return item
        elif not check_tag:
            if isSongWithInLengthRange(location_length, item.song_length):
                USED_INDEXES.append(referenced_index)
                return item
            # Not similar enough, push to dictionary
            pushSongToUnplaced(item, referenced_index)
        else:
            loc_set = set(location_tags)
            song_set = set(item.location_tags)
            if loc_set & song_set:  # Has a tag in common
                USED_INDEXES.append(referenced_index)
                return item
            # No matches, push to dictionary
            pushSongToUnplaced(item, referenced_index)
    return None


def insertUploaded(settings: Settings, uploaded_songs: list, uploaded_song_names: list, uploaded_song_extensions: list, target_type: SongType):
    """Insert uploaded songs into ROM."""
    global UNPLACED_SONGS, GLOBAL_SEARCH_INDEX, USED_INDEXES

    # Initial Global Variables
    UNPLACED_SONGS = {}
    GLOBAL_SEARCH_INDEX = 0
    USED_INDEXES = []
    file_data = list(zip(uploaded_songs, uploaded_song_names, uploaded_song_extensions))
    random.shuffle(file_data)
    # Initial temporary variables
    all_target_songs = [song_enum for song_enum, song in song_data.items() if song.type == target_type]

    # Calculate Proportion, add songs if necessary
    proportion = settings.custom_music_proportion / 100
    if proportion < 0:
        proportion = 0
    elif proportion > 1:
        proportion = 1
    swap_amount = len(file_data)
    # Calculate Cap
    cap = int(len(all_target_songs) * proportion)
    if settings.fill_with_custom_music:
        swap_amount = cap
    if swap_amount > cap:
        swap_amount = cap

    # Process user-selected songs
    custom_song_locations = []
    custom_song_names = set()
    vanilla_song_locations = []
    for song_loc_enum, song_name in getAllAssignedVanillaSongs(settings).items():
        song_location = Songs(int(song_loc_enum))
        if song_location not in all_target_songs:
            continue
        vanilla_song_locations.append(song_location)
    for song_loc_enum, song_name in getAllAssignedCustomSongs(settings).items():
        song_location = Songs(int(song_loc_enum))
        if song_location not in all_target_songs:
            continue
        custom_song_locations.append(song_location)
        custom_song_names.add(song_name)
    # Remove all assigned locations from the target songs, if any.
    available_target_songs = [x for x in all_target_songs if x not in custom_song_locations and x not in vanilla_song_locations]
    swap_amount -= len(custom_song_locations)

    # Move all user-assigned custom songs to the back of the list. This will
    # mitigate the chances of these songs being assigned multiple times.
    songs_to_relocate = [item for item in file_data if item[1] in custom_song_names]
    file_data = [item for item in file_data if item[1] not in custom_song_names]
    file_data.extend(songs_to_relocate)

    # Assign random locations from unassigned songs.
    songs_to_be_replaced = []
    if swap_amount > 0:
        try:
            songs_to_be_replaced = random.sample(available_target_songs, swap_amount)
        except ValueError:
            # Too many vanilla songs have been placed to hit the requested
            # proportion. Just fill all possible locations.
            songs_to_be_replaced = available_target_songs
    # Add assigned custom songs back as locations.
    songs_to_be_replaced.extend(custom_song_locations)

    # Place Songs
    ROM_COPY = ROM()
    for song_enum in songs_to_be_replaced:
        song = song_data[song_enum]
        selected_bank = None
        assigned_song_name = getCustomSongAssignedToLocation(settings, song_enum)
        if assigned_song_name is not None:
            new_song = getAssignedCustomSong(file_data, assigned_song_name)
        else:
            new_song = requestNewSong(file_data, song.location_tags, song.song_length, target_type, not settings.fill_with_custom_music)
        selected_cap = 0xFFFFFF
        if new_song is not None:
            new_song_data = bytes(new_song.song_file)
            for bank in storage_banks:
                if len(new_song_data) <= storage_banks[bank]:  # Song can fit in bank
                    if selected_cap > storage_banks[bank]:  # Bank size is new lowest that fits
                        selected_bank = bank
                        selected_cap = storage_banks[bank]
            if selected_bank is not None:
                old_bank = (song.memory >> 1) & 3
                if old_bank < selected_bank:
                    selected_bank = old_bank  # If vanilla bank is bigger, use the vanilla bank
                # Construct new memory data based on variables
                song.memory &= 0xFEF9
                song.memory |= (selected_bank & 3) << 1
                loop = doesSongLoop(new_song_data)
                loop_val = 0
                if loop:
                    loop_val = 1
                song.memory |= loop_val << 8
                # Write Song
                song.output_name = new_song.name
                song.shuffled = True
                entry_data = js.pointer_addresses[0]["entries"][song.mem_idx]
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

    for song in song_data.values():
        song.Reset()
        ROM_COPY.seek(TYPE_ARRAY + song.mem_idx)
        if song.type in TYPE_VALUES:
            ROM_COPY.write(TYPE_VALUES.index(song.type))
        else:
            ROM_COPY.write(255)
    # Check if we have anything beyond default set for BGM
    if settings.music_bgm_randomized or settings.song_select_enabled:
        # If the user selected standard rando
        if not ENABLE_CHAOS:
            if js.cosmetics is not None and js.cosmetic_names is not None and js.cosmetic_extensions is not None:
                # If uploaded, replace some songs with the uploaded songs
                if settings.music_bgm_randomized:
                    # Insert all of the custom songs.
                    insertUploaded(settings, list(js.cosmetics.bgm), list(js.cosmetic_names.bgm), list(js.cosmetic_extensions.bgm), SongType.BGM)
                else:
                    # Only insert the assigned songs.
                    assigned_songs = []
                    assigned_names = []
                    assigned_extensions = []
                    for song, name, extension in zip(js.cosmetics.bgm, js.cosmetic_names.bgm, js.cosmetic_extensions.bgm):
                        if name in getAllAssignedCustomSongs(settings).values():
                            assigned_songs.append(song)
                            assigned_names.append(name)
                            assigned_extensions.append(extension)
                    insertUploaded(settings, assigned_songs, assigned_names, assigned_extensions, SongType.BGM)
            # Generate the list of BGM songs
            song_list = []
            pre_shuffled_songs = []
            assigned_songs = []
            assigned_locations = []
            for channel_index in range(12):
                song_list.append([])
                pre_shuffled_songs.append([])
                assigned_songs.append([])
                assigned_locations.append([])
            # Assign all of the user-specified songs.
            if settings.song_select_enabled:
                for song_location, song in song_data.items():
                    if song.type != SongType.BGM or song.shuffled:
                        continue
                    assigned_song_enum = getVanillaSongAssignedToLocation(settings, song_location)
                    if assigned_song_enum is not None:
                        # The location is given the channel of the song replacing it.
                        assigned_song = song_data[assigned_song_enum]
                        assigned_songs[assigned_song.channel - 1].append(js.pointer_addresses[0]["entries"][assigned_song.mem_idx])
                        assigned_locations[assigned_song.channel - 1].append(js.pointer_addresses[0]["entries"][song.mem_idx])
            for song in song_data.values():
                if song.type == SongType.BGM:
                    # For testing, flip these two lines
                    # song_list.append(pointer_addresses[0]["entries"][song.mem_idx])
                    if song.shuffled:
                        pre_shuffled_songs[song.channel - 1].append(js.pointer_addresses[0]["entries"][song.mem_idx])
                    else:
                        song_list[song.channel - 1].append(js.pointer_addresses[0]["entries"][song.mem_idx])
            # ShuffleMusicWithSizeCheck(music_data, song_list)
            for channel_index in range(12):
                shuffled_music = song_list[channel_index].copy()
                if settings.music_bgm_randomized:
                    random.shuffle(shuffled_music)
                # Remove assigned locations.
                open_locations = [x for x in song_list[channel_index] if x not in assigned_locations[channel_index]]
                if settings.music_bgm_randomized:
                    # Move assigned songs to the back of the list, and shorten
                    # to match open_locations.
                    pre_assigned_songs = [x for x in shuffled_music if x in assigned_songs[channel_index]]
                    open_songs = [x for x in shuffled_music if x not in assigned_songs[channel_index]] + pre_assigned_songs
                    open_songs = open_songs[: len(open_locations)]
                else:
                    # We want all non-assigned, non-shuffled songs to be the
                    # same as their locations.
                    open_songs = open_locations.copy()
                location_pool = open_locations + assigned_locations[channel_index] + pre_shuffled_songs[channel_index].copy()
                song_pool = open_songs + assigned_songs[channel_index] + pre_shuffled_songs[channel_index].copy()
                shuffle_music(music_data, location_pool, song_pool)
        # If the user was a poor sap and selected chaos put DK rap for everything
        # Don't assign songs, the user must learn from their mistake
        else:
            # Find the DK rap in the list
            rap_song_data = song_data[Songs.DKRap]
            rap = js.pointer_addresses[0]["entries"][rap_song_data.mem_idx]
            # Find all BGM songs
            song_list = []
            for song in song_data.values():
                if song.type == SongType.BGM:
                    song_list.append(js.pointer_addresses[0]["entries"][song.mem_idx])

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
                ROM_COPY.writeMultipleBytes(rap_song_data.memory, 2)

    for type_data in NON_BGM_DATA:
        if type_data.setting or settings.song_select_enabled:  # If the user wants to randomize the group
            if js.cosmetics is not None and js.cosmetic_names is not None and js.cosmetic_extensions is not None:
                # If uploaded, replace some songs with the uploaded songs
                if type_data.setting:
                    # Insert all of the custom songs.
                    insertUploaded(settings, list(type_data.files), list(type_data.names), list(type_data.extensions), type_data.song_type)
                else:
                    # Only insert the assigned songs.
                    assigned_songs = []
                    assigned_names = []
                    assigned_extensions = []
                    for song, name, extension in zip(list(type_data.files), list(type_data.names), list(type_data.extensions)):
                        if name in getAllAssignedCustomSongs(settings).values():
                            assigned_songs.append(song)
                            assigned_names.append(name)
                            assigned_extensions.append(extension)
                    insertUploaded(settings, assigned_songs, assigned_names, assigned_extensions, type_data.song_type)
            # Load the list of items in that group
            group_items = []
            shuffled_group_items = []
            assigned_items = []
            assigned_item_locations = []
            # Assign all of the user-specified songs.
            if settings.song_select_enabled:
                for song_location, song in song_data.items():
                    if song.type != type_data.song_type:
                        continue
                    assigned_song_enum = getVanillaSongAssignedToLocation(settings, song_location)
                    if assigned_song_enum is not None:
                        assigned_item_locations.append(js.pointer_addresses[0]["entries"][song.mem_idx])
                        assigned_item = song_data[assigned_song_enum]
                        assigned_items.append(js.pointer_addresses[0]["entries"][assigned_item.mem_idx])
            for song in song_data.values():
                if song.type == type_data.song_type:
                    if song.shuffled:
                        shuffled_group_items.append(js.pointer_addresses[0]["entries"][song.mem_idx])
                    else:
                        group_items.append(js.pointer_addresses[0]["entries"][song.mem_idx])
            # Shuffle the group list
            shuffled_music = group_items.copy()
            if type_data.setting:
                random.shuffle(shuffled_music)
            # Remove assigned locations.
            open_locations = [x for x in group_items if x not in assigned_item_locations]
            if type_data.setting:
                # Move assigned songs to the back of the list, and shorten
                # to match open_locations.
                pre_assigned_songs = [x for x in shuffled_music if x in assigned_items]
                open_songs = [x for x in shuffled_music if x not in assigned_items] + pre_assigned_songs
                open_songs = open_songs[: len(open_locations)]
            else:
                # We want all non-assigned, non-shuffled songs to be the
                # same as their locations.
                open_songs = open_locations.copy()
            location_pool = open_locations + assigned_item_locations + shuffled_group_items.copy()
            song_pool = open_songs + assigned_items + shuffled_group_items.copy()
            shuffle_music(music_data, location_pool, song_pool)
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
        memory = song_idx_list[shuffledIndex].memory
        ROM_COPY.seek(0x1FFF000 + 2 * originalIndex)
        ROM_COPY.writeMultipleBytes(memory, 2)
        if song_idx_list[originalIndex].type == SongType.BGM:
            music_data["music_bgm_data"][song_idx_list[originalIndex].name] = song_idx_list[shuffledIndex].output_name
        elif song_idx_list[originalIndex].type == SongType.MajorItem:
            music_data["music_majoritem_data"][song_idx_list[originalIndex].name] = song_idx_list[shuffledIndex].output_name
        elif song_idx_list[originalIndex].type == SongType.MinorItem:
            music_data["music_minoritem_data"][song_idx_list[originalIndex].name] = song_idx_list[shuffledIndex].output_name
        elif song_idx_list[originalIndex].type == SongType.Event:
            music_data["music_event_data"][song_idx_list[originalIndex].name] = song_idx_list[shuffledIndex].output_name
