"""Temp file used for testing new logic system."""
import random
import json
from randomizer.Fill import Fill


def run(fill_type):
    """Generate a seed with a fill type.

    Args:
        fill_type (str): Fill type of forward or assumed.

    Returns:
        str: Currently just a placeholder string return to prove the data moving back to the main UI.
    """
    random.seed()
    return json.dumps(Fill(fill_type))
