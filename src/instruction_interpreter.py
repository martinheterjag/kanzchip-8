# Copyright authors of kanzchip-8, licenced under MIT licence

from log import logger


class InstructionInterpreter:
    def __init__(self):
        # Allocate memory for all registers
        self.reg_v = [0] * 16     # Vx where x is 0-15, 8.bit registers
        self.reg_i = 0            # 16-bit register
        self.reg_delay = 0        # 8-bit timer
        self.reg_sound = 0        # 8-bit timer
        self.program_counter = 0  # 16-bit PC
        self.stack = [0] * 16     # 16-bit array
        self.stack_pointer = 0    # 8-bit
        logger.info("Registers initialized")

        # 0x000 - 0xFFF (4095). 0x000-0x1FF is reserved.
        # Most programs start at 0x200
        self.memory = bytearray(4096)

    def incr_pc(self):
        self.program_counter = self.program_counter + 1
        # Emulate 16 bit register rollover
        if self.program_counter > 0xFFFF:
            logger.warning("program counter rollover")
            self.program_counter = 0
