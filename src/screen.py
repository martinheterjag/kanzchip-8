# Copyright authors of kanzchip-8, licenced under MIT licence

import sys

import pygame
from pygame.locals import *

from src.log import logger


class Screen:
    def __init__(self):
        pygame.init()
        self.PIXEL_SIZE = 20
        self.MENU_HEIGHT = 40
        self.WIDTH = 64 * self.PIXEL_SIZE
        self.HEIGHT = 32 * self.PIXEL_SIZE
        self.TOTAL_HEIGHT = self.HEIGHT + self.MENU_HEIGHT
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.TOTAL_HEIGHT), 0, 1)

        self.WHITE = (230, 230, 230)
        self.BLACK = (20, 20, 20)

        self.paused = False

        self.pixel_matrix = [[False] * 32 for i in range(64)]

        logger.info("Screen initialized")

    # Run spin in main loop to check for pygame events and update screen
    def spin(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
        # Redraw screen
        for y in range(32):
            for x in range(64):
                if self.pixel_matrix[x][y] == True:
                    self.draw_pixel(x, y, self.WHITE)
                else:
                    self.draw_pixel(x, y, self.BLACK)
        pygame.display.update()

    def get_pixel_state(self, x, y):
        return self.pixel_matrix[x][y]

    def draw_pixel(self, x, y, color):
        x = x * self.PIXEL_SIZE
        y = y * self.PIXEL_SIZE + self.MENU_HEIGHT  # Offset to fit menu bar
        pygame.draw.rect(self.DISPLAY, color,
                         (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))

    def set_pixel(self, x, y):
        self.pixel_matrix[x][y] = True


    def clear_pixel(self, x, y):
        self.pixel_matrix[x][y] = False

    def clear_all(self):
        for x in range(64):
            for y in range(32):
                self.clear_pixel(x, y)
