"""Import functions within the UI folder to have them run on load of the UI."""
from ui.generate_buttons import disable_input
from ui.rando_options import set_preset_options, toggle_b_locker_boxes, toggle_counts_boxes, update_boss_required, disable_colors, disable_music

disable_input(None)
set_preset_options()
toggle_counts_boxes(None)
toggle_b_locker_boxes(None)
update_boss_required(None)
disable_colors(None)
disable_music(None)
