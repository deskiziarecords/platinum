from os_core import PlatinumOS
import time

def run_singularity_demo():
    print("=== INITIALIZING PLATINUM SINGULARITY (Fractal Computing Organism) ===")
    os_system = PlatinumOS()

    # 1. Hardware Fabric (TUNGSTEN)
    os_system.hardware.initialize_tungsten_fabric(os_system.hardware.backend)

    # 2. Universal Translator (FERROS)
    print("\n[FERROS] Sending high-level intent: 'find_anomaly'")
    plan = os_system.netp.execute("translate", "find_anomaly")
    for step in plan:
        print(f"  -> {step['action']}")

    # 3. Self-Healing Host (NEUROMETAL)
    print("\n[NEUROMETAL] Generating new optimization kernel...")
    os_system.spine.inject_module("QuantumEntropyReducer", "lambda x: x * 0.5")

    # 4. Entropy Duality (Synth-Fuse)
    print("\n[Synth-Fuse] Monitoring physical/informational duality cycles...")
    # Create an INAS instance and inject Synth-Fuse
    from inas import INAS
    cognitive_engine = INAS()
    cognitive_engine.physical_auditor = os_system.synth_fuse

    for i in range(25):
        state = os_system.run_cycle()
        if (i+1) % 5 == 0 or i > 15:
            print(f"Cycle {i+1} | Efficiency: {state['efficiency_gain']:.4f} | Temp: {state['temperature']:.2f}C")

        # Simulate high load in cycle 15
        if i == 15:
             print("\n[System] Simulating high computational load (Synth-Fuse Threshold)...")
             os_system.synth_fuse.current_temperature = 98.0

        # Test INAS Mutation with Synth-Fuse
        # Force many steps to trigger mutation condition
        for _ in range(5):
            cognitive_engine.step("constant_idea")

        time.sleep(0.05)

    print("\n=== SINGULARITY DEMO COMPLETE ===")

if __name__ == "__main__":
    run_singularity_demo()
