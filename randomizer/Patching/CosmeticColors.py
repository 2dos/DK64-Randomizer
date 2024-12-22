"""Apply cosmetic skins to kongs."""

from __future__ import annotations

import gzip
import random
import zlib
from random import randint
from typing import TYPE_CHECKING, List, Tuple
from io import BytesIO

from PIL import Image, ImageDraw, ImageEnhance

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, ColorblindMode, RandomModels, KongModels, WinConditionComplex
from randomizer.Enums.Models import Model, Sprite
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import BarrierItems
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Cosmetics.CustomTextures import writeTransition, writeCustomPaintings, writeCustomPortal
from randomizer.Patching.Cosmetics.Krusha import placeKrushaHead, fixBaboonBlasts, kong_index_mapping, fixModelSmallKongCollision
from randomizer.Patching.Cosmetics.Colorblind import (
    recolorKlaptraps,
    writeWhiteKasplatHairColorToROM,
    recolorBells,
    recolorWrinklyDoors,
    recolorSlamSwitches,
    recolorBlueprintModelTwo,
    recolorPotions,
    recolorMushrooms,
    writeKasplatHairColorToROM,
    maskBlueprintImage,
    maskLaserImage,
    recolorKRoolShipSwitch,
    recolorRotatingRoomTiles,
)
from randomizer.Patching.Lib import (
    PaletteFillType,
    SpawnerChange,
    applyCharacterSpawnerChanges,
    compatible_background_textures,
    TableNames,
    getRawFile,
)
from randomizer.Patching.LibImage import (
    getImageFile, 
    TextureFormat, 
    getRandomHueShift, 
    hueShift, 
    ExtraTextures, 
    getBonusSkinOffset, 
    writeColorImageToROM, 
    numberToImage, 
    getRGBFromHash,
    maskImage,
    maskImageWithColor,
    getKongItemColor,
    hueShiftImageContainer,
)
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Settings import Settings
from randomizer.Patching.Cosmetics.ModelSwaps import (
    turtle_models,
    panic_models,
    bother_models,
    piano_models,
    piano_extreme_model,
    spotlight_fish_models,
    candy_cutscene_models,
    funky_cutscene_models,
    funky_cutscene_models_extreme,
    boot_cutscene_models,
    melon_random_sprites,
)

if TYPE_CHECKING:
    from PIL.Image import Image


class HelmDoorSetting:
    """Class to store information regarding helm doors."""

    def __init__(self, item_setting: BarrierItems, count: int, item_image: int, number_image: int) -> None:
        """Initialize with given parameters."""
        self.item_setting = item_setting
        self.count = count
        self.item_image = item_image
        self.number_image = number_image


class HelmDoorImages:
    """Class to store information regarding helm door item images."""

    def __init__(
        self,
        setting: BarrierItems,
        image_indexes: List[int],
        flip: bool = False,
        table: int = 25,
        dimensions: Tuple[int, int] = (44, 44),
        format: TextureFormat = TextureFormat.RGBA5551,
    ) -> None:
        """Initialize with given parameters."""
        self.setting = setting
        self.image_indexes = image_indexes
        self.flip = flip
        self.table = table
        self.dimensions = dimensions
        self.format = format




model_mapping = {
    KongModels.default: 0,
    KongModels.disco_chunky: 6,
    KongModels.krusha: 7,
    KongModels.krool_cutscene: 9,
    KongModels.krool_fight: 8,
    KongModels.cranky: 10,
    KongModels.candy: 11,
    KongModels.funky: 12,
}
krusha_texture_replacement = {
    # Textures Krusha can use when he replaces various kongs (Main color, belt color)
    Kongs.donkey: (3724, 0x177D),
    Kongs.diddy: (4971, 4966),
    Kongs.lanky: (3689, 0xE9A),
    Kongs.tiny: (6014, 0xE68),
    Kongs.chunky: (3687, 3778),
}
model_texture_sections = {
    KongModels.krusha: {
        "skin": [0x4738, 0x2E96, 0x3A5E],
        "kong": [0x3126, 0x354E, 0x37FE, 0x41E6],
    },
    KongModels.krool_fight: {
        "skin": [
            0x61D6,
            0x63FE,
            0x6786,
            0x7DD6,
            0x7E8E,
            0x7F3E,
            0x7FEE,
            0x5626,
            0x56E6,
            0x5A86,
            0x5BAE,
            0x5D46,
            0x5E2E,
            0x5FAE,
            0x69BE,
            0x735E,
            0x7C5E,
            0x7E4E,
            0x7EF6,
            0x7FA6,
            0x8056,
        ],
        "kong": [0x607E, 0x7446, 0x7D46, 0x80FE],
    },
    # KongModels.krool_cutscene: {
    #     "skin": [0x4A6E, 0x4CBE, 0x52AE, 0x55BE, 0x567E, 0x57E6, 0x5946, 0x5AA6, 0x5E06, 0x5EC6, 0x6020, 0x618E, 0x62F6, 0x6946, 0x6A6E, 0x6C5E, 0x6D86, 0x6F76, 0x702E, 0x70DE, 0x718E, 0x72FE, 0x4FBE, 0x51FE, 0x5C26, 0x6476, 0x6826, 0x6B26, 0x6E3E, 0x6FE6, 0x7096, 0x7146, 0x71F6, 0x733E, 0x743E],
    #     "kong": [],
    # }
}


class KongPalette:
    """Class to store information regarding a kong palette."""

    def __init__(self, name: str, image: int, fill_type: PaletteFillType, alt_name: str = None):
        """Initialize with given parameters."""
        self.name = name
        self.image = image
        self.fill_type = fill_type
        self.alt_name = alt_name
        if alt_name is None:
            self.alt_name = name


class KongPaletteSetting:
    """Class to store information regarding the kong palette setting."""

    def __init__(self, kong: str, kong_index: int, palettes: list[KongPalette]):
        """Initialize with given parameters."""
        self.kong = kong
        self.kong_index = kong_index
        self.palettes = palettes.copy()
        self.setting_kong = kong


def getKongColor(settings: Settings, index: int):
    """Get color index for a kong."""
    kong_colors = ["#ffd700", "#ff0000", "#1699ff", "#B045ff", "#41ff25"]
    mode = settings.colorblind_mode
    if mode != ColorblindMode.off and settings.override_cosmetics:
        if mode == ColorblindMode.prot:
            kong_colors = ["#000000", "#0072FF", "#766D5A", "#FFFFFF", "#FDE400"]
        elif mode == ColorblindMode.deut:
            kong_colors = ["#000000", "#318DFF", "#7F6D59", "#FFFFFF", "#E3A900"]
        elif mode == ColorblindMode.trit:
            kong_colors = ["#000000", "#C72020", "#13C4D8", "#FFFFFF", "#FFA4A4"]
    return kong_colors[index]


DEFAULT_COLOR = "#000000"
KLAPTRAPS = [Model.KlaptrapGreen, Model.KlaptrapPurple, Model.KlaptrapRed]
RECOLOR_MEDAL_RIM = False


def getRandomKlaptrapModel() -> Model:
    """Get random klaptrap model."""
    return random.choice(KLAPTRAPS)


def changePatchFace(settings: Settings):
    """Change the top of the dirt patch image."""
    if not settings.better_dirt_patch_cosmetic:
        return
    dirt_im = getImageFile(25, 0x1379, True, 32, 32, TextureFormat.RGBA5551)
    letd_im = getImageFile(14, 0x75, True, 40, 51, TextureFormat.RGBA5551).resize((18, 32)).rotate(-5)
    letk_im = getImageFile(14, 0x76, True, 40, 51, TextureFormat.RGBA5551).resize((18, 32))
    letter_ims = (letd_im, letk_im)
    for letter in letter_ims:
        imw, imh = letter.size
        px = letter.load()
        for x in range(imw):
            for y in range(imh):
                r, g, b, a = letter.getpixel((x, y))
                px[x, y] = (r, g, b, 150 if a > 128 else 0)
    dirt_im.paste(letd_im, (0, 0), letd_im)
    dirt_im.paste(letk_im, (16, 0), letk_im)
    writeColorImageToROM(dirt_im, 25, 0x1379, 32, 32, False, TextureFormat.RGBA5551)


def apply_cosmetic_colors(settings: Settings):
    """Apply cosmetic skins to kongs."""
    bother_model_index = Model.KlaptrapGreen
    panic_fairy_model_index = Model.BananaFairy
    panic_klap_model_index = Model.KlaptrapGreen
    turtle_model_index = Model.Turtle
    sseek_klap_model_index = Model.KlaptrapGreen
    fungi_tomato_model_index = Model.Tomato
    caves_tomato_model_index = Model.IceTomato
    racer_beetle = Model.Beetle
    racer_rabbit = Model.Rabbit
    piano_burper = Model.KoshKremlingRed
    spotlight_fish_model_index = Model.SpotlightFish
    candy_model_index = Model.Candy
    funky_model_index = Model.Funky
    boot_model_index = Model.Boot
    melon_sprite = Sprite.BouncingMelon
    swap_bitfield = 0

    ROM_COPY = ROM()
    sav = settings.rom_data

    changePatchFace(settings)

    model_inverse_mapping = {}
    for model in model_mapping:
        val = model_mapping[model]
        model_inverse_mapping[val] = model
    ROM_COPY.seek(settings.rom_data + 0x1B8)
    settings.kong_model_dk = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_diddy = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_lanky = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_tiny = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    settings.kong_model_chunky = model_inverse_mapping[int.from_bytes(ROM_COPY.readBytes(1), "big")]
    if settings.override_cosmetics:
        model_setting = RandomModels[js.document.getElementById("random_models").value]
    else:
        model_setting = settings.random_models
    if model_setting == RandomModels.random:
        bother_model_index = getRandomKlaptrapModel()
    elif model_setting == RandomModels.extreme:
        bother_model_index = random.choice(bother_models)
        racer_beetle = random.choice([Model.Beetle, Model.Rabbit])
        racer_rabbit = random.choice([Model.Beetle, Model.Rabbit])
        if racer_rabbit == Model.Beetle:
            spawner_changes = []
            # Fungi
            rabbit_race_fungi_change = SpawnerChange(Maps.FungiForest, 2)
            rabbit_race_fungi_change.new_scale = 50
            rabbit_race_fungi_change.new_speed_0 = 70
            rabbit_race_fungi_change.new_speed_1 = 136
            spawner_changes.append(rabbit_race_fungi_change)
            # Caves
            rabbit_caves_change = SpawnerChange(Maps.CavesChunkyIgloo, 1)
            rabbit_caves_change.new_scale = 40
            spawner_changes.append(rabbit_caves_change)
            applyCharacterSpawnerChanges(spawner_changes)
    if model_setting != RandomModels.off:
        panic_fairy_model_index = random.choice(panic_models)
        turtle_model_index = random.choice(turtle_models)
        panic_klap_model_index = getRandomKlaptrapModel()
        sseek_klap_model_index = getRandomKlaptrapModel()
        fungi_tomato_model_index = random.choice([Model.Tomato, Model.IceTomato])
        caves_tomato_model_index = random.choice([Model.Tomato, Model.IceTomato])
        referenced_piano_models = piano_models.copy()
        referenced_funky_models = funky_cutscene_models.copy()
        if model_setting == RandomModels.extreme:
            referenced_piano_models.extend(piano_extreme_model)
            spotlight_fish_model_index = random.choice(spotlight_fish_models)
            referenced_funky_models.extend(funky_cutscene_models_extreme)
            boot_model_index = random.choice(boot_cutscene_models)
        piano_burper = random.choice(referenced_piano_models)
        candy_model_index = random.choice(candy_cutscene_models)
        funky_model_index = random.choice(funky_cutscene_models)
    settings.bother_klaptrap_model = bother_model_index
    settings.beetle_model = racer_beetle
    settings.rabbit_model = racer_rabbit
    settings.panic_fairy_model = panic_fairy_model_index
    settings.turtle_model = turtle_model_index
    settings.panic_klaptrap_model = panic_klap_model_index
    settings.seek_klaptrap_model = sseek_klap_model_index
    settings.fungi_tomato_model = fungi_tomato_model_index
    settings.caves_tomato_model = caves_tomato_model_index
    settings.piano_burp_model = piano_burper
    settings.spotlight_fish_model = spotlight_fish_model_index
    settings.candy_cutscene_model = candy_model_index
    settings.funky_cutscene_model = funky_model_index
    settings.boot_cutscene_model = boot_model_index
    settings.wrinkly_rgb = [255, 255, 255]
    # Compute swap bitfield
    swap_bitfield |= 0x10 if settings.rabbit_model == Model.Beetle else 0
    swap_bitfield |= 0x20 if settings.beetle_model == Model.Rabbit else 0
    swap_bitfield |= 0x40 if settings.fungi_tomato_model == Model.IceTomato else 0
    swap_bitfield |= 0x80 if settings.caves_tomato_model == Model.Tomato else 0
    # Write Models
    ROM_COPY.seek(sav + 0x1B5)
    ROM_COPY.writeMultipleBytes(settings.panic_fairy_model + 1, 1)  # Still needed for end seq fairy swap
    ROM_COPY.seek(sav + 0x1E2)
    ROM_COPY.write(swap_bitfield)
    settings.jetman_color = [0xFF, 0xFF, 0xFF]
    if settings.misc_cosmetics and settings.override_cosmetics:
        ROM_COPY.seek(sav + 0x196)
        ROM_COPY.write(1)
        # Menu Background
        textures = list(compatible_background_textures.keys())
        weights = [compatible_background_textures[x].weight for x in textures]
        selected_texture = random.choices(textures, weights=weights, k=1)[0]
        settings.menu_texture_index = selected_texture
        settings.menu_texture_name = compatible_background_textures[selected_texture].name
        # Jetman
        jetman_color = [0xFF] * 3
        sufficiently_bright = False
        brightness_threshold = 80
        for channel in range(3):
            jetman_color[channel] = random.randint(0, 0xFF)
            if jetman_color[channel] >= brightness_threshold:
                sufficiently_bright = True
        if not sufficiently_bright:
            channel = random.randint(0, 2)
            value = random.randint(brightness_threshold, 0xFF)
            jetman_color[channel] = value
        settings.jetman_color = jetman_color.copy()
        melon_sprite = random.choice(melon_random_sprites)
    settings.minigame_melon_sprite = melon_sprite
    color_palettes = []
    color_obj = {}
    colors_dict = {}
    kong_settings = [
        KongPaletteSetting(
            "dk",
            0,
            [
                KongPalette("fur", 3724, PaletteFillType.block),
                KongPalette("tie", 0x177D, PaletteFillType.block),
                KongPalette("tie", 0xE8D, PaletteFillType.patch),
            ],
        ),
        KongPaletteSetting(
            "diddy",
            1,
            [
                KongPalette("clothes", 3686, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "lanky",
            2,
            [
                KongPalette("clothes", 3689, PaletteFillType.block),
                KongPalette("clothes", 3734, PaletteFillType.patch),
                KongPalette("fur", 0xE9A, PaletteFillType.block),
                KongPalette("fur", 0xE94, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "tiny",
            3,
            [
                KongPalette("clothes", 6014, PaletteFillType.block),
                KongPalette("hair", 0xE68, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "chunky",
            4,
            [
                KongPalette("main", 3769, PaletteFillType.checkered, "other"),
                KongPalette("main", 3687, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "rambi",
            5,
            [
                KongPalette("skin", 3826, PaletteFillType.block),
            ],
        ),
        KongPaletteSetting(
            "enguarde",
            6,
            [
                KongPalette("skin", 3847, PaletteFillType.block),
            ],
        ),
    ]

    KONG_ZONES = {
        "DK": ["Fur", "Tie"],
        "Diddy": ["Clothes"],
        "Lanky": ["Clothes", "Fur"],
        "Tiny": ["Clothes", "Hair"],
        "Chunky": ["Main", "Other"],
        "Rambi": ["Skin"],
        "Enguarde": ["Skin"],
    }

    if js.document.getElementById("override_cosmetics").checked or True:
        writeTransition(settings)
        writeCustomPortal(settings)
        writeCustomPaintings(settings)
        # randomizePlants(ROM_COPY, settings)  # Not sure how much I like how this feels
        if js.document.getElementById("random_colors").checked:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors.randomized)
        else:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(
                        f"{kong.lower()}_{zone.lower()}_colors",
                        CharacterColors[js.document.getElementById(f"{kong.lower()}_{zone.lower()}_colors").value],
                    )
                    settings.__setattr__(
                        f"{kong.lower()}_{zone.lower()}_custom_color",
                        js.document.getElementById(f"{kong.lower()}_{zone.lower()}_custom_color").value,
                    )
        settings.gb_colors = CharacterColors[js.document.getElementById("gb_colors").value]
        settings.gb_custom_color = js.document.getElementById("gb_custom_color").value
    else:
        if settings.random_colors:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors.randomized)
        settings.gb_colors = CharacterColors.randomized

    colors_dict = {}
    for kong in KONG_ZONES:
        for zone in KONG_ZONES[kong]:
            colors_dict[f"{kong.lower()}_{zone.lower()}_colors"] = settings.__getattribute__(f"{kong.lower()}_{zone.lower()}_colors")
            colors_dict[f"{kong.lower()}_{zone.lower()}_custom_color"] = settings.__getattribute__(f"{kong.lower()}_{zone.lower()}_custom_color")
    for kong in kong_settings:
        if kong.kong_index == 4:
            if settings.kong_model_chunky == KongModels.disco_chunky:
                kong.palettes = [
                    KongPalette("main", 3777, PaletteFillType.sparkle),
                    KongPalette("other", 3778, PaletteFillType.sparkle),
                ]
        settings_values = [
            settings.kong_model_dk,
            settings.kong_model_diddy,
            settings.kong_model_lanky,
            settings.kong_model_tiny,
            settings.kong_model_chunky,
        ]
        if kong.kong_index >= 0 and kong.kong_index < len(settings_values):
            if settings_values[kong.kong_index] in model_texture_sections:
                base_setting = kong.palettes[0].name
                kong.palettes = [
                    KongPalette(base_setting, krusha_texture_replacement[kong.kong_index][0], PaletteFillType.block),  # krusha_skin
                    KongPalette(base_setting, krusha_texture_replacement[kong.kong_index][1], PaletteFillType.kong),  # krusha_indicator
                ]
        base_obj = {"kong": kong.kong, "zones": []}
        zone_to_colors = {}
        for palette in kong.palettes:
            arr = [DEFAULT_COLOR]
            if palette.fill_type == PaletteFillType.checkered:
                arr = ["#FFFF00", "#00FF00"]
            elif palette.fill_type == PaletteFillType.kong:
                arr = [getKongColor(settings, kong.kong_index)]
            zone_data = {
                "zone": palette.name,
                "image": palette.image,
                "fill_type": palette.fill_type,
                "colors": arr,
            }
            for index in range(len(arr)):
                base_setting = f"{kong.kong}_{palette.name}_colors"
                custom_setting = f"{kong.kong}_{palette.name}_custom_color"
                if index == 1:  # IS THE CHECKERED PATTERN
                    base_setting = f"{kong.kong}_{palette.alt_name}_colors"
                    custom_setting = f"{kong.kong}_{palette.alt_name}_custom_color"
                if (settings.override_cosmetics and colors_dict[base_setting] != CharacterColors.vanilla) or (palette.fill_type == PaletteFillType.kong):
                    color = None
                    # if this palette color is randomized, and isn't krusha's kong indicator:
                    if colors_dict[base_setting] == CharacterColors.randomized and palette.fill_type != PaletteFillType.kong:
                        if base_setting in zone_to_colors:
                            color = zone_to_colors[base_setting]
                        else:
                            color = f"#{format(randint(0, 0xFFFFFF), '06x')}"
                            zone_to_colors[base_setting] = color
                    # if this palette color is not randomized (but might be a custom color) and isn't krusha's kong indicator:
                    elif palette.fill_type != PaletteFillType.kong:
                        color = colors_dict[custom_setting]
                        if not color:
                            color = DEFAULT_COLOR
                    # if this is krusha's kong indicator:
                    else:
                        color = getKongColor(settings, kong.kong_index)
                    if color is not None:
                        zone_data["colors"][index] = color
                        base_obj["zones"].append(zone_data)
                        color_palettes.append(base_obj)
                        color_obj[f"{kong.kong} {palette.name}"] = color
    settings.colors = color_obj
    if len(color_palettes) > 0:
        # this is just to prune the duplicates that appear. someone should probably fix the root of the dupe issue tbh
        new_color_palettes = []
        for pal in color_palettes:
            if pal not in new_color_palettes:
                new_color_palettes.append(pal)
        convertColors(new_color_palettes)
    # GB Shine
    if settings.override_cosmetics and settings.gb_colors != CharacterColors.vanilla:
        channels = []
        if settings.gb_colors == CharacterColors.randomized:
            for x in range(3):
                channels.append(random.randint(0, 255))
        elif settings.gb_colors == CharacterColors.custom:
            for x in range(3):
                start = (2 * x) + 1
                finish = (2 * x) + 3
                channel = int(settings.gb_custom_color[start:finish], 16)
                channels.append(channel)
        rim_texture = getBonusSkinOffset(ExtraTextures.MedalRim)
        base_textures = [0xB7B, 0x323]
        if RECOLOR_MEDAL_RIM:
            base_textures.extend([rim_texture, 0xBAA])  # Medal and top ring
        # base_textures = [0xB7B, 0x323, 0xBAA, rim_texture, 0xE4D, 0xE4E]  # Banana hoard looks **very** strange like this
        textures = base_textures + list(range(0x155C, 0x1568))
        for tex in textures:
            dim_pattern = {
                0xB7B: (32, 32),
                0x323: (32, 32),
                0xBAA: (4, 4),
                rim_texture: (32, 32),
                0xE4D: (64, 32),
                0xE4E: (64, 32),
            }
            dim_pattern_local = dim_pattern.get(tex, (44, 44))
            width = dim_pattern_local[0]
            height = dim_pattern_local[1]
            shine_img = getImageFile(25, tex, True, width, height, TextureFormat.RGBA5551)
            gb_shine_img = maskImageGBSpin(shine_img, tuple(channels), tex)
            if tex == 0xB7B:
                # Create fake GB shine img
                min_rgb = min(channels[0], channels[1], channels[2])
                max_rgb = max(channels[0], channels[1], channels[2])
                is_greyscale = (max_rgb - min_rgb) < 50
                fakegb_shine_img = None
                delta_mag = 80
                if is_greyscale:
                    delta = -delta_mag
                    if max_rgb < 128:
                        delta = delta_mag
                    fakegb_shine_img = maskImageWithColor(shine_img, tuple([x + delta for x in channels]))
                else:
                    new_color = hueShiftColor(tuple(channels), 60, 1750)
                    fakegb_shine_img = maskImageWithColor(shine_img, new_color)
                writeColorImageToROM(
                    fakegb_shine_img,
                    25,
                    getBonusSkinOffset(ExtraTextures.FakeGBShine),
                    width,
                    height,
                    False,
                    TextureFormat.RGBA5551,
                )
            writeColorImageToROM(gb_shine_img, 25, tex, width, height, False, TextureFormat.RGBA5551)

balloon_single_frames = [(4, 38), (5, 38), (5, 38), (5, 38), (5, 38), (5, 38), (4, 38), (4, 38)]

def getSpinPixels() -> dict:
    """Get pixels that shouldn't be affected by the mask."""
    spin_lengths = {
        0x155C: {
            17: (12, 2),
            18: (11, 4),
            19: (10, 6),
            20: (10, 7),
            21: (10, 7),
            22: (10, 6),
            23: (11, 3),
        },
        0x155D: {
            14: (15, 1),
            15: (14, 5),
            16: (13, 7),
            17: (12, 9),
            18: (12, 10),
            19: (12, 11),
            20: (12, 11),
            21: (13, 10),
            22: (14, 8),
            23: (15, 4),
        },
        0x155E: {
            14: (19, 5),
            15: (19, 7),
            16: (18, 9),
            17: (18, 10),
            18: (18, 10),
            19: (19, 10),
            20: (20, 9),
            21: (21, 8),
            22: (22, 7),
        },
        0x155F: {
            14: (27, 2),
            15: (26, 5),
            16: (26, 6),
            17: (26, 6),
            18: (27, 6),
            19: (27, 6),
            20: (28, 5),
            21: (29, 4),
            22: (29, 4),
            23: (30, 3),
        },
        0x1560: {
            16: (32, 1),
            17: (32, 2),
            18: (33, 1),
            19: (33, 2),
            20: (33, 1),
            21: (33, 1),
            22: (33, 1),
        },
    }
    spin_pixels = {}
    for tex in spin_lengths:
        local_lst = []
        for y in spin_lengths[tex]:
            for x_o in range(spin_lengths[tex][y][1]):
                local_lst.append((spin_lengths[tex][y][0] + x_o, y))
        spin_pixels[tex] = local_lst
    return spin_pixels


def maskImageGBSpin(im_f, color: tuple, image_index: int):
    """Mask the GB Spin Sprite."""
    if image_index in (getBonusSkinOffset(ExtraTextures.MedalRim), 0xBAA):
        color = tuple([int(x * 0.75) for x in list(color)])
    masked_im = maskImageWithColor(im_f, color)
    spin_pixels = getSpinPixels()
    if image_index not in spin_pixels:
        return masked_im
    px = im_f.load()
    px_0 = masked_im.load()
    for point in spin_pixels[image_index]:
        px_0[point[0], point[1]] = px[point[0], point[1]]
    return masked_im

def hueShiftColor(color: tuple, amount: int, head_ratio: int = None) -> tuple:
    """Apply a hue shift to a color."""
    # RGB -> HSV Conversion
    red_ratio = color[0] / 255
    green_ratio = color[1] / 255
    blue_ratio = color[2] / 255
    color_max = max(red_ratio, green_ratio, blue_ratio)
    color_min = min(red_ratio, green_ratio, blue_ratio)
    color_delta = color_max - color_min
    hue = 0
    if color_delta != 0:
        if color_max == red_ratio:
            hue = 60 * (((green_ratio - blue_ratio) / color_delta) % 6)
        elif color_max == green_ratio:
            hue = 60 * (((blue_ratio - red_ratio) / color_delta) + 2)
        else:
            hue = 60 * (((red_ratio - green_ratio) / color_delta) + 4)
    sat = 0 if color_max == 0 else color_delta / color_max
    val = color_max
    # Adjust Hue
    if head_ratio is not None and sat != 0:
        amount = head_ratio / (sat * 100)
    hue = (hue + amount) % 360
    # HSV -> RGB Conversion
    c = val * sat
    x = c * (1 - abs(((hue / 60) % 2) - 1))
    m = val - c
    if hue < 60:
        red_ratio = c
        green_ratio = x
        blue_ratio = 0
    elif hue < 120:
        red_ratio = x
        green_ratio = c
        blue_ratio = 0
    elif hue < 180:
        red_ratio = 0
        green_ratio = c
        blue_ratio = x
    elif hue < 240:
        red_ratio = 0
        green_ratio = x
        blue_ratio = c
    elif hue < 300:
        red_ratio = x
        green_ratio = 0
        blue_ratio = c
    else:
        red_ratio = c
        green_ratio = 0
        blue_ratio = x
    return (int((red_ratio + m) * 255), int((green_ratio + m) * 255), int((blue_ratio + m) * 255))


def maskImageWithOutline(im_f, base_index, min_y, colorblind_mode, type=""):
    """Apply RGB mask to image with an Outline in a different color."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if type != "bunch" or base_index == 4:
        brightener = ImageEnhance.Brightness(im_dupe)
        im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getRGBFromHash(getKongItemColor(colorblind_mode, base_index))
    if base_index == 2 or (base_index == 0 and colorblind_mode == ColorblindMode.trit):  # lanky or (DK in tritanopia mode)
        border_color = getKongItemColor(colorblind_mode, Kongs.chunky)
    else:
        border_color = getKongItemColor(colorblind_mode, Kongs.diddy)
    mask2 = getRGBFromHash(border_color)
    contrast = False
    if base_index == 0:
        contrast = True
    for channel in range(3):
        mask[channel] = max(39, mask[channel])  # Too black is bad for these items
        if base_index == 0 and type == "single":  # Donkey's single
            mask[channel] += 20
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                    if contrast is True:
                        if base[channel] > 30:
                            base[channel] = int(base[channel] / 2)
                        else:
                            base[channel] = int(base[channel] / 4)
                pix[x, y] = (base[0], base[1], base[2], base[3])
    for t in range(3):
        for x in range(w):
            for y in range(min_y, h):
                base = list(pix[x, y])
                if base[3] > 0:
                    if (
                        (x + t < w and list(pix[x + t, y])[3] == 0)
                        or (y + t < h and list(pix[x, y + t])[3] == 0)
                        or (x - t > -1 and list(pix[x - t, y])[3] == 0)
                        or (y - t > min_y - 1 and list(pix[x, y - t])[3] == 0)
                    ):
                        pix[x, y] = (mask2[0], mask2[1], mask2[2], base[3])
    return im_f

BALLOON_START = [5835, 5827, 5843, 5851, 5819]


def overwrite_object_colors(settings, ROM_COPY: ROM):
    """Overwrite object colors."""
    mode = settings.colorblind_mode
    sav = settings.rom_data
    galleon_switch_value = None
    ROM_COPY.seek(sav + 0x103)
    switch_rando_on = int.from_bytes(ROM_COPY.readBytes(1), "big") != 0
    if switch_rando_on:
        ROM_COPY.seek(sav + 0x104 + 3)
        galleon_switch_value = int.from_bytes(ROM_COPY.readBytes(1), "big")
    if mode != ColorblindMode.off:
        if mode in (ColorblindMode.prot, ColorblindMode.deut):
            recolorBells()
        # Preload DK single cb image to paste onto balloons
        file = 175
        dk_single = getImageFile(7, file, False, 44, 44, TextureFormat.RGBA5551)
        dk_single = dk_single.resize((21, 21))
        blueprint_lanky = []
        # Preload blueprint images. Lanky's blueprint image is so much easier to mask, because it is blue, and the frame is brown
        for file in range(8):
            blueprint_lanky.append(getImageFile(25, 5519 + (file), True, 48, 42, TextureFormat.RGBA5551))
        writeWhiteKasplatHairColorToROM("#FFFFFF", "#000000", 25, 4125, TextureFormat.RGBA5551)
        recolorWrinklyDoors(mode)
        recolorSlamSwitches(galleon_switch_value, ROM_COPY, mode)
        recolorRotatingRoomTiles(mode)
        recolorBlueprintModelTwo(mode)
        recolorKlaptraps(mode)
        recolorPotions(mode)
        recolorMushrooms(mode)
        for kong_index in range(5):
            # file = 4120
            # # Kasplat Hair
            # hair_im = getFile(25, file, True, 32, 44, TextureFormat.RGBA5551)
            # hair_im = maskImage(hair_im, kong_index, 0)
            # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False)
            writeKasplatHairColorToROM(getKongItemColor(mode, kong_index), 25, [4124, 4122, 4123, 4120, 4121][kong_index], TextureFormat.RGBA5551)
            for file in range(5519, 5527):
                # Blueprint sprite
                blueprint_start = [5624, 5608, 5519, 5632, 5616]
                blueprint_im = blueprint_lanky[(file - 5519)]
                blueprint_im = maskBlueprintImage(blueprint_im, kong_index, mode)
                writeColorImageToROM(blueprint_im, 25, blueprint_start[kong_index] + (file - 5519), 48, 42, False, TextureFormat.RGBA5551)
            for file in range(4925, 4931):
                # Shockwave
                shockwave_start = [4897, 4903, 4712, 4950, 4925]
                shockwave_im = getImageFile(25, shockwave_start[kong_index] + (file - 4925), True, 32, 32, TextureFormat.RGBA32)
                shockwave_im = maskImage(shockwave_im, kong_index, 0, False, mode)
                writeColorImageToROM(shockwave_im, 25, shockwave_start[kong_index] + (file - 4925), 32, 32, False, TextureFormat.RGBA32)
            for file in range(784, 796):
                # Helm Laser (will probably also affect the Pufftoss laser and the Game Over laser)
                laser_start = [784, 748, 363, 760, 772]
                laser_im = getImageFile(7, laser_start[kong_index] + (file - 784), False, 32, 32, TextureFormat.RGBA32)
                laser_im = maskLaserImage(laser_im, kong_index, mode)
                writeColorImageToROM(laser_im, 7, laser_start[kong_index] + (file - 784), 32, 32, False, TextureFormat.RGBA32)
            if kong_index == 0 or kong_index == 3 or (kong_index == 2 and mode != ColorblindMode.trit):  # Lanky (prot, deut only) or DK or Tiny
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getImageFile(7, single_start[kong_index] + (file - 152), False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImageWithOutline(single_im, kong_index, 0, mode, "single")
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getImageFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImageWithOutline(coin_im, kong_index, 0, mode)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, TextureFormat.RGBA5551)
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getImageFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImageWithOutline(bunch_im, kong_index, 0, mode, "bunch")
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getImageFile(25, BALLOON_START[kong_index] + (file - 5819), True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImageWithOutline(balloon_im, kong_index, 33, mode)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + (file - 5819), 32, 64, False, TextureFormat.RGBA5551)
            else:
                for file in range(152, 160):
                    # Single
                    single_start = [168, 152, 232, 208, 240]
                    single_im = getImageFile(7, single_start[kong_index] + (file - 152), False, 44, 44, TextureFormat.RGBA5551)
                    single_im = maskImage(single_im, kong_index, 0, False, mode)
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getImageFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImage(coin_im, kong_index, 0, False, mode)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, TextureFormat.RGBA5551)
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getImageFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImage(bunch_im, kong_index, 0, True, mode)
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getImageFile(25, BALLOON_START[kong_index] + (file - 5819), True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImage(balloon_im, kong_index, 33, False, mode)
                    balloon_im.paste(dk_single, balloon_single_frames[file - 5819], dk_single)
                    writeColorImageToROM(balloon_im, 25, BALLOON_START[kong_index] + (file - 5819), 32, 64, False, TextureFormat.RGBA5551)
    else:
        # Recolor slam switch if colorblind mode is off
        if galleon_switch_value is not None:
            if galleon_switch_value != 1:
                new_color = [0xFF, 0x00, 0x00]
                if galleon_switch_value == 2:
                    new_color = [0x26, 0xA3, 0xE9]
                recolorKRoolShipSwitch(new_color, ROM_COPY)
    if settings.head_balloons:
        for kong in range(5):
            for offset in range(8):
                balloon_im = getImageFile(25, BALLOON_START[kong] + offset, True, 32, 64, TextureFormat.RGBA5551)
                kong_im = getImageFile(14, 190 + kong, True, 32, 32, TextureFormat.RGBA5551)
                kong_im = kong_im.transpose(Image.FLIP_TOP_BOTTOM).resize((20, 20))
                balloon_im.paste(kong_im, (5, 39), kong_im)
                writeColorImageToROM(balloon_im, 25, BALLOON_START[kong] + offset, 32, 64, False, TextureFormat.RGBA5551)


ORANGE_SCALING = 0.7
model_index_mapping = {
    # Regular model, instrument model
    KongModels.krusha: (0xDA, 0xDA),
    KongModels.disco_chunky: (0xD, 0xEC),
    KongModels.krool_fight: (0x113, 0x113),
    KongModels.krool_cutscene: (0x114, 0x114),
    KongModels.cranky: (0x115, 0x115),
    KongModels.candy: (0x116, 0x116),
    KongModels.funky: (0x117, 0x117),
}


def applyKongModelSwaps(settings: Settings) -> None:
    """Apply Krusha Kong setting."""
    ROM_COPY = LocalROM()
    settings_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    for index, value in enumerate(settings_values):
        ROM_COPY.seek(settings.rom_data + 0x1B8 + index)
        if value not in model_mapping:
            ROM_COPY.write(0)
        else:
            ROM_COPY.write(model_mapping[value])
            if value == KongModels.default:
                continue
            dest_data = kong_index_mapping[index]
            source_data = model_index_mapping[value]
            for model_subindex in range(2):
                if dest_data[model_subindex] is not None:
                    dest_start = js.pointer_addresses[5]["entries"][dest_data[model_subindex]]["pointing_to"]
                    source_start = js.pointer_addresses[5]["entries"][source_data[model_subindex]]["pointing_to"]
                    source_end = js.pointer_addresses[5]["entries"][source_data[model_subindex] + 1]["pointing_to"]
                    source_size = source_end - source_start
                    ROM_COPY.seek(source_start)
                    file_bytes = ROM_COPY.readBytes(source_size)
                    ROM_COPY.seek(dest_start)
                    ROM_COPY.writeBytes(file_bytes)
                    # Write uncompressed size
                    unc_table = js.pointer_addresses[26]["entries"][5]["pointing_to"]
                    ROM_COPY.seek(unc_table + (source_data[model_subindex] * 4))
                    unc_size = int.from_bytes(ROM_COPY.readBytes(4), "big")
                    ROM_COPY.seek(unc_table + (dest_data[model_subindex] * 4))
                    ROM_COPY.writeMultipleBytes(unc_size, 4)
            changeModelTextures(settings, index)
            if value in (KongModels.krusha, KongModels.krool_cutscene, KongModels.krool_fight):
                fixModelSmallKongCollision(index)
            if value == KongModels.krusha:
                placeKrushaHead(settings, index)
                if index == Kongs.donkey:
                    fixBaboonBlasts()
                # Orange Switches
                switch_faces = [0xB25, 0xB1E, 0xC81, 0xC80, 0xB24]
                base_im = getImageFile(25, 0xC20, True, 32, 32, TextureFormat.RGBA5551)
                orange_im = getImageFile(7, 0x136, False, 32, 32, TextureFormat.RGBA5551)
                if settings.colorblind_mode == ColorblindMode.off:
                    match index:
                        case Kongs.donkey:
                            color_r = 255
                            color_g = 224
                            color_b = 8
                        case Kongs.diddy:
                            color_r = 255
                            color_g = 48
                            color_b = 32
                        case Kongs.lanky:
                            color_r = 40
                            color_g = 168
                            color_b = 255
                        case Kongs.tiny:
                            color_r = 216
                            color_g = 100
                            color_b = 248
                        case Kongs.chunky:
                            color_r = 0
                            color_g = 255
                            color_b = 0
                        case _:
                            color_r = 100
                            color_g = 255
                            color_b = 60
                    orange_im = maskImageWithColor(orange_im, (color_r, color_g, color_b))
                else:
                    orange_im = maskImageWithColor(orange_im, (0, 255, 0))  # Brighter green makes this more distinguishable for colorblindness
                dim_length = int(32 * ORANGE_SCALING)
                dim_offset = int((32 - dim_length) / 2)
                orange_im = orange_im.resize((dim_length, dim_length))
                base_im.paste(orange_im, (dim_offset, dim_offset), orange_im)
                writeColorImageToROM(base_im, 25, switch_faces[index], 32, 32, False, TextureFormat.RGBA5551)

def changeModelTextures(settings: Settings, kong_index: int):
    """Change the textures associated with a model."""
    settings_values = [
        settings.kong_model_dk,
        settings.kong_model_diddy,
        settings.kong_model_lanky,
        settings.kong_model_tiny,
        settings.kong_model_chunky,
    ]
    if kong_index < 0 or kong_index >= len(settings_values):
        return
    model = settings_values[kong_index]
    if model not in model_texture_sections:
        return
    for x in range(2):
        file = kong_index_mapping[kong_index][x]
        if file is None:
            continue
        krusha_model_start = js.pointer_addresses[5]["entries"][file]["pointing_to"]
        krusha_model_finish = js.pointer_addresses[5]["entries"][file + 1]["pointing_to"]
        krusha_model_size = krusha_model_finish - krusha_model_start
        ROM_COPY = LocalROM()
        ROM_COPY.seek(krusha_model_start)
        indicator = int.from_bytes(ROM_COPY.readBytes(2), "big")
        ROM_COPY.seek(krusha_model_start)
        data = ROM_COPY.readBytes(krusha_model_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Retexture for colors
        for tex_idx in model_texture_sections[model]["skin"]:
            for di, d in enumerate(int_to_list(krusha_texture_replacement[kong_index][0], 2)):  # Main
                num_data[tex_idx + di] = d
        for tex_idx in model_texture_sections[model]["kong"]:
            for di, d in enumerate(int_to_list(krusha_texture_replacement[kong_index][1], 2)):  # Belt
                num_data[tex_idx + di] = d
        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        LocalROM().seek(krusha_model_start)
        LocalROM().writeBytes(data)

def darkenDPad():
    """Change the DPad cross texture for the DPad HUD."""
    img = getImageFile(14, 187, True, 32, 32, TextureFormat.RGBA5551)
    px = img.load()
    bytes_array = []
    for y in range(32):
        for x in range(32):
            pix_data = list(px[x, y])
            if pix_data[0] > 245 and pix_data[1] > 245 and pix_data[2] > 245:
                # Main white bit
                pix_data[0] = 0
                pix_data[1] = 0
                pix_data[2] = 0
            elif pix_data[0] == 0 and pix_data[1] == 0 and pix_data[2] == 0:
                # Arrow impressions
                pix_data[0] = 0xAB
                pix_data[1] = 0xAB
                pix_data[2] = 0xAB
            value = 1 if pix_data[3] > 128 else 0
            for v in range(3):
                value |= (pix_data[v] >> 3) << 1 + (5 * (2 - v))
            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    px_data = gzip.compress(px_data, compresslevel=9)
    ROM().seek(js.pointer_addresses[14]["entries"][187]["pointing_to"])
    ROM().writeBytes(px_data)

def getValueFromByteArray(ba: bytearray, offset: int, size: int) -> int:
    """Get value from byte array given an offset and size."""
    value = 0
    for x in range(size):
        local_value = ba[offset + x]
        value <<= 8
        value += local_value
    return value


def getEnemySwapColor(channel_min: int = 0, channel_max: int = 255, min_channel_variance: int = 0) -> int:
    """Get an RGB color compatible with enemy swaps."""
    channels = []
    for _ in range(2):
        channels.append(random.randint(channel_min, channel_max))
    min_channel = min(channels[0], channels[1])
    max_channel = max(channels[0], channels[1])
    bounds = []
    if (min_channel - channel_min) >= min_channel_variance:
        bounds.append([channel_min, min_channel])
    if (channel_max - max_channel) >= min_channel_variance:
        bounds.append([max_channel, channel_max])
    if (len(bounds) == 0) or ((max_channel - min_channel) >= min_channel_variance):
        # Default to random number pick
        channels.append(random.randint(channel_min, channel_max))
    else:
        selected_bound = random.choice(bounds)
        channels.append(random.randint(selected_bound[0], selected_bound[1]))
    random.shuffle(channels)
    value = 0
    for x in range(3):
        value <<= 8
        value += channels[x]
    return value


class EnemyColorSwap:
    """Class to store information regarding an enemy color swap."""

    def __init__(self, search_for: list, forced_color: int = None):
        """Initialize with given parameters."""
        self.search_for = search_for.copy()
        total_channels = [0] * 3
        for color in self.search_for:
            for channel in range(3):
                shift = 8 * (2 - channel)
                value = (color >> shift) & 0xFF
                total_channels[channel] += value
        average_channels = [int(x / len(self.search_for)) for x in total_channels]
        self.average_color = 0
        for x in average_channels:
            self.average_color <<= 8
            self.average_color += x
        self.replace_with = forced_color
        if forced_color is None:
            self.replace_with = getEnemySwapColor(80, min_channel_variance=80)

    def getOutputColor(self, color: int):
        """Get output color based on randomization."""
        if color not in self.search_for:
            return color
        if color == self.search_for[0]:
            return self.replace_with
        new_color = 0
        total_boost = 0
        for x in range(3):
            shift = 8 * (2 - x)
            provided_channel = (color >> shift) & 0xFF
            primary_channel = (self.search_for[0] >> shift) & 0xFF
            boost = 1  # Failsafe for div by 0
            if primary_channel != 0:
                boost = provided_channel / primary_channel
            total_boost += boost  # Used to get an average
        for x in range(3):
            shift = 8 * (2 - x)
            replacement_channel = (self.replace_with >> shift) & 0xFF
            replacement_channel = int(replacement_channel * (total_boost / 3))
            if replacement_channel > 255:
                replacement_channel = 255
            elif replacement_channel < 0:
                replacement_channel = 0
            new_color <<= 8
            new_color += replacement_channel
        return new_color


def convertColorIntToTuple(color: int) -> tuple:
    """Convert color stored as 3-byte int to tuple."""
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


def getLuma(color: tuple) -> float:
    """Get the luma value of a color."""
    return (0.299 * color[0]) + (0.587 * color[1]) + (0.114 * color[2])


def adjustFungiMushVertexColor(shift: int):
    """Adjust the special vertex coloring on Fungi Giant Mushroom."""
    fungi_geo = bytearray(getRawFile(TableNames.MapGeometry, Maps.FungiForest, True))
    DEFAULT_MUSHROOM_COLOR = (255, 90, 82)
    NEW_MUSHROOM_COLOR = hueShiftColor(DEFAULT_MUSHROOM_COLOR, shift)
    for x in range(0x27DA, 0x2839):
        start = 0x25140 + (x * 0x10) + 0xC
        channels = []
        is_zero = True
        for y in range(3):
            val = fungi_geo[start + y]
            if val != 0:
                is_zero = False
            channels.append(val)
        if is_zero:
            continue
        visual_color = [int((x / 255) * DEFAULT_MUSHROOM_COLOR[xi]) for xi, x in enumerate(channels)]
        luma = int(getLuma(visual_color))
        # Diversify shading
        luma -= 128
        luma = int(luma * 1.2)
        luma += 128
        # Brighten
        luma += 60
        # Clamp
        if luma < 0:
            luma = 0
        elif luma > 255:
            luma = 255
        # Apply shading
        for y in range(3):
            fungi_geo[start + y] = luma
        fungi_geo[start + 3] = 0xFF
    file_data = gzip.compress(fungi_geo, compresslevel=9)
    ROM().seek(js.pointer_addresses[TableNames.MapGeometry]["entries"][Maps.FungiForest]["pointing_to"])
    ROM().writeBytes(file_data)


def writeMiscCosmeticChanges(settings):
    """Write miscellaneous changes to the cosmetic colors."""
    if settings.override_cosmetics:
        enemy_setting = RandomModels[js.document.getElementById("random_enemy_colors").value]
    else:
        enemy_setting = settings.random_enemy_colors
    if settings.misc_cosmetics:
        # Melon HUD
        data = {
            7: [[0x13C, 0x147]],
            14: [[0x5A, 0x5D]],
            25: [
                [getBonusSkinOffset(ExtraTextures.MelonSurface), getBonusSkinOffset(ExtraTextures.MelonSurface)],
                [0x144B, 0x1452],
            ],
        }
        shift = getRandomHueShift()
        for table in data:
            table_data = data[table]
            for set in table_data:
                for img in range(set[0], set[1] + 1):
                    if table == 25:
                        dims = (32, 32)
                    else:
                        dims = (48, 42)
                    melon_im = getImageFile(table, img, table != 7, dims[0], dims[1], TextureFormat.RGBA5551)
                    melon_im = hueShift(melon_im, shift)
                    melon_px = melon_im.load()
                    bytes_array = []
                    for y in range(dims[1]):
                        for x in range(dims[0]):
                            pix_data = list(melon_px[x, y])
                            red = int((pix_data[0] >> 3) << 11)
                            green = int((pix_data[1] >> 3) << 6)
                            blue = int((pix_data[2] >> 3) << 1)
                            alpha = int(pix_data[3] != 0)
                            value = red | green | blue | alpha
                            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
                    px_data = bytearray(bytes_array)
                    if table != 7:
                        px_data = gzip.compress(px_data, compresslevel=9)
                    ROM().seek(js.pointer_addresses[table]["entries"][img]["pointing_to"])
                    ROM().writeBytes(px_data)

        # Shockwave Particles
        shockwave_shift = getRandomHueShift()
        for img_index in range(0x174F, 0x1757):
            hueShiftImageContainer(25, img_index, 16, 16, TextureFormat.RGBA32, shockwave_shift)
        if settings.colorblind_mode == ColorblindMode.off:
            # Fire-based sprites
            fire_shift = getRandomHueShift()
            fires = (
                [0x1539, 0x1553, 32],  # Fireball. RGBA32 32x32
                [0x14B6, 0x14F5, 32],  # Fireball. RGBA32 32x32
                [0x1554, 0x155B, 16],  # Small Fireball. RGBA32 16x16
                [0x1654, 0x1683, 32],  # Fire Wall. RGBA32 32x32
                [0x1495, 0x14A0, 32],  # Small Explosion, RGBA32 32x32
                [0x13B9, 0x13C3, 32],  # Small Explosion, RGBA32 32x32
            )
            for sprite_data in fires:
                for img_index in range(sprite_data[0], sprite_data[1] + 1):
                    dim = sprite_data[2]
                    hueShiftImageContainer(25, img_index, dim, dim, TextureFormat.RGBA32, fire_shift)
            for img_index in range(0x29, 0x32 + 1):
                hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift)
            for img_index in range(0x250, 0x26F + 1):
                hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift)
            for img_index in range(0xA0, 0xA7 + 1):
                hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA5551, fire_shift)
            # Blue Fire
            for img_index in range(129, 138 + 1):
                hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift)
            # Number Game Numbers
            COLOR_COUNT = 2  # 2 or 16
            colors = [getRandomHueShift() for x in range(16)]
            # vanilla_green = [2, 4, 5, 7, 9, 10, 12, 13]
            vanilla_blue = [1, 3, 6, 8, 11, 14, 15, 16]
            for x in range(16):
                number_hue_shift = colors[0]
                if COLOR_COUNT == 2:
                    if (x + 1) in vanilla_blue:
                        number_hue_shift = colors[1]
                else:
                    number_hue_shift = colors[x]
                for sub_img in range(2):
                    img_index = 0x1FE + (2 * x) + sub_img
                    hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA5551, number_hue_shift)
            if COLOR_COUNT == 2:
                hueShiftImageContainer(25, 0xC2D, 32, 32, TextureFormat.RGBA5551, colors[1])
                hueShiftImageContainer(25, 0xC2E, 32, 32, TextureFormat.RGBA5551, colors[0])
        boulder_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x12F4, 1, 1372, TextureFormat.RGBA5551, boulder_shift)
        for img_index in range(2):
            hueShiftImageContainer(25, 0xDE1 + img_index, 32, 64, TextureFormat.RGBA5551, boulder_shift)

    if enemy_setting != RandomModels.off:
        # Barrel Enemy Skins - Random
        klobber_shift = getRandomHueShift(0, 300)
        kaboom_shift = getRandomHueShift()
        for img_index in range(3):
            px_count = 1404 if img_index < 2 else 1372
            hueShiftImageContainer(25, 0xF12 + img_index, 1, px_count, TextureFormat.RGBA5551, klobber_shift)
            hueShiftImageContainer(25, 0xF22 + img_index, 1, px_count, TextureFormat.RGBA5551, kaboom_shift)
            if img_index < 2:
                hueShiftImageContainer(25, 0xF2B + img_index, 1, px_count, TextureFormat.RGBA5551, kaboom_shift)
        # Klump
        klump_jacket_shift = getRandomHueShift()
        klump_hatammo_shift = getRandomHueShift()
        jacket_images = [
            {"image": 0x104D, "px": 1372},
            {"image": 0x1058, "px": 1372},
            {"image": 0x1059, "px": 176},
        ]
        hatammo_images = [
            {"image": 0x104E, "px": 1372},
            {"image": 0x104F, "px": 1372},
            {"image": 0x1050, "px": 1372},
            {"image": 0x1051, "px": 700},
            {"image": 0x1052, "px": 348},
            {"image": 0x1053, "px": 348},
        ]
        for img_data in jacket_images:
            hueShiftImageContainer(25, img_data["image"], 1, img_data["px"], TextureFormat.RGBA5551, klump_jacket_shift)
        for img_data in hatammo_images:
            hueShiftImageContainer(25, img_data["image"], 1, img_data["px"], TextureFormat.RGBA5551, klump_hatammo_shift)
        # Kosha
        kosha_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x1232, 1, 348, TextureFormat.RGBA5551, kosha_shift)
        hueShiftImageContainer(25, 0x1235, 1, 348, TextureFormat.RGBA5551, kosha_shift)
        if enemy_setting == RandomModels.extreme:
            kosha_helmet_int = getEnemySwapColor(80, min_channel_variance=80)
            kosha_helmet_list = [
                (kosha_helmet_int >> 16) & 0xFF,
                (kosha_helmet_int >> 8) & 0xFF,
                kosha_helmet_int & 0xFF,
            ]
            kosha_club_int = getEnemySwapColor(80, min_channel_variance=80)
            kosha_club_list = [(kosha_club_int >> 16) & 0xFF, (kosha_club_int >> 8) & 0xFF, kosha_club_int & 0xFF]
            for img in range(0x122E, 0x1230):
                kosha_im = getImageFile(25, img, True, 1, 1372, TextureFormat.RGBA5551)
                kosha_im = maskImageWithColor(kosha_im, tuple(kosha_helmet_list))
                writeColorImageToROM(kosha_im, 25, img, 1, 1372, False, TextureFormat.RGBA5551)
            for img in range(0x1229, 0x122C):
                kosha_im = getImageFile(25, img, True, 1, 1372, TextureFormat.RGBA5551)
                kosha_im = maskImageWithColor(kosha_im, tuple(kosha_club_list))
                writeColorImageToROM(kosha_im, 25, img, 1, 1372, False, TextureFormat.RGBA5551)
            if settings.colorblind_mode == ColorblindMode.off:
                # Kremling
                kremling_dimensions = [
                    [32, 64],  # FCE
                    [64, 24],  # FCF
                    [1, 1372],  # fd0
                    [32, 32],  # fd1
                    [24, 8],  # fd2
                    [24, 8],  # fd3
                    [24, 8],  # fd4
                    [24, 24],  # fd5
                    [32, 32],  # fd6
                    [32, 64],  # fd7
                    [32, 64],  # fd8
                    [36, 16],  # fd9
                    [20, 28],  # fda
                    [32, 32],  # fdb
                    [32, 32],  # fdc
                    [12, 28],  # fdd
                    [64, 24],  # fde
                    [32, 32],  # fdf
                ]
                while True:
                    kremling_shift = getRandomHueShift()
                    # Block red coloring
                    if kremling_shift > 290:
                        break
                    if kremling_shift > -70 and kremling_shift < 228:
                        break
                    if kremling_shift < -132:
                        break
                for dim_index, dims in enumerate(kremling_dimensions):
                    if dims is not None:
                        hueShiftImageContainer(25, 0xFCE + dim_index, dims[0], dims[1], TextureFormat.RGBA5551, kremling_shift)
            # Rabbit
            rabbit_dimensions = [
                [1, 1372],  # 111A
                [1, 1372],  # 111B
                [1, 700],  # 111C
                [1, 700],  # 111D
                [1, 1372],  # 111E
                [1, 1372],  # 111F
                [1, 1372],  # 1120
                [1, 1404],  # 1121
                [1, 348],  # 1122
                [32, 64],  # 1123
                [1, 688],  # 1124
                [64, 32],  # 1125
            ]
            rabbit_shift = getRandomHueShift()
            for dim_index, dims in enumerate(rabbit_dimensions):
                if dims is not None:
                    hueShiftImageContainer(25, 0x111A + dim_index, dims[0], dims[1], TextureFormat.RGBA5551, rabbit_shift)
            # Snake
            snake_shift = getRandomHueShift()
            for x in range(2):
                hueShiftImageContainer(25, 0xEF7 + x, 32, 32, TextureFormat.RGBA5551, snake_shift)
        # Headphones Sprite
        headphones_shift = getRandomHueShift()
        for x in range(8):
            hueShiftImageContainer(7, 0x3D3 + x, 40, 40, TextureFormat.RGBA5551, headphones_shift)
        # Instruments
        trombone_sax_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xEA2, 32, 32, TextureFormat.RGBA5551, trombone_sax_shift)  # Shine
        hueShiftImageContainer(25, 0x15AF, 40, 40, TextureFormat.RGBA5551, trombone_sax_shift)  # Trombone Icon
        hueShiftImageContainer(25, 0x15AD, 40, 40, TextureFormat.RGBA5551, trombone_sax_shift)  # Sax Icon
        hueShiftImageContainer(25, 0xBCC, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift)  # Sax (Pad)
        hueShiftImageContainer(25, 0xBCD, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift)  # Sax (Pad)
        hueShiftImageContainer(25, 0xBD0, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift)  # Trombone (Pad)
        hueShiftImageContainer(25, 0xBD1, 32, 64, TextureFormat.RGBA5551, trombone_sax_shift)  # Trombone (Pad)
        triangle_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xEBF, 32, 32, TextureFormat.RGBA5551, triangle_shift)  # Shine
        hueShiftImageContainer(25, 0x15AE, 40, 40, TextureFormat.RGBA5551, triangle_shift)  # Triangle Icon
        hueShiftImageContainer(25, 0xBCE, 32, 64, TextureFormat.RGBA5551, triangle_shift)  # Triangle (Pad)
        hueShiftImageContainer(25, 0xBCF, 32, 64, TextureFormat.RGBA5551, triangle_shift)  # Triangle (Pad)
        bongo_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x1317, 1, 1372, TextureFormat.RGBA5551, bongo_shift)  # Skin
        hueShiftImageContainer(25, 0x1318, 1, 1404, TextureFormat.RGBA5551, bongo_shift)  # Side
        hueShiftImageContainer(25, 0x1319, 1, 1404, TextureFormat.RGBA5551, bongo_shift)  # Side 2
        hueShiftImageContainer(25, 0x15AC, 40, 40, TextureFormat.RGBA5551, bongo_shift)  # Bongo Icon
        hueShiftImageContainer(25, 0xBC8, 32, 64, TextureFormat.RGBA5551, bongo_shift)  # Bongo (Pad)
        hueShiftImageContainer(25, 0xBC9, 32, 64, TextureFormat.RGBA5551, bongo_shift)  # Bongo (Pad)
        if enemy_setting == RandomModels.extreme:
            # Beanstalk
            beanstalk_unc_size = [
                0x480,
                0x480,
                0x480,
                0x2B8,
                0xAC0,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAF8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAF8,
                0x578,
                0xAB8,
                0x578,
                0x5F8,
                0xAB8,
                0xAB8,
                0xAB8,
                0xAB8,
                0x578,
                0xAB8,
                0xAF8,
                0xAB8,
                0xAB8,
                0x560,
                0xAB8,
                0x2B8,
            ]
            beanstalk_shift = getRandomHueShift()
            for index, size in enumerate(beanstalk_unc_size):
                hueShiftImageContainer(25, 0x1126 + index, 1, int(size >> 1), TextureFormat.RGBA5551, beanstalk_shift)
        # Fairy Particles Sprites
        fairy_particles_shift = getRandomHueShift()
        for x in range(0xB):
            hueShiftImageContainer(25, 0x138D + x, 32, 32, TextureFormat.RGBA32, fairy_particles_shift)
        race_coin_shift = getRandomHueShift()
        for x in range(8):
            hueShiftImageContainer(7, 0x1F0 + x, 48, 42, TextureFormat.RGBA5551, race_coin_shift)
        scoff_shift = getRandomHueShift()
        troff_shift = getRandomHueShift()
        scoff_data = {
            0xFB8: 0x55C,
            0xFB9: 0x800,
            0xFBA: 0x40,
            0xFBB: 0x800,
            0xFBC: 0x240,
            0xFBD: 0x480,
            0xFBE: 0x80,
            0xFBF: 0x800,
            0xFC0: 0x200,
            0xFC1: 0x240,
            0xFC2: 0x100,
            0xFB2: 0x240,
            0xFB3: 0x800,
            0xFB4: 0x800,
            0xFB5: 0x200,
            0xFB6: 0x200,
            0xFB7: 0x200,
        }
        troff_data = {
            0xF78: 0x800,
            0xF79: 0x800,
            0xF7A: 0x800,
            0xF7B: 0x800,
            0xF7C: 0x800,
            0xF7D: 0x400,
            0xF7E: 0x600,
            0xF7F: 0x400,
            0xF80: 0x800,
            0xF81: 0x600,
            0xF82: 0x400,
            0xF83: 0x400,
            0xF84: 0x800,
            0xF85: 0x800,
            0xF86: 0x280,
            0xF87: 0x180,
            0xF88: 0x800,
            0xF89: 0x800,
            0xF8A: 0x400,
            0xF8B: 0x300,
            0xF8C: 0x800,
            0xF8D: 0x400,
            0xF8E: 0x500,
            0xF8F: 0x180,
        }
        for img in scoff_data:
            hueShiftImageContainer(25, img, 1, scoff_data[img], TextureFormat.RGBA5551, scoff_shift)

        # Scoff had too many bananas, and passed potassium poisoning onto Troff
        # https://i.imgur.com/WFDLSzA.png
        # for img in troff_data:
        #     hueShiftImageContainer(25, img, 1, troff_data[img], TextureFormat.RGBA5551, troff_shift)
        # Krobot
        spinner_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xFA9, 1, 1372, TextureFormat.RGBA5551, spinner_shift)
        krobot_textures = [[[1, 1372], [0xFAF, 0xFAA, 0xFA8, 0xFAB, 0xFAD]], [[32, 32], [0xFAC, 0xFB1, 0xFAE, 0xFB0]]]
        krobot_color_int = getEnemySwapColor(80, min_channel_variance=80)
        krobot_color_list = [(krobot_color_int >> 16) & 0xFF, (krobot_color_int >> 8) & 0xFF, krobot_color_int & 0xFF]
        for tex_set in krobot_textures:
            for tex in tex_set[1]:
                krobot_im = getImageFile(25, tex, True, tex_set[0][0], tex_set[0][1], TextureFormat.RGBA5551)
                krobot_im = maskImageWithColor(krobot_im, tuple(krobot_color_list))
                writeColorImageToROM(krobot_im, 25, tex, tex_set[0][0], tex_set[0][1], False, TextureFormat.RGBA5551)
        # Jetman
        for xi, x in enumerate(settings.jetman_color):
            ROM().seek(settings.rom_data + 0x1E8 + xi)
            ROM().writeMultipleBytes(x, 1)
        # Blast Barrels
        blast_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x127E, 1, 1372, TextureFormat.RGBA5551, blast_shift)
        for x in range(4):
            hueShiftImageContainer(25, 0x127F + x, 16, 64, TextureFormat.RGBA5551, blast_shift)
        hueShiftImageContainer(25, getBonusSkinOffset(ExtraTextures.BlastTop), 1, 1372, TextureFormat.RGBA5551, blast_shift)
        # K Rool
        red_cs_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        shorts_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        glove_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor()))
        krool_data = {
            0x1149: red_cs_im,
            0x1261: shorts_im,
            0xDA8: glove_im,
        }
        if enemy_setting == RandomModels.extreme:
            skin_im = Image.new(mode="RGBA", size=(32, 32), color=convertColorIntToTuple(getEnemySwapColor(80, min_channel_variance=80)))
            krool_data[0x114A] = skin_im
            krool_data[0x114D] = skin_im
        for index in krool_data:
            writeColorImageToROM(krool_data[index], 25, index, 32, 32, False, TextureFormat.RGBA5551)
        toe_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0x126E, 1, 1372, TextureFormat.RGBA5551, toe_shift)
        hueShiftImageContainer(25, 0x126F, 1, 1372, TextureFormat.RGBA5551, toe_shift)
        if enemy_setting == RandomModels.extreme:
            gold_shift = getRandomHueShift()
            hueShiftImageContainer(25, 0x1265, 32, 32, TextureFormat.RGBA5551, gold_shift)
            hueShiftImageContainer(25, 0x1148, 32, 32, TextureFormat.RGBA5551, gold_shift)
        # Ghost
        ghost_shift = getRandomHueShift()
        for img in range(0x119D, 0x11AF):
            px_count = 1372
            if img == 0x119E:
                px_count = 176
            elif img == 0x11AC:
                px_count = 688
            hueShiftImageContainer(25, img, 1, px_count, TextureFormat.RGBA5551, ghost_shift)
        # Funky
        funky_shift = getRandomHueShift()
        hueShiftImageContainer(25, 0xECF, 1, 1372, TextureFormat.RGBA5551, funky_shift)
        hueShiftImageContainer(25, 0xED6, 1, 1372, TextureFormat.RGBA5551, funky_shift)
        hueShiftImageContainer(25, 0xEDF, 1, 1372, TextureFormat.RGBA5551, funky_shift)
        # Zinger
        zinger_shift = getRandomHueShift()
        zinger_color = hueShiftColor((0xFF, 0xFF, 0x0A), zinger_shift)
        zinger_color_int = (zinger_color[0] << 16) | (zinger_color[1] << 8) | (zinger_color[2])
        hueShiftImageContainer(25, 0xF0A, 1, 1372, TextureFormat.RGBA5551, zinger_shift)
        # Mechazinger, use zinger color
        for img_index in (0x10A0, 0x10A2, 0x10A4, 0x10A5):
            hueShiftImageContainer(25, img_index, 1, 1372, TextureFormat.RGBA5551, zinger_shift)
        hueShiftImageContainer(25, 0x10A3, 32, 32, TextureFormat.RGBA32, zinger_shift)
        # Rings/DK Star
        ring_shift = getRandomHueShift()
        for x in range(2):
            hueShiftImageContainer(25, 0xE1C + x, 1, 344, TextureFormat.RGBA5551, ring_shift)
            hueShiftImageContainer(25, 0xD38 + x, 64, 32, TextureFormat.RGBA5551, ring_shift)
        hueShiftImageContainer(7, 0x2EB, 32, 32, TextureFormat.RGBA5551, ring_shift)
        # Buoys
        for x in range(2):
            hueShiftImageContainer(25, 0x133A + x, 1, 1372, TextureFormat.RGBA5551, getRandomHueShift())
        # Trap Bubble
        hueShiftImageContainer(25, 0x134C, 32, 32, TextureFormat.RGBA5551, getRandomHueShift())
        # Spider
        spider_shift = getRandomHueShift()
        spider_dims = {
            0x110A: (32, 64),
            0x110B: (32, 64),
            0x110C: (32, 64),
            0x110D: (64, 16),
            0x110E: (32, 64),
            0x110F: (32, 64),
            0x1110: (32, 64),
            0x1111: (32, 64),
            0x1112: (32, 64),
            0x1113: (16, 32),
            0x1114: (32, 32),
            0x1115: (32, 32),
            0x1116: (32, 32),
            0x1117: (64, 16),
            0x1118: (64, 32),
            0x1119: (64, 32),
        }
        for img_index in spider_dims:
            hueShiftImageContainer(
                25,
                img_index,
                spider_dims[img_index][0],
                spider_dims[img_index][1],
                TextureFormat.RGBA5551,
                spider_shift,
            )

        if enemy_setting == RandomModels.extreme:
            # Army Dillo
            dillo_px_count = {
                0x102D: 64 * 32,
                0x103A: 16 * 16,
                0x102A: 24 * 24,
                0x102B: 24 * 24,
                0x102C: 1372,
                0x103D: 688,
                0x103E: 688,
            }
            dillo_shift = getRandomHueShift()
            for img, px_count in dillo_px_count.items():
                hueShiftImageContainer(25, img, 1, px_count, TextureFormat.RGBA5551, dillo_shift)

        # Mushrooms
        mush_man_shift = getRandomHueShift()
        for img_index in (0x11FC, 0x11FD, 0x11FE, 0x11FF, 0x1200, 0x1209, 0x120A, 0x120B):
            hueShiftImageContainer(25, img_index, 1, 1372, TextureFormat.RGBA5551, mush_man_shift)
        for img_index in (0x11F8, 0x1205):
            hueShiftImageContainer(25, img_index, 1, 692, TextureFormat.RGBA5551, mush_man_shift)
        for img_index in (0x67F, 0x680):
            hueShiftImageContainer(25, img_index, 32, 64, TextureFormat.RGBA5551, mush_man_shift)
        hueShiftImageContainer(25, 0x6F3, 4, 4, TextureFormat.RGBA5551, mush_man_shift)
        adjustFungiMushVertexColor(mush_man_shift)

        # Enemy Vertex Swaps
        blue_beaver_color = getEnemySwapColor(80, min_channel_variance=80)
        enemy_changes = {
            Model.BeaverBlue_LowPoly: EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color),  # Primary
            Model.BeaverBlue: EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color),  # Primary
            Model.BeaverGold: EnemyColorSwap([0xFFE5B2, 0xFFCC65, 0xE8AB00, 0x824E00, 0xD18B00, 0x331300, 0xCE9116]),  # Primary
            Model.Zinger: EnemyColorSwap([0xFFFF0A, 0xFF7F00], zinger_color_int),  # Legs
            Model.RoboZinger: EnemyColorSwap([0xFFFF00, 0xFF5500], zinger_color_int),  # Legs
            Model.Candy: EnemyColorSwap(
                [
                    0xFF96EB,
                    0x572C58,
                    0xB86CAA,
                    0xEB4C91,
                    0x8B2154,
                    0xD13B80,
                    0xFF77C1,
                    0xFF599E,
                    0x7F1E4C,
                    0x61173A,
                    0x902858,
                    0xA42E64,
                    0x791C49,
                    0x67183E,
                    0x9E255C,
                    0xC12E74,
                    0x572C58,
                    0xFF96EB,
                    0xB86CAA,
                ]
            ),
            Model.Laser: EnemyColorSwap([0xF30000]),
            Model.Kasplat: EnemyColorSwap([0x8FD8FF, 0x182A4F, 0x0B162C, 0x7A98D3, 0x3F6CC4, 0x8FD8FF, 0x284581]),
            # Model.BananaFairy: EnemyColorSwap([0xFFD400, 0xFFAA00, 0xFCD200, 0xD68F00, 0xD77D0A, 0xe49800, 0xdf7f1f, 0xa26c00, 0xd6b200, 0xdf9f1f])
        }
        if enemy_setting == RandomModels.extreme:
            enemy_changes[Model.Klump] = EnemyColorSwap([0xE66B78, 0x621738, 0x300F20, 0xD1426F, 0xA32859])
            dogadon_color = getEnemySwapColor(80, 160, min_channel_variance=80)
            enemy_changes[Model.Dogadon] = EnemyColorSwap(
                [
                    0xFF0000,
                    0xFF7F00,
                    0x450A1F,
                    0xB05800,
                    0xFF3200,
                    0xFFD400,
                    0x4F260D,
                    0x600F00,
                    0x6A1400,
                    0xAA0000,
                    0xDF3F1F,
                    0xFF251F,
                    0x8F4418,
                    0x522900,
                    0xDF9F1F,
                    0x3B0606,
                    0x91121E,
                    0x700C0D,
                    0xFF5900,
                    0xFF7217,
                    0xFF7425,
                    0xFF470B,
                    0xA82100,
                    0x4A0D18,
                    0x580E00,
                    0x461309,
                    0x4C1503,
                    0x780D0E,
                    0xFFA74A,
                    0x7E120F,
                    0x700000,
                    0xB64D19,
                    0x883A13,
                    0xBD351A,
                    0xD42900,
                    0xFF2A00,
                    0x921511,
                    0x9C662D,
                    0xDF5F1F,
                    0x9B1112,
                    0x461F0A,
                    0x4B0808,
                    0x500809,
                    0xA42000,
                    0x5F0B13,
                    0xBF6A3F,
                    0x602E10,
                    0x971414,
                    0x422C15,
                    0xFC5800,
                    0x5C0D0B,
                ],
                dogadon_color,
            )
        for enemy in enemy_changes:
            file_data = bytearray(getRawFile(5, enemy, True))
            vert_start = 0x28
            file_head = getValueFromByteArray(file_data, 0, 4)
            disp_list_end = (getValueFromByteArray(file_data, 4, 4) - file_head) + 0x28
            vert_end = (getValueFromByteArray(file_data, disp_list_end, 4) - file_head) + 0x28
            vert_count = int((vert_end - vert_start) / 0x10)
            for vert in range(vert_count):
                local_start = 0x28 + (0x10 * vert)
                test_rgb = getValueFromByteArray(file_data, local_start + 0xC, 3)
                new_rgb = enemy_changes[enemy].getOutputColor(test_rgb)
                for x in range(3):
                    shift = 8 * (2 - x)
                    channel = (new_rgb >> shift) & 0xFF
                    file_data[local_start + 0xC + x] = channel
            file_data = gzip.compress(file_data, compresslevel=9)
            ROM().seek(js.pointer_addresses[5]["entries"][enemy]["pointing_to"])
            ROM().writeBytes(file_data)

def applyHelmDoorCosmetics(settings: Settings) -> None:
    """Apply Helm Door Cosmetic Changes."""
    crown_door_required_item = settings.crown_door_item
    coin_door_required_item = settings.coin_door_item
    Doors = [
        HelmDoorSetting(crown_door_required_item, settings.crown_door_item_count, 6022, 6023),
        HelmDoorSetting(coin_door_required_item, settings.coin_door_item_count, 6024, 6025),
    ]
    Images = [
        HelmDoorImages(BarrierItems.GoldenBanana, [0x155C]),
        HelmDoorImages(BarrierItems.Blueprint, [x + 4 for x in (0x15F8, 0x15E8, 0x158F, 0x1600, 0x15F0)], False, 25, (48, 42)),
        HelmDoorImages(BarrierItems.Bean, [6020], False, 25, (64, 32)),
        HelmDoorImages(BarrierItems.Pearl, [0xD5F], False, 25, (32, 32)),
        HelmDoorImages(BarrierItems.Fairy, [0x16ED], False, 25, (32, 32), TextureFormat.RGBA32),
        HelmDoorImages(BarrierItems.Key, [5877]),
        HelmDoorImages(BarrierItems.Medal, [0x156C]),
        HelmDoorImages(BarrierItems.RainbowCoin, [5963], False, 25, (48, 42)),
        HelmDoorImages(BarrierItems.Crown, [5893]),
        HelmDoorImages(BarrierItems.CompanyCoin, [5905, 5912]),
    ]
    for door in Doors:
        for image_data in Images:
            if image_data.setting == door.item_setting:
                base = Image.new(mode="RGBA", size=(44, 44))
                base_overlay = Image.new(mode="RGBA", size=image_data.dimensions)
                for image_slot, image in enumerate(image_data.image_indexes):
                    item_im = getImageFile(
                        image_data.table,
                        image,
                        image_data.table in (14, 25),
                        image_data.dimensions[0],
                        image_data.dimensions[1],
                        image_data.format,
                    )
                    start_x = 0
                    finish_x = image_data.dimensions[0]
                    if len(image_data.image_indexes) > 1:
                        start_x = int(image_slot * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        finish_x = int((image_slot + 1) * (image_data.dimensions[0] / len(image_data.image_indexes)))
                        item_im = item_im.crop((start_x, 0, finish_x, image_data.dimensions[1]))
                    base_overlay.paste(item_im, (start_x, 0), item_im)
                if image_data.flip:
                    base_overlay = base_overlay.transpose(Image.FLIP_TOP_BOTTOM)
                if image_data.dimensions[0] > image_data.dimensions[1]:
                    # Width shrinked to 44
                    new_height = image_data.dimensions[1] * (44 / image_data.dimensions[0])
                    base_overlay = base_overlay.resize((44, int(new_height)))
                    base.paste(base_overlay, (0, int(22 - (new_height / 2))), base_overlay)
                else:
                    # Height shrinked to 44
                    new_width = image_data.dimensions[0] * (44 / image_data.dimensions[1])
                    base_overlay = base_overlay.resize((int(new_width), 44))
                    base.paste(base_overlay, (int(22 - (new_width / 2)), 0), base_overlay)
                if door.item_setting == BarrierItems.Pearl:
                    pearl_mask_im = Image.new("RGBA", (44, 44), (0, 0, 0, 255))
                    draw = ImageDraw.Draw(pearl_mask_im)
                    draw.ellipse((0, 0, 43, 43), fill=(0, 0, 0, 0), outline=(0, 0, 0, 0))
                    pix_pearl = base.load()
                    for y in range(44):
                        for x in range(44):
                            r, g, b, a = pearl_mask_im.getpixel((x, y))
                            if a > 128:
                                pix_pearl[x, y] = (0, 0, 0, 0)
                writeColorImageToROM(base, 25, door.item_image, 44, 44, True, TextureFormat.RGBA5551)
                writeColorImageToROM(
                    numberToImage(door.count, (44, 44)).transpose(Image.FLIP_TOP_BOTTOM),
                    25,
                    door.number_image,
                    44,
                    44,
                    True,
                    TextureFormat.RGBA5551,
                )

def darkenPauseBubble(settings: Settings):
    """Change the brightness of the text bubble used for the pause menu for dark mode."""
    if not settings.dark_mode_textboxes:
        return
    img = getImageFile(14, 107, True, 48, 32, TextureFormat.RGBA5551)
    px = img.load()
    canary_px = list(px[24, 16])
    if canary_px[0] < 128 and canary_px[1] < 128 and canary_px[2] < 128:
        # Already darkened, cancel
        return
    bytes_array = []
    for y in range(32):
        for x in range(48):
            pix_data = list(px[x, y])
            value = 1 if pix_data[3] > 128 else 0
            for v in range(3):
                pix_data[v] = 0xFF - pix_data[v]
                value |= (pix_data[v] >> 3) << 1 + (5 * (2 - v))
            bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    px_data = gzip.compress(px_data, compresslevel=9)
    ROM().seek(js.pointer_addresses[14]["entries"][107]["pointing_to"])
    ROM().writeBytes(px_data)


class WinConData:
    """Class to store information about win condition."""

    def __init__(self, table: int, image: int, tex_format: TextureFormat, width: int, height: int, flip: bool, default_count: int):
        """Initialize with given parameters."""
        self.table = table
        self.image = image
        self.tex_format = tex_format
        self.width = width
        self.height = height
        self.flip = flip
        self.default_count = default_count


def showWinCondition(settings: Settings):
    """Alter the image that's shown on the main menu to display the win condition."""
    win_con = settings.win_condition_item
    if win_con == WinConditionComplex.beat_krool:
        # Default, don't alter image
        return
    if win_con == WinConditionComplex.get_key8:
        output_image = Image.open(BytesIO(js.getFile("./base-hack/assets/displays/key8.png")))
        output_image = output_image.resize((32, 32))
        writeColorImageToROM(output_image, 14, 195, 32, 32, False, TextureFormat.RGBA5551)
        return
    if win_con == WinConditionComplex.req_bean:
        output_image = Image.open(BytesIO(js.getFile("./base-hack/assets/arcade_jetpac/arcade/bean.png")))
        output_image = output_image.resize((32, 32))
        writeColorImageToROM(output_image, 14, 195, 32, 32, False, TextureFormat.RGBA5551)
        return
    if win_con == WinConditionComplex.krem_kapture:
        item_im = getImageFile(14, 0x90, True, 32, 32, TextureFormat.RGBA5551)
        writeColorImageToROM(item_im, 14, 195, 32, 32, False, TextureFormat.RGBA5551)
        return
    if win_con == WinConditionComplex.dk_rap_items:
        item_im = getImageFile(7, 0x3D3, False, 40, 40, TextureFormat.RGBA5551)
        item_im = item_im.resize((32, 32)).transpose(Image.FLIP_TOP_BOTTOM)
        writeColorImageToROM(item_im, 14, 195, 32, 32, False, TextureFormat.RGBA5551)
        return
    win_con_data = {
        WinConditionComplex.req_bp: WinConData(25, 0x1593, TextureFormat.RGBA5551, 48, 42, True, 40),
        WinConditionComplex.req_medal: WinConData(25, 0x156C, TextureFormat.RGBA5551, 44, 44, True, 40),
        WinConditionComplex.req_fairy: WinConData(25, 0x16ED, TextureFormat.RGBA32, 32, 32, True, 20),
        WinConditionComplex.req_key: WinConData(25, 0x16F6, TextureFormat.RGBA5551, 44, 44, True, 8),
        WinConditionComplex.req_companycoins: WinConData(25, 0x1718, TextureFormat.RGBA5551, 44, 44, True, 2),
        WinConditionComplex.req_crown: WinConData(25, 0x1707, TextureFormat.RGBA5551, 44, 44, True, 10),
        WinConditionComplex.req_gb: WinConData(25, 0x155C, TextureFormat.RGBA5551, 44, 44, True, 201),
        WinConditionComplex.req_pearl: WinConData(25, 0, TextureFormat.RGBA5551, 44, 44, True, 5),
        WinConditionComplex.req_rainbowcoin: WinConData(25, 0x174B, TextureFormat.RGBA5551, 48, 42, True, 16),
    }
    if win_con not in win_con_data:
        return
    item_data = win_con_data[win_con]
    if win_con == WinConditionComplex.req_pearl:
        base_im = Image.open(BytesIO(js.getFile("./base-hack/assets/arcade_jetpac/arcade/pearl.png")))
    else:
        item_im = getImageFile(
            item_data.table,
            item_data.image,
            item_data.table != 7,
            item_data.width,
            item_data.height,
            item_data.tex_format,
        )
        if item_data.flip:
            item_im = item_im.transpose(Image.FLIP_TOP_BOTTOM)
        dim = max(item_data.width, item_data.height)
        base_im = Image.new(mode="RGBA", size=(dim, dim))
        base_im.paste(item_im, (int((dim - item_data.width) >> 1), int((dim - item_data.height) >> 1)), item_im)
    base_im = base_im.resize((32, 32))
    num_im = numberToImage(settings.win_condition_count, (20, 20))
    base_im.paste(num_im, (6, 6), num_im)
    writeColorImageToROM(base_im, 14, 195, 32, 32, False, TextureFormat.RGBA5551)

def randomizePlants(ROM_COPY: ROM, settings: Settings):
    """Randomize the plants in the setup file."""
    if not settings.misc_cosmetics:
        return

    flowers = [0x05, 0x08, 0x43]
    for x in range(0x1F1 - 0x1DE):
        flowers.append(0x1DE + x)
    maps_that_contain_flowers = [
        Maps.JungleJapes,
        Maps.JungleJapesLobby,
        Maps.TrainingGrounds,
        Maps.JapesTinyHive,
        Maps.AngryAztec,
        Maps.Isles,
        Maps.BananaFairyRoom,
    ]
    for map_id in maps_that_contain_flowers:
        setup_file = js.pointer_addresses[TableNames.Setups]["entries"][map_id]["pointing_to"]
        ROM_COPY.seek(setup_file)
        model2_count = int.from_bytes(ROM_COPY.readBytes(4), "big")
        for model2_item in range(model2_count):
            item_start = setup_file + 4 + (model2_item * 0x30)
            ROM_COPY.seek(item_start + 0x28)
            item_type = int.from_bytes(ROM_COPY.readBytes(2), "big")
            if item_type in flowers:
                ROM_COPY.seek(item_start + 0x28)
                ROM_COPY.writeMultipleBytes(random.choice(flowers), 2)
