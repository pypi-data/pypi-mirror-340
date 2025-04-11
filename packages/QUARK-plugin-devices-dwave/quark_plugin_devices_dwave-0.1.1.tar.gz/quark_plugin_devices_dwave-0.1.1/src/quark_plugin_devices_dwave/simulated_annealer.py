from dataclasses import dataclass
from typing import override

import dwave.samplers

from quark.core import Core
from quark.interface_types.qubo import Qubo

@dataclass
class SimulatedAnnealer(Core):
    """
    A module for solving a qubo problem using simulated annealing

    :param num_reads: The number of reads to perform
    """

    num_reads: int = 100

    @override
    def preprocess(self, data: Qubo) -> None:
        device = dwave.samplers.SimulatedAnnealingSampler()
        self._result = device.sample_qubo(data.as_dict(), num_reads=self.num_reads)


    @override
    def postprocess(self, data: None) -> dict:
        return self._result.lowest().first.sample # type: ignore
