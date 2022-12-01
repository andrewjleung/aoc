import os
from solution import maxCaloriesPerElf

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d01", filename)


def readInput(filename: str) -> list[list[int]]:
    elves = []

    with open(getAbsolutePath(filename)) as f:
        curr = []

        for line in f:
            if line == "\n" or len(line.strip()) < 1:
                elves.append(curr)
                curr = []
            else:
                curr.append(int(line))

    return elves


def test_1():
    assert maxCaloriesPerElf(readInput("input2.txt")) == 24000


def test_solution():
    print(maxCaloriesPerElf(readInput("input1.txt")))
