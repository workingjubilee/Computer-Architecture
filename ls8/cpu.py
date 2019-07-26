"""CPU functionality."""

import sys
import re
import binascii
from time import monotonic
from alu import ALU


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.fl = 0b00000000
        self.ram = [0] * 256
        self.R = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.ALU = ALU(mount=self)
        self.OP = [0, self.halt, self.load_this, self.load_mem,
                   self.store, self.push, self.pop, self.print_decimal,
                   self.print_ASCII]

        self.JOP = [self.call, self.ret, 0, self.iret,
                    self.jump, self.jeq, self.jne, 0]
        self.OPT = [self.OP, self.JOP, self.ALU.OP]
        self.tick = monotonic()
        self.tock = monotonic()
        self.listening = True

        '''
        Opcodes to implement:

        0 operands:
            IRET = 00010011 # 19
        '''
    def adhd(self):
        bitmask = self.R[5] & self.R[6]
        if bitmask:
            vector = -1
            for bit in range(8):
                # Right shift interrupts down by i, then mask with 1 to see if that bit was set
                if ((bitmask >> bit) & 1) == 1:
                    vector = bit
                    self.R[6] = self.R[6] ^ (2**bit)
                    break
            self.interrupt(vector)
        return

    def call(self, *operand):
        self.R[7] = (self.R[7] - 1) & 0xFF
        self.ram_write(((self.pc + 2) & 0xFF), self.R[7])
        self.pc = (self.R[operand[0]] & 0xFF)

    def clock(self):
        self.tick = monotonic()
        if self.tick-self.tock > 1:
            self.R[6] = self.R[6] | 0b0001
            self.tock = monotonic()
        return

    def jump(self, *operand):
        self.pc = self.R[operand[0]]

    def jeq(self, *operand):
        if self.fl & 0b1:
            self.pc = self.R[operand[0]]
        else:
            self.pc = (self.pc + 2) & 0xFF

    def jne(self, *operand):
        if self.fl & 0b1 is 0:
            self.pc = self.R[operand[0]]
        else:
            self.pc = (self.pc + 2) & 0xFF

    def interrupt(self, vector):
        self.R[5] = 0
        self.R[6] = 0
        for register in range(7):
            self.push(register)
        self.R[7] = (self.R[7] - 1) & 0xFF
        self.ram_write(self.fl, self.R[7])
        self.R[7] = (self.R[7] - 1) & 0xFF
        self.ram_write(self.pc, self.R[7])
        self.listening = False
        self.pc = self.ram[0xF8 + vector]
        return

    def iret(self, *operand):
        for register in range(6, -1, -1):
            self.pop(register)
        self.fl = self.ram_read(self.R[7]) & 0xFF
        self.R[7] = (self.R[7] + 1) & 0xFF
        self.ret()
        self.listening = True
        return

    def halt(self, *operands):
        sys.exit(1)

    def load(self, file):
        """Load a program into memory."""

        address = 0
        program = open(file, 'r')

        for instruction in program:
            try:
                binary = re.match(r'^[01]{8}', instruction)
                if binary is not None:
                    self.ram[address] = int(binary[0], 2)
                    address += 1
            except ValueError:
                print(f'Skipping {instruction}')

        program.close()

    def load_mem(self, *operand):
        self.R[operand[0]] = self.ram_read(self.R[operand[1]])

    def load_this(self, *operand):
        self.R[operand[0]] = (operand[1] & 0xFF)

    def print_ASCII(self, *operand):
        print(chr(self.R[operand[0]]))

    def print_decimal(self, *operand):
        print(self.R[operand[0]])

    def push(self, *operand):
        self.R[7] = (self.R[7] - 1) & 0xFF
        self.ram_write(self.R[operand[0]], self.R[7])

    def pop(self, *operand):
        self.R[operand[0]] = self.ram_read(self.R[7]) & 0xFF
        self.R[7] = (self.R[7] + 1) & 0xFF

    def ret(self, *operand):
        self.pc = self.ram_read(self.R[7]) & 0xFF
        self.R[7] = (self.R[7] + 1) & 0xFF

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr & 0xFF

    def store(self, *operand):
        self.ram_write(self.R[operand[1]], self.R[operand[0]])

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.R[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        s = self

        while running:
            try:
                if s.R[5] > 0 and s.listening:
                    s.clock()
                    s.adhd()

                ir = s.ram_read(s.pc)

                # this uses bitwise operators to "slice" the IR
                op_ands = ir >> 6
                op_flags = ir >> 4 & 0b0011
                op_id = ir & 0b1111

                operands = [0] * (op_ands)

                for i in range(op_ands):
                    operands[i] = s.ram_read(s.pc+1+i)

                s.OPT[op_flags][op_id](*operands)

                if op_flags & 0b1 == 0:
                    s.pc = (s.pc + 1 + (op_ands)) & 0xFF
            except TypeError:
                print(bin(ir))
                print(bin(op_ands))
                print(bin(op_flags))
                print(bin(op_id))
                raise Exception("Doh!")
