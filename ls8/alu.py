class ALU:
    def __init__(self, mount):
        self.CPU = mount
        self.OP = [self.add,0,self.mul,0,0,0,self.dec,self.cmp,0,0,0,0,0,0,0,0]

    def add(self, *operand):
        self.CPU.R[operand[0]] += self.CPU.R[operand[1]]

    def mul(self, *operand):
        self.CPU.R[operand[0]] *= self.CPU.R[operand[1]]

    def cmp(self, *operand):
        pass

    def dec(self, *operand):
        pass