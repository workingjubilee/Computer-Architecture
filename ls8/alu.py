class ALU:
    def __init__(self, mount):
        self.CPU = mount
        self.OP = [self.add,0,self.multiply,0,0,0,self.dec,self.cmp,0,0,0,0,0,0,0,0]

    def add(self, *operand):
        self.CPU.R[operand[0]] = ((self.CPU.R[operand[0]] + self.CPU.R[operand[1]]) & 0xFF)

    def multiply(self, *operand):
        self.CPU.R[operand[0]] = ((self.CPU.R[operand[0]] * self.CPU.R[operand[1]]) & 0xFF)

    def cmp(self, *operand):
        pass

    def dec(self, *operand):
        pass