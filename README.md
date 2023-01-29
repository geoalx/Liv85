# Liv85 Project
A complete system based on Intel 8085 CPU that is focused on learning and for basic understanding of the digital systems. This project includes an EEPROM assembler and writer written in Python 3 and a Raspberry Pi pico is also used in order to write the machine code into the EEPROM.

[![built with Python3](https://img.shields.io/badge/built%20with-Python3-red.svg)](https://www.python.org/) [![built with Raspberry Pi Pico](https://img.shields.io/badge/built%20with-Raspberry%20Pi%20Pico-blue)](https://www.raspberrypi.org/products/raspberry-pi-pico/) [![built with Intel 8085](https://img.shields.io/badge/built%20with-Intel%208085-orange)](https://el.wikipedia.org/wiki/Intel_8085)

<a href="https://www.buymeacoffee.com/geoalx" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

## ASSEMBLER

  The assembler supports code written using 8085 (all versions) instruction set in a ```.asm``` file. Then, with the following instruction:
```
python3 start.py (YOUR_FILE).asm
```
a ```.txt``` file is produced with the same name as the input file. This file contains machine code written in the following format:
```
000F:e6
0010:1
0011:fe
0012:1
0013:ca
```
which later can be used by the EEPROM writer.

  Because this is the first release so it is absolutely not a finished project, some compromises must be made. So in order for the assembler to work the following instructions
must be taken into consideration:
- All the instructions with 1 parameter must have an ONLY 1 SPACE distance from the instruction as the following example.
```
CPI 03H
```
- All the instructions with 2 parameters must have an ONLY 1 SPACE distance from the instruction and NO DISTANCE from the comma as the following example
```
MOV A,B
```
- The programm is stored using the ```0000H``` as starting address.To change that you should add ```.ORG``` to your code and the target address.This function works like the following example.

```
.ORG 0800H ;From this point data is stored after 0800H address.
```

The critical improvements that will be implemented and added soon in the script is the following:
- [x] Comment Support.
- [x] Automated Interrupt and Vector Address handling.
- [ ] Better User Interaction.

## WRITER

![writer](/WRITER/sch_img.png)

The EEPROM model that is beeing used for this project is **Atmel AT28C16**.

Software required for the writer is [Thonny](https://thonny.org/) and also python rshell.
  
For running the writer script at first you should have the ```.txt``` file with machine code (as mentioned above) in the same directory with the script. After that you should
make a virtual environment in python. You can make this by running the following script in your directory:
```
python3 -m venv (YOUR_ENVIRONMENT_NAME)
```

Then you must activate scripts with the following command:
```
(YOUR_ENVIRONMENT_NAME)\Scripts\activate
```

After that operation the **rshell** must be installed with this command:
```
pip install rshell
```

With rshell installed you now connect the raspberry pi pico and run the following command:
```
rshell -p COM9 --buffer-size 512
```
Notice that there is a chance that the ```COM9``` port must be a different port on your machine.

After the connection is established you must copy the ```.txt``` file in the raspberry pi pico with the name ```ask.txt``` (you must use exactly that name).
You can do that with the following command:
```
cp (YOUR_FILE).txt /pyboard/ask.txt
```

After that you can connect the EEPROM to the pico as show in the schematic and run ```writer.py``` script using Thonny. Further instructions can be seen [here](https://www.youtube.com/watch?v=_ouzuI_ZPLs).

**In a future release there will be an automated shell script for Linux that automates all the above process.**

## 8085-SYSTEM

The given 8085 based system is a proof of concept of the power of the 8-bit electronics. At this time the system supports 8 leds for output, 8 dip-switches for input, an LCD display and a arduino driven keyboard (which is currently using the keyboard of the external PC but a PS/2 style keyboard will be added in the near future).

The parts of the current system is the following:
- 1xIntel 8085AH CPU
- 1xAtmel AT28C16 EEPROM
- 1xHitachi HM62256ALP DRAM
- 8xLEDs
- 1x8port dip switch
- 6x 74ls373 8bit octal latch
- 3x 74hc32 4 2-input OR gates
- 3x 73ls08 4 2-input AND gates
- 1x 74hc154 4 to 16 MUX
- 1x 74ls00 4 2-input NAND gates
- 1x 74ls04 hex inverter
- 1x 2 line LCD display (2x16)
- 22x 330Ω Resistors
- 1x 10K linear variable resistor
- Custom Arduino script that sends the keyboard data (included in the ```SYSTEM``` folder)

A (really messy :cry:) prototype of this project made with breadboards is presented below:
![prototype](/SYSTEM/PROTOTYPE.jpg)
(dip switches have been removed from the prototype due to a small technical issue but can the connections can be found in the detailed schematic in ```SYSTEM``` folder)

Example codes running on this prototype system and also a very early version of an OS I am building can be shown in the ```CODES``` folder.

A basic schematic of this system can be seen below and it is also attached to the ```SCHMATICS``` folder along with the ***gerber files for the eeprop programmer pcb and the PC pcb***

![pc schematic](/SCHEMATICS/Schematic_8085_2022-10-12.png)


***This project is actively updating and all of this information is not necessary will be included in a future release***
