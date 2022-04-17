from PIL import Image
import PIL
import os

print("Composing complex images")
number_crop = [
	{
		"image": "01234.png",
		"image_list":[
			{
				"num":0,
				"crop":(0,0,20,24)
			},
			{
				"num":1,
				"crop":(20,0,30,24)
			},
			{
				"num":2,
				"crop":(30,0,45,24)
			},
			{
				"num":3,
				"crop":(45,0,58,24)
			},
			{
				"num":4,
				"crop":(58,0,76,24)
			}
		]
	},
	{
		"image": "56789.png",
		"image_list":[
			{
				"num":5,
				"crop":(0,0,14,24)
			},
			{
				"num":6,
				"crop":(14,0,29,24)
			},
			{
				"num":7,
				"crop":(29,0,43,24)
			},
			{
				"num":8,
				"crop":(43,0,58,24)
			},
			{
				"num":9,
				"crop":(58,0,76,24)
			},
		]
	}
]

kongs = ["dk","diddy","lanky","tiny","chunky"]

hash_dir = "assets/Non-Code/hash/"
if not os.path.exists(hash_dir):
	os.mkdir(hash_dir)

for file_info in number_crop:
	for num_info in file_info["image_list"]:
		key_num = num_info["num"]
		if key_num >= 1 and key_num <= 8:
			base_dir = "assets/Non-Code/hash/"
			if not os.path.exists(base_dir):
				os.mkdir(base_dir)
			file_dir = f"{base_dir}{file_info['image']}"
			key_dir = f"{base_dir}boss_key.png"
			num_im = Image.open(file_dir)
			key_im = Image.open(key_dir)
			key_im = key_im.rotate(45, PIL.Image.NEAREST, expand=1)
			num_im = num_im.crop(num_info["crop"])
			Image.Image.paste(key_im,num_im, (40,10))
			bbox = key_im.getbbox()
			key_im = key_im.crop(bbox)
			key_im = key_im.resize((32,32))
			key_im.save(f"assets/Non-Code/file_screen/key{key_num}.png")
for kong in kongs:
	base_dir = "assets/Non-Code/displays/"
	if not os.path.exists(base_dir):
		os.mkdir(base_dir)
	im = Image.new(mode="RGBA", size=(64, 64))
	for x in range(2):
		im1 = Image.open(f"{hash_dir}{kong}_face_{x}.png")
		x_p = 32 * x
		if kong == "dk" or kong == "tiny":
			x_p = 32 - x_p
		Image.Image.paste(im,im1,(x_p,0))
	im = im.resize((32,32))
	im.save(f"{base_dir}{kong}_face.png")

# Generate Shared Image
im = Image.new(mode="RGBA", size=(64, 64))
shared_x_move=[4,16,30,10,26]
shared_y_move=[0,0,0,23,23]
kong_z_order=[0,1,2,3,4]
disp_dir = "assets/Non-Code/displays/"
for x in range(5):
	kong_index = kong_z_order[x]
	im1 = Image.open(f"{disp_dir}{kongs[kong_index]}_face.png")
	im.paste(im1,(shared_x_move[kong_index],shared_y_move[kong_index]),im1)
bbox = im.getbbox()
im = im.crop(bbox)
im = im.resize((32,32))
im.save(f"{disp_dir}shared.png")
im = Image.new(mode="RGBA", size=(32, 32))
im.save(f"{disp_dir}none.png")

rmve = ["01234.png","56789.png","boss_key.png"]
for kong in kongs:
	for x in range(2):
		rmve.append(f"{kong}_face_{x}.png")
for x in rmve:
	if os.path.exists(f"assets/Non-Code/hash/{x}"):
		os.remove(f"assets/Non-Code/hash/{x}")