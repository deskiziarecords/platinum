class AdaptiveCostModel:

    def __init__(self, registry, profiler,
                 alpha=1.0, beta=0.5, gamma=0.3):
        self.registry = registry
        self.profiler = profiler
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma

    def evaluate(self, graph):
        total_cost = 0

        for node_id in graph.topological_sort():
            node = graph.nodes[node_id]
            tool = self.registry.get(node.tool_name)
            manifest = tool["manifest"]

            stats = self.profiler.stats(node.tool_name)

            if stats:
                time_cost = stats["avg_runtime"]
                memory_cost = stats["avg_memory"]
            else:
                # fallback to declared cost
                time_cost = manifest.cost.time
                memory_cost = manifest.cost.memory

            total_cost += (
                self.alpha * time_cost +
                self.beta * memory_cost
            )

        return total_cost
