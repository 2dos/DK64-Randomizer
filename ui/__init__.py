"""Import functions within the UI folder to have them run on load of the UI."""
from ui.generate_buttons import disable_input
from ui.rando_options import set_preset_options, preset_select_changed, toggle_b_locker_boxes, toggle_counts_boxes, update_disabled_progression

disable_input(None)
set_preset_options()
preset_select_changed(None)
toggle_counts_boxes(None)
toggle_b_locker_boxes(None)
update_disabled_progression(None)