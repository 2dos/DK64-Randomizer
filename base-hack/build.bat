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
	echo 'Error: DK64.z64 file missing from base-hack/rom/'
	exit 1
)
mkdir obj
IF NOT DEFINED python_ver (set python_ver="python3")
IF DEFINED test_on (echo "Building patch file" >> rom/build.log)  ELSE (set test_on="")
echo.
if %test_on% == --test (
	call :runscript "Fixing Krusha's size", "build\write_krusha_variables.py"
	echo 0 > Build/BuildingBPS.txt
) else (
	echo -1 > krusha_setting.txt
	echo 1 > Build/BuildingBPS.txt
)
call :runscript "Define Heap", "build\heap.py"
call :runscript "Installing Packages", "build\install_packages.py"
call :runscript "Pulling Images from ROM", "build\pull_images_from_rom.py"
call :runscript "Modifying images from ROM", "build\createComplexImages.py"
call :runscript "Building Cutscene Database", "build\build_cutscene_dict.py"
call :runscript "Building Item Database", "build\item_dictionaries.py"
call :runscript "Compile C Code", "build\compile.py"

<nul set /p=Running ARMIPS (Jumplist)!CR!
call :setstart
build\armips.exe asm/jump_list.asm
call :setfinish runtime
echo Running ARMIPS (Jumplist) [32mDONE[0m (%runtime%)

call :runscript "Running Cranky's Lab", "build\build.py"

<nul set /p=Building Symbols File!CR!
call :setstart
build\armips.exe asm/main.asm -sym rom\dk64-randomizer-base-dev.sym
call :setfinish runtime
echo Building Symbols File [32mDONE[0m (%runtime%)

rmdir /s /q .\obj > NUL

call :runscript "Align ROM File Size", "build\correct_file_size.py"

if %test_on% == --test (
	echo Applying test variables >> rom/build.log

	call :runscript "Apply Test Variables", "test_variables_apply.py"
	call :runscript "Modifying Kong Colors", "build\generate_kong_color_images.py"
)

<nul set /p=Modify ROM CRC!CR!
call :setstart
build\n64crc.exe rom\dk64-randomizer-base-dev.z64 >> rom/build.log
call :setfinish runtime
echo Modify ROM CRC [32mDONE[0m (%runtime%)

<nul set /p=Dump pointer tables!CR!
call :setstart
%python_ver% build\dump_pointer_tables_vanilla.py >> rom/build.log
%python_ver% build\dump_pointer_tables_modified.py >> rom/build.log
call :setfinish runtime
echo Dump pointer tables [32mDONE[0m (%runtime%)

if %test_on% == --test GOTO finish
<nul set /p=Create base hack BPS!CR!
call :setstart
build\flips.exe .\rom\dk64.z64 .\rom\dk64-randomizer-base-dev.z64 .\rom\patch.bps --bps >> rom/build.log
call :setfinish runtime
echo Create base hack BPS [32mDONE[0m (%runtime%)

copy rom\patch.bps ..\static\patches\shrink-dk64.bps >> rom/build.log
del rom\dk64-randomizer-base-temp.z64
del rom\dk64-randomizer-base.z64
del rom\dk64-randomizer-base-dev.z64
del rom\dk64-randomizer-base.wch
del rom\dk64-randomizer-base-dev.sym
del rom\patch.bps

:finish
del krusha_setting.txt
del Build\BuildingBPS.txt
call :runscript "Removing unneccessary files", "build\cleanup.py"

echo.
echo Completed: %date% %time% >> rom/build.log
echo Completed: %date% %time%
exit /b

:runscript
<nul set /p=%~1!CR!
call :setstart
%python_ver% %~2 >> rom/build.log
call :setfinish runtime
echo %~1 [32mDONE[0m (%runtime%)
exit /B 0

:setstart
set "startTime=%time: =0%"
exit /B 0

:setfinish
set "endTime=%time: =0%"
set "end=!endTime:%time:~8,1%=%%100)*100+1!"  &  set "start=!startTime:%time:~8,1%=%%100)*100+1!"
set /A "elap=((((10!end:%time:~2,1%=%%100)*60+1!%%100)-((((10!start:%time:~2,1%=%%100)*60+1!%%100), elap-=(elap>>31)*24*60*60*100"
set /A "cc=elap%%100+100,elap/=100,ss=elap%%60+100,elap/=60,mm=elap%%60+100,hh=elap/60+100"
set "%~1=%hh:~1%%time:~2,1%%mm:~1%%time:~2,1%%ss:~1%%time:~8,1%%cc:~1%"
exit /B 0