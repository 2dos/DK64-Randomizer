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

move_hints = [
	{
        "move": "Baboon Blast",
        "cranky": "I'VE PERFECTED ANOTHER POTION, DONKEY. THIS ONE WILL MAKE YOU BREAK THE DONKEY AIR-SPEED RECORD.",
        "funky": "PAY UP DUDE, FUNKY'S GOT A NEW MOVE FOR YOU WHICH WILL ENABLE YOU TO LAUNCH INTO THE STRATOSPHERE.",
        "candy": "COME ON NOW DONKEY, GIVE ME SOME OF THOSE COINS AND I CAN HELP YOU MOVE UP INTO THE SKY."
    },
    {
        "move": "Strong Kong",
        "cranky": "I'VE PERFECTED ANOTHER POTION, DONKEY. YOU MAY BE BIGGER AND FASTER, BUT THIS WILL HELP YOU FULFILL THE FINAL PART OF YOUR VERSE.",
        "funky": "PAY UP DUDE, FUNKY'S GOT A NEW MOVE FOR YOU. PERHAPS WITH THIS YOU'LL GET MUSCLES AS BIG AS MINE.",
        "candy": "COME ON NOW DONKEY, GIVE ME SOME OF THOSE COINS AND I WILL HELP YOU WALK WITH SPARKLES"
    },
    {
        "move": "Gorilla Grab",
        "cranky": "I'VE PERFECTED ANOTHER POTION, DONKEY. THIS ONE WILL ALLOW YOU TO TIME TRAVEL TO 1981.",
        "funky": "PAY UP DUDE, FUNKY'S GOT A NEW MOVE FOR YOU WHICH WILL HELP YOU GO BACK TO THEM GOOD OLD DAYS",
        "candy": "COME ON NOW DONKEY, GIVE ME SOME OF THOSE COINS AND I WILL HELP YOU OPEN UP YOUR MINECART RIDE"
    },
    {
        "move": "Chimpy Charge",
        "cranky": "I'VE PERFECTED ANOTHER POTION, DIDDY. BETTER GET THAT CRANIUM TOUGHENED IF YOU PURCHASE THIS MOVE",
        "funky": "",
    }
]

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
