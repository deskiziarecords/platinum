def optimize(self, graph):
    current_graph = graph.clone()
    best_graph = current_graph
    best_cost = self.cost_model.evaluate(current_graph)

    for _ in range(self.max_iterations):
        for opt_pass in self.passes:
            candidate = opt_pass.run(current_graph, self.registry)

            candidate_cost = self.cost_model.evaluate(candidate)

            if candidate_cost < best_cost:
                best_graph = candidate
                best_cost = candidate_cost
                current_graph = candidate

        if current_graph.signature() == best_graph.signature():
            break

    return best_graph

    def __init__(self, registry, max_iterations=10):
        self.registry = registry
        self.passes = []
        self.max_iterations = max_iterations

    def register_pass(self, opt_pass):
        self.passes.append(opt_pass)

    def optimize(self, graph):
        current_graph = graph.clone()

        for _ in range(self.max_iterations):
            previous_signature = current_graph.signature()

            for opt_pass in self.passes:
                current_graph = opt_pass.run(current_graph, self.registry)

            new_signature = current_graph.signature()

            if new_signature == previous_signature:
                break  # Converged

        return current_graphclass GraphOptimizer:

    def __init__(self, registry):
        self.registry = registry
   

    # -----------------------------
    # Entry Point
    # -----------------------------
    def optimize(self, graph):
        self._prune_dead_nodes(graph)
        self._merge_parallel_duplicates(graph)
        return graph

    # -----------------------------
    # Dead Node Pruning
    # -----------------------------
    def _prune_dead_nodes(self, graph):
        removable = []

        for node_id, node in graph.nodes.items():
            has_outgoing = len(graph.adjacency[node_id]) > 0
            if not has_outgoing:
                # If no outgoing edges, check if terminal
                if not getattr(node, "terminal", False):
                    removable.append(node_id)

        for node_id in removable:
            del graph.nodes[node_id]
            if node_id in graph.adjacency:
                del graph.adjacency[node_id]

    # -----------------------------
    # Merge Parallel Duplicates
    # -----------------------------
    def _merge_parallel_duplicates(self, graph):
        seen = {}

        for node_id, node in list(graph.nodes.items()):
            key = (node.tool_name, tuple(sorted(node.args.items())))

            tool = self.registry.get(node.tool_name)
            manifest = tool["manifest"]

            if manifest.flags.parallel:
                if key in seen:
                    # Redirect dependencies
                    original_id = seen[key]
                    for src, targets in graph.adjacency.items():
                        graph.adjacency[src] = [
                            original_id if t == node_id else t
                            for t in targets
                        ]
                    del graph.nodes[node_id]
                else:
                    seen[key] = node_id

