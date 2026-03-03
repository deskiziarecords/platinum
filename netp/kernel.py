from .registry import ToolRegistry
from .engine import ExecutionEngine
from .context import RuntimeContext
from .optimizer import GraphOptimizer


class NETPKernel:

    def __init__(self, device="auto"):
        # Core components
        self.registry = ToolRegistry()
        self.context = RuntimeContext(device=device)

        # Execution system
        self.engine = ExecutionEngine(self.registry)
        self.optimizer = GraphOptimizer(self.registry)

    # -------------------------
    # Tool Registration
    # -------------------------
    def register_tool(self, manifest, handler):
        self.registry.register(manifest, handler)

    # -------------------------
    # Direct Call
    # -------------------------
    def call(self, tool_name, args):
        return self.engine.call(tool_name, args, self.context)

    # -------------------------
    # Graph Execution
    # -------------------------
    def execute_graph(self, graph):
        optimized_graph = self.optimizer.optimize(graph)
        return self.engine.execute_graph(optimized_graph, self.context)

    # -------------------------
    # Introspection
    # -------------------------
    def list_tools(self):
        return self.registry.list_tools()

    def metrics(self):
        return self.context.metrics
