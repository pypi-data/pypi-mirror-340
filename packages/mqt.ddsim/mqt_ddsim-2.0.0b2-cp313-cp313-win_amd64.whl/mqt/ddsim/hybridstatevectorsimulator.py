"""Backend for DDSIM Hybrid Schrodinger-Feynman Simulator."""

from __future__ import annotations

from qiskit.transpiler import Target

from .hybridqasmsimulator import HybridQasmSimulatorBackend


class HybridStatevectorSimulatorBackend(HybridQasmSimulatorBackend):
    """Python interface to MQT DDSIM Hybrid Schrodinger-Feynman Simulator."""

    _SHOW_STATE_VECTOR = True
    _HSF_SV_TARGET = Target(
        description="MQT DDSIM HSF Statevector Simulator Target",
        num_qubits=30,  # corresponds to 16GiB memory for storing the full statevector
    )

    def __init__(self) -> None:
        """Constructor for the DDSIM Hybrid Schrodinger-Feynman Statevector simulator backend."""
        super().__init__(
            name="hybrid_statevector_simulator",
            description="MQT DDSIM Hybrid Schrodinger-Feynman Statevector simulator",
        )

    @property
    def target(self) -> Target:
        """Return the target of the backend."""
        return self._HSF_SV_TARGET
