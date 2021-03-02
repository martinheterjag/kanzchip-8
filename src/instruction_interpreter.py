# Copyright authors of kanzchip-8, licenced under MIT licence

from src.log import logger


class InstructionInterpreter:
    def __init__(self, screen):
        # Allocate memory for all registers
        self.reg_v = [0] * 16     # Vx where x is 0-15, 8.bit registers
        self.reg_i = 0            # 16-bit register
        self.reg_delay = 0        # 8-bit timer
        self.reg_sound = 0        # 8-bit timer
        self.program_counter = 0  # 16-bit PC
        self.stack = [0] * 16     # 16-bit array
        self.stack_pointer = 0    # 8-bit

        # 0x000 - 0xFFF (4095). 0x000-0x1FF is reserved.
        # Most programs start at 0x200
        self.memory = bytearray(4096)

        # TODO: Decide if this should be a setting or not?
        self.CHIP_48 = False

        self.screen = screen
        logger.info("InstructionInterpreter initialized")

    def incr_pc(self):
        self.program_counter += 2
        # Emulate 16 bit register rollover
        if self.program_counter > 0xFFFF:
            logger.warning("program counter rollover")
            self.program_counter = 0

    def interpret_group_0(self, instruction):
        # 00E0 and 00EE, rest can be ignored.
        if instruction == 0x00E0:  # CLS
            self.screen.clear_all()
        elif instruction == 0x00EE:  # RET
            self.program_counter = self.stack[self.stack_pointer]
            self.stack_pointer -= 1
        else:
            logger.warning(f"OpCode {instruction:X} not supported!")

    def interpret_group_8(self, instruction):
        # Logic and arithmetic operations between Vx and Vy
        x = (instruction & 0x0F00) >> 8
        y = (instruction & 0x00F0) >> 4
        last_nibble = instruction & 0x000F

        logger.debug(f"instruction:{instruction:X} x:{x:X} y:{y:X}")
        if last_nibble == 0x0:  # LD Vx, Vy
            self.reg_v[x] = self.reg_v[y]
        elif last_nibble == 0x1:  # OR Vx, Vy
            self.reg_v[x] = self.reg_v[x] | self.reg_v[y]
        elif last_nibble == 0x2:  # AND Vx, Vy
            self.reg_v[x] = self.reg_v[x] & self.reg_v[y]
        elif last_nibble == 0x3:  # XOR Vx, Vy
            self.reg_v[x] = self.reg_v[x] ^ self.reg_v[y]
        elif last_nibble == 0x4:  # ADD Vx, Vy
            # Vf is used as carry
            if self.reg_v[x] + self.reg_v[y] > 0xFF:
                self.reg_v[0xF] = 1
            else:
                self.reg_v[0xF] = 0
            self.reg_v[x] = (self.reg_v[x] + self.reg_v[y]) % 0x100
        elif last_nibble == 0x5:  # SUB Vx, Vy
            # If negative, wrap around and set Vf as carry
            if self.reg_v[x] > self.reg_v[y]:
                tmp = self.reg_v[x] - self.reg_v[y]
                self.reg_v[x] = 0x100 - tmp
                self.reg_v[0xF] = 1
            else:
                self.reg_v[x] = self.reg_v[x] - self.reg_v[y]
                self.reg_v[0xF] = 0
        elif last_nibble == 0x6:  # SHR Vx {, Vy}
            # Vf shall be set to same value as the bit that is shifted out
            if self.CHIP_48:
                self.reg_v[x] = self.reg_v[y]
            self.reg_v[0xF] = self.reg_v[x] & 0x0001
            self.reg_v[x] = self.reg_v[x] >> 1
        elif last_nibble == 0x7:  # SUBN Vx, Vy
            # If negative, wrap around and set Vf as carry
            if self.reg_v[y] > self.reg_v[x]:
                tmp = self.reg_v[y] - self.reg_v[x]
                self.reg_v[x] = 0x100 - tmp
                self.reg_v[0xF] = 1
            else:
                self.reg_v[x] = self.reg_v[y] - self.reg_v[x]
                self.reg_v[0xF] = 0
        elif last_nibble == 0xE:  # SHL Vx {, Vy}
            # Vf shall be set to same value as the bit that is shifted out
            if self.CHIP_48:
                self.reg_v[x] = self.reg_v[y]
            self.reg_v[0xF] = self.reg_v[x] & 0x8000
            self.reg_v[x] = self.reg_v[x] << 1
        else:
            logger.warning(f"OpCode {instruction:X} supported ")

    def interpret_instruction(self, instruction):
        if instruction < 0x00:
            logger.error(f"Trying to pass a negative value {instruction:X} as instuction")
            return

        if instruction > 0xFFFF:
            logger.warning(f"Instruction {instruction:X} bigger than 8 bit, using {instruction % 0x10000:X}")
            instruction %= 0x10000

        if instruction & 0xF000 == 0x0000:
            # Group 0 CLS, RET, SYS
            self.interpret_group_0(instruction)
        elif instruction & 0xF000 == 0x1000:
            # JP
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x2000:
            # CALL
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x3000:
            # SE
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x4000:
            # SNE
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x5000:
            # SE
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x6000:
            # LD (Vx, Byte)
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x7000:
            # ADD (Vx, Byte)
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0x8000:
            # Arithmetic (Vx + Vy, Vx xor Vy etc.)
            self.interpret_group_8(instruction)
        elif instruction & 0xF000 == 0x9000:
            # SNE
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xA000:
            # LD (Vx, Vy)
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xB000:
            # JP V0
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xC000:
            # RND
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xD000:
            # DRW
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xE000:
            # SKP, SKNP
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xF000:
            # A lot of different LD variants + ADD (I, Vx)
            logger.warning(f"OpCode {instruction:X} not yet supported ")
