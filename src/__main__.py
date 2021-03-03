# Copyright authors of kanzchip-8, licenced under MIT licence

import pygame

from src.instruction_interpreter import InstructionInterpreter
from src.log import logger
from src.screen import Screen

VERSION = "0.0.1"
ROM = "roms/IBM Logo.ch8"  # temporary


def main():
    logger.info(f"--- kanzchip-8, chip-8 emulator version {VERSION} ---")
    screen = Screen()
    clock = pygame.time.Clock()

    ii = InstructionInterpreter(screen)
    ii.load_rom(ROM)

    pygame.display.set_caption(ROM.split("/")[-1].removesuffix(".ch8"))

    while True:
        screen.spin()
        clock.tick(60)  # run at 60 fps

        # Run 10 instructions per frame to simulate 600hz
        # Most CHIP-8 interpreters ran at about 500-1000hz,
        # Could make this configurable
        for tick in range(10):
            instruction = ii.next_instruction()
            ii.interpret_instruction(instruction)


if __name__ == "__main__":
    main()
