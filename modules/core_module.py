class CoreModule:
    def __init__(self, spine, hardware):
        self.spine = spine
        self.hardware = hardware

    def tick(self):
        self.hardware.compute(self.spine.rewrite)
