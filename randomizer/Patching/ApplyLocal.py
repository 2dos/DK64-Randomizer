"""Apply Patch data to the ROM."""

import asyncio
import base64
import io
import json
import math
import random
import time
import zipfile

import js
from randomizer.Patching.CosmeticColors import apply_cosmetic_colors, applyHolidayMode, overwrite_object_colors, writeMiscCosmeticChanges
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.MusicRando import randomize_music
from randomizer.Patching.Patcher import ROM

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings
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


async def patching_response(data, from_patch_gen=False):
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
    settings = Settings(serialize_settings())
    seed_id = str(extracted_variables["seed_id"].decode("utf-8"))
    spoiler = json.loads(extracted_variables["spoiler_log"])
    # Make sure we re-load the seed id
    if settings.download_patch_file and from_patch_gen is False:
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
    random.seed(None)
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
        loaded_hash = get_hash_images("browser")
        for count in json.loads(extracted_variables["hash"].decode("utf-8")):
            js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
            order += 1

        music_data = randomize_music(settings)

        spoiler = updateJSONCosmetics(spoiler, settings, music_data)

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


def updateJSONCosmetics(spoiler, settings, music_data):
    """Update spoiler JSON with cosmetic settings."""
    humanspoiler = spoiler
    if settings.colors != {} or settings.klaptrap_model_index:
        humanspoiler["Cosmetics"]["Colors and Models"] = {}
        for color_item in settings.colors:
            if color_item == "dk":
                humanspoiler["Cosmetics"]["Colors and Models"]["DK Color"] = settings.colors[color_item]
            else:
                humanspoiler["Cosmetics"]["Colors and Models"][f"{color_item.capitalize()} Color"] = settings.colors[color_item]
        klap_models = {
            0x19: "Beaver",
            0x1E: "Klobber",
            0x20: "Kaboom",
            0x21: "Green Klaptrap",
            0x22: "Purple Klaptrap",
            0x23: "Red Klaptrap",
            0x24: "Klaptrap Teeth",
            0x26: "Krash",
            0x27: "Troff",
            0x30: "N64 Logo",
            0x34: "Mech Fish",
            0x42: "Krossbones",
            0x47: "Rabbit",
            0x4B: "Minecart Skeleton Head",
            0x51: "Tomato",
            0x62: "Ice Tomato",
            0x69: "Golden Banana",
            0x70: "Microbuffer",
            0x72: "Bell",
            0x96: "Missile (Car Race)",
            0xB0: "Red Buoy",
            0xB1: "Green Buoy",
            0xBD: "Rareware Logo",
        }
        if settings.klaptrap_model_index in klap_models:
            humanspoiler["Cosmetics"]["Colors and Models"]["Klaptrap Model"] = klap_models[settings.klaptrap_model_index]
        else:
            humanspoiler["Cosmetics"]["Colors and Models"]["Klaptrap Model"] = f"Unknown Model {hex(settings.klaptrap_model_index)}"
    if settings.music_bgm_randomized:
        humanspoiler["Cosmetics"]["Background Music"] = music_data.get("music_bgm_data")
    if settings.music_majoritems_randomized:
        humanspoiler["Cosmetics"]["Major Item Themes"] = music_data.get("music_majoritem_data")
    if settings.music_minoritems_randomized:
        humanspoiler["Cosmetics"]["Minor Item Themes"] = music_data.get("music_minoritem_data")
    if settings.music_events_randomized:
        humanspoiler["Cosmetics"]["Event Themes"] = music_data.get("music_event_data")
    return humanspoiler
