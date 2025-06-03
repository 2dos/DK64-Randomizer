"""Library functions for Item Rando."""

import random
from enum import IntEnum, auto
from randomizer.Enums.Items import Items
from randomizer.Enums.Types import Types
from randomizer.Enums.Locations import Locations

IceTrapItems = [
    Items.IceTrapBubble,
    Items.IceTrapReverse,
    Items.IceTrapSlow,
    Items.IceTrapBubbleBean,
    Items.IceTrapReverseBean,
    Items.IceTrapSlowBean,
    Items.IceTrapBubbleKey,
    Items.IceTrapReverseKey,
    Items.IceTrapSlowKey,
]


class CustomActors(IntEnum):
    """Custom Actors Enum."""

    NintendoCoin = 0x8000  # Starts at 0x8000
    RarewareCoin = auto()
    Null = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    KongDK = auto()
    KongDiddy = auto()
    KongLanky = auto()
    KongTiny = auto()
    KongChunky = auto()
    KongDisco = auto()
    KongKrusha = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    IceTrapBubble = auto()
    IceTrapReverse = auto()
    IceTrapSlow = auto()
    Medal = auto()
    JetpacItemOverlay = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    ZingerFlamethrower = auto()
    Scarab = auto()
    HintItemDK = auto()
    KopDummy = auto()
    HintItemDiddy = auto()
    HintItemLanky = auto()
    HintItemTiny = auto()
    HintItemChunky = auto()
    ArchipelagoItem = auto()


class GraphicOverlay(IntEnum):
    """Graphic Overlay Enum."""

    Banana = 0
    Blueprint = auto()
    Key = auto()
    Crown = auto()
    CompanyCoin = auto()
    Medal = auto()
    CrankyPotion = auto()
    FunkyPotion = auto()
    CandyPotion = auto()
    TrainingBarrel = auto()
    Shockwave = auto()
    Kong = auto()
    Bean = auto()
    Pearl = auto()
    Fairy = auto()
    RainbowCoin = auto()
    IceTrapBubble = auto()
    JunkMelon = auto()
    CrankyItem = auto()
    FunkyItem = auto()
    CandyItem = auto()
    SnideItem = auto()
    NoItem = auto()
    IceTrapReverse = auto()
    IceTrapSlow = auto()
    Hint = auto()


class ItemPlacementData:
    """Class to store information pertaining to writing Item Rando data."""

    def __init__(
        self,
        model_index: list[int] = None,
        kong_model_index: list[int] = None,
        model_two_index: list[int] = None,
        actor_index: list[int] = None,
        overlay: list[GraphicOverlay] = None,
        index_getter=None,
        preview_text: str = "",
        seal_preview_text: str = "",
        scale: float = 0.25,
    ):
        """Initialize with given parameters."""
        self.has_model = model_index is not None
        self.model_index = model_index
        if kong_model_index is None:
            self.kong_model_index = model_index
        else:
            self.kong_model_index = kong_model_index
        self.model_two_index = model_two_index
        self.actor_index = actor_index
        self.overlay = overlay
        if index_getter is None:
            self.index_getter = lambda item, flag, shared: 0
        else:
            self.index_getter = index_getter
        self.preview_text = preview_text
        self.seal_preview_text = seal_preview_text
        self.scale = scale


item_db = {
    Types.Banana: ItemPlacementData(
        model_index=[0x69],
        model_two_index=[0x74],
        actor_index=[45],
        overlay=[GraphicOverlay.Banana],
        preview_text="\x04GOLDEN BANANA\x04",
        seal_preview_text="\x04BANANA OF PURE GOLD\x04",
    ),
    Types.Key: ItemPlacementData(
        model_index=[0xF5], model_two_index=[0x13C], actor_index=[72], overlay=[GraphicOverlay.Key], preview_text="\x04BOSS KEY\x04", seal_preview_text="\x04KEY TO DAVY JONES LOCKER\x04", scale=0.17
    ),
    Types.Crown: ItemPlacementData(
        model_index=[0xF4],
        model_two_index=[0x18D],
        actor_index=[86],
        overlay=[GraphicOverlay.Crown],
        preview_text="\x04BATTLE CROWN\x04",
        seal_preview_text="\x04CROWN TO PLACE ATOP YER HEAD\x04",
    ),
    Types.Fairy: ItemPlacementData(
        model_index=[0x3D],
        model_two_index=[0x25C],
        actor_index=[CustomActors.Fairy],
        overlay=[GraphicOverlay.Fairy],
        preview_text="\x04BANANA FAIRY\x04",
        seal_preview_text="\x04MAGICAL FLYING PIXIE\x04",
    ),
    Types.Shop: ItemPlacementData(
        model_index=[0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB],
        model_two_index=[0x5B, 0x1F2, 0x59, 0x1F3, 0x1F5, 0x1F6],
        actor_index=[
            CustomActors.PotionDK,
            CustomActors.PotionDiddy,
            CustomActors.PotionLanky,
            CustomActors.PotionTiny,
            CustomActors.PotionChunky,
            CustomActors.PotionAny,
        ],
        overlay=[GraphicOverlay.CrankyPotion] * 6,  # Handled elsewhere
        index_getter=lambda item, flag, shared: (flag >> 12) & 7 if flag & 0x8000 and not shared and ((flag >> 12) & 7) < 5 else 5,
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.Shockwave: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        overlay=[GraphicOverlay.Shockwave],
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.TrainingBarrel: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        overlay=[GraphicOverlay.TrainingBarrel],
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.Climbing: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        overlay=[GraphicOverlay.TrainingBarrel],
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.Kong: ItemPlacementData(
        model_index=[4, 1, 6, 9, 0xC],
        model_two_index=[0x257, 0x258, 0x259, 0x25A, 0x25B],
        actor_index=[
            CustomActors.KongDK,
            CustomActors.KongDiddy,
            CustomActors.KongLanky,
            CustomActors.KongTiny,
            CustomActors.KongChunky,
        ],
        overlay=[GraphicOverlay.Kong],
        index_getter=lambda item, flag, shared: (385, 6, 70, 66, 117).index(flag),
        preview_text="\x04KONG\x04",
        seal_preview_text="\x04WEIRD MONKEY\x04",
    ),
    Types.FakeItem: ItemPlacementData(
        model_index=[
            0x103,
            0x103,
            0x103,
            0x127,
            0x127,
            0x127,
            0x128,
            0x128,
            0x128,
        ],
        kong_model_index=[0x103, 0x103, 0x103, 0x127, 0x127, 0x127, 0x128, 0x128, 0x128],
        model_two_index=[0x25D, 0x264, 0x265, 0x292, 0x293, 0x294, 0x295, 0x296, 0x297],
        actor_index=[
            CustomActors.IceTrapBubble,
            CustomActors.IceTrapReverse,
            CustomActors.IceTrapSlow,
            151,
            152,
            153,
            154,
            155,
            157,
        ],
        overlay=[GraphicOverlay.IceTrapBubble, GraphicOverlay.IceTrapReverse, GraphicOverlay.IceTrapSlow] * 3,
        index_getter=lambda item, flag, shared: IceTrapItems.index(item),
        preview_text="\x04GLODEN BANANE\x04",
        seal_preview_text="\x04BANANA OF FOOLS GOLD\x04",
    ),
    Types.Bean: ItemPlacementData(
        model_index=[0x104],
        model_two_index=[0x198],
        actor_index=[CustomActors.Bean],
        overlay=[GraphicOverlay.Bean],
        preview_text="\x04BEAN\x04",
        seal_preview_text="\x04QUESTIONABLE VEGETABLE\x04",
    ),
    Types.Pearl: ItemPlacementData(
        model_index=[0x106],
        model_two_index=[0x1B4],
        actor_index=[CustomActors.Pearl],
        overlay=[GraphicOverlay.Pearl],
        preview_text="\x04PEARL\x04",
        seal_preview_text="\x04BLACK PEARL\x04",
    ),
    Types.Medal: ItemPlacementData(
        model_index=[0x108],
        model_two_index=[0x90],
        actor_index=[CustomActors.Medal],
        overlay=[GraphicOverlay.Medal],
        preview_text="\x04BANANA MEDAL\x04",
        seal_preview_text="\x04MEDALLION\x04",
        scale=0.22,
    ),
    Types.NintendoCoin: ItemPlacementData(
        model_index=[0x10A],
        model_two_index=[0x48],
        actor_index=[CustomActors.NintendoCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="\x04NINTENDO COIN\x04",
        seal_preview_text="\x04ANCIENT DOUBLOON\x04",
        scale=0.4,
    ),
    Types.RarewareCoin: ItemPlacementData(
        model_index=[0x10C],
        model_two_index=[0x28F],
        actor_index=[CustomActors.RarewareCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="\x04RAREWARE COIN\x04",
        seal_preview_text="\x04DOUBLOON OF THE RAREST KIND\x04",
        scale=0.4,
    ),
    Types.JunkItem: ItemPlacementData(
        model_index=[0x10E],
        model_two_index=[0x25E],
        actor_index=[0x2F],
        overlay=[GraphicOverlay.JunkMelon],
        preview_text="\x04JUNK ITEM\x04",
        seal_preview_text="\x04HEAP OF JUNK\x04",
    ),
    Types.Cranky: ItemPlacementData(
        model_index=[0x11],
        model_two_index=[0x25F],
        actor_index=[CustomActors.CrankyItem],
        overlay=[GraphicOverlay.CrankyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Funky: ItemPlacementData(
        model_index=[0x12],
        model_two_index=[0x260],
        actor_index=[CustomActors.FunkyItem],
        overlay=[GraphicOverlay.FunkyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Candy: ItemPlacementData(
        model_index=[0x13],
        model_two_index=[0x261],
        actor_index=[CustomActors.CandyItem],
        overlay=[GraphicOverlay.CandyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Snide: ItemPlacementData(
        model_index=[0x1F],
        model_two_index=[0x262],
        actor_index=[CustomActors.SnideItem],
        overlay=[GraphicOverlay.SnideItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04NERDY SOUL\x04",
    ),
    Types.Hint: ItemPlacementData(
        model_index=[0x11B, 0x11D, 0x11F, 0x121, 0x123],
        model_two_index=[638, 649, 650, 651, 652],
        actor_index=[
            CustomActors.HintItemDK,
            CustomActors.HintItemDiddy,
            CustomActors.HintItemLanky,
            CustomActors.HintItemTiny,
            CustomActors.HintItemChunky,
        ],
        overlay=[GraphicOverlay.Hint],
        index_getter=lambda item, flag, shared: (flag - 0x384) % 5,
        preview_text="\x04HINT\x04",
        seal_preview_text="\x04LAYTON RIDDLE\x04",
    ),
    Types.Blueprint: ItemPlacementData(
        model_two_index=[0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
        actor_index=[78, 75, 77, 79, 76],
        overlay=[GraphicOverlay.Blueprint],
        index_getter=lambda item, flag, shared: (flag - 0x1D5) % 5,
        preview_text="\x04BLUEPRINT\x04",
        seal_preview_text="\x04MAP O' DEATH MACHINE\x04",
        scale=2,
    ),
    Types.RainbowCoin: ItemPlacementData(
        model_two_index=[0xB7],
        actor_index=[0x8C],
        overlay=[GraphicOverlay.RainbowCoin],
        preview_text="\x04RAINBOW COIN\x04",
        seal_preview_text="\x04COLORFUL COIN HIDDEN FOR 17 YEARS\x04",
    ),
    Types.NoItem: ItemPlacementData(
        model_two_index=[0],
        actor_index=[CustomActors.Null],
        overlay=[GraphicOverlay.NoItem],
        preview_text="\x04NOTHING\x04",
        seal_preview_text="\x04DIDDLY SQUAT\x04",
    ),
    Types.ArchipelagoItem: ItemPlacementData(
        model_index=[0x125],
        model_two_index=[0x291],
        actor_index=[CustomActors.ArchipelagoItem],
        overlay=[GraphicOverlay.Hint],
        preview_text="\x04ARCHIPELAGO ITEM\x04",
        seal_preview_text="\x04ANOTHER SCALLYWAG'S BOOTY\x04",
    ),
}

FILLER_MAPPING = {
    Types.FillerBanana: Types.Banana,
    Types.FillerCrown: Types.Crown,
    Types.FillerFairy: Types.Fairy,
    Types.FillerMedal: Types.Medal,
    Types.FillerPearl: Types.Pearl,
}

def getItemDBEntry(type: Types) -> ItemPlacementData:
    """Get the item db entry for an item type."""
    if type in FILLER_MAPPING:
        return item_db[FILLER_MAPPING[type]]
    return item_db[type]

def getIceTrapText(input_text: str) -> str:
    """Get the text associated with ice traps."""
    while True:
        characters = list(input_text)
        new_characters = []
        vowels = ["A", "E", "I", "O", "U"]
        vowels_in_string = [x for x in characters if x in vowels]
        unique_vowels = list(set(vowels_in_string))
        if len(vowels_in_string) < 3 or len(unique_vowels) < 2:
            if len(vowels_in_string) == 0:
                # Not sure what to do for strings with no vowels
                return input_text
            vowel_index = 0
            target_vowel_index = random.randint(0, len(vowels_in_string))
            for char in characters:
                if char in vowels:
                    if target_vowel_index == vowel_index:
                        new_characters.append(random.choice(vowels))
                        vowel_index += 1
                        continue
                    vowel_index += 1
                new_characters.append(char)
            new_text = "".join(new_characters)
        else:
            # More vowels
            vowel_idxs = random.sample(range(len(vowels_in_string)), 2)
            vowel_a = vowels_in_string[vowel_idxs[0]]
            vowel_b = vowels_in_string[vowel_idxs[1]]
            if vowel_a == vowel_b:
                continue
            vowels_in_string[vowel_idxs[1]] = vowel_a
            vowels_in_string[vowel_idxs[0]] = vowel_b
            for char in characters:
                if char in vowels:
                    new_characters.append(vowels_in_string.pop(0))
                else:
                    new_characters.append(char)
            new_text = "".join(new_characters)
        if new_text != input_text:
            return new_text


def getModelFromItem(item: Items, item_type: Types, flag: int, shared: bool = False, is_kong: bool = False) -> int:
    """Get the model index associated with an item."""
    if item_type not in item_db and item_type not in FILLER_MAPPING:
        return None
    item_db_entry = getItemDBEntry(item_type)
    if not item_db_entry.has_model:
        return None
    index = item_db_entry.index_getter(item, flag, shared)
    if is_kong:
        return item_db_entry.kong_model_index[index]
    return item_db_entry.model_index[index]


def getPropFromItem(item: Items, item_type: Types, flag: int, shared: bool = False) -> int:
    """Get the prop index associated with an item."""
    index = getItemDBEntry(item_type).index_getter(item, flag, shared)
    return getItemDBEntry(item_type).model_two_index[index]


IceTrapMasks = {
    Items.IceTrapBubble: Types.Banana,
    Items.IceTrapReverse: Types.Banana,
    Items.IceTrapSlow: Types.Banana,
    Items.IceTrapBubbleBean: Types.Bean,
    Items.IceTrapReverseBean: Types.Bean,
    Items.IceTrapSlowBean: Types.Bean,
    Items.IceTrapBubbleKey: Types.Key,
    Items.IceTrapReverseKey: Types.Key,
    Items.IceTrapSlowKey: Types.Key,
}


def getModelMask(item: Items) -> Types:
    """Get the model mask for an ice trap."""
    return IceTrapMasks.get(item, Types.Banana)


def getItemPreviewText(item_type: Types, location: Locations, allow_special_text: bool = True, masked_model: Types = None) -> str:
    """Get the preview text for an item."""
    if item_type == Types.FakeItem and (location != Locations.GalleonDonkeySealRace or not allow_special_text):
        masked_name = getItemDBEntry(masked_model).preview_text
        return getIceTrapText(masked_name)
    text = ""
    if item_type in item_db or item_type in FILLER_MAPPING:
        text = getItemDBEntry(item_type).preview_text
        if location == Locations.GalleonDonkeySealRace and allow_special_text:
            text = getItemDBEntry(item_type).seal_preview_text
    return text
