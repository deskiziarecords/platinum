class OptimizationState:

    def __init__(self, graph, initial_cost):
        self.current_graph = graph.clone()
        self.best_graph = self.current_graph
        self.best_cost = initial_cost

    def update(self, graph, cost):
        self.current_graph = graph
        self.best_graph = graph
        self.best_cost = cost
