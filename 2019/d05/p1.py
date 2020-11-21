import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from d02.p1 import IntcodeComputer, get_program_from_input


class ThermalEnvironmentSupervisionTerminal(IntcodeComputer):
    def _run_opcode_3(self, parameters: list[int], modes: list[int]):
        self.program[parameters[0]] = int(input('Enter input for opcode 3: '))

    def _run_opcode_4(self, parameters: list[int], modes: list[int]):
        address = parameters[0]
        print(f'Value at address {address}: {self.program[address]}')

    def _run_program(self):
        i = 0
        while True:
            instruction = str(self.program[i])
            opcode = self._get_opcode_from_instruction(instruction)
            if opcode == 99:
                return
            modes = self._pad_modes(instruction, opcode)
            self._run_instruction(opcode, self.program[i + 1: i + 1 + self.OPCODES_TO_AMOUNT_OF_PARAMS[opcode]], modes)

            i += self.OPCODES_TO_AMOUNT_OF_PARAMS[opcode] + 1
            # print(i, instruction, sep=', ')

    @staticmethod
    def _get_opcode_from_instruction(instruction: str) -> int:
        opcode_string = instruction[-2:]  # The opcode is based on the last two digits of the instruction.
        return int(opcode_string)

    @classmethod
    def _pad_modes(cls, instruction: str, opcode: int) -> list[int]:
        """
        :param instruction: instruction with maybe missing modes
        :param opcode: opcode of the instruction
        :return: instruction with padded zeroes that replace missing modes cv
        """
        amount_of_parameters = cls.OPCODES_TO_AMOUNT_OF_PARAMS[opcode]
        existing_modes = instruction[:-2]
        modes = existing_modes.rjust(amount_of_parameters, '0')
        modes = reversed(modes)  # Modes are read from right to left, but indices start on the left.
        return [int(mode) for mode in modes]


if __name__ == '__main__':
    ThermalEnvironmentSupervisionTerminal(get_program_from_input(5)).program_output()
