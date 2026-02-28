from platinum.core.spine import RGKMSpine
from platinum.core.entropy import EntropyCap
from platinum.hardware.backend import HardwareBackend
from platinum.letters.library import LettersLibrary
from platinum.netp.protocol import NETP
from platinum.memory.orbitals import MemoryOrbitals
from platinum.modules.factory import Factory
from platinum.modules.lab import Lab
from platinum.modules.observatory import Observatory
from platinum.modules.core_module import CoreModule


class PlatinumOS:
    def __init__(self):
        self.letters = LettersLibrary()
        self.hardware = HardwareBackend()
        self.spine = RGKMSpine()
        self.entropy_cap = EntropyCap()
        self.netp = NETP()
        self.memory = MemoryOrbitals()

        self.factory = Factory()
        self.lab = Lab(self.letters)
        self.observatory = Observatory()
        self.core = CoreModule(self.spine, self.hardware)

        self._register()

    def _register(self):
        self.netp.register("ingest", self.factory.ingest)
        self.netp.register("experiment", self.lab.experiment)
        self.netp.register("monitor", lambda: self.observatory.monitor(self.spine))

    def run_cycle(self):
        self.core.tick()
        state = self.spine.get_state()
        state["entropy"] = self.entropy_cap.enforce(state["entropy"])
        return state
