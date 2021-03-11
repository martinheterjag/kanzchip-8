# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence

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
    ticks_per_frame = 10

    def reset_rom():
        screen.clear_all()
        ii.reset()

    def open_rom_file(filename=""):
        if filename == "":
            root = tk.Tk()
            root.withdraw()
            rom = filedialog.askopenfilename(initialdir="roms",
                                             filetypes=(("ROM", "*.ch8"),
                                                        ("All files", "*"),))
        else:
            rom = filename

        if rom == "":
            logger.info("No rom selected!")
            logger.info("Exiting")
            quit()
        ii.load_rom(rom)
        nonlocal title
        title = rom.split("/")[-1].removesuffix(".ch8")
        logger.info(f"Loaded ROM-file {rom}")
        reset_rom()

    def set_cpu_rate(selected_value, hz):
        nonlocal ticks_per_frame
        ticks_per_frame = hz//60
        logger.info(f"selected: {selected_value}, hz: {hz},"
                    f"ticks_per_frame: {ticks_per_frame}")

    screen = Screen()
    keyboard = HexKeyboard()
    sound = Sound()

    ii = InstructionInterpreter(screen, keyboard)
    open_rom_file(filename="roms/BC_test.ch8")

    theme = pygame_menu.themes.Theme(background_color=(70, 30, 20),
                                     title_background_color=(50, 30, 20),
                                     widget_font=pygame_menu.font.FONT_DIGITAL,
                                     title_font_size=1,
                                     widget_font_size=14)
    menu = pygame_menu.Menu(height=screen.MENU_HEIGHT, width=screen.DISPLAY.get_width(),
                            title='',
                            theme=theme,
                            joystick_enabled=False,
                            keyboard_enabled=False,
                            position=(0, 0),
                            columns=3,
                            column_min_width=(210, 400, 200),
                            rows=1,
                            mouse_motion_selection=True
                            )
    menu.add.button('Reset ROM', reset_rom)
    menu.add.button('Load ROM', open_rom_file)
    menu.add.selector('CPU :', [(' 600Hz', 600),
                                (' 900hz', 900),
                                ('1200Hz', 1200),
                                ('6000Hz', 6000)],
                      onchange=set_cpu_rate, align=pygame_menu.locals.ALIGN_LEFT)

    logger.info(f"Running main loop")
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # run at 60 fps
        menu.mainloop(screen.DISPLAY, bgfun=None, clear_surface=False, disable_loop=True, fps_limit=0)

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
        for tick in range(ticks_per_frame):
            instruction = ii.next_instruction()
            ii.interpret_instruction(instruction)

        fps = format(clock.get_fps(), ".1f")
        pygame.display.set_caption(f"{title}     FPS: {fps}")
        screen.spin()


if __name__ == "__main__":
    main()
