"""Create complex images from in-game assets."""

import os

import PIL
from PIL import Image

pre = "../"
cwd = os.getcwd()
cwd_split = cwd.split("\\")
last_part = cwd_split[-1]
pre = ""
if last_part.upper() == "BUILD":
    pre = "../"


def getDir(directory):
    """Convert directory into the right format based on where the script is run."""
    return f"{pre}{directory}"


print("Composing complex images")
number_crop = [
    {
        "image": "01234.png",
        "image_list": [
            {"num": 0, "crop": (0, 0, 20, 24)},
            {"num": 1, "crop": (20, 0, 30, 24)},
            {"num": 2, "crop": (30, 0, 45, 24)},
            {"num": 3, "crop": (45, 0, 58, 24)},
            {"num": 4, "crop": (58, 0, 76, 24)},
        ],
    },
    {
        "image": "56789.png",
        "image_list": [
            {"num": 5, "crop": (0, 0, 14, 24)},
            {"num": 6, "crop": (14, 0, 29, 24)},
            {"num": 7, "crop": (29, 0, 43, 24)},
            {"num": 8, "crop": (43, 0, 58, 24)},
            {"num": 9, "crop": (58, 0, 76, 24)},
        ],
    },
]

kongs = ["dk", "diddy", "lanky", "tiny", "chunky"]

hash_dir = getDir("assets/Non-Code/hash/")
if not os.path.exists(hash_dir):
    os.mkdir(hash_dir)
kong_res = (32, 32)
for kong in kongs:
    base_dir = getDir("assets/Non-Code/displays/")
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    im = Image.new(mode="RGBA", size=(64, 64))
    for x in range(2):
        im1 = Image.open(f"{hash_dir}{kong}_face_{x}.png")
        x_p = 32 * x
        if kong in ("dk", "tiny"):
            x_p = 32 - x_p
        Image.Image.paste(im, im1, (x_p, 0))
    im = im.resize(kong_res)
    # im = im.resize((32,32))
    im.save(f"{base_dir}{kong}_face.png")

# Generate Shared Image
im = Image.new(mode="RGBA", size=(64, 64))
shared_x_move = [4, 16, 30, 10, 26]
shared_y_move = [0, 0, 0, 23, 23]
kong_z_order = [0, 1, 2, 3, 4]
disp_dir = getDir("assets/Non-Code/displays/")
for x in range(5):
    kong_index = kong_z_order[x]
    im1 = Image.open(f"{disp_dir}{kongs[kong_index]}_face.png")
    im.paste(im1, (shared_x_move[kong_index], shared_y_move[kong_index]), im1)
bbox = im.getbbox()
im = im.crop(bbox)
im = im.resize(kong_res)
im.save(f"{disp_dir}shared.png")
im = Image.new(mode="RGBA", size=kong_res)
im.save(f"{disp_dir}none.png")
im = Image.new(mode="RGBA", size=(44, 44))
im.save(f"{disp_dir}empty44.png")
im = Image.new(mode="RGBA", size=(32, 64))
im.save(f"{disp_dir}empty3264.png")
im = Image.new(mode="RGBA", size=(1, 1))
im.save(f"{disp_dir}empty11.png")
#
im = Image.open(f"{disp_dir}soldout_bismuth.png")
im_height = 26
im = im.resize((32, im_height))
im1 = Image.new(mode="RGBA", size=(32, 32))
Image.Image.paste(im1, im, (0, int((32 - im_height) / 2)))
im1.save(f"{disp_dir}soldout32.png")

# Generate / in spot of unused L button
im = Image.open(f"{hash_dir}specialchars.png")
im = im.crop((30, 0, 55, 32))
bbox = im.getbbox()
im = im.crop(bbox)
imw, imh = im.size
if imh == 0:
    imh = 1
imhb = 22
scale = imhb / imh
imw = int(imw * scale)
im = im.resize((imw, imhb))
im1 = Image.open(f"{hash_dir}WXYL.png")
im2 = Image.new(mode="RGBA", size=(32, 32))
Image.Image.paste(im1, im2, (61, 0))
Image.Image.paste(im1, im, (65, 1))
im1.save(f"{disp_dir}wxys.png")

# Generate Yellow Q Mark
for idx in range(2):
    im = Image.open(f"{hash_dir}red_qmark_{idx}.png")
    im_hsv = im.convert("HSV")
    H, S, V = im_hsv.split()
    H = H.point(lambda p: p + 40 if p < 10 else p)
    im_hsv = Image.merge("HSV", (H, S, V))
    im_rgb = im_hsv.convert("RGBA")
    pix_alpha = im.load()
    imw, imh = im.size
    pix_hsv = im_rgb.load()
    im_new = Image.new(mode="RGBA", size=(imw, imh))
    pix_new = im_new.load()
    for x in range(imw):
        for y in range(imh):
            r, g, b, a = im.getpixel((x, y))
            r2, g2, b2, a2 = im_rgb.getpixel((x, y))
            pix_new[x, y] = (r2, g2, b2, a)
    im_new.save(f"{disp_dir}yellow_qmark_{idx}.png")

# Ammo Crates
crate_names = ["standard_crate", "homing_crate"]
for crate in crate_names:
    base_dir = getDir("assets/Non-Code/displays/")
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    im = Image.new(mode="RGBA", size=(64, 64))
    crate_r_offset = 0
    for x in range(2):
        im1 = Image.open(f"{hash_dir}{crate}_{x}.png")
        x_p = 32 * x
        y_p = 0
        if x == 1:
            y_p = crate_r_offset
        Image.Image.paste(im, im1, (x_p, y_p))
    im = im.resize(kong_res)
    # im = im.resize((32,32))
    im.save(f"{base_dir}{crate}.png")

# Number Game Images
# 6 (1 as template)
lit = ["num_6_lit", "num_1_lit"]
unlit = ["num_6_unlit", "num_1_unlit"]
num_types = [lit, unlit]
base_dir = getDir("assets/Non-Code/displays/")
hash_dir = getDir("assets/Non-Code/hash/")
for num_type in num_types:
    number = num_type[0]
    line_num = num_type[1]
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    line_im = Image.open(f"{hash_dir}{line_num}.png")
    line = line_im.crop((13, 5, 16, 18))
    line_90 = line.rotate(90, PIL.Image.Resampling.NEAREST, expand=1)
    num_im = Image.open(f"{hash_dir}{number}.png")
    line_y = 2
    num_im.paste(line_90, (5, line_y), line_90)
    num_im.paste(line_90, (12, line_y), line_90)
    num_im.save(f"{base_dir}{number}.png")
# 9 (7 as template)
lit = ["num_9_lit", "num_7_lit"]
unlit = ["num_9_unlit", "num_7_unlit"]
num_types = [lit, unlit]
for num_type in num_types:
    number = num_type[0]
    line_num = num_type[1]
    line_im = Image.open(f"{hash_dir}{line_num}.png")
    line = line_im.crop((10, 23, 22, 26))
    num_im = Image.open(f"{hash_dir}{number}.png")
    line_y = 1
    num_im.paste(line, (7, line_y), line)
    num_im.paste(line, (14, line_y), line)
    num_im.save(f"{base_dir}{number}.png")

# Tracker Image
tracker_im = Image.new(mode="RGBA", size=(254, 128))
instruments = ("bongos", "guitar", "trombone", "sax", "triangle")
pellets = ("coconut", "peanut", "grape", "feather", "pineapple")
extra_moves = ("film", "shockwave", "slam", "homing_crate", "sniper")
training_moves = ("swim", "orange", "barrel", "vine")
kong_submoves = ("_move", "pad", "barrel")
dim = 20
gap = int(dim * 1.1)
small_gap = int(dim * 0.8)
for ins_index, instrument in enumerate(instruments):
    ins_im = Image.open(f"{hash_dir}{instrument}.png")
    ins_im = ins_im.resize((dim, dim))
    tracker_im.paste(ins_im, (gap * ins_index, gap), ins_im)
for pel_index, pellet in enumerate(pellets):
    pel_im = Image.open(f"{hash_dir}{pellet}.png")
    if pellet == "pineapple":
        pel_im = pel_im.resize((dim, int(dim * 1.5)))
    elif pellet == "coconut":
        pel_im = pel_im.resize((dim, int(dim * 1.275)))
    else:
        pel_im = pel_im.resize((dim, dim))
    tracker_im.paste(pel_im, (gap * pel_index, 0), pel_im)
for kong_index, kong in enumerate(kongs):
    for sub_index, sub in enumerate(kong_submoves):
        move_im = Image.open(f"{getDir('assets/Non-Code/file_screen/')}tracker_images/{kong}{sub}.png")
        move_im = move_im.resize((dim, dim))
        tracker_im.paste(move_im, ((gap * kong_index), ((sub_index + 2) * gap)), move_im)
for move_index, move in enumerate(extra_moves):
    if move in ("homing_crate"):
        move_im = Image.open(f"{base_dir}{move}.png")
    elif move in ("film"):
        move_im = Image.open(f"{hash_dir}{move}.png")
    else:
        move_im = Image.open(f"{getDir('assets/Non-Code/file_screen/')}tracker_images/{move}.png")
    move_im = move_im.resize((dim, dim))
    tracker_im.paste(move_im, ((6 * gap), (move_index * gap)), move_im)
for move_index, move in enumerate(training_moves):
    if move in ("orange"):
        move_im = Image.open(f"{hash_dir}{move}.png")
    else:
        move_im = Image.open(f"{getDir('assets/Non-Code/file_screen/')}tracker_images/{move}.png")
    move_im = move_im.resize((dim, dim))
    tracker_im.paste(move_im, ((move_index * gap), 128 - dim), move_im)
for file_info in number_crop:
    for num_info in file_info["image_list"]:
        key_num = num_info["num"]
        if key_num >= 1 and key_num <= 8:
            base_dir = getDir("assets/Non-Code/hash/")
            if not os.path.exists(base_dir):
                os.mkdir(base_dir)
            file_dir = f"{base_dir}{file_info['image']}"
            key_dir = f"{base_dir}boss_key.png"
            num_im = Image.open(file_dir)
            key_im = Image.open(key_dir)
            num_im = num_im.crop(num_info["crop"])
            num_w, num_h = num_im.size
            targ_h = 36
            num_im_scale = targ_h / num_h
            new_w = int(num_w * num_im_scale)
            num_im = num_im.resize((new_w, targ_h))
            key_im.paste(num_im, (targ_h - num_w - [5, 0, 2, -2, 0, -1, 0, -1][key_num - 1], 2), num_im)
            key_im = key_im.resize((20, 20))
            key_im.save(f"{getDir('assets/Non-Code/file_screen/key')}{key_num}.png")
            tracker_im.paste(key_im, (249 - (small_gap * (9 - key_num)), 128 - dim), key_im)
for melon in range(3):
    melon_im = Image.open(f"{hash_dir}melon.png")
    melon_im = melon_im.resize((dim, dim))
    tracker_im.paste(melon_im, (200 - (small_gap * melon), 0), melon_im)
prog_offset = 218
for p_i, progressive in enumerate([f"{hash_dir}headphones.png", f"{disp_dir}standard_crate.png"]):
    prog_im = Image.open(progressive)
    prog_im = prog_im.resize((dim, dim))
    tracker_im.paste(prog_im, (prog_offset, gap + (p_i * gap)), prog_im)
    num_im = Image.open(f"{hash_dir}01234.png")
    num_im = num_im.crop((30, 0, 45, 24))
    num_w, num_h = num_im.size
    num_size = 15
    num_scale = num_size / num_h
    new_w = int(num_w * num_scale)
    num_im = num_im.resize((new_w, num_size))
    tracker_im.paste(num_im, (prog_offset + [22, 17][p_i], int(gap + 3 + (p_i * small_gap * 1.2))), num_im)

tracker_im.save(f"{getDir('assets/Non-Code/file_screen/')}tracker.png")

# Nin/RW Coin Objects
for coin in ("nin_coin", "rw_coin"):
    loc = f"{hash_dir}{coin}.png"
    coin_im = Image.open(loc)
    coin_im = coin_im.crop((2, 0, 28, 31))
    coin_im = coin_im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
    coin_im = coin_im.resize((64, 64))
    coin_im_0 = coin_im.crop((0, 0, 32, 64))
    coin_im_1 = coin_im.crop((32, 0, 64, 64))
    coin_im_0.save(f"{hash_dir}{coin}_0.png")
    coin_im_1.save(f"{hash_dir}{coin}_1.png")
side_im = Image.open(f"{hash_dir}special_coin_side.png")
side_im = side_im.crop((17, 3, 25, 19))
side_im = side_im.resize((32, 16))
side_im = side_im.rotate(90, PIL.Image.Resampling.NEAREST, expand=1)
side_im.save(f"{hash_dir}modified_coin_side.png")

# Krusha Head
krusha_im = Image.open(f"{disp_dir}krusha_head.png")
krusha_im = krusha_im.resize((64, 64))
krusha_im = krusha_im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
krusha_im.save(f"{disp_dir}krusha_head64.png")

# Blueprints
for bp in ("dk_bp", "lanky_bp"):
    bp_im = Image.open(f"{hash_dir}{bp}.png")
    bp_im = bp_im.crop((8, 2, 40, 34))
    bp_im.save(f"{disp_dir}{bp}.png")

# Shop indicator items (44x44)
for item in ("crown_shop", "gb", "key", "medal"):
    item_im = Image.open(f"{hash_dir}{item}.png")
    item_im = item_im.resize((32, 32))
    item_im.save(f"{disp_dir}{item}.png")

# Smaller potion image
potion_im = Image.open(f"{disp_dir}potion.png")
potion_im = potion_im.resize((32, 32))
potion_im.save(f"{disp_dir}potion32.png")

# Coins
for coin in ("nin_coin", "rw_coin"):
    coin_im = Image.open(f"{hash_dir}{coin}.png")
    coin_im.save(f"{disp_dir}{coin}.png")

# # Christmas Theme
# snow_by = []
# snow_im = Image.open(f"{disp_dir}snow.png")
# for dim in (32, 16, 8, 4):
#     snow_im = snow_im.resize((dim, dim))
#     snow_px = snow_im.load()
#     for y in range(dim):
#         for x in range(dim):
#             px_data = list(snow_px[x, y])
#             data = 0
#             for c in range(3):
#                 data |= (px_data[c] >> 3) << (1 + (5 * c))
#             if px_data[3] != 0:
#                 data |= 1
#             snow_by.extend([(data >> 8), (data & 0xFF)])
# with open(f"{disp_dir}snow.bin","wb") as fh:
#     fh.write(bytearray(snow_by))


rmve = [
    "01234.png",
    "56789.png",
    "boss_key.png",
    "WXYL.png",
    "specialchars.png",
    "red_qmark_0.png",
    "red_qmark_1.png",
    "headphones.png",
    "film.png",
    "melon.png",
    "dk_bp.png",
    "lanky_bp.png",
    "crown_shop.png",
    "gb.png",
    "key.png",
    "medal.png",
]
for kong in kongs:
    for x in range(2):
        rmve.append(f"{kong}_face_{x}.png")
for x in rmve:
    if os.path.exists(f"{getDir('assets/Non-Code/hash/')}{x}"):
        os.remove(f"{getDir('assets/Non-Code/hash/')}{x}")
