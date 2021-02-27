# Copyright authors of kanzchip-8, licenced under MIT licence

import time
from log import logger
from screen import Screen

VERSION = "0.0.1"


if __name__ == "__main__":
    logger.info("kanzchip-8, chip-8 emulator version " + VERSION + "-")
    screen = Screen()
    # TODO: Replace test code below
    x = 0
    y = 0
    count = 0
    while(True):
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
