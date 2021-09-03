def set_fairy_rewards(asm: str, post_data: dict):
    asm += ".align" + "\n" + "FairyQueenRewards:" + "\n"
    if post_data.get("unlock_fairy_shockwave"):
        asm += "\t" + ".half 377\n"
    asm += "\t" + ".half 0\n"
    return asm, None
