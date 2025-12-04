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


def compute_num_reachable_cells(grid: NDArray) -> int:
    # Also set the center to 1 to disambiguate a non-empty cell surrounded by empty
    # cells and an empty cell surrounded by empty cells.
    kernel = np.ones((3, 3), dtype=np.int8)
    conv = signal.convolve2d(grid, kernel, mode="same", boundary="fill", fillvalue=0)
    counts = grid * conv
    # Increment the upper threshold from 4 to 5 to avoid counting the center cell.
    return np.count_nonzero((counts > 0) & (counts < 5))


def solve_part_1():
    with open("data/day4.txt") as f:
        lines = [line.rstrip() for line in f]
        grid = parse_grid(lines)
        return compute_num_reachable_cells(grid)


if __name__ == "__main__":
    print("Part 1:", solve_part_1())
