"""Physical entropy (heat / thermodynamics / adiabatic processes).

The default implementation is a small, dependency-free model so the core boots
instantly on a bare Python install. When the optional ``synthfuse`` package is
available it can be used as the thermal-state container instead:

    PLATINUM_THERMAL_BACKEND=synthfuse python main.py

Importing synthfuse pulls in JAX and takes a few seconds, so the bridge is
opt-in; if the import fails the local model is used and a warning is emitted.
"""

from __future__ import annotations

import os
import warnings

IDLE_TEMPERATURE = 35.0  # Celsius, the demo baseline
THERMAL_BACKEND_ENV = "PLATINUM_THERMAL_BACKEND"


def _load_thermal_state():
    """Return synthfuse's ThermalState class, or None if unavailable."""
    try:
        from synthfuse.os.kernel import ThermalState  # type: ignore[import-not-found]
    except Exception as exc:  # ImportError, JAX init errors, ...
        warnings.warn(
            f"synthfuse thermal backend unavailable ({exc!r}); "
            "falling back to the local physical-entropy model",
            RuntimeWarning,
            stacklevel=2,
        )
        return None
    return ThermalState


class SynthFuse:
    """Physical entropy (heat, thermodynamics, adiabatic processes).

    Owns the thermal side of the informational/physical duality: informational
    entropy raises the temperature, natural cooling lowers it, and structural
    mutations are refused when the projected temperature would cross the limit.
    """

    def __init__(self, thermal_limit: float = 100.0, backend: str | None = None):
        self.thermal_limit = thermal_limit
        self.current_temperature = IDLE_TEMPERATURE
        self.entropy = 0.0
        self._state_cls = None
        self.backend = "local"

        requested = (backend or os.environ.get(THERMAL_BACKEND_ENV, "local")).lower()
        if requested == "synthfuse":
            self._state_cls = _load_thermal_state()
            if self._state_cls is not None:
                self.backend = "synthfuse"

    # -- internal helpers -------------------------------------------------
    def _load_fraction(self, temperature: float | None = None) -> float:
        span = self.thermal_limit - IDLE_TEMPERATURE
        if span <= 0:
            return 0.0
        temp = self.current_temperature if temperature is None else temperature
        return (temp - IDLE_TEMPERATURE) / span

    def _thermal_state(self, load: float | None = None):
        """Build a synthfuse ThermalState for the given (or current) load."""
        if self._state_cls is None:
            return None
        load = self._load_fraction() if load is None else load
        return self._state_cls(
            load=load,
            entropy=self.entropy,
            capacity_remaining=max(0.0, 1.0 - load),
        )

    # -- public API ---------------------------------------------------------
    def get_thermal_load(self) -> float:
        """Current temperature in Celsius."""
        return self.current_temperature

    def can_handle_mutation(self, complexity_gain: float) -> bool:
        """Can the hardware absorb the thermal cost of a structural mutation?"""
        projected = self.current_temperature + (complexity_gain * 2.0)
        if self._state_cls is not None:
            state = self._thermal_state(self._load_fraction(projected))
            # ThermalState.exceeds() is strict (>), so at exactly the limit it
            # would report "fine"; require headroom instead.
            return not state.exceeds(1.0) and state.load < 1.0
        return projected < self.thermal_limit

    def update_physics(self, entropy_delta: float) -> None:
        """Simulate physical heat generation from informational entropy."""
        self.entropy = max(0.0, entropy_delta)
        self.current_temperature += entropy_delta * 10.0
        # Natural cooling
        self.current_temperature = max(IDLE_TEMPERATURE, self.current_temperature - 0.5)
