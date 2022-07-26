"""Apply cosmetic skins to kongs."""
from randomizer.Patching.Patcher import ROM
from randomizer.Spoiler import Spoiler
from randomizer.Patching.generate_kong_color_images import convertColors
from random import randint
import random
import js


def apply_cosmetic_colors(spoiler: Spoiler):
    """Apply cosmetic skins to kongs."""
    if spoiler.settings.klaptrap_model:
        model_index = 0
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
                0x19,
                0x1E,
                0x20,
                0x21,
                0x22,
                0x23,
                0x24,
                0x26,
                0x27,
                0x2E,
                0x30,
                0x34,
                0x3E,
                0x42,
                0x47,
                0x4B,
                0x4D,
                0x51,
                0x54,
                0x62,
                0x69,
                0x70,
                0x72,
                0x96,
                0xA6,
                0xB0,
                0xB1,
                0xBD,
            ]
            model_index = random.choice(permitted_models)
        ROM().seek(spoiler.settings.rom_data + 0x126)
        ROM().writeMultipleBytes(model_index, 1)
    color_palettes = []
    color_obj = {}
    if js.document.getElementById("random_colors").checked:
        js.document.getElementById("dk_colors").value = "randomized"
        js.document.getElementById("diddy_colors").value = "randomized"
        js.document.getElementById("lanky_colors").value = "randomized"
        js.document.getElementById("tiny_colors").value = "randomized"
        js.document.getElementById("chunky_colors").value = "randomized"
        js.document.getElementById("rambi_colors").value = "randomized"
        js.document.getElementById("enguarde_colors").value = "randomized"

    kong_settings = [
        {"kong": "dk", "palettes": [{"name": "base", "image": 3724, "fill_type": "block"}], "base_setting": "dk_colors", "custom_setting": "dk_custom_color", "kong_index": 0},
        {"kong": "diddy", "palettes": [{"name": "cap_shirt", "image": 3686, "fill_type": "block"}], "base_setting": "diddy_colors", "custom_setting": "diddy_custom_color", "kong_index": 1},
        {"kong": "lanky", "palettes": [{"name": "overalls", "image": 3689, "fill_type": "block"}], "base_setting": "lanky_colors", "custom_setting": "lanky_custom_color", "kong_index": 2},
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

    for kong in kong_settings:
        base_obj = {"kong": kong["kong"], "zones": []}
        for palette in kong["palettes"]:
            arr = ["#000000"]
            if palette["fill_type"] == "checkered":
                arr = ["#000000", "#000000"]
            base_obj["zones"].append({"zone": palette["name"], "image": palette["image"], "fill_type": palette["fill_type"], "colors": arr})
        if js.document.getElementById(kong["base_setting"]).value != "vanilla":
            if js.document.getElementById(kong["base_setting"]).value == "randomized":
                color = f"#{format(randint(0, 0xFFFFFF), '06x')}"
            else:
                color = js.document.getElementById(kong["custom_setting"]).value
                if not color:
                    color = "#000000"
            base_obj["zones"][0]["colors"][0] = color
            if kong["kong_index"] == 4:
                base_obj["zones"][1]["colors"][0] = color
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
