class MemoryOrbitals:
    def __init__(self):
        self.layers = [[] for _ in range(12)]

    def store(self, layer: int, data):
        self.layers[layer % 12].append(data)

    def retrieve(self, layer: int):
        return self.layers[layer % 12]
