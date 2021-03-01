# Copyright authors of kanzchip-8, licenced under MIT licence

import pygame
import sys
from pygame.locals import *
from log import logger


class Screen:
    def __init__(self, flags=0):
        pygame.init()
        print("pygame.HIDDEN", pygame.HIDDEN)
        self.PIXEL_SIZE = 20
        self.WIDTH = 64 * self.PIXEL_SIZE
        self.HEIGHT = 32 * self.PIXEL_SIZE
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT), flags, 1)

        self.WHITE = (230, 230, 230)
        self.BLACK = (20, 20, 20)

        self.clear_all()
        logger.info("Screen initialized")

    # Run spin in main loop to check for pygame events and update screen
    def spin(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

    def set_pixel(self, x, y):
        x = x * self.PIXEL_SIZE
        y = y * self.PIXEL_SIZE
        pygame.draw.rect(self.DISPLAY, self.WHITE,
                         (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))

    def clear_pixel(self, x, y):
        x = x * self.PIXEL_SIZE
        y = y * self.PIXEL_SIZE
        pygame.draw.rect(self.DISPLAY, self.BLACK,
                         (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))

    def clear_all(self):
        self.DISPLAY.fill(self.BLACK)
