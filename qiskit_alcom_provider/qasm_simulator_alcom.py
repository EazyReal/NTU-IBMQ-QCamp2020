# This code is part of Qiskit.
#
# (C) Copyright IBM 2018, 2019.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.
"""
ALCom qasm simulator backend.
Almost idendentical to Aer.
Should specify supported gates, device couple_map, etc.
"""

import logging
from math import log2
import json

from qiskit.util import local_hardware_info
from qiskit.providers.models import QasmBackendConfiguration

from .bdd_backend import BDDBackend
# import proposed model here
# from .qcsim_alcom import get_statevector, get_counts
from .version import __version__

logger = logging.getLogger(__name__)

"""
# for testing without qcsim_alcom
def get_statevector(qasm_str):
    # use a simulation result of 1024 shots on measurement of Bell states as an example for testing
    return '[0.5,0,0, 0.5]'

def get_counts(qasm_str):
    # use a simulation result of 1024 shots on measurement of Bell states as an example for testing
    return '{"00": 512, "01": 0, "10": 0, "11": 512}'

bdd_controller = {
    "state": get_statevector,
    "count": get_counts,
}
"""

bell_result = {
    #'results': [],
    'counts': {
        '00': 512, 
        '11': 512,
    },
    'statevector':[
        [0.70710678118, 0, 0, 0.70710678118],
        [0, 0, 0, 0],
    ]
}

# api_result = str([bell_result["counts"], bell_result["statevector"]])
api_result = json.dumps(bell_result)


def bdd_controller(qasm_str, use_statevector, shots):
    # return a bell state expetiment results with 1024 shots for testing API
    return api_result


class QasmSimulator(BDDBackend):
    """ 
    Run option here?
    """
    # MAX_QUBIT_MEMORY = int(log2(local_hardware_info()['memory'] * (1024**3) / 16))
    MAX_QUBIT_MEMORY = 30
    DEFAULT_CONFIGURATION = {
        'backend_name': 'qasm_simulator',
        'backend_version': __version__,
        'n_qubits': MAX_QUBIT_MEMORY,
        'url': 'TODO',
        'simulator': True,
        'local': True,
        'conditional': True,
        'open_pulse': False,
        'memory': True,
        'max_shots': 100000,
        'description': 'A C++ simulator using BDD operations for qobj files',
        'coupling_map': None,
        'basis_gates': [
            'u1', 'u2', 'u3', 'cx', 'cz', 'id', 'x', 'y', 'z', 'h', 's', 'sdg',
            't', 'tdg', 'swap', 'ccx', 'unitary', 'initialize', 'cu1', 'cu2',
            'cu3', 'cswap', 'mcx', 'mcy', 'mcz', 'mcu1', 'mcu2', 'mcu3',
            'mcswap', 'multiplexer', 'kraus', 'roerror'
        ],
        'gates': [{
            'name': 'u1',
            'parameters': ['lam'],
            'conditional': True,
            'description': 'Single-qubit gate [[1, 0], [0, exp(1j*lam)]]',
            'qasm_def': 'gate u1(lam) q { U(0,0,lam) q; }'
        }, {
            'name': 'u2',
            'parameters': ['phi', 'lam'],
            'conditional': True,
            'description':
            'Single-qubit gate [[1, -exp(1j*lam)], [exp(1j*phi), exp(1j*(phi+lam))]]/sqrt(2)',
            'qasm_def': 'gate u2(phi,lam) q { U(pi/2,phi,lam) q; }'
        }, {
            'name':
            'u3',
            'parameters': ['theta', 'phi', 'lam'],
            'conditional':
            True,
            'description':
            'Single-qubit gate with three rotation angles',
            'qasm_def':
            'gate u3(theta,phi,lam) q { U(theta,phi,lam) q; }'
        }, {
            'name': 'cx',
            'parameters': [],
            'conditional': True,
            'description': 'Two-qubit Controlled-NOT gate',
            'qasm_def': 'gate cx c,t { CX c,t; }'
        }, {
            'name': 'cz',
            'parameters': [],
            'conditional': True,
            'description': 'Two-qubit Controlled-Z gate',
            'qasm_def': 'gate cz a,b { h b; cx a,b; h b; }'
        }, {
            'name': 'id',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit identity gate',
            'qasm_def': 'gate id a { U(0,0,0) a; }'
        }, {
            'name': 'x',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit Pauli-X gate',
            'qasm_def': 'gate x a { U(pi,0,pi) a; }'
        }, {
            'name': 'y',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit Pauli-Y gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'z',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit Pauli-Z gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'h',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit Hadamard gate',
            'qasm_def': 'TODO'
        }, {
            'name': 's',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit phase gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'sdg',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit adjoint phase gate',
            'qasm_def': 'TODO'
        }, {
            'name': 't',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit T gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'tdg',
            'parameters': [],
            'conditional': True,
            'description': 'Single-qubit adjoint T gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'swap',
            'parameters': [],
            'conditional': True,
            'description': 'Two-qubit SWAP gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'ccx',
            'parameters': [],
            'conditional': True,
            'description': 'Three-qubit Toffoli gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'cswap',
            'parameters': [],
            'conditional': True,
            'description': 'Three-qubit Fredkin (controlled-SWAP) gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'unitary',
            'parameters': ['matrix'],
            'conditional': True,
            'description': 'N-qubit arbitrary unitary gate. '
                           'The parameter is the N-qubit matrix to apply.',
            'qasm_def': 'unitary(matrix) q1, q2,...'
        }, {
            'name': 'initialize',
            'parameters': ['vector'],
            'conditional': False,
            'description': 'N-qubit state initialize. '
                           'Resets qubits then sets statevector to the parameter vector.',
            'qasm_def': 'initialize(vector) q1, q2,...'
        }, {
            'name': 'cu1',
            'parameters': ['lam'],
            'conditional': True,
            'description': 'Two-qubit Controlled-u1 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'cu2',
            'parameters': ['phi', 'lam'],
            'conditional': True,
            'description': 'Two-qubit Controlled-u2 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'cu3',
            'parameters': ['theta', 'phi', 'lam'],
            'conditional': True,
            'description': 'Two-qubit Controlled-u3 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcx',
            'parameters': [],
            'conditional': True,
            'description': 'N-qubit multi-controlled-X gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcy',
            'parameters': [],
            'conditional': True,
            'description': 'N-qubit multi-controlled-Y gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcz',
            'parameters': [],
            'conditional': True,
            'description': 'N-qubit multi-controlled-Z gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcu1',
            'parameters': ['lam'],
            'conditional': True,
            'description': 'N-qubit multi-controlled-u1 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcu2',
            'parameters': ['phi', 'lam'],
            'conditional': True,
            'description': 'N-qubit multi-controlled-u2 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcu3',
            'parameters': ['theta', 'phi', 'lam'],
            'conditional': True,
            'description': 'N-qubit multi-controlled-u3 gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'mcswap',
            'parameters': [],
            'conditional': True,
            'description': 'N-qubit multi-controlled-SWAP gate',
            'qasm_def': 'TODO'
        }, {
            'name': 'multiplexer',
            'parameters': ['mat1', 'mat2', '...'],
            'conditional': True,
            'description': 'N-qubit multi-plexer gate. '
                           'The input parameters are the gates for each value.',
            'qasm_def': 'TODO'
        }, {
            'name': 'kraus',
            'parameters': ['mat1', 'mat2', '...'],
            'conditional': True,
            'description': 'N-qubit Kraus error instruction. '
                           'The input parameters are the Kraus matrices.',
            'qasm_def': 'TODO'
        }, {
            'name': 'roerror',
            'parameters': ['matrix'],
            'conditional': False,
            'description': 'N-bit classical readout error instruction. '
                           'The input parameter is the readout error probability matrix.',
            'qasm_def': 'TODO'
        }]
    }
    def __init__(self, configuration=None, provider=None):
        super().__init__(
            controller=bdd_controller,
            configuration=QasmBackendConfiguration.from_dict(self.DEFAULT_CONFIGURATION),
            provider=provider,
        )
        
    def _validate(self, qobj, backend_options, noise_model):
        """Semantic validations of the qobj which cannot be done via schemas.
        Warn if no measurements in circuit with classical registers.
        """
        for experiment in qobj.experiments:
            # If circuit contains classical registers but not
            # measurements raise a warning
            if experiment.config.memory_slots > 0:
                # Check if measure opts missing
                no_measure = True
                for op in experiment.instructions:
                    if not no_measure:
                        break  # we don't need to check any more ops
                    if no_measure and op.name == "measure":
                        no_measure = False
                # Print warning if clbits but no measure
                if no_measure:
                    logger.warning(
                        'No measurements in circuit "%s": '
                        'count data will return all zeros.',
                        experiment.header.name)
