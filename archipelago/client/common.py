"""Common classes and functions for the N64 client for DK64."""

import asyncio
from CommonClient import logger


class DK64MemoryMap:
    """
    DK64MemoryMap is a class that contains memory addresses and offsets used in the game Donkey Kong 64.
    """

    name_location = 0xD0A0A6F8
    memory_pointer = 0x807FFF1C
    counter_offset = 0x000
    start_flag = 0x002
    arch_items = 0x004
    fed_string = 0x008
    connection = 0x029
    fed_subtitle = 0x02B
    EEPROM = 0x807ECEA8
    CurrentGamemode = 0x80755314
    NextGamemode = 0x80755318
    safety_text_timer = 0x02A
    end_credits = 0x1B0


all_tasks = set()


def create_task_log_exception(awaitable) -> asyncio.Task:
    """
    Creates an asyncio task that logs any exceptions raised during its execution.
    Args:
        awaitable: An awaitable object (e.g., coroutine) to be executed.
    Returns:
        asyncio.Task: The created asyncio task.
    The task will log any exceptions raised during its execution using the logger.
    It will also remove itself from the `all_tasks` set upon completion.
    """

    async def _log_exception(awaitable):
        try:
            return await awaitable
        except Exception as e:
            logger.exception(e)
            pass
        finally:
            all_tasks.remove(task)
        return

    task = asyncio.create_task(_log_exception(awaitable))
    all_tasks.add(task)
    return task
