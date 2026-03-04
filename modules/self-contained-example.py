# modules/example/ex.py

"""
Platinum OS – Embedded Structural Model Example

This file demonstrates:

- Minimal Graph abstraction
- Feature extraction
- Learned structural model
- Acceptance policy
- Simple optimization loop demo

This is a self-contained demonstration module.
"""


# -------------------------------------------------
# Minimal Graph Representation
# -------------------------------------------------

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
        new_graph = Graph()
        for node in self.nodes.values():
            new_graph.add_node(
                Node(
                    node.id,
                    terminal=node.terminal,
                    parallelizable=node.parallelizable,
                )
            )
        for src, targets in self.adjacency.items():
            for dst in targets:
                new_graph.add_edge(src, dst)
        return new_graph

    def depth(self):
        # naive depth estimation
        visited = set()

        def dfs(node_id):
            visited.add(node_id)
            children = self.adjacency.get(node_id, [])
            if not children:
                return 1
            return 1 + max(dfs(c) for c in children if c not in visited)

        max_depth = 0
        for node_id in self.nodes:
            max_depth = max(max_depth, dfs(node_id))
        return max_depth


# -------------------------------------------------
# Feature Extractor
# -------------------------------------------------

class GraphFeatureExtractor:

    def extract(self, graph):
        num_nodes = len(graph.nodes)
        num_edges = sum(len(v) for v in graph.adjacency.values())
        depth = graph.depth()

        out_degrees = [len(v) for v in graph.adjacency.values()]
        avg_out = sum(out_degrees) / len(out_degrees) if out_degrees else 0
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


# -------------------------------------------------
# Structural Model (Linear Ranking)
# -------------------------------------------------

import random


class StructuralModel:

    def __init__(self, feature_extractor, lr=0.001):
        self.feature_extractor = feature_extractor
        self.lr = lr
        self.weights = [random.uniform(-0.01, 0.01) for _ in range(7)]

    def score(self, graph):
        features = self.feature_extractor.extract(graph)
        return sum(w * f for w, f in zip(self.weights, features))

    def update(self, better_graph, worse_graph):
        f_better = self.feature_extractor.extract(better_graph)
        f_worse = self.feature_extractor.extract(worse_graph)

        for i in range(len(self.weights)):
            gradient = f_better[i] - f_worse[i]
            self.weights[i] -= self.lr * gradient


# -------------------------------------------------
# Acceptance Policy
# -------------------------------------------------

class LearnedAcceptancePolicy:

    def __init__(self, structural_model):
        self.structural_model = structural_model

    def accept(self, candidate, best_graph, equal_cost=True):
        if not equal_cost:
            return False

        score_candidate = self.structural_model.score(candidate)
        score_best = self.structural_model.score(best_graph)

        if score_candidate < score_best:
            self.structural_model.update(candidate, best_graph)
            return True

        return False


# -------------------------------------------------
# Example Usage
# -------------------------------------------------

if __name__ == "__main__":

    # Build graph A
    g1 = Graph()
    g1.add_node(Node("A", parallelizable=True))
    g1.add_node(Node("B", terminal=True))
    g1.add_edge("A", "B")

    # Build graph B (slightly more complex)
    g2 = g1.clone()
    g2.add_node(Node("C"))
    g2.add_edge("A", "C")

    extractor = GraphFeatureExtractor()
    model = StructuralModel(extractor)
    policy = LearnedAcceptancePolicy(model)

    print("Initial Scores:")
    print("Graph A:", model.score(g1))
    print("Graph B:", model.score(g2))

    accepted = policy.accept(g2, g1, equal_cost=True)

    print("\nAccepted B over A?", accepted)

    print("\nUpdated Scores:")
    print("Graph A:", model.score(g1))
    print("Graph B:", model.score(g2))
