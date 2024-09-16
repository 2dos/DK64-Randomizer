"""Location/item type enum."""


from randomizer.JsonReader import generate_globals
from typing import TYPE_CHECKING
import json

if TYPE_CHECKING:
    from randomizer.Enums.Types import Types

globals().update(generate_globals(__file__))

with open("randomizer/Enums/Types.json", "r") as f:
    _data = json.load(f)
    KeySelector = _data["KeySelector"]
    ItemRandoSelector = _data["ItemRandoSelector"]