"""Create the disco donkey model."""

from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, getBonusSkinOffset

DARKER_SKIN = 0xEB4
PURPLE_SUIT = getBonusSkinOffset(ExtraTextures.DiscoDonkShirt)
PINK_HANDS = getBonusSkinOffset(ExtraTextures.DiscoDonkGlove)

with open(ROMName, "rb") as rom:
    donkey_model = ROMPointerFile(rom, TableNames.ActorGeometry, 3).grabFile(rom)
    with open("disco_donkey.bin", "wb") as fh:
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
