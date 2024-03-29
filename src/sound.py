# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence

import pygame

from src.log import logger


class Sound:
    def __init__(self) -> None:
        self.volume = 0.75
        pygame.mixer.init()
        square_wave = bytearray([128] * 400 + [0] * 400)
        self.sound = pygame.mixer.Sound(buffer=square_wave)
        self.sound.play(loops=-1)
        self.sound.set_volume(0.0)
        logger.info("Sound initialized")

    def buzzer_on(self) -> None:
        self.sound.set_volume(self.volume)

    def buzzer_off(self) -> None:
        self.sound.set_volume(0.0)
