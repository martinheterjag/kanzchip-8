# Copyright authors of kanzchip-8, licenced under MIT licence

import time
from log import logger
from screen import Screen
from memory import Memory

VERSION = "0.0.1"


def main():
    logger.info("kanzchip-8, chip-8 emulator version " + VERSION + "-")
    screen = Screen()
    memory = Memory()
    # TODO: Replace test code below
    logger.debug("V4 is set to: 0x{:X}".format(memory.get_vx(4)))
    memory.set_vx(4, 0xFF)
    logger.debug("V4 is set to: 0x{:X}".format(memory.get_vx(4)))

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
            screen.clear_all()
            count = 0
    # TODO: Test code ends here


if __name__ == "__main__":
    main()
