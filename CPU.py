import os, sys

class Memory:
    # Constructs memory with 14 blocks of memory to be used. Data for memory block is stored utilizing an index
    def __init__(self, blocks=14):
        self.blocks = blocks
        self.data = ["" for x in range(0, blocks)]
        print(self.data)
    
    # Stores values within memory to be used
    def store_values(self):
        # Obtains working directory for program 
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        data_to_add = open(dirname + '\data_input.txt', 'r')
        data_to_store = [x.split(",") for x in data_to_add.read().splitlines()]
        print(data_to_store)

new_memory = Memory()
new_memory.store_values()
