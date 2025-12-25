import copy
import dataclasses
import heapq
import itertools
from typing import Iterable

import networkx as nx
import numpy as np
from numpy.typing import NDArray


# Use left value as the tie breaker when distances are equal
# for multiple items in the heap.
# Ref: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
@dataclasses.dataclass(slots=True, order=True)
class HeapItem:
    distance: float
    left: int
    right: int


Heap = list[HeapItem]


def parse_position(position: str) -> NDArray:
    x, y, z = position.split(",")
    return np.array([int(x), int(y), int(z)])


def parse_positions(positions: Iterable[str]) -> list[NDArray]:
    return [parse_position(p) for p in positions]


def build_distance_matrix(positions: list[NDArray]) -> dict[tuple, float]:
    distances = {}
    for i, p_i in enumerate(positions):
        for j, p_j in enumerate(positions):
            if i < j:
                distances[(i, j)] = np.linalg.norm(p_i - p_j)
    return distances


def build_heap(distances: dict[tuple, float]) -> Heap:
    heap = []
    for (i, j), distance in distances.items():
        item = HeapItem(distance=distance, left=i, right=j)
        heapq.heappush(heap, item)
    return heap


def compute_components(heap: Heap, n: int) -> Iterable[set]:
    heap = copy.copy(heap)
    graph = nx.Graph()
    for _ in range(min(len(heap), n)):
        item = heapq.heappop(heap)
        graph.add_edge(item.left, item.right)
    return nx.algorithms.components.connected_components(graph)


def compute_component_size_product(components: Iterable[set], k: int) -> int:
    sizes = sorted(map(len, components), reverse=True)
    return int(np.prod(sizes[:k]))


def solve_part_1(filepath: str, n: int, k: int) -> int:
    with open(filepath) as f:
        positions = parse_positions(f)
        distances = build_distance_matrix(positions)
        heap = build_heap(distances)
        components = compute_components(heap, n)
        product = compute_component_size_product(components, k)
        return product


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1("data/day8.txt", n=1000, k=3)}")
