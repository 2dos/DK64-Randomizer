"""Write new end sequence text credits."""
import os
import sys

header_length = 0x78
names_length = 0xA0
general_buffer = 0x9A
end_buffer = 0xCC

end_sequence_cards = [
    {
        "squish": {
            "from": "top",
            "duration": header_length,
            "cooldown": general_buffer,
        },
        "text": [
            "Developers",
        ],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "2dos",
            "Ballaam",
        ],
    },
    {
        "squish": {
            "from": "right",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": ["Bismuth", "Cfox"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "GloriousLiar",
            "KillKlli",
        ],
    },
    {
        "squish": {
            "from": "right",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": ["Mittenz", "Naramgamjan"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": end_buffer,
        },
        "text": ["Rain", "ShadowShine57", "Znernicus"],
    },
    {
        "squish": {
            "from": "top",
            "duration": header_length,
            "cooldown": general_buffer,
        },
        "text": ["Beta Testers"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "Adam Whitmore",
            "Auphonium",
            "CandyBoots",
        ],
    },
    {
        "squish": {
            "from": "top",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "ChelseyXLynn",
            "ChristianVega64",
            "Connor75",
        ],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "CornCobx0",
            "Fuzzyness",
            "KaptainKohl",
        ],
    },
    {
        "squish": {
            "from": "top",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": ["KiwiKiller67", "Nukkuler"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "Obiyo",
            "Revven",
        ],
    },
    {
        "squish": {
            "from": "bottom",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": ["Riley", "SirSmackStrikesBack"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "UsedPizza",
            "VidyaJames",
        ],
    },
    {
        "squish": {
            "from": "right",
            "duration": names_length,
            "cooldown": end_buffer,
        },
        "text": ["Wex", "Zorulda"],
    },
    {
        "squish": {
            "from": "top",
            "duration": header_length,
            "cooldown": general_buffer,
        },
        "text": ["Additional Thanks"],
    },
    {
        "squish": {
            "from": "left",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": [
            "Game Developers",
            " ",
            "Rareware Ltd",
            "Nintendo",
        ],
    },
    {
        "squish": {
            "from": "bottom",
            "duration": names_length,
            "cooldown": general_buffer,
        },
        "text": ["Crankys Lab Developer", "Isotarge"],
    },
    {
        "squish": {
            "from": "top",
            "duration": names_length * 2,
            "cooldown": general_buffer,
        },
        "text": ["You have been playing", "DK64 Randomizer", "dk64randomizer.com"],
    },
    {
        "squish": {
            "from": "bottom",
            "duration": names_length * 2,
            "cooldown": general_buffer,
        },
        "text": ["Discord", " ", "discord.dk64randomizer.com"],
    },
]


def createTextFile(directory):
    """Create the text file associated with end sequence."""
    if not os.path.exists(directory):
        os.mkdir(directory)
    if len(end_sequence_cards) > 21:
        print("ERROR: Too many cards")
        sys.exit()
    with open(f"{directory}/credits.bin", "wb") as fh:
        for card in end_sequence_cards:
            for item in card["text"]:
                new_item = item.upper() + "\n"
                fh.write(new_item.encode("ascii"))
        terminator = "*\n"
        fh.write(terminator.encode("ascii"))


def createSquishFile(directory):
    """Create the squish data associated with end sequence."""
    if len(end_sequence_cards) > 21:
        print("ERROR: Too many cards")
        sys.exit()
    directions = ["top", "left", "bottom", "right"]
    with open(f"{directory}/squish.bin", "wb") as fh:
        for card in end_sequence_cards:
            direction_index = 0
            if card["squish"]["from"] in directions:
                direction_index = directions.index(card["squish"]["from"])
            fh.write(card["squish"]["duration"].to_bytes(2, "big"))
            fh.write(card["squish"]["cooldown"].to_bytes(2, "big"))
            fh.write(direction_index.to_bytes(1, "big"))
            fh.write(len(card["text"]).to_bytes(1, "big"))
        term = []
        for x in range(6):
            term.append(0xFF)
        fh.write(bytearray(term))
