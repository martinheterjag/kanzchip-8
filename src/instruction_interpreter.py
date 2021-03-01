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

        # 0x000 - 0xFFF (4095). 0x000-0x1FF is reserved.
        # Most programs start at 0x200
        self.memory = bytearray(4096)

        logger.info("InstructionInterpreter initialized")

    def incr_pc(self):
        self.program_counter = self.program_counter + 1
        # Emulate 16 bit register rollover
        if self.program_counter > 0xFFFF:
            logger.warning("program counter rollover")
            self.program_counter = 0

    def interpret_instruction(self, instruction):
        if instruction < 0x00:
            logger.error("Trying to pass a negative value {:X} as instuction"
                         .format(instruction))
            program_counter += 1
            return

        if instruction > 0xFFFF:
            logger.warning ("Instruction {:X} bigger than 8 bit, using {:X}"
                            .format(instruction, instruction % 0x10000))
            instruction %= 0x10000


        if instruction & 0xF000 == 0x0000:
            # CLS, RET, SYS
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x1000:
            # JP
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x2000:
            # CALL
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x3000:
            # SE
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x4000:
            # SNE
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x5000:
            # SE
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x6000:
            # LD (Vx, Byte)
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x7000:
            # ADD (Vx, Byte)
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x8000:
            # Arithmetic (Vx + Vy, Vx xor Vy etc.)
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0x9000:
            # SNE
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xA000:
            # LD (Vx, Vy)
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xB000:
            # JP V0
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xC000:
            # RND
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xD000:
            # DRW
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xE000:
            # SKP, SKNP
            logger.warning("OpCode {} not yet supported ".format(instruction))
        elif instruction & 0xF000 == 0xF000:
            # A lot of different LD variants + ADD (I, Vx)
            logger.warning("OpCode {} not yet supported ".format(instruction))

        # TODO: Should we step PC here or will it be messy when OpCode==CALL?
        program_counter += 1
