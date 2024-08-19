"""Write new end sequence text credits."""

import os
from BuildEnums import CreditsDirection, CreditsType

header_length = 0x78
names_length = 0xA0
general_buffer = 0x9A
end_buffer = 0xCC


class CreditItem:
    """Credit Squish Item."""

    def __init__(self, squish_from: CreditsDirection, subtype: CreditsType, text: list):
        """Initialize with given data."""
        self.squish_from = squish_from
        self.duration = names_length
        self.cooldown = general_buffer
        if subtype == CreditsType.header:
            self.duration = header_length
        elif subtype == CreditsType.longheader:
            self.duration = names_length * 2
        self.text = text


stats = [
    CreditItem(CreditsDirection.top, CreditsType.header, [""]),  # Header
    CreditItem(
        CreditsDirection.left,
        CreditsType.longheader,
        [
            "",  # Kong IGT
            "",  # DK Count
            "",  # Diddy Count
            "",  # Lanky Count
            "",  # Tiny Count
            "",  # Chunky Count
        ],
    ),
    CreditItem(
        CreditsDirection.right,
        CreditsType.longheader,
        [
            "",  # Misc
            "",  # Tags
            "",  # Photos
            "",  # Kops
            "",  # Enemies
        ],
    ),
]

main_devs = [
    CreditItem(CreditsDirection.top, CreditsType.header, ["Randomizer Developers"]),
    CreditItem(CreditsDirection.left, CreditsType.normal, ["2dos", "AlmostSeagull", "Ballaam"]),
    CreditItem(CreditsDirection.right, CreditsType.normal, ["Bismuth", "Cfox", "KillKlli"]),
    CreditItem(CreditsDirection.left, CreditsType.normal, ["Lrauq", "ShadowShine57", "The Sound Defense", "Znernicus"]),
]

assistant_devs = [
    CreditItem(CreditsDirection.top, CreditsType.header, ["Assistant Developers"]),
    CreditItem(CreditsDirection.right, CreditsType.normal, ["Aljex", "GloriousLiar", "JXJacob"]),
    CreditItem(CreditsDirection.left, CreditsType.normal, ["Mittenz", "Naramgamjan", "OnlySpaghettiCode"]),
    CreditItem(CreditsDirection.right, CreditsType.normal, ["Plessy", "Rain", "Snap", "UmedMuzl"]),
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

additional_thanks = [
    CreditItem(CreditsDirection.top, CreditsType.header, ["Additional Thanks"]),
    CreditItem(CreditsDirection.left, CreditsType.normal, ["Game Developers", " ", "Rareware Ltd", "Nintendo"]),
    CreditItem(CreditsDirection.bottom, CreditsType.normal, ["Crankys Lab Developer", "Isotarge"]),
    CreditItem(CreditsDirection.right, CreditsType.normal, ["SpikeVegeta", "KeiperDontCare", "NintendoSara", "Flargrah"]),
    CreditItem(CreditsDirection.left, CreditsType.normal, ["Beta Testers", "Dev Branch Testers"]),
]

links = [
    CreditItem(CreditsDirection.top, CreditsType.longheader, ["You have been playing", "DK64 Randomizer", "dk64randomizer.com"]),
    CreditItem(CreditsDirection.bottom, CreditsType.longheader, ["Discord", " ", "discord.dk64randomizer.com"]),
]

end_sequence_cards = []
end_sequence_cards.extend(stats)
end_sequence_cards.extend(main_devs)
end_sequence_cards.extend(assistant_devs)

end_sequence_cards.extend(additional_thanks)
end_sequence_cards.extend(links)


def checkSequenceValidity():
    """Check if the end sequence credits are valid."""
    if len(end_sequence_cards) > 21:
        raise Exception("Too many cards")


def createTextFile(directory):
    """Create the text file associated with end sequence."""
    if not os.path.exists(directory):
        os.mkdir(directory)
    checkSequenceValidity()
    with open(f"{directory}/credits.bin", "wb") as fh:
        for card in end_sequence_cards:
            for item in card.text:
                if len(item) > 0:
                    new_item = item.upper() + "\n"
                    fh.write(new_item.encode("ascii"))
        terminator = "*\n"
        fh.write(terminator.encode("ascii"))


def createSquishFile(directory):
    """Create the squish data associated with end sequence."""
    checkSequenceValidity()
    with open(f"{directory}/squish.bin", "wb") as fh:
        for card in end_sequence_cards:
            fh.write(card.duration.to_bytes(2, "big"))
            fh.write(card.cooldown.to_bytes(2, "big"))
            fh.write(int(card.squish_from).to_bytes(1, "big"))
            fh.write(len(card.text).to_bytes(1, "big"))
        term = []
        for x in range(6):
            term.append(0xFF)
        fh.write(bytearray(term))
