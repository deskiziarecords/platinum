from .registry import ToolRegistry
from .engine import ExecutionEngine
from .context import RuntimeContext
from .graph import ExecutionGraph


class NETPKernel:

    def __init__(self):
        self.registry = ToolRegistry()
        self.engine = ExecutionEngine(self.registry)
        self.context = RuntimeContext()

    def register_tool(self, manifest, handler):
        self.registry.register(manifest, handler)

    def call(self, tool_name, args):
        return self.engine.call(tool_name, args, self.context)

    def execute_graph(self, graph: ExecutionGraph):
        return self.engine.execute_graph(graph, self.context)
