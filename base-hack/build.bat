@echo off
set test_on=%1
echo Started: %date% %time%
mkdir obj

python3 build\compile.py
build\armips.exe asm/jump_list.asm
python3 build\build.py
build\armips.exe asm/main.asm -sym rom\dk64-randomizer-base-dev.sym
rmdir /s /q .\obj > NUL
python3 build\correct_file_size.py
if %test_on% == --test (
	echo Applying test variables
	python3 test_variables_apply.py
)
build\n64crc.exe rom\dk64-randomizer-base-dev.z64
python3 build\dump_pointer_tables_vanilla.py
python3 build\dump_pointer_tables_modified.py
del rom\dk64-randomizer-base-temp.z64
del rom\dk64-randomizer-base.z64


echo Completed: %date% %time%