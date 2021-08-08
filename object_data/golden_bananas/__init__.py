"""Gen all golden bananas into a single dict."""
import object_data.golden_bananas.aztec as aztec
import object_data.golden_bananas.castle as castle
import object_data.golden_bananas.caves as caves
import object_data.golden_bananas.factory as factory
import object_data.golden_bananas.fungi as fungi
import object_data.golden_bananas.galleon as galleon
import object_data.golden_bananas.isles as isles
import object_data.golden_bananas.japes as japes

golden_bananas = {
    "aztec": aztec.aztec_gbs,
    "castle": castle.castle_gbs,
    "caves": caves.caves_gbs,
    "factory": factory.factory_gbs,
    "fungi": fungi.fungi_gbs,
    "galleon": galleon.galleon_gbs,
    "isles": isles.isles_gbs,
    "japes": japes.japes_gbs,
}
