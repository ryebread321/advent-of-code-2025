import dataclasses
import itertools
import numpy as np
from scipy import sparse

START_SYMBOL = "S"
SPLITTER_SYMBOL = "^"
EMPTY_SYMBOL = "."
MAX_CAPACITY = 100_000


@dataclasses.dataclass(slots=True)
class MaxFlowGraph:
    nodes: int
    source: int
    sink: int


def get_max_flow_graph(diagram: Iterable[str]) -> MaxFlowGraph:
    nodes = 0
    source = None
    for symbol in itertools.chain.from_iterable(diagram):
        if symbol == START_SYMBOL:
            source = nodes
        nodes += 1
    # Increment nodes to include the sink node.
    return MaxFlowGraph(nodes=nodes + 1, source=source, sink=nodes)


def get_max_flow_capacity(
    graph: MaxFlowGraph, diagram: Iterable[str]
) -> sparse.sparray:
    # List-of-lists format is efficient for incremental construction.
    # Ref: https://en.wikipedia.org/wiki/Sparse_matrix#Storage
    capacity = sparse.lil_array((graph.nodes, graph.nodes), dtype=np.int32)
    i = 0
    for line in diagram:
        for symbol in line:
            if symbol == EMPTY_SYMBOL or symbol == START_SYMBOL:
                # Add capacity to the symbol below i in the diagram.
                if (k := i + len(line)) < graph.nodes - 1:
                    capacity[i, k] = MAX_CAPACITY
            elif symbol == SPLITTER_SYMBOL:
                # Add 1 capacity to the sink node to count the number of splits.
                capacity[i, graph.sink] = 1
                # Add max capacity to the adjacent nodes to model the beam splitting.
                capacity[i, i - 1] = MAX_CAPACITY
                capacity[i, i + 1] = MAX_CAPACITY
            i += 1
    # Compressed-sparse-row format is efficient for access
    # Ref: https://en.wikipedia.org/wiki/Sparse_matrix#Storage
    return capacity.tocsr()


def compute_tachyon_beam_splits(diagram: list[str]) -> int:
    graph = get_max_flow_graph(diagram)
    capacity = get_max_flow_capacity(graph, diagram)
    result = sparse.csgraph.maximum_flow(capacity, graph.source, graph.sink)
    return result.flow_value


def solve_part_1():
    with open("data/day7.txt") as f:
        return compute_tachyon_beam_splits(f.readlines())


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
