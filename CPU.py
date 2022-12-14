import os, sys

class Memory:
    # Constructs memory to be used. Data for memory block is stored utilizing an index
    def __init__(self, name):
        self.blocks = None
        self.data = None
        self.name = name
        print(self.data)
        if name == "main memory":
            self.store_values()

    # Stores values within memory to be used
    def store_values(self):
        # Obtains working directory for program 
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        data_to_add = open(dirname + '\data_input.txt', 'r')
        data_to_store = [x.split(",") for x in data_to_add.read().splitlines()]
        self.blocks = len(data_to_store)
        self.data = data_to_store
        for idx in range(0, self.blocks):
            self.data[idx][0] = int(self.data[idx][0], 2)
        print(self.data)
    
    # Reads data within memory based on address
    def memory_read(self, address):
        for node in self.data:
            if node != '':
                if node[0] == address:
                    return node[1]
        print(f"Memory address {address} was not found")
        return None
    
    # Writes data into memory and uses memory address as index
    def memory_write(self, address, data):
        for idx, node in enumerate(self.data):
            if node[0] == address:
                self.data[idx][1] = data
                return

class Cache(Memory):
    def __init__(self, main_memory):
        super().__init__(name="cache")
        self.main_memory = main_memory
        self.blocks = 4
        self.data = ["" for x in range(0, self.blocks)]
        self.last_index_written = None

    # Returns data from a specified memory address within the cache or reads from main memory and writes address and data into cache first if necessary
    def cache_read(self, address):
        data_to_return = self.memory_read(address)
        if data_to_return == None:
            data_to_return = self.main_memory.memory_read(address)
            self.cache_write(address, data_to_return)
        return data_to_return
    
    # Handles which block of memory to clear out within the cache if writing to a full cache
    def fifo_policy(self):
        print(self.last_index_written)
        if self.last_index_written == 3:
            data_to_store = self.data[0][1]
            address_to_store = self.data[0][0]
            self.data[0] = '' 
            self.main_memory.memory_write(address_to_store, data_to_store)
            self.last_index_written = 0
        else:
            data_to_store = self.data[self.last_index_written + 1][1]
            address_to_store = self.data[self.last_index_written + 1][0]
            self.data[self.last_index_written + 1] = '' 
            self.main_memory.memory_write(address_to_store, data_to_store)
            self.last_index_written += 1

    # Writes address and data into cache, if address is currently already in cache, overwrites data for address
    def cache_write(self, address, data):
        if self.memory_read(address) != None:
            self.memory_write(address, data)
        elif self.data.count("") == 0 and self.last_index_written == None:
            self.last_index_written = 3
            self.fifo_policy()
            self.store_to_empty_block(address, data)
        elif self.data.count("") == 0:
            self.fifo_policy()
            self.store_to_empty_block(address, data)
        else:
            self.store_to_empty_block(address, data)
        print(self.data)
    
    # Finds empty block to write to within cache
    def store_to_empty_block(self, address, data):
        for idx, node in enumerate(self.data):
                if node == '':
                    self.data[idx] = [address, data]
                    return
    
    # Flushes out cache, writes all data currently stored within cache to main memory and then empties the cache
    def flush_cache(self):
        for idx, block in enumerate(self.data):
            if block != '':
                self.main_memory.memory_write(block[0], block[1])
                self.data[idx] = ''

class CPU:
    def __init__(self):
        self.storage_registers = [0 for x in range(0, 32)]
        self.temp_register = None
        self.instruction_address_register = 0
        self.instruction_register = None
        self.cache_state = 1
        self.main_memory = Memory(name="main memory")
        self.cache = Cache(self.main_memory)
        self.halt = 0
        self.run_instructions()
    
    def fetch_instructions(self):
        if self.cache_state == 0:
            self.instruction_register = self.main_memory.memory_read(self.instruction_address_register)
        else:
            self.instruction_register = self.cache.cache_read(self.instruction_address_register)
    
    def decode_instructions(self):
        opcode = self.instruction_register[0:6]
        if len(self.instruction_register) < 32 or len(self.instruction_register) > 32:
            print("Invalid instruction length")
        elif opcode == '001000':
            self.ADDI(self.instruction_register[6:11], self.instruction_register[11:16], self.instruction_register[16:])
        elif opcode == '000101':
            self.BNE(self.instruction_register[6:11], self.instruction_register[11:16], self.instruction_register[16:])
        elif opcode == '000010':
            self.JUMP(self.instruction_register[6:])
        elif opcode == '000011':
            self.JAL(self.instruction_register[6:])
        elif opcode == '100011':
            self.LW(self.instruction_register[6:11], self.instruction_register[11:16], self.instruction_register[16:])
        elif opcode == '101011':
            self.SW(self.instruction_register[6:11], self.instruction_register[11:16], self.instruction_register[16:])
        elif opcode == '101111':
            self.CACHE_F(self.instruction_register[6:])
        elif opcode == '000001':
            self.HALT()
        elif opcode == '000000':
            func = self.instruction_register[26:]
            rs = int(self.instruction_register[6:11], 2)
            rt = int(self.instruction_register[11:16], 2)
            rd = int(self.instruction_register[16:21], 2)
            if func == '100000':
                self.ADD(rs, rt, rd)
            elif func == '100010':
                self.SUB(rs, rt, rd)
            elif func == '101010':
                self.SLT(rs, rt, rd)
    
    def process(self):
        self.instruction_address_register += 4
        self.fetch_instructions()
        self.decode_instructions()
    
    def run_instructions(self):
        while self.halt == 0:
            self.process()
    
    def ADDI(self, rs,  rt, immediate):
        destination_register = int(rt, 2)
        self.temp_register = self.storage_registers[int(rs, 2)] + int(immediate, 2)
        self.storage_registers[destination_register] = self.temp_register
        self.temp_register = None
    
    def BNE(self, rs, rt, offset):
        if self.storage_registers[int(rs, 2)] != self.storage_registers[int(rt, 2)]:
            self.instruction_address_register += 4
            self.instruction_address_register += int(offset, 2) * 4
            self.fetch_instructions()
            self.decode_instructions()

    def JUMP(self, memory_address):
        self.instruction_address_register = int(memory_address, 2) * 4
        self.fetch_instructions()
        self.decode_instructions()

    def JAL(self, memory_address):
        self.process()
        self.JUMP(memory_address)
    
    def LW(self, base, rt, offset):
        if self.cache_state == 0:
            self.storage_registers[int(rt, 2)] = int(self.main_memory.memory_read(int(base, 2) + int(offset, 2)), 2)
        else:
            print(int(base, 2), int(offset, 2))
            self.storage_registers[int(rt, 2)] = int(self.cache.cache_read((int(base, 2) + int(offset, 2))), 2)

    def SW(self, base, rt, offset):
        if self.cache_state == 0:
            self.main_memory.memory_write(int(base, 2) + int(offset, 2), self.storage_registers[int(rt, 2)])
        else:
            self.cache.cache_write(int(base, 2) + int(offset, 2), self.storage_registers[int(rt, 2)])
    
    def CACHE_F(self, code):
        if int(code) == 0:
            self.cache_state = 0
        elif int(code) == 1:
            self.cache_state = 1
        elif int(code) == 2:
            self.cache.flush_cache()
    
    def HALT(self):
        self.halt = 1

    def ADD(self, rs, rt, rd):
        self.storage_registers[rd] = self.storage_registers[rs] + self.storage_registers[rt]
    
    def SUB(self, rs, rt, rd):
        self.storage_registers[rd] = self.storage_registers[rs] - self.storage_registers[rt]
    
    def SLT(self, rs, rt, rd):
        if self.storage_registers[rs] < self.storage_registers[rt]:
            self.storage_registers[rd] = 1
        else:
            self.storage_registers[rd] = 0
        
    




new_CPU = CPU()




