from .router import route
from .safety import safety_check


class ExecutionEngine:
    def __init__(self, registry):
        self.registry = registry

    def call(self, tool_name: str, args: dict, context):
        tool = self.registry.get(tool_name)
        manifest = tool["manifest"]
        handler = tool["handler"]

        # Safety check
        safety_check(manifest, context)

        # Hardware routing
        device = route(manifest.requires.device)
        context.device = device

        # Execute
        result = handler(args, context)

        # Metrics update
        context.metrics["calls"] += 1

        return result
