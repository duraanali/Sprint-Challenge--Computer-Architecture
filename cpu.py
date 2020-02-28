"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256  
        self.reg = [0] * 8  
        self.pc = 0  
        self.stack_pointer = 7  
        self.less = 0
        self.greater = 0
        self.equal = 0
        self.blank = ""  

        # ---------------------
        self.ADD = 0b10100000
        self.CALL = 0b01010000
        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.MUL = 0b10100010
        self.POP = 0b01000110
        self.PRN = 0b01000111
        self.PUSH = 0b01000101
        self.RET = 0b00010001
        # --------------------

        # -----------------------
        self.CMP = 0b10100111
        self.JEQ = 0b01010101
        self.JMP = 0b01010100
        self.JNE = 0b01010110
        # ---------------------
    
   
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, val, address):
        self.ram[address] = val

    def load(self):
        """Load a program into memory."""

        address = 0
        with open(sys.argv[1]) as program:
            for row in program:
                row = row.split("#")[0].strip()
                if row is self.blank:
                    continue
                value = int(row, 2)  # set value to the number, of base 2
                print(f"\t\tdef load-> binary: {value: 08b}: \t decimal: {value}")
                self.ram[address] = value
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":  # add
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":  # multiply
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":  # compare
            if self.reg[reg_a] < self.reg[reg_b]:
                self.less = 1
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.greater = 1
            elif self.reg[reg_a] == self.reg[reg_b]:
                self.equal = 1
        else:
            raise Exception("Unsupported ALU operation")

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
        while True:

         
            instruction_reg = self.ram[self.pc]
            operand_x = self.ram_read(self.pc + 1)
            operand_y = self.ram_read(self.pc + 2)

            if instruction_reg is self.LDI:
                self.reg[operand_x] = operand_y
                self.pc += 3

            elif instruction_reg is self.PRN:
                print(self.reg[operand_x])  # print the register at that place
                self.pc += 2    # increments by 2 to pass the arguments
            elif instruction_reg is self.ADD:
                self.alu("ADD", operand_x, operand_y)
                self.pc += 3

            elif instruction_reg is self.MUL:
                self.alu("MUL", operand_x, operand_y)
                self.pc += 3

            elif instruction_reg is self.CMP:
                self.alu("CMP", operand_x, operand_y)
                self.pc += 3

            elif instruction_reg is self.POP:
                self.reg[operand_x] = self.ram[self.stack_pointer]
                self.stack_pointer += 1
                self.pc += 2

            elif instruction_reg is self.PUSH:
                self.stack_pointer -= 1
                self.ram[self.stack_pointer] = self.reg[operand_x]
                self.pc += 2

            elif instruction_reg is self.CALL:
                self.reg[self.stack_pointer] -= 1
                self.ram[self.stack_pointer] = self.pc + 2
                self.pc = self.reg[operand_x]

            elif instruction_reg is self.RET:
                self.pc = self.ram[self.stack_pointer]
                self.reg[self.stack_pointer] += 1

            elif instruction_reg is self.JMP:
                self.pc = self.reg[operand_x]

            elif instruction_reg is self.JEQ:
                if self.equal == 1:
                    self.pc = self.reg[operand_x]
                else:
                    self.pc += 2

            elif instruction_reg is self.JNE:
                if self.equal == 0:
                    self.pc = self.reg[operand_x]
                else:
                    self.pc += 2
                    
            elif instruction_reg is self.HLT:
                break

            else:
                print(f"Unknown instruction at index: \t {self.pc}")
                sys.exit(1)
