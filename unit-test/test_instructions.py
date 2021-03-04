import unittest
from unittest.mock import Mock, patch

from src.instruction_interpreter import InstructionInterpreter


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.screen = Mock()
        self.ii = InstructionInterpreter(self.screen)

    def test_next_instruction(self):
        self.ii.memory[0x200] = 0x00
        self.ii.memory[0x201] = 0xE0
        self.ii.program_counter = 0x200

        self.assertEqual(self.ii.next_instruction(), 0x00E0)
        self.assertEqual(self.ii.program_counter, 0x202)

    # Test is supposed to verify that 0x00E0 will clear the screen
    def test_00E0_clear_screen(self):
        self.ii.interpret_instruction(0x00E0)
        self.screen.clear_all.assert_called_once()

    # Test verifies that 0x00EE will set program_counter to address in stack the
    # pointer is pointing to, and that the pointer is decremented.
    def test_00EE_ret(self):
        self.ii.stack = [400, 500]
        self.ii.stack_pointer = 1
        self.ii.interpret_instruction(0x00EE)

        self.assertEqual(self.ii.stack_pointer, 0)
        self.assertEqual(self.ii.program_counter, 500)

    # Test that the program counter to set to the address in the last 3 nibbles
    def test_1nnn_jump(self):
        self.ii.interpret_instruction(0x11FF)
        self.assertEqual(self.ii.program_counter, 0x01FF)

        for instruction in range(0x1200, 0x2000):
            self.ii.interpret_instruction(instruction)
            jump = instruction & 0x0FFF
            self.assertEqual(self.ii.program_counter, jump)

    def test_2nnn_call(self):
        self.ii.stack_pointer = 0
        self.ii.program_counter = 0x500

        self.ii.interpret_instruction(0x2823)
        self.assertEqual(self.ii.stack[1], 0x0500)
        self.assertEqual(self.ii.stack_pointer, 1)
        self.assertEqual(self.ii.program_counter, 0x0823)

    def test_3xkk_x_equal_to_kk(self):
        self.ii.program_counter = 100
        self.ii.reg_v[0x1] = 0xBE
        self.ii.interpret_instruction(0x31BA)
        self.assertEqual(self.ii.program_counter, 100)
        self.ii.interpret_instruction(0x31BE)
        self.assertEqual(self.ii.program_counter, 102)

    def test_4xkk_x_not_equal_to_kk(self):
        self.ii.program_counter = 100
        self.ii.reg_v[0x1] = 0xBE
        self.ii.interpret_instruction(0x41BA)
        self.assertEqual(self.ii.program_counter, 102)
        self.ii.interpret_instruction(0x41BE)
        self.assertEqual(self.ii.program_counter, 102)

    def test_5xy0_skip_if_vx_equal_vy(self):
        self.ii.program_counter = 0x200
        self.ii.reg_v[0x1] = 0xBE
        self.ii.reg_v[0x2] = 0xBB
        self.ii.interpret_instruction(0x5120)
        self.assertEqual(self.ii.program_counter, 0x200)

        self.ii.reg_v[0x1] = 0xBB
        self.ii.interpret_instruction(0x5120)
        self.assertEqual(self.ii.program_counter, 0x202)

    def test_6xkk_set_vx_to_kk(self):
        self.ii.interpret_instruction(0x62F3)
        self.assertEqual(self.ii.reg_v[0x2], 0xF3)

        self.ii.interpret_instruction(0x6A12)
        self.assertEqual(self.ii.reg_v[0xA], 0x12)

    def test_7xkk_add_vx_to_kk(self):
        self.ii.reg_v[0xA] = 0x12
        self.ii.interpret_instruction(0x7A10)
        self.assertEqual(self.ii.reg_v[0xA], 0x22)

        self.ii.interpret_instruction(0x7AB1)
        self.assertEqual(self.ii.reg_v[0xA], 0xD3)

        # test overflow
        self.ii.reg_v[0x1] = 0xD3
        self.ii.interpret_instruction(0x7153)
        self.assertEqual(self.ii.reg_v[0x1], 0x26)

    # Test is supposed to verify that 8xy0 load ii.reg_v[y] into ii.reg_v[x]
    def test_8xy0_load_vx_vy(self):
        self.ii.reg_v[0x0] = 0x10
        self.ii.reg_v[0x1] = 0x11
        self.ii.reg_v[0xA] = 0x12
        # Load V1 == 0x11 into V0
        self.assertEqual(self.ii.reg_v[0x0], 0x10)
        self.ii.interpret_instruction(0x8010)
        self.assertEqual(self.ii.reg_v[0x0], 0x11)
        # Load VA == 0x12 into V1
        self.assertEqual(self.ii.reg_v[0x1], 0x11)
        self.ii.interpret_instruction(0x81A0)
        self.assertEqual(self.ii.reg_v[0xA], 0x12)

    def test_8xy1_or_vx_vy(self):
        self.ii.reg_v[0x2] = 0xF0
        self.ii.reg_v[0x3] = 0x0F
        self.ii.interpret_instruction(0x8231)
        self.assertEqual(self.ii.reg_v[0x2], 0xFF)

    def test_8xy2_and_vx_vy(self):
        self.ii.reg_v[0x4] = 0xF0
        self.ii.reg_v[0x5] = 0xAF
        self.ii.interpret_instruction(0x8452)
        self.assertEqual(self.ii.reg_v[0x4], 0xA0)

    def test_8xy3_xor_vx_vy(self):
        self.ii.reg_v[0x6] = 0xFF
        self.ii.reg_v[0x7] = 0xA5
        self.ii.interpret_instruction(0x8673)
        self.assertEqual(self.ii.reg_v[0x6], 0x5A)

    def test_8xy4_add_vx_vy_no_carry(self):
        self.ii.reg_v[0x8] = 0x11
        self.ii.reg_v[0x9] = 0x11
        self.ii.interpret_instruction(0x8894)
        self.assertEqual(self.ii.reg_v[0x8], 0x22)
        self.assertEqual(self.ii.reg_v[0xF], 0x00)

    def test_8xy4_add_vx_vy_with_carry(self):
        self.ii.reg_v[0xA] = 0xFF
        self.ii.reg_v[0xB] = 0x03
        self.ii.interpret_instruction(0x8AB4)
        self.assertEqual(self.ii.reg_v[0xA], 0x02)
        self.assertEqual(self.ii.reg_v[0xF], 0x01)

    def test_8xy5_sub_vx_vy_no_borrow(self):
        self.ii.reg_v[0xC] = 0x20
        self.ii.reg_v[0xD] = 0x10
        self.ii.interpret_instruction(0x8CD5)
        self.assertEqual(self.ii.reg_v[0xC], 0x10)
        self.assertEqual(self.ii.reg_v[0xF], 0x01)

    def test_8xy5_sub_vx_vy_with_borrow(self):
        self.ii.reg_v[0xE] = 0x00
        self.ii.reg_v[0x0] = 0x01
        self.ii.interpret_instruction(0x8E05)
        self.assertEqual(self.ii.reg_v[0xE], 0xFF)
        self.assertEqual(self.ii.reg_v[0xF], 0x00)

    def test_8xy6_shr_vx_vy_no_carry(self):
        self.ii.reg_v[0x0] = 0b01000000
        self.ii.interpret_instruction(0x8006)
        self.assertEqual(self.ii.reg_v[0x0], 0b00100000)
        self.assertEqual(self.ii.reg_v[0xF], 0x00)

    def test_8xy6_shr_vx_vy_with_carry(self):
        self.ii.reg_v[0x0] = 0b01000001
        self.ii.interpret_instruction(0x8006)
        self.assertEqual(self.ii.reg_v[0x0], 0b00100000)
        self.assertEqual(self.ii.reg_v[0xF], 0x01)

    def test_8xy7_subn_vx_vy_no_borrow(self):
        self.ii.reg_v[0xC] = 0x10
        self.ii.reg_v[0xD] = 0x20
        self.ii.interpret_instruction(0x8CD7)
        self.assertEqual(self.ii.reg_v[0xC], 0x10)
        self.assertEqual(self.ii.reg_v[0xF], 0x01)

    def test_8xy7_subn_vx_vy_with_borrow(self):
        self.ii.reg_v[0xE] = 0x01
        self.ii.reg_v[0x0] = 0x00
        self.ii.interpret_instruction(0x8E07)
        self.assertEqual(self.ii.reg_v[0xE], 0xFF)
        self.assertEqual(self.ii.reg_v[0xF], 0x00)

    def test_8xyE_shl_vx_vy_no_carry(self):
        self.ii.reg_v[0x0] = 0b01000000
        self.ii.interpret_instruction(0x800E)
        self.assertEqual(self.ii.reg_v[0x0], 0b10000000)
        self.assertEqual(self.ii.reg_v[0xF], 0x00)

    def test_8xyE_shl_vx_vy_with_carry(self):
        self.ii.reg_v[0x0] = 0b11000001
        self.ii.interpret_instruction(0x800E)
        self.assertEqual(self.ii.reg_v[0x0], 0b10000010)
        self.assertEqual(self.ii.reg_v[0xF], 0x01)

    def test_9xy0_skip_if_vx_not_equal_vy(self):
        self.ii.program_counter = 0x200
        self.ii.reg_v[0x1] = 0xBE
        self.ii.reg_v[0x2] = 0xBE
        self.ii.interpret_instruction(0x9120)
        self.assertEqual(self.ii.program_counter, 0x200)

        self.ii.reg_v[0x1] = 0xBB
        self.ii.interpret_instruction(0x9120)
        self.assertEqual(self.ii.program_counter, 0x202)

    def test_annn_set_i_to_nnn(self):
        self.ii.interpret_instruction(0xA120)
        self.assertEqual(self.ii.reg_i, 0x120)

        self.ii.interpret_instruction(0xAFBB)
        self.assertEqual(self.ii.reg_i, 0xFBB)

    def test_bnnn_jump_with_offset(self):
        self.ii.reg_v[0x0] = 0x50
        self.ii.interpret_instruction(0xB750)
        self.assertEqual(self.ii.program_counter, 0x7a0)

    @patch("random.randint", return_value=82)
    def test_cxkk_random(self, mocked_randint):
        self.ii.interpret_instruction(0xC318)
        self.assertEqual(self.ii.reg_v[0x3], 16)

        self.ii.interpret_instruction(0xC2EE)
        self.assertEqual(self.ii.reg_v[0x2], 66)

        mocked_randint.return_value = 221
        self.ii.interpret_instruction(0xC22F)
        self.assertEqual(self.ii.reg_v[0x2], 13)

    def test_fx07_set_delay_timer_to_vx(self):
        self.ii.reg_delay = 0x20
        self.ii.interpret_instruction(0xF107)
        self.assertEqual(self.ii.reg_v[0x1], 0x20)

    def test_fx15_set_delay_timer_to_vx(self):
        self.assertEqual(self.ii.reg_delay, 0x0)
        self.ii.reg_v[0x1] = 0x10
        self.ii.interpret_instruction(0xF115)
        self.assertEqual(self.ii.reg_delay, 0x10)

    def test_fx18_set_sound_timer_to_vx(self):
        self.assertEqual(self.ii.reg_sound, 0x0)
        self.ii.reg_v[0x1] = 0x10
        self.ii.interpret_instruction(0xF118)
        self.assertEqual(self.ii.reg_sound, 0x10)

    def test_fx1e_add_vx_to_index(self):
        self.ii.reg_v[0x2] = 20
        self.ii.reg_i = 10
        self.ii.interpret_instruction(0xF21E)
        self.assertEqual(self.ii.reg_i, 30)

    def test_fx33_save_reg_vx_bcd_representation_to_memory(self):
        self.ii.reg_i = 0x500
        self.ii.reg_v[0xA] = 254
        self.ii.interpret_instruction(0xFA33)
        self.assertEqual(self.ii.memory[0x500], 2)
        self.assertEqual(self.ii.memory[0x501], 5)
        self.assertEqual(self.ii.memory[0x502], 4)

        self.ii.reg_i = 0x500
        self.ii.reg_v[0xA] = 19
        self.ii.interpret_instruction(0xFA33)
        self.assertEqual(self.ii.memory[0x500], 0)
        self.assertEqual(self.ii.memory[0x501], 1)
        self.assertEqual(self.ii.memory[0x502], 9)

    def test_fx55_save_reg_v0_through_vx_to_memory(self):
        self.ii.reg_i = 0x500
        for i in range(0x0, 0xF):
            self.ii.reg_v[i] = 0x10 + i
        self.ii.interpret_instruction(0xFE55)
        self.assertEqual(self.ii.memory[0x500], 0x10)
        self.assertEqual(self.ii.memory[0x501], 0x11)
        self.assertEqual(self.ii.memory[0x502], 0x12)
        self.assertEqual(self.ii.memory[0x503], 0x13)
        self.assertEqual(self.ii.memory[0x504], 0x14)
        self.assertEqual(self.ii.memory[0x505], 0x15)
        self.assertEqual(self.ii.memory[0x506], 0x16)
        self.assertEqual(self.ii.memory[0x507], 0x17)
        self.assertEqual(self.ii.memory[0x508], 0x18)
        self.assertEqual(self.ii.memory[0x509], 0x19)
        self.assertEqual(self.ii.memory[0x50A], 0x1A)
        self.assertEqual(self.ii.memory[0x50B], 0x1B)
        self.assertEqual(self.ii.memory[0x50C], 0x1C)
        self.assertEqual(self.ii.memory[0x50D], 0x1D)
        self.assertEqual(self.ii.memory[0x50E], 0x1E)

    def test_fx65_save_memory_to_reg_v0_through_vx(self):
        self.ii.reg_i = 0x500
        for i in range(0x0, 0xF):
            self.ii.memory[self.ii.reg_i + i] = 0x10 + i
        self.ii.interpret_instruction(0xFE65)
        self.assertEqual(self.ii.reg_v[0x0], 0x10)
        self.assertEqual(self.ii.reg_v[0x1], 0x11)
        self.assertEqual(self.ii.reg_v[0x2], 0x12)
        self.assertEqual(self.ii.reg_v[0x3], 0x13)
        self.assertEqual(self.ii.reg_v[0x4], 0x14)
        self.assertEqual(self.ii.reg_v[0x5], 0x15)
        self.assertEqual(self.ii.reg_v[0x6], 0x16)
        self.assertEqual(self.ii.reg_v[0x7], 0x17)
        self.assertEqual(self.ii.reg_v[0x8], 0x18)
        self.assertEqual(self.ii.reg_v[0x9], 0x19)
        self.assertEqual(self.ii.reg_v[0xA], 0x1A)
        self.assertEqual(self.ii.reg_v[0xB], 0x1B)
        self.assertEqual(self.ii.reg_v[0xC], 0x1C)
        self.assertEqual(self.ii.reg_v[0xD], 0x1D)
        self.assertEqual(self.ii.reg_v[0xE], 0x1E)


if __name__ == '__main__':
    unittest.main()
