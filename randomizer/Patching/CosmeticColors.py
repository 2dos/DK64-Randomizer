"""Apply cosmetic skins to kongs."""
import random
from random import randint

import js
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    model_index = 0
    if js.document.getElementById("override_cosmetics").checked:
        model_setting = js.document.getElementById("klaptrap_model").value
    else:
        model_setting = spoiler.settings.klaptrap_model
    if model_setting == "green":
        model_index = 0x21
    elif model_setting == "purple":
        model_index = 0x22
    elif model_setting == "red":
        model_index = 0x23
    elif model_setting == "random_klap":
        model_index = random.randint(0x21, 0x23)
    elif model_setting == "random_model":
        permitted_models = [
            0x19,  # Beaver
            0x1E,  # Klobber
            0x20,  # Kaboom
            0x21,  # Green Klap
            0x22,  # Purple Klap
            0x23,  # Red Klap
            0x24,  # Klap Teeth
            0x26,  # Krash
            0x27,  # Troff
            0x30,  # N64 Logo
            0x34,  # Mech Fish
            0x42,  # Krossbones
            0x47,  # Rabbit
            0x4B,  # Minecart Skeleton Head
            0x51,  # Tomato
            0x62,  # Ice Tomato
            0x69,  # Golden Banana
            0x70,  # Microbuffer
            0x72,  # Bell
            0x96,  # Missile (Car Race)
            0xB0,  # Red Buoy
            0xB1,  # Green Buoy
            0xBD,  # Rareware Logo
        ]
        model_index = random.choice(permitted_models)
    ROM().seek(spoiler.settings.rom_data + 0x136)
    ROM().writeMultipleBytes(model_index, 1)
    color_palettes = []
    color_obj = {}
    colors_dict = {}
    kong_settings = [
        {"kong": "dk", "palettes": [{"name": "base", "image": 3724, "fill_type": "block"}], "base_setting": "dk_colors", "custom_setting": "dk_custom_color", "kong_index": 0},
        {"kong": "diddy", "palettes": [{"name": "cap_shirt", "image": 3686, "fill_type": "block"}], "base_setting": "diddy_colors", "custom_setting": "diddy_custom_color", "kong_index": 1},
        {
            "kong": "lanky",
            "palettes": [{"name": "overalls", "image": 3689, "fill_type": "block"}, {"name": "patch", "image": 3734, "fill_type": "patch"}],
            "base_setting": "lanky_colors",
            "custom_setting": "lanky_custom_color",
            "kong_index": 2,
        },
        {"kong": "tiny", "palettes": [{"name": "overalls", "image": 6014, "fill_type": "block"}], "base_setting": "tiny_colors", "custom_setting": "tiny_custom_color", "kong_index": 3},
        {
            "kong": "chunky",
            "palettes": [{"name": "shirt_back", "image": 3769, "fill_type": "checkered"}, {"name": "shirt_front", "image": 3687, "fill_type": "block"}],
            "base_setting": "chunky_colors",
            "custom_setting": "chunky_custom_color",
            "kong_index": 4,
        },
        {"kong": "rambi", "palettes": [{"name": "base", "image": 3826, "fill_type": "block"}], "base_setting": "rambi_colors", "custom_setting": "rambi_custom_color", "kong_index": 5},
        {"kong": "enguarde", "palettes": [{"name": "base", "image": 3847, "fill_type": "block"}], "base_setting": "enguarde_colors", "custom_setting": "enguarde_custom_color", "kong_index": 6},
    ]

    if js.document.getElementById("override_cosmetics").checked:
        if js.document.getElementById("random_colors").checked:
            spoiler.settings.dk_colors = "randomized"
            spoiler.settings.diddy_colors = "randomized"
            spoiler.settings.lanky_colors = "randomized"
            spoiler.settings.tiny_colors = "randomized"
            spoiler.settings.chunky_colors = "randomized"
            spoiler.settings.rambi_colors = "randomized"
            spoiler.settings.enguarde_colors = "randomized"
        else:
            spoiler.settings.dk_colors = js.document.getElementById("dk_colors").value
            spoiler.settings.dk_custom_color = js.document.getElementById("dk_custom_color").value
            spoiler.settings.diddy_colors = js.document.getElementById("diddy_colors").value
            spoiler.settings.diddy_custom_color = js.document.getElementById("diddy_custom_color").value
            spoiler.settings.lanky_colors = js.document.getElementById("lanky_colors").value
            spoiler.settings.lanky_custom_color = js.document.getElementById("lanky_custom_color").value
            spoiler.settings.tiny_colors = js.document.getElementById("tiny_colors").value
            spoiler.settings.tiny_custom_color = js.document.getElementById("tiny_custom_color").value
            spoiler.settings.chunky_colors = js.document.getElementById("chunky_colors").value
            spoiler.settings.chunky_custom_color = js.document.getElementById("chunky_custom_color").value
            spoiler.settings.rambi_colors = js.document.getElementById("rambi_colors").value
            spoiler.settings.rambi_custom_color = js.document.getElementById("rambi_custom_color").value
            spoiler.settings.enguarde_colors = js.document.getElementById("enguarde_colors").value
            spoiler.settings.enguarde_custom_color = js.document.getElementById("enguarde_custom_color").value
    else:
        if spoiler.settings.random_colors:
            spoiler.settings.dk_colors = "randomized"
            spoiler.settings.diddy_colors = "randomized"
            spoiler.settings.lanky_colors = "randomized"
            spoiler.settings.tiny_colors = "randomized"
            spoiler.settings.chunky_colors = "randomized"
            spoiler.settings.rambi_colors = "randomized"
            spoiler.settings.enguarde_colors = "randomized"

    colors_dict = {
        "dk_colors": spoiler.settings.dk_colors,
        "dk_custom_color": spoiler.settings.dk_custom_color,
        "diddy_colors": spoiler.settings.diddy_colors,
        "diddy_custom_color": spoiler.settings.diddy_custom_color,
        "lanky_colors": spoiler.settings.lanky_colors,
        "lanky_custom_color": spoiler.settings.lanky_custom_color,
        "tiny_colors": spoiler.settings.tiny_colors,
        "tiny_custom_color": spoiler.settings.tiny_custom_color,
        "chunky_colors": spoiler.settings.chunky_colors,
        "chunky_custom_color": spoiler.settings.chunky_custom_color,
        "rambi_colors": spoiler.settings.rambi_colors,
        "rambi_custom_color": spoiler.settings.rambi_custom_color,
        "enguarde_colors": spoiler.settings.enguarde_colors,
        "enguarde_custom_color": spoiler.settings.enguarde_custom_color,
    }
    for kong in kong_settings:
        base_obj = {"kong": kong["kong"], "zones": []}
        for palette in kong["palettes"]:
            arr = ["#000000"]
            if palette["fill_type"] == "checkered":
                arr = ["#000000", "#000000"]
            base_obj["zones"].append({"zone": palette["name"], "image": palette["image"], "fill_type": palette["fill_type"], "colors": arr})
        if colors_dict[kong["base_setting"]] != "vanilla":
            if colors_dict[kong["base_setting"]] == "randomized":
                color = f"#{format(randint(0, 0xFFFFFF), '06x')}"
            else:
                color = colors_dict[kong["custom_setting"]]
                if not color:
                    color = "#000000"
            base_obj["zones"][0]["colors"][0] = color
            if kong["kong_index"] in (2, 4):
                base_obj["zones"][1]["colors"][0] = color
                if kong["kong_index"] == 4:
                    red = int(f"0x{color[1:3]}", 16)
                    green = int(f"0x{color[3:5]}", 16)
                    blue = int(f"0x{color[5:7]}", 16)
                    opp_color = f"#{format(255-red,'02x')}{format(255-green,'02x')}{format(255-blue,'02x')}"
                    base_obj["zones"][0]["colors"][1] = opp_color
            color_palettes.append(base_obj)
            color_obj[f"{kong['kong']}"] = color
    spoiler.settings.colors = color_obj
    if len(color_palettes) > 0:
        convertColors(color_palettes)
