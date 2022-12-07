import os
from collections import deque
from solution import (
    rearrangeAndGetTopOfStacks,
    applyCrateMover9000Move,
    applyCrateMover9001Move,
)

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d05", filename)


# Parse a single level of crates.
def parseStackLine(line: str) -> list[str]:
    crates = []

    for i in range(0, len(line), 4):
        crate = line[i : i + 3]

        if len(crate.strip()) < 1:
            crates.append(None)
        else:
            crates.append(crate[1])

    return crates


# Parse a single move.
def parseMoveLine(line: str) -> tuple[int, int, int]:
    tokens = line.split(" ")
    return (int(tokens[1]), int(tokens[3]), int(tokens[5]))


# Cursed input parsing...
def readInput(filename: str) -> tuple[list[list[str]], list[tuple[int, int, int]]]:
    stackLines = []
    moves = []

    # "Quick" and dirty parsing strategy to get just the lines that need to be
    # parsed and not for instance, blank lines, crate column labels, etc.
    # Another downside is this puts the whole input in memory, but this isn't a
    # huge deal with the size of this input.
    with open(getAbsolutePath(filename)) as f:
        # Flag to switch from accumulating arrangement lines to accumulating
        # move lines. Hate this...
        parsingArrangement = True

        for line in f:
            if len(line.strip()) < 1:
                parsingArrangement = False
                continue

            if parsingArrangement:
                stackLines.append(line)
            else:
                moves.append(parseMoveLine(line))

    # Pop off the column labels line from the arrangement.
    stackLines.pop()

    # Parsing the first row ahead of time is necessary to initialize the length
    # of the list of stacks.
    firstRow = parseStackLine(stackLines[-1])
    stacks = [[crate] for crate in firstRow]

    # Create the final stacks input.
    for i in range(len(stackLines) - 2, -1, -1):
        parsedRow = parseStackLine(stackLines[i])

        for j, crate in enumerate(parsedRow):
            if crate is None:
                continue

            stacks[j].append(crate)

    return (stacks, moves)


def test_parse():
    input1 = readInput(getAbsolutePath("input_1.txt"))
    expectedArrangement = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]

    expectedMoves = [(1, 2, 1), (3, 1, 3), (2, 2, 1), (1, 1, 2)]

    assert input1 == (expectedArrangement, expectedMoves)


def test_part_1_input_1():
    input1 = readInput(getAbsolutePath("input_1.txt"))
    stacks, moves = input1
    assert rearrangeAndGetTopOfStacks(stacks, moves, applyCrateMover9000Move) == "CMZ"


def test_part_1_solution():
    mainInput = readInput(getAbsolutePath("input_main.txt"))
    stacks, moves = mainInput
    print(rearrangeAndGetTopOfStacks(stacks, moves, applyCrateMover9000Move))


def test_part_2_input_1():
    input1 = readInput(getAbsolutePath("input_1.txt"))
    stacks, moves = input1
    assert rearrangeAndGetTopOfStacks(stacks, moves, applyCrateMover9001Move) == "MCD"


def test_part_2_solution():
    mainInput = readInput(getAbsolutePath("input_main.txt"))
    stacks, moves = mainInput
    print(rearrangeAndGetTopOfStacks(stacks, moves, applyCrateMover9001Move))
