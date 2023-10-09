"""Encodes Enum values to JSON."""
from enum import Enum
import json


class EnumEncoder(json.JSONEncoder):
    """Encodes Enum values to JSON."""

    def default(self, obj):
        """Return the JSON representation of obj."""
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)
