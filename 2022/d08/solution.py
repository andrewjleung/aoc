import os
import math
from heapq import heappush, heappop
from collections.abc import Iterator

"""
PART 1

You are given a grid of tree heights (0-9).

A tree is defined as visible if all trees between it and an edge of the grid in
the four cardinal directions are shorter than it, or if the tree is on the edge
of the grid.

You need to find how many unique trees are visible from outside of the grid.

A naive solution would just be to calculate for each tree not on the edge,
whether it is visible or not. In an m * n grid, the complexity of this would be
O(m * n * (m + n)) = O((m^2 * n) + (n^2 * m)).

There is clearly overlapping work when examining surrounding trees. Can this be
alleviated? One intuition is that in each direction, a single tree can affect 
visibility. That is, if we just know the max height tree in each direction of 
the tree we are examining, we can determine visibility in that direction.

You can leverage this to reduce to linear complexity (in multiple passes) and 
linear space using the following strategy.

Maintain a parallel matrix which initializes every bordering cell as `True` and
every other cell as `False`. This represents whether this cell is visible or
not. 

Then, do four passes iterating across the matrix in each of four directions. 

What these passes will do is keep track of the largest tree seen on a particular
row/column so far, using that to determine if a cell is visible from that
direction. As soon as an invisible tree is visible from a direction, increment
the number of visible trees.

This is essentially looking at the matrix from each direction and counting the
number of visible trees while keeping track of which ones have already been 
counted.
"""

"""
PART 2

The intuition here is that this problem maps to finding the next greatest 
element in a sequence of numbers. Traversing a row/column in a certain 
direction, a viewing distance is just the difference in position between an 
element and its next greater than or equal element in the array, which can be 
found in linear time with respect to that sequence for all elements using a
stack.

By using this algorithm, you essentially just traverse each row and column 
a total of three times. The first two times are to find the viewing distances 
for elements in the forward and backward directions, then the last time is to 
create the scenic score by multiplying the results together.

This yields a linear time algorithm to find scenic scores.

Part 1 can also be solved with this algorithm...
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d08", filename)


def readInput(filename: str) -> list[list[int]]:
    grid = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            grid.append([int(digit) for digit in list(line.strip())])

    return grid


def countVisibleTrees(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    visibility = [[False for _ in row] for row in grid]

    # All bordering trees are visible by default.
    count = 0

    def updateVisibility(row: int, col: int, largestTree: int) -> int:
        nonlocal count

        tree = grid[row][col]
        treeIsVisible = visibility[row][col]

        if not treeIsVisible and tree > largestTree:
            visibility[row][col] = True
            count += 1

        return max(largestTree, tree)

    # Examine visibility from the left border.
    for row in range(rows):
        largestTree = -math.inf
        for col in range(cols):
            largestTree = updateVisibility(row, col, largestTree)

    # Examine visibility from the right border.
    for row in range(rows):
        largestTree = -math.inf
        for col in range(cols - 1, -1, -1):
            largestTree = updateVisibility(row, col, largestTree)

    # Examine visibility from the top border.
    for col in range(cols):
        largestTree = -math.inf
        for row in range(rows):
            largestTree = updateVisibility(row, col, largestTree)

    # Examine visibility from the bottom border.
    for col in range(cols):
        largestTree = -math.inf
        for row in range(rows - 1, -1, -1):
            largestTree = updateVisibility(row, col, largestTree)

    return count


def getRightIterator(matrix: list[list[int]], row: int):
    return matrix[row]


def getLeftIterator(matrix: list[list[int]], row: int):
    for col in range(len(matrix[row]) - 1, -1, -1):
        yield matrix[row][col]


def getDownIterator(matrix: list[list[int]], col: int):
    for row in range(len(matrix)):
        yield matrix[row][col]


def getUpIterator(matrix: list[list[int]], col: int):
    for row in range(len(matrix) - 1, -1, -1):
        yield matrix[row][col]


# For each element in the given iterator, find the distance between it and its
# next greater than or equal element in the iterator or the end of the elements.
def getNextGTEElement(iterator: Iterator[int]) -> list[int]:
    stack = []
    result = []

    # Try to find the next GTE element for each element in the sequence.
    i = 0
    for num in iterator:
        while len(stack) > 0 and num >= stack[-1][0]:
            _, j = stack.pop()
            result[j] = i - j

        stack.append((num, i))
        result.append(-1)
        i += 1

    # Find the distance from the end of the sequence for all remaining elements
    # which don't have a next GTE element. At this point, `i` is the length of
    # the sequence.
    while len(stack) > 0:
        _, j = stack.pop()
        result[j] = i - 1 - j

    return result


def calculateScenicScores(grid: list[list[int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    scenicScores = [[1 for _ in row] for row in grid]

    # Multiply scenic scores by horizontal viewing distances.
    for row in range(rows):
        rightScores = getNextGTEElement(getRightIterator(grid, row))
        leftScores = getNextGTEElement(getLeftIterator(grid, row))

        for col in range(len(rightScores)):
            scenicScores[row][col] *= rightScores[col] * leftScores[cols - 1 - col]

    # Multiply scenic scores by vertical viewing distances.
    for col in range(cols):
        downScores = getNextGTEElement(getDownIterator(grid, col))
        upScores = getNextGTEElement(getUpIterator(grid, col))

        for row in range(len(downScores)):
            scenicScores[row][col] *= downScores[row] * upScores[rows - 1 - row]

    return scenicScores


def getMaxScenicScore(grid: list[list[int]]) -> int:
    return max([max(row) for row in calculateScenicScores(grid)])
