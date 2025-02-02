<div id="top"></div>
<br />
<div align="center" style="text-align:center">
  <a href="https://github.com/2dos/DK64-Randomizer">
    <img src="https://raw.githubusercontent.com/2dos/DK64-Randomizer/refs/heads/dev/static/img/logo.png" alt="Logo" width="381" height="300">
  </a>

  <h1 align="center">DK64 Randomizer</h1>
<img alt="Stable Branch Version" src="https://img.shields.io/badge/stable-3.0-darkgreen">
<img alt="Dev Branch Version" src="https://img.shields.io/badge/dev-4.0-midnightblue">
<img alt="GitHub License" src="https://img.shields.io/github/license/2dos/DK64-Randomizer?color=darkred">
<img alt="Seeds Genned" src="https://img.shields.io/endpoint?url=https%3A%2F%2Fapi.dk64rando.com%2Fapi%2Fcurrent_total%3Fformat%3Dtotal_shield">


<p align="center">
    Python/C based builder and patching system for randomizing DK64 entirely within your browser.
    <br />
    <a href="https://dk64randomizer.com/wiki/"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://dk64randomizer.com/">Live Site</a>
    ·
    <a href="https://dev.dk64randomizer.com/">Dev Site</a>
    ·
    <a href="https://github.com/2dos/DK64-Randomizer/issues">Report Bug/Features</a>
    ·
    <a href="https://discord.dk64randomizer.com">Discord</a>
  </p>
</div>



## Table of Contents
- [Table of Contents](#table-of-contents)
- [About the project](#about-the-project)
- [Getting Started](#getting-started)
  - [Requirements](#requirements)
  - [Installation](#installation)
- [Usage](#usage)
- [FAQ](#faq)
  - [Q: Is this randomizer beatable?](#q-is-this-randomizer-beatable)
  - [Q: Can I use this on console hardware?](#q-can-i-use-this-on-console-hardware)
  - [Q: Where can I report issues?](#q-where-can-i-report-issues)
- [Contributing](#contributing)

## About the project

**DK64 Randomizer** is a tool that randomizes various elements of *Donkey Kong 64*, giving players a new and unpredictable experience each time they play. This randomizer shuffles item placements, Kongs, enemies, and more, creating a fresh and challenging take on the beloved classic.

<p align="right">(<a href="#top">back to top</a>)</p>

## Getting Started

### Requirements
- **Base ROM of *Donkey Kong 64*:** You will need a legally obtained ROM of the US version of *Donkey Kong 64* for this randomizer to work. PAL, JP, Kiosk and the Lodgenet releases are not supported. No help will be provided to acquire this.
- **Emulator or Console Setup:** Compatible with many platforms, more information about this can be found on our [wiki](https://dev.dk64randomizer.com/wiki/index.html?title=Consoles-and-Emulators)
- **Python 3.11 or Higher:** The randomizer is largely coded implemented in Python, so make sure you have Python installed on your system.

<p align="right">(<a href="#top">back to top</a>)</p>

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/2dos/DK64-Randomizer.git
   cd DK64-Randomizer
   ```
2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. **Place a DK64 ROM into the repo**:
The US ROM needs to be named `dk64.z64` and placed into the base directory of the repository.
4. **Run the Randomizer**:
   Run `runner.py` to boot up a local copy of the randomizer webpage at `localhost:8000`. This can also be achieved with the `Run Server` task on VSCode.

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage

1. **Load Your ROM**:
   When prompted, provide the path to your *Donkey Kong 64* ROM file.
   
2. **Set Randomization Options**:
   Customize your randomization preferences (items, Kongs, enemies, etc.) via the locally generated webpage.
   
3. **Generate ROM**:
   Once settings are configured, generate a randomized ROM file by following the prompts.

4. **Play**:
   Load the newly generated ROM file into your platform of choice.

<p align="right">(<a href="#top">back to top</a>)</p>

## FAQ

### Q: Is this randomizer beatable?
Yes! The randomizer includes logic to ensure that all generated seeds are beatable to 101% completion.

### Q: Can I use this on console hardware?
Yes, but you will need a flash cart like the EverDrive 64 to load the randomized ROM. The Wii U Virtual Console is also supported if you have a homebrewed Wii U.

### Q: Where can I report issues?
Please report any issues on the [GitHub Issues page](https://github.com/2dos/DK64-Randomizer/issues).

<p align="right">(<a href="#top">back to top</a>)</p>

## Contributing
We welcome contributions from the community! To contribute:
1. Fork the repository.
2. Create a new branch for your changes.
3. Make your modifications.
4. Submit a pull request.

For major changes, please open a discussion first to ensure your feature or change is something that we think would result in a better product.

<p align="right">(<a href="#top">back to top</a>)</p>
