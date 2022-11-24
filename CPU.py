import os, sys

class Memory:
    # Constructs memory with 14 blocks of memory to be used. Data for memory block is stored utilizing an index
    def __init__(self):
        self.blocks = None
        self.data = None
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



new_memory = Memory()
new_memory.store_values()
