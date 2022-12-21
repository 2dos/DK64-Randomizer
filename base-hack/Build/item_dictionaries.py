"""Database of items, which will create some C code to reduce code maintainence issues when adding new item types to item rando."""


class InGameItem:
    """Class to define an in-game item."""

    def __init__(self, *, name="", actor=0, model_two=0, scale=0.25, base=None, force_dance=True, boss_enabled=True, bounce=False, will_dance=True, is_null=False):
        """Initialize with given parameters."""
        if base is not None:
            self.name = base.name
            self.actor = base.actor
            self.model_two = base.model_two
            self.scale = base.scale
            self.force_dance = base.force_dance
            self.boss_enabled = base.boss_enabled
            self.bounce = base.bounce
            self.will_dance = base.will_dance
            self.is_null = base.is_null
        self.name = name
        self.actor = actor
        self.model_two = model_two
        self.scale = scale
        self.force_dance = force_dance  # Force dance if in boss/crown
        self.boss_enabled = boss_enabled  # Can be a boss reward
        self.bounce = bounce  # Will bounce (excl sprites)
        self.will_dance = will_dance  # Produces dance animation upon grabbing it (if auto-dance skip off)
        self.is_null = is_null


base_potion = InGameItem(scale=0.25, bounce=True)
base_kong = InGameItem(scale=0.25, bounce=True)
base_bp = InGameItem(scale=2, will_dance=False)
base_coin = InGameItem(scale=0.4, will_dance=False)

db = [
    InGameItem(name="Golden Banana", actor=45, model_two=0x74, scale=0.25, bounce=True),
    InGameItem(name="DK Blueprint", actor=78, model_two=0xDE, base=base_bp, scale=2),
    InGameItem(name="Diddy Blueprint", actor=75, model_two=0xE0, base=base_bp, scale=2),
    InGameItem(name="Lanky Blueprint", actor=77, model_two=0xE1, base=base_bp, scale=2),
    InGameItem(name="Tiny Blueprint", actor=79, model_two=0xDD, base=base_bp, scale=2),
    InGameItem(name="Chunky Blueprint", actor=76, model_two=0xDF, base=base_bp, scale=2),
    InGameItem(name="Nintendo Coin", actor=151, model_two=0x48, base=base_coin, scale=0.4),
    InGameItem(name="Rareware Coin", actor=152, model_two=0x28F, base=base_coin, scale=0.4),
    InGameItem(name="Boss Key", actor=72, model_two=0x13C, scale=0.17, bounce=True),
    InGameItem(name="Battle Crown", actor=86, model_two=0x18D, scale=0.25, bounce=True),
    InGameItem(name="Banana Medal", actor=154, model_two=0x90, scale=0.22),
    InGameItem(name="DK Potion", actor=157, model_two=0x5B, base=base_potion, bounce=True),
    InGameItem(name="Diddy Potion", actor=158, model_two=0x1F2, base=base_potion, bounce=True),
    InGameItem(name="Lanky Potion", actor=159, model_two=0x59, base=base_potion, bounce=True),
    InGameItem(name="Tiny Potion", actor=160, model_two=0x1F3, base=base_potion, bounce=True),
    InGameItem(name="Chunky Potion", actor=161, model_two=0x1F5, base=base_potion, bounce=True),
    InGameItem(name="Any Potion", actor=162, model_two=0x1F6, base=base_potion, bounce=True),
    InGameItem(name="No Item", actor=153, model_two=0x0, scale=0.25, force_dance=False, boss_enabled=False, is_null=True),
    InGameItem(name="DK Item", actor=141, model_two=0x257, base=base_kong, bounce=True),
    InGameItem(name="Diddy Item", actor=142, model_two=0x258, base=base_kong, bounce=True),
    InGameItem(name="Lanky Item", actor=143, model_two=0x259, base=base_kong, bounce=True),
    InGameItem(name="Tiny Item", actor=144, model_two=0x25A, base=base_kong, bounce=True),
    InGameItem(name="Chunky Item", actor=155, model_two=0x25B, base=base_kong, bounce=True),
    InGameItem(name="Bean", actor=172, model_two=0x198, scale=0.25, will_dance=False),
    InGameItem(name="Pearl", actor=174, model_two=0x1B4, scale=0.25, will_dance=False),
]

dance_acceptable_items = [x for x in db if x.force_dance]
boss_enabled_items = [x for x in db if x.boss_enabled]
bounce_items = [x for x in db if x.bounce]
actor_drops = [x for x in db if x.actor is not None]
danceless_items = [x for x in db if not x.will_dance]
warning_text_data = [
    "This is a pre-generated file. Please don't directly modify this file as this will be overwritten upon next build.",
    "Visit build/item_dictionaries.py to modify this output.",
    "\nThanks,",
    "\tBallaam",
]
warning_text = "/*\n\t" + "\n\t".join(warning_text_data) + "\n*/\n"

with open("include/item_data.h", "w") as fh:
    fh.write(warning_text)
    fh.write(f"extern const short acceptable_items[{len(dance_acceptable_items)}];\n")
    fh.write(f"extern const item_conversion_info item_conversions[{len(boss_enabled_items)}];\n")
    fh.write(f"extern const unsigned char bounce_objects[{len(bounce_items)}];\n")
    fh.write(f"extern const unsigned char actor_drops[{len(actor_drops)}];\n")
    fh.write(f"extern const unsigned char danceless_items[{len(danceless_items)}];\n")

with open("src/lib_items.c", "w") as fh:
    fh.write('#include "../include/common.h"\n\n')
    fh.write(warning_text)
    fh.write("\nconst short acceptable_items[] = {" + ",".join([hex(x.model_two) for x in dance_acceptable_items]) + "};")
    fh.write("\nconst item_conversion_info item_conversions[] = {\n\t" + ",\n\t".join([f"{{.actor={x.actor}, .model_two={x.model_two}, .scale={x.scale:.2f}f}}" for x in boss_enabled_items]) + "\n};")
    fh.write("\nconst unsigned char bounce_objects[] = {" + ",".join([str(x.actor) for x in bounce_items]) + "};")
    fh.write("\nconst unsigned char actor_drops[] = {" + ",".join([str(x.actor) for x in actor_drops]) + "};")
    fh.write("\nconst unsigned char danceless_items[] = {" + ",".join([str(x.actor) for x in danceless_items]) + "};")
