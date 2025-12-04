import numpy as np
from scipy import signal

from numpy.typing import NDArray


def parse_grid(grid: list[str]) -> NDArray:
    n_rows = len(grid)
    n_cols = len(grid[0])
    parsed = np.zeros((n_rows, n_cols), dtype=np.int8)
    for i, row in enumerate(grid):
        for j, element in enumerate(row):
            if element == "@":
                parsed[i, j] = 1
    return parsed


def compute_reachable_cells(grid: NDArray) -> NDArray:
    # Also set the center to 1 to disambiguate a non-empty cell surrounded by empty
    # cells and an empty cell surrounded by empty cells.
    kernel = np.ones((3, 3), dtype=np.int8)
    conv = signal.convolve2d(grid, kernel, mode="same", boundary="fill", fillvalue=0)
    counts = grid * conv
    # Increment the upper threshold from 4 to 5 to avoid counting the center cell.
    return (counts > 0) & (counts < 5)


def compute_num_reachable_cells(grid: NDArray) -> int:
    reachable = compute_reachable_cells(grid)
    return np.count_nonzero(reachable)


def compute_num_reachable_cells_with_removal(grid: NDArray) -> int:
    total = 0
    reachable = 1
    while reachable > 0:
        mask = compute_reachable_cells(grid)
        reachable = np.count_nonzero(mask)
        total += reachable
        grid *= ~mask
    return total


def solve_part_1():
    with open("data/day4.txt") as f:
        lines = [line.rstrip() for line in f]
        grid = parse_grid(lines)
        return compute_num_reachable_cells(grid)


def solve_part_2():
    with open("data/day4.txt") as f:
        lines = [line.rstrip() for line in f]
        grid = parse_grid(lines)
        return compute_num_reachable_cells_with_removal(grid)


if __name__ == "__main__":
    print("Part 1:", solve_part_1())
    print("Part 2:", solve_part_2())
