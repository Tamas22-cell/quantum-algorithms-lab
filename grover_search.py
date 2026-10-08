
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt

qc = QuantumCircuit(2, 2)

# Superposition
qc.h([0, 1])

# Oracle: mark state 11
qc.cz(0, 1)

# Diffusion operator
qc.h([0, 1])
qc.x([0, 1])
qc.h(1)
qc.cx(0, 1)
qc.h(1)
qc.x([0, 1])
qc.h([0, 1])

qc.measure([0, 1], [0, 1])

simulator = AerSimulator()
compiled = transpile(qc, simulator)
result = simulator.run(compiled, shots=1024).result()
counts = result.get_counts()

print("Grover Search Results:", counts)

states = ["00", "01", "10", "11"]
values = [counts.get(s, 0) for s in states]

plt.bar(states, values)
plt.title("Grover Quantum Search")
plt.xlabel("Quantum State")
plt.ylabel("Measurement Counts")
plt.savefig("grover_results.png", dpi=200)
plt.show()
