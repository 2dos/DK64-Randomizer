"""Library functions for the build procedure."""

import struct
from PIL import Image
import math
import zlib
from BuildEnums import MusicTypes, Song

main_pointer_table_offset = 0x101C50
BLOCK_COLOR_SIZE = 64  # Bytes allocated to a block 32x32 image. Brute forcer says we can go as low as 0x25 bytes, but leaving some room for me to have left out something
ROMName = "rom/dk64.z64"
newROMName = "rom/dk64-randomizer-base.z64"
finalROM = "rom/dk64-randomizer-base-dev.z64"
music_size = 24000
music_sizes_fine = {
    MusicTypes.BGM: 24000,
    MusicTypes.Event: 7000,
    MusicTypes.MajorItem: 3000,
    MusicTypes.MinorItem: 1500,
}
music_type_mapping = {
    Song.TrainingGrounds: MusicTypes.BGM,
    Song.Isles: MusicTypes.BGM,
    Song.IslesKremIsle: MusicTypes.BGM,
    Song.IslesKLumsy: MusicTypes.BGM,
    Song.IslesBFI: MusicTypes.BGM,
    Song.IslesSnideRoom: MusicTypes.BGM,
    Song.JapesLobby: MusicTypes.BGM,
    Song.AztecLobby: MusicTypes.BGM,
    Song.FactoryLobby: MusicTypes.BGM,
    Song.GalleonLobby: MusicTypes.BGM,
    Song.ForestLobby: MusicTypes.BGM,
    Song.CavesLobby: MusicTypes.BGM,
    Song.CastleLobby: MusicTypes.BGM,
    Song.HelmLobby: MusicTypes.BGM,
    # Jungle Japes BGM
    Song.JapesMain: MusicTypes.BGM,
    Song.JapesStart: MusicTypes.BGM,
    Song.JapesTunnels: MusicTypes.BGM,
    Song.JapesStorm: MusicTypes.BGM,
    Song.JapesCaves: MusicTypes.BGM,
    Song.JapesBlast: MusicTypes.BGM,
    Song.JapesCart: MusicTypes.BGM,
    Song.JapesDillo: MusicTypes.BGM,
    # Angry Aztec BGM
    Song.AztecMain: MusicTypes.BGM,
    Song.AztecTunnels: MusicTypes.BGM,
    Song.AztecTemple: MusicTypes.BGM,
    Song.Aztec5DT: MusicTypes.BGM,
    Song.AztecBlast: MusicTypes.BGM,
    Song.AztecBeetle: MusicTypes.BGM,
    Song.AztecChunkyKlaptraps: MusicTypes.BGM,
    Song.AztecDogadon: MusicTypes.BGM,
    # Frantic Factory BGM
    Song.FactoryMain: MusicTypes.BGM,
    Song.FactoryProduction: MusicTypes.BGM,
    Song.FactoryResearchAndDevelopment: MusicTypes.BGM,
    Song.FactoryCrusher: MusicTypes.BGM,
    Song.FactoryCarRace: MusicTypes.BGM,
    Song.FactoryJack: MusicTypes.BGM,
    # Gloomy Galleon BGM
    Song.GalleonTunnels: MusicTypes.BGM,
    Song.GalleonOutside: MusicTypes.BGM,
    Song.GalleonLighthouse: MusicTypes.BGM,
    Song.GalleonMechFish: MusicTypes.BGM,
    Song.Galleon2DS: MusicTypes.BGM,
    Song.Galleon5DS: MusicTypes.BGM,
    Song.GalleonMermaid: MusicTypes.BGM,
    Song.GalleonChest: MusicTypes.BGM,
    Song.GalleonBlast: MusicTypes.BGM,
    Song.GalleonSealRace: MusicTypes.BGM,
    Song.GalleonPufftoss: MusicTypes.BGM,
    # Fungi Forest BGM
    Song.ForestDay: MusicTypes.BGM,
    Song.ForestNight: MusicTypes.BGM,
    Song.ForestBarn: MusicTypes.BGM,
    Song.ForestMill: MusicTypes.BGM,
    Song.ForestAnthill: MusicTypes.BGM,
    Song.ForestMushroom: MusicTypes.BGM,
    Song.ForestMushroomRooms: MusicTypes.BGM,
    Song.ForestSpider: MusicTypes.BGM,
    Song.ForestBlast: MusicTypes.BGM,
    Song.ForestRabbitRace: MusicTypes.BGM,
    Song.ForestCart: MusicTypes.BGM,
    Song.ForestDogadon: MusicTypes.BGM,
    # Crystal Caves BGM
    Song.Caves: MusicTypes.BGM,
    Song.CavesIgloos: MusicTypes.BGM,
    Song.CavesCabins: MusicTypes.BGM,
    Song.CavesRotatingRoom: MusicTypes.BGM,
    Song.CavesTantrum: MusicTypes.BGM,
    Song.CavesBlast: MusicTypes.BGM,
    Song.CavesIceCastle: MusicTypes.BGM,
    Song.CavesBeetleRace: MusicTypes.BGM,
    Song.CavesDillo: MusicTypes.BGM,
    # Creepy Castle BGM
    Song.Castle: MusicTypes.BGM,
    Song.CastleShed: MusicTypes.BGM,
    Song.CastleTree: MusicTypes.BGM,
    Song.CastleTunnels: MusicTypes.BGM,
    Song.CastleCrypt: MusicTypes.BGM,
    Song.CastleInnerCrypts: MusicTypes.BGM,
    Song.CastleDungeon_Chains: MusicTypes.BGM,
    Song.CastleDungeon_NoChains: MusicTypes.BGM,
    Song.CastleBallroom: MusicTypes.BGM,
    Song.CastleMuseum: MusicTypes.BGM,
    Song.CastleGreenhouse: MusicTypes.BGM,
    Song.CastleTrash: MusicTypes.BGM,
    Song.CastleTower: MusicTypes.BGM,
    Song.CastleBlast: MusicTypes.BGM,
    Song.CastleCart: MusicTypes.BGM,
    Song.CastleKutOut: MusicTypes.BGM,
    # Hideout Helm BGM
    Song.HelmBoMOn: MusicTypes.BGM,
    Song.HelmBoMOff: MusicTypes.BGM,
    Song.HelmBonus: MusicTypes.BGM,
    # NPC BGM
    Song.Cranky: MusicTypes.BGM,
    Song.Funky: MusicTypes.BGM,
    Song.Candy: MusicTypes.BGM,
    Song.Snide: MusicTypes.BGM,
    Song.WrinklyKong: MusicTypes.BGM,
    # Moves and Animals BGM
    Song.StrongKong: MusicTypes.BGM,
    Song.Rocketbarrel: MusicTypes.BGM,
    Song.Sprint: MusicTypes.BGM,
    Song.MiniMonkey: MusicTypes.BGM,
    Song.HunkyChunky: MusicTypes.BGM,
    Song.GorillaGone: MusicTypes.BGM,
    Song.Rambi: MusicTypes.BGM,
    Song.Enguarde: MusicTypes.BGM,
    # Battle BGM
    Song.BattleArena: MusicTypes.BGM,
    Song.TroffNScoff: MusicTypes.BGM,
    Song.AwaitingBossEntry: MusicTypes.BGM,
    Song.BossIntroduction: MusicTypes.BGM,
    Song.MiniBoss: MusicTypes.BGM,
    Song.KRoolBattle: MusicTypes.BGM,
    # Menu and Story BGM
    Song.MainMenu: MusicTypes.BGM,
    Song.PauseMenu: MusicTypes.BGM,
    Song.NintendoLogo: MusicTypes.BGM,
    Song.DKRap: MusicTypes.Protected,
    Song.IntroStory: MusicTypes.BGM,
    Song.KRoolTheme: MusicTypes.BGM,
    Song.KLumsyCelebration: MusicTypes.BGM,
    Song.KRoolTakeoff: MusicTypes.BGM,
    Song.KRoolEntrance: MusicTypes.BGM,
    Song.KLumsyEnding: MusicTypes.BGM,
    Song.EndSequence: MusicTypes.BGM,
    # Minigame BGM
    Song.Minigames: MusicTypes.BGM,
    Song.MadMazeMaul: MusicTypes.BGM,
    Song.StealthySnoop: MusicTypes.BGM,
    Song.MinecartMayhem: MusicTypes.BGM,
    Song.MonkeySmash: MusicTypes.BGM,
    # Major Items
    Song.OhBanana: MusicTypes.MajorItem,
    Song.GBGet: MusicTypes.MajorItem,
    Song.MoveGet: MusicTypes.MajorItem,
    Song.GunGet: MusicTypes.MajorItem,
    Song.BananaMedalGet: MusicTypes.MajorItem,
    Song.BlueprintDrop: MusicTypes.MajorItem,
    Song.BlueprintGet: MusicTypes.MajorItem,
    Song.HeadphonesGet: MusicTypes.MajorItem,
    Song.DropRainbowCoin: MusicTypes.MajorItem,
    Song.RainbowCoinGet: MusicTypes.MajorItem,
    Song.CompanyCoinGet: MusicTypes.MajorItem,
    Song.BeanGet: MusicTypes.MajorItem,
    Song.PearlGet: MusicTypes.MajorItem,
    # Minor Items
    Song.MelonSliceDrop: MusicTypes.MinorItem,
    Song.MelonSliceGet: MusicTypes.MinorItem,
    Song.BananaCoinGet: MusicTypes.MinorItem,
    Song.CrystalCoconutGet: MusicTypes.MinorItem,
    Song.FairyTick: MusicTypes.MinorItem,
    Song.MinecartCoinGet: MusicTypes.MinorItem,
    Song.DropCoins: MusicTypes.MinorItem,
    Song.Checkpoint: MusicTypes.MinorItem,
    Song.NormalStar: MusicTypes.MinorItem,
    # Events
    Song.Success: MusicTypes.Event,
    Song.Failure: MusicTypes.Event,
    Song.SuccessRaces: MusicTypes.Event,
    Song.FailureRaces: MusicTypes.Event,
    Song.BossUnlock: MusicTypes.Event,
    Song.BossDefeat: MusicTypes.Event,
    Song.Bongos: MusicTypes.Event,
    Song.Guitar: MusicTypes.Event,
    Song.Trombone: MusicTypes.Event,
    Song.Saxophone: MusicTypes.Event,
    Song.Triangle: MusicTypes.Event,
    Song.BaboonBalloon: MusicTypes.Event,
    Song.Transformation: MusicTypes.Event,
    Song.VultureRing: MusicTypes.Event,
    Song.BBlastFinalStar: MusicTypes.Event,
    Song.FinalCBGet: MusicTypes.Event,
    # Ambient
    Song.WaterDroplets: MusicTypes.Ambient,
    Song.TwinklySounds: MusicTypes.Ambient,
    Song.FairyNearby: MusicTypes.Ambient,
    Song.FakeFairyNearby: MusicTypes.Ambient,
    Song.SeasideSounds: MusicTypes.Ambient,
    # Protected
    Song.UnusedCoin: MusicTypes.Protected,
    Song.StartPause: MusicTypes.Protected,
    Song.JapesHighPitched: MusicTypes.Protected,
    Song.BonusBarrelIntroduction: MusicTypes.Protected,
    Song.TagBarrel: MusicTypes.Protected,
    Song.GameOver: MusicTypes.Protected,
    Song.KRoolDefeat: MusicTypes.Protected,
    # System
    Song.Silence: MusicTypes.System,
    Song.TransitionOpen: MusicTypes.System,
    Song.TransitionClose: MusicTypes.System,
    Song.NintendoLogoOld: MusicTypes.System,
}
heap_size = 0x34000 + music_size
flut_size = 0
MODEL_DIRECTORY = "assets/models/"
KONG_MODEL_EXP_SIZE = 0x5000

INSTRUMENT_PADS = {
    168: "bongo",
    169: "guitar",
    170: "sax",
    171: "triangle",
    172: "trombone",
}

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
    "ap",
    "fakebean",
    "fakekey",
    "shared",
    "soldout",
    "null",
    "fakefairy",
    "ap_useful",
    "ap_junk",
    "ap_trap",
)


def getBonusSkinOffset(offset: int):
    """Get texture index after the barrel skins."""
    return 6026 + (3 * len(barrel_skins)) + offset


def intf_to_float(intf):
    """Convert float as int format to float."""
    if intf == 0:
        return 0
    else:
        return struct.unpack("!f", bytes.fromhex("{:08X}".format(intf)))[0]


def float_to_hex(f):
    """Convert float to hex."""
    if f == 0:
        return "0x00000000"
    return hex(struct.unpack("<I", struct.pack("<f", f))[0])


def getMusicType(song) -> MusicTypes:
    """Get the music type from song num."""
    return music_type_mapping.get(song, MusicTypes.Protected)


def getMusicSize(song) -> int:
    """Get the allocated size for a song in ROM."""
    mtype = getMusicType(song)
    if mtype not in music_sizes_fine:
        with open(ROMName, "rb") as fh:
            fh.seek(main_pointer_table_offset)
            music_table = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            fh.seek(music_table + (song * 4))
            file_start = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            file_end = main_pointer_table_offset + int.from_bytes(fh.read(4), "big")
            fh.seek(file_start)
            try:
                return len(zlib.decompress(fh.read(file_end - file_start), (15 + 32)))
            except Exception:
                return 16000
    return music_sizes_fine[mtype]


def hueShift(im: Image, amount: int):
    """Apply a hue shift on an image."""
    hsv_im = im.convert("HSV")
    im_px = im.load()
    w, h = hsv_im.size
    hsv_px = hsv_im.load()
    for y in range(h):
        for x in range(w):
            old = list(hsv_px[x, y]).copy()
            old[0] = (old[0] + amount) % 360
            hsv_px[x, y] = (old[0], old[1], old[2])
    rgb_im = hsv_im.convert("RGB")
    rgb_px = rgb_im.load()
    for y in range(h):
        for x in range(w):
            new = list(rgb_px[x, y])
            new.append(list(im_px[x, y])[3])
            im_px[x, y] = (new[0], new[1], new[2], new[3])
    return im


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


def convertToI4(png_file):
    """Convert PNG to I4 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".i4")
    polarity = 0
    value = 0
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                intensity = int((r + g + b) / 3) >> 4
                if polarity == 0:
                    value = intensity << 4
                    polarity = 1
                elif polarity == 1:
                    value |= intensity
                    polarity = 0
                    fh.write(value.to_bytes(1, "big"))
                    value = 0
        if polarity != 0:
            fh.write(value.to_bytes(1, "big"))


def convertToI8(png_file):
    """Convert PNG to I8 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".i8")
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                intensity = int((r + g + b) / 3)
                fh.write(intensity.to_bytes(1, "big"))


def convertToIA4(png_file):
    """Convert PNG to IA4 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".ia4")
    polarity = 0
    value = 0
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                intensity = int((r + g + b) / 3) >> 5
                alpha = 1 if a > 0 else 0
                output = intensity << 1 | alpha
                if polarity == 0:
                    value = output << 4
                    polarity = 1
                elif polarity == 1:
                    value |= output
                    polarity = 0
                    fh.write(value.to_bytes(1, "big"))
                    value = 0
        if polarity != 0:
            fh.write(value.to_bytes(1, "big"))


def convertToIA8(png_file):
    """Convert PNG to IA8 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".ia8")
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                intensity = int((r + g + b) / 3) >> 4
                alpha = a >> 4
                value = (intensity << 4) | alpha
                fh.write(value.to_bytes(1, "big"))


def convertToRGBA5551(png_file):
    """Convert PNG to RGBA5551 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".rgba5551")
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                has_alpha = 1 if a > 0 else 0
                data = ((r >> 3) << 11) | ((g >> 3) << 6) | ((b >> 3) << 1) | has_alpha
                fh.write(data.to_bytes(2, "big"))


def convertToRGBA32(png_file):
    """Convert PNG to RGBA32 binary."""
    im = Image.open(png_file).convert("RGBA")
    width, height = im.size
    new_file = png_file.replace(".png", ".rgba32")
    with open(new_file, "wb") as fh:
        for y in range(height):
            for x in range(width):
                r, g, b, a = im.getpixel((x, y))
                fh.write((r & 0xFF).to_bytes(1, "big"))
                fh.write((g & 0xFF).to_bytes(1, "big"))
                fh.write((b & 0xFF).to_bytes(1, "big"))
                fh.write((a & 0xFF).to_bytes(1, "big"))


def imageToMinMap(img_path: str):
    """Convert an image to a min map rgba5551 texture."""
    mode = 3
    out_name = img_path.replace(".png", "_mipped.png")

    with open(img_path, "rb") as file:
        pi = Image.open(file)
        pi = pi.transpose(Image.Transpose.FLIP_TOP_BOTTOM).resize((32, 32))
        dims = pi.size

        # mipmapping occurs for every 8-byte block, so this is 8 divided by bytesPerPixel.
        # for RGBA5551, bPP is 2
        pixelsPerBlock = 4

        match mode:
            case 0:
                # scramble/unscramble
                out = Image.new(mode="RGBA", size=dims)
                for y in range(dims[1]):
                    for x in range(dims[0]):
                        curpx = pi.getpixel((x, y))
                        newX = x
                        if y % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newX = x - floor(pixelsPerBlock / 2)
                            else:
                                newX = x + floor(pixelsPerBlock / 2)
                        out.putpixel((newX, y), curpx)
                out.save(f"unmipped_{file.name}")
            case 1:
                # break mipmapped textures into parts (parts are also unscrambled for good measure)
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, targetWidth))
                for y in range(dims[1]):
                    for x in range(dims[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {targetWidth}^2")
                            out.save(f"{targetWidth}_{file.name}")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            out = Image.new(mode="RGBA", size=(targetWidth, targetWidth))
                            pixelsWrittenSoFar = 0
                        curpx = pi.getpixel((x, y))
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newX = newX - floor(pixelsPerBlock / 2)
                            else:
                                newX = newX + floor(pixelsPerBlock / 2)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        out.putpixel((newX, newY), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break
            case 2:
                # assembles mipped texture from a series of images, READY TO PLACE INTO ROM
                # if in.png is the input file at 32x32, it stitches 32_in.png, 16_in.png, 8_in.png and 4_in.png together
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                # also theres like a 99 percent chance that this formula breaks with images that arent 32x32
                outY = int(targetWidth + targetWidth / 4 + targetWidth / 8)
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, outY))
                current_in = Image.open(open(f"{targetWidth}_in.png", "rb"))
                for y in range(out.size[1]):
                    for x in range(out.size[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {targetWidth}^2 image")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            current_in = Image.open(open(f"{targetWidth}_in.png", "rb"))
                            pixelsWrittenSoFar = 0
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        curpx = current_in.getpixel((newX, newY))
                        newerX = x
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newerX = x - floor(pixelsPerBlock / 2)
                            else:
                                newerX = x + floor(pixelsPerBlock / 2)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        out.putpixel((newerX, y), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break
                out.save(f"assembled_{file.name}")
            case 3:
                # take a 32x32 and mipmap it 4 times, READY TO PLACE INTO ROM
                # might work with other dimensions, not sure yet tbh
                targetWidth = dims[0]
                pixelsWrittenSoFar = 0
                timesResized = 0
                # also theres like a 99 percent chance that this formula breaks with images that arent 32x32
                outY = int(targetWidth + targetWidth / 4 + targetWidth / 8)
                safe = True
                out = Image.new(mode="RGBA", size=(targetWidth, outY))
                for y in range(out.size[1]):
                    for x in range(out.size[0]):
                        if pixelsWrittenSoFar == targetWidth**2:
                            # print(f"finished {tar}^2, shrinking")
                            timesResized += 1
                            if timesResized == 4:
                                safe = False
                                break
                            targetWidth = int(targetWidth / 2)
                            pi.thumbnail((targetWidth, targetWidth))
                            pixelsWrittenSoFar = 0
                        newX = x % targetWidth
                        newY = int(pixelsWrittenSoFar / targetWidth)
                        # print(f"{x}:{newX}  -  {y}:{newY}")
                        curpx = pi.getpixel((newX, newY))
                        newerX = x
                        if newY % 2 == 1:
                            if x % pixelsPerBlock > (pixelsPerBlock / 2) - 1:
                                newerX = x - math.floor(pixelsPerBlock / 2)
                            else:
                                newerX = x + math.floor(pixelsPerBlock / 2)
                        out.putpixel((newerX, y), curpx)
                        pixelsWrittenSoFar += 1
                    if not safe:
                        break

                out.save(out_name)
            case _:
                print("unknown mode")
