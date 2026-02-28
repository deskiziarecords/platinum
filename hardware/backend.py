import platform

class HardwareBackend:
    def __init__(self):
        self.backend = self.detect_backend()

    def detect_backend(self):
        proc = platform.processor().lower()
        if "arm" in proc:
            return "TPU"
        elif "intel" in proc:
            return "CPU"
        else:
            return "GPU"

    def compute(self, func, *args, **kwargs):
        print(f"[Hardware:{self.backend}] Executing")
        return func(*args, **kwargs)
