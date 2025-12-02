"""
NOTES:

Definitions:

- Product ID: positive integer
- Product ID range: 'xxx-yyy' (closed interval)
- Product ID ranges: comma-delimited list
- Invalid product ID: a product ID comprised of digits that repeat twice
    - Need a function that determines if a string is symmetric

Algorithm:

Input: list of product ID ranges
Output: sum of invalid product IDs

total = 0
for each product ID range R:
    for each product ID i in R:
        if i is invalid:
            total += i
return total
"""

from typing import Iterable


def parse_product_ids(value: str) -> Iterable[int]:
    for rng in value.split(","):
        start, end = rng.strip().split("-")
        start = int(start.strip())
        end = int(end.strip())
        yield from range(start, end + 1)


def is_invalid(product_id: int) -> bool:
    product_id = str(product_id)
    n = len(product_id)
    if n < 2 or n % 2:
        return False
    pivot = n // 2
    return product_id[pivot:] == product_id[:pivot]


def sum_invalid_product_ids(product_ids: Iterable[int]) -> int:
    return sum(i for i in product_ids if is_invalid(i))


def solve_part_1():
    with open("data/day2.txt") as f:
        product_ids = parse_product_ids(f.readline())
        return sum_invalid_product_ids(product_ids)


if __name__ == "__main__":
    print(f"Sum of invalid product IDs: {solve_part_1()}")
