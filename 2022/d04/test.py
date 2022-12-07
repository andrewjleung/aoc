import os
from solution import countAssignmentsWithFullOverlap, countAssignmentsWithOverlap

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d04", filename)


def parseRange(rangeStr: str) -> tuple[int, int]:
    splitRangeStr = rangeStr.split("-")
    return (int(splitRangeStr[0]), int(splitRangeStr[1]))


def readInput(filename: str) -> tuple[tuple[int, int], tuple[int, int]]:
    assignmentPairs = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            range1, range2 = line.split(",")
            assignmentPairs.append((parseRange(range1), parseRange(range2)))

    return assignmentPairs


input1 = readInput(getAbsolutePath("input_1.txt"))
mainInput = readInput(getAbsolutePath("input_main.txt"))


def test_part1_input_1():
    assert countAssignmentsWithFullOverlap(input1) == 2


def test_part1_solution():
    print(countAssignmentsWithFullOverlap(mainInput))


def test_part2_input_1():
    assert countAssignmentsWithOverlap(input1) == 4


def test_part2_solution():
    print(countAssignmentsWithOverlap(mainInput))
