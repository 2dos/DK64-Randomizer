"""Update wrinkly hints compressed file."""
import random
from io import BytesIO

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.WrinklyHints import HintLocation, hints
from randomizer.Patching.Lib import grabText, writeText
from randomizer.Patching.Patcher import ROM, LocalROM


def writeWrinklyHints(file_start_offset, text):
    """Write the text to ROM."""
    LocalROM().seek(file_start_offset)
    LocalROM().writeMultipleBytes(len(text), 1)
    position = 0
    offset = 1
    for textbox in text:
        LocalROM().seek(file_start_offset + offset)
        LocalROM().writeMultipleBytes(1, 1)
        LocalROM().seek(file_start_offset + offset + 1)
        LocalROM().writeMultipleBytes(1, 1)
        LocalROM().seek(file_start_offset + offset + 2)
        LocalROM().writeMultipleBytes(len(textbox), 1)
        offset += 3
        for string in textbox:
            LocalROM().seek(file_start_offset + offset)
            LocalROM().writeMultipleBytes(position, 4)
            LocalROM().seek(file_start_offset + offset + 4)
            LocalROM().writeMultipleBytes(len(string), 2)
            LocalROM().seek(file_start_offset + offset + 6)
            LocalROM().writeMultipleBytes(0, 2)
            offset += 8
            position += len(string)
        LocalROM().seek(file_start_offset + offset)
        LocalROM().writeMultipleBytes(0, 4)
        offset += 4
    LocalROM().seek(file_start_offset + offset)
    LocalROM().writeMultipleBytes(position, 2)
    offset += 2
    for textbox in text:
        for string in textbox:
            for x in range(len(string)):
                LocalROM().seek(file_start_offset + offset + x)
                LocalROM().writeMultipleBytes(int.from_bytes(string[x].encode("ascii"), "big"), 1)
            offset += len(string)


def UpdateHint(WrinklyHint: HintLocation, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    if len(message) <= 914:
        # We're safely below the character limit
        WrinklyHint.hint = message
        return True
    else:
        raise Exception("Hint message is longer than allowed.")
    return False


def updateRandomHint(message: str, kongs_req=[], keywords=[], levels=[]):
    """Update a random hint with the string specifed.

    Args:
        message (str): Hint message to write.
    """
    hint_pool = []
    for x in range(len(hints)):
        if hints[x].hint == "" and hints[x].kong in kongs_req and hints[x].level in levels:
            is_banned = False
            for banned in hints[x].banned_keywords:
                if banned in keywords:
                    is_banned = True
            if not is_banned:
                hint_pool.append(x)
    if len(hint_pool) > 0:
        selected = random.choice(hint_pool)
        return UpdateHint(hints[selected], message)
    return False


def PushHints(spoiler):
    """Update the ROM with all hints."""
    hint_arr = []
    for replacement_hint in spoiler.hint_list.values():
        if replacement_hint == "":
            replacement_hint = "PLACEHOLDER HINT"
        hint_arr.append([replacement_hint.upper()])
    writeWrinklyHints(js.pointer_addresses[12]["entries"][41]["pointing_to"], hint_arr)
    spoiler.hint_list.pop("First Time Talk")  # The FTT needs to be written to the ROM but should not be found in the spoiler log


def wipeHints():
    """Wipe the hint block."""
    for x in range(len(hints)):
        if hints[x].kong != Kongs.any:
            hints[x].hint = ""


def replaceIngameText(spoiler):
    """Replace text in-game with defined modifications."""
    for file_index in spoiler.text_changes:
        old_text = grabText(file_index)
        modification_data = spoiler.text_changes[file_index]
        for mod in modification_data:
            if mod["mode"] == "replace":
                old_textbox = old_text[mod["textbox_index"]]
                new_textbox = []
                for seg in old_textbox:
                    text = []
                    for line in seg["text"]:
                        new_line = line.replace(mod["search"], mod["target"])
                        text.append(new_line)
                    new_textbox.append({"text": text.copy()})
                old_text[mod["textbox_index"]] = new_textbox.copy()
            elif mod["mode"] == "replace_whole":
                # print(mod["target"])
                old_text[mod["textbox_index"]] = ({"text": [mod["target"]]},)
        writeText(file_index, old_text)
