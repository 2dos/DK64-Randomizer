"""Library classes for compiling instance scripts."""
from enum import IntEnum, auto
from randomizer.Enums.Kongs import Kongs

class FunctionData:
    """Function Data Class."""

    def __init__(self, function: int, parameters: list, inverted: bool = False, inclusion_lambda=None):
        """Initialize with given parameters."""
        self.function = function
        self.parameters = parameters.copy()
        self.inverted = inverted
        self.include = inclusion_lambda
        if inclusion_lambda is None:
            self.include = lambda _: True

    def compile(self, allow_inversion: bool, val: int) -> list[int]:
        """Compile into a line for a script."""
        if not self.include(val):
            return []
        func = self.function
        if allow_inversion and self.inverted:
            func |= 0x8000
        if len(self.parameters) < 3:
            self.parameters = self.parameters + [0, 0, 0]
            self.parameters = self.parameters[:3]
        return [func] + self.parameters[:3]


class ScriptBlock:
    """Script Block Class."""

    def __init__(self, conditions: list[FunctionData], executions: list[FunctionData], inclusion_lambda=None):
        """Initialize with given parameters."""
        self.conditions = conditions.copy()
        self.executions = executions.copy()
        self.include = inclusion_lambda
        if inclusion_lambda is None:
            self.include = lambda _: True

    def getActiveConditions(self, val: int):
        """Get the active conditions for a block."""
        return [x for x in self.conditions if x.include(val)]

    def getActiveExecutions(self, val: int):
        """Get the active executions for a block."""
        return [x for x in self.executions if x.include(val)]

    def compile(self, val: int) -> list[int]:
        """Compile into a block for a script."""
        if not self.include(val):
            return []
        active_conds = self.getActiveConditions(val)
        active_execs = self.getActiveExecutions(val)
        output_bin = [len(active_conds)]
        if len(active_conds) > 255:
            raise Exception("Too many conditions to compile script.")
        if len(active_execs) > 255:
            raise Exception("Too many executions to compile script.")
        for cond in active_conds:
            output_bin.extend(cond.compile(True, val))
        output_bin.append(len(active_execs))
        for exec in active_execs:
            output_bin.extend(exec.compile(False, val))
        return output_bin


def compileInstanceScript(item_id, script: list[ScriptBlock], val: int = None) -> list[int]:
    """Compile instance script into a binary format."""
    output_bin = [item_id, 0, 0]
    block_count = 0
    for block in script:
        if len(block.getActiveConditions(val)) > 0 or len(block.getActiveExecutions(val)) > 0:
            if block.include(val):
                block_count += 1
                output_bin.extend(block.compile(val))
    output_bin[1] = block_count
    return output_bin

class IScript_IsState(FunctionData):
    """Is the instance script within a certain state."""

    def __init__(self, state, index=0, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(1, [state, index, 0], inverted, inclusion_lambda)

class IScript_SetState(FunctionData):
    """Set the instance script to a certain state."""

    def __init__(self, state, index=0, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(1, [state, index, 0], False, inclusion_lambda)

class IScript_True(FunctionData):
    """Always returns true, unless inverted, in which case always returns false."""

    def __init__(self, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(0, [0, 0, 0], inverted, inclusion_lambda)

class IScript_IsTimer(FunctionData):
    """Is the instance script countdown timer at a certain value."""

    def __init__(self, timer, index=0, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(4, [timer, index, 0], inverted, inclusion_lambda)

class IScript_SetTimer(FunctionData):
    """Set the instance script countdown timer to a certain value."""

    def __init__(self, timer, index=0, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(3, [0, timer, index], False, inclusion_lambda)

class FlagType(IntEnum):
    """Flag Type enum."""
    permanent = auto()
    temporary = auto()
    gbl = auto()

class IScript_IsFlagSet(FunctionData):
    """Is a flag set."""

    def __init__(self, flag_index, flag_type=FlagType.permanent, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        macro_index = 45
        if flag_type == FlagType.temporary:
            macro_index = 54
        elif flag_type == FlagType.gbl:
            macro_index = 59
        super().__init__(macro_index, [flag_index, 0, 0], inverted, inclusion_lambda)

class IScript_SetFlag(FunctionData):
    """Set a certain flag to a certain state."""

    def __init__(self, flag_index, flag_type=FlagType.permanent, output_state=True, inclusion_lambda=None):
        """Initialize with given variables."""
        macro_index = 107
        if flag_type == FlagType.temporary:
            macro_index = 121
        elif flag_type == FlagType.gbl:
            macro_index = 132
        super().__init__(macro_index, [flag_index, 1 if output_state else 0, 0], False, inclusion_lambda)

class IScript_InRange(FunctionData):
    """Is the player within a certain range of the target object."""

    def __init__(self, range, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(19, [range, 0, 0], inverted, inclusion_lambda)

class IScript_IsCutsceneActive(FunctionData):
    """Is a cutscene active."""

    def __init__(self, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(35, [0, 0, 0], inverted, inclusion_lambda)

class RunState(IntEnum):
    init = 0
    run = 1
    pause = 2
    distance = 3

class IScript_SetScriptRunState(FunctionData):
    """Set the script run state of the object tied to the script."""

    def __init__(self, state: RunState, distance: int=0, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(38, [state, distance, 0], False, inclusion_lambda)

class IScript_PlayCutscene(FunctionData):
    """Set the script run state of the object tied to the script."""

    def __init__(self, cutscene_index: int, extra_args: int = 1, tied_spawner_index: int = 0, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(37, [cutscene_index, extra_args, tied_spawner_index], False, inclusion_lambda)

class IScript_HasSpecialMove(FunctionData):
    """Set the script run state of the object tied to the script."""

    def __init__(self, kong: Kongs, move_index: int, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(52, [2 + int(kong), move_index, 0], inverted, inclusion_lambda)

class IScript_IsStandingOnObject(FunctionData):
    """Is standing on the object tied to the script."""

    def __init__(self, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(2, [0, 0, 0], inverted, inclusion_lambda)

class IScript_InControlState(FunctionData):
    """Is the player is in a certain control state."""

    def __init__(self, control_state: int, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(23, [control_state, 0, 0], inverted, inclusion_lambda)

class IScript_InControlStateAndProgress(FunctionData):
    """Is the player is in a certain control state and progress."""

    def __init__(self, control_state: int, progress: int, inverted=False, inclusion_lambda=None):
        """Initialize with given variables."""
        super().__init__(23, [control_state, progress, 0], inverted, inclusion_lambda)