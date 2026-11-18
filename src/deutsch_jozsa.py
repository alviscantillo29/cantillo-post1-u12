"""Algoritmo de Deutsch-Jozsa para n=2 qubits en Qiskit sobre AerSimulator."""
import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def build_deutsch_jozsa(oracle_type: str = "balanced") -> QuantumCircuit:
    """Construye el circuito Deutsch-Jozsa para n=2 qubits de entrada + 1 ancilla."""
    qc = QuantumCircuit(3, 2)

    # Inicializar el qubit ancilla en |1>
    qc.x(2)
    qc.barrier()

    # Superposicion inicial en todos los qubits
    qc.h([0, 1, 2])
    qc.barrier()

    # Oraculo U_f
    if oracle_type == "balanced":
        # f(x0, x1) = x0 XOR x1 (funcion balanceada)
        qc.cx(0, 2)
        qc.cx(1, 2)
    elif oracle_type == "constant":
        # f(x0, x1) = 1 (funcion constante)
        qc.x(2)
    else:
        raise ValueError("oracle_type debe ser 'balanced' o 'constant'")
    qc.barrier()

    # Interferencia mediante compuertas Hadamard en los qubits de entrada
    qc.h([0, 1])
    qc.measure([0, 1], [0, 1])
    return qc


def main():
    os.makedirs("capturas", exist_ok=True)
    simulator = AerSimulator()

    for oracle_type, filename in [
        ("balanced", "capturas/02_deutsch_jozsa_balanced.png"),
        ("constant", "capturas/02_deutsch_jozsa_constant.png"),
    ]:
        qc = build_deutsch_jozsa(oracle_type)
        print(f"\nCircuito Deutsch-Jozsa ({oracle_type}):")
        print(qc.draw(output="text"))

        compiled = transpile(qc, simulator)
        counts = simulator.run(compiled, shots=1024).result().get_counts()
        print(f"Conteos ({oracle_type}, 1024 shots):", counts)

        fig = plot_histogram(
            counts, title=f"Deutsch-Jozsa n=2 - Oraculo {oracle_type} (1024 shots)"
        )
        fig.savefig(filename, dpi=150, bbox_inches="tight")
        plt.close(fig)


if __name__ == "__main__":
    main()
