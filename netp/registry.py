from typing import Dict, Callable
from .manifest import ToolManifest


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Dict] = {}

    def register(self, manifest: ToolManifest, handler: Callable):
        if manifest.name in self._tools:
            raise ValueError(f"Tool {manifest.name} already registered")

        self._tools[manifest.name] = {
            "manifest": manifest,
            "handler": handler
        }

    def get(self, name: str):
        if name not in self._tools:
            raise KeyError(f"Tool {name} not found")

        return self._tools[name]

    def list_tools(self):
        return list(self._tools.keys())
