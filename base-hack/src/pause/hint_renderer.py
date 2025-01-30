"""A quick script to simulate how hints render, making it easier to debug hint render issues."""

# INFRASTRUCTURE

# - The code written by me in `drawSplitString()` takes a string, goes through each character
# and if the character is a color control character, then it filters it out and sets all subsequent
# characters to the value of that color until it reaches another control character of the same value,
# like a toggle switch.
# - It splits the string into lines of at most 50 characters, determining the end of a line that would
# exceed 50 characters as the last space of the line before 50 characters.

# CHALLENGE RULES

# - The color control characters must be filtered out with the code sent to `simulatedPrint`,
# with the color of each character in the line being set with `setCharacterColor`. The index passed
# into `setCharacterColor` is the index of the character in the string which does **NOT** have the
# color control characters

# - Don't use text manipulation functions like `.split()`, `.join()`, `.trim()`. The intention is that
# the most optimal function will be able to be converted into C that will interface with those games,
# and the game does not have those functions in place to use. The method chosen in my original function
# is to copy everything after the control character to 1 space earlier. However, if you think there's
# something different which would be more efficient and be possible in C, go for it.

# - Don't alter `wipeColors`, `setCharacterColor` or `simulatedPrint`. These should be treated as
# library functions which we're using to interface with the game

# - Write your new function into `drawSplitString_test`. I've included a bunch of safety features at the
# start of the function that you should avoid modifying, as they protect against hints that are too long
# and memory buffer overflow


# Coloring
class bcolors:
    """bcolors class."""

    WHITE = "\033[00m"
    ORANGE = "\033[33m"
    RED = "\033[31m"
    BLUE = "\033[34m"
    PURPLE = "\033[35m"
    LIGHTGREEN = "\033[92m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    PALERED = "\033[91m"
    PALEBLUE = "\033[94m"
    VIBRANTGREEN = "\033[92m"


cindex_table = [
    bcolors.WHITE,
    bcolors.ORANGE,
    bcolors.RED,
    bcolors.BLUE,
    bcolors.PURPLE,
    bcolors.LIGHTGREEN,
    bcolors.MAGENTA,
    bcolors.CYAN,
    bcolors.PALERED,
    bcolors.PALEBLUE,
    bcolors.VIBRANTGREEN,
]

# Consts
ELLIPSIS_CUTOFF = 123
STRING_MAX_SIZE = 128
SPLIT_STRING_LINE_LIMIT = 50

# Vars
string_copy = bytes(bytearray([0] * STRING_MAX_SIZE))
char_colors = [0] * 0x40


def simulatedPrint(text: bytearray):
    """Rough simulation of the game's draw function to handle text parsing."""
    string_end = 0
    while True:
        if text[string_end] == 0:
            break
        string_end += 1
    str_copy = text[:string_end].decode()
    str_elements = []
    for xi, x in enumerate(str_copy):
        if char_colors[xi] == 0:
            str_elements.append(x)
        else:
            selected_color = char_colors[xi]
            str_elements.append(f"{cindex_table[selected_color]}{x}{cindex_table[0]}")
    print("".join(str_elements))


def setCharacterColor(pos: int, color_index: int):
    """Set the character color value."""
    global char_colors

    char_colors[pos] = color_index


def wipeColors():
    """Wipe color list."""
    global char_colors
    char_colors = [0] * 0x40


def drawSplitString(input: str):
    """Simulate of drawSplitString in the C Code."""
    global string_copy

    str_len = len(input)
    trigger_ellipsis = False
    if str_len > ELLIPSIS_CUTOFF:
        str_len = ELLIPSIS_CUTOFF
        trigger_ellipsis = True
    string_copy_ref = 0
    string_copy = bytearray([0] * STRING_MAX_SIZE)  # Wipe memory
    b = bytearray()
    b.extend(map(ord, input))
    for xi, x in enumerate(b):
        string_copy[xi] = x
    if trigger_ellipsis:
        for x in range(3):
            string_copy[ELLIPSIS_CUTOFF + x] = 0x2E
    string_copy[126] = 0
    string_copy[127] = 0
    # Loop defs
    header = 0
    last_safe = 0
    line_count = 0
    color_index = 0
    force_split = False
    while True:
        reference_character = string_copy[string_copy_ref + header]
        is_control = False
        if reference_character == 0:  # Null Terminator
            simulatedPrint(string_copy[string_copy_ref:])
            return
        elif reference_character == 0x20:  # Space
            last_safe = header
            seg_addition = 1
            while True:
                ref_seg_character = string_copy[string_copy_ref + header + seg_addition]
                if ref_seg_character in (0, 0x20):
                    break
                else:
                    seg_addition += 1
            if (header + seg_addition) > SPLIT_STRING_LINE_LIMIT:
                force_split = True
        elif (reference_character > 0) and (reference_character <= 0x10):
            # Control Character
            if (reference_character >= 4) and (reference_character <= 0xD):
                # Color Control Character
                temp_color = reference_character - 3
                if temp_color == color_index:
                    color_index = 0
                else:
                    color_index = temp_color
            is_control = True
            end = STRING_MAX_SIZE - 1
            size = end - (string_copy_ref + header + 1)
            # Simulated memcpy
            copied = string_copy[string_copy_ref + header + 1 :]
            for x in range(size):
                string_copy[string_copy_ref + header + x] = copied[x]
        setCharacterColor(header, color_index)
        if not is_control:
            if (header > SPLIT_STRING_LINE_LIMIT) or force_split:
                string_copy[string_copy_ref + last_safe] = 0
                simulatedPrint(string_copy[string_copy_ref:])
                line_count += 1
                if line_count == 3:
                    return
                string_copy_ref += last_safe + 1
                header = 0
                last_safe = 0
                force_split = False
            else:
                header += 1


def drawSplitString_test(input: str):
    """Test case to see whether a more efficient algorithm works."""
    global string_copy

    str_len = len(input)
    trigger_ellipsis = False
    if str_len > ELLIPSIS_CUTOFF:
        str_len = ELLIPSIS_CUTOFF
        trigger_ellipsis = True
    string_copy_ref = 0
    string_copy = bytearray([0] * STRING_MAX_SIZE)  # Wipe memory
    b = bytearray()
    b.extend(map(ord, input))
    for xi, x in enumerate(b):
        string_copy[xi] = x
    if trigger_ellipsis:
        for x in range(3):
            string_copy[ELLIPSIS_CUTOFF + x] = 0x2E
    string_copy[126] = 0
    string_copy[127] = 0
    # Loop defs
    # Put your code here to handle string_copy (don't handle "input")


test_string = "SOMETHING IN THE \x0aIGLOO AREA\x0a IS ON THE PATH TO \x04KEY 4\x04."
print("WORKING CASE:")
drawSplitString(test_string)
wipeColors()
print("TEST CASE:")
drawSplitString_test(test_string)
