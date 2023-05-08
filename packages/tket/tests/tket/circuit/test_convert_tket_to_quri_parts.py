import numpy as np
from pytket import Circuit, OpType  # type: ignore

from quri_parts.circuit import QuantumGate, gates
from quri_parts.tket.circuit.tket_circuit_converter import circuit_from_tket


def gate_equal(gate_1: QuantumGate, gate_2: QuantumGate) -> None:
    assert gate_1.name == gate_2.name
    assert gate_1.control_indices == gate_2.control_indices
    assert gate_1.target_indices == gate_2.target_indices
    assert np.allclose(
        (np.array(gate_1.params) / np.pi) % 2, (np.array(gate_2.params) / np.pi) % 2
    )


def test_circuit_from_tket() -> None:
    tket_circuit = Circuit(4)
    tket_circuit.add_gate(OpType.noop, (0,))
    tket_circuit.X(1)
    tket_circuit.Y(2)
    tket_circuit.Z(3)
    tket_circuit.H(0)
    tket_circuit.S(1)
    tket_circuit.Sdg(2)
    tket_circuit.SX(3)
    tket_circuit.SXdg(0)
    tket_circuit.T(1)
    tket_circuit.Tdg(2)
    tket_circuit.Rx(0.387, 3)
    tket_circuit.Ry(-9.956, 0)
    tket_circuit.Rz(3.643, 1)
    tket_circuit.U1(0.387, 2)
    tket_circuit.U2(0.387, -9.956, 3)
    tket_circuit.U3(0.387, -9.956, 3.643, 0)
    tket_circuit.CX(0, 1)
    tket_circuit.CZ(1, 2)
    tket_circuit.SWAP(0, 2)
    tket_circuit.CCX(0, 1, 2)

    qp_circuit = circuit_from_tket(tket_circuit)

    gate_sequence = [
        gates.Identity(0),
        gates.X(1),
        gates.Y(2),
        gates.Z(3),
        gates.H(0),
        gates.S(1),
        gates.Sdag(2),
        gates.SqrtX(3),
        gates.SqrtXdag(0),
        gates.T(1),
        gates.Tdag(2),
        gates.RX(3, 0.387 * np.pi),
        gates.RY(0, -9.956 * np.pi),
        gates.RZ(1, 3.643 * np.pi),
        gates.U1(2, (0.387) * np.pi),
        gates.U2(3, (0.387) * np.pi, -9.956 * np.pi),
        gates.U3(0, (0.387) * np.pi, -9.956 * np.pi, (3.643) * np.pi),
        gates.CNOT(0, 1),
        gates.CZ(1, 2),
        gates.SWAP(0, 2),
        gates.TOFFOLI(0, 1, 2),
    ]

    for i, g in enumerate(qp_circuit.gates):
        gate_equal(gate_sequence[i], g)
