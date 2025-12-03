from typing import Iterable


def parse_battery_banks(banks: Iterable[str]) -> Iterable[list[int]]:
    for bank in banks:
        yield [int(joltage) for joltage in bank]


def max_bank_joltage(bank: list[int]) -> int:
    if (n := len(bank)) < 2:
        return max(bank, default=0)
    ten_idx = 0
    one_idx = 1
    for i in range(1, n - 1):
        if bank[i] > bank[ten_idx]:
            ten_idx = i
            one_idx = i + 1
        elif bank[i + 1] > bank[one_idx]:
            one_idx = i + 1
    return bank[ten_idx] * 10 + bank[one_idx]


def max_sum_output_joltage(banks: Iterable[list[int]]) -> int:
    return sum(map(max_bank_joltage, banks))


def solve_part_1() -> int:
    with open("data/day3.txt") as f:
        lines = (line.rstrip() for line in f)
        banks = parse_battery_banks(lines)
        return max_sum_output_joltage(banks)


if __name__ == "__main__":
    print(f"Part 1: {solve_part_1()}")
