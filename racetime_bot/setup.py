"""Setup script for racetime_bot."""

from setuptools import find_packages, setup


setup(
    name="dk64-randobot",
    description="racetime.gg bot for generating DK64R seeds.",
    license="MIT",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    url="https://racetime.gg/dk64r",
    project_urls={
        "Source": "https://github.com/2dos/dk64-randomizer",
    },
    version="1.0.0",
    install_requires=[
        "gql[aiohttp]>=3.4.0,<4.0",
        "isodate>=0.6.1,<0.7",
        "racetime_bot>=1.5.0,<3.0",
        "requests>=2.25.1,<3.0",
        "opentelemetry-exporter-otlp-proto-http",
        "opentelemetry-instrumentation-requests",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "randobot=randobot:main",
        ],
    },
)
