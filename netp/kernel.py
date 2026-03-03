from .registry import ToolRegistry
from .engine import ExecutionEngine
from .context import RuntimeContext
from .graph import ExecutionGraph
from .optimizer import GraphOptimizer


class NETPKernel:
    """
    Single-node execution kernel.
    Acts as the operating substrate for Platinum OS.
    """

    def __init__(self, device="auto"):
        self.registry = ToolRegistry()
        self.context = RuntimeContext(device=device)
        self.engine = ExecutionEngine(self.registry)

    # -----------------------------
    # Tool Registration
    # -----------------------------
    def register_tool(self, manifest, handler):
        self.registry.register(manifest, handler)

    # -----------------------------
    # Direct Invocation
    # -----------------------------
    def call(self, tool_name: str, args: dict):
        return self.engine.call(tool_name, args, self.context)

    # -----------------------------
    # Graph Execution
    # -----------------------------
    def execute_graph(self, graph: ExecutionGraph):
        return self.engine.execute_graph(graph, self.context)

    # -----------------------------
    # Introspection
    # -----------------------------
    def list_tools(self):
        return self.registry.list_tools()

    def metrics(self):
        return self.context.metrics
