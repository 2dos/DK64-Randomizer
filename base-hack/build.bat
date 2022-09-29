@echo off
set test_on=%1
set python_ver=%2
cls
setlocal EnableDelayedExpansion
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"
echo Started: %date% %time% > rom/build.log
echo Started: %date% %time%
IF EXIST "rom/dk64.z64" (
    echo 'ROM Exists.' >> rom/build.log
) ELSE (
    echo 'Error: DK64.z64 file missing from base-hack/rom/' >> rom/build.log
	exit 1
)
mkdir obj
IF NOT DEFINED python_ver (set python_ver="python3")
IF DEFINED test_on (echo "Building patch file" >> rom/build.log)  ELSE (set test_on="")
@REM %python_ver% build\build_offset_file.py
echo.

<nul set /p=Installing Packages!CR!
%python_ver% build\install_packages.py >> rom/build.log
echo Installing Packages [32mDONE[0m

<nul set /p=Pulling Images from ROM!CR!
%python_ver% build\pull_images_from_rom.py >> rom/build.log
echo Pulling Images from ROM [32mDONE[0m

<nul set /p=Modifying images from ROM!CR!
%python_ver% build\createComplexImages.py >> rom/build.log
echo Modifying images from ROM [32mDONE[0m

<nul set /p=Compile C Code!CR!
%python_ver% build\compile.py >> rom/build.log
echo Compile C Code [32mDONE[0m

<nul set /p=Running ARMIPS (Jumplist)!CR!
build\armips.exe asm/jump_list.asm
echo Running ARMIPS (Jumplist) [32mDONE[0m

<nul set /p=Running Cranky's Lab!CR!
%python_ver% build\build.py >> rom/build.log
echo Running Cranky's Lab [32mDONE[0m

<nul set /p=Building Symbols File!CR!
build\armips.exe asm/main.asm -sym rom\dk64-randomizer-base-dev.sym
echo Building Symbols File [32mDONE[0m

rmdir /s /q .\obj > NUL

<nul set /p=Align ROM File Size!CR!
%python_ver% build\correct_file_size.py >> rom/build.log
echo Align ROM File Size [32mDONE[0m

if %test_on% == --test (
	echo Applying test variables >> rom/build.log

	<nul set /p=Apply Test Variables!CR!
	%python_ver% test_variables_apply.py >> rom/build.log
	echo Apply Test Variables [32mDONE[0m

	<nul set /p=Modify Kong Colors!CR!
	%python_ver% build\generate_kong_color_images.py >> rom/build.log
	echo Modify Kong Colors [32mDONE[0m
)

<nul set /p=Modify ROM CRC!CR!
build\n64crc.exe rom\dk64-randomizer-base-dev.z64 >> rom/build.log
echo Modify ROM CRC [32mDONE[0m

<nul set /p=Dump pointer tables!CR!
%python_ver% build\dump_pointer_tables_vanilla.py >> rom/build.log
%python_ver% build\dump_pointer_tables_modified.py >> rom/build.log
echo Dump pointer tables [32mDONE[0m

if %test_on% == --test GOTO finish
<nul set /p=Create base hack BPS!CR!
build\flips.exe .\rom\dk64.z64 .\rom\dk64-randomizer-base-dev.z64 .\rom\patch.bps --bps >> rom/build.log
echo Create base hack BPS [32mDONE[0m

copy rom\patch.bps ..\static\patches\shrink-dk64.bps >> rom/build.log
del rom\dk64-randomizer-base-temp.z64
del rom\dk64-randomizer-base.z64
del rom\dk64-randomizer-base-dev.z64
del rom\dk64-randomizer-base.wch
del rom\dk64-randomizer-base-dev.sym
del rom\patch.bps

:finish

echo.
echo Completed: %date% %time% >> rom/build.log
echo Completed: %date% %time%
exit /b

:spinner
set /a "spinner=(spinner + 1) %% 4"
set "spinChars=\|/-"
<nul set /p ".=Waiting !spinChars:~%spinner%,1!!CR!"
exit /b