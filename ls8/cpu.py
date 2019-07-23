"""CPU functionality."""

import sys
import re
from alu import ALU

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0b00000000
        self.ram = [0] * 256
        self.R = [0,0,0,0,0,0,0,0xF4]
        self.ALU = ALU(mount=self)
        self.OP = [0,self.halt,self.load_immediate,0,0,0,0,self.print,0,0,0,0,0,0,0,0]
#         | FF  I7 vector         |    Interrupt vector table
# | FE  I6 vector         |
# | FD  I5 vector         |
# | FC  I4 vector         |
# | FB  I3 vector         |
# | FA  I2 vector         |
# | F9  I1 vector         |
# | F8  I0 vector         |
# | F7  Reserved          |
# | F6  Reserved          |
# | F5  Reserved          |
# | F4  Key pressed       |    Holds the most recent key pressed on the keyboard
# | F3  Start of Stack    |

        '''
        Opcodes to implement:

        0 operands:
            IRET = 00010011 # 19
            RET  = 00010001 # 17

        1 operand:
            CALL = 01010000 # 80
            JEQ  = 01010101 # 85
            JMP  = 01010100 # 84
            JNE  = 01010110 # 86
            PRA  = 01001000 # 72
            POP  = 01000110 # 70
            PUSH = 01000101 # 69, nice

        2 operands:
            LD   = 10000011 # 131
            ST   = 10000100 # 132
        '''

    def halt(self, *operands):
        return True


    def load(self, file):
        """Load a program into memory."""

        address = 0
        program = open(file, 'r')

        for instruction in program:
            try:
                binary = re.match(r'[01]+', instruction)
                if binary is not None:
                    self.ram[address] = int(binary[0], 2)
                    address += 1
            except ValueError:
                print(f'Skipping {instruction}')

        program.close()

    def load_immediate(self, *operand):
        self.R[operand[0]] = operand[1]

    def print(self, *operand):
        print(self.R[operand[0]])

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr
        return None

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.R[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        halt = None
        s = self

        while halt == None:
            ir = s.ram_read(s.pc)
            operands = [0] * (ir >> 0b00000110)

            for i in range(len(operands)):
                operands[i] = s.ram_read(s.pc+1+i)

            if ir & 0b00100000:
                halt = s.ALU.OP[ir & 0b1111](*operands)
            else:
                halt = s.OP[ir & 0b1111](*operands)

            if ir & 0b00010000:
                raise Exception("TODO")
            else:
                s.pc += 1 + len(operands)