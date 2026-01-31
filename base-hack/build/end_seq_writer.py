"""Write new end sequence text credits."""

import os
import math
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


class CreditName:
    """Credited user name."""

    def __init__(self, user_name: str, dev_status: str = None, artist: bool = False, composer: bool = False, add_thanks: str = None):
        """Initialize with given data."""
        self.user_name = user_name
        self.dev_status = dev_status
        self.artist = artist
        self.composer = composer
        self.add_thanks = add_thanks


class UserCreditData:
    """Data associated with user credit creation formula."""

    def __init__(self, condition, header: str = "", show_header: bool = True, header_sep: bool = True, sort: bool = True, limit: int = 6):
        """Initialize with given data."""
        self.condition = condition
        self.header = header
        self.show_header = show_header
        self.header_sep = header_sep and show_header
        self.sort = sort
        self.limit = limit


user_credits = [
    CreditName("2dos", dev_status="Main"),
    CreditName("AlmostSeagull", dev_status="Main"),
    CreditName("Ballaam", dev_status="Main"),
    CreditName("Bismuth", dev_status="Main", artist=True, composer=True),
    CreditName("Cfox", dev_status="Main"),
    CreditName("KillKlli", dev_status="Main"),
    CreditName("Lrauq", dev_status="Main"),
    CreditName("ShadowShine57", dev_status="Main"),
    CreditName("TheSoundDefense", dev_status="Main"),
    CreditName("Znernicus", dev_status="Main"),
    CreditName("Aljex", dev_status="Assistant"),
    CreditName("GloriousLiar", dev_status="Assistant"),
    CreditName("JXJacob", dev_status="Assistant", artist=True),
    CreditName("Green Bean", dev_status="Main"),
    CreditName("KnownAsChuck", dev_status="Assistant"),
    CreditName("Mittenz", dev_status="Assistant"),
    CreditName("Naramgamjan", dev_status="Assistant"),
    CreditName("OnlySpaghettiCode", dev_status="Assistant"),
    CreditName("Plessy", dev_status="Assistant"),
    CreditName("Porygone", dev_status="Assistant"),
    CreditName("Rain", dev_status="Assistant"),
    CreditName("Retroben", dev_status="Assistant"),
    CreditName("Snap", dev_status="Assistant"),
    CreditName("UmedMuzl", dev_status="Main"),
    CreditName("Rareware Ltd", add_thanks="Game Developers"),
    CreditName("Nintendo", add_thanks="Game Developers"),
    CreditName("L. Godfrey", add_thanks="Game Developers"),
    CreditName("Isotarge", add_thanks="Untitled"),
    CreditName("SpikeVegeta", add_thanks="Untitled"),
    CreditName("KeiperDontCare", add_thanks="Untitled"),
    CreditName("NintendoSara", add_thanks="Untitled"),
    CreditName("Flargrah", add_thanks="Untitled"),
    CreditName("The Community", add_thanks="Untitled"),
    CreditName("Dahni", artist=True),
    CreditName("Adeleine64DS", add_thanks="Untitled2"),
    CreditName("SirEnobMort", add_thanks="Untitled2"),
    CreditName("SchwartzGandhi", add_thanks="Untitled2"),
    CreditName("gloomy", composer=True),
]


def generateUserCredits():
    """Generate the list of user credits in the correct format."""
    WAS_LEFT = False
    WAS_TOP = False

    conditions = [
        UserCreditData(lambda x: x.dev_status == "Main", "Rando Developers", limit=4),
        UserCreditData(lambda x: x.dev_status == "Assistant", "Assistant Devs"),
        UserCreditData(lambda x: x.artist, "Artists", header_sep=False),
        UserCreditData(lambda x: x.composer, "Composers", header_sep=False),
        UserCreditData(lambda x: x.add_thanks == "Untitled", "Additional Thanks"),
        UserCreditData(lambda x: x.add_thanks == "Game Developers", "Game Developers", header_sep=False, sort=False),
        UserCreditData(lambda x: x.add_thanks == "Untitled2", show_header=False),
    ]
    items = []
    for c in conditions:
        if c.header_sep and c.show_header:
            direction = CreditsDirection.top
            if WAS_TOP:
                direction = CreditsDirection.bottom
            items.append(CreditItem(direction, CreditsType.header, [c.header]))
            WAS_TOP = not WAS_TOP
        user_list = []
        for user in user_credits:
            if c.condition(user):
                user_list.append(user.user_name)
        if c.sort:
            user_list.sort()
        if not c.header_sep and c.show_header:
            user_list = [c.header, " "] + user_list
        # Split the list evenly
        section_count = math.ceil(len(user_list) / c.limit)
        section_size = len(user_list) / section_count
        for x in range(section_count):
            direction = CreditsDirection.left
            if WAS_LEFT:
                direction = CreditsDirection.right
            WAS_LEFT = not WAS_LEFT
            if x == (section_count - 1):
                items.append(CreditItem(direction, CreditsType.normal, user_list))
            else:
                selection = [y for yi, y in enumerate(user_list) if yi < section_size]
                user_list = [y for yi, y in enumerate(user_list) if yi >= section_size]
                items.append(CreditItem(direction, CreditsType.normal, selection))
    return items


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
            "",  # Trapped
            "",  # Deaths
        ],
    ),
]

user_credit_items = generateUserCredits()

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

links = [
    CreditItem(CreditsDirection.top, CreditsType.longheader, ["You have been playing", "DK64 Randomizer", "dk64randomizer.com"]),
    CreditItem(CreditsDirection.bottom, CreditsType.longheader, ["Discord", " ", "discord.dk64randomizer.com"]),
]

end_sequence_cards = []
end_sequence_cards.extend(stats)
end_sequence_cards.extend(user_credit_items)
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
