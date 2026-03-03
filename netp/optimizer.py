class GraphOptimizer:

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

