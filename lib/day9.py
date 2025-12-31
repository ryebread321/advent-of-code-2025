import dataclasses
import itertools

from typing import Iterable


@dataclasses.dataclass(slots=True, frozen=True)
class Point:
    x: float
    y: float


def parse_point(point: str) -> Point:
    x, y = point.strip().split(",")
    return Point(x=float(x), y=float(y))


def parse_points(points: Iterable[str]) -> Iterable[Point]:
    return map(parse_point, points)


def max_area(points: Iterable[Point]) -> float:
    max_area = 0
    for p1, p2 in itertools.product(points, repeat=2):
        width = abs(p1.x - p2.x) + 1
        height = abs(p1.y - p2.y) + 1
        area = width * height
        max_area = max(max_area, area)
    return max_area


def solve_part_1(filepath: str) -> int:
    with open(filepath) as f:
        points = parse_points(f)
        return max_area(points)


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1("data/day9.txt")}")
