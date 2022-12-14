import os
import math
from heapq import heappush, heappop

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

The viewing distance from a tree in a certain direction is the minimum of its 
distance to the edge of the grid or the first tree that is the same height or
taller than the tree itself.

A scenic score for a tree is then the product of its viewing distance in all 
four directions.

Find the highest scenic score of any tree.

One intuition is that we can do something similar to the previous part by 
splitting the examining of each direction into a separate pass. Instead of
keeping track of visibility however, we keep track of the current scenic score
product for each cell. We then update the scenic score in each direction row by
row, column by column in both directions.

To leverage overlapping computation, we can search for the first blocking tree
for each tree in the same row/column simultaneously. That is, to determine the 
first blocking tree to the right, we iterate by rows from left to right. 

Take the row `30373`.

Starting out you see the leftmost 3. We need to then find the first number that
is greater than or equal to 3, so we remember that this position's scenic score
needs to be updated as soon as we see any such number.

We then continue on to 0. We see that there are no numbers which are less than 
or equal to 0 which still haven't had their viewing distance determined for this
direction, so we remember that this position's scenic score needs to be updated
as soon as we see any number that is 0 or greater.

Next we see another 3. We see that we have two numbers which are less than or 
equal to 3, so we update the scenic scores for each of those numbers accordingly
and so on.

What data structure can we use to keep track of what needs to have its viewing
distance determined still? Well, if we can always get the smallest tree that
hasn't had its viewing distance determined, then we can always find all smaller 
trees than the current tree. 

A data structure that lends itself to this is a heap! This makes the complexity
for determining scenic scores O(mn log n + nm log m). This is opposed to a
brute force strategy calculating for each cell individually which would have a 
complexity of O((n^2 * m) + (m^2 * n)). This also increases space complexity to
O(max(n, m)).
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


def calculateScenicScores(grid: list[list[int]]) -> list[list[int]]:
    rows, cols = len(grid), len(grid[0])
    scenicScores = [
        [
            1 if col not in [0, cols - 1] and row not in [0, rows - 1] else 0
            for col in range(cols)
        ]
        for row in range(rows)
    ]
    minHeap = []

    def updateScenicScores(row: int, col: int, horizontal: bool):
        nonlocal minHeap, scenicScores
        tree = grid[row][col]

        # Get all trees which are shorter or the same height of this
        # tree and update their scenic scores.
        while len(minHeap) > 0 and minHeap[0][0] <= tree:
            blockedTree, i = heappop(minHeap)

            if horizontal:
                scenicScores[row][i] *= abs(col - i)
            else:
                scenicScores[i][col] *= abs(row - i)

        if horizontal:
            heappush(minHeap, (tree, col))
        else:
            heappush(minHeap, (tree, row))

    # Update scenic scores in the right direction.
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            updateScenicScores(row, col, True)

        # TODO: Lots of repetition here... maybe this solution isn't that worth it...
        while len(minHeap) > 0:
            blockedTree, i = heappop(minHeap)
            scenicScores[row][i] *= abs(cols - 1 - i)

    # Update scenic scores in the left direction.
    for row in range(1, rows - 1):
        for col in range(cols - 2, -1, -1):
            updateScenicScores(row, col, True)

        while len(minHeap) > 0:
            blockedTree, i = heappop(minHeap)
            scenicScores[row][i] *= i

    # Update scenic scores in the down direction.
    for col in range(1, cols - 1):
        for row in range(1, rows - 1):
            updateScenicScores(row, col, False)

        while len(minHeap) > 0:
            blockedTree, i = heappop(minHeap)
            scenicScores[i][col] *= abs(rows - 1 - i)

    # Update scenic scores in the up direction.
    for col in range(1, cols - 1):
        for row in range(rows - 2, -1, -1):
            updateScenicScores(row, col, False)

        while len(minHeap) > 0:
            blockedTree, i = heappop(minHeap)
            scenicScores[i][col] *= i

    return scenicScores


def getMaxScenicScore(grid: list[list[int]]) -> int:
    return max([max(row) for row in calculateScenicScores(grid)])
