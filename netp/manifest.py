from dataclasses import dataclass, field
from typing import Dict, Any, Callable, Optional


@dataclass
class ToolRequirements:
    memory_mb: int = 128
    device: str = "auto"  # auto | cpu | gpu | tpu


@dataclass
class ToolFlags:
    parallel: bool = False
    deterministic: bool = True
    safety_tier: int = 1  # 1=safe, 5=critical


@dataclass
class ToolManifest:
    name: str
    version: str
    inputs: Dict[str, Any]
    outputs: Dict[str, Any]
    requires: ToolRequirements = field(default_factory=ToolRequirements)
    flags: ToolFlags = field(default_factory=ToolFlags)
    @dataclass
class ToolCost:
    time: float = 1.0
    memory: float = 1.0
    energy: float = 1.0


@dataclass
class ToolManifest:
    ...
    cost: ToolCost = field(default_factory=ToolCost)
