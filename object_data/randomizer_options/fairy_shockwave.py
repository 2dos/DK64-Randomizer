"""Code only ran for fairy shockwave."""


def set_fairy_rewards(asm: str, post_data: dict):
    """Set fairy reward ASM value.

    Args:
        asm (str): Current ASM code.
        post_data (dict): Form dict options.

    Returns:
        tuple: asm, log_data
    """
    asm += ".align" + "\n" + "FairyQueenRewards:" + "\n"
    if post_data.get("unlock_fairy_shockwave"):
        asm += "\t" + ".half 377\n"
    asm += "\t" + ".half 0\n"
    return asm, None
