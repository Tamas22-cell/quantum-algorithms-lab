
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import numpy as np

# Quantum Phase Estimation
# Target phase: 0.125 = 1/8
n = 3
phase = 0.125

qc = QuantumCircuit(n + 1, n)

# Prepare eigenstate |1>
qc.x(n)

# Counting qubits
for q in range(n):
    qc.h(q)

# Controlled phase rotations
for q in range(n):
    qc.cp(2 * np.pi * phase * (2 ** q), q, n)

# Inverse Quantum Fourier Transform
for i in range(n // 2):
    qc.swap(i, n - i - 1)

for j in range(n):
    for k in range(j):
        qc.cp(-np.pi / (2 ** (j - k)), k, j)
    qc.h(j)

# Measure counting register
qc.measure(range(n), range(n))

simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Quantum Phase Estimation Results:")
print(counts)

states = [format(i, f"0{n}b") for i in range(2 ** n)]
values = [counts.get(s, 0) for s in states]

plt.figure(figsize=(10, 5))
plt.bar(states, values)
plt.title("Quantum Phase Estimation")
plt.xlabel("Measured State")
plt.ylabel("Counts")
plt.tight_layout()
plt.savefig("qpe_results.png", dpi=200)
plt.show()
