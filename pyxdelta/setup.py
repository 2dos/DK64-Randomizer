"""Pyxdelta setup script."""
import os
import sys
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

MACROS = [
    ("SIZEOF_SIZE_T", "8" if sys.maxsize > 2**32 else "4"),
    ("SIZEOF_UNSIGNED_LONG_LONG", "8"),
    ("XD3_DEBUG", "0"),
    ("XD3_USE_LARGEFILE64", "1"),
    ("SECONDARY_DJW", "1"),
    ("SECONDARY_FGK", "1"),
    ("SECONDARY_LZMA", "0"),
    ("EXTERNAL_COMPRESSION", "0"),
    ("NOT_MAIN", "1"),
]

if os.name == "nt":
    MACROS.append(("XD3_WIN32", "1"))
    MACROS.append(("XD3_STDIO", "0"))
    MACROS.append(("XD3_POSIX", "0"))
    MACROS.append(("XDWORKAROUND", ""))
    MACROS.append(("WIN32", ""))
    EXTRA_COMPILE_ARGS = []
else:
    MACROS.append(("XD3_WIN32", "0"))
    MACROS.append(("XD3_STDIO", "1"))
    MACROS.append(("XD3_POSIX", "0"))
    EXTRA_COMPILE_ARGS = ["-Wall", "-Wshadow", "-fno-builtin", "-Wextra", "-Wsign-compare", "-Wformat=2", "-Wno-format-nonliteral", "-Wno-unused-parameter", "-Wno-unused-function"]

INCLUDES = ["xdelta/xdelta3"]
SOURCES = ["pyxdelta.c"]


def main():
    """Func for setup."""
    setup(
        name="pyxdelta",
        version="0.1.2",
        author="Illidan",
        description="Python interface for xdelta.",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Illidanz/pyxdelta",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
        ],
        ext_modules=[Extension("pyxdelta", SOURCES, include_dirs=INCLUDES, define_macros=MACROS, extra_compile_args=EXTRA_COMPILE_ARGS)],
    )


if __name__ == "__main__":
    main()
