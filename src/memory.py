# Copyright authors of kanzchip-8, licenced under MIT licence

from log import logger


class Memory:
    def __init__(self):
        # Allocate memory for all registers
        self.reg_v = [0] * 16     # Vx where x is 0-15, 8.bit registers
        self.reg_i = 0            # 16-bit register
        self.reg_vf = 0           # Flag register can be 1 or 0
        self.reg_delay = 0        # 8-bit timer
        self.reg_sound = 0        # 8-bit timer
        self.program_counter = 0  # 16-bit PC
        self.stack = [0] * 16     # 16-bit array
        self.stack_pointer = 0    # 8-bit
        logger.info("Registers initialized")

    def is_16_bit(self, value):
        return 0 < value < 0x10000

    def is_8_bit(self, value):
        print("value {}".format((0 < value < 0x100)))
        return 0 < value < 0x100

    def set_vx(self, vx, value):
        assert self.is_8_bit(value)
        self.reg_v[vx] = value

    def get_vx(self, vx):
        return self.reg_v[vx]

    def set_i(self, value):
        assert self.is_16_bit(value)
        self.reg_i = value

    def get_i(self):
        return self.reg_i

    def set_vf(self, flag):
        assert flag == 0 or flag == 1
        self.reg_vf = flag

    def get_pc(self):
        return self.program_counter

    def set_pc(self, value):
        assert self.is_16_bit(value)
        self.program_counter = value

    def incr_pc(self):
        self.program_counter = self.program_counter + 1
        # Emulate 16 bit register rollover
        if self.program_counter > 0xFFFF:
            logger.warning("program counter rollover")
            self.program_counter = 0
