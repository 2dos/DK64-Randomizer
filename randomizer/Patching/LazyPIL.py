"""Lazy PIL import proxies.

PIL (Pillow) is only required for ROM patching / cosmetics. This module exposes
proxy objects that defer the real ``from PIL import ...`` until a PIL attribute
is first accessed, so modules that merely *import* these names can be loaded
in environments where Pillow is not installed (e.g. Archipelago).
"""

import importlib
from typing import Any


class _LazyModule:
    """Proxy that imports a submodule on first attribute access."""

    __slots__ = ("_module_name", "_loaded")

    def __init__(self, module_name: str) -> None:
        object.__setattr__(self, "_module_name", module_name)
        object.__setattr__(self, "_loaded", None)

    def _load(self) -> Any:
        loaded = object.__getattribute__(self, "_loaded")
        if loaded is None:
            loaded = importlib.import_module(object.__getattribute__(self, "_module_name"))
            object.__setattr__(self, "_loaded", loaded)
        return loaded

    def __getattr__(self, name: str) -> Any:
        return getattr(self._load(), name)


Image = _LazyModule("PIL.Image")
ImageEnhance = _LazyModule("PIL.ImageEnhance")
ImageDraw = _LazyModule("PIL.ImageDraw")
