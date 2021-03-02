import unittest
from unittest.mock import Mock
from src.instruction_interpreter import InstructionInterpreter


class TestInstructions(unittest.TestCase):
    def setUp(self):
        self.screen = Mock()
        self.ii = InstructionInterpreter(self.screen)

    # Test is supposed to verify that 0x00E0 will clear the screen
    def test_00E0_clear_screen(self):
        self.ii.interpret_instruction(0x00E0)
        self.screen.clear_all.assert_called_once()

    # Test verifies that 0x00EE will set program_counter to address in stack the pointer is pointing to,
    # and that the pointer is decremented.
    def test_00EE_ret(self):
        self.ii.stack = [400, 500]
        self.ii.stack_pointer = 1
        self.ii.interpret_instruction(0x00EE)

        self.assertEqual(self.ii.stack_pointer, 0)
        self.assertEqual(self.ii.program_counter, 500)

    # def test_2nnn_jump(self):

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


if __name__ == '__main__':
    unittest.main()
