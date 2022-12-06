import os
from solution import calculateMoveStrategyScore, calculateResultStrategyScore

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d02", filename)


def readInput(filename: str) -> list[tuple[int, int]]:
    rounds = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if len(line.strip()) < 1:
                continue

            theyPlay, youPlay = line.split(" ")
            rounds.append((theyPlay.strip(), youPlay.strip()))

    return rounds


input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_part1():
    assert calculateMoveStrategyScore(input1) == 15


def test_part1_solution():
    print(calculateMoveStrategyScore(mainInput))


def test_part2():
    assert calculateResultStrategyScore(input1) == 12


def test_part2_solution():
    print(calculateResultStrategyScore(mainInput))
