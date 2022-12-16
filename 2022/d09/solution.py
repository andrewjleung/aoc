import os
import math

"""
PART 1

Conceptually, there is a 2-D grid containing a head and a tail which begin on 
the same cell.

You are given a list of cardinal movements on the 2-D grid, where each movement
describes the head moving a specified number of steps in a specified direction. 
The head knot and tail knot must always be touching at each step (adjacent, 
diagonal, or even overlapping), or else the tail must move in the direction of 
the head.

In cases where they are not in the same row or column, the tail will always move
diagonally towards the head.

You need to count how many positions the tail visited at least once.

The first thought is that we need to have a sort of infinite grid with indexed
positions so that we actually distinguish unique positions that the tail has 
moved. This is pretty simple, as we can arbitrarily set a starting position for
both the head and tail and just update the position from there based on 
movements.

Let's just use the origin (0, 0) as the starting point.

From there, we start moving the head according to the given movements. We can 
keep track of a set of point tuples in order to keep a count of the unique 
points to which the tail travels.

We can just move the head a step at a time, and depending on the adjacency and 
relative positions of the head and tail, move the tail.
"""

"""
PART 2

This is just an abstraction of part 1.
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d09", filename)


def readInput(filename: str) -> list[tuple[str, int]]:
    moves = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            tokens = line.split(" ")
            direction, distance = tokens[0], int(tokens[1])
            moves.append((direction, distance))

    return moves


DIRECTIONS = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}


def isAdjacent(p1: tuple[int, int], p2: tuple[int, int]) -> bool:
    return math.dist(p1, p2) < 2


def movePointTowardsPoint(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    if isAdjacent(p1, p2):
        return p1

    newPos = list(p1)

    for dim in range(2):
        if p1[dim] > p2[dim]:
            newPos[dim] -= 1
        elif p1[dim] < p2[dim]:
            newPos[dim] += 1

    return tuple(newPos)


def executeMove(point: tuple[int, int], direction: str) -> tuple[int, int]:
    y, x = DIRECTIONS[direction]
    return (point[0] + y, point[1] + x)


def getSimulatedTailPositions(
    headMoves: list[tuple[str, int]], ropeLength: int
) -> set[tuple[int, int]]:
    if ropeLength < 2:
        raise ValueError("Rope length must be at least 2.")

    # The first position holds the head knot position and the last holds the
    # tail knot position.
    knotPositions = [(0, 0) for _ in range(ropeLength)]
    tailPositions = set([knotPositions[-1]])

    for move in headMoves:
        direction, distance = move

        for _ in range(distance):
            # Move the head.
            knotPositions[0] = executeMove(knotPositions[0], direction)

            # Move all the other knots relative to each other.
            for i in range(len(knotPositions) - 1):
                frontKnot, backKnot = knotPositions[i], knotPositions[i + 1]
                knotPositions[i + 1] = movePointTowardsPoint(backKnot, frontKnot)

            tailPositions.add(knotPositions[-1])

    return tailPositions


def countSimulatedTailPositions(
    headMoves: list[tuple[str, int]], ropeLength: int
) -> int:
    return len(getSimulatedTailPositions(headMoves, ropeLength))
