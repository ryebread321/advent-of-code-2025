import dataclasses
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

    def rotate_left(self, n: int) -> None:
        self._rotate(n, -1)

    def rotate_right(self, n: int) -> None:
        self._rotate(n, 1)

    def _rotate(self, n: int, sign: int) -> None:
        assert n >= 0
        assert sign != 0

        self.position = (self.position + n * sign) % self.num_ticks

    @property
    def num_ticks(self) -> int:
        return self.high - self.low + 1


class PasswordSolver:

    def solve(self, dial: Dial, rotations: Iterable[str]) -> int:
        password = 0
        for rotation in rotations:
            self._rotate_dial(dial, rotation)
            if dial.position == 0:
                password += 1
        return password

    def _rotate_dial(self, dial: Dial, rotation: str) -> None:
        direction = rotation[0]
        n = int(rotation[1:])
        match direction:
            case "L":
                dial.rotate_left(n)
            case "R":
                dial.rotate_right(n)
            case _:
                raise ValueError(f"Invalid direction: {direction}")


if __name__ == "__main__":
    with open("data/day1.txt") as rotations:
        dial = Dial(position=50, low=0, high=99)
        solver = PasswordSolver()
        password = solver.solve(dial, rotations)
        print(f"Password: {password}")
