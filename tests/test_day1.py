from lib import day1

import pytest


@pytest.mark.parametrize("n,expected", [(0, 0), (10, 0), (50, 1), (51, 1), (279, 3)])
def test_dial_left_num_low_passes(n, expected):
    dial = day1.Dial(position=30, low=0, high=99)
    assert dial.rotate_left(n) == expected


@pytest.mark.parametrize("n,expected", [(0, 0), (10, 0), (69, 0), (70, 1), (279, 3)])
def test_dial_right_num_low_passes(n, expected):
    dial = day1.Dial(position=30, low=0, high=99)
    assert dial.rotate_right(n) == expected
