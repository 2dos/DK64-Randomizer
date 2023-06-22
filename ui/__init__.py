"""Import functions within the UI folder to have them run on load of the UI."""
from ui.generate_buttons import update_seed_text
from ui.rando_options import (
    disable_barrel_modal,
    disable_boss_rando,
    disable_colors,
    disable_enemy_modal,
    disable_helm_hurry,
    disable_move_shuffles,
    disable_music,
    hide_rgb,
    item_rando_list_changed,
    max_doorone_requirement,
    max_doortwo_requirement,
    max_music,
    max_randomized_blocker,
    max_randomized_fairies,
    max_randomized_medal_cb_req,
    max_randomized_medals,
    max_randomized_troff,
    max_sfx,
    max_starting_moves_count,
    set_preset_options,
    toggle_b_locker_boxes,
    toggle_counts_boxes,
    toggle_item_rando,
    toggle_key_settings,
    toggle_medals_box,
    toggle_vanilla_door_rando,
    update_boss_required,
    updateDoorOneNumAccess,
    updateDoorTwoNumAccess,
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
max_music(None)
max_sfx(None)
disable_barrel_modal(None)
disable_enemy_modal(None)
toggle_item_rando(None)
disable_boss_rando(None)
hide_rgb(None)
toggle_medals_box(None)
max_randomized_medals(None)
max_randomized_medal_cb_req(None)
max_randomized_fairies(None)
max_starting_moves_count(None)
max_doorone_requirement(None)
max_doortwo_requirement(None)
updateDoorOneNumAccess(None)
updateDoorTwoNumAccess(None)
item_rando_list_changed(None)
toggle_key_settings(None)
disable_helm_hurry(None)
toggle_vanilla_door_rando(None)
