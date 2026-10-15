"""Create the disco donkey model."""

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, getBonusSkinOffset

DARKER_SKIN = 0xEB4
GREY_SKIN = getBonusSkinOffset(ExtraTextures.KongBananzaGrey)
GOLD_SKIN = 0xEC0
BLACK_SKIN = getBonusSkinOffset(ExtraTextures.KongBananzaBlack)
PURPLE_SUIT = getBonusSkinOffset(ExtraTextures.DiscoDonkShirt)
PINK_HANDS = getBonusSkinOffset(ExtraTextures.DiscoDonkGlove)

with open(ROMName, "rb") as rom:
    donkey_model = ROMPointerFile(rom, TableNames.ActorGeometry, 3).grabFile(rom)
    with open("disco_donkey.bin", "wb") as fh:
        fh.write(donkey_model)
    with open("bananza_donkey.bin", "wb") as fh:
        fh.write(donkey_model)
with open("disco_donkey.bin", "r+b") as mdl:
    # Changing fur
    mdl.seek(0x4324)
    mdl.write(DARKER_SKIN.to_bytes(4, "big"))  # Hair
    mdl.seek(0x457C)
    mdl.write(DARKER_SKIN.to_bytes(4, "big"))
    mdl.seek(0x4AB4)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x4CD4)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x4DAC)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x4DAC)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5074)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5704)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5914)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5B94)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5D84)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    # Changing Skin
    mdl.seek(0x489C)
    mdl.write(PINK_HANDS.to_bytes(4, "big"))
    mdl.seek(0x49E4)
    mdl.write(PINK_HANDS.to_bytes(4, "big"))
    mdl.seek(0x4E1C)
    mdl.write(PINK_HANDS.to_bytes(4, "big"))
    mdl.seek(0x4F74)
    mdl.write(PINK_HANDS.to_bytes(4, "big"))
    mdl.seek(0x51B4)
    mdl.write(PINK_HANDS.to_bytes(4, "big"))
    mdl.seek(0x4C64)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x4D44)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5564)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    mdl.seek(0x5D3C)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
    # Change Tie Loop
    mdl.seek(0x47EC)
    mdl.write(PURPLE_SUIT.to_bytes(4, "big"))
with open("bananza_donkey.bin", "r+b") as mdl:
    for x in (0x3D8C, 0x3F74, 0x4044, 0x489C, 0x49E4, 0x4C64, 0x4D44, 0x4E1C, 0x4F74, 0x51B4, 0x5564, 0x57FC, 0x5A7C, 0x5D3C):
        mdl.seek(x)
        mdl.write(GREY_SKIN.to_bytes(4, "big"))
    for x in (0x4324, 0x457C):
        mdl.seek(x)
        mdl.write(GOLD_SKIN.to_bytes(4, "big"))
    for x in (0x4AB4, 0x4CD4, 0x4DAC, 0x4DAC, 0x5074, 0x5704, 0x5914, 0x5B94, 0x5D84):
        mdl.seek(x)
        mdl.write(BLACK_SKIN.to_bytes(4, "big"))