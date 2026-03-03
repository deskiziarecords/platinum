class RuntimeContext:
    def __init__(self, device="cpu"):
        self.device = device
        self.state = {}
        self.metrics = {
            "energy": 0,
            "calls": 0
        }
