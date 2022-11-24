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

class CPU:
    def __init__(self):
        self.storage_registers = ["" for x in range(0, 32)]
        self.temp_register = None
        self.instruction_address_register = 0
        self.instruction_register = None
        self.cache_state = 1
        self.main_memory = Memory(name="main memory")
        self.cache = Cache(self.main_memory)
        self.halt = 0

        print(self.storage_registers)
    
    def fetch_instructions(self):
        if self.cache_state == 0:
            self.instruction_register = self.main_memory.memory_read(self.instruction_address_register)
        else:
            self.instruction_register = self.cache.cache_read(self.instruction_address_register)
        
    




new_CPU = CPU()
new_CPU.cache.cache_read("00000100")
new_CPU.cache.cache_read("00001000")
new_CPU.cache.cache_write("00001000", "test write successful")
new_CPU.cache.cache_read("00010000")
new_CPU.cache.cache_read("00010100")
new_CPU.cache.cache_read("00011000")
new_CPU.cache.cache_read("00011100")
new_CPU.cache.cache_read("00001000")