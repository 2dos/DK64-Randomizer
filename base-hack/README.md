# Donkey Kong 64 Randomizer - Base Hack

## Building Pre-requisites
- Python 3
- [n64chain](https://github.com/tj90241/n64chain/releases/tag/9.1.0)

## Build Setup (Windows)
1. Download ```n64chain-windows.zip``` from [here](https://github.com/tj90241/n64chain/releases/tag/9.1.0)
2. Extract to ```C:\n64chain```
3. Add ```C:\n64chain\tools\bin``` to your system %path% environment variable
4. Install ```Python 3```
5. Git clone (or download a zip + extract) this repo to somewhere convenient
6. Create a ```base-hack/rom``` subdirectory in the root of the repo
7. Put ```dk64.z64``` (SHA1: CF806FF2603640A748FCA5026DED28802F1F4A50) in the ```rom``` subdirectory
8. Run ```build.bat```

Provided everything is working, the built ROM will appear in the ```rom``` subdirectory