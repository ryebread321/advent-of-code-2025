import abc
import dataclasses
import math

from typing import Iterable


@dataclasses.dataclass(slots=True)
class Dial:
    position: int
    low: int
    high: int

    def __post_init__(self) -> None:
        assert self.low >= 0
        assert self.high > self.low
        assert self.low <= self.position <= self.high

    def rotate_left(self, n: int) -> int:
        return self._rotate(n, -1)

    def rotate_right(self, n: int) -> int:
        return self._rotate(n, 1)

    def _rotate(self, n: int, sign: int) -> int:
        assert n >= 0

        unbounded_position = self.position + math.copysign(n, sign)
        self.position = math.fmod(unbounded_position, self.num_ticks) + self.low

        if sign < 0:
            num_low_passes = abs((unbounded_position - 1) // self.num_ticks)
        else:
            num_low_passes = abs(unbounded_position // self.num_ticks)

        return int(num_low_passes)

    @property
    def num_ticks(self) -> int:
        return self.high - self.low + 1


def rotate_dial(dial: Dial, rotation: str) -> int:
    n = int(rotation[1:])
    match (direction := rotation[0]):
        case "L":
            return dial.rotate_left(n)
        case "R":
            return dial.rotate_right(n)
        case _:
            raise ValueError(f"Invalid direction: {direction}")


def solve_part_1() -> int:
    with open("data/day1.txt") as rotations:
        dial = Dial(position=50, low=0, high=99)
        password = 0
        for rotation in rotations:
            rotate_dial(dial, rotation)
            if dial.position == 0:
                password += 1
        return password

"""
Guesses:

204 - too low
5366
6486
7109
7533
7676
9850 - too high
"""
def solve_part_2() -> None:
    with open("data/day1.txt") as rotations:
        dial = Dial(position=50, low=0, high=99)
        password = sum(rotate_dial(dial, r) for r in rotations)
        return password


if __name__ == "__main__":
    print(f"Password: {solve_part_1()}")
    print(f"Password: {solve_part_2()}")
