class EntropyCap:
    def __init__(self, area=1.0):
        self.area = area
        self.cap = self.area / 4

    def enforce(self, entropy: float) -> float:
        return min(entropy, self.cap)
