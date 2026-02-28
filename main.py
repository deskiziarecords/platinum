from platinum.os import PlatinumOS
import time

if __name__ == "__main__":
    os_system = PlatinumOS()

    print("=== Platinum OS Booted ===")
    print("Letters:", os_system.letters.stats())

    print(os_system.netp.execute("ingest", "ExampleRepo"))

    for _ in range(5):
        state = os_system.run_cycle()
        print("State:", state)
        time.sleep(0.5)
