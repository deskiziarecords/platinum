def safety_check(manifest, context):
    # ACBF - boundary enforcement
    if manifest.flags.safety_tier > 4:
        raise PermissionError("Tool exceeds allowed safety tier")

    # TRE - energy control
    if context.metrics["energy"] > 10000:
        raise RuntimeError("Energy threshold exceeded")

    return True
