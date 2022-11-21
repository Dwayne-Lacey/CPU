class Memory:
    def __init__(self, blocks=14):
        self.blocks = blocks
        self.data = ["" for x in range(0, blocks)]
        print(self.data)

new_memory = Memory()
