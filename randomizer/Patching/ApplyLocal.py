"""Apply Patch data to the ROM."""
# import json
# import js
# import random
# from randomizer.Patching.CosmeticColors import (
#     apply_cosmetic_colors,
#     overwrite_object_colors,
#     applyKrushaKong,
#     writeMiscCosmeticChanges,
#     applyHolidayMode,
#     applyHelmDoorCosmetics,
# )
# from randomizer.Patching.Hash import get_hash_images
# from randomizer.Patching.MusicRando import randomize_music
import io
import js
import zipfile
import base64
# from randomizer.Spoiler import Spoiler
#from randomizer.Settings import Settings


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


def patching_response(spoiler):
    # Unzip the data_passed
    
    # Base64 decode the data
    spoiler = base64.b64decode(spoiler)
 # Create an in-memory byte stream from the zip data
    zip_stream = io.BytesIO(spoiler)

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

    print(extracted_variables["spoiler_log"])
    print(extracted_variables["hash"])    
    
    # # Make sure we re-load the seed id
    # spoiler.settings.set_seed()
    # if spoiler.settings.download_patch_file:
    #     spoiler.settings.download_patch_file = False
  
    
    # sav = spoiler.settings.rom_data


    # random.seed(None)
    # randomize_music(spoiler)
    # applyKrushaKong(spoiler)
    # apply_cosmetic_colors(spoiler)
    # overwrite_object_colors(spoiler)
    # writeMiscCosmeticChanges(spoiler)
    # applyHolidayMode(spoiler)
    # applyHelmDoorCosmetics(spoiler)
    # random.seed(spoiler.settings.seed)



    # if spoiler.settings.homebrew_header:
    #     # Write ROM Header to assist some Mupen Emulators with recognizing that this has a 16K EEPROM
    #     ROM().seek(0x3C)
    #     CARTRIDGE_ID = "ED"
    #     ROM().writeBytes(CARTRIDGE_ID.encode("ascii"))
    #     ROM().seek(0x3F)
    #     SAVE_TYPE = 2  # 16K EEPROM
    #     ROM().writeMultipleBytes(SAVE_TYPE << 4, 1)     
       

    # # Colorblind mode
    # ROM().seek(sav + 0x43)
    # # The ColorblindMode enum is indexed to allow this.
    # ROM().write(int(spoiler.settings.colorblind_mode))




    # #Remaining Menu Settings
    # ROM().seek(sav + 0xC7)
    # ROM().write(int(spoiler.settings.sound_type)) # Sound Type
    
    
    
    
    # music_volume = 40
    # sfx_volume = 40
    # if spoiler.settings.sfx_volume is not None and spoiler.settings.sfx_volume != "":
    #     sfx_volume = int(spoiler.settings.sfx_volume / 2.5)
    # if spoiler.settings.music_volume is not None and spoiler.settings.music_volume != "":
    #     music_volume = int(spoiler.settings.music_volume / 2.5)
    # ROM().seek(sav + 0xC8)
    # ROM().write(sfx_volume)
    # ROM().seek(sav + 0xC9)
    # ROM().write(music_volume) 
        
    # boolean_props = [
    #     BooleanProperties(spoiler.settings.disco_chunky, 0x12F),  # Disco Chunky
    #     BooleanProperties(spoiler.settings.remove_water_oscillation, 0x10F),  # Remove Water Oscillation
    #     BooleanProperties(spoiler.settings.dark_mode_textboxes, 0x44),  # Dark Mode Text bubble
    #     BooleanProperties(spoiler.settings.camera_is_follow, 0xCB),  # Free/Follow Cam
    #     BooleanProperties(spoiler.settings.camera_is_widescreen, 0xCA),  # Normal/Widescreen
    #     BooleanProperties(spoiler.settings.camera_is_not_inverted, 0xCC),  # Inverted/Non-Inverted Camera
    # ]

    # for prop in boolean_props:
    #     if prop.check:
    #         ROM().seek(sav + prop.offset)
    #         ROM().write(prop.target)

    # # Apply Hash
    # order = 0
    # loaded_hash = get_hash_images()
    # for count in spoiler.settings.seed_hash:
    #     js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
    #     order += 1

    # spoiler.updateJSONCosmetics()
   
    
    # loaded_settings = json.loads(spoiler.json)["Settings"]
   
    # ROM().fixSecurityValue()
    # ROM().save(f"dk64r-rom-{spoiler.settings.seed_id}.z64")
    

        

def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result
