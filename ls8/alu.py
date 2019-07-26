class ALU:
    def __init__(self, mount):
        self.CPU = mount
        self.OP = [self.add, 0, self.multiply, 0,
                   0, self.increment, self.decrement, self.compare]

    def add(self, *operand):
        self.CPU.R[operand[0]] = (
            (self.CPU.R[operand[0]] + self.CPU.R[operand[1]]) & 0xFF)

    def multiply(self, *operand):
        self.CPU.R[operand[0]] = (
            (self.CPU.R[operand[0]] * self.CPU.R[operand[1]]) & 0xFF)

    def compare(self, *operand):
        self.CPU.fl = self.CPU.fl & 0b0000
        if self.CPU.R[operand[0]] == self.CPU.R[operand[1]]:
            self.CPU.fl = self.CPU.fl | 0b0001
        elif self.CPU.R[operand[0]] < self.CPU.R[operand[1]]:
            self.CPU.fl = self.CPU.fl | 0b0010
        elif self.CPU.R[operand[0]] > self.CPU.R[operand[1]]:
            self.CPU.fl = self.CPU.fl | 0b0100
        else:
            pass

    def decrement(self, *operand):
        self.CPU.R[operand[0]] = self.CPU.R[operand[0]] -1

    def increment(self, *operand):
        self.CPU.R[operand[0]] = self.CPU.R[operand[0]] +1