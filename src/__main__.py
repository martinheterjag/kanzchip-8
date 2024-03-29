# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence
import argparse
import logging
import sys
import tkinter as tk
from tkinter import filedialog

import pygame
import pygame_menu

from src import __version__
from src.hex_keyboard import HexKeyboard
from src.instruction_interpreter import InstructionInterpreter
from src.log import logger
from src.screen import Screen
from src.sound import Sound


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Set log severity to debug.")

    args = parser.parse_args()
    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.info(f"--- kanzchip-8, chip-8 emulator version {__version__} ---")

    title = ""
    ticks_per_frame = 10

    def reset_rom() -> None:
        screen.clear_all()
        ii.reset()

    def open_rom_file(filename: str = "") -> None:
        if filename == "":
            root = tk.Tk()
            root.withdraw()
            rom: str = filedialog.askopenfilename(
                initialdir="roms",
                filetypes=(("ROM", "*.ch8"), ("All files", "*"),)
            )
            root.destroy()
        else:
            rom = filename

        if rom == "":
            logger.info("No rom selected!")
            return
        ii.load_rom(rom)
        nonlocal title
        title = rom.split("/")[-1].removesuffix(".ch8")
        logger.info(f"Loaded ROM-file {rom}")
        reset_rom()

    def set_cpu_rate(selected_value: str, cpu_rate: int) -> None:
        nonlocal ticks_per_frame
        ticks_per_frame = cpu_rate // 60
        logger.debug(f"Selected option: {selected_value}, CPU rate: {cpu_rate} Hz, "
                     f"ticks per frame: {ticks_per_frame}")

    def set_volume(_: str, volume: float) -> None:
        sound.volume = volume

    def set_shift_quirks(selected_value: str, setting: bool) -> None:
        ii.shift_quirks = setting
        logger.debug(f"Selected shift_quirks: {selected_value}, {setting}")

    screen = Screen()
    keyboard = HexKeyboard()
    sound = Sound()

    ii = InstructionInterpreter(screen, keyboard)

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
                            columns=6,
                            column_min_width=(100, 100, 100, 100, 100, 100),
                            rows=1,
                            mouse_motion_selection=True
                            )
    menu.add.button('Reset ROM', reset_rom, align=pygame_menu.locals.ALIGN_CENTER)
    menu.add.button('Load ROM', open_rom_file, align=pygame_menu.locals.ALIGN_CENTER)
    menu.add.selector('CPU Rate :', [(' 600Hz', 600),
                                     (' 900hz', 900),
                                     ('1200Hz', 1200),
                                     ('6000Hz', 6000)],
                      onchange=set_cpu_rate, align=pygame_menu.locals.ALIGN_CENTER)
    menu.add.selector('Sound Volume :', [('Mute', 0.0),
                                         (' 25%', 0.25),
                                         (' 50%', 0.5),
                                         (' 75%', 0.75),
                                         ('100%', 1.0)],
                      onchange=set_volume, default=4,
                      align=pygame_menu.locals.ALIGN_CENTER)
    menu.add.selector('Shift Quirks :', [('Off', False),
                                         (' On', True)],
                      onchange=set_shift_quirks, default=0,
                      align=pygame_menu.locals.ALIGN_CENTER)

    logger.info("Running main loop")
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)  # run at 60 fps

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                screen.paused = not screen.paused

        if menu.is_enabled():
            menu.draw(screen.DISPLAY)
            menu.update(events)

        if screen.paused or not ii.rom_loaded:
            caption = "Load a rom" if not ii.rom_loaded else "PAUSED"
            pygame.display.set_caption(f"{title}     {caption}")
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
        for _ in range(ticks_per_frame):
            instruction = ii.next_instruction()
            ii.interpret_instruction(instruction)

        fps = format(clock.get_fps(), ".1f")
        pygame.display.set_caption(f"{title}     FPS: {fps}")
        screen.spin()


if __name__ == "__main__":
    main()
