"""Patch some common text."""


# def patchDolbyText(filename):
#     """Patch the dolby text data."""
#     with open(filename, "r+b") as fh:
#         fh.seek(0x30)
#         fh.write("PRESENTED IN".encode("ascii"))  # Originally: PRESENTED IN
#         fh.seek(0x3C)
#         fh.write("BY THE DK64 RANDOMIZER DEV TEAM\0".encode("ascii"))  # Originally: DOLBY AND THE DOUBLE-D SYMBOL ARE
#         fh.seek(0x5D)
#         fh.write("DK64RANDOMIZER.COM\0".encode("ascii"))  # Originally: TRADEMARKS OF DOLBY LABORATORIES.

from text_encoder import writeText

writeText("dolby_text.bin",
	[
		["DONKEY KONG 64 RANDOMIZER"],
		["DEVELOPERS - 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, BISMUTH"],
		["DK64RANDOMIZER.COM"]
	]
)