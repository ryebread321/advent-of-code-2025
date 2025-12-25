import collections
import dataclasses
import heapq
import itertools
from typing import Iterable

import networkx as nx
import numpy as np
from numpy.typing import NDArray

# Use named tuples for convience when computing distances.
Position = collections.namedtuple("Position", "x y z")


# Use left value as the tie breaker when distances are equal
# for multiple items in the heap.
# Ref: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
@dataclasses.dataclass(slots=True, order=True)
class HeapItem:
    distance: float
    left: int
    right: int


Heap = list[HeapItem]


def parse_position(position: str) -> Position:
    x, y, z = position.split(",")
    return Position(x=int(x), y=int(y), z=int(z))


def parse_positions(positions: Iterable[str]) -> list[Position]:
    return [parse_position(p) for p in positions]


def build_distance_matrix(positions: list[Position]) -> NDArray:
    distances = np.zeros((len(positions), len(positions)))
    for i, pi in enumerate(positions):
        for j, pj in enumerate(positions):
            distances[i, j] = np.linalg.norm(np.array(pi) - np.array(pj))
    return distances


def build_heap(distances: NDArray) -> Heap:
    heap = []
    indices = range(len(distances))
    for i, j in itertools.product(indices, repeat=2):
        if i != j:
            item = HeapItem(distance=distances[i, j], left=i, right=j)
            heapq.heappush(heap, item)
    return heap


def compute_components(heap: Heap, n: int) -> Iterable[set]:
    heap = heap.copy()
    graph = nx.Graph()
    for _ in range(n):
        item = heapq.heappop(heap)
        graph.add_edge(item.left, item.right)
    return nx.algorithms.components.connected_components(graph)


def compute_component_size_product(components: Iterable[set], n: int) -> int:
    sizes = sorted(map(len, components), reverse=True)
    return int(np.prod(sizes[:n]))


def solve_part_1() -> int:
    with open("data/day8.txt") as f:
        positions = parse_positions(f)
        distances = build_distance_matrix(positions)
        heap = build_heap(distances)
        components = compute_components(heap, 1000)
        product = compute_component_size_product(components, 3)
        return product


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
