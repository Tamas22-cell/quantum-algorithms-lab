
import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, SparsePauliOp

# ----------------------------------
# VQE - Variational Quantum Eigensolver
# Two-qubit Hamiltonian
# ----------------------------------

hamiltonian = SparsePauliOp.from_list([
    ("ZI", 0.5),
    ("IZ", 0.5),
    ("XX", 0.3),
    ("ZZ", 0.2)
])

# Variational quantum circuit
def create_circuit(params):
    qc = QuantumCircuit(2)

    qc.ry(params[0], 0)
    qc.ry(params[1], 1)

    qc.cx(0, 1)

    qc.rz(params[2], 0)
    qc.ry(params[3], 1)

    return qc


energy_history = []

# Energy expectation value
def energy_function(params):
    circuit = create_circuit(params)

    state = Statevector.from_instruction(circuit)

    energy = np.real(
        state.expectation_value(hamiltonian)
    )

    energy_history.append(energy)

    return energy


# Classical optimization
initial_params = np.array([0.5, 1.0, 0.3, 0.7])

result = minimize(
    energy_function,
    initial_params,
    method="COBYLA",
    options={"maxiter": 2000, "tol": 1e-6}
)

# Exact ground-state energy for comparison
matrix = hamiltonian.to_matrix()
eigenvalues = np.linalg.eigvalsh(matrix)
exact_energy = np.min(eigenvalues)

print("\nVQE Optimization Results")
print("-------------------------")
print("Optimization success:", result.success)
print("VQE Energy:", round(result.fun, 6))
print("Exact Ground Energy:", round(exact_energy, 6))
print("Energy Error:", round(abs(result.fun - exact_energy), 6))
print("Iterations:", len(energy_history))

# Plot convergence
plt.figure(figsize=(10, 5))

plt.plot(
    energy_history,
    label="VQE Energy",
    linewidth=2
)

plt.axhline(
    exact_energy,
    color="red",
    linestyle="--",
    label="Exact Ground Energy"
)

plt.title("VQE Quantum Energy Optimization")
plt.xlabel("Function Evaluations")
plt.ylabel("Energy")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("vqe_results.png", dpi=200)
plt.show()
