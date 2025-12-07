import enum
import functools
import operator
import re
from typing import Callable, Iterable

import numpy as np
from numpy.typing import NDArray

Ints = Iterable[int]
IntReducer = Callable[[Ints], int]
IntReducers = Iterable[IntReducer]


class ParsingStrategy(enum.Enum):
    ROW = enum.auto()
    REVERSED_COLUMN = enum.auto()


def multiply(ints: Ints) -> int:
    return functools.reduce(operator.mul, ints, initial=1)


def parse_reducer(string: str) -> IntReducer:
    match (string):
        case "*":
            return multiply
        case "+":
            return sum
        case _:
            raise ValueError(f"Unknown symbol: '{string}'")


def parse_rows(char_array: NDArray) -> Ints:
    return (int("".join(row)) for row in char_array)


def parse_reversed_columns(char_array: NDArray) -> Ints:
    int_strings = ("".join(row) for row in np.rot90(char_array))
    return (int(s) for s in int_strings if not s.isspace())


def parse_args(char_array: NDArray, strategy: ParsingStrategy) -> Ints:
    match (strategy):
        case ParsingStrategy.ROW:
            return parse_rows(char_array)
        case ParsingStrategy.REVERSED_COLUMN:
            return parse_reversed_columns(char_array)


def parse_expressions(
    lines: list[str], strategy: ParsingStrategy
) -> tuple[IntReducers, Iterable[Ints]]:
    lines = [line.rstrip() for line in lines]

    reducer_strings = re.split("\\s+", lines[-1])
    reducers = map(parse_reducer, reducer_strings)

    char_array = np.array([list(line) for line in lines[:-1]])
    cuts = np.flatnonzero(np.all(char_array == " ", axis=0))
    char_arrays = np.hsplit(char_array, cuts)
    args = (parse_args(arr, strategy) for arr in char_arrays)

    return reducers, args


def sum_expressions(reducers: IntReducers, args: Iterable[Ints]) -> int:
    return sum(reducer(ints) for reducer, ints in zip(reducers, args))


def solve_part_1() -> int:
    with open("data/day6.txt") as f:
        reducers, args = parse_expressions(f.readlines(), ParsingStrategy.ROW)
        return sum_expressions(reducers, args)


def solve_part_2() -> int:
    with open("data/day6.txt") as f:
        reducers, args = parse_expressions(
            f.readlines(), ParsingStrategy.REVERSED_COLUMN
        )
        return sum_expressions(reducers, args)


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
    print(f"Part 2: {solve_part_2()}")
