# Copyright (C) 2021 authors of kanzchip-8, licenced under MIT licence

"""
The keyboard is mapped to fit the pattern of a querty keyboard

Mapping table:
Original Keyboard | Querty Keyboard
------------------+-------------------
1  2  3  C        | 1  2  3  4
4  5  6  D        | Q  W  E  R
7  8  9  E        | A  S  D  F
A  0  B  F        | Z  X  C  V
"""
import pygame

from src.log import logger


class HexKeyboard:
    def __init__(self):
        self.hex_pygame_key_map = {
            0x1: pygame.K_1,
            0x2: pygame.K_2,
            0x3: pygame.K_3,
            0xC: pygame.K_4,
            0x4: pygame.K_q,
            0x5: pygame.K_w,
            0x6: pygame.K_e,
            0xD: pygame.K_r,
            0x7: pygame.K_a,
            0x8: pygame.K_s,
            0x9: pygame.K_d,
            0xE: pygame.K_f,
            0xA: pygame.K_z,
            0x0: pygame.K_x,
            0xB: pygame.K_c,
            0xF: pygame.K_v,
        }
        logger.info("Keyboard Initialized")

    def is_pressed(self, hex_key):
        if hex_key > 0xF or hex_key < 0x0:
            logger.error(f"Invalid key {hex_key:X}")
            return False

        pygame_key = self.hex_pygame_key_map[hex_key]
        if pygame.key.get_pressed()[pygame_key]:
            return True
        else:
            return False
