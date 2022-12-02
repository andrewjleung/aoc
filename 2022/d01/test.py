import os
from solution import maxCaloriesPerElf, caloriesOfTopThreeElves

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

        elves.append(curr)

    return elves


input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_part1():
    assert maxCaloriesPerElf(input1) == 24000


def test_part1_solution():
    print(maxCaloriesPerElf(mainInput))


def test_part2():
    assert set(caloriesOfTopThreeElves(input1)) == set([24000, 11000, 10000])


def test_part2_solution():
    print(sum(caloriesOfTopThreeElves(mainInput)))
