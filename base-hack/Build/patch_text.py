"""Patch some common text."""

from text_encoder import writeText
import shutil

move_hints = [
    {
        "move": "Baboon Blast",
        "kong": "Donkey",
        "cranky": "",
        "funky": "",
        "candy": ""
    },
    {
        "move": "Strong Kong",
        "kong": "Donkey",
        "cranky": "",
        "funky": "",
        "candy": ""
    },
    {
        "move": "Gorilla Grab",
        "kong": "Donkey",
        "cranky": "",
        "funky": "",
        "candy": ""
    },
    {
        "move": "Chimpy Charge",
        "kong": "Diddy",
        "cranky": "",
        "funky": "",
        "candy": ""
    },
    {
    	"move": "Rocketbarrel",
    	"kong": "Diddy",
    	"cranky": "",
        "funky": "",
        "candy": ""
    }
]

pre_amble = {"cranky": "I'VE PERFECTED ANOTHER POTION, {KONG}. ", "funky": "PAY UP DUDE, FUNKY'S GOT A NEW MOVE FOR YOU", "candy": "COME ON NOW {KONG}, GIVE ME SOME OF THOSE COINS AND "}

moves = [
	"Baboon Blast",
	"Strong Kong",
	"Gorilla Grab",
	"Chimpy Charge",
	"Rocketbarrel",
	"Simian Spring",
	"Orangstand",
	"Baboon Balloon",
	"Orangstand Sprint",
	"Mini Monkey",
	"Ponytail Twirl",
	"Monkeyport",
	"Hunky Chunky",
	"Primate Punch",
	"Gorilla Gone",
	"Simian Slam Upgrade",
	"Coconut Gun",
	"Peanut Popguns",
	"Grape Shooter",
	"Feather Bow",
	"Pineapple Launcher",
	"Homing Ammo",
	"Sniper Scope",
	"Ammo Belt Upgrade",
	"Bongo Blast",
	"Guitar Gazump",
	"Trombone Tremor",
	"Saxophone Slam",
	"Triangle Trample",
	"Instrument Upgrade",
	"Not enough coins - Special Move",
	"Not enough coins - Slam",
	"Not enough coins - Gun",
	"Not enough coins - Ammo Belt",
	"Not enough coins - Instrument"
]

shop_owners = [
	"Cranky",
	"Funky",
	"Candy",
]

hint_text = []

for move in moves:
	for shop in shop_owners:
		hint_text.append([f"{move.upper()} ({shop.upper()})"])


writeText(
    "dolby_text.bin",
    [
        ["DONKEY KONG 64 RANDOMIZER"],
        ["DEVELOPERS - 2DOS, BALLAAM, BISMUTH, CFOX, KILLKLLI, SHADOWSHINE, ZNERNICUS"],
        ["DK64RANDOMIZER.COM"],
    ],
)

writeText(
	"custom_text.bin",
	hint_text
)