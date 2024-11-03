"""Import functions within the UI folder to have them run on load of the UI."""

import ui.plando_settings
import js
from ui.rando_options import (
    set_preset_options,
    set_random_weights_options,
)

js.check_seed_info_tab()

# Update Rando Options
set_random_weights_options()
set_preset_options()
