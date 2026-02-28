class GodelStabilizer:
    def verify(self, state: dict) -> bool:
        return state.get("entropy", 0) < state.get("entropy_cap", float("inf"))
