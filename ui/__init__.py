"""Import functions within the UI folder to have them run on load of the UI."""
from ui.rando_options import set_blocker_preset, set_troff_preset, randomseed, update_disabled_progression
from ui.generate_buttons import disable_input

set_blocker_preset(None)
set_troff_preset(None)
disable_input(None)
randomseed(None)
update_disabled_progression(None)
