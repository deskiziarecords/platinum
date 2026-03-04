class OptimizationPipeline:

    def __init__(self, registry, cost_model, max_iterations=10):
        self.registry = registry
        self.cost_model = cost_model
        self.passes = []
        self.max_iterations = max_iterations

    def register_pass(self, opt_pass):
        self.passes.append(opt_pass)

    def optimize(self, graph):
        current_graph = graph.clone()
        best_graph = current_graph
        best_cost = self.cost_model.evaluate(current_graph)

        for _ in range(self.max_iterations):
            previous_signature = current_graph.signature()
            improved = False

            for opt_pass in self.passes:
                candidate = opt_pass.run(current_graph, self.registry)
                candidate_cost = self.cost_model.evaluate(candidate)

                # Only accept candidate if strictly better
                if candidate_cost < best_cost:
                    best_graph = candidate
                    best_cost = candidate_cost
                    current_graph = candidate
                    improved = True

            if not improved:
                break  # No pass produced improvement

            if current_graph.signature() == previous_signature:
                break  # Structural convergence

        return best_graph
