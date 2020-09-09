# How to use python side with a success C++ package

## Step 1
- https://github.com/EazyReal/NTU-IBMQ-QCamp2020/blob/master/qiskit_alcom_provider/qasm_simulator_alcom.py
    - `qiskit_alcom_provider/qasm_simulator_alcom.py`, line 300
    - `from cpp_package import sim_file`
    - `controller = sim_file`
    
## Step 2 (if there is a bug)
- if there is other issue, check out when the function is applied
    - https://github.com/EazyReal/NTU-IBMQ-QCamp2020/blob/master/qiskit_alcom_provider/bdd_backend.py
    - `qiskit_alcom_provider/bdd_backend.py`, line 162