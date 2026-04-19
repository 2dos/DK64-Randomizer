"""Script to write the full_item_table from DK64 to a file."""

import sys
from types import ModuleType


def _inject_ap_stubs() -> None:
    """
    Inject minimal Archipelago stubs so archipelago.Items can be imported without AP installed.

    full_item_table is built entirely from DK64R's own ItemList; the AP types
    (Item, ItemClassification, World, etc.) only appear in class/function
    definitions that are never executed during table construction.
    """
    # --- BaseClasses ---
    bc = ModuleType("BaseClasses")

    class _ItemClassification:
        progression = "progression"
        useful = "useful"
        filler = "filler"
        trap = "trap"
        progression_skip_balancing = "progression_skip_balancing"
        progression_deprioritized = "progression_deprioritized"

    bc.Item = type("Item", (), {"game": ""})  # type: ignore[attr-defined]
    bc.ItemClassification = _ItemClassification  # type: ignore[attr-defined]
    for _name in ("PlandoOptions", "MultiWorld", "CollectionState", "Location", "LocationProgressType", "Region", "Entrance", "EntranceType", "Tutorial"):
        setattr(bc, _name, type(_name, (), {}))
    sys.modules["BaseClasses"] = bc

    # --- worlds / worlds.AutoWorld ---
    worlds_mod = ModuleType("worlds")
    aw_mod = ModuleType("worlds.AutoWorld")
    aw_mod.World = type("World", (), {})  # type: ignore[attr-defined]
    aw_mod.WebWorld = type("WebWorld", (), {})  # type: ignore[attr-defined]
    worlds_mod.AutoWorld = aw_mod  # type: ignore[attr-defined]
    sys.modules.setdefault("worlds", worlds_mod)
    sys.modules["worlds.AutoWorld"] = aw_mod

    # --- Options (AP's Options module, not Python's) ---
    opt_mod = ModuleType("Options")

    class _Base:
        def __init__(self, *args, **kwargs):
            pass

    for _name in ("Choice", "PerGameCommonOptions", "Range", "Option", "OptionDict", "OptionList", "Toggle", "DeathLink", "DefaultOnToggle", "OptionGroup", "TextChoice"):
        setattr(opt_mod, _name, type(_name, (_Base,), {}))
    opt_mod.OptionError = type("OptionError", (Exception,), {})  # type: ignore[attr-defined]
    sys.modules["Options"] = opt_mod

    # --- entrance_rando (imported by some AP modules) ---
    sys.modules.setdefault("entrance_rando", ModuleType("entrance_rando"))


_inject_ap_stubs()

from archipelago.Items import full_item_table  # noqa: E402


def write_item_table():
    """Write the full_item_table to a text file."""
    with open("dk64_full_item_table.txt", "w") as f:
        f.write("DK64 Full Item Table\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Total items: {len(full_item_table)}\n\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Item Name':<50} {'Item ID':<12} {'Progression':<12}\n")
        f.write("-" * 80 + "\n")

        # Sort by item code for better readability
        sorted_items = sorted(full_item_table.items(), key=lambda x: x[1].code if x[1].code else 0)

        for item_name, item_data in sorted_items:
            item_id = str(item_data.code) if item_data.code else "None"
            progression = "Yes" if item_data.progression else "No"
            f.write(f"{item_name:<50} {item_id:<12} {progression:<12}\n")

    print(f"Successfully wrote {len(full_item_table)} items to dk64_full_item_table.txt")


if __name__ == "__main__":
    write_item_table()
