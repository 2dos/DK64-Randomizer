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

# move_hints = [
#     {
#         "move": "Baboon Blast",
#         "kong": "Donkey",
#         "cranky": "THIS ONE WILL MAKE YOU BREAK THE DONKEY AIR-SPEED RECORD.",
#         "funky": " WHICH WILL ENABLE YOU TO LAUNCH INTO THE STRATOSPHERE.",
#         "candy": "I CAN HELP YOU MOVE UP INTO THE SKY."
#     },
#     {
#         "move": "Strong Kong",
#         "kong": "Donkey",
#         "cranky": "YOU MAY BE BIGGER AND FASTER, BUT THIS WILL HELP YOU FULFILL THE FINAL PART OF YOUR VERSE.",
#         "funky": ". PERHAPS WITH THIS YOU'LL GET MUSCLES AS BIG AS MINE.",
#         "candy": "I WILL HELP YOU WALK WITH SPARKLES."
#     },
#     {
#         "move": "Gorilla Grab",
#         "kong": "Donkey",
#         "cranky": "THIS ONE WILL ALLOW YOU TO TIME TRAVEL TO 1981.",
#         "funky": " WHICH WILL HELP YOU GO BACK TO THEM GOOD OLD DAYS.",
#         "candy": "I WILL HELP YOU OPEN UP YOUR MINECART RIDE."
#     },
#     {
#         "move": "Chimpy Charge",
#         "kong": "Diddy",
#         "cranky": "BETTER GET THAT CRANIUM TOUGHENED IF YOU PURCHASE THIS MOVE.",
#         "funky": ". GOTTA WARN YOU, ALL THAT HEAD BASHING WILL LOSE YOU A FEW IQ POINTS.",
#         "candy": "I WILL HELP YOU CHARGE INTO SWITCHES."
#     },
#     {
#     	"move": "Rocketbarrel",
#     	"kong": "Diddy",
#     	"cranky": "THIS ONE WILL ALLOW YOU TO FLY HIGH INTO THE SKY",
#     	"funky": ". PERHAPS THIS WILL "
#     }
# ]

pre_amble = {"cranky": "I'VE PERFECTED ANOTHER POTION, {KONG}. ", "funky": "PAY UP DUDE, FUNKY'S GOT A NEW MOVE FOR YOU", "candy": "COME ON NOW {KONG}, GIVE ME SOME OF THOSE COINS AND "}


writeText(
    "dolby_text.bin",
    [
        ["DONKEY KONG 64 RANDOMIZER"],
        ["DEVELOPERS - 2DOS, BALLAAM, KILLKLLI, SHADOWSHINE, BISMUTH, ZNERNICUS"],
        ["DK64RANDOMIZER.COM"],
    ],
)

# writeText(
# 	"custom_text.bin",
# 	[

# 	]
# )
