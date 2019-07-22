"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.ops = [0] * 18 # actual number not known for sure yet

        '''
        Opcodes to implement:

        0 operands:
            HLT  = 00000001 # 1
            IRET = 00010011 # 19
            RET  = 00010001 # 17

        1 operand:
            CALL = 01010000 # 80
            DEC  = 01100110 # 102
            JEQ  = 01010101 # 85
            JMP  = 01010100 # 84
            JNE  = 01010110 # 86
            PRA  = 01001000 # 72
            PRN  = 01000111 # 71
            POP  = 01000110 # 70
            PUSH = 01000101 # 69, nice

        2 operands:
            ADD  = 10100000 # 160
            CMP  = 10100111 # 167
            LD   = 10000011 # 131
            LDI  = 10000010 # 130
            MUL  = 10100010 # 162
            ST   = 10000100 # 132
        '''


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, target):
        return self.ram[target]

    def ram_write(self, value, target):
        self.ram[target] = value
        return None

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        pass
