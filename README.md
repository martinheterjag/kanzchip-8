# kanzchip-8

kanzchip-8 is a python based CHIP-8 emulator made by Chris Stewart and
Martin Eriksson

https://github.com/cstewart90

https://github.com/martinheterjag

# What is CHIP-8?

Snipped from wikipedia:
>"CHIP-8 is an interpreted programming language, developed by Joseph Weisbecker. It was initially used on the COSMAC VIP and Telmac 1800 8-bit microcomputers in the mid-1970s. CHIP-8 programs are run on a CHIP-8 virtual machine. It was made to allow video games to be more easily programmed for these computers."

CHIP-8 has 35 instructions that are all two bytes long. We have implemented the instructions based on [Cowgod's Chip-8 technical reference](http://devernay.free.fr/hacks/chip8/C8TECH10.HTM).

# How to run kanzchip-8

From the root folder of the repository, run `python -m src`. To run unit tests run `python -m unit-test`. To run with debug logs run `python -m src -d`

## Dependencies

kanzchip-8 was developed with Python 3.9 and pygame, run `pip install -r requirements.txt` to install all modules needed to run the emulator.

## Menu bar

The menu bar holds functions to load a ROM file, reset the currently playing ROM, set CPU rate, sound volume as well as setting shift quirks on or off, which affects how the bit-shift instructions are working.
