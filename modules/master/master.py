# modules/master/master.py

"""
Platinum OS – Master Self-Contained Module (MSCM)

This module contains:

- Graph engine
- Feature extraction
- Structural learning model
- Cost evaluation
- Optimization engine
- Extension registry
- Hook integration system

Fully self-contained.
"""


# =====================================================
# Graph Engine
# =====================================================

class Node:
    def __init__(self, node_id, terminal=False, parallelizable=False):
        self.id = node_id
        self.terminal = terminal
        self.parallelizable = parallelizable


class Graph:
    def __init__(self):
        self.nodes = {}
        self.adjacency = {}

    def add_node(self, node):
        self.nodes[node.id] = node
        self.adjacency[node.id] = []

    def add_edge(self, src, dst):
        self.adjacency[src].append(dst)

    def clone(self):
        new = Graph()
        for n in self.nodes.values():
            new.add_node(
                Node(n.id, n.terminal, n.parallelizable)
            )
        for src, targets in self.adjacency.items():
            for dst in targets:
                new.add_edge(src, dst)
        return new

    def depth(self):
        visited = set()

        def dfs(n):
            visited.add(n)
            children = self.adjacency.get(n, [])
            if not children:
                return 1
            return 1 + max(dfs(c) for c in children if c not in visited)

        return max((dfs(n) for n in self.nodes), default=0)


# =====================================================
# Feature Extractor
# =====================================================

class GraphFeatureExtractor:

    def extract(self, graph):
        num_nodes = len(graph.nodes)
        num_edges = sum(len(v) for v in graph.adjacency.values())
        depth = graph.depth()

        out_degrees = [len(v) for v in graph.adjacency.values()]
        avg_out = sum(out_degrees)/len(out_degrees) if out_degrees else 0
        max_out = max(out_degrees) if out_degrees else 0

        terminal_count = sum(
            1 for n in graph.nodes.values() if n.terminal
        )

        parallelizable = sum(
            1 for n in graph.nodes.values() if n.parallelizable
        )

        return [
            num_nodes,
            num_edges,
            depth,
            avg_out,
            max_out,
            terminal_count,
            parallelizable,
        ]


# =====================================================
# Structural Model
# =====================================================

import random


class StructuralModel:

    def __init__(self, extractor, lr=0.001):
        self.extractor = extractor
        self.lr = lr
        self.weights = [random.uniform(-0.01, 0.01) for _ in range(7)]

    def score(self, graph):
        features = self.extractor.extract(graph)
        return sum(w * f for w, f in zip(self.weights, features))

    def update(self, better, worse):
        fb = self.extractor.extract(better)
        fw = self.extractor.extract(worse)

        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * (fb[i] - fw[i])


# =====================================================
# Cost Model
# =====================================================

class CostModel:

    def evaluate(self, graph):
        # Simple default cost: nodes + edges
        nodes = len(graph.nodes)
        edges = sum(len(v) for v in graph.adjacency.values())
        return nodes + edges


# =====================================================
# Extension Registry (Integrator)
# =====================================================

class ExtensionRegistry:

    def __init__(self):
        self.passes = []
        self.hooks = {}
        self.extra_functions = {}

    def register_pass(self, opt_pass):
        self.passes.append(opt_pass)

    def register_hook(self, name, func):
        self.hooks.setdefault(name, []).append(func)

    def register_function(self, name, func):
        self.extra_functions[name] = func

    def call_hook(self, name, *args, **kwargs):
        for func in self.hooks.get(name, []):
            func(*args, **kwargs)


# =====================================================
# Optimizer Core
# =====================================================

class MasterOptimizer:

    def __init__(self):
        self.extractor = GraphFeatureExtractor()
        self.structural_model = StructuralModel(self.extractor)
        self.cost_model = CostModel()
        self.registry = ExtensionRegistry()

    def optimize(self, graph, max_iterations=10):

        best = graph.clone()
        best_cost = self.cost_model.evaluate(best)

        for _ in range(max_iterations):
            improved = False

            for opt_pass in self.registry.passes:
                candidate = opt_pass(best.clone())
                candidate_cost = self.cost_model.evaluate(candidate)

                if candidate_cost < best_cost:
                    best = candidate
                    best_cost = candidate_cost
                    improved = True

                elif candidate_cost == best_cost:
                    if self.structural_model.score(candidate) < \
                       self.structural_model.score(best):

                        self.structural_model.update(candidate, best)
                        best = candidate
                        improved = True

            self.registry.call_hook("post_iteration", best)

            if not improved:
                break

        return best

# =====================================================
# Adaptive Pass Entry
# =====================================================

class PassEntry:

    def __init__(self, func):
        self.func = func
        self.times_called = 0
        self.improvements = 0
        self.cumulative_gain = 0.0

    def record(self, gain):
        self.times_called += 1
        if gain > 0:
            self.improvements += 1
            self.cumulative_gain += gain

    @property
    def average_gain(self):
        if self.improvements == 0:
            return 0
        return self.cumulative_gain / self.improvements
# =====================================================
# Example Integration
# =====================================================

if __name__ == "__main__":

    optimizer = MasterOptimizer()

    # Example optimization pass
    def prune_isolated(graph):
        to_remove = [
            nid for nid, targets in graph.adjacency.items()
            if not targets
        ]
        for nid in to_remove:
            graph.nodes.pop(nid, None)
            graph.adjacency.pop(nid, None)
        return graph

    optimizer.registry.register_pass(prune_isolated)

    # Example hook
    def log_graph(graph):
        print("Current nodes:", len(graph.nodes))

    optimizer.registry.register_hook("post_iteration", log_graph)

    # Example graph
    g = Graph()
    g.add_node(Node("A"))
    g.add_node(Node("B"))
    g.add_node(Node("C"))
    g.add_edge("A", "B")

    optimized = optimizer.optimize(g)

    print("Final node count:", len(optimized.nodes))
