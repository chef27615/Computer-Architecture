"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        ram = [0] * 256
        self.ram = ram
        
        reg = [0] * 8
        self.reg = reg

        pc = 0
        self.pc = pc

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
    
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value
        return None

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        # print('______\n')
        # self. trace()
        # print('______\n')

        while running:
            cmd_list = self.ram
            for cmd in cmd_list:
                if cmd == 130:
                    pass
                elif cmd == 1:
                    running = False
                elif cmd == 0:
                    self.pc += 1
                elif cmd == 8:
                    num = cmd_list[self.pc+1]
                elif cmd == 71:
                    print(num)
                else:
                    print(f'unknown cmd: {cmd}')
        # print(f'ram {self.ram}')
        # print(f'pc {self.pc}')