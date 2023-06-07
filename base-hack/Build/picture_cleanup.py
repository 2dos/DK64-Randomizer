"""Clean up an image to fix any alpha inaccuracies with the n64tex converter."""
import tkinter as tk
from tkinter import filedialog

from PIL import Image

root = tk.Tk()
root.withdraw()

file = filedialog.askopenfilename()
rwd_im = Image.open(file)
w, h = rwd_im.size
rwd_px = rwd_im.load()
for y in range(h):
    for x in range(w):
        px_data = list(rwd_px[x, y])
        if px_data[3] == 0:
            rwd_px[x, y] = (0, 0, 0, 0)
rwd_im.save(file)
