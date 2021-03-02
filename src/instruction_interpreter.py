# Copyright authors of kanzchip-8, licenced under MIT licence

from src.log import logger

FONTS = (
    0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
    0x20, 0x60, 0x20, 0x20, 0x70,  # 1
    0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
    0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
    0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
    0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
    0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
    0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
    0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
    0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
    0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
    0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
    0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
    0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
    0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
    0xF0, 0x80, 0xF0, 0x80, 0x80   # F
)


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

        # Memory is 0x000 - 0xFFF (4095). 0x000-0x1FF is reserved.
        # Most programs start at 0x200
        self.memory = bytearray(4096)

        for i, byte in enumerate(FONTS):
            self.memory[i] = byte
        logger.info("Fonts loaded in memory")

        # TODO: Decide if this should be a setting or not?
        self.CHIP_48 = False

        self.screen = screen
        logger.info("InstructionInterpreter initialized")

    def load_rom(self, filename):
        rom = open(filename, 'rb').read()
        for i, val in enumerate(rom):
            self.memory[0x200 + i] = val
        self.program_counter = 0x200

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

    def jump(self, instruction):
        """
        1nnn - JP addr
        Jump to location nnn.

        The interpreter sets the program counter to nnn.
        """
        self.program_counter = instruction & 0x0FFF

    def set_vx_to_kk(self, instruction):
        """
        6xkk - LD Vx, byte
        Set Vx = kk.

        The interpreter puts the value kk into register Vx.
        """
        x = (instruction & 0x0F00) >> 8
        kk = instruction & 0x00FF
        self.reg_v[x] = kk

    def add_kk_to_vx(self, instruction):
        """
        7xkk - ADD Vx, byte
        Set Vx = Vx + kk.

        Adds the value kk to the value of register Vx, then stores the result in Vx.
        """
        x = (instruction & 0x0F00) >> 8
        kk = instruction & 0x00FF
        self.reg_v[x] = (self.reg_v[x] + kk) & 0x00FF  # discard extra bits

    def interpret_group_8(self, instruction):
        # Logic and arithmetic operations between Vx and Vy
        x = (instruction & 0x0F00) >> 8
        y = (instruction & 0x00F0) >> 4
        last_nibble = instruction & 0x000F

        logger.debug(f"instruction:{instruction:X} x:{x:X}(0x{self.reg_v[x]:X})"
                     f" y:{y:X}(0x{self.reg_v[y]:X})")
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
            if self.reg_v[x] <= self.reg_v[y]:
                tmp = self.reg_v[x] - self.reg_v[y]
                self.reg_v[x] = 0x100 + tmp  # + since tmp is negative
                self.reg_v[0xF] = 0
            else:
                self.reg_v[x] = self.reg_v[x] - self.reg_v[y]
                self.reg_v[0xF] = 1
        elif last_nibble == 0x6:  # SHR Vx {, Vy}
            # Vf shall be set to same value as the bit that is shifted out
            if self.CHIP_48:
                self.reg_v[x] = self.reg_v[y]
            self.reg_v[0xF] = self.reg_v[x] & 0x0001
            self.reg_v[x] = self.reg_v[x] >> 1
        elif last_nibble == 0x7:  # SUBN Vx, Vy
            if self.reg_v[y] <= self.reg_v[x]:
                logger.info("WTF?")
                tmp = self.reg_v[y] - self.reg_v[x]
                self.reg_v[x] = 0x100 + tmp
                self.reg_v[0xF] = 0
            else:
                self.reg_v[x] = self.reg_v[y] - self.reg_v[x]
                self.reg_v[0xF] = 1
        elif last_nibble == 0xE:  # SHL Vx {, Vy}
            # Vf shall be set to same value as the bit that is shifted out
            if self.CHIP_48:
                self.reg_v[x] = self.reg_v[y]
            self.reg_v[0xF] = self.reg_v[x] & 0x8000
            self.reg_v[x] = self.reg_v[x] << 1
        else:
            logger.warning(f"OpCode {instruction:X} supported ")

    def set_index_to_nnn(self, instruction):
        """
        Annn - LD I, addr
        Set I = nnn.

        The value of register I is set to nnn.
        """
        nnn = instruction & 0x0FFF
        self.reg_i = nnn

    def interpret_instruction(self, instruction):
        if instruction < 0x00:
            logger.error(f"Trying to pass a negative value {instruction:X} as instruction")
            return

        if instruction > 0xFFFF:
            logger.warning(f"Instruction {instruction:X} bigger than 8 bit, using {instruction % 0x10000:X}")
            instruction %= 0x10000

        if instruction & 0xF000 == 0x0000:
            # Group 0 CLS, RET, SYS
            self.interpret_group_0(instruction)
        elif instruction & 0xF000 == 0x1000:
            # JP
            self.jump(instruction)
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
            self.set_vx_to_kk(instruction)
        elif instruction & 0xF000 == 0x7000:
            # ADD (Vx, Byte)
            self.add_kk_to_vx(instruction)
        elif instruction & 0xF000 == 0x8000:
            # Arithmetic (Vx + Vy, Vx xor Vy etc.)
            self.interpret_group_8(instruction)
        elif instruction & 0xF000 == 0x9000:
            # SNE
            logger.warning(f"OpCode {instruction:X} not yet supported ")
        elif instruction & 0xF000 == 0xA000:
            # LD (Vx, Vy)
            self.set_index_to_nnn(instruction)
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
