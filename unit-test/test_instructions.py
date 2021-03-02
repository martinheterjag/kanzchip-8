import unittest
from unittest.mock import Mock
import sys
sys.path.append('../src')
from instruction_interpreter import InstructionInterpreter

class TestInstructions(unittest.TestCase):
    # Test is supposed to verify that 0x00E0 will clear the screen
    def test_00E0_clear_screen(self):
        screen = Mock()
        ii = InstructionInterpreter(screen)
        ii.interpret_instruction(0x00E0)
        screen.clear_all.assert_called_once()

if __name__ == '__main__':
    unittest.main()
