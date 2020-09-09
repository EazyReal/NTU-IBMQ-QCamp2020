# Qiskit ALCom Provider

A fast and robust quantum computation siumulator can be incorporated into qiskit.  
The original paper is [Bit-Slicing the Hilbert Space: Scaling Up Accurate Quantum Circuit Simulation to a New Level](https://arxiv.org/abs/2007.09304).

## Installation (TBA)
```
pip install qiskit-alcom-provider
```

## An Example
```python
from qiskit import QuantumCircuit, execute
from qiskit_alcom_provider import ALComProvider


# A Simple Bell State Generation Circuit
num_qubits = 2
qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0,1)
qc.measure([0, 1], [0, 1])
qc.draw()

# get an ALComProvider instance
ALCom = ALComProvider()
# from provider get a backend for our toy experiments
backend = ALCom.get_backend('qasm_simulator')
# add backend_options
# backend_options = {"method": "statevector"}
# backend_options = {"method": "counts"}
backend_options = None # default is counts mode
# execute the experiment
job = execute(qc, backend, shots=1024, backend_options=backend_options)
# get the result
result = job.result()

print(result.get_counts())
```

## Implementation
- `ALComProvider` provides `QasmSimulator(BBDBackend)`
- `QasmSimulator(BBDBackend)` is a simple wrapper over `BBDBackend`
- `BBDBackend` calls `_run_job`
    - the main changing area
    - get the qasm string from QC (qobj -> qc -> qasm string)
    - feed the string to bdd simulator written in c++
    - get the result string and parse it
    - return a `TrimResult`
- other files are almost identical to `Aer` project
    
## Future Works
- Support `qiskit.result.Result` and `Experiment` 
- Seperate backend for different method (i.e. `statevector mode` and `counts mode`)
- thorogh test
- documentation
- pip package


## Contact Information
- for this README.md and python side
    - YanTong Lin
        - 0312fs3@gmail.com
- for Pybinder issue
    - TBA
- for original paper and 
    - Yuan-Hung Tsai
    - TBA
