"""Apply Patch data to the ROM."""
import json
import random

from randomizer.DKTV import randomize_dktv
from randomizer.MusicRando import randomize_music
from randomizer.Patcher import ROM
from ui.progress_bar import ProgressBar


def patching_response(responded_data):
    """Response data from the background task.

    Args:
        responded_data (dict): Json data
    """
    loaded_data = json.loads(responded_data)
    if loaded_data.get("error"):
        error = loaded_data.get("error")
        ProgressBar().set_class("bg-danger")
        ProgressBar().update_progress(10, f"Error: {error}")
        ProgressBar().reset()
        return None
    ProgressBar().update_progress(5, "Applying Patches")
    settings = loaded_data.get("Settings")
    random.seed(settings.get("seed"))

    # Starting index for our settings
    sav = 0x1FED020

    if settings.get("shuffle_levels"):
        ROM().seek(sav + 0x000)
        ROM().write(1)

    # TODO: Dummy function
    if settings.get("Level_Order"):
        order = 0
        for level in loaded_data:
            ROM().seek(sav + 0x001 + order)
            ROM().write(level)
            order += 1
    else:
        for i in range(0, 6):
            ROM().seek(sav + 0x001 + i)
            ROM().write(i)

    if settings.get("troff_n_scoff_bananas"):
        order = 0
        for count in settings.get("troff_n_scoff_bananas"):
            ROM().seek(sav + 0x008 + order)
            ROM().write(count)
            order += 2
    else:
        ROM().seek(sav + 0x008 + 0)
        ROM().writeMultipleBytes(60,2)
        ROM().seek(sav + 0x008 + 2)
        ROM().writeMultipleBytes(120,2)
        ROM().seek(sav + 0x008 + 4)
        ROM().writeMultipleBytes(200,2)
        ROM().seek(sav + 0x008 + 6)
        ROM().writeMultipleBytes(250,2)
        ROM().seek(sav + 0x008 + 8)
        ROM().writeMultipleBytes(300,2)
        ROM().seek(sav + 0x008 + 10)
        ROM().writeMultipleBytes(350,2)
        ROM().seek(sav + 0x008 + 12)
        ROM().writeMultipleBytes(400,2)

    if settings.get("blocker_golden_bananas"):
        order = 0
        for count in settings.get("blocker_golden_bananas"):
            ROM().seek(sav + 0x016 + order)
            ROM().write(count)
            order += 1
    else:
        ROM().seek(sav + 0x016 + 0)
        ROM().write(1)
        ROM().seek(sav + 0x016 + 1)
        ROM().write(5)
        ROM().seek(sav + 0x016 + 2)
        ROM().write(15)
        ROM().seek(sav + 0x016 + 3)
        ROM().write(30)
        ROM().seek(sav + 0x016 + 4)
        ROM().write(50)
        ROM().seek(sav + 0x016 + 5)
        ROM().write(65)
        ROM().seek(sav + 0x016 + 6)
        ROM().write(80)
        ROM().seek(sav + 0x016 + 7)
        ROM().write(100)

    # TODO: Dummy function
    if settings.get("key_flags"):
        order = 0
        for level in loaded_data:
            ROM().seek(sav + 0x01E + order)
            ROM().write(level)
            order += 2
    else:
        ROM().seek(sav + 0x01E + 0)
        ROM().writeMultipleBytes(0x1A,2)
        ROM().seek(sav + 0x01E + 2)
        ROM().writeMultipleBytes(0x4A,2)

        ROM().seek(sav + 0x01E + 4)
        ROM().writeMultipleBytes(0x8A,2)

        ROM().seek(sav + 0x01E + 6)
        ROM().writeMultipleBytes(0xA8,2)

        ROM().seek(sav + 0x01E + 8)
        ROM().writeMultipleBytes(0xEC,2)

        ROM().seek(sav + 0x01E + 10)
        ROM().writeMultipleBytes(0x124,2)

        ROM().seek(sav + 0x01E + 12)
        ROM().writeMultipleBytes(0x13D,2)


    if settings.get("unlock_all_kongs"):
        ROM().seek(sav + 0x02C)
        ROM().write(1)

    if settings.get("unlock_all_moves"):
        ROM().seek(sav + 0x02D)
        ROM().write(1)

    if settings.get("fast_start_beginning_of_game"):
        ROM().seek(sav + 0x02E)
        ROM().write(1)

    if settings.get("unlock_fairy_shockwave"):
        ROM().seek(sav + 0x02F)
        ROM().write(1)

    if settings.get("enable_tag_anywhere"):
        ROM().seek(sav + 0x030)
        ROM().write(1)

    if settings.get("fast_start_hideout_helm"):
        ROM().seek(sav + 0x031)
        ROM().write(1)

    if settings.get("crown_door_open"):
        ROM().seek(sav + 0x032)
        ROM().write(1)

    if settings.get("coin_door_open"):
        ROM().seek(sav + 0x033)
        ROM().write(1)

    if settings.get("quality_of_life"):
        ROM().seek(sav + 0x034)
        ROM().write(1)

    randomize_dktv()
    randomize_music(settings)
    ProgressBar().update_progress(10, "Seed Generated.")
    ROM().fixSecurityValue()
    seed = settings.get("seed")
    ROM().save(f"dk64-{seed}.z64")
    ProgressBar().reset()
