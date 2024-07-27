"""Apply Patch data to the ROM."""

import asyncio
import base64
import io
import json
import math
import random
import zipfile
import time
import string
from datetime import datetime as Datetime
from datetime import UTC
import js
from randomizer.Enums.Models import Model
from randomizer.Enums.Settings import RandomModels
from randomizer.Lists.Songs import ExcludedSongsSelector
from randomizer.Patching.CosmeticColors import apply_cosmetic_colors, applyHolidayMode, overwrite_object_colors, writeMiscCosmeticChanges, writeCrownNames, darkenDPad, lightenPauseBubble
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.MusicRando import randomize_music
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Lib import recalculatePointerJSON, camelCaseToWords, writeText
from randomizer.Patching.ASMPatcher import patchAssemblyCosmetic
from randomizer.Lists.Songs import getSongIndexFromName

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings, ExcludedSongs, DPadDisplays, KongModels
from ui.GenSpoiler import GenerateSpoiler
from ui.GenTracker import generateTracker
from ui.progress_bar import ProgressBar
from ui.serialize_settings import serialize_settings

from version import major, minor, patch


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


async def patching_response(data, from_patch_gen=False, lanky_from_history=False, gen_history=False):
    """Apply the patch data to the ROM in the BROWSER not the server."""
    # Unzip the data_passed
    loop = asyncio.get_event_loop()
    # Base64 decode the data
    decoded_data = base64.b64decode(data)
    # Create an in-memory byte stream from the zip data
    zip_stream = io.BytesIO(decoded_data)

    # Dictionary to store the extracted variables
    extracted_variables = {}

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_stream, "r") as zip_file:
        for file_name in zip_file.namelist():
            # Read the contents of each file in the zip
            with zip_file.open(file_name) as file:
                # Convert the file contents back to their original data type
                variable_value = file.read()

                # Store the extracted variable
                variable_name = file_name.split(".")[0]
                extracted_variables[variable_name] = variable_value
    settings = Settings(serialize_settings(include_plando=True))
    seed_id = str(extracted_variables["seed_id"].decode("utf-8"))
    spoiler = json.loads(extracted_variables["spoiler_log"])
    if extracted_variables.get("version") is None:
        version = "0.0.0"
    else:
        version = str(extracted_variables["version"].decode("utf-8"))
    try:
        hash_id = str(extracted_variables["seed_number"].decode("utf-8"))
    except Exception:
        hash_id = None
    # Make sure we re-load the seed id for patch file creation
    js.event_response_data = data
    if lanky_from_history:
        js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        loop.run_until_complete(ProgressBar().reset())
        return
    # elif settings.download_patch_file and from_patch_gen is False:
    #     js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
    #     js.load_old_seeds()
    #     js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
    #     loop.run_until_complete(ProgressBar().reset())
    #     return
    elif from_patch_gen is True:
        if js.document.getElementById("download_patch_file").checked and js.document.getElementById("generate_seed").value != "Download Seed":
            js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        gif_fairy = get_hash_images("browser", "loading-fairy")
        gif_dead = get_hash_images("browser", "loading-dead")
        js.document.getElementById("progress-fairy").src = "data:image/jpeg;base64," + gif_fairy[0]
        js.document.getElementById("progress-dead").src = "data:image/jpeg;base64," + gif_dead[0]
        # Apply the base patch
        await js.apply_patch(data)
        if gen_history is False:
            js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
            js.load_old_seeds()

    curr_time = Datetime.now(UTC)
    unix = time.mktime(curr_time.timetuple())
    random.seed(int(unix))
    split_version = version.split(".")
    patch_major = split_version[0]
    patch_minor = split_version[1]
    patch_patch = split_version[2]
    if major != patch_major or minor != patch_minor:
        js.document.getElementById("patch_version_warning").hidden = False
        js.document.getElementById("patch_warning_message").innerHTML = (
            f"This patch was generated with version {patch_major}.{patch_minor}.{patch_patch} of the randomizer, but you are using version {major}.{minor}.{patch}. Cosmetic packs have been disabled for this patch."
        )
    elif from_patch_gen is True:
        sav = settings.rom_data
        if from_patch_gen:
            recalculatePointerJSON(ROM())
        js.document.getElementById("patch_version_warning").hidden = True
        ROM_COPY = ROM()
        if settings.disco_chunky and settings.kong_model_chunky == KongModels.default and settings.override_cosmetics:
            settings.kong_model_chunky = KongModels.disco_chunky
            ROM_COPY.seek(settings.rom_data + 0x1B8 + 4)
            ROM_COPY.writeMultipleBytes(6, 1)
            chunky_slots = [11, 12]
            disco_slots = [0xD, 0xEC]
            for model_slot in range(2):
                dest_start = js.pointer_addresses[5]["entries"][chunky_slots[model_slot]]["pointing_to"]
                source_start = js.pointer_addresses[5]["entries"][disco_slots[model_slot]]["pointing_to"]
                source_end = js.pointer_addresses[5]["entries"][disco_slots[model_slot] + 1]["pointing_to"]
                source_size = source_end - source_start
                ROM_COPY.seek(source_start)
                file_bytes = ROM_COPY.readBytes(source_size)
                ROM_COPY.seek(dest_start)
                ROM_COPY.writeBytes(file_bytes)
                # Write uncompressed size
                unc_table = js.pointer_addresses[26]["entries"][5]["pointing_to"]
                ROM_COPY.seek(unc_table + (disco_slots[model_slot] * 4))
                unc_size = int.from_bytes(ROM_COPY.readBytes(4), "big")
                ROM_COPY.seek(unc_table + (chunky_slots[model_slot] * 4))
                ROM_COPY.writeMultipleBytes(unc_size, 4)
        apply_cosmetic_colors(settings)

        if settings.override_cosmetics:
            overwrite_object_colors(settings, ROM_COPY)
            writeMiscCosmeticChanges(settings)
            applyHolidayMode(settings)
            lightenPauseBubble(settings)
            if settings.misc_cosmetics:
                writeCrownNames()

            # D-Pad Display
            ROM_COPY.seek(sav + 0x139)
            # The DPadDisplays enum is indexed to allow this.
            ROM_COPY.write(int(settings.dpad_display))

            if settings.dpad_display == DPadDisplays.on and settings.dark_mode_textboxes:
                darkenDPad()

            if settings.homebrew_header:
                # Write ROM Header to assist some Mupen Emulators with recognizing that this has a 16K EEPROM
                ROM_COPY.seek(0x3C)
                CARTRIDGE_ID = "ED"
                ROM_COPY.writeBytes(CARTRIDGE_ID.encode("ascii"))
                ROM_COPY.seek(0x3F)
                SAVE_TYPE = 2  # 16K EEPROM
                ROM_COPY.writeMultipleBytes(SAVE_TYPE << 4, 1)

            # Colorblind mode
            ROM_COPY.seek(sav + 0x43)
            # The ColorblindMode enum is indexed to allow this.
            ROM_COPY.write(int(settings.colorblind_mode))

            # Big head mode
            ROM_COPY.seek(sav + 0x1E1)
            # The BigHeadMode enum is indexed to allow this.
            ROM_COPY.write(int(settings.big_head_mode))

            # Remaining Menu Settings
            ROM_COPY.seek(sav + 0xC7)
            ROM_COPY.write(int(settings.sound_type))  # Sound Type

            music_volume = 40
            sfx_volume = 40
            if settings.sfx_volume is not None and settings.sfx_volume != "":
                sfx_volume = int(settings.sfx_volume / 2.5)
            if settings.music_volume is not None and settings.music_volume != "":
                music_volume = int(settings.music_volume / 2.5)
            ROM_COPY.seek(sav + 0xC8)
            ROM_COPY.write(sfx_volume)
            ROM_COPY.seek(sav + 0xC9)
            ROM_COPY.write(music_volume)

            boolean_props = [
                BooleanProperties(settings.remove_water_oscillation, 0x10F),  # Remove Water Oscillation
                BooleanProperties(settings.dark_mode_textboxes, 0x44),  # Dark Mode Text bubble
                BooleanProperties(settings.pause_hint_coloring, 0x1E4),  # Pause Hint Coloring
                BooleanProperties(settings.camera_is_follow, 0xCB),  # Free/Follow Cam
                BooleanProperties(settings.camera_is_not_inverted, 0xCC),  # Inverted/Non-Inverted Camera
            ]

            for prop in boolean_props:
                if prop.check:
                    ROM_COPY.seek(sav + prop.offset)
                    ROM_COPY.write(prop.target)

            # Excluded Songs
            if settings.songs_excluded:
                disabled_songs = settings.excluded_songs_selected.copy()
                write_data = [0]
                for item in ExcludedSongsSelector:
                    if (ExcludedSongs[item["value"]] in disabled_songs and item["shift"] >= 0) or len(disabled_songs) == 0:
                        offset = int(item["shift"] >> 3)
                        check = int(item["shift"] % 8)
                        write_data[offset] |= 0x80 >> check
                ROM_COPY.seek(sav + 0x1B7)
                ROM_COPY.writeMultipleBytes(write_data[0], 1)

            ROM_COPY.seek(sav + 0xC3)
            ROM_COPY.writeMultipleBytes(int(settings.crosshair_outline), 1)

            ROM_COPY.seek(sav + 0x114)
            ROM_COPY.writeMultipleBytes(int(settings.troff_brighten), 1)

            patchAssemblyCosmetic(ROM_COPY, settings)
            music_data, music_names = randomize_music(settings)
            music_text = []
            accepted_characters = [*string.ascii_uppercase] + [" ", "\n", "(", ")", "%", ",", ".", "!", ">", ":", ";", "'", "-"] + [*string.digits]
            for name in music_names:
                output_name = name
                if name is None:
                    output_name = ""
                music_text.append([{"text": ["".join([x for x in [*output_name.upper()] if x in accepted_characters])]}])
            if len(music_names) > 0:
                writeText(46, music_text, True)
            if settings.show_song_name:
                ROM_COPY.seek(sav + 0x1ED)
                ROM_COPY.write(1)

            spoiler = updateJSONCosmetics(spoiler, settings, music_data, int(unix))

        # Apply Hash
        order = 0
        loaded_hash = get_hash_images("browser", "hash")
        for count in json.loads(extracted_variables["hash"].decode("utf-8")):
            js.document.getElementById("hashdiv").innerHTML = ""
            # clear the innerHTML of the hash element
            js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
            order += 1
    # if the hash is not set, just put the text in the spoiler log
    if js.document.getElementById("hash0").src == "":
        # insert a text div into the js.document.getElementById("hashdiv") and set the innerHTML to the No ROM loaded message add the div
        js.document.getElementById("hashdiv").innerHTML = "Shared Link, No Hash Images Loaded."

    if from_patch_gen is True:
        await ProgressBar().update_progress(10, "Seed Generated.")
    js.document.getElementById("nav-settings-tab").style.display = ""
    js.document.getElementById("spoiler_log_block").style.display = ""
    loop.run_until_complete(GenerateSpoiler(spoiler))
    js.document.getElementById("generated_seed_id").innerHTML = seed_id
    # Set the current URL to the seed ID so that it can be shared without reloading the page
    js.window.history.pushState("generated_seed", hash_id, f"/randomizer?seed_id={hash_id}")
    # if generate_spoiler_log is False enable the download_unlocked_spoiler_button button
    if settings.generate_spoilerlog is False and hash_id is not None:
        try:
            js.document.getElementById("download_unlocked_spoiler_button").onclick = lambda x: js.unlock_spoiler_log(hash_id)
            js.document.getElementById("download_unlocked_spoiler_button").hidden = False
        except Exception:
            js.document.getElementById("download_unlocked_spoiler_button").hidden = True
            js.document.getElementById("download_unlocked_spoiler_button").onclick = None
    else:
        js.document.getElementById("download_unlocked_spoiler_button").hidden = True
        js.document.getElementById("download_unlocked_spoiler_button").onclick = None
    if from_patch_gen is True:
        ROM().fixSecurityValue()
        ROM().save(f"dk64r-rom-{seed_id}.z64")
        loop.run_until_complete(ProgressBar().reset())
    js.jq("#nav-settings-tab").tab("show")
    js.check_seed_info_tab()


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result


def updateJSONCosmetics(spoiler, settings, music_data, cosmetic_seed):
    """Update spoiler JSON with cosmetic settings."""
    humanspoiler = spoiler
    humanspoiler["Settings"]["Cosmetic Seed"] = cosmetic_seed

    random_model_choices = [
        {"name": "Beaver Bother Klaptrap", "setting": settings.bother_klaptrap_model},
        {"name": "Beetle", "setting": settings.beetle_model},
        {"name": "Rabbit", "setting": settings.rabbit_model},
        {"name": "Peril Path Panic Fairy", "setting": settings.panic_fairy_model},
        {"name": "Peril Path Panic Klaptrap", "setting": settings.panic_klaptrap_model},
        {"name": "Turtle", "setting": settings.turtle_model},
        {"name": "Searchlight Seek Klaptrap", "setting": settings.seek_klaptrap_model},
        {"name": "Forest Tomato", "setting": settings.fungi_tomato_model},
        {"name": "Caves Tomato", "setting": settings.caves_tomato_model},
        {"name": "Factory Piano Burper", "setting": settings.piano_burp_model},
        {"name": "Spotlight Fish", "setting": settings.spotlight_fish_model},
        {"name": "Candy (Chunky Phase, End Sequence)", "setting": settings.candy_cutscene_model},
        {"name": "Funky (Chunky Phase, End Sequence)", "setting": settings.funky_cutscene_model},
        {"name": "Funky's Boot (Chunky Phase)", "setting": settings.boot_cutscene_model},
    ]

    if settings.colors != {} or settings.random_models != RandomModels.off:
        humanspoiler["Cosmetics"]["Colors"] = {}
        humanspoiler["Cosmetics"]["Models"] = {}
        for color_item in settings.colors:
            if color_item == "dk":
                humanspoiler["Cosmetics"]["Colors"]["DK Color"] = settings.colors[color_item]
            else:
                humanspoiler["Cosmetics"]["Colors"][f"{color_item.capitalize()} Color"] = settings.colors[color_item]
        for data in random_model_choices:
            if isinstance(data["setting"], Model):
                humanspoiler["Cosmetics"]["Models"][data["name"]] = camelCaseToWords(data["setting"].name)
            else:
                humanspoiler["Cosmetics"]["Models"][data["name"]] = f"Unknown Model {hex(int(data['setting']))}"
    if settings.music_bgm_randomized or settings.bgm_songs_selected:
        humanspoiler["Cosmetics"]["Background Music"] = music_data.get("music_bgm_data")
    if settings.music_majoritems_randomized or settings.majoritems_songs_selected:
        humanspoiler["Cosmetics"]["Major Item Themes"] = music_data.get("music_majoritem_data")
    if settings.music_minoritems_randomized or settings.minoritems_songs_selected:
        humanspoiler["Cosmetics"]["Minor Item Themes"] = music_data.get("music_minoritem_data")
    if settings.music_events_randomized or settings.events_songs_selected:
        humanspoiler["Cosmetics"]["Event Themes"] = music_data.get("music_event_data")
    humanspoiler["Cosmetics"]["Textures"] = {}
    if settings.custom_transition is not None:
        humanspoiler["Cosmetics"]["Textures"]["Transition"] = settings.custom_transition
    if settings.custom_troff_portal is not None:
        humanspoiler["Cosmetics"]["Textures"]["Troff 'n' Scoff Portal"] = settings.custom_troff_portal
    return humanspoiler
