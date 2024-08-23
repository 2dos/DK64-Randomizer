"""Apply cosmetic skins to kongs."""

from __future__ import annotations

import gzip
import random
import zlib
from random import randint
from typing import TYPE_CHECKING, List, Tuple
from enum import IntEnum, auto
from io import BytesIO

from PIL import Image, ImageDraw, ImageEnhance

import js
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Settings import CharacterColors, ColorblindMode, RandomModels, KongModels, WinConditionComplex
from randomizer.Enums.Models import Model
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Types import BarrierItems
from randomizer.Patching.generate_kong_color_images import convertColors
from randomizer.Patching.Lib import (
    float_to_hex,
    getObjectAddress,
    int_to_list,
    intf_to_float,
    PaletteFillType,
    SpawnerChange,
    applyCharacterSpawnerChanges,
    compatible_background_textures,
    grabText,
    writeText,
    TableNames,
    getRawFile,
    writeRawFile,
)
from randomizer.Patching.LibImage import getImageFile, TextureFormat, getRandomHueShift, hueShift
from randomizer.Patching.Patcher import ROM, LocalROM
from randomizer.Settings import Settings

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
        self, setting: BarrierItems, image_indexes: List[int], flip: bool = False, table: int = 25, dimensions: Tuple[int, int] = (44, 44), format: TextureFormat = TextureFormat.RGBA5551
    ) -> None:
        """Initialize with given parameters."""
        self.setting = setting
        self.image_indexes = image_indexes
        self.flip = flip
        self.table = table
        self.dimensions = dimensions
        self.format = format


turtle_models = [
    Model.Diddy,  # Diddy
    Model.DK,  # DK
    Model.Lanky,  # Lanky
    Model.Tiny,  # Tiny
    Model.Chunky,  # Regular Chunky
    Model.ChunkyDisco,  # Disco Chunky
    Model.Cranky,  # Cranky
    Model.Funky,  # Funky
    Model.Candy,  # Candy
    Model.Seal,  # Seal
    Model.Enguarde,  # Enguarde
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Squawks_28,  # Squawks
    Model.KlaptrapGreen,  # Klaptrap Green
    Model.KlaptrapPurple,  # Klaptrap Purple
    Model.KlaptrapRed,  # Klaptrap Red
    Model.KlaptrapTeeth,  # Klaptrap Teeth
    Model.SirDomino,  # Sir Domino
    Model.MrDice_41,  # Mr Dice
    Model.Beetle,  # Beetle
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.ToyCar,  # Toy Car
    Model.BananaFairy,  # Fairy
    Model.Shuri,  # Starfish
    Model.Gimpfish,  # Gimpfish
    Model.Spider,  # Spider
    Model.Rabbit,  # Rabbit
    Model.KRoolCutscene,  # K Rool
    Model.SkeletonHead,  # Skeleton Head
    Model.Vulture_76,  # Vulture
    Model.Vulture_77,  # Racing Vulture
    Model.Tomato,  # Tomato
    Model.Fly,  # Fly
    Model.SpotlightFish,  # Spotlight Fish
    Model.Puftup,  # Pufftup
    Model.CuckooBird,  # Cuckoo Bird
    Model.IceTomato,  # Ice Tomato
    Model.Boombox,  # Boombox
    Model.KRoolFight,  # K Rool (Boxing)
    Model.Microphone,  # Microbuffer
    Model.DeskKRool,  # K Rool's Desk
    Model.Bell,  # Bell
    Model.BonusBarrel,  # Bonus Barrel
    Model.HunkyChunkyBarrel,  # HC Barrel
    Model.MiniMonkeyBarrel,  # MM Barrel
    Model.TNTBarrel,  # TNT Barrel
    Model.Rocketbarrel,  # RB Barrel
    Model.StrongKongBarrel,  # SK Barrel
    Model.OrangstandSprintBarrel,  # OSS Barrel
    Model.BBBSlot_143,  # BBB Slot
    Model.PlayerCar,  # Tiny Car
    Model.Boulder,  # Boulder
    Model.Boat_158,  # Boat
    Model.Potion,  # Potion
    Model.ArmyDilloMissle,  # AD Missile
    Model.TagBarrel,  # Tag Barrel
    Model.QuestionMark,  # Question Mark
    Model.Krusha,  # Krusha
    Model.BananaPeel,  # Banana Peel
    Model.Butterfly,  # Butterfly
    Model.FunkyGun,  # Funky's Gun
]

panic_models = [
    Model.Diddy,  # Diddy
    Model.DK,  # DK
    Model.Lanky,  # Lanky
    Model.Tiny,  # Tiny
    Model.Chunky,  # Regular Chunky
    Model.ChunkyDisco,  # Disco Chunky
    Model.Cranky,  # Cranky
    Model.Funky,  # Funky
    Model.Candy,  # Candy
    Model.Seal,  # Seal
    Model.Enguarde,  # Enguarde
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Squawks_28,  # Squawks
    Model.KlaptrapGreen,  # Klaptrap Green
    Model.KlaptrapPurple,  # Klaptrap Purple
    Model.KlaptrapRed,  # Klaptrap Red
    Model.MadJack,  # Mad Jack
    Model.Troff,  # Troff
    Model.SirDomino,  # Sir Domino
    Model.MrDice_41,  # Mr Dice
    Model.RoboKremling,  # Robo Kremling
    Model.Scoff,  # Scoff
    Model.Beetle,  # Beetle
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.ToyCar,  # Toy Car
    Model.Klump,  # Klump
    Model.Dogadon,  # Dogadon
    Model.BananaFairy,  # Fairy
    Model.Guard,  # Guard
    Model.Shuri,  # Starfish
    Model.Gimpfish,  # Gimpfish
    Model.KLumsy,  # K Lumsy
    Model.Spider,  # Spider
    Model.Rabbit,  # Rabbit
    # Model.Beanstalk,  # Beanstalk
    Model.KRoolCutscene,  # K Rool
    Model.SkeletonHead,  # Skeleton Head
    Model.Vulture_76,  # Vulture
    Model.Vulture_77,  # Racing Vulture
    Model.Ghost,  # Ghost
    Model.Fly,  # Fly
    Model.FlySwatter_83,  # Fly Swatter
    Model.Owl,  # Owl
    Model.Book,  # Book
    Model.SpotlightFish,  # Spotlight Fish
    Model.Puftup,  # Pufftup
    Model.Mermaid,  # Mermaid
    Model.Mushroom,  # Mushroom Man
    Model.Worm,  # Worm
    Model.EscapeShip,  # Escape Ship
    Model.KRoolFight,  # K Rool (Boxing)
    Model.Microphone,  # Microbuffer
    Model.BonusBarrel,  # Bonus Barrel
    Model.HunkyChunkyBarrel,  # HC Barrel
    Model.MiniMonkeyBarrel,  # MM Barrel
    Model.TNTBarrel,  # TNT Barrel
    Model.Rocketbarrel,  # RB Barrel
    Model.StrongKongBarrel,  # SK Barrel
    Model.OrangstandSprintBarrel,  # OSS Barrel
    Model.PlayerCar,  # Tiny Car
    Model.Boulder,  # Boulder
    Model.VaseCircle,  # Vase
    Model.VaseColon,  # Vase
    Model.VaseTriangle,  # Vase
    Model.VasePlus,  # Vase
    Model.ArmyDilloMissle,  # AD Missile
    Model.TagBarrel,  # Tag Barrel
    Model.QuestionMark,  # Question Mark
    Model.Krusha,  # Krusha
    Model.Light,  # Light
    Model.BananaPeel,  # Banana Peel
    Model.FunkyGun,  # Funky's Gun
]

bother_models = [
    Model.BeaverBlue_LowPoly,  # Beaver
    Model.Klobber,  # Klobber
    Model.Kaboom,  # Kaboom
    Model.KlaptrapGreen,  # Green Klap
    Model.KlaptrapPurple,  # Purple Klap
    Model.KlaptrapRed,  # Red Klap
    Model.KlaptrapTeeth,  # Klap Teeth
    Model.Krash,  # Krash
    Model.Troff,  # Troff
    Model.NintendoLogo,  # N64 Logo
    Model.MechanicalFish,  # Mech Fish
    Model.Krossbones,  # Krossbones
    Model.Rabbit,  # Rabbit
    Model.SkeletonHead,  # Minecart Skeleton Head
    Model.Tomato,  # Tomato
    Model.IceTomato,  # Ice Tomato
    Model.GoldenBanana_104,  # Golden Banana
    Model.Microphone,  # Microbuffer
    Model.Bell,  # Bell
    Model.Missile,  # Missile (Car Race)
    Model.Buoy,  # Red Buoy
    Model.BuoyGreen,  # Green Buoy
    Model.RarewareLogo,  # Rareware Logo
]

piano_models = [
    Model.Krash,
    Model.RoboKremling,
    Model.KoshKremling,
    Model.KoshKremlingRed,
    Model.Kasplat,
    Model.Guard,
    Model.Krossbones,
    Model.Mermaid,
    Model.Mushroom,
    Model.GoldenBanana_104,
    Model.FlySwatter_83,
    Model.Ruler,
]
piano_extreme_model = [
    Model.SkeletonHead,
    Model.Owl,
    Model.Kosha,
    # Model.Beanstalk,
]

spotlight_fish_models = [
    # Model.Turtle,  # Lighting Bug
    Model.Seal,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Zinger,
    Model.Squawks_28,
    Model.Klobber,
    Model.Kaboom,
    Model.KlaptrapGreen,
    Model.KlaptrapPurple,
    Model.KlaptrapRed,
    Model.Krash,
    Model.SirDomino,
    # Model.MrDice_41,  # Lighting issue
    # Model.Ruler, # Lighting issue
    # Model.RoboKremling, # Lighting isuse
    Model.NintendoLogo,
    Model.MechanicalFish,
    Model.ToyCar,
    Model.Kasplat,
    Model.BananaFairy,
    Model.Guard,
    Model.Gimpfish,
    Model.Shuri,
    Model.Spider,
    Model.Rabbit,
    Model.KRoolCutscene,
    Model.KRoolFight,
    Model.SkeletonHead,
    # Model.Vulture_76, # Lighting bug
    # Model.Vulture_77, # Lighting bug
    # Model.Bat, # Lighting bug
    # Model.Tomato, # Lighting bug
    # Model.IceTomato, # Lighting bug
    # Model.FlySwatter_83, # Lighting bug
    Model.SpotlightFish,
    Model.Microphone,
    Model.Rocketbarrel,
    Model.StrongKongBarrel,
    Model.OrangstandSprintBarrel,
    Model.MiniMonkeyBarrel,
    Model.HunkyChunkyBarrel,
]
candy_cutscene_models = [
    Model.Cranky,
    # Model.Funky, # Disappears with collision
    Model.Candy,
    Model.Snide,
    Model.Seal,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Klobber,
    Model.Kaboom,
    Model.Krash,
    Model.Troff,
    Model.Scoff,
    Model.RoboKremling,
    Model.Beetle,
    Model.MrDice_41,
    Model.MrDice_56,
    Model.BananaFairy,
    Model.Rabbit,
    Model.KRoolCutscene,
    Model.KRoolFight,
    Model.Vulture_76,
    Model.Vulture_77,
    Model.Tomato,
    Model.IceTomato,
    Model.FlySwatter_83,
    Model.Microphone,
    Model.StrongKongBarrel,
    Model.Rocketbarrel,
    Model.OrangstandSprintBarrel,
    Model.MiniMonkeyBarrel,
    Model.HunkyChunkyBarrel,
    Model.RambiCrate,
    Model.EnguardeCrate,
    Model.Boulder,
    Model.SteelKeg,
    Model.GoldenBanana_104,
]

funky_cutscene_models = [
    Model.Cranky,
    Model.Candy,
    Model.Funky,
    Model.Troff,
    Model.Scoff,
    Model.Ruler,
    Model.RoboKremling,
    Model.KRoolCutscene,
    Model.KRoolFight,
    Model.Microphone,
]

# Not holding gun
funky_cutscene_models_extreme = [
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Klobber,
    Model.Kaboom,
    Model.SirDomino,
    Model.MechanicalFish,
    Model.BananaFairy,
    Model.SkeletonHand,
    Model.IceTomato,
    Model.Tomato,
]

boot_cutscene_models = [
    Model.Turtle,
    Model.Enguarde,
    Model.BeaverBlue,
    Model.BeaverGold,
    Model.Zinger,
    Model.Squawks_28,
    Model.KlaptrapGreen,
    Model.KlaptrapPurple,
    Model.KlaptrapRed,
    Model.BananaFairy,
    Model.Spider,
    Model.Bat,
    Model.KRoolGlove,
]

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
        "skin": [0x61D6, 0x63FE, 0x6786, 0x7DD6, 0x7E8E, 0x7F3E, 0x7FEE, 0x5626, 0x56E6, 0x5A86, 0x5BAE, 0x5D46, 0x5E2E, 0x5FAE, 0x69BE, 0x735E, 0x7C5E, 0x7E4E, 0x7EF6, 0x7FA6, 0x8056],
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

    KONG_ZONES = {"DK": ["Fur", "Tie"], "Diddy": ["Clothes"], "Lanky": ["Clothes", "Fur"], "Tiny": ["Clothes", "Hair"], "Chunky": ["Main", "Other"], "Rambi": ["Skin"], "Enguarde": ["Skin"]}

    if js.document.getElementById("override_cosmetics").checked or True:
        writeTransition(settings)
        writeCustomPortal(settings)
        if js.document.getElementById("random_colors").checked:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors.randomized)
        else:
            for kong in KONG_ZONES:
                for zone in KONG_ZONES[kong]:
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_colors", CharacterColors[js.document.getElementById(f"{kong.lower()}_{zone.lower()}_colors").value])
                    settings.__setattr__(f"{kong.lower()}_{zone.lower()}_custom_color", js.document.getElementById(f"{kong.lower()}_{zone.lower()}_custom_color").value)
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
        textures = [0xB7B, 0x323] + list(range(0x155C, 0x1568))
        for tex in textures:
            dimension = 32 if tex in (0xB7B, 0x323) else 44
            shine_img = getImageFile(25, tex, True, dimension, dimension, TextureFormat.RGBA5551)
            gb_shine_img = maskImageGBSpin(shine_img, tuple(channels), tex)
            if tex in (0xB7B, 0x323):
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
                writeColorImageToROM(fakegb_shine_img, 25, getBonusSkinOffset(0), 32, 32, False, TextureFormat.RGBA5551)
            writeColorImageToROM(gb_shine_img, 25, tex, dimension, dimension, False, TextureFormat.RGBA5551)


color_bases = []
balloon_single_frames = [(4, 38), (5, 38), (5, 38), (5, 38), (5, 38), (5, 38), (4, 38), (4, 38)]


def getRGBFromHash(hash: str):
    """Convert hash RGB code to rgb array."""
    red = int(hash[1:3], 16)
    green = int(hash[3:5], 16)
    blue = int(hash[5:7], 16)
    return [red, green, blue]


def maskImageWithColor(im_f: Image, mask: tuple):
    """Apply rgb mask to image using a rgb color tuple."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.copy()
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def maskImage(im_f, base_index, min_y, keep_dark=False):
    """Apply RGB mask to image."""
    w, h = im_f.size
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, min_y, w, h))
    if keep_dark is False:
        brightener = ImageEnhance.Brightness(im_dupe)
        im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, min_y), im_dupe)
    pix = im_f.load()
    mask = getRGBFromHash(color_bases[base_index])
    w, h = im_f.size
    for x in range(w):
        for y in range(min_y, h):
            base = list(pix[x, y])
            if base[3] > 0:
                for channel in range(3):
                    base[channel] = int(mask[channel] * (base[channel] / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def maskMushroomImage(im_f, reference_image, color, side_2=False):
    """Apply RGB mask to mushroom image."""
    w, h = im_f.size
    pixels_to_mask = []
    pix_ref = reference_image.load()
    for x in range(w):
        for y in range(h):
            base_ref = list(pix_ref[x, y])
            # Filter out the white dots that won't get filtered out correctly with the below conditions
            if not (max(abs(base_ref[0] - base_ref[2]), abs(base_ref[1] - base_ref[2])) < 41 and abs(base_ref[0] - base_ref[1]) < 11):
                # Filter out that one lone pixel that is technically blue AND gets through the above filter, but should REALLY not be blue
                if not (side_2 is True and x == 51 and y == 21):
                    # Select the exact pixels to mask, which is all the "blue" pixels, filtering out the white spots
                    if base_ref[2] > base_ref[0] and base_ref[2] > base_ref[1] and int(base_ref[0] + base_ref[1]) < 200:
                        pixels_to_mask.append([x, y])
                    # Select the darker blue pixels as well
                    elif base_ref[2] > int(base_ref[0] + base_ref[1]):
                        pixels_to_mask.append([x, y])
    pix = im_f.load()
    mask = getRGBFromHash(color)
    for channel in range(3):
        mask[channel] = max(1, mask[channel])  # Absolute black is bad
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            if base[3] > 0 and [x, y] in pixels_to_mask:
                average_light = int((base[0] + base[1] + base[2]) / 3)
                for channel in range(3):
                    base[channel] = int(mask[channel] * (average_light / 255))
                pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorRotatingRoomTiles():
    """Determine how to recolor the tiles rom the memory game in Donkey's Rotating Room in Caves."""
    question_mark_tiles = [900, 901, 892, 893, 896, 897, 890, 891, 898, 899, 894, 895]
    face_tiles = [874, 878, 875, 879, 876, 886, 877, 885, 880, 887, 881, 888, 870, 872, 871, 873, 866, 882, 867, 883, 868, 889, 869, 884]
    question_mark_tile_masks = [508, 509]
    face_tile_masks = [636, 635, 633, 634, 631, 632, 630, 629, 627, 628, 5478, 5478]
    question_mark_resize = [17, 37]
    face_resize = [[32, 64], [32, 64], [32, 64], [32, 64], [32, 64], [71, 66]]
    question_mark_offsets = [[16, 14], [0, 14]]
    face_offsets = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [-5, -1], [-38, -1]]

    for tile in range(len(question_mark_tiles)):
        tile_image = getImageFile(7, question_mark_tiles[tile], False, 32, 64, TextureFormat.RGBA5551)
        mask = getImageFile(7, question_mark_tile_masks[(tile % 2)], False, 32, 64, TextureFormat.RGBA5551)
        resize = question_mark_resize
        mask = mask.resize((resize[0], resize[1]))
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, question_mark_offsets[(tile % 2)], int(tile / 2), (tile % 2))
        writeColorImageToROM(masked_tile, 7, question_mark_tiles[tile], 32, 64, False, TextureFormat.RGBA5551)
    for tile in range(len(face_tiles)):
        face_index = int(tile / 4)
        if face_index < 5:
            width = 32
            height = 64
        else:
            width = 44
            height = 44
        mask = getImageFile(25, face_tile_masks[int(tile / 2)], True, width, height, TextureFormat.RGBA5551)
        resize = face_resize[face_index]
        mask = mask.resize((resize[0], resize[1]))
        tile_image = getImageFile(7, face_tiles[tile], False, 32, 64, TextureFormat.RGBA5551)
        masked_tile = maskImageRotatingRoomTile(tile_image, mask, face_offsets[int(tile / 2)], face_index, (int(tile / 2) % 2))
        writeColorImageToROM(masked_tile, 7, face_tiles[tile], 32, 64, False, TextureFormat.RGBA5551)


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
    masked_im = maskImageWithColor(im_f, color)
    spin_pixels = getSpinPixels()
    if image_index not in spin_pixels:
        return masked_im
    px = im_f.load()
    px_0 = masked_im.load()
    for point in spin_pixels[image_index]:
        px_0[point[0], point[1]] = px[point[0], point[1]]
    return masked_im


def maskImageRotatingRoomTile(im_f, im_mask, paste_coords, image_color_index, tile_side):
    """Apply RGB mask to image of a Rotating Room Memory Tile."""
    w, h = im_f.size
    im_original = im_f
    pix_original = im_original.load()
    pixels_original = []
    for x in range(w):
        pixels_original.append([])
        for y in range(h):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    brightener = ImageEnhance.Brightness(im_f)
    im_f = brightener.enhance(2)
    pix = im_f.load()
    pix_mask = im_mask.load()
    w2, h2 = im_mask.size
    mask_coords = []
    for x in range(w2):
        for y in range(h2):
            coord = list(pix_mask[x, y])
            if coord[3] > 0:
                mask_coords.append([(x + paste_coords[0]), (y + paste_coords[1])])
    if image_color_index < 5:
        mask = getRGBFromHash(color_bases[image_color_index])
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too dark looks bad
    else:
        mask = getRGBFromHash(color_bases[2])
    mask2 = getRGBFromHash("#000000")
    if image_color_index == 0:
        mask2 = getRGBFromHash("#FFFFFF")
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base_original = list(pixels_original[x][y])
            if [x, y] not in mask_coords:
                if image_color_index in [1, 2, 4]:  # Diddy, Lanky and Chunky don't get any special features
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                elif image_color_index in [0, 3]:  # Donkey and Tiny get a diamond-shape frame
                    side = w
                    if tile_side == 1:
                        side = 0
                    if abs(abs(side - x) - y) < 2 or abs(abs(side - x) - abs(h - y)) < 2:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                else:  # Golden Banana gets a block-pattern
                    if (int(x / 8) + int(y / 8)) % 2 == 0:
                        for channel in range(3):
                            base[channel] = int(mask[channel] * (base[channel] / 255))
                    else:
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
            else:
                for channel in range(3):
                    base[channel] = base_original[channel]
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


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
    mask = getRGBFromHash(color_bases[base_index])
    if base_index == 2 or (base_index == 0 and colorblind_mode == ColorblindMode.trit):  # lanky or (DK in tritanopia mode)
        border_color = color_bases[4]
    else:
        border_color = color_bases[1]
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


def writeColorImageToROM(im_f: PIL.Image.Image, table_index: int, file_index: int, width: int, height: int, transparent_border: bool, format: TextureFormat) -> None:
    """Write texture to ROM."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    file_end = js.pointer_addresses[table_index]["entries"][file_index + 1]["pointing_to"]
    file_size = file_end - file_start
    try:
        LocalROM().seek(file_start)
    except Exception:
        ROM().seek(file_start)
    pix = im_f.load()
    width, height = im_f.size
    bytes_array = []
    border = 1
    right_border = 3
    for y in range(height):
        for x in range(width):
            if transparent_border:
                if ((x < border) or (y < border) or (x >= (width - border)) or (y >= (height - border))) or (x == (width - right_border)):
                    pix_data = [0, 0, 0, 0]
                else:
                    pix_data = list(pix[x, y])
            else:
                pix_data = list(pix[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            elif format == TextureFormat.RGBA5551:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
            elif format == TextureFormat.IA4:
                intensity = pix_data[0] >> 5
                alpha = 0 if pix_data[3] == 0 else 1
                data = ((intensity << 1) | alpha) & 0xF
                bytes_array.append(data)
    bytes_per_px = 2
    if format == TextureFormat.IA4:
        temp_ba = bytes_array.copy()
        bytes_array = []
        value_storage = 0
        bytes_per_px = 0.5
        for idx, val in enumerate(temp_ba):
            polarity = idx % 2
            if polarity == 0:
                value_storage = val << 4
            else:
                value_storage |= val
                bytes_array.append(value_storage)
    data = bytearray(bytes_array)
    if format == TextureFormat.RGBA32:
        bytes_per_px = 4
    if len(data) > (bytes_per_px * width * height):
        print(f"Image too big error: {table_index} > {file_index}")
    if table_index in (14, 25):
        data = gzip.compress(data, compresslevel=9)
    if len(data) > file_size:
        print(f"File too big error: {table_index} > {file_index}")
    try:
        LocalROM().writeBytes(data)
    except Exception:
        ROM().writeBytes(data)


def writeKasplatHairColorToROM(color, table_index, file_index, format: str):
    """Write color to ROM for kasplats."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color)
    if format == TextureFormat.RGBA32:
        color_lst = mask.copy()
        color_lst.append(255)  # Alpha
        null_color = [0] * 4
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        color_lst = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            bytes_array.extend(color_lst)
    for i in range(18):
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeWhiteKasplatHairColorToROM(color1, color2, table_index, file_index, format: str):
    """Write color to ROM for white kasplats, giving them a black-white block pattern."""
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    mask = getRGBFromHash(color1)
    mask2 = getRGBFromHash(color2)
    if format == TextureFormat.RGBA32:
        color_lst_0 = mask.copy()
        color_lst_0.append(255)
        color_lst_1 = mask2.copy()
        color_lst_1.append(255)
        null_color = [0] * 4
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        val_r2 = int((mask2[0] >> 3) << 11)
        val_g2 = int((mask2[1] >> 3) << 6)
        val_b2 = int((mask2[2] >> 3) << 1)
        rgba_val2 = val_r2 | val_g2 | val_b2 | 1
        color_lst_0 = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
        color_lst_1 = [(rgba_val2 >> 8) & 0xFF, rgba_val2 & 0xFF]
        null_color = [0] * 2
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if (int(y / 7) + int(x / 8)) % 2 == 0:
                bytes_array.extend(color_lst_0)
            else:
                bytes_array.extend(color_lst_1)
    for i in range(18):
        bytes_array.extend(color_lst_0)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        bytes_array.extend(color_lst_0)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeKlaptrapSkinColorToROM(color_index, table_index, file_index, format: str):
    """Write color to ROM for klaptraps."""
    im_f = getImageFile(table_index, file_index, True, 32, 43, format)
    im_f = maskImage(im_f, color_index, 0, (color_index != 3))
    pix = im_f.load()
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def writeSpecialKlaptrapTextureToROM(color_index, table_index, file_index, format: str, pixels_to_ignore: list):
    """Write color to ROM for klaptraps special texture(s)."""
    im_f = getImageFile(table_index, file_index, True, 32, 43, format)
    pix_original = im_f.load()
    pixels_original = []
    for x in range(32):
        pixels_original.append([])
        for y in range(43):
            pixels_original[x].append(list(pix_original[x, y]).copy())
    im_f_masked = maskImage(im_f, color_index, 0, (color_index != 3))
    pix = im_f_masked.load()
    file_start = js.pointer_addresses[table_index]["entries"][file_index]["pointing_to"]
    if format == TextureFormat.RGBA32:
        null_color = [0] * 4
    else:
        null_color = [0, 0]
    bytes_array = []
    for y in range(42):
        for x in range(32):
            if [x, y] not in pixels_to_ignore:
                color_lst = calculateKlaptrapPixel(list(pix[x, y]), format)
            else:
                color_lst = calculateKlaptrapPixel(list(pixels_original[x][y]), format)
            bytes_array.extend(color_lst)
    for i in range(18):
        if [i, 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[i, 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[i][42]), format)
        bytes_array.extend(color_lst)
    for i in range(4):
        bytes_array.extend(null_color)
    for i in range(3):
        if [(22 + i), 42] not in pixels_to_ignore:
            color_lst = calculateKlaptrapPixel(list(pix[(22 + i), 42]), format)
        else:
            color_lst = calculateKlaptrapPixel(list(pixels_original[(22 + i)][42]), format)
        bytes_array.extend(color_lst)
    data = bytearray(bytes_array)
    if table_index == 25:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(file_start)
    ROM().writeBytes(data)


def calculateKlaptrapPixel(mask: list, format: str):
    """Calculate the new color for the given pixel."""
    if format == TextureFormat.RGBA32:
        color_lst = mask.copy()
        color_lst.append(255)  # Alpha
    else:
        val_r = int((mask[0] >> 3) << 11)
        val_g = int((mask[1] >> 3) << 6)
        val_b = int((mask[2] >> 3) << 1)
        rgba_val = val_r | val_g | val_b | 1
        color_lst = [(rgba_val >> 8) & 0xFF, rgba_val & 0xFF]
    return color_lst


def maskBlueprintImage(im_f, base_index):
    """Apply RGB mask to blueprint image."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getRGBFromHash(color_bases[base_index])
    if max(mask[0], max(mask[1], mask[2])) < 39:
        for channel in range(3):
            mask[channel] = max(39, mask[channel])  # Too black is bad for these items
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the wooden frame
                # brown is orange, is red and (red+green), is very little blue
                # but, if the color is light, we can't rely on the blue value alone.
                if base2[2] > 20 and (base2[2] > base2[1] or base2[1] - base2[2] < 20):
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskLaserImage(im_f, base_index):
    """Apply RGB mask to laser texture."""
    w, h = im_f.size
    im_f_original = im_f
    converter = ImageEnhance.Color(im_f)
    im_f = converter.enhance(0)
    im_dupe = im_f.crop((0, 0, w, h))
    brightener = ImageEnhance.Brightness(im_dupe)
    im_dupe = brightener.enhance(2)
    im_f.paste(im_dupe, (0, 0), im_dupe)
    pix = im_f.load()
    pix2 = im_f_original.load()
    mask = getRGBFromHash(color_bases[base_index])
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            base2 = list(pix2[x, y])
            if base[3] > 0:
                # Filter out the white center of the laser
                if min(base2[0], min(base2[1], base2[2])) <= 210:
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (base[channel] / 255))
                    pix[x, y] = (base[0], base[1], base[2], base[3])
                else:
                    pix[x, y] = (base2[0], base2[1], base2[2], base2[3])
    return im_f


def maskPotionImage(im_f, primary_color, secondary_color=None):
    """Apply RGB mask to DK arcade potion reward preview texture."""
    w, h = im_f.size
    pix = im_f.load()
    mask = getRGBFromHash(primary_color)
    if secondary_color is not None:
        mask2 = secondary_color
    for channel in range(3):
        mask[channel] = max(1, mask[channel])
    w, h = im_f.size
    for x in range(w):
        for y in range(h):
            base = list(pix[x, y])
            # Filter out transparent pixels and the cork
            if base[3] > 0 and y > 2 and [x, y] not in [[9, 4], [10, 4]]:
                # Filter out the bottle's contents
                if base[0] == base[1] and base[1] == base[2]:
                    if secondary_color is not None:
                        # Color the bottle itself
                        for channel in range(3):
                            base[channel] = int(mask2[channel] * (base[channel] / 255))
                else:
                    # Color the bottle's contents
                    average_light = int((base[0] + base[1] + base[2]) / 3)
                    for channel in range(3):
                        base[channel] = int(mask[channel] * (average_light / 255))
            pix[x, y] = (base[0], base[1], base[2], base[3])
    return im_f


def recolorWrinklyDoors():
    """Recolor the Wrinkly hint door doorframes for colorblind mode."""
    file = [0xF0, 0xF2, 0xEF, 0x67, 0xF1]
    for kong in range(5):
        wrinkly_door_start = js.pointer_addresses[4]["entries"][file[kong]]["pointing_to"]
        wrinkly_door_finish = js.pointer_addresses[4]["entries"][file[kong] + 1]["pointing_to"]
        wrinkly_door_size = wrinkly_door_finish - wrinkly_door_start
        ROM().seek(wrinkly_door_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(wrinkly_door_start)
        data = ROM().readBytes(wrinkly_door_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them (list extensions to mitigate the linter's "artistic freedom" putting 1 value per line)
        color1_offsets = [1548, 1580, 1612, 1644, 1676, 1708, 1756, 1788, 1804, 1820, 1836, 1852, 1868, 1884, 1900, 1916]
        color1_offsets = color1_offsets + [1932, 1948, 1964, 1980, 1996, 2012, 2028, 2044, 2076, 2108, 2124, 2156, 2188, 2220, 2252, 2284]
        color1_offsets = color1_offsets + [2316, 2348, 2380, 2396, 2412, 2428, 2444, 2476, 2508, 2540, 2572, 2604, 2636, 2652, 2668, 2684]
        color1_offsets = color1_offsets + [2700, 2716, 2732, 2748, 2764, 2780, 2796, 2812, 2828, 2860, 2892, 2924, 2956, 2988, 3020, 3052]
        color2_offsets = [1564, 1596, 1628, 1660, 1692, 1724, 1740, 1772, 2332, 2364, 2460, 2492, 2524, 2556, 2588, 2620]
        new_color1 = getRGBFromHash(color_bases[kong])
        new_color2 = getRGBFromHash(color_bases[kong])
        if kong == 0:
            for channel in range(3):
                new_color2[channel] = max(80, new_color1[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the doorframe
        for offset in color1_offsets:
            for i in range(3):
                num_data[offset + i] = new_color1[i]
        for offset in color2_offsets:
            for i in range(3):
                num_data[offset + i] = new_color2[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(wrinkly_door_start)
        ROM().writeBytes(data)


def recolorSlamSwitches(galleon_switch_value, ROM_COPY: ROM):
    """Recolor the Simian Slam switches for colorblind mode."""
    file = [0x94, 0x93, 0x95, 0x96, 0xB8, 0x16C, 0x16B, 0x16D, 0x16E, 0x16A, 0x167, 0x166, 0x168, 0x169, 0x165]
    written_galleon_ship = False
    for switch in range(15):
        slam_switch_start = js.pointer_addresses[4]["entries"][file[switch]]["pointing_to"]
        slam_switch_finish = js.pointer_addresses[4]["entries"][file[switch] + 1]["pointing_to"]
        slam_switch_size = slam_switch_finish - slam_switch_start
        ROM().seek(slam_switch_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(slam_switch_start)
        data = ROM().readBytes(slam_switch_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color_offsets = [1828, 1844, 1860, 1876, 1892, 1908]
        new_color1 = getRGBFromHash(color_bases[4])  # chunky's color
        new_color2 = getRGBFromHash(color_bases[2])  # lanky's color
        new_color3 = getRGBFromHash(color_bases[1])  # diddy's color

        # Green switches
        if switch < 5:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color1[i]
        # Blue switches
        elif switch < 10:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color2[i]
        # Red switches
        else:
            for offset in color_offsets:
                for i in range(3):
                    num_data[offset + i] = new_color3[i]

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(slam_switch_start)
        ROM().writeBytes(data)
        if not written_galleon_ship:
            galleon_switch_color = new_color1.copy()
            if galleon_switch_value is not None:
                if galleon_switch_value != 1:
                    galleon_switch_color = new_color3.copy()
                    if galleon_switch_value == 2:
                        galleon_switch_color = new_color2.copy()
            recolorKRoolShipSwitch(galleon_switch_color, ROM_COPY)
            written_galleon_ship = True


def recolorBlueprintModelTwo():
    """Recolor the Blueprint Model2 items for colorblind mode."""
    file = [0xDE, 0xE0, 0xE1, 0xDD, 0xDF]
    for kong in range(5):
        blueprint_model2_start = js.pointer_addresses[4]["entries"][file[kong]]["pointing_to"]
        blueprint_model2_finish = js.pointer_addresses[4]["entries"][file[kong] + 1]["pointing_to"]
        blueprint_model2_size = blueprint_model2_finish - blueprint_model2_start
        ROM().seek(blueprint_model2_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(blueprint_model2_start)
        data = ROM().readBytes(blueprint_model2_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x52C, 0x54C, 0x57C, 0x58C, 0x5AC, 0x5CC, 0x5FC, 0x61C]
        color2_offsets = [0x53C, 0x55C, 0x5EC, 0x60C]
        color3_offsets = [0x56C, 0x59C, 0x5BC, 0x5DC]
        new_color = getRGBFromHash(color_bases[kong])
        if kong == 0:
            for channel in range(3):
                new_color[channel] = max(39, new_color[channel])  # Too black is bad, because anything times 0 is 0

        # Recolor the model2 item
        for offset in color1_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color2_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color3_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(blueprint_model2_start)
        ROM().writeBytes(data)


def recolorBells():
    """Recolor the Chunky Minecart bells for colorblind mode (prot/deut)."""
    file = 693
    minecart_bell_start = js.pointer_addresses[4]["entries"][file]["pointing_to"]
    minecart_bell_finish = js.pointer_addresses[4]["entries"][file + 1]["pointing_to"]
    minecart_bell_size = minecart_bell_finish - minecart_bell_start
    ROM().seek(minecart_bell_start)
    indicator = int.from_bytes(ROM().readBytes(2), "big")
    ROM().seek(minecart_bell_start)
    data = ROM().readBytes(minecart_bell_size)
    if indicator == 0x1F8B:
        data = zlib.decompress(data, (15 + 32))
    num_data = []  # data, but represented as nums rather than b strings
    for d in data:
        num_data.append(d)
    # Figure out which colors to use and where to put them
    color1_offsets = [0x214, 0x244, 0x264, 0x274, 0x284]
    color2_offsets = [0x224, 0x234, 0x254]
    new_color1 = getRGBFromHash("#0066FF")
    new_color2 = getRGBFromHash("#0000FF")

    # Recolor the bell
    for offset in color1_offsets:
        for i in range(3):
            num_data[offset + i] = new_color1[i]
    for offset in color2_offsets:
        for i in range(3):
            num_data[offset + i] = new_color2[i]

    data = bytearray(num_data)  # convert num_data back to binary string
    if indicator == 0x1F8B:
        data = gzip.compress(data, compresslevel=9)
    ROM().seek(minecart_bell_start)
    ROM().writeBytes(data)


def recolorKlaptraps():
    """Recolor the klaptrap models for colorblind mode."""
    green_files = [0xF31, 0xF32, 0xF33, 0xF35, 0xF37, 0xF39]  # 0xF2F collar? 0xF30 feet?
    red_files = [0xF44, 0xF45, 0xF46, 0xF47, 0xF48, 0xF49]  # , 0xF42 collar? 0xF43 feet?
    purple_files = [0xF3C, 0xF3D, 0xF3E, 0xF3F, 0xF40, 0xF41]  # 0xF3B feet?, 0xF3A collar?

    # Regular textures
    for file in range(6):
        writeKlaptrapSkinColorToROM(4, 25, green_files[file], TextureFormat.RGBA5551)
        writeKlaptrapSkinColorToROM(1, 25, red_files[file], TextureFormat.RGBA5551)
        writeKlaptrapSkinColorToROM(3, 25, purple_files[file], TextureFormat.RGBA5551)

    belly_pixels_to_ignore = []
    for x in range(32):
        for y in range(43):
            if y < 29 or (y > 31 and y < 39) or y == 40 or y == 42:
                belly_pixels_to_ignore.append([x, y])
            elif (y == 39 and x < 16) or (y == 41 and x < 24):
                belly_pixels_to_ignore.append([x, y])

    # Special texture that requires only partial recoloring, in this case file 0xF38 which is the belly, and only the few green pixels
    writeSpecialKlaptrapTextureToROM(4, 25, 0xF38, TextureFormat.RGBA5551, belly_pixels_to_ignore)


def recolorPotions(colorblind_mode):
    """Overwrite potion colors."""
    secondary_color = [color_bases[1], None, color_bases[4], color_bases[1], None, None]
    if colorblind_mode == ColorblindMode.trit:
        secondary_color[0] = color_bases[4]
        secondary_color[2] = None
    for color in range(len(secondary_color)):
        if secondary_color[color] is not None:
            secondary_color[color] = getRGBFromHash(secondary_color[color])

    # Actor:
    file = [[0xED, 0xEE, 0xEF, 0xF0, 0xF1, 0xF2], [0xF5, 0xF6, 0xF7, 0xF8, 0xF9, 0xFA]]
    for type in range(2):
        for potion_color in range(6):
            potion_actor_start = js.pointer_addresses[5]["entries"][file[type][potion_color]]["pointing_to"]
            potion_actor_finish = js.pointer_addresses[5]["entries"][file[type][potion_color] + 1]["pointing_to"]
            potion_actor_size = potion_actor_finish - potion_actor_start
            ROM().seek(potion_actor_start)
            indicator = int.from_bytes(ROM().readBytes(2), "big")
            ROM().seek(potion_actor_start)
            data = ROM().readBytes(potion_actor_size)
            if indicator == 0x1F8B:
                data = zlib.decompress(data, (15 + 32))
            num_data = []  # data, but represented as nums rather than b strings
            for d in data:
                num_data.append(d)
            # Figure out which colors to use and where to put them
            color1_offsets = [0x34]
            color2_offsets = [0x44, 0x54, 0xA4]
            color3_offsets = [0x64, 0x74, 0x84, 0xE4]
            color4_offsets = [0x94]
            color5_offsets = [0xB4, 0xC4, 0xD4]
            # color6_offsets = [0xF4, 0x104, 0x114, 0x124, 0x134, 0x144, 0x154, 0x164]
            if potion_color < 5:
                new_color = getRGBFromHash(color_bases[potion_color])
            else:
                new_color = getRGBFromHash("#FFFFFF")

            # Recolor the actor item
            for offset in color1_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    if secondary_color[potion_color] is not None and potion_color == 3:  # tiny
                        num_data[offset + i] = int(num_data[offset + i] * (secondary_color[potion_color][i] / 255))
                    elif secondary_color[potion_color] is not None:  # donkey gets an even darker shade
                        num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 8) / 255))
                    elif secondary_color[potion_color] is not None:  # other kongs with a secondary color get a darker shade
                        num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 4) / 255))
                    else:
                        num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color2_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color3_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color4_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
            for offset in color5_offsets:
                total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
                for i in range(3):
                    num_data[offset + i] = int(total_light / 3)
                for i in range(3):
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

            data = bytearray(num_data)  # convert num_data back to binary string
            if indicator == 0x1F8B:
                data = gzip.compress(data, compresslevel=9)
            ROM().seek(potion_actor_start)
            ROM().writeBytes(data)

    # Model2:
    file = [91, 498, 89, 499, 501, 502]
    for potion_color in range(6):
        potion_model2_start = js.pointer_addresses[4]["entries"][file[potion_color]]["pointing_to"]
        potion_model2_finish = js.pointer_addresses[4]["entries"][file[potion_color] + 1]["pointing_to"]
        potion_model2_size = potion_model2_finish - potion_model2_start
        ROM().seek(potion_model2_start)
        indicator = int.from_bytes(ROM().readBytes(2), "big")
        ROM().seek(potion_model2_start)
        data = ROM().readBytes(potion_model2_size)
        if indicator == 0x1F8B:
            data = zlib.decompress(data, (15 + 32))
        num_data = []  # data, but represented as nums rather than b strings
        for d in data:
            num_data.append(d)
        # Figure out which colors to use and where to put them
        color1_offsets = [0x144]
        color2_offsets = [0x154, 0x164, 0x1B4]
        color3_offsets = [0x174, 0x184, 0x194, 0x1F4]
        color4_offsets = [0x1A4]
        color5_offsets = [0x1C4, 0x1D4, 0x1E4]
        # color6_offsets = [0x204, 0x214, 0x224, 0x234, 0x244, 0x254, 0x264, 0x274]
        if potion_color < 5:
            new_color = getRGBFromHash(color_bases[potion_color])
        else:
            new_color = getRGBFromHash("#FFFFFF")

        # Recolor the model2 item
        for offset in color1_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                if secondary_color[potion_color] is not None and potion_color == 3:  # tiny
                    num_data[offset + i] = int(num_data[offset + i] * (secondary_color[potion_color][i] / 255))
                elif secondary_color[potion_color] is not None:  # donkey gets an even darker shade
                    num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 8) / 255))
                elif secondary_color[potion_color] is not None:  # other kongs with a secondary color get a darker shade
                    num_data[offset + i] = int(num_data[offset + i] * (int(secondary_color[potion_color][i] / 4) / 255))
                else:
                    num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color2_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color3_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color4_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))
        for offset in color5_offsets:
            total_light = int(num_data[offset] + num_data[offset + 1] + num_data[offset + 2])
            for i in range(3):
                num_data[offset + i] = int(total_light / 3)
            for i in range(3):
                num_data[offset + i] = int(num_data[offset + i] * (new_color[i] / 255))

        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        ROM().seek(potion_model2_start)
        ROM().writeBytes(data)

    # DK Arcade sprites
    for file in range(8, 14):
        index = file - 8
        if index < 5:
            color = color_bases[index]
        else:
            color = "#FFFFFF"
        potion_image = getImageFile(6, file, False, 20, 20, TextureFormat.RGBA5551)
        potion_image = maskPotionImage(potion_image, color, secondary_color[index])
        writeColorImageToROM(potion_image, 6, file, 20, 20, False, TextureFormat.RGBA5551)


def recolorMushrooms():
    """Recolor the various colored mushrooms in the game for colorblind mode."""
    reference_mushroom_image = getImageFile(7, 297, False, 32, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side1 = getImageFile(25, 0xD64, True, 64, 32, TextureFormat.RGBA5551)
    reference_mushroom_image_side2 = getImageFile(25, 0xD65, True, 64, 32, TextureFormat.RGBA5551)
    files_table_7 = [296, 295, 297, 299, 298]
    files_table_25_side_1 = [0xD60, 0x67F, 0xD64, 0xD62, 0xD66]
    files_table_25_side_2 = [0xD61, 0x680, 0xD65, 0xD63, 0xD67]
    for file in range(5):
        # Mushroom on the ceiling inside Fungi Forest Lobby
        mushroom_image = getImageFile(7, files_table_7[file], False, 32, 32, TextureFormat.RGBA5551)
        mushroom_image = maskMushroomImage(mushroom_image, reference_mushroom_image, color_bases[file])
        writeColorImageToROM(mushroom_image, 7, files_table_7[file], 32, 32, False, TextureFormat.RGBA5551)
        # Mushrooms in Lanky's colored mushroom puzzle (and possibly also the bouncy mushrooms)
        mushroom_image_side_1 = getImageFile(25, files_table_25_side_1[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_1 = maskMushroomImage(mushroom_image_side_1, reference_mushroom_image_side1, color_bases[file])
        writeColorImageToROM(mushroom_image_side_1, 25, files_table_25_side_1[file], 64, 32, False, TextureFormat.RGBA5551)
        mushroom_image_side_2 = getImageFile(25, files_table_25_side_2[file], True, 64, 32, TextureFormat.RGBA5551)
        mushroom_image_side_2 = maskMushroomImage(mushroom_image_side_2, reference_mushroom_image_side2, color_bases[file], True)
        writeColorImageToROM(mushroom_image_side_2, 25, files_table_25_side_2[file], 64, 32, False, TextureFormat.RGBA5551)


BALLOON_START = [5835, 5827, 5843, 5851, 5819]


def overwrite_object_colors(settings, ROM_COPY: ROM):
    """Overwrite object colors."""
    global color_bases
    mode = settings.colorblind_mode
    sav = settings.rom_data
    galleon_switch_value = None
    ROM_COPY.seek(sav + 0x103)
    switch_rando_on = int.from_bytes(ROM_COPY.readBytes(1), "big") != 0
    if switch_rando_on:
        ROM_COPY.seek(sav + 0x104 + 3)
        galleon_switch_value = int.from_bytes(ROM_COPY.readBytes(1), "big")
    if mode != ColorblindMode.off:
        if mode == ColorblindMode.prot:
            color_bases = ["#000000", "#0072FF", "#766D5A", "#FFFFFF", "#FDE400"]
        elif mode == ColorblindMode.deut:
            color_bases = ["#000000", "#318DFF", "#7F6D59", "#FFFFFF", "#E3A900"]
        elif mode == ColorblindMode.trit:
            color_bases = ["#000000", "#C72020", "#13C4D8", "#FFFFFF", "#FFA4A4"]
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
        recolorWrinklyDoors()
        recolorSlamSwitches(galleon_switch_value, ROM_COPY)
        recolorRotatingRoomTiles()
        recolorBlueprintModelTwo()
        recolorKlaptraps()
        recolorPotions(mode)
        recolorMushrooms()
        for kong_index in range(5):
            # file = 4120
            # # Kasplat Hair
            # hair_im = getFile(25, file, True, 32, 44, TextureFormat.RGBA5551)
            # hair_im = maskImage(hair_im, kong_index, 0)
            # writeColorImageToROM(hair_im, 25, [4124, 4122, 4123, 4120, 4121][kong_index], 32, 44, False)
            writeKasplatHairColorToROM(color_bases[kong_index], 25, [4124, 4122, 4123, 4120, 4121][kong_index], TextureFormat.RGBA5551)
            for file in range(5519, 5527):
                # Blueprint sprite
                blueprint_start = [5624, 5608, 5519, 5632, 5616]
                blueprint_im = blueprint_lanky[(file - 5519)]
                blueprint_im = maskBlueprintImage(blueprint_im, kong_index)
                writeColorImageToROM(blueprint_im, 25, blueprint_start[kong_index] + (file - 5519), 48, 42, False, TextureFormat.RGBA5551)
            for file in range(4925, 4931):
                # Shockwave
                shockwave_start = [4897, 4903, 4712, 4950, 4925]
                shockwave_im = getImageFile(25, shockwave_start[kong_index] + (file - 4925), True, 32, 32, TextureFormat.RGBA32)
                shockwave_im = maskImage(shockwave_im, kong_index, 0)
                writeColorImageToROM(shockwave_im, 25, shockwave_start[kong_index] + (file - 4925), 32, 32, False, TextureFormat.RGBA32)
            for file in range(784, 796):
                # Helm Laser (will probably also affect the Pufftoss laser and the Game Over laser)
                laser_start = [784, 748, 363, 760, 772]
                laser_im = getImageFile(7, laser_start[kong_index] + (file - 784), False, 32, 32, TextureFormat.RGBA32)
                laser_im = maskLaserImage(laser_im, kong_index)
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
                    single_im = maskImage(single_im, kong_index, 0)
                    writeColorImageToROM(single_im, 7, single_start[kong_index] + (file - 152), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(216, 224):
                    # Coin
                    coin_start = [224, 256, 248, 216, 264]
                    coin_im = getImageFile(7, coin_start[kong_index] + (file - 216), False, 48, 42, TextureFormat.RGBA5551)
                    coin_im = maskImage(coin_im, kong_index, 0)
                    writeColorImageToROM(coin_im, 7, coin_start[kong_index] + (file - 216), 48, 42, False, TextureFormat.RGBA5551)
                for file in range(274, 286):
                    # Bunch
                    bunch_start = [274, 854, 818, 842, 830]
                    bunch_im = getImageFile(7, bunch_start[kong_index] + (file - 274), False, 44, 44, TextureFormat.RGBA5551)
                    bunch_im = maskImage(bunch_im, kong_index, 0, True)
                    writeColorImageToROM(bunch_im, 7, bunch_start[kong_index] + (file - 274), 44, 44, False, TextureFormat.RGBA5551)
                for file in range(5819, 5827):
                    # Balloon
                    balloon_im = getImageFile(25, BALLOON_START[kong_index] + (file - 5819), True, 32, 64, TextureFormat.RGBA5551)
                    balloon_im = maskImage(balloon_im, kong_index, 33)
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
kong_index_mapping = {
    # Regular model, instrument model
    Kongs.donkey: (3, None),
    Kongs.diddy: (0, 1),
    Kongs.lanky: (5, 6),
    Kongs.tiny: (8, 9),
    Kongs.chunky: (11, 12),
}
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
                placeKrushaHead(index)
                if index == Kongs.donkey:
                    fixBaboonBlasts()
                # Orange Switches
                switch_faces = [0xB25, 0xB1E, 0xC81, 0xC80, 0xB24]
                base_im = getImageFile(25, 0xC20, True, 32, 32, TextureFormat.RGBA5551)
                orange_im = getImageFile(7, 0x136, False, 32, 32, TextureFormat.RGBA5551)
                if settings.colorblind_mode == ColorblindMode.off:
                    orange_im = maskImageWithColor(orange_im, (0, 150, 0))
                else:
                    orange_im = maskImageWithColor(orange_im, (0, 255, 0))  # Brighter green makes this more distinguishable for colorblindness
                dim_length = int(32 * ORANGE_SCALING)
                dim_offset = int((32 - dim_length) / 2)
                orange_im = orange_im.resize((dim_length, dim_length))
                base_im.paste(orange_im, (dim_offset, dim_offset), orange_im)
                writeColorImageToROM(base_im, 25, switch_faces[index], 32, 32, False, TextureFormat.RGBA5551)


DK_SCALE = 0.75
GENERIC_SCALE = 0.49
krusha_scaling = [
    # [x, y, z, xz, y]
    # DK
    [lambda x: x * DK_SCALE, lambda x: x * DK_SCALE, lambda x: x * GENERIC_SCALE, lambda x: x * DK_SCALE, lambda x: x * DK_SCALE],
    # Diddy
    [lambda x: (x * 1.043) - 41.146, lambda x: (x * 9.893) - 8.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.103) - 14.759, lambda x: (x * 0.823) + 35.220],
    # Lanky
    [lambda x: (x * 0.841) - 17.231, lambda x: (x * 6.925) - 2.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 0.680) - 18.412, lambda x: (x * 0.789) + 42.138],
    # Tiny
    [lambda x: (x * 0.632) + 7.590, lambda x: (x * 6.925) + 0.0, lambda x: x * GENERIC_SCALE, lambda x: (x * 1.567) - 21.676, lambda x: (x * 0.792) + 41.509],
    # Chunky
    [lambda x: x, lambda x: x, lambda x: x, lambda x: x, lambda x: x],
]


def readListAsInt(arr: list, start: int, size: int) -> int:
    """Read list and convert to int."""
    val = 0
    for i in range(size):
        val = (val * 256) + arr[start + i]
    return val


def fixModelSmallKongCollision(kong_index: int):
    """Modify Krusha Model to be smaller to enable him to fit through smaller gaps."""
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
        head = readListAsInt(num_data, 0, 4)
        ptr = readListAsInt(num_data, 0xC, 4)
        base = (ptr - head) + 0x28 + 8
        count_0 = readListAsInt(num_data, base, 4)
        changes = krusha_scaling[kong_index][:3]
        changes_0 = [
            krusha_scaling[kong_index][3],
            krusha_scaling[kong_index][4],
            krusha_scaling[kong_index][3],
        ]
        for i in range(count_0):
            i_start = base + 4 + (i * 0x14)
            for coord_index, change in enumerate(changes):
                val_i = readListAsInt(num_data, i_start + (4 * coord_index) + 4, 4)
                val_f = change(intf_to_float(val_i))
                val_i = int(float_to_hex(val_f), 16)
                for di, d in enumerate(int_to_list(val_i, 4)):
                    num_data[i_start + (4 * coord_index) + 4 + di] = d
        section_2_start = base + 4 + (count_0 * 0x14)
        count_1 = readListAsInt(num_data, section_2_start, 4)
        for i in range(count_1):
            i_start = section_2_start + 4 + (i * 0x10)
            for coord_index, change in enumerate(changes_0):
                val_i = readListAsInt(num_data, i_start + (4 * coord_index), 4)
                val_f = change(intf_to_float(val_i))
                val_i = int(float_to_hex(val_f), 16)
                for di, d in enumerate(int_to_list(val_i, 4)):
                    num_data[i_start + (4 * coord_index) + di] = d
        data = bytearray(num_data)  # convert num_data back to binary string
        if indicator == 0x1F8B:
            data = gzip.compress(data, compresslevel=9)
        LocalROM().seek(krusha_model_start)
        LocalROM().writeBytes(data)


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


def fixBaboonBlasts():
    """Fix various baboon blasts to work for Krusha."""
    # Fungi Baboon Blast
    ROM_COPY = LocalROM()
    for id in (2, 5):
        item_start = getObjectAddress(0xBC, id, "actor")
        if item_start is not None:
            ROM_COPY.seek(item_start + 0x14)
            ROM_COPY.writeMultipleBytes(0xFFFFFFEC, 4)
            ROM_COPY.seek(item_start + 0x1B)
            ROM_COPY.writeMultipleBytes(0, 1)
    # Caves Baboon Blast
    item_start = getObjectAddress(0xBA, 4, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x4)
        ROM_COPY.writeMultipleBytes(int(float_to_hex(510), 16), 4)
    item_start = getObjectAddress(0xBA, 12, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x4)
        ROM_COPY.writeMultipleBytes(int(float_to_hex(333), 16), 4)
    # Castle Baboon Blast
    item_start = getObjectAddress(0xBB, 4, "actor")
    if item_start is not None:
        ROM_COPY.seek(item_start + 0x0)
        ROM_COPY.writeMultipleBytes(int(float_to_hex(2472), 16), 4)
        ROM_COPY.seek(item_start + 0x8)
        ROM_COPY.writeMultipleBytes(int(float_to_hex(1980), 16), 4)


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


def placeKrushaHead(slot):
    """Replace a kong's face with the Krusha face."""
    kong_face_textures = [[0x27C, 0x27B], [0x279, 0x27A], [0x277, 0x278], [0x276, 0x275], [0x273, 0x274]]
    unc_face_textures = [[579, 586], [580, 587], [581, 588], [582, 589], [577, 578]]
    ROM_COPY = LocalROM()
    ROM_COPY.seek(0x1FF6000)
    left = []
    right = []
    img32 = []
    img32_rgba32 = []
    y32 = []
    y32_rgba32 = []
    for y in range(64):
        x32 = []
        x32_rgba32 = []
        for x in range(64):
            data_hi = int.from_bytes(ROM_COPY.readBytes(1), "big")
            data_lo = int.from_bytes(ROM_COPY.readBytes(1), "big")
            val = (data_hi << 8) | data_lo
            val_r = ((val >> 11) & 0x1F) << 3
            val_g = ((val >> 6) & 0x1F) << 3
            val_b = ((val >> 1) & 0x1F) << 3
            val_a = 0
            if val & 1:
                val_a = 255
            data_rgba32 = [val_r, val_g, val_b, val_a]
            if x < 32:
                right.extend([data_hi, data_lo])
            else:
                left.extend([data_hi, data_lo])
            if ((x % 2) + (y % 2)) == 0:
                x32.extend([data_hi, data_lo])
                x32_rgba32.extend(data_rgba32)
        if len(x32) > 0 and len(x32_rgba32):
            y32.append(x32)
            y32_rgba32.append(x32_rgba32)
    y32.reverse()
    for y in y32:
        img32.extend(y)
    y32_rgba32.reverse()
    for y in y32_rgba32:
        img32_rgba32.extend(y)
    for x in range(2):
        img_data = [right, left][x]
        texture_index = kong_face_textures[slot][x]
        unc_index = unc_face_textures[slot][x]
        texture_addr = js.pointer_addresses[25]["entries"][texture_index]["pointing_to"]
        unc_addr = js.pointer_addresses[7]["entries"][unc_index]["pointing_to"]
        data = gzip.compress(bytearray(img_data), compresslevel=9)
        ROM_COPY.seek(texture_addr)
        ROM_COPY.writeBytes(data)
        ROM_COPY.seek(unc_addr)
        ROM_COPY.writeBytes(bytearray(img_data))
    rgba32_addr32 = js.pointer_addresses[14]["entries"][197 + slot]["pointing_to"]
    rgba16_addr32 = js.pointer_addresses[14]["entries"][190 + slot]["pointing_to"]
    data32 = gzip.compress(bytearray(img32), compresslevel=9)
    data32_rgba32 = gzip.compress(bytearray(img32_rgba32), compresslevel=9)
    ROM_COPY.seek(rgba32_addr32)
    ROM_COPY.writeBytes(bytearray(data32_rgba32))
    ROM_COPY.seek(rgba16_addr32)
    ROM_COPY.writeBytes(bytearray(data32))


barrel_skins = (
    "gb",
    "dk",
    "diddy",
    "lanky",
    "tiny",
    "chunky",
    "bp",
    "nin_coin",
    "rw_coin",
    "key",
    "crown",
    "medal",
    "potion",
    "bean",
    "pearl",
    "fairy",
    "rainbow",
    "fakegb",
    "melon",
    "cranky",
    "funky",
    "candy",
    "snide",
    "hint",
)


def getBonusSkinOffset(offset: int):
    """Get texture index after the barrel skins."""
    return 6026 + (3 * len(barrel_skins)) + offset


def getValueFromByteArray(ba: bytearray, offset: int, size: int) -> int:
    """Get value from byte array given an offset and size."""
    value = 0
    for x in range(size):
        local_value = ba[offset + x]
        value <<= 8
        value += local_value
    return value


def hueShiftImageContainer(table: int, image: int, width: int, height: int, format: TextureFormat, shift: int):
    """Load an image, shift the hue and rewrite it back to ROM."""
    loaded_im = getImageFile(table, image, table != 7, width, height, format)
    loaded_im = hueShift(loaded_im, shift)
    loaded_px = loaded_im.load()
    bytes_array = []
    for y in range(height):
        for x in range(width):
            pix_data = list(loaded_px[x, y])
            if format == TextureFormat.RGBA32:
                bytes_array.extend(pix_data)
            elif format == TextureFormat.RGBA5551:
                red = int((pix_data[0] >> 3) << 11)
                green = int((pix_data[1] >> 3) << 6)
                blue = int((pix_data[2] >> 3) << 1)
                alpha = int(pix_data[3] != 0)
                value = red | green | blue | alpha
                bytes_array.extend([(value >> 8) & 0xFF, value & 0xFF])
    px_data = bytearray(bytes_array)
    if table != 7:
        px_data = gzip.compress(px_data, compresslevel=9)
    ROM().seek(js.pointer_addresses[table]["entries"][image]["pointing_to"])
    ROM().writeBytes(px_data)


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


def writeMiscCosmeticChanges(settings):
    """Write miscellaneous changes to the cosmetic colors."""
    if settings.override_cosmetics:
        enemy_setting = RandomModels[js.document.getElementById("random_enemy_colors").value]
    else:
        enemy_setting = settings.random_enemy_colors
    if settings.misc_cosmetics:
        # Melon HUD
        data = {7: [0x13C, 0x147], 14: [0x5A, 0x5D], 25: [getBonusSkinOffset(4), getBonusSkinOffset(4)]}
        shift = getRandomHueShift()
        for table in data:
            table_data = data[table]
            for img in range(table_data[0], table_data[1] + 1):
                if table == 25 and img == getBonusSkinOffset(4):
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
            )
            for sprite_data in fires:
                for img_index in range(sprite_data[0], sprite_data[1] + 1):
                    dim = sprite_data[2]
                    hueShiftImageContainer(25, img_index, dim, dim, TextureFormat.RGBA32, fire_shift)
            for img_index in range(0x29, 0x32 + 1):
                hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA32, fire_shift)
            # Number Game Numbers
            for x in range(16):
                number_hue_shift = getRandomHueShift()
                for sub_img in range(2):
                    img_index = 0x1FE + (2 * x) + sub_img
                    hueShiftImageContainer(7, img_index, 32, 32, TextureFormat.RGBA5551, number_hue_shift)

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
            kosha_helmet_list = [(kosha_helmet_int >> 16) & 0xFF, (kosha_helmet_int >> 8) & 0xFF, kosha_helmet_int & 0xFF]
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
            kremling_shift = getRandomHueShift()
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
        headphones_shift = getRandomHueShift()
        for x in range(8):
            hueShiftImageContainer(7, 0x3D3 + x, 40, 40, TextureFormat.RGBA5551, headphones_shift)
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

        # Enemy Vertex Swaps
        blue_beaver_color = getEnemySwapColor(80, min_channel_variance=80)
        enemy_changes = {
            Model.BeaverBlue_LowPoly: EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color),  # Primary
            Model.BeaverBlue: EnemyColorSwap([0xB2E5FF, 0x65CCFF, 0x00ABE8, 0x004E82, 0x008BD1, 0x001333, 0x1691CE], blue_beaver_color),  # Primary
            Model.BeaverGold: EnemyColorSwap([0xFFE5B2, 0xFFCC65, 0xE8AB00, 0x824E00, 0xD18B00, 0x331300, 0xCE9116]),  # Primary
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
            Model.Kasplat: EnemyColorSwap([0x8FD8FF, 0x182A4F, 0x0B162C, 0x7A98D3, 0x3F6CC4, 0x8FD8FF, 0x284581]),
            # Model.BananaFairy: EnemyColorSwap([0xFFD400, 0xFFAA00, 0xFCD200, 0xD68F00, 0xD77D0A, 0xe49800, 0xdf7f1f, 0xa26c00, 0xd6b200, 0xdf9f1f])
        }
        if enemy_setting == RandomModels.extreme:
            enemy_changes[Model.Klump] = EnemyColorSwap([0xE66B78, 0x621738, 0x300F20, 0xD1426F, 0xA32859])
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


def getNumberImage(number: int) -> PIL.Image.Image:
    """Get Number Image from number."""
    if number < 5:
        num_0_bounds = [0, 20, 30, 45, 58, 76]
        x = number
        return getImageFile(14, 15, True, 76, 24, TextureFormat.RGBA5551).crop((num_0_bounds[x], 0, num_0_bounds[x + 1], 24))
    num_1_bounds = [0, 15, 28, 43, 58, 76]
    x = number - 5
    return getImageFile(14, 16, True, 76, 24, TextureFormat.RGBA5551).crop((num_1_bounds[x], 0, num_1_bounds[x + 1], 24))


def numberToImage(number: int, dim: Tuple[int, int]) -> PIL.Image.Image:
    """Convert multi-digit number to image."""
    digits = 1
    if number < 10:
        digits = 1
    elif number < 100:
        digits = 2
    else:
        digits = 3
    current = number
    nums = []
    total_width = 0
    max_height = 0
    sep_dist = 1
    for _ in range(digits):
        base = getNumberImage(current % 10)
        bbox = base.getbbox()
        base = base.crop(bbox)
        nums.append(base)
        base_w, base_h = base.size
        max_height = max(max_height, base_h)
        total_width += base_w
        current = int(current / 10)
    nums.reverse()
    total_width += (digits - 1) * sep_dist
    base = Image.new(mode="RGBA", size=(total_width, max_height))
    pos = 0
    for num in nums:
        base.paste(num, (pos, 0), num)
        num_w, num_h = num.size
        pos += num_w + sep_dist
    output = Image.new(mode="RGBA", size=dim)
    xScale = dim[0] / total_width
    yScale = dim[1] / max_height
    scale = xScale
    if yScale < xScale:
        scale = yScale
    new_w = int(total_width * scale)
    new_h = int(max_height * scale)
    x_offset = int((dim[0] - new_w) / 2)
    y_offset = int((dim[1] - new_h) / 2)
    new_dim = (new_w, new_h)
    base = base.resize(new_dim)
    output.paste(base, (x_offset, y_offset), base)
    return output


def recolorKRoolShipSwitch(color: tuple, ROM_COPY: ROM):
    """Recolors the simian slam switch that is part of K. Rool's ship in galleon."""
    addresses = (
        0x4C34,
        0x4C44,
        0x4C54,
        0x4C64,
        0x4C74,
        0x4C84,
    )
    data = bytearray(getRawFile(TableNames.ModelTwoGeometry, 305, True))
    for addr in addresses:
        for x in range(3):
            data[addr + x] = color[x]
    new_tex = [
        0xE7,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xE2,
        0x00,
        0x00,
        0x1C,
        0x0C,
        0x19,
        0x20,
        0x38,
        0xE3,
        0x00,
        0x0A,
        0x01,
        0x00,
        0x10,
        0x00,
        0x00,
        0xE3,
        0x00,
        0x0F,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xE7,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xFC,
        0x12,
        0x7E,
        0x03,
        0xFF,
        0xFF,
        0xF9,
        0xF8,
        0xFD,
        0x90,
        0x00,
        0x00,
        0x00,
        0x00,
        0x0B,
        0xAF,
        0xF5,
        0x90,
        0x00,
        0x00,
        0x07,
        0x08,
        0x02,
        0x00,
        0xE6,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xF3,
        0x00,
        0x00,
        0x00,
        0x07,
        0x7F,
        0xF1,
        0x00,
        0xE7,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0x00,
        0xF5,
        0x88,
        0x10,
        0x00,
        0x00,
        0x08,
        0x02,
        0x00,
        0xF2,
        0x00,
        0x00,
        0x00,
        0x00,
        0x0F,
        0xC0,
        0xFC,
    ]
    for x in range(8):
        data[0x1AD8 + x] = 0
    for xi, x in enumerate(new_tex):
        data[0x1AE8 + xi] = x
    for x in range(40):
        data[0x1B58 + x] = 0
    writeRawFile(TableNames.ModelTwoGeometry, 305, True, data, ROM_COPY)


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
                    item_im = getImageFile(image_data.table, image, image_data.table in (14, 25), image_data.dimensions[0], image_data.dimensions[1], image_data.format)
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
                writeColorImageToROM(numberToImage(door.count, (44, 44)).transpose(Image.FLIP_TOP_BOTTOM), 25, door.number_image, 44, 44, True, TextureFormat.RGBA5551)


def applyHolidayMode(settings):
    """Change grass texture to snow."""
    HOLIDAY = "christmas"  # Or "" "halloween"
    if settings.holiday_setting_offseason:
        if HOLIDAY == "christmas":
            # Set season to Christmas
            ROM().seek(settings.rom_data + 0xDB)
            ROM().writeMultipleBytes(2, 1)
            # Grab Snow texture, transplant it
            ROM().seek(0x1FF8000)
            snow_im = Image.new(mode="RGBA", size=((32, 32)))
            snow_px = snow_im.load()
            snow_by = []
            for y in range(32):
                for x in range(32):
                    rgba_px = int.from_bytes(ROM().readBytes(2), "big")
                    red = ((rgba_px >> 11) & 31) << 3
                    green = ((rgba_px >> 6) & 31) << 3
                    blue = ((rgba_px >> 1) & 31) << 3
                    alpha = (rgba_px & 1) * 255
                    snow_px[x, y] = (red, green, blue, alpha)
            for dim in (32, 16, 8, 4):
                snow_im = snow_im.resize((dim, dim))
                px = snow_im.load()
                for y in range(dim):
                    for x in range(dim):
                        rgba_data = list(px[x, y])
                        data = 0
                        for c in range(3):
                            data |= (rgba_data[c] >> 3) << (1 + (5 * c))
                        if rgba_data[3] != 0:
                            data |= 1
                        snow_by.extend([(data >> 8), (data & 0xFF)])
            byte_data = gzip.compress(bytearray(snow_by), compresslevel=9)
            for img in (0x4DD, 0x4E4, 0x6B, 0xF0, 0x8B2, 0x5C2, 0x66E, 0x66F, 0x685, 0x6A1, 0xF8, 0x136):
                start = js.pointer_addresses[25]["entries"][img]["pointing_to"]
                ROM().seek(start)
                ROM().writeBytes(byte_data)
            # Alter CI4 Palettes
            start = js.pointer_addresses[25]["entries"][2007]["pointing_to"]
            mags = [140, 181, 156, 181, 222, 206, 173, 230, 255, 255, 255, 189, 206, 255, 181, 255]
            new_ci4_palette = []
            for mag in mags:
                comp_mag = mag >> 3
                data = (comp_mag << 11) | (comp_mag << 6) | (comp_mag << 1) | 1
                new_ci4_palette.extend([(data >> 8), (data & 0xFF)])
            byte_data = gzip.compress(bytearray(new_ci4_palette), compresslevel=9)
            ROM().seek(start)
            ROM().writeBytes(byte_data)
            # Alter rims
            bananas = [getImageFile(7, x, False, 44, 44, TextureFormat.RGBA5551).resize((14, 14)) for x in [0xD0, 0xE8, 0xA8, 0x98]]
            banana_placement = [
                # File, x, y
                [0xBB3, 15, 1],  # 3
                [0xBB2, 2, 1],  # 2
                [0xBB3, 0, 1],  # 4
                [0xBB2, 17, 1],  # 1
            ]
            for img in (0xBB2, 0xBB3):
                side_im = getImageFile(25, img, True, 32, 16, TextureFormat.RGBA5551)
                hueShift(side_im, 50)
                for bi, banana in enumerate(bananas):
                    if banana_placement[bi][0] == img:
                        b_x = banana_placement[bi][1]
                        b_y = banana_placement[bi][2]
                        side_im.paste(banana, (b_x, b_y), banana)
                side_by = []
                side_px = side_im.load()
                for y in range(16):
                    for x in range(32):
                        red_short = (side_px[x, y][0] >> 3) & 31
                        green_short = (side_px[x, y][1] >> 3) & 31
                        blue_short = (side_px[x, y][2] >> 3) & 31
                        alpha_short = 1 if side_px[x, y][3] > 128 else 0
                        value = (red_short << 11) | (green_short << 6) | (blue_short << 1) | alpha_short
                        side_by.extend([(value >> 8) & 0xFF, value & 0xFF])
                px_data = bytearray(side_by)
                px_data = gzip.compress(px_data, compresslevel=9)
                ROM().seek(js.pointer_addresses[25]["entries"][img]["pointing_to"])
                ROM().writeBytes(px_data)
            # Change DK's Tie and Tiny's Hair
            if settings.dk_tie_colors != CharacterColors.custom and settings.kong_model_dk == KongModels.default:
                tie_hang = [0xFF] * 0xAB8
                tie_hang_data = gzip.compress(bytearray(tie_hang), compresslevel=9)
                ROM().seek(js.pointer_addresses[25]["entries"][0xE8D]["pointing_to"])
                ROM().writeBytes(tie_hang_data)
                tie_loop = [0xFF] * (32 * 32 * 2)
                tie_loop_data = gzip.compress(bytearray(tie_loop), compresslevel=9)
                ROM().seek(js.pointer_addresses[25]["entries"][0x177D]["pointing_to"])
                ROM().writeBytes(tie_loop_data)
            if settings.tiny_hair_colors != CharacterColors.custom and settings.kong_model_tiny == KongModels.default:
                tiny_hair = []
                for x in range(32 * 32):
                    tiny_hair.extend([0xF8, 0x01])
                tiny_hair_data = gzip.compress(bytearray(tiny_hair), compresslevel=9)
                ROM().seek(js.pointer_addresses[25]["entries"][0xE68]["pointing_to"])
                ROM().writeBytes(tiny_hair_data)

        elif HOLIDAY == "halloween":
            ROM().seek(settings.rom_data + 0xDB)
            ROM().writeMultipleBytes(1, 1)
            for img in (0xBB2, 0xBB3):
                side_im = getImageFile(25, img, True, 32, 16, TextureFormat.RGBA5551)
                hueShift(side_im, -12)
                side_by = []
                side_px = side_im.load()
                for y in range(16):
                    for x in range(32):
                        red_short = (side_px[x, y][0] >> 3) & 31
                        green_short = (side_px[x, y][1] >> 3) & 31
                        blue_short = (side_px[x, y][2] >> 3) & 31
                        alpha_short = 1 if side_px[x, y][3] > 128 else 0
                        value = (red_short << 11) | (green_short << 6) | (blue_short << 1) | alpha_short
                        side_by.extend([(value >> 8) & 0xFF, value & 0xFF])
                px_data = bytearray(side_by)
                px_data = gzip.compress(px_data, compresslevel=9)
                ROM().seek(js.pointer_addresses[25]["entries"][img]["pointing_to"])
                ROM().writeBytes(px_data)


def updateMillLeverTexture(settings: Settings) -> None:
    """Update the 21132 texture."""
    if settings.mill_levers[0] > 0:
        # Get Number bounds
        base_num_texture = getImageFile(table_index=25, file_index=0x7CA, compressed=True, width=64, height=32, format=TextureFormat.RGBA5551)
        number_textures = [None, None, None]
        number_x_bounds = (
            (18, 25),
            (5, 16),
            (36, 47),
        )
        modified_tex = getImageFile(table_index=25, file_index=0x7CA, compressed=True, width=64, height=32, format=TextureFormat.RGBA5551)
        for tex in range(3):
            number_textures[tex] = base_num_texture.crop((number_x_bounds[tex][0], 7, number_x_bounds[tex][1], 25))
        total_width = 0
        for x in range(5):
            if settings.mill_levers[x] > 0:
                idx = settings.mill_levers[x] - 1
                total_width += number_x_bounds[idx][1] - number_x_bounds[idx][0]
        # Overwrite old panel
        overwrite_panel = Image.new(mode="RGBA", size=(58, 26), color=(131, 65, 24))
        modified_tex.paste(overwrite_panel, (3, 3), overwrite_panel)
        # Generate new number texture
        new_num_texture = Image.new(mode="RGBA", size=(total_width, 18))
        x_pos = 0
        for num in range(5):
            if settings.mill_levers[num] > 0:
                num_val = settings.mill_levers[num] - 1
                new_num_texture.paste(number_textures[num_val], (x_pos, 0), number_textures[num_val])
                x_pos += number_x_bounds[num_val][1] - number_x_bounds[num_val][0]
        scale_x = 58 / total_width
        scale_y = 26 / 18
        scale = min(scale_x, scale_y)
        x_size = int(total_width * scale)
        y_size = int(18 * scale)
        new_num_texture = new_num_texture.resize((x_size, y_size))
        x_offset = int((58 - x_size) / 2)
        modified_tex.paste(new_num_texture, (3 + x_offset, 3), new_num_texture)
        writeColorImageToROM(modified_tex, 25, 0x7CA, 64, 32, False, TextureFormat.RGBA5551)


def updateDiddyDoors(settings: Settings):
    """Update the textures for the doors."""
    enable_code = False
    for code in settings.diddy_rnd_doors:
        if sum(code) > 0:  # Has a non-zero element
            enable_code = True
    SEG_WIDTH = 48
    SEG_HEIGHT = 42
    NUMBERS_START = (27, 33)
    if enable_code:
        # Order: 4231, 3124, 1342
        starts = (0xCE8, 0xCE4, 0xCE0)
        for index, code in enumerate(settings.diddy_rnd_doors):
            start = starts[index]
            total = Image.new(mode="RGBA", size=(SEG_WIDTH * 2, SEG_HEIGHT * 2))
            for img_index in range(4):
                img = getImageFile(25, start + img_index, True, SEG_WIDTH, SEG_HEIGHT, TextureFormat.RGBA5551)
                x_offset = SEG_WIDTH * (img_index & 1)
                y_offset = SEG_HEIGHT * ((img_index & 2) >> 1)
                total.paste(img, (x_offset, y_offset), img)
            total = total.transpose(Image.FLIP_TOP_BOTTOM)
            # Overlay color
            cover = Image.new(mode="RGBA", size=(42, 20), color=(115, 98, 65))
            total.paste(cover, NUMBERS_START, cover)
            # Paste numbers
            number_images = []
            number_offsets = []
            total_length = 0
            for num in code:
                num_img = getNumberImage(num + 1)
                w, h = num_img.size
                number_offsets.append(total_length)
                total_length += w
                number_images.append(num_img)
            total_numbers = Image.new(mode="RGBA", size=(total_length, 24))
            for img_index, img in enumerate(number_images):
                total_numbers.paste(img, (number_offsets[img_index], 0), img)
            total.paste(total_numbers, (SEG_WIDTH - int(total_length / 2), SEG_HEIGHT - 12), total_numbers)
            total = total.transpose(Image.FLIP_TOP_BOTTOM)
            for img_index in range(4):
                x_offset = SEG_WIDTH * (img_index & 1)
                y_offset = SEG_HEIGHT * ((img_index & 2) >> 1)
                sub_img = total.crop((x_offset, y_offset, x_offset + SEG_WIDTH, y_offset + SEG_HEIGHT))
                writeColorImageToROM(sub_img, 25, start + img_index, SEG_WIDTH, SEG_HEIGHT, False, TextureFormat.RGBA5551)


def updateCryptLeverTexture(settings: Settings) -> None:
    """Update the two textures for Donkey Minecart entry."""
    if settings.crypt_levers[0] > 0:
        # Get a blank texture
        texture_0 = getImageFile(table_index=25, file_index=0x999, compressed=True, width=32, height=64, format=TextureFormat.RGBA5551)
        blank = texture_0.crop((8, 5, 23, 22))
        texture_0.paste(blank, (8, 42), blank)
        texture_1 = texture_0.copy()
        for xi, x in enumerate(settings.crypt_levers):
            corrected = x - 1
            y_slot = corrected % 3
            num = getNumberImage(xi + 1)
            num = num.transpose(Image.FLIP_TOP_BOTTOM)
            w, h = num.size
            scale = 2 / 3
            y_offset = int((h * scale) / 2)
            x_offset = int((w * scale) / 2)
            num = num.resize((int(w * scale), int(h * scale)))
            y_pos = (51, 33, 14)
            tl_y = y_pos[y_slot] - y_offset
            tl_x = 16 - x_offset
            if corrected < 3:
                texture_0.paste(num, (tl_x, tl_y), num)
            else:
                texture_1.paste(num, (tl_x, tl_y), num)
        writeColorImageToROM(texture_0, 25, 0x99A, 32, 64, False, TextureFormat.RGBA5551)
        writeColorImageToROM(texture_1, 25, 0x999, 32, 64, False, TextureFormat.RGBA5551)


def lightenPauseBubble(settings: Settings):
    """Change the brightness of the text bubble used for the pause menu for light mode."""
    if settings.dark_mode_textboxes:
        return
    img = getImageFile(14, 107, True, 48, 32, TextureFormat.RGBA5551)
    px = img.load()
    canary_px = list(px[24, 16])
    if canary_px[0] > 128 and canary_px[1] > 128 and canary_px[2] > 128:
        # Already brightened, cancel
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
        item_im = getImageFile(item_data.table, item_data.image, item_data.table != 7, item_data.width, item_data.height, item_data.tex_format)
        if item_data.flip:
            item_im = item_im.transpose(Image.FLIP_TOP_BOTTOM)
        dim = max(item_data.width, item_data.height)
        base_im = Image.new(mode="RGBA", size=(dim, dim))
        base_im.paste(item_im, (int((dim - item_data.width) >> 1), int((dim - item_data.height) >> 1)), item_im)
    base_im = base_im.resize((32, 32))
    num_im = numberToImage(settings.win_condition_count, (20, 20))
    base_im.paste(num_im, (6, 6), num_im)
    writeColorImageToROM(base_im, 14, 195, 32, 32, False, TextureFormat.RGBA5551)


boot_phrases = (
    "Removing Lanky Kong",
    "Telling 2dos to play DK64",
    "Locking K. Lumsy in a cage",
    "Stealing the Banana Hoard",
    "Finishing the game in a cave",
    "Becoming the peak of randomizers",
    "Giving kops better eyesight",
    "Patching in the glitches",
    "Enhancing Cfox Luck",
    "Finding Rareware GB in Galleon",
    "Resurrecting Chunky Kong",
    "Shouting out Grant Kirkhope",
    "Crediting L. Godfrey",
    "Removing Stop n Swop",
    "Assembling the scraps",
    "Blowing in the cartridge",
    "Backflipping in Chunky Phase",
    "Hiding 20 fairies",
    "Randomizing collision normals",
    "Removing hit detection",
    "Compressing K Rools Voice Lines",
    "Checking divide by 0 doesnt work",
    "Adding every move to Isles",
    "Segueing in dk64randomizer.com",
    "Removing lag. Or am I?",
    "Hiding a dirt patch under grass",
    "Giving Wrinkly the spoiler log",
    "Questioning sub 2:30 in LUA Rando",
    "Chasing Lanky in Fungi Forest",
    "Banning Potions from Candys Shop",
    "Finding someone who can help you",
    "Messing up your seed",
    "Crashing Krem Isle",
    "Increasing Robot Punch Resistance",
    "Caffeinating banana fairies",
    "Bothering Beavers",
    "Inflating Banana Balloons",
    "Counting to 16",
    "Removing Walls",
    "Taking it to the fridge",
    "Brewing potions",
    "Reticulating Splines",  # SimCity 2000
    "Ironing Donks",
    "Replacing mentions of Hero with Hoard",
    "Suggesting you also try BK Randomizer",
    "Scattering 3500 Bananas",
    "Stealing ideas from other randomizers",
    "Fixing Krushas Collision",
    "Falling on 75m",
    "Summoning Salt",
    "Combing Chunkys Afro",
    "Asking what you gonna do",
    "Thinking with portals",
    "Reminding you to hydrate",
    "Injecting lag",
    "Turning Sentient",
    "Performing for you",
    "Charging 2 coins per save",
    "Loading in Beavers",
    "Lifting Boulders with Relative Ease",
    "Doing Monkey Science Probably",
    "Telling Killi to eventually play DK64",
    "Crediting Grant Kirkhope",
    "Dropping Crayons",
    "Saying Hello when others wont",
    "Mangling Music",
    "Killing Speedrunning",
    "Enhancing Cfox Luck Voice Linesmizers",
    "Enforcing the law of the Jungle",
    "Saving 20 frames",
)

crown_heads = (
    # Object
    "Arena",
    "Beaver",
    "Bish Bash",
    "Forest",
    "Kamikaze",
    "Kritter",
    "Pinnacle",
    "Plinth",
    "Shockwave",
    "Bean",
    "Dogadon",
    "Banana",
    "Squawks",
    "Lanky",
    "Diddy",
    "Tiny",
    "Chunky",
    "DK",
    "Krusha",
    "Kosha",
    "Klaptrap",
    "Zinger",
    "Gnawty",
    "Kasplat",
    "Pufftup",
    "Shuri",
    "Krossbones",
    "Caves",
    "Castle",
    "Helm",
    "Japes",
    "Jungle",
    "Angry",
    "Aztec",
    "Frantic",
    "Factory",
    "Gloomy",
    "Galleon",
    "Crystal",
    "Creepy",
    "Hideout",
)

crown_tails = (
    # Synonym for brawl/similar
    "Ambush",
    "Brawl",
    "Fracas",
    "Karnage",
    "Kremlings",
    "Palaver",
    "Panic",
    "Showdown",
    "Slam",
    "Melee",
    "Tussle",
    "Altercation",
    "Wrangle",
    "Clash",
    "Free for All",
    "Skirmish",
    "Scrap",
    "Fight",
    "Rumpus",
    "Fray",
    "Wrestle",
    "Brouhaha",
    "Commotion",
    "Uproar",
    "Rough and Tumble",
    "Broil",
    "Argy Bargy",
    "Bother",
    "Mayhem",
    "Bonanza",
    "Battle",
    "Kerfuffle",
    "Rumble",
    "Fisticuffs",
    "Ruckus",
    "Scrimmage",
    "Strife",
    "Dog and Duck",
    "Joust",
    "Scuffle",
    "Hootenanny",
)


def getCrownNames() -> list:
    """Get crown names from head and tail pools."""
    # Get 10 names for heads just in case "Forest" and "Fracas" show up
    heads = random.sample(crown_heads, 10)
    tails = random.sample(crown_tails, 9)
    # Remove "Forest" if both "Forest" and "Fracas" show up
    if "Forest" in heads and "Fracas" in tails:
        heads.remove("Forest")
    # Only get 9 names, Forest Fracas can't be overwritten without having negative impacts
    names = []
    for x in range(9):
        head = heads[x]
        tail = tails[x]
        if head[0] == "K" and tail[0] == "C":
            split_tail = list(tail)
            split_tail[0] = "K"
            tail = "".join(split_tail)
        names.append(f"{head} {tail}!".upper())
    names.append("Forest Fracas!".upper())
    return names


def writeCrownNames():
    """Write Crown Names to ROM."""
    names = getCrownNames()
    old_text = grabText(35, True)
    for name_index, name in enumerate(names):
        old_text[0x1E + name_index] = ({"text": [name]},)
    writeText(35, old_text, True)


def writeBootMessages() -> None:
    """Write boot messages into ROM."""
    ROM_COPY = LocalROM()
    placed_messages = random.sample(boot_phrases, 4)
    for message_index, message in enumerate(placed_messages):
        ROM_COPY.seek(0x1FFD000 + (0x40 * message_index))
        ROM_COPY.writeBytes(message.upper().encode("ascii"))


def writeTransition(settings: Settings) -> None:
    """Write transition cosmetic to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.transitions is None:
        return
    if js.cosmetic_names.transitions is None:
        return
    file_data = list(zip(js.cosmetics.transitions, js.cosmetic_names.transitions))
    settings.custom_transition = None
    if len(file_data) == 0:
        return
    selected_transition = random.choice(file_data)
    settings.custom_transition = selected_transition[1].split("/")[-1]  # File Name
    im_f = Image.open(BytesIO(bytes(selected_transition[0])))
    writeColorImageToROM(im_f, 14, 95, 64, 64, False, TextureFormat.IA4)


def writeCustomPortal(settings: Settings) -> None:
    """Write custom portal file to ROM."""
    if js.cosmetics is None:
        return
    if js.cosmetics.tns_portals is None:
        return
    if js.cosmetic_names.tns_portals is None:
        return
    file_data = list(zip(js.cosmetics.tns_portals, js.cosmetic_names.tns_portals))
    settings.custom_troff_portal = None
    if len(file_data) == 0:
        return
    selected_portal = random.choice(file_data)
    settings.custom_troff_portal = selected_portal[1].split("/")[-1]  # File Name
    im_f = Image.open(BytesIO(bytes(selected_portal[0])))
    im_f = im_f.resize((63, 63)).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
    portal_data = {
        "NW": {
            "x_min": 0,
            "y_min": 0,
            "writes": [0x39E, 0x39F],
        },
        "SW": {
            "x_min": 0,
            "y_min": 31,
            "writes": [0x3A0, 0x39D],
        },
        "SE": {
            "x_min": 31,
            "y_min": 31,
            "writes": [0x3A2, 0x39B],
        },
        "NE": {
            "x_min": 31,
            "y_min": 0,
            "writes": [0x39C, 0x3A1],
        },
    }
    for sub in portal_data.keys():
        x_min = portal_data[sub]["x_min"]
        y_min = portal_data[sub]["y_min"]
        local_img = im_f.crop((x_min, y_min, x_min + 32, y_min + 32))
        for idx in portal_data[sub]["writes"]:
            writeColorImageToROM(local_img, 7, idx, 32, 32, False, TextureFormat.RGBA5551)
