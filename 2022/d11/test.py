from solution import (
    Monkey,
    MonkeyOperation,
    MonkeyTest,
    readInput,
    GetMonkeyBusiness,
)
from collections import deque
import logging


def test_read_input():
    input1 = readInput("input_1.txt")

    expected = [
        Monkey(deque([79, 98]), MonkeyOperation("*", "19"), MonkeyTest(23, 2, 3)),
        Monkey(
            deque([54, 65, 75, 74]),
            MonkeyOperation("+", "6"),
            MonkeyTest(19, 2, 0),
        ),
        Monkey(
            deque([79, 60, 97]),
            MonkeyOperation("*", "old"),
            MonkeyTest(13, 1, 3),
        ),
        Monkey(deque([74]), MonkeyOperation("+", "3"), MonkeyTest(17, 0, 1)),
    ]

    assert input1 == expected


def test_part_1_input_1():
    input1 = readInput("input_1.txt")
    assert GetMonkeyBusiness(input1, True).runRounds(20) == 10605


def test_part_1_solution():
    mainInput = readInput("input_main.txt")
    logging.info(GetMonkeyBusiness(mainInput, True).runRounds(20))


def test_part_2_input_1():
    input1 = readInput("input_1.txt")
    assert GetMonkeyBusiness(input1, False).runRounds(10000) == 2713310158


def test_part_2_solution():
    mainInput = readInput("input_main.txt")
    logging.info(GetMonkeyBusiness(mainInput, False).runRounds(10000))
