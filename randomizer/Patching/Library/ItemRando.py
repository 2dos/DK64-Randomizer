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
    Items.IceTrapDisableA,
    Items.IceTrapDisableB,
    Items.IceTrapDisableZ,
    Items.IceTrapDisableCU,
    Items.IceTrapDisableABean,
    Items.IceTrapDisableBBean,
    Items.IceTrapDisableZBean,
    Items.IceTrapDisableCUBean,
    Items.IceTrapDisableAKey,
    Items.IceTrapDisableBKey,
    Items.IceTrapDisableZKey,
    Items.IceTrapDisableCUKey,
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
    IceTrapDisableAGB = auto()
    IceTrapDisableBGB = auto()
    IceTrapDisableZGB = auto()
    IceTrapDisableCUGB = auto()
    IceTrapDisableABean = auto()
    IceTrapDisableBBean = auto()
    IceTrapDisableZBean = auto()
    IceTrapDisableCUBean = auto()
    IceTrapDisableAKey = auto()
    IceTrapDisableBKey = auto()
    IceTrapDisableZKey = auto()
    IceTrapDisableCUKey = auto()


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
    IceTrapDisableA = auto()
    IceTrapDisableB = auto()
    IceTrapDisableZ = auto()
    IceTrapDisableCU = auto()


class ArcadeRewards(IntEnum):
    """Enum of Arcade Rewards."""

    NintendoCoin = 0  # Or No Item
    Bean = auto()
    Blueprint = auto()
    Crown = auto()
    Fairy = auto()
    Banana = auto()
    Key = auto()
    Medal = auto()
    Pearl = auto()
    PotionDK = auto()
    PotionDiddy = auto()
    PotionLanky = auto()
    PotionTiny = auto()
    PotionChunky = auto()
    PotionAny = auto()
    Donkey = auto()
    Diddy = auto()
    Lanky = auto()
    Tiny = auto()
    Chunky = auto()
    RainbowCoin = auto()
    RarewareCoin = auto()
    JunkItem = auto()
    IceTrap = auto()
    Cranky = auto()
    Funky = auto()
    Candy = auto()
    Snide = auto()
    Hint = auto()
    BPDK = auto()
    BPDiddy = auto()
    BPLanky = auto()
    BPTiny = auto()
    BPChunky = auto()
    APItem = auto()


class JetpacRewards(IntEnum):
    """Enum of Jetpac Rewards."""

    RarewareCoin = 0  # Or NoItem
    Bean = auto()
    Blueprint = auto()
    Crown = auto()
    Fairy = auto()
    Banana = auto()
    Key = auto()
    Medal = auto()
    Pearl = auto()
    Potion = auto()
    Kong = auto()
    RainbowCoin = auto()
    NintendoCoin = auto()
    JunkItem = auto()
    IceTrap = auto()
    Cranky = auto()
    Funky = auto()
    Candy = auto()
    Snide = auto()
    Hint = auto()
    APItem = auto()


class BuyText(IntEnum):
    """Enum of items in the order of buy text."""

    blast = 0
    strong = auto()
    grab = auto()
    charge = auto()
    rocket = auto()
    spring = auto()
    ostand = auto()
    balloon = auto()
    sprint = auto()
    mini = auto()
    ptt = auto()
    port = auto()
    hunky = auto()
    punch = auto()
    gone = auto()
    slam = auto()
    coconut = auto()
    peanut = auto()
    grape = auto()
    feather = auto()
    pineapple = auto()
    homing = auto()
    sniper = auto()
    ammo_belt = auto()
    bongos = auto()
    guitar = auto()
    trombone = auto()
    sax = auto()
    triangle = auto()
    instrument_upgrade = auto()
    dive = auto()
    orange = auto()
    barrel = auto()
    vine = auto()
    climb = auto()
    camera = auto()
    shockwave = auto()
    camera_and_shockwave = auto()
    golden_banana = auto()
    crown = auto()
    medal = auto()
    key = auto()
    blueprint = auto()
    nin_coin = auto()
    rw_coin = auto()
    bean = auto()
    pearl = auto()
    kong = auto()
    fairy = auto()
    ice_trap = auto()
    hint = auto()
    terminator = auto()  # Used for nobuytext calculations


class NoBuyText(IntEnum):
    """Enum of items in the order of can't buy text."""

    special_move = 0
    slam = auto()
    gun = auto()
    gun_upgrade = auto()
    ammo_belt = auto()
    instrument = auto()
    training_move = auto()
    fairy_move = auto()
    misc_item = auto()
    golden_banana = auto()
    blueprint = auto()
    medal = auto()
    kong = auto()


class ItemPlacementData:
    """Class to store information pertaining to writing Item Rando data."""

    def __init__(
        self,
        model_index: list[int] = None,
        model_two_index: list[int] = None,
        actor_index: list[int] = None,
        arcade_reward_index: list[int] = None,
        jetpac_reward_index: list[int] = None,
        overlay: list[GraphicOverlay] = None,
        index_getter=None,
        preview_text: str = "",
        seal_preview_text: str = "",
        scale: float = 0.25,
    ):
        """Initialize with given parameters."""
        self.has_model = model_index is not None
        self.model_index = model_index
        self.model_two_index = model_two_index
        self.arcade_reward_index = arcade_reward_index
        self.jetpac_reward_index = jetpac_reward_index
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
        arcade_reward_index=[ArcadeRewards.Banana],
        jetpac_reward_index=[JetpacRewards.Banana],
        overlay=[GraphicOverlay.Banana],
        preview_text="\x04GOLDEN BANANA\x04",
        seal_preview_text="\x04BANANA OF PURE GOLD\x04",
    ),
    Types.Key: ItemPlacementData(
        model_index=[0xF5],
        model_two_index=[0x13C],
        actor_index=[72],
        arcade_reward_index=[ArcadeRewards.Key],
        jetpac_reward_index=[JetpacRewards.Key],
        overlay=[GraphicOverlay.Key],
        preview_text="\x04BOSS KEY\x04",
        seal_preview_text="\x04KEY TO DAVY JONES LOCKER\x04",
        scale=0.17,
    ),
    Types.Crown: ItemPlacementData(
        model_index=[0xF4],
        model_two_index=[0x18D],
        actor_index=[86],
        arcade_reward_index=[ArcadeRewards.Crown],
        jetpac_reward_index=[JetpacRewards.Crown],
        overlay=[GraphicOverlay.Crown],
        preview_text="\x04BATTLE CROWN\x04",
        seal_preview_text="\x04CROWN TO PLACE ATOP YER HEAD\x04",
    ),
    Types.Fairy: ItemPlacementData(
        model_index=[0x3D],
        model_two_index=[0x25C],
        actor_index=[CustomActors.Fairy],
        arcade_reward_index=[ArcadeRewards.Fairy],
        jetpac_reward_index=[JetpacRewards.Fairy],
        overlay=[GraphicOverlay.Fairy],
        preview_text="\x04BANANA FAIRY\x04",
        seal_preview_text="\x04MAGICAL FLYING PIXIE\x04",
    ),
    Types.Shop: ItemPlacementData(
        model_index=[0xF6, 0xF7, 0xF8, 0xF9, 0xFA, 0xFB],
        model_two_index=[0x5B, 0x1F2, 0x59, 0x1F3, 0x1F5, 0x1F6],
        arcade_reward_index=[
            ArcadeRewards.PotionDK,
            ArcadeRewards.PotionDiddy,
            ArcadeRewards.PotionLanky,
            ArcadeRewards.PotionTiny,
            ArcadeRewards.PotionChunky,
            ArcadeRewards.PotionAny,
        ],
        actor_index=[
            CustomActors.PotionDK,
            CustomActors.PotionDiddy,
            CustomActors.PotionLanky,
            CustomActors.PotionTiny,
            CustomActors.PotionChunky,
            CustomActors.PotionAny,
        ],
        jetpac_reward_index=[JetpacRewards.Potion] * 6,
        overlay=[GraphicOverlay.CrankyPotion] * 6,  # Handled elsewhere
        index_getter=lambda item, flag, shared: (flag >> 12) & 7 if flag & 0x8000 and not shared and ((flag >> 12) & 7) < 5 else 5,
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.Shockwave: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
        overlay=[GraphicOverlay.Shockwave],
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.TrainingBarrel: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
        overlay=[GraphicOverlay.TrainingBarrel],
        preview_text="\x04POTION\x04",
        seal_preview_text="\x04BOTTLE OF GROG\x04",
    ),
    Types.Climbing: ItemPlacementData(
        model_index=[0xFB],
        model_two_index=[0x1F6],
        actor_index=[CustomActors.PotionAny],
        arcade_reward_index=[ArcadeRewards.PotionAny],
        jetpac_reward_index=[JetpacRewards.Potion],
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
        arcade_reward_index=[
            ArcadeRewards.Donkey,
            ArcadeRewards.Diddy,
            ArcadeRewards.Lanky,
            ArcadeRewards.Tiny,
            ArcadeRewards.Chunky,
        ],
        jetpac_reward_index=[JetpacRewards.Kong] * 5,
        overlay=[GraphicOverlay.Kong],
        index_getter=lambda item, flag, shared: (385, 6, 70, 66, 117).index(flag),
        preview_text="\x04KONG\x04",
        seal_preview_text="\x04WEIRD MONKEY\x04",
    ),
    Types.FakeItem: ItemPlacementData(
        model_index=[0x103, 0x103, 0x103, 0x127, 0x127, 0x127, 0x128, 0x128, 0x128, 0x103, 0x103, 0x103, 0x103, 0x127, 0x127, 0x127, 0x127, 0x128, 0x128, 0x128, 0x128],
        model_two_index=[0x25D, 0x264, 0x265, 0x292, 0x293, 0x294, 0x295, 0x296, 0x297, 0x2A6, 0x299, 0x29A, 0x29B, 0x29C, 0x29D, 0x29E, 0x29F, 0x2A0, 0x2A1, 0x2A4, 0x2A5],
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
            CustomActors.IceTrapDisableAGB,
            CustomActors.IceTrapDisableBGB,
            CustomActors.IceTrapDisableZGB,
            CustomActors.IceTrapDisableCUGB,
            CustomActors.IceTrapDisableABean,
            CustomActors.IceTrapDisableBBean,
            CustomActors.IceTrapDisableZBean,
            CustomActors.IceTrapDisableCUBean,
            CustomActors.IceTrapDisableAKey,
            CustomActors.IceTrapDisableBKey,
            CustomActors.IceTrapDisableZKey,
            CustomActors.IceTrapDisableCUKey,
        ],
        arcade_reward_index=[ArcadeRewards.IceTrap] * (3 * 7),
        jetpac_reward_index=[JetpacRewards.IceTrap] * (3 * 7),
        overlay=[
            GraphicOverlay.IceTrapBubble,
            GraphicOverlay.IceTrapReverse,
            GraphicOverlay.IceTrapSlow,
            GraphicOverlay.IceTrapBubble,
            GraphicOverlay.IceTrapReverse,
            GraphicOverlay.IceTrapSlow,
            GraphicOverlay.IceTrapBubble,
            GraphicOverlay.IceTrapReverse,
            GraphicOverlay.IceTrapSlow,
            GraphicOverlay.IceTrapDisableA,
            GraphicOverlay.IceTrapDisableB,
            GraphicOverlay.IceTrapDisableZ,
            GraphicOverlay.IceTrapDisableCU,
            GraphicOverlay.IceTrapDisableA,
            GraphicOverlay.IceTrapDisableB,
            GraphicOverlay.IceTrapDisableZ,
            GraphicOverlay.IceTrapDisableCU,
            GraphicOverlay.IceTrapDisableA,
            GraphicOverlay.IceTrapDisableB,
            GraphicOverlay.IceTrapDisableZ,
            GraphicOverlay.IceTrapDisableCU,
        ],
        index_getter=lambda item, flag, shared: IceTrapItems.index(item),
        preview_text="\x04GLODEN BANANE\x04",
        seal_preview_text="\x04BANANA OF FOOLS GOLD\x04",
    ),
    Types.Bean: ItemPlacementData(
        model_index=[0x104],
        model_two_index=[0x198],
        actor_index=[CustomActors.Bean],
        arcade_reward_index=[ArcadeRewards.Bean],
        jetpac_reward_index=[JetpacRewards.Bean],
        overlay=[GraphicOverlay.Bean],
        preview_text="\x04BEAN\x04",
        seal_preview_text="\x04QUESTIONABLE VEGETABLE\x04",
    ),
    Types.Pearl: ItemPlacementData(
        model_index=[0x106],
        model_two_index=[0x1B4],
        actor_index=[CustomActors.Pearl],
        arcade_reward_index=[ArcadeRewards.Pearl],
        jetpac_reward_index=[JetpacRewards.Pearl],
        overlay=[GraphicOverlay.Pearl],
        preview_text="\x04PEARL\x04",
        seal_preview_text="\x04BLACK PEARL\x04",
    ),
    Types.Medal: ItemPlacementData(
        model_index=[0x108],
        model_two_index=[0x90],
        actor_index=[CustomActors.Medal],
        arcade_reward_index=[ArcadeRewards.Medal],
        jetpac_reward_index=[JetpacRewards.Medal],
        overlay=[GraphicOverlay.Medal],
        preview_text="\x04BANANA MEDAL\x04",
        seal_preview_text="\x04MEDALLION\x04",
        scale=0.22,
    ),
    Types.NintendoCoin: ItemPlacementData(
        model_index=[0x10A],
        model_two_index=[0x48],
        actor_index=[CustomActors.NintendoCoin],
        arcade_reward_index=[ArcadeRewards.NintendoCoin],
        jetpac_reward_index=[JetpacRewards.NintendoCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="\x04NINTENDO COIN\x04",
        seal_preview_text="\x04ANCIENT DOUBLOON\x04",
        scale=0.4,
    ),
    Types.RarewareCoin: ItemPlacementData(
        model_index=[0x10C],
        model_two_index=[0x28F],
        actor_index=[CustomActors.RarewareCoin],
        arcade_reward_index=[ArcadeRewards.RarewareCoin],
        jetpac_reward_index=[JetpacRewards.RarewareCoin],
        overlay=[GraphicOverlay.CompanyCoin],
        preview_text="\x04RAREWARE COIN\x04",
        seal_preview_text="\x04DOUBLOON OF THE RAREST KIND\x04",
        scale=0.4,
    ),
    Types.JunkItem: ItemPlacementData(
        model_index=[0x10E],
        model_two_index=[0x25E],
        actor_index=[0x2F],
        arcade_reward_index=[ArcadeRewards.JunkItem],
        jetpac_reward_index=[JetpacRewards.JunkItem],
        overlay=[GraphicOverlay.JunkMelon],
        preview_text="\x04JUNK ITEM\x04",
        seal_preview_text="\x04HEAP OF JUNK\x04",
    ),
    Types.Cranky: ItemPlacementData(
        model_index=[0x11],
        model_two_index=[0x25F],
        actor_index=[CustomActors.CrankyItem],
        arcade_reward_index=[ArcadeRewards.Cranky],
        jetpac_reward_index=[JetpacRewards.Cranky],
        overlay=[GraphicOverlay.CrankyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Funky: ItemPlacementData(
        model_index=[0x12],
        model_two_index=[0x260],
        actor_index=[CustomActors.FunkyItem],
        arcade_reward_index=[ArcadeRewards.Funky],
        jetpac_reward_index=[JetpacRewards.Funky],
        overlay=[GraphicOverlay.FunkyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Candy: ItemPlacementData(
        model_index=[0x13],
        model_two_index=[0x261],
        actor_index=[CustomActors.CandyItem],
        arcade_reward_index=[ArcadeRewards.Candy],
        jetpac_reward_index=[JetpacRewards.Candy],
        overlay=[GraphicOverlay.CandyItem],
        preview_text="\x04SHOPKEEPER\x04",
        seal_preview_text="\x04BARTERING SOUL\x04",
    ),
    Types.Snide: ItemPlacementData(
        model_index=[0x1F],
        model_two_index=[0x262],
        actor_index=[CustomActors.SnideItem],
        arcade_reward_index=[ArcadeRewards.Snide],
        jetpac_reward_index=[JetpacRewards.Snide],
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
        arcade_reward_index=[ArcadeRewards.Hint] * 5,
        jetpac_reward_index=[JetpacRewards.Hint] * 5,
        overlay=[GraphicOverlay.Hint],
        index_getter=lambda item, flag, shared: (flag - 0x384) % 5,
        preview_text="\x04HINT\x04",
        seal_preview_text="\x04LAYTON RIDDLE\x04",
    ),
    Types.Blueprint: ItemPlacementData(
        model_two_index=[0xDE, 0xE0, 0xE1, 0xDD, 0xDF],
        actor_index=[78, 75, 77, 79, 76],
        overlay=[GraphicOverlay.Blueprint],
        arcade_reward_index=[
            ArcadeRewards.BPDK,
            ArcadeRewards.BPDiddy,
            ArcadeRewards.BPLanky,
            ArcadeRewards.BPTiny,
            ArcadeRewards.BPChunky,
        ],
        jetpac_reward_index=[JetpacRewards.Blueprint] * 5,
        index_getter=lambda item, flag, shared: (flag - 0x1D5) % 5,
        preview_text="\x04BLUEPRINT\x04",
        seal_preview_text="\x04MAP O' DEATH MACHINE\x04",
        scale=2,
    ),
    Types.RainbowCoin: ItemPlacementData(
        model_two_index=[0xB7],
        actor_index=[0x8C],
        arcade_reward_index=[ArcadeRewards.RainbowCoin],
        jetpac_reward_index=[JetpacRewards.RainbowCoin],
        overlay=[GraphicOverlay.RainbowCoin],
        preview_text="\x04RAINBOW COIN\x04",
        seal_preview_text="\x04COLORFUL COIN HIDDEN FOR 17 YEARS\x04",
    ),
    Types.NoItem: ItemPlacementData(
        model_two_index=[0],
        actor_index=[CustomActors.Null],
        arcade_reward_index=[ArcadeRewards.NintendoCoin],
        jetpac_reward_index=[JetpacRewards.RarewareCoin],
        overlay=[GraphicOverlay.NoItem],
        preview_text="\x04NOTHING\x04",
        seal_preview_text="\x04DIDDLY SQUAT\x04",
    ),
    Types.ArchipelagoItem: ItemPlacementData(
        model_index=[0x125],
        model_two_index=[0x291],
        actor_index=[CustomActors.ArchipelagoItem],
        arcade_reward_index=[ArcadeRewards.APItem],
        jetpac_reward_index=[JetpacRewards.APItem],
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
    if type is None:
        return item_db[Types.NoItem]
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


def getModelFromItem(item: Items, item_type: Types, flag: int, shared: bool = False) -> int:
    """Get the model index associated with an item."""
    if item_type not in item_db and item_type not in FILLER_MAPPING:
        return None
    item_db_entry = getItemDBEntry(item_type)
    if not item_db_entry.has_model:
        return None
    index = item_db_entry.index_getter(item, flag, shared)
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
    Items.IceTrapDisableA: Types.Banana,
    Items.IceTrapDisableABean: Types.Bean,
    Items.IceTrapDisableAKey: Types.Key,
    Items.IceTrapDisableB: Types.Banana,
    Items.IceTrapDisableBBean: Types.Bean,
    Items.IceTrapDisableBKey: Types.Key,
    Items.IceTrapDisableZ: Types.Banana,
    Items.IceTrapDisableZBean: Types.Bean,
    Items.IceTrapDisableZKey: Types.Key,
    Items.IceTrapDisableCU: Types.Banana,
    Items.IceTrapDisableCUBean: Types.Bean,
    Items.IceTrapDisableCUKey: Types.Key,
}


def getModelMask(item: Items) -> Types:
    """Get the model mask for an ice trap."""
    return IceTrapMasks.get(item, Types.Banana)


def getItemPreviewText(item_type: Types, location: Locations, allow_special_text: bool = True, masked_model: Types = None) -> str:
    """Get the preview text for an item."""
    use_special_text = location == Locations.GalleonDonkeySealRace and allow_special_text
    reference_item = item_type
    if item_type == Types.FakeItem:
        reference_item = masked_model
    if reference_item not in item_db and reference_item not in FILLER_MAPPING:
        return ""
    item_data = getItemDBEntry(reference_item)
    text = item_data.preview_text
    if use_special_text:
        text = item_data.seal_preview_text
    if item_type == Types.FakeItem:
        return getIceTrapText(text)
    return text


item_shop_text_mapping = {
    # Kongs
    Items.Donkey: (BuyText.kong, NoBuyText.kong),
    Items.Diddy: (BuyText.kong, NoBuyText.kong),
    Items.Lanky: (BuyText.kong, NoBuyText.kong),
    Items.Tiny: (BuyText.kong, NoBuyText.kong),
    Items.Chunky: (BuyText.kong, NoBuyText.kong),
    Items.Cranky: (BuyText.kong, NoBuyText.kong),
    Items.Funky: (BuyText.kong, NoBuyText.kong),
    Items.Candy: (BuyText.kong, NoBuyText.kong),
    Items.Snide: (BuyText.kong, NoBuyText.kong),
    # Training
    Items.Vines: (BuyText.vine, NoBuyText.training_move),
    Items.Swim: (BuyText.dive, NoBuyText.training_move),
    Items.Oranges: (BuyText.orange, NoBuyText.training_move),
    Items.Barrels: (BuyText.barrel, NoBuyText.training_move),
    Items.Climbing: (BuyText.climb, NoBuyText.training_move),
    # Slams
    Items.ProgressiveSlam: (BuyText.slam, NoBuyText.slam),
    Items.ProgressiveSlam2: (BuyText.slam, NoBuyText.slam),
    Items.ProgressiveSlam3: (BuyText.slam, NoBuyText.slam),
    # Special Moves
    Items.BaboonBlast: (BuyText.blast, NoBuyText.special_move),
    Items.StrongKong: (BuyText.strong, NoBuyText.special_move),
    Items.GorillaGrab: (BuyText.grab, NoBuyText.special_move),
    Items.ChimpyCharge: (BuyText.charge, NoBuyText.special_move),
    Items.RocketbarrelBoost: (BuyText.rocket, NoBuyText.special_move),
    Items.SimianSpring: (BuyText.spring, NoBuyText.special_move),
    Items.Orangstand: (BuyText.ostand, NoBuyText.special_move),
    Items.BaboonBalloon: (BuyText.balloon, NoBuyText.special_move),
    Items.OrangstandSprint: (BuyText.sprint, NoBuyText.special_move),
    Items.MiniMonkey: (BuyText.mini, NoBuyText.special_move),
    Items.PonyTailTwirl: (BuyText.ptt, NoBuyText.special_move),
    Items.Monkeyport: (BuyText.port, NoBuyText.special_move),
    Items.HunkyChunky: (BuyText.hunky, NoBuyText.special_move),
    Items.PrimatePunch: (BuyText.punch, NoBuyText.special_move),
    Items.GorillaGone: (BuyText.gone, NoBuyText.special_move),
    # Guns
    Items.Coconut: (BuyText.coconut, NoBuyText.gun),
    Items.Peanut: (BuyText.peanut, NoBuyText.gun),
    Items.Grape: (BuyText.grape, NoBuyText.gun),
    Items.Feather: (BuyText.feather, NoBuyText.gun),
    Items.Pineapple: (BuyText.pineapple, NoBuyText.gun),
    # Gun Upgrades
    Items.HomingAmmo: (BuyText.homing, NoBuyText.gun_upgrade),
    Items.SniperSight: (BuyText.sniper, NoBuyText.gun_upgrade),
    Items.ProgressiveAmmoBelt: (BuyText.ammo_belt, NoBuyText.ammo_belt),
    Items.ProgressiveAmmoBelt2: (BuyText.ammo_belt, NoBuyText.ammo_belt),
    # Instruments
    Items.Bongos: (BuyText.bongos, NoBuyText.instrument),
    Items.Guitar: (BuyText.guitar, NoBuyText.instrument),
    Items.Trombone: (BuyText.trombone, NoBuyText.instrument),
    Items.Saxophone: (BuyText.sax, NoBuyText.instrument),
    Items.Triangle: (BuyText.triangle, NoBuyText.instrument),
    # Instrument Upgrades
    Items.ProgressiveInstrumentUpgrade: (BuyText.instrument_upgrade, NoBuyText.instrument),
    Items.ProgressiveInstrumentUpgrade2: (BuyText.instrument_upgrade, NoBuyText.instrument),
    Items.ProgressiveInstrumentUpgrade3: (BuyText.instrument_upgrade, NoBuyText.instrument),
    # Fairy Moves
    Items.Camera: (BuyText.camera, NoBuyText.fairy_move),
    Items.Shockwave: (BuyText.shockwave, NoBuyText.fairy_move),
    Items.CameraAndShockwave: (BuyText.camera_and_shockwave, NoBuyText.fairy_move),
    # Company Coins
    Items.NintendoCoin: (BuyText.nin_coin, NoBuyText.misc_item),
    Items.RarewareCoin: (BuyText.rw_coin, NoBuyText.misc_item),
    # Boss Keys
    Items.JungleJapesKey: (BuyText.key, NoBuyText.misc_item),
    Items.AngryAztecKey: (BuyText.key, NoBuyText.misc_item),
    Items.FranticFactoryKey: (BuyText.key, NoBuyText.misc_item),
    Items.GloomyGalleonKey: (BuyText.key, NoBuyText.misc_item),
    Items.FungiForestKey: (BuyText.key, NoBuyText.misc_item),
    Items.CrystalCavesKey: (BuyText.key, NoBuyText.misc_item),
    Items.CreepyCastleKey: (BuyText.key, NoBuyText.misc_item),
    Items.HideoutHelmKey: (BuyText.key, NoBuyText.misc_item),
    # Misc Items
    Items.GoldenBanana: (BuyText.golden_banana, NoBuyText.golden_banana),
    Items.BananaFairy: (BuyText.fairy, NoBuyText.misc_item),
    Items.BananaMedal: (BuyText.medal, NoBuyText.medal),
    Items.BattleCrown: (BuyText.crown, NoBuyText.misc_item),
    Items.Bean: (BuyText.bean, NoBuyText.misc_item),
    Items.Pearl: (BuyText.pearl, NoBuyText.misc_item),
    Items.FillerPearl: (BuyText.pearl, NoBuyText.misc_item),
    Items.FillerBanana: (BuyText.golden_banana, NoBuyText.golden_banana),
    Items.FillerFairy: (BuyText.fairy, NoBuyText.misc_item),
    Items.FillerCrown: (BuyText.crown, NoBuyText.misc_item),
    Items.FillerMedal: (BuyText.medal, NoBuyText.medal),
    # Ice Traps
    Items.IceTrapBubble: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverse: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlow: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapBubbleBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverseBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlowBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapBubbleKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapReverseKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapSlowKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableA: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableABean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableAKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableB: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableBBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableBKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZ: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableZKey: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCU: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCUBean: (BuyText.ice_trap, NoBuyText.misc_item),
    Items.IceTrapDisableCUKey: (BuyText.ice_trap, NoBuyText.misc_item),
    # Items not yet considered
    # Items.RainbowCoin: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkCrystal: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkMelon: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkAmmo: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkFilm: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.JunkOrange: (BuyText.blueprint, NoBuyText.misc_item),
    # Items.ArchipelagoItem: (BuyText.blueprint, NoBuyText.misc_item),
    # Hints
    Items.JapesDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.JapesChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.AztecChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.FactoryChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.GalleonChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.ForestChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CavesChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleDonkeyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleDiddyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleLankyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleTinyHint: (BuyText.hint, NoBuyText.misc_item),
    Items.CastleChunkyHint: (BuyText.hint, NoBuyText.misc_item),
    # Blueprint
    Items.JungleJapesDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.JungleJapesDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.JungleJapesLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.JungleJapesTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.JungleJapesChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.AngryAztecDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.AngryAztecDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.AngryAztecLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.AngryAztecTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.AngryAztecChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FranticFactoryDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FranticFactoryDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FranticFactoryLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FranticFactoryTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FranticFactoryChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.GloomyGalleonDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.GloomyGalleonDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.GloomyGalleonLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.GloomyGalleonTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.GloomyGalleonChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FungiForestDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FungiForestDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FungiForestLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FungiForestTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.FungiForestChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CrystalCavesDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CrystalCavesDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CrystalCavesLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CrystalCavesTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CrystalCavesChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CreepyCastleDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CreepyCastleDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CreepyCastleLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CreepyCastleTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.CreepyCastleChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DKIslesDonkeyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DKIslesDiddyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DKIslesLankyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DKIslesTinyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
    Items.DKIslesChunkyBlueprint: (BuyText.blueprint, NoBuyText.blueprint),
}
