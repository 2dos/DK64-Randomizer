from BuildClasses import ROMPointerFile
from BuildEnums import TableNames, ExtraTextures
from BuildLib import ROMName, getBonusSkinOffset

# DK
# 0xe64 - Skin
# 0xe91 - Mouth
# 0xe6a - Ear?
# 0xe6b - Pink?
# 0xd000000 - All Fur (Dyn Tex)
# 0xc000000
# 0xe92 - ?
# 0xe8d - DK Logo
# 0xe000000
# 0xe65 - Fur?
# 0xe84 - Not genned
# 0xe83 - Not Genned
# 0x130 - Green Leaf?

# Chunky
# 0xe64
# 0xe91
# 0xeb4 - Dark Skin
# 0xe6b
# 0xc000000
# 0xe66
# 0xeb5
# 0xe84
# 0xe83
# 0x130
# 0xe000000
# 0xd000000
# 0xead
# 0xeb8
# 0xebd
# 0xebe

# Disco Chunky
# 0xe64
# 0xe91
# 0xeb4
# 0xe6b
# 0xc000000
# 0xec2 - Hands
# 0xec1 - Main Suit
# 0xe84
# 0xe83
# 0x130
# 0xead
# 0xec0 - Belt
# 0xebd
# 0xebe

# DK: 8D862E
# Disco Chunk: 8EC3E8

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