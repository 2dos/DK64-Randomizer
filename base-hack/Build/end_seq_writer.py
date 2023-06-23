"""Write new end sequence text credits."""
import os
import sys

import requests as rs

is_v2_release = False
csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTjqxasaI40I2zf3RG9_7Vv-H1grc2JMhy_C08SZkW9MFApNaZ8ARnUDRfA0QrgCi874s9efWxhy6mW/pub?gid=1075755893&single=true&output=csv"
basher_names = []
if is_v2_release:
    try:
        res = rs.get(url=csv_url)
        txt = res.content.decode("ascii")
        bigbugbashers = txt.split("\r\n")[1:]
        basher_names = []
        for b in bigbugbashers:
            if len(b.split(",")[1]) > 0:
                basher_names.append(b.split(",")[1])
    except rs.exceptions.HTTPError as err:
        raise SystemExit(err)


header_length = 0x78
names_length = 0xA0
general_buffer = 0x9A
end_buffer = 0xCC


class CreditItem:
    """Credit Squish Item."""

    def __init__(self, squish_from, subtype, text):
        """Initialize with given data."""
        self.squish_from = squish_from
        self.duration = names_length
        self.cooldown = general_buffer
        if subtype == "header":
            self.duration = header_length
        elif subtype == "longheader":
            self.duration = names_length * 2
        self.text = text


main_devs = [
    CreditItem("top", "header", ["Randomizer Developers"]),
    CreditItem("left", "normal", ["2dos", "AlmostSeagull", "Ballaam"]),
    CreditItem("right", "normal", ["Bismuth", "Cfox", "KillKlli"]),
    CreditItem("left", "normal", ["Lrauq", "ShadowShine57", "Znernicus"]),
]

assistant_devs = [
    CreditItem("top", "header", ["Assistant Developers"]),
    CreditItem("right", "normal", ["Aljex", "GloriousLiar", "JXJacob"]),
    CreditItem("left", "normal", ["Mittenz", "Naramgamjan", "OnlySpaghettiCode"]),
    CreditItem("right", "normal", ["Plessy", "Rain", "The Sound Defense"]),
]

# BETA TESTERS
# Adam Whitmore
# Auphonium
# Candy Boots
# ChelseyXLynn
# ChristianVega64
# Connor75
# CornCobX0
# Fuzzyness
# KaptainKohl
# Kiwikiller67
# Nukkuler
# Obiyo
# Revven
# Riley
# SirSmackStrikesBack
# UsedPizza
# VidyaJames
# Wex_AZ
# Zorulda

bbb_contest = [CreditItem("top", "header", ["Big Bug Bashers"]), CreditItem("right", "normal", basher_names)]

additional_thanks = [
    CreditItem("top", "header", ["Additional Thanks"]),
    CreditItem("left", "normal", ["Game Developers", " ", "Rareware Ltd", "Nintendo"]),
    CreditItem("bottom", "normal", ["Crankys Lab Developer", "Isotarge"]),
    CreditItem("right", "normal", ["SpikeVegeta", "KeiperDontCare"]),
    CreditItem("left", "normal", ["Beta Testers", "Dev Branch Testers"]),
]

links = [CreditItem("top", "longheader", ["You have been playing", "DK64 Randomizer", "dk64randomizer.com"]), CreditItem("bottom", "longheader", ["Discord", " ", "discord.dk64randomizer.com"])]

end_sequence_cards = []
end_sequence_cards.extend(main_devs)
end_sequence_cards.extend(assistant_devs)

if len(basher_names) > 0 and is_v2_release:
    end_sequence_cards.extend(bbb_contest)
end_sequence_cards.extend(additional_thanks)
end_sequence_cards.extend(links)


def createTextFile(directory):
    """Create the text file associated with end sequence."""
    if not os.path.exists(directory):
        os.mkdir(directory)
    if len(end_sequence_cards) > 21:
        print("ERROR: Too many cards")
        sys.exit()
    with open(f"{directory}/credits.bin", "wb") as fh:
        for card in end_sequence_cards:
            for item in card.text:
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
            if card.squish_from in directions:
                direction_index = directions.index(card.squish_from)
            fh.write(card.duration.to_bytes(2, "big"))
            fh.write(card.cooldown.to_bytes(2, "big"))
            fh.write(direction_index.to_bytes(1, "big"))
            fh.write(len(card.text).to_bytes(1, "big"))
        term = []
        for x in range(6):
            term.append(0xFF)
        fh.write(bytearray(term))
