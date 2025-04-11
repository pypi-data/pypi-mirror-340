from dataclasses import dataclass
import logging
from typing import Optional, override

import networkx as nx
import dwave_networkx as dnx

from quark.core import Core
from quark.interface_types.qubo import Qubo

@dataclass
class TspQuboMappingDnx(Core):
    """
    A module for mapping a graph to a QUBO formalism for the TSP problem
    """


    @override
    def preprocess(self, data: nx.Graph) -> Qubo:
        self._graph = data
        q = dnx.traveling_salesperson_qubo(data)
        return Qubo.from_dict(q)

    @override
    def postprocess(self, data: dict) -> Optional[list[int]]:
        relevant_data = filter(lambda x: x[1] == 1, data.items())
        tuples = map(lambda x: x[0], relevant_data)
        sorted_tuples = sorted(tuples, key=lambda x: x[1])
        path = map(lambda x: x[0], sorted_tuples)
        time_steps = map(lambda x: x[1], sorted_tuples)

        if list(time_steps) != list(range(self._graph.number_of_nodes())):
            logging.warn("Invalid route")
            return None

        return list(path)
