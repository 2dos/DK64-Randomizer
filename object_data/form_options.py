from object_data.randomizer_options import (
    set_blockers,
    set_keys,
    set_troff_n_scoff,
    shuffle_progression,
    fairy_shockwave
)
from object_data.objects import ASMPatch

asm_options = [
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="generate_spoilerlog",
        tab="misc",
        title="""This option enables spoiler log files to be created on randomizer generation.""",
        content="Generate Spoiler Log",
        checked=True,
    ),
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="randomize_progression",
        function=shuffle_progression.shuffle_progression,
    ),
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="randomize_progression",
        function=set_blockers.set_blockers,
    ),
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="randomize_progression",
        function=set_keys.set_keys,
    ),
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="randomize_progression",
        function=set_troff_n_scoff.set_troff,
    ),
    ASMPatch(
        asm_file="unlock_kongs",
        var_type="checkbox",
        form_var="unlock_all_kongs",
        asm_start=[{"UnlockKongs": "before"}],
        tab="misc",
        title="""This option will make all 5 kongs available from the start without freeing them.
            The golden bananas awarded when freeing specific kongs still must be collected even with this option on.
            If using Level Progression Randomizer and playing through glitchless, this option is forced on.""",
        content="Unlock All Kongs",
        checked=True,
        disabled=True,
    ),
    ASMPatch(
        asm_file="moves",
        var_type="checkbox",
        form_var="unlock_all_moves",
        asm_start=[{"GiveMoves": "after"}],
        tab="misc",
        title="""This option will make all moves available from the start without purchasing them.
            Includes all Cranky, all Candy, and almost all Funky purchasables.
            Does not include access to JetPac in Cranky; you will still need 15 banana medals.
            Does not include snipe scope to reduce 1st person camera lag. Is still purchasable.
            Does not include the shockwave attack from the banana fairy queen.""",
        content="Unlock All Purchasable Moves",
    ),
    ASMPatch(
        asm_file="null",
        var_type="checkbox",
        form_var="unlock_fairy_shockwave",
        tab="misc",
        title="""This option makes the fairy camera and shockwave attack available from the start.
            Normally obtainable by visiting the Banana Fairy Queen with Tiny as Mini Monkey.""",
        content="Fairy Camera and Shockwave Attack",
        function=fairy_shockwave.set_fairy_rewards,
        always_run_function=True,
    ),
    ASMPatch(
        asm_file="tag_anywhere",
        var_type="checkbox",
        form_var="enable_tag_anywhere",
        asm_start=[{"TagAnywhere": "before"}],
        tab="misc",
        title="""This option will allow you to switch kongs almost anywhere using DPad left or DPad right.
            You will still need to unlock the kong you want if Unlock All Kongs isn't enabled.
            You cannot switch kongs in rooms or areas that would otherwise break the puzzle.""",
        content="Enable Tag Anywhere",
    ),
    ASMPatch(
        asm_file="qol/fast_start",
        var_type="checkbox",
        form_var="fast_start_beginning_of_game",
        asm_start=[{"IslesSpawn": "before"}, {"ApplyFastStart": "after"}],
        tab="misc",
        title="""Training Barrels complete, start with Simian Slam, spawn in DK Isles, Japes lobby entrance open.""",
        content="Fast Start - Beginning of Game",
        checked=True,
    ),
    ASMPatch(
        asm_file="shorter_helm",
        var_type="checkbox",
        form_var="fast_start_hideout_helm",
        asm_start=[{"ChangeLZToHelm": "before"}],
        tab="misc",
        title="""This option will shorten the time it takes to beat Hideout Helm with the following changes:
            - You will spawn in the Blast o Matic room.
            - Opens the roman numeral doors to each Kong's room.
            - The gates in front of the music pads are gone.""",
        content="Fast Start - Hideout Helm",
        checked=True,
    ),
    ASMPatch(
        asm_file="castle_autowalk",
        var_type="",
        form_var="",
        asm_start=[{"FixCastleAutowalk": "before"}],
    ),
    ASMPatch(
        asm_file="open_crown_door",
        var_type="checkbox",
        form_var="crown_door_open",
        asm_start=[{"OpenCrownDoor": "after"}],
        tab="misc",
        title="""You do not need to collect 4 crowns to collect Key 8.""",
        content="Open Crown Door",
        checked=True,
    ),
    ASMPatch(
        asm_file="open_coin_door",
        var_type="checkbox",
        form_var="coin_door_open",
        asm_start=[{"OpenCoinDoor": "after"}],
        tab="misc",
        title="""You do not need to collect the Nintendo and Rareware coin to collect Key 8.
            You will not be able to collect the GB from DK Arcade with this option enabled.""",
        content="Open Nintendo + Rareware Coin Door",
        checked=True,
    ),
    ASMPatch(
        asm_file="rando_level_order",
        var_type="checkbox",
        form_var="randomize_progression",
        asm_start=[{"RandoLevelOrder": "before"}, {"SwapRequirements": "before"}],
    ),
    ASMPatch(
        asm_file="qol/quality_of_life",
        var_type="checkbox",
        form_var="quality_of_life",
        asm_start=[{"QOLChangesShorten": "before"}, {"QOLChanges": "before"}],
        tab="misc",
        title="""This option enables the following quality of life changes to the game:
            - Removes first time text.
            - Removes first time boss cutscenes.
            - Removes first time area visit cutscenes.
            - Removes banana dance cutscenes.
            - Remove cutscenes from the startup sequence.
            - Story Skip option in the main menu set to On by default.""",
        content="Quality of Life Changes",
        checked=True,
    ),
]
