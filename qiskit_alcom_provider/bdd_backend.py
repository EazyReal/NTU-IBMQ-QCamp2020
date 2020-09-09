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
BDD backend for qasm simulator.
Implementation of the quantum simulator described in ``
Original Paper can be found at `https://arxiv.org/abs/2007.09304`.
This is a wrapper for executives from c++ files.
"""

import json
import logging
import datetime
import os
import time
import uuid
from numpy import ndarray

from typing import Union, Dict, Any, List, Tuple, Iterable

from qiskit.providers import BaseBackend, BaseProvider
from qiskit.providers.models import BackendStatus, BackendConfiguration
from qiskit.qobj import QasmQobjConfig, validate_qobj_against_schema
#from qiskit.result import Result, after hackathon todo
from qiskit.util import local_hardware_info # for how many quibit can be simulated
# to get quantm circuit
from qiskit.assembler import disassemble

# Local Import 
from .alcom_job import ALComJob
from .alcom_error import ALComError
from .trimmed_result import TrimResult as Result

# Import Pybind

# Logger
logger = logging.getLogger(__name__)

class AerJSONEncoder(json.JSONEncoder):
    """
    JSON encoder for NumPy arrays and complex numbers.
    This functions as the standard JSON Encoder but adds support
    for encoding:
        complex numbers z as lists [z.real, z.imag]
        ndarrays as nested lists.
    """

    # pylint: disable=method-hidden,arguments-differ
    def default(self, obj):
        if isinstance(obj, ndarray):
            return obj.tolist()
        if isinstance(obj, complex):
            return [obj.real, obj.imag]
        if hasattr(obj, "to_dict"):
            return obj.to_dict()
        return super().default(obj)

class BDDBackend(BaseBackend):
    """
    BDD backend for qasm simulator.
    Implementation of the quantum simulator described in ``
    Original Paper can be found at `https://arxiv.org/abs/2007.09304`.
    This is a wrapper for executives from c++ files.
    """

    def __init__(self,
                 controller,
                 configuration: BackendConfiguration,
                 provider: BaseProvider=None
                ):
        """
        This method should initialize the module and its configuration, and
        raise an exception if a component of the module is
        not available.
        Args:
            configuration (BackendConfiguration): backend configuration
            provider (BaseProvider): provider responsible for this backend
        Raises:
            FileNotFoundError if backend executable is not available.
            BDDError: if there is no name in the configuration
        """
        super().__init__(configuration=configuration, provider=provider)
        # TODO
        self._controller = controller

    # pylint: disable=arguments-differ
    def run(self, qobj, backend_options=None, noise_model=None, validate=True):
        """Run a qobj on the backend.
        Args:
            qobj (QasmQobj): The Qobj to be executed.
            backend_options (dict or None): dictionary of backend options
                                            for the execution (default: None).
            noise_model (NoiseModel or None): noise model to use for
                                              simulation (default: None).
            validate (bool): validate the Qobj before running (default: True).
        Returns:
            AerJob: The simulation job.
        Additional Information:
            * The entries in the ``backend_options`` will be combined with
              the ``Qobj.config`` dictionary with the values of entries in
              ``backend_options`` taking precedence.
            * If present the ``noise_model`` will override any noise model
              specified in the ``backend_options`` or ``Qobj.config``.
        """
        # Does not support NoiseModel Now 
        if noise_model is not None:
            raise NoiseModelNotSupportedError
        # Submit job
        job_id = str(uuid.uuid4())
        alcom_job = ALComJob(self, job_id, self._run_job, qobj,
                         backend_options, noise_model, validate)
        alcom_job.submit()
        return alcom_job

    def status(self):
        """Return backend status.
        Returns:
            BackendStatus: the status of the backend.
        """
        return BackendStatus(backend_name=self.name(),
                             backend_version=self.configuration().backend_version,
                             operational=True,
                             pending_jobs=0,
                             status_msg='')

    def _run_job(self, job_id, qobj, backend_options, noise_model, validate):
        """Run a qobj job"""
        start = time.time()
        if validate:
            validate_qobj_against_schema(qobj)
            self._validate(qobj, backend_options, noise_model)
        # convert to  format that can run on our simulator
        # and extract flag from backend_options
        qasm_str = self._get_qasm_str_from_qobj(qobj)
        use_statevector = backend_options
        # Now the output is of type TrimResult
        # TODO after hackathon prototype: use QOBJ, Result and ExperimentResult together
        output = self._controller(qasm_str)
        output = {
            "counts": output[0],
            "statevector": output[1],
        }
        ##########################
        self._validate_controller_output(output)
        end = time.time()
        return self._format_results(job_id, output, end - start)

    def _get_qasm_str_from_qobj(self, qobj):
        """
        convert to format(QASM) that can run on our simulator,
        we now assume that there is only one experiment(QC) (2020/9/9, YT Lin),
        can do multi-circuit easily by list comprehension 
        """
        original_config = qobj.config
        assert len(disassemble(qobj)[0]) == 1, "we now assume that there is only one experiment(QC) (2020/9/9, YT Lin)"
        qc = disassemble(qobj)[0][0]
        qasm_str = qc.qasm()
        # print(qasm_str)
        return qasm_str

    def _format_results(self, job_id, output, time_taken):
        """
        Construct Result object from simulator output.
        And add extra information.
        """
        # Add result metadata
        output["job_id"] = job_id
        output["date"] = datetime.datetime.now().isoformat()
        output["backend_name"] = self.name()
        output["backend_version"] = self.configuration().backend_version
        output["time_taken"] = time_taken
        return Result.from_dict(output) # is TrimResult

    def _validate_controller_output(self, output):
        """Validate output from the controller wrapper."""
        if not isinstance(output, dict):
            logger.error("%s: simulation failed.", self.name())
            if output:
                logger.error('Output: %s', output)
            raise ALComError("simulation terminated without returning valid output.")

    def _validate(self, qobj, backend_options, noise_model):
        """Validate the qobj, backend_options, noise_model for the backend"""
        pass

    def __repr__(self):
        """Official string representation of an ALComBackend."""
        display = "{}('{}')".format(self.__class__.__name__, self.name())
        provider = self.provider()
        if provider is not None:
            display = display + " from {}()".format(provider)
        return "<" + display + ">"