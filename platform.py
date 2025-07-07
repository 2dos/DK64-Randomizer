import sys
from enum import Enum, auto

class Platform(Enum):
    WINDOWS = auto()
    LINUX = auto()

    def get_type():
        platform_type = sys.platform
        platform_dict = {
                "win32": Platform.WINDOWS,
                "linux": Platform.LINUX,
        }

        if platform_type not in platform_dict:
            raise Exception(f"Unsupported platform: {platform_type}")
        else:
            return platform_dict[platform_type]

