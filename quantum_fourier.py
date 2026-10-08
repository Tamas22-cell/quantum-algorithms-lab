
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

# Quantum Fourier Transform - 3 qubits
n = 3
qc = QuantumCircuit(n)

# Initial state |001>
qc.x(0)

# Quantum Fourier Transform
for j in range(n):
    qc.h(j)
    for k in range(j + 1, n):
        qc.cp(np.pi / (2 ** (k - j)), k, j)

# Reverse qubit order
for i in range(n // 2):
    qc.swap(i, n - i - 1)

# Simulate statevector
simulator = AerSimulator(method="statevector")
qc.save_statevector()

result = simulator.run(qc).result()
state = result.get_statevector(qc)

probabilities = np.abs(np.asarray(state)) ** 2

print("QFT Probabilities:")
for i, p in enumerate(probabilities):
    print(f"|{i:03b}>: {p:.4f}")

# Visualization
states = [f"{i:03b}" for i in range(2 ** n)]

plt.figure(figsize=(10, 5))
plt.bar(states, probabilities)
plt.title("Quantum Fourier Transform - State Probabilities")
plt.xlabel("Quantum State")
plt.ylabel("Probability")
plt.ylim(0, 1)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("qft_results.png", dpi=200)
plt.show()
