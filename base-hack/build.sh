#!/usr/bin/env bash
set -euo pipefail

test_on="${1:-}"
python_ver="${2:-python}"
use_compiled=0

# Clear screen
clear

# Create log file
mkdir -p rom
echo "Started: $(date)" > rom/build.log
echo "Started: $(date)"

# Check ROM exists
if [[ -f "rom/dk64.z64" ]]; then
    echo "ROM Exists." >> rom/build.log
else
    echo "Error: DK64.z64 file missing from base-hack/rom/" | tee -a rom/build.log
    exit 1
fi

# Create object directory
mkdir -p obj

if [[ -n "$test_on" ]]; then
    echo "Building patch file" >> rom/build.log
fi

# Set Build flag
if [[ "$test_on" == "--test" ]]; then
    echo 0 > build/BuildingBPS.txt
else
    echo 1 > build/BuildingBPS.txt
fi

# Helper function to run python scripts
runscript() {
    local msg="$1"
    local script="$2"
    echo -n "$msg..."
    start_time=$(date +%s%3N)
    "$python_ver" "$script" >> rom/build.log
    end_time=$(date +%s%3N)
    runtime=$((end_time - start_time))
    echo " $msg DONE ($runtime ms)"
}

runscriptarg() {
    local msg="$1"
    local script="$2"
    local arg="$3"
    echo -n "$msg..."
    start_time=$(date +%s%3N)
    "$python_ver" "$script" "$arg" >> rom/build.log
    end_time=$(date +%s%3N)
    runtime=$((end_time - start_time))
    echo " $msg DONE ($runtime ms)"
}

# Run all build scripts
runscript "Pulling actor data from ROM" "build/getDefaultData.py"
runscript "Building Item Previews File" "build/dump_previews.py"
runscript "Define Heap" "build/heap.py"
runscript "Installing Packages" "build/install_packages.py"
runscript "Pulling Images from ROM" "build/pull_images_from_rom.py"
runscript "Modifying images from ROM" "build/createComplexImages.py"
runscript "Building Item Database" "build/item_dictionaries.py"
runscript "Adjusting Pause Menu Variables" "build/adjust_pause_rotation.py"
runscript "Building Hint Regions" "build/build_hint_regions.py"
runscript "Building Dynamic Bitfields" "build/build_dynamic_bitfields.py"
runscript "Remembering the 21st Night of September" "build/disco_donkey.py"

if [[ "$use_compiled" -eq 1 ]]; then
    runscript "Compile Cranky's Lab" "build/pyinstaller_handler.py"
fi

runscript "Compile C Code" "build/compile-linux.py"

# Run ARMIPS Jumplist
echo -n "Running ARMIPS (Jumplist)..."
start_time=$(date +%s%3N)
build/armips/build/armips asm/jump_list.asm
end_time=$(date +%s%3N)
runtime=$((end_time - start_time))
echo " DONE ($runtime ms)"

if [[ "$use_compiled" -eq 0 ]]; then
    runscript "Running Cranky's Lab" "build/build.py"
else
    echo -n "Running Cranky's Lab..."
    start_time=$(date +%s%3N)
    build/dist/build >> rom/build.log
    end_time=$(date +%s%3N)
    runtime=$((end_time - start_time))
    echo " DONE ($runtime ms)"
fi

runscript "Building Cutscene Database" "build/build_cutscene_dict.py"

# Build Symbols File
echo -n "Building Symbols File..."
start_time=$(date +%s%3N)
build/armips/build/armips asm/main.asm -sym rom/dev-symbols.sym
end_time=$(date +%s%3N)
runtime=$((end_time - start_time))
echo " DONE ($runtime ms)"

# Remove object files
rm -rf obj

runscript "Align ROM File Size" "build/correct_file_size.py"
runscript "Assessing Function Sizes" "build/assess_rom.py"

if [[ "$test_on" == "--test" ]]; then
    echo "Applying test variables" >> rom/build.log
    # runscript "Apply Test Variables" "../base_hack_test.py"
    runscript "Modifying Kong Colors" "build/generate_kong_color_images.py"
fi

# Modify ROM CRC
runscriptarg "Modify ROM CRC..." "build/crc.py" "rom/dk64-randomizer-base-dev.z64"

# Dump pointer tables
echo -n "Dump pointer tables..."
start_time=$(date +%s%3N)
"$python_ver" build/dump_pointer_tables_vanilla.py >> rom/build.log
"$python_ver" build/dump_pointer_tables_modified.py >> rom/build.log
"$python_ver" build/symbol_json_builder.py >> rom/build.log
end_time=$(date +%s%3N)
runtime=$((end_time - start_time))
echo " DONE ($runtime ms)"

if [[ "$test_on" == "--test" ]]; then
    :
else
    # Create base hack BPS
    echo -n "Create base hack BPS..."
    start_time=$(date +%s%3N)
    build/flips-linux ./rom/dk64.z64 ./rom/dk64-randomizer-base-dev.z64 ./rom/patch.bps --bps >> rom/build.log
    end_time=$(date +%s%3N)
    runtime=$((end_time - start_time))
    echo " DONE ($runtime ms)"

    # Copy patch
    mkdir -p ../static/patches
    cp rom/patch.bps ../static/patches/shrink-dk64.bps
    rm -f rom/dk64-randomizer-base-temp.z64 rom/dk64-randomizer-base.z64 rom/dk64-randomizer-base-dev.z64 rom/dk64-randomizer-base.wch rom/patch.bps
fi

runscript "Removing unnecessary files" "build/cleanup.py"

echo
echo "Completed: $(date)" >> rom/build.log
echo "Completed: $(date)"
