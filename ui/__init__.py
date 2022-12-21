"""Import functions within the UI folder to have them run on load of the UI."""
from ui.generate_buttons import update_seed_text
from ui.rando_options import (
    disable_barrel_modal,
    disable_enemy_modal,
    disable_items_modal,
    disable_boss_rando,
    disable_colors,
    disable_music,
    disable_move_shuffles,
    hide_rgb,
    max_randomized_blocker,
    max_randomized_medals,
    max_randomized_medal_cb_req,
    max_randomized_fairies,
    max_doorone_requirement,
    max_doortwo_requirement,
    updateDoorOneNumAccess,
    updateDoorTwoNumAccess,
    max_randomized_troff,
    set_preset_options,
    toggle_b_locker_boxes,
    toggle_counts_boxes,
    toggle_medals_box,
    update_boss_required,
    disable_coupled_camera_shockwave,
    toggle_key_settings,
)

# Call the generate_buttons function just to force loading of the file
update_seed_text(None)

# Update Rando Options
set_preset_options()
toggle_counts_boxes(None)
toggle_b_locker_boxes(None)
update_boss_required(None)
disable_colors(None)
disable_music(None)
disable_move_shuffles(None)
max_randomized_blocker(None)
max_randomized_troff(None)
disable_barrel_modal(None)
disable_enemy_modal(None)
disable_items_modal(None)
disable_boss_rando(None)
hide_rgb(None)
toggle_medals_box(None)
max_randomized_medals(None)
max_randomized_medal_cb_req(None)
max_randomized_fairies(None)
max_doorone_requirement(None)
max_doortwo_requirement(None)
updateDoorOneNumAccess(None)
updateDoorTwoNumAccess(None)
disable_coupled_camera_shockwave(None)
toggle_key_settings(None)
