"""Algoritmo de Grover para n=2 qubits (estado objetivo |11>) en AerSimulator."""
import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def build_grover_2q() -> QuantumCircuit:
    """Construye el circuito de Grover de 2 qubits con 1 iteracion para |11>."""
    qc = QuantumCircuit(2, 2)

    # 1. Superposicion uniforme
    qc.h([0, 1])
    qc.barrier()

    # 2. Oraculo de fase para |11>
    qc.cz(0, 1)
    qc.barrier()

    # 3. Operador de difusion (inversion respecto a la media)
    qc.h([0, 1])
    qc.x([0, 1])
    qc.cz(0, 1)
    qc.x([0, 1])
    qc.h([0, 1])
    qc.barrier()

    # 4. Medicion
    qc.measure([0, 1], [0, 1])
    return qc


def main():
    os.makedirs("capturas", exist_ok=True)
    qc = build_grover_2q()
    print("Circuito Grover n=2 (objetivo |11>):")
    print(qc.draw(output="text"))

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    counts = simulator.run(compiled, shots=1024).result().get_counts()
    print("Conteos Grover ideal (1024 shots):", counts)

    fig = plot_histogram(counts, title="Grover n=2 ideal - Objetivo |11> (1024 shots)")
    fig.savefig("capturas/03_grover_ideal.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
