@echo off
set test_on=%1
set python_ver=%2
echo Started: %date% %time%
IF EXIST "rom/dk64.z64" (
    echo 'ROM Exists.'
) ELSE (
    echo 'Error: DK64.z64 file missing from base-hack/rom/'
	exit 1
)
mkdir obj
IF NOT DEFINED python_ver (set python_ver="python3")
IF DEFINED test_on (echo "Building patch file")  ELSE (set test_on="")
%python_ver% build\pull_images_from_rom.py
%python_ver% build\createComplexImages.py
%python_ver% build\compile.py
build\armips.exe asm/jump_list.asm
%python_ver% build\build.py
build\armips.exe asm/main.asm -sym rom\dk64-randomizer-base-dev.sym
rmdir /s /q .\obj > NUL
%python_ver% build\correct_file_size.py
if %test_on% == --test (
	echo Applying test variables
	%python_ver% test_variables_apply.py
)
build\n64crc.exe rom\dk64-randomizer-base-dev.z64
%python_ver% build\dump_pointer_tables_vanilla.py
%python_ver% build\dump_pointer_tables_modified.py
if %test_on% == --test GOTO finish
build\flips.exe .\rom\dk64.z64 .\rom\dk64-randomizer-base-dev.z64 .\rom\patch.bps --bps

copy rom\patch.bps ..\static\patches\shrink-dk64.bps
del rom\dk64-randomizer-base-temp.z64
del rom\dk64-randomizer-base.z64
del rom\dk64-randomizer-base-dev.z64
del rom\dk64-randomizer-base.wch
del rom\dk64-randomizer-base-dev.sym
del rom\patch.bps

:finish

echo Completed: %date% %time%