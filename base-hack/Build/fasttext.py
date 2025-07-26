"""Conversion functions to a custom file format which is used for fast simple text lookup."""

MAX_LINES = 3
MAX_LINE_LENGTH = 400
CHAR_KERNING = 0
SPACE_KERNING = 5
DEBUG = False
HINT_CHARACTER_LIMIT = 125
CHAR_WIDTH = {
    "A": 10,
    "B": 9,
    "C": 9,
    "D": 9,
    "E": 8,
    "F": 8,
    "G": 11,
    "H": 9,
    "I": 4,
    "J": 9,
    "K": 9,
    "L": 8,
    "M": 11,
    "N": 9,
    "O": 10,
    "P": 8,
    "Q": 11,
    "R": 9,
    "S": 10,
    "T": 9,
    "U": 9,
    "V": 9,
    "W": 12,
    "X": 8,
    "Y": 9,
    "Z": 8,
    ".": 5,
    ",": 5,
    "!": 4,
    "?": 7,
    ":": 5,
    ";": 5,
    "'": 5,
    "-": 9,
    "&": 11,
    "1": 6,
    "2": 9,
    "3": 9,
    "4": 10,
    "5": 10,
    "6": 9,
    "7": 9,
    "8": 10,
    "9": 10,
    "0": 10,
    "(": 5,
    ")": 5,
    "%": 12,
}
CONTROL_CHARACTERS = [
    "\x04",
    "\x05",
    "\x06",
    "\x07",
    "\x08",
    "\x09",
    "\x0a",
    "\x0b",
    "\x0c",
    "\x0d",
]


def getActiveEffectStr(active_effects: list[str], ending: bool) -> str:
    """Get the start or end of a string to properly account for the active effect list."""
    effects_copy = active_effects[:]
    if ending:
        effects_copy.reverse()  # If ending a string, remove the effects in reverse order to how they were applied
    return "".join(effects_copy)


def splitText(text: str, truncate_split: bool) -> str:
    """Split a text entry into lines."""
    lines = []
    line_index = 0
    line_length = 0
    line_text = ""
    text = text.strip(" ")  # Filter out any trailing whitespaces
    most_recent_word = ""
    word_length = 0
    displayed_characters = 0
    active_effects = []
    if DEBUG:
        print("----------")
        print(text)
    while line_index < MAX_LINES:
        if len(text) == 0:
            if len(most_recent_word) > 0:
                line_text += most_recent_word
                line_text = line_text.strip(" ")
                line_text += getActiveEffectStr(active_effects, True)
                lines.append(line_text)
            break
        elif line_length == 0:
            # Start of a string
            line_text += getActiveEffectStr(active_effects, False)
        if line_length == 0 and DEBUG:
            print("Starting new line")
        char = text[0]
        add_word = False
        width = 0
        if char == " ":
            width = SPACE_KERNING
            add_word = True
        elif char in CONTROL_CHARACTERS:
            width = CHAR_KERNING
            if char in active_effects:
                active_effects.remove(char)
            else:
                active_effects.append(char)
        else:
            char_width = CHAR_WIDTH.get(char, 0)
            if char_width:
                displayed_characters += 1
            width = CHAR_KERNING + char_width
        if displayed_characters > HINT_CHARACTER_LIMIT and len(text) > 1 and truncate_split:
            line_text += most_recent_word
            line_text = line_text.strip(" ")
            if len(line_text) < 3:
                line_text = "..."
            else:
                line_text = line_text[:3].strip(" ") + "..."
            line_text += getActiveEffectStr(active_effects, True)
            lines.append(line_text)
            break
        word_length += width
        line_length += width
        most_recent_word += text[0]
        if add_word:
            line_text += most_recent_word
            if DEBUG:
                print("Parsed new world", most_recent_word, "|", line_text)
            # Reset
            word_length = 0
            most_recent_word = ""
        text = text[1:]
        if line_length > MAX_LINE_LENGTH and truncate_split:
            line_index += 1
            line_length = 0
            if line_index == MAX_LINES:
                line_text = line_text.strip(" ") + "..."
            line_text = line_text.strip(" ")
            line_text += getActiveEffectStr(active_effects, True)
            lines.append(line_text)
            if DEBUG:
                print("Next line: ", line_text, "|", most_recent_word)
            line_text = ""
    base_text = "\x0f".join(lines)
    return f"{base_text}\x00"


def fastTextConv(input_data: list, file_name: str, truncate_split: bool = True):
    """Conversion function."""
    bad_chars = ["\x00, \x0f"]
    entries = []
    for entry in input_data:
        text = ""
        for obj in entry:
            if "text" in obj:
                for line in obj["text"]:
                    filtered_line = "".join(c for c in line if c not in bad_chars)
                    text += f"{filtered_line} "
        entries.append(splitText(text, truncate_split))
    with open(file_name, "w") as fh:
        fh.write("".join(entries))
