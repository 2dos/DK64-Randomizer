from object_data.randomizer_options import set_blockers, set_keys, set_troff_n_scoff, shuffle_progression
from object_data.objects import ASMPatch

asm_options = [
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="randomize_progression",
        function=shuffle_progression.shuffle_progression,
    ),
    ASMPatch(
        asm_file="null", var_type="checkbox", form_var="randomize_progression", function=set_blockers.set_blockers
    ),
    ASMPatch(asm_file="null", var_type="checkbox", form_var="randomize_progression", function=set_keys.set_keys),
    ASMPatch(
        asm_file="null", var_type="checkbox", form_var="randomize_progression", function=set_troff_n_scoff.set_troff
    ),
    ASMPatch(
        asm_file="qol/quality_of_life",
        var_type="checkbox",
        form_var="quality_of_life",
        asm_start=["QOLChangesShorten", "QOLChanges"],
    ),
    ASMPatch(
        asm_file="qol/fast_start",
        var_type="checkbox",
        form_var="fast_start_beginning_of_game",
        asm_start=["IslesSpawn", "ApplyFastStart"],
    ),
    ASMPatch(asm_file="castle_autowalk", var_type="", form_var="", asm_start=["FixCastleAutowalk"]),
    ASMPatch(asm_file="moves", var_type="checkbox", form_var="unlock_all_moves", asm_start=["GiveMoves"]),
    ASMPatch(asm_file="open_coin_door", var_type="checkbox", form_var="coin_door_open", asm_start=["OpenCoinDoor"]),
    ASMPatch(asm_file="open_crown_door", var_type="checkbox", form_var="crown_door_open", asm_start=["OpenCrownDoor"]),
    ASMPatch(
        asm_file="rando_level_order",
        var_type="checkbox",
        form_var="randomize_progression",
        replace=True,
        asm_start=["RandoLevelOrder", "SwapRequirements"],
    ),
    ASMPatch(
        asm_file="shorter_helm", var_type="checkbox", form_var="fast_start_hideout_helm", asm_start=["ChangeLZToHelm"]
    ),
    ASMPatch(asm_file="tag_anywhere", var_type="checkbox", form_var="enable_tag_anywhere", asm_start=["TagAnywhere"]),
    ASMPatch(asm_file="unlock_kongs", var_type="checkbox", form_var="unlock_all_kongs", asm_start=["UnlockKongs"]),
]
