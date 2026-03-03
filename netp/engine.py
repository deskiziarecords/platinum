from .router import route
from .safety import safety_check


class ExecutionEngine:

    def __init__(self, registry):
        self.registry = registry

    def execute_node(self, node, context):
        tool = self.registry.get(node.tool_name)
        manifest = tool["manifest"]
        handler = tool["handler"]

        safety_check(manifest, context)

        device = route(manifest.requires.device)
        context.device = device

        result = handler(node.args, context)

        context.metrics["calls"] += 1
        return result

    def execute_graph(self, graph, context):
        order = graph.topological_sort()

        for node_id in order:
            node = graph.nodes[node_id]

            # Inject dependency results into args
            for dep in node.dependencies:
                node.args[f"dep_{dep}"] = graph.nodes[dep].result

            node.result = self.execute_node(node, context)

        return {
            node_id: graph.nodes[node_id].result
            for node_id in graph.nodes
        }
