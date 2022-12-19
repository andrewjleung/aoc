from solution import (
    Monkey,
    MonkeyOperation,
    MonkeyTest,
    readInput,
    getMonkeyBusinessAfterTwentyRounds,
)
from collections import deque

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    expected = [
        Monkey(
            deque([79, 98]), MonkeyOperation("old", "*", "19"), MonkeyTest(23, 2, 3)
        ),
        Monkey(
            deque([54, 65, 75, 74]),
            MonkeyOperation("old", "+", "6"),
            MonkeyTest(19, 2, 0),
        ),
        Monkey(
            deque([79, 60, 97]),
            MonkeyOperation("old", "*", "old"),
            MonkeyTest(13, 1, 3),
        ),
        Monkey(deque([74]), MonkeyOperation("old", "+", "3"), MonkeyTest(17, 0, 1)),
    ]

    assert input1 == expected


def test_part_1_input_1():
    assert getMonkeyBusinessAfterTwentyRounds(input1) == 10605
