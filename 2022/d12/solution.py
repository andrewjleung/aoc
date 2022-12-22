import os
from collections import deque
from typing import Callable
import logging

"""
PART 1

You are given a heightmap, a grid where each cell is marked with a letter a-z
denoting the height increasing for that cell. 

The heightmap also has your position marked as `S` which has a elevation of `a`,
and a location with the best signal, `E` which has an elevation of `z`.

You want to reach `E` from `S` with as few steps as possible. At any point you
can either move on square up, down, left, or right. In addition, the destination
must have an elevation at most one higher than the elevation of the current
square. The destination can be arbitrarily lower than the current cell.
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d12", filename)


def readInput(filename: str) -> list[str]:
    with open(getAbsolutePath(filename)) as f:
        return [line.strip() for line in f.readlines() if line != "\n"]


DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def find(heightmap: list[str], target: str) -> tuple[int, int]:
    rows, cols = len(heightmap), len(heightmap[0])
    for row in range(rows):
        for col in range(cols):
            if heightmap[row][col] == target:
                return (row, col)


def getElevationValue(elevation: str) -> int:
    if elevation == "S":
        return ord("a")

    if elevation == "E":
        return ord("z")

    return ord(elevation)


def canVisitElevation(currentElevation: str, destinationElevation: str) -> bool:
    return (
        getElevationValue(destinationElevation)
        <= getElevationValue(currentElevation) + 1
    )


def BFS(
    heightmap: list[str],
    start: tuple[int, int],
    destination: str,
    canVisit: Callable[[str, str], bool],
) -> int:
    rows, cols = len(heightmap), len(heightmap[0])
    visited = set([start])
    breadth = 0
    toVisit = deque([start])

    while len(toVisit) > 0:
        for _ in range(len(toVisit)):
            row, col = toVisit.popleft()

            if heightmap[row][col] in destination:
                return breadth

            for xDiff, yDiff in DIRECTIONS:
                newRow, newCol = row + xDiff, col + yDiff

                if newRow < 0 or newRow >= rows:
                    continue
                if newCol < 0 or newCol >= cols:
                    continue
                if (newRow, newCol) in visited:
                    continue
                if not canVisit(heightmap[row][col], heightmap[newRow][newCol]):
                    continue

                visited.add((newRow, newCol))
                toVisit.append((newRow, newCol))

        breadth += 1

    # Couldn't reach the signal.
    return -1


def shortestPathToSignal(heightmap: list[str]) -> int:
    # This is just an unweighted directed graph. We can do a BFS taking into
    # account cycles and not traversing nodes that have already been traversed.
    # The first path to reach the signal will automatically be the shortest
    # path. We just need to keep track of the current breadth to return that
    # once it is found.
    rows, cols = len(heightmap), len(heightmap[0])

    # Find the location of the starting point, `S`.
    S = find(heightmap, "S")

    if S is None:
        return -1

    # BFS from the starting point.
    return BFS(heightmap, S, "E", canVisitElevation)


def shortestPathFromAtoE(heightmap: list[str]) -> int:
    # Instead of just searching from every elevation `a` cell to find `E`, we
    # can save effort by instead working backwards from `E` to find the nearest
    # elevation `a`, making sure to take into account the rules for moving from
    # cell to cell are now reversed.
    E = find(heightmap, "E")

    return BFS(heightmap, E, "aS", lambda u, v: canVisitElevation(v, u))
