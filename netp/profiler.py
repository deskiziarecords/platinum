from collections import defaultdict


class Profiler:

    def __init__(self):
        self.data = defaultdict(list)

    def record(self, tool_name, runtime, memory, device):
        self.data[tool_name].append({
            "runtime": runtime,
            "memory": memory,
            "device": device
        })

    def stats(self, tool_name):
        records = self.data.get(tool_name, [])
        if not records:
            return None

        avg_runtime = sum(r["runtime"] for r in records) / len(records)
        avg_memory = sum(r["memory"] for r in records) / len(records)

        return {
            "avg_runtime": avg_runtime,
            "avg_memory": avg_memory,
            "samples": len(records)
        }
