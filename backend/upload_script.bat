@echo off
cd ./pio_diplom
pio run
.\espota.exe -r -i {{ip_address}} -f ".\.pio\build\esp32doit-devkit-v1\firmware.bin"
exit 1