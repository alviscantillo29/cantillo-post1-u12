"""Estado de Bell (|Phi+>) en Qiskit sobre AerSimulator."""
import os
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


def main():
    os.makedirs("capturas", exist_ok=True)

    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    print("Circuito Estado de Bell:")
    print(qc.draw(output="text"))

    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    job = simulator.run(compiled, shots=1024)
    counts = job.result().get_counts()
    print("Conteos (1024 shots):", counts)

    fig = plot_histogram(counts, title="Estado de Bell |Phi+> (1024 shots)")
    fig.savefig("capturas/01_bell_state.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
