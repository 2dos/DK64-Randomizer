"""Apply cosmetic skins to kongs."""
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from random import randint
import js


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    enable = False
    sav = 0x1FED020
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
        elif js.document.getElementById("dk_colors").value == "blue":
            color = 1
        elif js.document.getElementById("dk_colors").value == "green":
            color = 2
        elif js.document.getElementById("dk_colors").value == "purple":
            color = 3
        ROM().seek(sav + 0x127)
        ROM().write(color)
    if js.document.getElementById("diddy_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("diddy_colors").value == "randomized":
            color = randint(0, 3)
        elif js.document.getElementById("diddy_colors").value == "dark_blue":
            color = 1
        elif js.document.getElementById("diddy_colors").value == "yellow":
            color = 2
        elif js.document.getElementById("diddy_colors").value == "light_blue":
            color = 3
        ROM().seek(sav + 0x128)
        ROM().write(color)
    if js.document.getElementById("lanky_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("lanky_colors").value == "randomized":
            color = randint(0, 3)
        elif js.document.getElementById("lanky_colors").value == "green":
            color = 1
        elif js.document.getElementById("lanky_colors").value == "purple":
            color = 2
        elif js.document.getElementById("lanky_colors").value == "red":
            color = 3
        ROM().seek(sav + 0x129)
        ROM().write(color)
    if js.document.getElementById("tiny_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("tiny_colors").value == "randomized":
            color = randint(0, 2)  # Change back to 3 once Red Tiny Color is fixed.
        elif js.document.getElementById("tiny_colors").value == "green":
            color = 1
        elif js.document.getElementById("tiny_colors").value == "purple":
            color = 2
        elif js.document.getElementById("tiny_colors").value == "red":
            color = 3
        ROM().seek(sav + 0x12A)
        ROM().write(color)
    if js.document.getElementById("chunky_colors").value != "vanilla":
        enable = True
        color = 0
        if js.document.getElementById("chunky_colors").value == "randomized":
            color = randint(0, 3)
        elif js.document.getElementById("chunky_colors").value == "red":
            color = 1
        elif js.document.getElementById("chunky_colors").value == "purple":
            color = 2
        elif js.document.getElementById("chunky_colors").value == "green":
            color = 3
        ROM().seek(sav + 0x12B)
        ROM().write(color)

    if enable:
        ROM().seek(sav + 0x126)
        ROM().write(1)
