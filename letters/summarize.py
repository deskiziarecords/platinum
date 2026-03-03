from netp.manifest import ToolManifest, ToolRequirements, ToolFlags


def summarize_handler(args, context):
    text = args["text"]
    return {"summary": text[:100]}


manifest = ToolManifest(
    name="SCP.summarize",
    version="0.1",
    inputs={"text": "string"},
    outputs={"summary": "string"},
    requires=ToolRequirements(memory_mb=128, device="auto"),
    flags=ToolFlags(parallel=True, deterministic=True, safety_tier=1)
)
