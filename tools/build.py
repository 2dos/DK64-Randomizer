"""Build C code along with package textures and associated items for release."""
import os
import urllib.request
import zipfile
import tarfile
import subprocess


file_data = [
    {
        "name": "Menu Text",
        "pointer_table_index": 12,
        "file_index": 37,
        "source_file": "Menu.bin",
        "patcher": "temp",
    }
]

# Change our root directory to where this script is located
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Set headers so we don't freak out webdownloaders
opener = urllib.request.build_opener()
opener.addheaders = [("User-agent", "Mozilla/5.0")]
urllib.request.install_opener(opener)

if os.name == "nt":
    print("Building for Windows")
    
    # Download our required files
    urllib.request.urlretrieve(
        "https://github.com/tj90241/n64chain/releases/download/9.1.0/n64chain-windows.zip", "n64chain-windows.zip"
    )
    urllib.request.urlretrieve("https://dl.smwcentral.net/11474/floating.zip", "flips.zip")
    # urllib.request.urlretrieve("https://github.com/Isotarge/n64tex/releases", "n64tex.exe")

    # Unzip the zipped packages
    with zipfile.ZipFile("flips.zip", "r") as zip_ref:
        zip_ref.extractall("./")
    with zipfile.ZipFile("n64chain-windows.zip", "r") as zip_ref:
        zip_ref.extractall("./")
    
    # Set our object vars
    n64tex = ["n64tex.exe"]
    flips = ["flips.exe"]
    n64chain = ["bin/mips64-elf-gcc.exe"]
else:
    print("Building for Linux")

    # Download our required files
    urllib.request.urlretrieve(
        "https://github.com/tj90241/n64chain/releases/download/9.1.0/n64chain-linux.tgz", "n64chain-linux.tgz"
    )
    urllib.request.urlretrieve("https://dl.smwcentral.net/11474/floating.zip", "flips.zip")
    # urllib.request.urlretrieve("https://github.com/Isotarge/n64tex/releases", "n64tex.exe")

    # Install mono so we can run n64tex
    subprocess.run(["apt", "install", "-y", "gnupg", "ca-certificates"])
    subprocess.run(
        [
            "apt-key",
            "adv",
            "--keyserver",
            "hkp://keyserver.ubuntu.com:80",
            "--recv-keys",
            "3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF",
        ]
    )
    subprocess.run(
        [
            "echo",
            '"deb https://download.mono-project.com/repo/ubuntu stable-focal main"',
            "|",
            "tee",
            "/etc/apt/sources.list.d/mono-official-stable.list",
        ]
    )
    subprocess.run(["apt", "update", "-y"])
    subprocess.run(["apt", "install", "-y", "mono-devel"])

    # Unpack tools
    with zipfile.ZipFile("flips.zip", "r") as zip_ref:
        zip_ref.extractall("./")
    with tarfile.open("n64chain-linux.tgz") as tar_file:
        tar_file.extractall("./")

    # Set our object vars
    n64tex = ["mono", "n64tex.exe"]
    flips = ["flips-linux"]
    n64chain = ["tools/bin/mips64-elf-gcc"]

# For each object in the file data, convert the texture
# We use *tool in the subprocess to unpack the tool into the CLI without needing all the vars defined
for file in file_data:
    if file["texture_format"] in ["rgba5551", "i4", "ia4", "i8", "ia8"]:
        result = subprocess.check_output([*n64tex, file["texture_format"], file["source_file"]])
    else:
        print(" - ERROR: Unsupported texture format " + file["texture_format"])

# subprocess.check_output([*flips, "-c"  "--bps", "input-file", "output-file"])
# subprocess.check_output([*n64chain, "blah"])
