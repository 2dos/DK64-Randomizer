from random import random
from object_data.objects import ASMPatch

asm_options = [
    ASMPatch(asm_file="global", required=True, var_type="", form_var=""),
    ASMPatch(asm_file="startup_pointers", required=True, var_type="", form_var=""),
    ASMPatch(asm_file="quality_of_life", var_type="checkbox", form_var="quality_of_life"),
    ASMPatch(asm_file="fast_start", var_type="checkbox", form_var="fast_start_beginning_of_game"),
    ASMPatch(asm_file="castle_autowalk", var_type="", form_var=""),
    ASMPatch(asm_file="moves", var_type="checkbox", form_var="unlock_all_moves"),
    ASMPatch(asm_file="open_coin_door", var_type="checkbox", form_var="coin_door_open"),
    ASMPatch(asm_file="open_crown_door", var_type="checkbox", form_var="crown_door_open"),
    ASMPatch(asm_file="rando_level_order", var_type="checkbox", form_var="randomize_progression", replace=True),
    ASMPatch(asm_file="shorter_helm", var_type="checkbox", form_var="fast_start_hideout_helm"),
    ASMPatch(asm_file="tag_anywhere", var_type="checkbox", form_var="enable_tag_anywhere"),
    ASMPatch(asm_file="unlock_kongs", var_type="checkbox", form_var="unlock_all_kongs"),
]
