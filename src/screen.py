# Copyright authors of kanzchip-8, licenced under MIT licence

import sys

import pygame
from pygame.locals import *

from src.log import logger


class Screen:
    def __init__(self):
        pygame.init()
        self.PIXEL_SIZE = 20
        self.WIDTH = 64 * self.PIXEL_SIZE
        self.HEIGHT = 32 * self.PIXEL_SIZE
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 1)

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

    def get_pixel_state(self, x, y):
        x = x * self.PIXEL_SIZE
        y = y * self.PIXEL_SIZE
        pixel = self.DISPLAY.get_at((x, y))
        return pixel == self.WHITE

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
