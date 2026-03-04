import hashlib
import json


def signature(self):
    graph_repr = {
        node_id: {
            "tool": node.tool_name,
            "args": node.args,
            "deps": node.dependencies
        }
        for node_id, node in sorted(self.nodes.items())
    }

    serialized = json.dumps(graph_repr, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


from collections import defaultdict, deque


class ExecutionNode:
    def __init__(self, node_id, tool_name, args):
        self.node_id = node_id
        self.tool_name = tool_name
        self.args = args
        self.dependencies = []
        self.result = None


class ExecutionGraph:
    def __init__(self):
        self.nodes = {}
        self.adjacency = defaultdict(list)
        self.in_degree = defaultdict(int)

    def add_node(self, node: ExecutionNode):
        self.nodes[node.node_id] = node

    def add_edge(self, from_node, to_node):
        self.adjacency[from_node].append(to_node)
        self.in_degree[to_node] += 1
        self.nodes[to_node].dependencies.append(from_node)

    def topological_sort(self):
        queue = deque()
        for node_id in self.nodes:
            if self.in_degree[node_id] == 0:
                queue.append(node_id)

        sorted_nodes = []

        while queue:
            current = queue.popleft()
            sorted_nodes.append(current)

            for neighbor in self.adjacency[current]:
                self.in_degree[neighbor] -= 1
                if self.in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_nodes) != len(self.nodes):
            raise RuntimeError("Cycle detected in execution graph")

        return sorted_nodes
