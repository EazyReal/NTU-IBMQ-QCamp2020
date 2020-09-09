# Qiskit ALCom Provider

A fast and robust quantum computation siumulator can be incorporated into qiskit.
The original paper is [Bit-Slicing the Hilbert Space: Scaling Up Accurate Quantum Circuit Simulation to a New Level](https://arxiv.org/abs/2007.09304).


## An Example
```
from qiskit import QuantumCircuit, execute

from qiskit_alcom_provider import ALComProvider


# Generate 3-qubit GHZ state
num_qubits = 3
circ = QuantumCircuit(3, 3)
circ.h(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0, 1, 2], [0, 1 ,2])

# Perform noisy simulation
ALCom = ALComProvider()
backend = ALCom.get_backend('qasm_simulator')
job = execute(circ, backend)
result = job.result()

print(result.get_counts())
print(result.get_statevector())
```
