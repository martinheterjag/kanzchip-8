# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence

import pygame

from src.log import logger


class Screen:
    def __init__(self) -> None:
        pygame.init()
        self.PIXEL_SIZE = 20
        self.MENU_HEIGHT = 40
        self.WIDTH = 64 * self.PIXEL_SIZE
        self.HEIGHT = 32 * self.PIXEL_SIZE
        self.TOTAL_HEIGHT = self.HEIGHT + self.MENU_HEIGHT
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.TOTAL_HEIGHT), 0, 1)

        self.WHITE: tuple[int, int, int] = (230, 230, 230)
        self.BLACK: tuple[int, int, int] = (20, 20, 20)

        self.pixel_matrix: list[list[int]] = [[0] * 32 for _ in range(64)]

        self.paused = False
        logger.info("Screen initialized")

    # Run spin in main loop to check for pygame events and update screen
    def spin(self) -> None:
        # Redraw screen
        for y in range(32):
            for x in range(64):
                if self.pixel_matrix[x][y] == 1:
                    self.draw_pixel(x, y, self.WHITE)
                else:
                    self.draw_pixel(x, y, self.BLACK)
        pygame.display.update()

    def get_pixel_state(self, x: int, y: int) -> bool:
        return self.pixel_matrix[x][y] == 1

    def draw_pixel(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        x = x * self.PIXEL_SIZE
        y = y * self.PIXEL_SIZE + self.MENU_HEIGHT  # Offset to fit menu bar
        pygame.draw.rect(self.DISPLAY, color,
                         (x, y, self.PIXEL_SIZE, self.PIXEL_SIZE))

    def set_pixel(self, x: int, y: int) -> None:
        self.pixel_matrix[x][y] = 1

    def clear_pixel(self, x: int, y: int) -> None:
        self.pixel_matrix[x][y] = 0

    def clear_all(self) -> None:
        for x in range(64):
            for y in range(32):
                self.clear_pixel(x, y)
