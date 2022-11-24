import os, sys

class Memory:
    # Constructs memory to be used. Data for memory block is stored utilizing an index
    def __init__(self, name):
        self.blocks = None
        self.data = None
        self.name = name
        print(self.data)
    
    # Stores values within memory to be used
    def store_values(self):
        # Obtains working directory for program 
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        data_to_add = open(dirname + '\data_input.txt', 'r')
        data_to_store = [x.split(",") for x in data_to_add.read().splitlines()]
        self.blocks = len(data_to_store)
        self.data = data_to_store
        print(self.data)
    
    def memory_read(self, address):
        for data in self.data:
            if data[0] == address:
                return data[1]
        print(f"Memory address {address} was not found")

class Cache(Memory):
    def __init__(self, main_memory):
        super().__init__(name="cache")
        self.main_memory = main_memory
        self.blocks = 4
        self.data = ["" for x in range(0, self.blocks)]

class CPU:
    def __init__(self):
        self.storage_registers = ["" for x in range(0, 32)]
        self.temp_register = None
        self.instruction_address_register = 0
        self.instruction_register = None
        self.cache_state = 1
        self.main_memory = Memory(self.main_memory, name="main memory")
        self.cache = Cache()
        self.halt = 0

        print(self.storage_registers)
    
    def fetch_instructions(self):
        if self.cache_state == 0:
            self.instruction_register = self.main_memory.memory_read(self.instruction_address_register)
        else:
            self.instruction_register = self.cache.cache_read(self.instruction_address_register)
        
    


new_memory = Memory()
new_memory.store_values()

new_CPU = CPU()
