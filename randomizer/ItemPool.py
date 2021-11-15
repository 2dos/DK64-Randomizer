
levels = [
    "DK Isles",
    "Jungle Japes",
    "Angry Aztec",
    "Frantic Factory",
    "Gloomy Galleon",
    "Fungi Forest",
    "Crystal Caves",
    "Creepy Castle",
]

kongs = [
    "Donkey",
    "Diddy",
    "Lanky",
    "Tiny",
    "Chunky",
]

def GenerateBlueprints():
    blueprints = []
    for level in levels:
        for kong in kongs:
            blueprints.append(level + " " + kong + " Blueprint")
    return blueprints


def GenerateItemPool():
    itemPool = []

    # Kongs
    itemPool.extend([
        "diddy",
        "lanky",
        "tiny",
        "chunky",
    ])

    # Cranky abilities
    itemPool.extend(["Progressive Slam"] * 3)
    itemPool.extend([
        "Baboon Blast",
        "Strong Kong",
        "Gorilla Grab",
        "Chimpy Charge",
        "Rocketbarrel Boost",
        "Simian Spring",
        "Orangstand",
        "Baboon Balloon",
        "Orangstand Sprint",
        "Mini Monkey",
        "Pony Tail Twirl",
        "Monkeyport",
        "Hunky Chunky",
        "Primate Punch",
        "Gorilla Gone",
    ])

    # Weapons and their upgrades
    itemPool.extend([
        "Coconut",
        "Peanut",
        "Grape",
        "Feather",
        "Pineapple",
        "Homing Ammo",
        "Sniper Sight",
    ])
    itemPool.extend(["Progressive Ammo Belt"] * 2)

    # Instruments and their upgrades
    itemPool.extend([
        "Bongos",
        "Guitar",
        "Trombone",
        "Saxophone",
        "Triangle",
    ])
    itemPool.extend(["Progressive Instrument Upgrade"] * 3)

    # Collectibles
    itemPool.extend(["Golden Banana"] * 201)
    itemPool.extend(GenerateBlueprints())
    itemPool.extend(["Banana Fairy"] * 20)
    itemPool.extend(["Battle Crown"] * 10)
    itemPool.extend(["Banana Medal"] * 5)
    itemPool.append("Nintendo Coin")
    itemPool.append("Rareware Coin")

    itemPool.append("Camera and Shockwave")

    return itemPool