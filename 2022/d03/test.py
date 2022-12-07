import os
from solution import getItemPriority, sumViolatingItemPriorities, sumBadgeTypes

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d03", filename)


def readInput(filename: str) -> list[str]:
    rucksacks = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            rucksacks.append(line.strip())

    return rucksacks


input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_getItemPriority_1():
    assert getItemPriority("b") == 2


def test_getItemPriority_2():
    assert getItemPriority("B") == 28


def test_part1_input_1():
    assert sumViolatingItemPriorities(input1) == 157


def test_part1_solution():
    print(sumViolatingItemPriorities(mainInput))


def test_part2_input_1():
    assert sumBadgeTypes(input1) == 70


def test_part2_solution():
    print(sumBadgeTypes(mainInput))
