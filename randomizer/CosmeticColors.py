"""Apply cosmetic skins to kongs."""
from randomizer.Patcher import ROM
from randomizer.Spoiler import Spoiler


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    enable = False
    sav = 0x1FED020
    if spoiler.settings.dk_colors != "vanilla":
        enable = True
        color = 0
        if spoiler.settings.dk_colors == "blue":
            color = 1
        elif spoiler.settings.dk_colors == "green":
            color = 2
        elif spoiler.settings.dk_colors == "purple":
            color = 3
        ROM().seek(sav + 0x127)
        ROM().write(color)
    if spoiler.settings.diddy_colors != "vanilla":
        enable = True
        color = 0
        if spoiler.settings.diddy_colors == "dark_blue":
            color = 1
        elif spoiler.settings.diddy_colors == "yellow":
            color = 2
        elif spoiler.settings.diddy_colors == "light_blue":
            color = 3
        ROM().seek(sav + 0x128)
        ROM().write(color)
    if spoiler.settings.lanky_colors != "vanilla":
        enable = True
        color = 0
        if spoiler.settings.lanky_colors == "green":
            color = 1
        elif spoiler.settings.lanky_colors == "purple":
            color = 2
        elif spoiler.settings.lanky_colors == "red":
            color = 3
        ROM().seek(sav + 0x129)
        ROM().write(color)
    if spoiler.settings.tiny_colors != "vanilla":
        enable = True
        color = 0
        if spoiler.settings.tiny_colors == "green":
            color = 1
        elif spoiler.settings.tiny_colors == "purple":
            color = 2
        elif spoiler.settings.tiny_colors == "red":
            color = 3
        ROM().seek(sav + 0x12A)
        ROM().write(color)
    if spoiler.settings.chunky_colors != "vanilla":
        enable = True
        color = 0
        if spoiler.settings.tiny_colors == "red":
            color = 1
        elif spoiler.settings.tiny_colors == "purple":
            color = 2
        elif spoiler.settings.tiny_colors == "green":
            color = 3
        ROM().seek(sav + 0x12B)
        ROM().write(color)

    if enable:
        ROM().seek(sav + 0x126)
        ROM().write(1)
