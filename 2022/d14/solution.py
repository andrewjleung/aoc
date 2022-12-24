import logging
import os
from dataclasses import dataclass
from typing import Set
import math

"""
PART 1

You are in a cave filling with sand. The cave is represented as a 2-D grid with 
rock cells and air cells. Rock formations are specified as sequences of 
coordinates representing how to draw the rock formation on the grid in straight
horizontal or vertical lines. The rest of the grid is air.

Sand falls from coordinate (500, 0) and falls a single unit one cell large at a 
time. Once it comes to rest, the next unit of sand falls. Sand falls according
to the following rules:

Sand will always fall down one step if possible. If the cell right below is 
blocked, it will first try to move diagonally down to the left one cell. If that
is blocked, it will try to move diagonally down to the right one cell. If that 
is blocked, then it comes to rest.

Sand may fall keep falling indefinitely if it flows out of the bottom of the 
rock structures. 

Return the number of units of sand that come to rest before the remaining sand
starts flowing into the abyss.
"""

"""
PART 2

The difference here is that sand can now rest on the floor below the lowest rock
formation, and the ending condition of the simulation is that there is a unit of
sand resting in the sand starting position. A few changes to the original 
simulation can achieve this.
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d14", filename)


def readInput(filename: str):
    rockFormations = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if line == "\n":
                continue

            line = line.strip()
            coordinates = line.split(" -> ")
            separatedCoordinates = [
                tuple([int(element) for element in coordinate.split(",")])
                for coordinate in coordinates
            ]
            rockFormations.append(separatedCoordinates)

    return rockFormations


def bidiRange(x: int, y: int):
    if x <= y:
        return range(x, y)

    return reversed(range(y + 1, x + 1))


def getRockCells(rockFormations: list[list[tuple[int, int]]]) -> Set[tuple[int, int]]:
    def getRockCellsFromRockFormation(
        rockFormation: list[tuple[int, int]]
    ) -> Set[tuple[int, int]]:
        rockCells = set()

        for i in range(0, len(rockFormation) - 1):
            c1, c2 = rockFormation[i], rockFormation[i + 1]
            c1x, c1y = c1
            c2x, c2y = c2

            # Add all cells between c1 and c2, not including c2.
            if c1x == c2x:
                for y in bidiRange(c1y, c2y):
                    rockCells.add((c1x, y))
            elif c1y == c2y:
                for x in bidiRange(c1x, c2x):
                    rockCells.add((x, c1y))
            else:
                raise ValueError("Malformed rock formation.")

        # Add the last cell.
        rockCells.add(rockFormation[-1])

        return rockCells

    rockCells = set()

    for rockFormation in rockFormations:
        rockCells = rockCells.union(getRockCellsFromRockFormation(rockFormation))

    return rockCells


def findLowestRockCell(rockCells: Set[tuple[int, int]]) -> int:
    lowestY = -math.inf
    for _, y in rockCells:
        lowestY = max(lowestY, y)
    return lowestY


DIRECTIONS = [(0, 1), (-1, 1), (1, 1)]
SAND_HOLE = (500, 0)


def numUnitsOfSandWhichComeToRest(rockFormations: list[list[tuple[int, int]]]) -> int:
    rockCells = getRockCells(rockFormations)
    restingSandCells = set()
    lowestY = findLowestRockCell(rockCells)
    abyssReached = False

    def sandCanEnterPosition(x: int, y: int) -> bool:
        return (x, y) not in rockCells and (x, y) not in restingSandCells

    # Simulate sand falling until a unit of sand falls below the lowest rock
    # cell. This indicates that it has fallen into the abyss because it is
    # impossible for anything to catch it.
    while not abyssReached:
        # Simulate a new sand unit until it comes to rest.
        resting = False
        sandPosition = SAND_HOLE

        while not resting:
            x, y = sandPosition

            # If the sand is lower than the lowest rock, it has reached the
            # abyss. Stop the simulation.
            if y > lowestY:
                abyssReached = True
                break

            # Try moving the sand. If it can't move, it becomes resting.
            for xDiff, yDiff in DIRECTIONS:
                newX, newY = x + xDiff, y + yDiff

                if sandCanEnterPosition(newX, newY):
                    sandPosition = (newX, newY)
                    break
            else:
                resting = True
                restingSandCells.add(sandPosition)

    return len(restingSandCells)


def numUnitsOfSandWhichComeToRestAfterBlocked(
    rockFormations: list[list[tuple[int, int]]]
) -> int:
    rockCells = getRockCells(rockFormations)
    restingSandCells = set()
    floor = findLowestRockCell(rockCells) + 2
    sandBlocked = False

    def sandCanEnterPosition(x: int, y: int) -> bool:
        return (x, y) not in rockCells and (x, y) not in restingSandCells and y < floor

    while not sandBlocked:
        sandPosition = SAND_HOLE
        resting = False

        while not resting:
            x, y = sandPosition

            for xDiff, yDiff in DIRECTIONS:
                newX, newY = x + xDiff, y + yDiff

                if sandCanEnterPosition(newX, newY):
                    sandPosition = (newX, newY)
                    break
            else:
                resting = True
                restingSandCells.add(sandPosition)

        if SAND_HOLE in restingSandCells:
            sandBlocked = True

    return len(restingSandCells)
