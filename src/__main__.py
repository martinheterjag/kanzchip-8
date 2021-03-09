# Copyright authors of kanzchip-8, licenced under MIT licence

import tkinter as tk
from tkinter import filedialog

import pygame
import pygame_menu

from src.instruction_interpreter import InstructionInterpreter
from src.log import logger
from src.screen import Screen
from src.sound import Sound
from src.hex_keyboard import HexKeyboard

VERSION = "0.0.1"


def main():
    logger.info(f"--- kanzchip-8, chip-8 emulator version {VERSION} ---")
    title = ""
    def reset_rom(instruction_interpreter, screen):
        screen.clear_all()
        instruction_interpreter.reset()

    def open_rom_file(instruction_interpreter, screen):
        root = tk.Tk()
        root.withdraw()
        rom = filedialog.askopenfilename(initialdir="roms",
                                         filetypes=(("ROM", "*.ch8"),
                                                    ("All files", "*"),))
        if rom == "":
            logger.info("No rom selected!")
            logger.info("Exiting")
            quit()
        instruction_interpreter.load_rom(rom)
        nonlocal title
        title = rom.split("/")[-1].removesuffix(".ch8")
        logger.info(f"Loaded ROM-file {rom}")
        reset_rom(instruction_interpreter, screen)

    def set_cpu_rate(value, difficulty):
        print("Setting not implemented")

    screen = Screen()
    keyboard = HexKeyboard()
    sound = Sound()

    ii = InstructionInterpreter(screen, keyboard)
    open_rom_file(ii, screen)

    theme = pygame_menu.themes.Theme(background_color=(70,30,20),
                                     title_background_color=(50,30,20),
                                     widget_font=pygame_menu.font.FONT_DIGITAL,
                                     title_font_size=1,
                                     widget_font_size=14)
    menu = pygame_menu.Menu(screen.MENU_HEIGHT, screen.DISPLAY.get_width(), '',
                           theme=theme,
                           joystick_enabled=False,
                           keyboard_enabled=False,
                           position=(0,0),
                           columns=5,
                           rows=1,
                           mouse_motion_selection=True
                           )

    menu.add_button('Reset ROM', reset_rom, ii, screen)
    menu.add_button('Load ROM', open_rom_file, ii, screen)
    menu.add.selector('CPU :', [('600Hz', 600),
                                ('1200Hz', 1200),
                                ('6000Hz', 6000)], onchange=set_cpu_rate)

    logger.info(f"Running main loop")
    clock = pygame.time.Clock()
    while True:
        menu.mainloop(screen.DISPLAY, bgfun=None, clear_surface=False, disable_loop=True)
        screen.spin()
        clock.tick(60)  # run at 60 fps

        if screen.paused:
            pygame.display.set_caption(f"{title}     PAUSED")
            screen.spin()
            continue

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

        fps = format(clock.get_fps(), ".1f")
        pygame.display.set_caption(f"{title}     FPS: {fps}")
        screen.spin()


if __name__ == "__main__":
    main()
