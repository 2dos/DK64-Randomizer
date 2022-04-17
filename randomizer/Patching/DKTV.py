"""Setting data related to DKTV."""
import random

import js
from randomizer.Patching.Patcher import ROM


def randomize_dktv():
    """Set our DKTV to a random intro."""
    available_demos = [0, 1, 2, 3, 4, 5]
    vanilla_data = [
        0x040001E0,  # DK - Japes
        0x00000294,  # Diddy - Minecart
        0x010001E0,  # Lanky - Temple
        0x03000258,  # Tiny - Race
        0x02000258,  # Chunky - Underground
        0x050001E0,  # DK - Seal Race (Length is assumed)
    ]
    random.shuffle(available_demos)
    for x in range(5):
        ROM().seek(0x1FED020 + 0x14C + (x * 4))
        selected_demo = available_demos[x]
        ROM().writeMultipleBytes(vanilla_data[selected_demo], 4)
