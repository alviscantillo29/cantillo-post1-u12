"""Algoritmo de Grover para n=2 qubits bajo modelo de ruido despolarizante NISQ."""
import os
import matplotlib.pyplot as plt
from qiskit import transpile
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
from qiskit.visualization import plot_histogram

from grover import build_grover_2q


def build_depolarizing_noise_model(p1q: float = 0.001, p2q: float = 0.01) -> NoiseModel:
    """Crea un NoiseModel con errores despolarizantes para compuertas de 1 y 2 qubits."""
    noise_model = NoiseModel()
    error_1q = depolarizing_error(p1q, 1)
    error_2q = depolarizing_error(p2q, 2)

    noise_model.add_all_qubit_quantum_error(error_1q, ["h", "x"])
    noise_model.add_all_qubit_quantum_error(error_2q, ["cz"])
    return noise_model


def main():
    os.makedirs("capturas", exist_ok=True)
    qc = build_grover_2q()
    noise_model = build_depolarizing_noise_model(p1q=0.001, p2q=0.01)

    noisy_sim = AerSimulator(noise_model=noise_model)
    compiled = transpile(qc, noisy_sim)
    counts = noisy_sim.run(compiled, shots=1024).result().get_counts()
    print("Conteos Grover con ruido (p1q=0.001, p2q=0.01, 1024 shots):", counts)

    fig = plot_histogram(
        counts,
        title="Grover n=2 con ruido despolarizante (p1q=0.001, p2q=0.01)",
    )
    fig.savefig("capturas/04_grover_noise.png", dpi=150, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
