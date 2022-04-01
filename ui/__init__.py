"""Import functions within the UI folder to have them run on load of the UI."""
from ui.generate_buttons import disable_input, toggle_counts_boxes
from ui.rando_options import (
    update_disabled_progression,
    toggle_loading_zone_coupling,
    set_preset_options,
    preset_select_changed,
)

disable_input(None)
update_disabled_progression(None)
toggle_loading_zone_coupling(None)
set_preset_options()
preset_select_changed(None)
toggle_counts_boxes(None)
