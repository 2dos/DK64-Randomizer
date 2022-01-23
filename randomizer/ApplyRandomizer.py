"""Apply Patch data to the ROM."""
import codecs
import json
import pickle

from randomizer.DKTV import randomize_dktv
from randomizer.MusicRando import randomize_music
from randomizer.Patcher import ROM
# from randomizer.Spoiler import Spoiler
from ui.progress_bar import ProgressBar


def patching_response(responded_data):
    """Response data from the background task.

    Args:
        responded_data (str): Pickled data (or json)
    """
    try:
        loaded_data = json.loads(responded_data)
        if loaded_data.get("error"):
            error = loaded_data.get("error")
            ProgressBar().set_class("bg-danger")
            ProgressBar().update_progress(10, f"Error: {error}")
            ProgressBar().reset()
            return None
    except Exception:
        pass

    ProgressBar().update_progress(5, "Applying Patches")
    spoiler= pickle.loads(codecs.decode(responded_data.encode(), "base64"))
    # Make sure we re-load the seed id
    spoiler.settings.set_seed()
    settings = {}
    # Starting index for our settings
    sav = 0x1FED020

    if spoiler.settings.shuffle_levels:
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

    order = 0
    for count in spoiler.settings.BossBananas:
        ROM().seek(sav + 0x008 + order)
        ROM().write(count)
        order += 2

    order = 0
    for count in spoiler.settings.EntryGBs:
        ROM().seek(sav + 0x016 + order)
        ROM().write(count)
        order += 1

    # TODO: Dummy function
    if settings.get("key_flags"):
        order = 0
        for level in loaded_data:
            ROM().seek(sav + 0x01E + order)
            ROM().write(level)
            order += 2
    else:
        ROM().seek(sav + 0x01E + 0)
        ROM().writeMultipleBytes(0x1A, 2)
        ROM().seek(sav + 0x01E + 2)
        ROM().writeMultipleBytes(0x4A, 2)

        ROM().seek(sav + 0x01E + 4)
        ROM().writeMultipleBytes(0x8A, 2)

        ROM().seek(sav + 0x01E + 6)
        ROM().writeMultipleBytes(0xA8, 2)

        ROM().seek(sav + 0x01E + 8)
        ROM().writeMultipleBytes(0xEC, 2)

        ROM().seek(sav + 0x01E + 10)
        ROM().writeMultipleBytes(0x124, 2)

        ROM().seek(sav + 0x01E + 12)
        ROM().writeMultipleBytes(0x13D, 2)

    if spoiler.settings.unlock_all_kongs:
        ROM().seek(sav + 0x02C)
        ROM().write(1)

    if spoiler.settings.unlock_all_moves:
        ROM().seek(sav + 0x02D)
        ROM().write(1)

    if spoiler.settings.fast_start_beginning_of_game:
        ROM().seek(sav + 0x02E)
        ROM().write(1)

    if spoiler.settings.unlock_fairy_shockwave:
        ROM().seek(sav + 0x02F)
        ROM().write(1)

    if spoiler.settings.enable_tag_anywhere:
        ROM().seek(sav + 0x030)
        ROM().write(1)

    if spoiler.settings.fast_start_hideout_helm:
        ROM().seek(sav + 0x031)
        ROM().write(1)

    if spoiler.settings.crown_door_open:
        ROM().seek(sav + 0x032)
        ROM().write(1)

    if spoiler.settings.coin_door_open:
        ROM().seek(sav + 0x033)
        ROM().write(1)

    if spoiler.settings.quality_of_life:
        ROM().seek(sav + 0x034)
        ROM().write(1)

    randomize_dktv()
    randomize_music(spoiler.settings)
    ProgressBar().update_progress(10, "Seed Generated.")
    ROM().fixSecurityValue()
    ROM().save(f"dk64-{spoiler.settings.seed}.z64")
    ProgressBar().reset()
