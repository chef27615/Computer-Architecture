"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # init ram
        self.ram = [000000000] * 256
        # init pointer
        self.pc = 0
        # init register
        self.reg = [0] * 8 
        # init stack_pointer, point from the end 
        self.stack_pointer = 0xF4 
        self.reg[7] = self.ram[self.stack_pointer]
        #op dictionary 
        self.op_table = {}
        self.op_table[0b01000111] = self.op_prn
        self.op_table[0b00000001] = self.op_hlt
        self.op_table[0b10000010] = self.op_ldi
        self.op_table[0b01000101] = self.op_push
        self.op_table[0b01000110] = self.op_pop
        self.op_table[0b00010001] = self.op_ret
        self.op_table[0b01010000] = self.op_call

    def op_prn(self, num):
        print(self.reg[num])
    
    def op_hlt(self):
        sys.exit(1)
    
    def op_ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
    
    def op_push(self, num):
        val = self.reg[num]
        self.stack_pointer -= 1
        self.ram[self.stack_pointer] = val
    
    def op_pop(self, num):
        val = self.ram[-1]
        self.reg[num] = val
        self.stack_pointer +=1

    def op_ret(self):
        val = self.ram[-1]
        self.pc = val
        self.stack_pointer +=1
    
    def op_call(self, num):
        self.stack_pointer -= 1
        address = self.pc + 2
        self.ram[self.stack_pointer] = address
        sub_route = self.reg[num]
        self.pc = sub_route

    def load(self):
        """Load a program into memory."""

        address = 0
        if len(sys.argv) != 2:
            print('Usage: using file <filename>', file=sys.stderr)
            sys.exit(1)
        try: 
            with open(sys.argv[1]) as f:
                for line in f:
                    number = line.split('#')[0]
                    number = number.replace('\n', '')
                    number = number.strip()

                    if number =='':
                        number= int(number, 2)
                    
                    print(f'value in loading {number}')
                    self.ram[address] = number
                    address += 1
        
        except FileNotFoundError:
            print(f'{sys.argv[0]}: sys.argv[1] not found')
            sys.exit()

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        MUL = 0b10100010
        ADD = 0b10100000
        DEC = 0b10100001
        DIV = 0b10100011
        XOR = 0b10101011
        SHR = 0b10101101
        SHL = 0b10101100

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == DEC:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == XOR:
            xor = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = xor
        elif op == SHR:
            shr = self.reg[reg_a]
            right = shr >> self.reg[reg_b]
            self.reg[reg_a] = right
        elif op == SHL:
            shl = self.reg[reg_a]
            left = shl << self.reg[reg_b]
            self.reg[reg_a] = left

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
        
        ir = self.ram[self.pc]
        print(f'ir: {ir}')

        while True:
            ir = self.ram[self.pc]

            cmd_a = self.ram_read(self.pc+1)
            cmd_b = self.ram_read(self.pc+2)
            print(cmd_a, cmd_b)

            cpu_op = (ir & 0b11000000) >> 6 
            alu_op = (ir & 0b00100000) >> 5 
            
            if ir == 0b01010000:
                self.op_table[ir](cmd_a)
                continue

            elif ir == 0b00010001:
                self.op_table[ir]()
                continue
            
            if alu_op:
                self.alu(ir, cmd_a, cmd_b)
            elif cpu_op == 2:
                self.op_table[ir](cmd_a, cmd_b)
            elif cpu_op == 1:
                self.op_table[ir](cmd_a)
            elif cpu_op == 0:
                self.op_table[ir]()
            else:
                self.op_table[ir]()
            self.pc += cpu_op + 1

        print(f'ir: {ir}')
        # cmd_a = (ir )

            
        # print(f'ram {self.ram}')
        # print(f'pc {self.pc}')