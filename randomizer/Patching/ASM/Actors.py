"""Write ASM data for the actor elements."""

from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.Library.ASM import *

def expandActorTable(ROM_COPY: LocalROM, settings, offset_dict: dict):
    """All changes related to the expansion of the actor table."""
    # Actor Expansion
    ACTOR_COLLISION_START = getSym("actor_collisions")
    ACTOR_HEALTH_START = getSym("actor_health_damage")
    # Definitions
    actor_def_hi = getHiSym("actor_defs")
    actor_def_lo = getLoSym("actor_defs")
    writeValue(ROM_COPY, 0x8068926A, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x8068927A, Overlay.Static, actor_def_lo, offset_dict)
    writeValue(ROM_COPY, 0x806892D2, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x806892D6, Overlay.Static, actor_def_lo, offset_dict)
    writeValue(ROM_COPY, 0x8068945A, Overlay.Static, actor_def_hi, offset_dict)
    writeValue(ROM_COPY, 0x80689466, Overlay.Static, actor_def_lo, offset_dict)
    def_limit = getVar("DEFS_LIMIT")
    writeValue(ROM_COPY, 0x8068928A, Overlay.Static, def_limit, offset_dict)
    writeValue(ROM_COPY, 0x80689452, Overlay.Static, def_limit, offset_dict)
    # Functions
    actor_function_hi = getHiSym("actor_functions")
    actor_function_lo = getLoSym("actor_functions")
    writeValue(ROM_COPY, 0x806788F2, Overlay.Static, actor_function_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067890E, Overlay.Static, actor_function_lo, offset_dict)
    writeValue(ROM_COPY, 0x80678A3E, Overlay.Static, actor_function_hi, offset_dict)
    writeValue(ROM_COPY, 0x80678A52, Overlay.Static, actor_function_lo, offset_dict)
    # writeLabelValue(ROM_COPY, 0x8076152C, Overlay.Static, "actor_functions", offset_dict)
    # writeLabelValue(ROM_COPY, 0x80764768, Overlay.Static, "actor_functions", offset_dict)
    # Collision
    actor_col_hi_info = getHi(ACTOR_COLLISION_START + 0)
    actor_col_lo_info = getLo(ACTOR_COLLISION_START + 0)
    actor_col_hi_unk4 = getHi(ACTOR_COLLISION_START + 4)
    actor_col_lo_unk4 = getLo(ACTOR_COLLISION_START + 4)
    writeValue(ROM_COPY, 0x8067586A, Overlay.Static, actor_col_hi_info, offset_dict)
    writeValue(ROM_COPY, 0x80675876, Overlay.Static, actor_col_lo_info, offset_dict)
    writeValue(ROM_COPY, 0x806759F2, Overlay.Static, actor_col_hi_unk4, offset_dict)
    writeValue(ROM_COPY, 0x80675A02, Overlay.Static, actor_col_lo_unk4, offset_dict)
    writeValue(ROM_COPY, 0x8067620E, Overlay.Static, actor_col_hi_unk4, offset_dict)
    writeValue(ROM_COPY, 0x8067621E, Overlay.Static, actor_col_lo_unk4, offset_dict)
    # Health
    actor_health_hi_health = getHi(ACTOR_HEALTH_START + 0)
    actor_health_lo_health = getLo(ACTOR_HEALTH_START + 0)
    actor_health_hi_dmg = getHi(ACTOR_HEALTH_START + 2)
    actor_health_lo_dmg = getLo(ACTOR_HEALTH_START + 2)
    writeValue(ROM_COPY, 0x806761D6, Overlay.Static, actor_health_hi_health, offset_dict)
    writeValue(ROM_COPY, 0x806761E2, Overlay.Static, actor_health_lo_health, offset_dict)
    writeValue(ROM_COPY, 0x806761F2, Overlay.Static, actor_health_hi_dmg, offset_dict)
    writeValue(ROM_COPY, 0x806761FE, Overlay.Static, actor_health_lo_dmg, offset_dict)
    # Interactions
    actor_interaction_hi = getHiSym("actor_interactions")
    actor_interaction_lo = getLoSym("actor_interactions")
    writeValue(ROM_COPY, 0x806781BA, Overlay.Static, actor_interaction_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067820A, Overlay.Static, actor_interaction_lo, offset_dict)
    writeValue(ROM_COPY, 0x8067ACCA, Overlay.Static, actor_interaction_hi, offset_dict)
    writeValue(ROM_COPY, 0x8067ACDA, Overlay.Static, actor_interaction_lo, offset_dict)
    # Master Type
    actor_mtype_hi = getHiSym("actor_master_types")
    actor_mtype_lo = getLoSym("actor_master_types")
    writeValue(ROM_COPY, 0x80677EF6, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80677F02, Overlay.Static, actor_mtype_lo, offset_dict)
    writeValue(ROM_COPY, 0x80677FCA, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80677FD2, Overlay.Static, actor_mtype_lo, offset_dict)
    writeValue(ROM_COPY, 0x80678CDA, Overlay.Static, actor_mtype_hi, offset_dict)
    writeValue(ROM_COPY, 0x80678CE6, Overlay.Static, actor_mtype_lo, offset_dict)
    # Paad
    writeValue(ROM_COPY, 0x8067805E, Overlay.Static, getHiSym("actor_extra_data_sizes"), offset_dict)
    writeValue(ROM_COPY, 0x80678062, Overlay.Static, getLoSym("actor_extra_data_sizes"), offset_dict)