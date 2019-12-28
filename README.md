# IQvizyon Prototype Iot Project
This project is written to test our software with real data.
Rationale behind choosing MicroPython is development time.
We abandoned development of the project in late 2018 and we're releasing the code under GPLv3 except bundled code.

## What it does
The project starts with connecting to the wifi, then updated the clock via NTP, after that, the main loop starts.
Main loop loads a settings json file, which should be bundled with the code, then starts sensors and polls every 100ms.
All sensors have a internal cache for sampling, and for every second, they return the average data.
Then the code is posted to a web service for every sensor, one by one.

For any error, the internal oled screen will show a simple information about the error.
Otherwise it'll show time and local ip address.

## Details
### upload.py
This file runs mpy-cross for all files to minimize both memory and storage footprints, as well as upload times.
It requires mpy-cross, ampy and fuser programs and meant to be run under any Gnu/Linux.

### Sensors and structure
Code is written for an esp8266 based development kit, all the parts are off the shelf and readily available at Adafruit.
We've never implemented some sensors due to lack of interest.

* TMP007 contact-less temperature sensor is unimplemented.
* LIS3DH triple axis accelerometer is implemented, yet the data is not accurately stored.
* SHT31-D temperature and humidity sensor is implemented, data is accurate.
* PCF8523 real time clock is unimplemented.

### Bundled code with licenses and links to the originals.
* SSD1306 driver is bundled from official MicroPython repository, licensed under MIT by Damien P. George. [link](https://github.com/micropython/micropython/blob/bb3412291a0f88cb958852b268d5dc43db23d4fb/drivers/display/ssd1306.py)
* urequests is bundled from micropython-lib repository, licensed under MIT by Paul Sokolovsky. [link](https://github.com/micropython/micropython-lib/blob/2e834672aa97856398835199ff786ad94ae247b4/urequests/urequests.py)
* sdcard driver is bundled from official MicroPython repository, licensed under MIT by Damien P. George. [link](https://github.com/micropython/micropython/blob/55f33240f3d7051d4213629e92437a36f1fac50e/drivers/sdcard/sdcard.py)
* LIS3DH driver is bundled from Adafruit's Circuit Python driver, licensed under MIT by Tony DiCola. [link](https://github.com/adafruit/Adafruit_CircuitPython_LIS3DH/blob/dd5d11c7aff0706efa12fae8028a1a418cf31f03/adafruit_lis3dh/lis3dh.py)
* adafruit_bus_device/i2c_device.py file is bundled from Adafruit's CircuitPython BusDevice repository, licensed under MIT by Scott Shawcroft for Adafruit Industries. [link](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice/blob/6a20bf8383fac55c75b8ba444ca4f83351b615a9/adafruit_bus_device/i2c_device.py)
    * All modifications can be found under i2c_device_modified.patch
    * Modifications remove circuitpython related code and makes the library work under standard micropython
