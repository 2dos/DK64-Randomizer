"""Apply Patch data to the ROM."""

import asyncio
import base64
import io
import json
import math
import random
import zipfile

import js
from randomizer.Enums.Models import Model
from randomizer.Enums.Settings import RandomModels
from randomizer.Lists.Songs import ExcludedSongsSelector
from randomizer.Patching.CosmeticColors import apply_cosmetic_colors, applyHolidayMode, overwrite_object_colors, writeMiscCosmeticChanges
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.MusicRando import randomize_music
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Lib import recalculatePointerJSON, camelCaseToWords

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings, ExcludedSongs
from ui.GenSpoiler import GenerateSpoiler
from ui.GenTracker import generateTracker
from ui.progress_bar import ProgressBar
from ui.serialize_settings import serialize_settings


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


async def patching_response(data, from_patch_gen=False, lanky_from_history=False):
    """Apply the patch data to the ROM in the BROWSER not the server."""
    import time
    from datetime import datetime

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
    try:
        hash_id = str(extracted_variables["file_string"].decode("utf-8"))
    except Exception:
        hash_id = None
    # Make sure we re-load the seed id for patch file creation
    if lanky_from_history:
        js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        loop.run_until_complete(ProgressBar().reset())
        return
    elif settings.download_patch_file and from_patch_gen is False:
        js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
        js.load_old_seeds()
        js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        loop.run_until_complete(ProgressBar().reset())
        return
    elif from_patch_gen is True:
        # Apply the base patch
        await js.apply_patch(data)
    else:
        js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
        js.load_old_seeds()

    sav = settings.rom_data
    datetime = datetime.utcnow()
    unix = time.mktime(datetime.timetuple())
    random.seed(int(unix))
    if from_patch_gen:
        recalculatePointerJSON(ROM())
    apply_cosmetic_colors(settings)

    if settings.override_cosmetics:
        overwrite_object_colors(settings)
        writeMiscCosmeticChanges(settings)
        applyHolidayMode(settings)

        # D-Pad Display
        ROM().seek(sav + 0x139)
        # The DPadDisplays enum is indexed to allow this.
        ROM().write(int(settings.dpad_display))

        if settings.homebrew_header:
            # Write ROM Header to assist some Mupen Emulators with recognizing that this has a 16K EEPROM
            ROM().seek(0x3C)
            CARTRIDGE_ID = "ED"
            ROM().writeBytes(CARTRIDGE_ID.encode("ascii"))
            ROM().seek(0x3F)
            SAVE_TYPE = 2  # 16K EEPROM
            ROM().writeMultipleBytes(SAVE_TYPE << 4, 1)

        # Colorblind mode
        ROM().seek(sav + 0x43)
        # The ColorblindMode enum is indexed to allow this.
        ROM().write(int(settings.colorblind_mode))

        # Remaining Menu Settings
        ROM().seek(sav + 0xC7)
        ROM().write(int(settings.sound_type))  # Sound Type

        music_volume = 40
        sfx_volume = 40
        if settings.sfx_volume is not None and settings.sfx_volume != "":
            sfx_volume = int(settings.sfx_volume / 2.5)
        if settings.music_volume is not None and settings.music_volume != "":
            music_volume = int(settings.music_volume / 2.5)
        ROM().seek(sav + 0xC8)
        ROM().write(sfx_volume)
        ROM().seek(sav + 0xC9)
        ROM().write(music_volume)

        boolean_props = [
            BooleanProperties(settings.disco_chunky, 0x12F),  # Disco Chunky
            BooleanProperties(settings.remove_water_oscillation, 0x10F),  # Remove Water Oscillation
            BooleanProperties(settings.dark_mode_textboxes, 0x44),  # Dark Mode Text bubble
            BooleanProperties(settings.camera_is_follow, 0xCB),  # Free/Follow Cam
            BooleanProperties(settings.camera_is_not_inverted, 0xCC),  # Inverted/Non-Inverted Camera
        ]

        for prop in boolean_props:
            if prop.check:
                ROM().seek(sav + prop.offset)
                ROM().write(prop.target)

        # Excluded Songs
        if settings.songs_excluded:
            disabled_songs = settings.excluded_songs_selected.copy()
            write_data = [0]
            for item in ExcludedSongsSelector:
                if (ExcludedSongs[item["value"]] in disabled_songs and item["shift"] >= 0) or len(disabled_songs) == 0:
                    offset = int(item["shift"] >> 3)
                    check = int(item["shift"] % 8)
                    write_data[offset] |= 0x80 >> check
            ROM().seek(sav + 0x1B7)
            ROM().writeMultipleBytes(write_data[0], 1)

        ROM().seek(sav + 0xC3)
        ROM().writeMultipleBytes(int(settings.crosshair_outline), 1)

        ROM().seek(sav + 0x114)
        ROM().writeMultipleBytes(int(settings.troff_brighten), 1)

        if settings.true_widescreen:
            ROM().seek(sav + 0x1B4)
            ROM().write(1)

            GFX_START = 0x101A40
            SCREEN_WD = 366
            SCREEN_HD = 208
            BOOT_OFFSET = 0xFB20 - 0xEF20

            ROM().seek(GFX_START + 0x00)
            ROM().writeMultipleBytes(SCREEN_WD * 2, 2)  # 2D Viewport Width
            ROM().seek(GFX_START + 0x02)
            ROM().writeMultipleBytes(SCREEN_HD * 2, 2)  # 2D Viewport Height
            ROM().seek(GFX_START + 0x08)
            ROM().writeMultipleBytes(SCREEN_WD * 2, 2)  # 2D Viewport X Position
            ROM().seek(GFX_START + 0x0A)
            ROM().writeMultipleBytes(SCREEN_HD * 2, 2)  # 2D Viewport Y Position
            ROM().seek(GFX_START + 0x9C)
            ROM().writeMultipleBytes((SCREEN_WD << 14) | (SCREEN_HD << 2), 4)  # Default Scissor for 2D
            data_offsets = [0xEF20, 0xF7E0]
            internal_size = 0x50
            internal_offsets = [0, 2]
            for tv_offset in data_offsets:
                for int_offset in internal_offsets:
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x08)
                    ROM().writeMultipleBytes(SCREEN_WD, 4)  # VI Width
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x20)
                    ROM().writeMultipleBytes(int((SCREEN_WD * 512) / 320), 4)  # VI X Scale
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x28)
                    ROM().writeMultipleBytes((SCREEN_WD * 2), 4)  # VI Field 1 Framebuffer Offset
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x3C)
                    ROM().writeMultipleBytes((SCREEN_WD * 2), 4)  # VI Field 2 Framebuffer Offset
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x2C)
                    ROM().writeMultipleBytes(int((SCREEN_HD * 1024) / 240), 4)  # VI Field 1 Y Scale
                    ROM().seek(BOOT_OFFSET + tv_offset + (internal_size * int_offset) + 0x40)
                    ROM().writeMultipleBytes(int((SCREEN_HD * 1024) / 240), 4)  # VI Field 2 Y Scale
            ROM().seek(BOOT_OFFSET + 0xBC4 + 2)
            ROM().writeMultipleBytes(SCREEN_WD * 2, 2)  # Row Offset of No Expansion Pak Image
            ROM().seek(BOOT_OFFSET + 0xBC8 + 2)
            ROM().writeMultipleBytes(SCREEN_WD * SCREEN_HD * 2, 2)  # Invalidation Size for Framebuffer 1
            ROM().seek(BOOT_OFFSET + 0xE08)
            ROM().writeMultipleBytes(0x24180000 | SCREEN_WD, 4)  # Row Pitch for No Expansion Pak Screen Text
            ROM().seek(BOOT_OFFSET + 0xE0C)
            ROM().writeMultipleBytes(0x03060019, 4)  # Calculate Row Pixel Number for No Expansion Pak Screen Text
            ROM().seek(BOOT_OFFSET + 0xE10)
            ROM().writeMultipleBytes(0x0000C012, 4)  # Get Row Pixel Number for No Expansion Pak Screen Text
            ROM().seek(BOOT_OFFSET + 0x1020 + 2)
            ROM().writeMultipleBytes((SCREEN_WD - 8) * 2, 2)  # Text Framebuffer Pitch

        # Apply Hash
        order = 0
        loaded_hash = get_hash_images("browser", "hash")
        for count in json.loads(extracted_variables["hash"].decode("utf-8")):
            js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
            order += 1

        music_data = randomize_music(settings)

        spoiler = updateJSONCosmetics(spoiler, settings, music_data, int(unix))

    loaded_settings = spoiler["Settings"]
    tables = {}
    t = 0
    for i in range(0, 3):
        js.document.getElementById(f"settings_table_{i}").innerHTML = ""
        tables[i] = js.document.getElementById(f"settings_table_{i}")
    for setting, value in loaded_settings.items():
        hidden_settings = ["Seed", "algorithm"]
        if setting not in hidden_settings:
            if tables[t].rows.length > math.ceil((len(loaded_settings.items()) - len(hidden_settings)) / len(tables)):
                t += 1
            row = tables[t].insertRow(-1)
            name = row.insertCell(0)
            description = row.insertCell(1)
            name.innerHTML = setting
            description.innerHTML = FormatSpoiler(value)

    await ProgressBar().update_progress(10, "Seed Generated.")
    js.document.getElementById("nav-settings-tab").style.display = ""
    if spoiler.get("Requirements"):
        js.document.getElementById("tracker_text").value = generateTracker(spoiler)
    else:
        js.document.getElementById("tracker_text").value = ""
    js.document.getElementById("spoiler_log_block").style.display = ""
    loop.run_until_complete(GenerateSpoiler(spoiler))
    js.document.getElementById("generated_seed_id").innerHTML = seed_id
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
    ROM().fixSecurityValue()
    ROM().save(f"dk64r-rom-{seed_id}.z64")
    loop.run_until_complete(ProgressBar().reset())
    js.jq("#nav-settings-tab").tab("show")


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
    return humanspoiler
