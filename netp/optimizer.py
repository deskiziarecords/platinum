def optimize(self, graph):
    current_graph = graph.clone()
    best_graph = current_graph
    best_cost = self.cost_model.evaluate(current_graph)

    for _ in range(self.max_iterations):
        improved = False

        for opt_pass in self.passes:
            candidate = opt_pass.run(current_graph, self.registry)
            candidate_cost = self.cost_model.evaluate(candidate)

            if (
                candidate_cost < best_cost
                or (
                    candidate_cost == best_cost
                    and self._is_structurally_better(candidate, best_graph)
                )
            ):
                best_graph = candidate
                best_cost = candidate_cost
                current_graph = candidate
                improved = True

        if not improved:
            break

    return best_graph
