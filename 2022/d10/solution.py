import os
from collections import deque
from dataclasses import dataclass

"""
PART 1 

There is a CPU that ticks at a constant rate. It has a single register `X`, 
which starts with the value `1`.

The CPU supports two instructions:

1. `addx V` takes two cycles to complete, and increases the value of the `X` 
   register by `V`.
2. `noop` takes one cycle to complete, and does nothing.

The input is a program containing a sequence of instructions.

Signal strength is the current cycle multiplied by the value in `X`.

Find the signal strength at the 20th, 60th, 100th, 140th, 180th, and 220th 
cycles and return the sum of them.
"""

"""
PART 2

The `X` register controls the horizontal position of the center of a 
3-pixel-wide sprite in a horizontal line. There is no vertical position.

The screen is a grid 40 pixels wide and 6 pixels high. It is drawn left to 
right, top to bottom, and a single pixel is drawn each cycle.

If, based upon the position of the sprite, any pixel of it overlaps the position
currently being drawn on the screen, then that pixel is drawn as lit (#).
Otherwise, it is drawn as dark (.).

Render the screen.
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d10", filename)


def readInput(filename: str) -> list[str]:
    with open(getAbsolutePath(filename)) as f:
        return f.readlines()


# Given a list of instructions, return the value of register `X` at every cycle
# where work is being done.
def simulateInstructions(instructions: list[str]) -> list[int]:
    X = 1
    cycle = 1
    instructionPointer = 0
    cycleStates = []

    def executeCycle():
        nonlocal X, cycle
        cycleStates.append(X)
        cycle += 1

    while instructionPointer < len(instructions):
        instruction = instructions[instructionPointer]
        instructionPointer += 1
        tokens = instruction.strip().split(" ")

        if tokens[0] == "noop":
            executeCycle()
        elif tokens[0] == "addx":
            executeCycle()
            executeCycle()
            X += int(tokens[1])

    # Execute the last cycle in case the last command was an `addx`. Note that
    # this may lead to an extra redundant cycle being executed.
    executeCycle()
    return cycleStates


MEASURE_CYCLES = set([20, 60, 100, 140, 180, 220])

# Simulate the running of the given list of instructions and sum the signal
# strength at certain cycles.
def simulateInstructionsAndSumSignalStrengths(instructions: list[str]) -> int:
    cycleStates = simulateInstructions(instructions)
    signalStrengthSum = 0

    for i, X in enumerate(cycleStates):
        cycle = i + 1

        if cycle in MEASURE_CYCLES:
            signalStrengthSum += X * cycle

    return signalStrengthSum


SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6

# Render a CRT screen based upon the given instructions.
def renderScreen(instructions: list[str]) -> int:
    cycleStates = simulateInstructions(instructions)
    render = [["." for _ in range(SCREEN_WIDTH)] for _ in range(SCREEN_HEIGHT)]

    for i, X in enumerate(cycleStates):
        cycle = i + 1

        if cycle > SCREEN_HEIGHT * SCREEN_WIDTH:
            break

        row, col = i // SCREEN_WIDTH, i % SCREEN_WIDTH

        if abs(col - X) <= 1:
            render[row][col] = "#"

    return ["".join(row) for row in render]
