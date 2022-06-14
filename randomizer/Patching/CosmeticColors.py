"""Apply cosmetic skins to kongs."""
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Patching.generate_kong_color_images import convertColors
from random import randint
import js


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    enable = False
    sav = 0x1FED020
    color_palettes = [
        {"kong": "dk", "zones": [{"zone": "base", "image": 3724, "colors": ["#2da1ad"], "fill_type": "radial"}]},
        {"kong": "diddy", "zones": [{"zone": "cap_shirt", "image": 3686, "colors": ["#00ff37"], "fill_type": "radial"}]},
        {"kong": "lanky", "zones": [{"zone": "overalls", "image": 3689, "colors": ["#3e1c73"], "fill_type": "radial"}]},
        {"kong": "tiny", "zones": [{"zone": "overalls", "image": 6014, "colors": ["#ff3beb"], "fill_type": "radial"}]},
        {
            "kong": "chunky",
            "zones": [
                {"zone": "shirt_back", "image": 3769, "colors": ["#FF0000", "#FFFFFF"], "fill_type": "checkered"},
                {"zone": "shirt_front", "image": 3687, "colors": ["#000000"], "fill_type": "radial"},
            ],
        },
    ]

    if js.document.getElementById("random_colors").checked:
        js.document.getElementById("dk_colors").value = "randomized"
        js.document.getElementById("diddy_colors").value = "randomized"
        js.document.getElementById("lanky_colors").value = "randomized"
        js.document.getElementById("tiny_colors").value = "randomized"
        js.document.getElementById("chunky_colors").value = "randomized"
    if js.document.getElementById("dk_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("dk_colors").value == "randomized":
            color = randint(0, 3)
        else:
            color = js.document.getElementById("dk_custom_color").value
            color_palettes[0]["zones"][0]["colors"] = [color]
        # ROM().seek(sav + 0x127)
        # ROM().write(color)
    if js.document.getElementById("diddy_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("diddy_colors").value == "randomized":
            color = randint(0, 3)
        else:
            color = js.document.getElementById("diddy_custom_color").value
            color_palettes[1]["zones"][0]["colors"] = [color]
        # ROM().seek(sav + 0x128)
        # ROM().write(color)
    if js.document.getElementById("lanky_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("lanky_colors").value == "randomized":
            color = randint(0, 3)
        else:
            color = js.document.getElementById("lanky_custom_color").value
            color_palettes[2]["zones"][0]["colors"] = [color]
        # ROM().seek(sav + 0x129)
        # ROM().write(color)
    if js.document.getElementById("tiny_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("tiny_colors").value == "randomized":
            color = randint(0, 2)  # Change back to 3 once Red Tiny Color is fixed.
        else:
            color = js.document.getElementById("tiny_custom_color").value
            color_palettes[3]["zones"][0]["colors"] = [color]
        # ROM().seek(sav + 0x12A)
        # ROM().write(color)
    if js.document.getElementById("chunky_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("chunky_colors").value == "randomized":
            color = randint(0, 3)
        else:
            color = js.document.getElementById("chunky_custom_color").value
            color_palettes[4]["zones"][0]["colors"] = [color, color]
            color_palettes[4]["zones"][1]["colors"] = [color]
        # ROM().seek(sav + 0x12B)
        # ROM().write(color)

    if enable:
        ROM().seek(sav + 0x126)
        ROM().write(1)

    convertColors(color_palettes)
