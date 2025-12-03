from typing import Iterable


def parse_product_ids(value: str) -> Iterable[int]:
    for rng in value.split(","):
        start, end = rng.strip().split("-")
        start = int(start.strip())
        end = int(end.strip())
        yield from range(start, end + 1)


def is_symmetric(product_id: int) -> bool:
    product_id = str(product_id)
    n = len(product_id)
    if n < 2 or n % 2:
        return False
    pivot = n // 2
    return product_id[pivot:] == product_id[:pivot]


def is_repeating(product_id: int) -> bool:
    product_id = str(product_id)
    for i in range(1, len(product_id) // 2 + 1):
        pattern = product_id[:i]
        result = product_id.split(pattern)
        if all(len(diff) == 0 for diff in result):
            return True
    return False


def sum_symmetric_product_ids(product_ids: Iterable[int]) -> int:
    return sum(i for i in product_ids if is_symmetric(i))


def sum_repeating_product_ids(product_ids: Iterable[int]) -> int:
    return sum(i for i in product_ids if is_repeating(i))


def solve_part_1():
    with open("data/day2.txt") as f:
        product_ids = parse_product_ids(f.readline())
        return sum_symmetric_product_ids(product_ids)


def solve_part_2():
    with open("data/day2.txt") as f:
        product_ids = parse_product_ids(f.readline())
        return sum_repeating_product_ids(product_ids)


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
    print(f"Part 2: {solve_part_2()}")
