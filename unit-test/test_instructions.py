import unittest
from unittest.mock import Mock

from src.instruction_interpreter import InstructionInterpreter


class TestInstructions(unittest.TestCase):
    # Test is supposed to verify that 0x00E0 will clear the screen
    def test_00E0_clear_screen(self):
        screen = Mock()
        ii = InstructionInterpreter(screen)
        ii.interpret_instruction(0x00E0)
        screen.clear_all.assert_called_once()

    # Test is supposed to verify that 8xy0 load ii.reg_v[y] into ii.reg_v[x]
    def test_8xy0_load_vx_vy(self):
        screen = Mock()
        ii = InstructionInterpreter(screen)
        ii.reg_v[0x0] = 0x10
        ii.reg_v[0x1] = 0x11
        ii.reg_v[0xA] = 0x12
        # Load V1 == 0x11 into V0
        self.assertEqual(ii.reg_v[0x0], 0x10)
        ii.interpret_instruction(0x8010)
        self.assertEqual(ii.reg_v[0x0], 0x11)
        # Load VA == 0x12 into V1
        self.assertEqual(ii.reg_v[0x1], 0x11)
        ii.interpret_instruction(0x81A0)
        self.assertEqual(ii.reg_v[0xA], 0x12)


if __name__ == '__main__':
    unittest.main()
