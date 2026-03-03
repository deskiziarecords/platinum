class ExecutionEngine:

    def __init__(self, registry):
        self.registry = registry
        self.cache = {}  # deterministic memoization

    def execute_node(self, node, context):
        tool = self.registry.get(node.tool_name)
        manifest = tool["manifest"]
        handler = tool["handler"]

        # Create deterministic cache key
        cache_key = (
            node.tool_name,
            tuple(sorted(node.args.items()))
        )

        if manifest.flags.deterministic and cache_key in self.cache:
            return self.cache[cache_key]

        from .safety import safety_check
        from .router import route

        safety_check(manifest, context)

        device = route(manifest.requires.device)
        context.device = device

        result = handler(node.args, context)

        context.metrics["calls"] += 1

        if manifest.flags.deterministic:
            self.cache[cache_key] = result

        return result
