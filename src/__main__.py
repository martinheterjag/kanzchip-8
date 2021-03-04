# Copyright authors of kanzchip-8, licenced under MIT licence

import tkinter as tk
from tkinter import filedialog

import pygame

from src.instruction_interpreter import InstructionInterpreter
from src.log import logger
from src.screen import Screen
from src.sound import Sound
from src.hex_keyboard import HexKeyboard

VERSION = "0.0.1"


# TODO: should probably be done form a menu instead of startup
def open_rom_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(initialdir="roms",
                                      filetypes=(("ROM", "*.ch8"),
                                                 ("All files", "*"),))


def main():
    logger.info(f"--- kanzchip-8, chip-8 emulator version {VERSION} ---")
    rom = open_rom_file()
    if rom == "":
        logger.info("No rom selected!")
        logger.info("Exiting")
        return

    logger.info(f"Loaded ROM-file {rom}")
    screen = Screen()
    keyboard = HexKeyboard()
    sound = Sound()
    clock = pygame.time.Clock()

    ii = InstructionInterpreter(screen, keyboard)
    ii.load_rom(rom)

    pygame.display.set_caption(rom.split("/")[-1].removesuffix(".ch8"))

    while True:
        screen.spin()
        clock.tick(60)  # run at 60 fps

        # Timer and sound registers shall decrement if not 0 at a rate of 60 Hz
        if ii.reg_delay > 0:
            ii.reg_delay -= 1
        if ii.reg_sound > 0:
            sound.buzzer_on()
            ii.reg_sound -= 1
            if ii.reg_sound == 0:
                sound.buzzer_off()

        # Run 10 instructions per frame to simulate 600hz
        # Most CHIP-8 interpreters ran at about 500-1000hz,
        # Could make this configurable
        for tick in range(10):
            instruction = ii.next_instruction()
            ii.interpret_instruction(instruction)


if __name__ == "__main__":
    main()
