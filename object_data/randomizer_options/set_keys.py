"""Used for setting Key order in the ASM."""


def set_keys(post_data: dict):
    """Set Key Order ASM Code.

    Args:
        post_data (dict): Form dict options.

    Returns:
        tuple: asm, log_data
    """
    # Set Keys
    finalKeyFlags = [
        "0x001A",
        "0x004A",
        "0x008A",
        "0x00A8",
        "0x00EC",
        "0x0124",
        "0x013D",
    ]
    finalNumerical = post_data.get("finalNumerical")
    # for x in finalNumerical:
    #     asm += "\t" + ".half " + str(finalKeyFlags[x]) + "\n"
    return None
