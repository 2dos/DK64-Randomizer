"""A quick script to simulate how hints render, making it easier to debug hint render issues."""


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
    input_copy = input.encode()
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
    line_starts = [0] * 3
    line_length = 0
    line_length_global = 0
    safe_haven = 0
    line_index = 0
    color_index = 0
    for xi in range(str_len):
        char_val = input_copy[xi]
        if char_val <= 0x10:
            if char_val >= 0x4:
                color_index = (char_val - 3) ^ color_index
                line_length_global += 1
            continue
        elif char_val == 0x20:
            safe_haven = xi
            line_length += 1
            line_length_global += 1
            continue
        setCharacterColor(line_length_global, color_index)
        if line_length > SPLIT_STRING_LINE_LIMIT:
            line_index += 1
            if line_index < 3:
                line_starts[line_index] = safe_haven + 1
            string_copy[safe_haven] = 0
            start_of_str = line_starts[line_index - 1]
            line_length = 0
            line_length_global = 0
            simulatedPrint(string_copy[start_of_str:])
            if line_index == 3:
                return
            continue
        line_length += 1
        line_length_global += 1
    simulatedPrint(string_copy)


test_string = "SOMETHING IN THE \x0AIGLOO AREA\x0A IS ON THE PATH TO \x04KEY 4\x04."
print("WORKING CASE:")
drawSplitString(test_string)
wipeColors()
print("TEST CASE:")
drawSplitString_test(test_string)
