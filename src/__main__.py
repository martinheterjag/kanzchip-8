# Copyright authors of kanzchip-8, licenced under MIT licence

import time
from .log import logger
from .screen import Screen
from .instruction_interpreter import InstructionInterpreter

VERSION = "0.0.1"


def main():
    logger.info("kanzchip-8, chip-8 emulator version " + VERSION + "-")
    screen = Screen()
    ii = InstructionInterpreter(screen)
    # TODO: Replace test code below
    x = 0
    y = 0
    count = 0

    while True:
        screen.spin()
        time.sleep(0.01)
        screen.set_pixel(x, y)
        screen.clear_pixel(x + 2, y)
        x = x + 3
        y = y + 2
        if x > 64:
            x = 64 - x
        if y > 32:
            y = 32 - y
        count = count + 1
        if count == 1200:
            ii.interpret_instruction(0x00E0)
            count = 0
    # TODO: Test code ends here


if __name__ == "__main__":
    main()
