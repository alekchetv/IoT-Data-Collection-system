@echo off
cd ./pio_diplom
pio run
.\espota.exe -r -i 192.168.39.232 -f ".\.pio\build\esp32doit-devkit-v1\firmware.bin"
exit 1