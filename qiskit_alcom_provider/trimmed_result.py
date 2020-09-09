from typing import Dict, List, Any, Union
import copy
from qiskit.result import Result
from qiskit.quantum_info.states import Statevector
# cannot inherit Result here for missing params for super init

JsonDict = Dict[str, Any]

class TrimResult():
    """
    from YanTong Lin
    for eazy result in 2020 NTU-IBMQ Q-Camp
    supports get_statevector and get_counts as API
    """
    def __init__(self, counts=None, statevector=None, **kwargs):
        # super(TrimResult, self).__init__()
        self._meta_data = {}
        self._meta_data["counts"] = counts
        self._meta_data["statevector"] = statevector
        self._meta_data.update(kwargs)
    
    def get_statevector(self):
        real = self._meta_data["statevector"][0]
        image = self._meta_data["statevector"][1]
        statevector = Statevector([complex(r,i) for r, i in zip(real, image)])
        return statevector
    
    def get_counts(self):
        return self._meta_data["counts"]
    
    def to_dict(self):
        """Return a dictionary format representation of the Result
        Returns:
            dict: The dictionary form of the Result
        """
        out_dict = {}
        out_dict.update(self._meta_data)
        return out_dict
    
    @classmethod
    def from_dict(cls, data: JsonDict):
        """Create a new `TrimResult` object from a dictionary.
        Args:
            data (dict): A dictionary representing the Result to create. It
                         will be in the same format as output by
                         :meth:`to_dict`.
        Returns:
            Result: The ``TrimResult`` object from the input dictionary.
        """
        in_data = copy.copy(data)
        return cls(**in_data)