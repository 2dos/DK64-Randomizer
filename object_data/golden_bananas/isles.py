"""Golden Banana Data."""
from object_data.objects import GoldenBanana

isles_gbs = [
    GoldenBanana("dk_japes_rock", dk_pickup=True),
    GoldenBanana("dk_lava_banana", dk_cranky=2, chunky_cranky=2, dk_pickup=True, chunky_pickup=True, lobby6=True),
    GoldenBanana("dk_caged_banana", dk_gun=True, dk_pickup=True, key2=True),
    GoldenBanana("dk_instrument_pad", dk_cranky=3, dk_pickup=True, dk_instrument=True, lobby3=True),
    GoldenBanana("dk_blueprint", dk_gun=True, sniper=True, dk_pickup=True, lobby8=True),
    GoldenBanana(
        "diddy_snides_lobby", vine=True, diddy_cranky=3, tiny_cranky=3, diddy_pickup=True, tiny_pickup=True, key2=True
    ),
    GoldenBanana(
        "diddy_summit",
        barrel=True,
        vine=True,
        diddy_cranky=2,
        diddy_pickup=True,
        lanky_pickup=True,
        chunky_pickup=True,
        lanky_instrument=True,
        key4=True,
    ),
    GoldenBanana("diddy_caged_banana", diddy_cranky=2, diddy_gun=True, diddy_pickup=True, key4=True),
    GoldenBanana("diddy_instrument_pad", diddy_cranky=2, diddy_pickup=True, diddy_instrument=True, lobby6=True),
    GoldenBanana("diddy_blueprint", dk_gun=True, dk_pickup=True, diddy_pickup=True, lobby7=True),
    GoldenBanana("lanky_orangsprint", lanky_cranky=3, lanky_pickup=True),
    GoldenBanana("lanky_castle_lobby", barrel=True, lanky_cranky=2, lanky_pickup=True, chunky_pickup=True, lobby7=True),
    GoldenBanana("lanky_caged_banana", lanky_gun=True, lanky_pickup=True),
    GoldenBanana(
        "lanky_instrument_pad", barrel=True, lanky_pickup=True, chunky_pickup=True, lanky_instrument=True, lobby1=True
    ),
    GoldenBanana("lanky_blueprint", chunky_cranky=2, lanky_pickup=True, chunky_pickup=True, lobby6=True),
    GoldenBanana("tiny_big_bug_bash", diddy_cranky=1, tiny_cranky=2, diddy_pickup=True, tiny_pickup=True, lobby2=True),
    GoldenBanana("tiny_galleon_lobby", slam=2, tiny_cranky=1, tiny_pickup=True, chunky_pickup=True, lobby4=True),
    GoldenBanana("tiny_caged_banana", tiny_gun=True, tiny_pickup=True),
    GoldenBanana("tiny_instrument_pad", tiny_cranky=3, tiny_pickup=True, tiny_instrument=True),
    GoldenBanana("tiny_blueprint", chunky_cranky=2, tiny_pickup=True, chunky_pickup=True, lobby3=True),
    GoldenBanana(
        "chunky_pound_the_x", tiny_cranky=3, chunky_cranky=1, tiny_pickup=True, chunky_pickup=True, tiny_instrument=True
    ),
    GoldenBanana("chunky_kremling_kosh", vine=True, chunky_cranky=3, chunky_pickup=True, lobby8=True),
    GoldenBanana("chunky_caged_banana", chunky_gun=True, chunky_pickup=True),
    GoldenBanana("chunky_instrument_pad", vine=True, chunky_pickup=True, chunky_instrument=True),
    GoldenBanana("chunky_blueprint", chunky_pickup=True, lobby4=True),
]
