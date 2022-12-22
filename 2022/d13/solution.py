import logging
import os
from dataclasses import dataclass

"""
PART 1

You are given pairs of packets, each pair separated by a blank line. 

Packets are lists of lists and integers. Lists are denoted with square bracket
notation and are comma-separated.

You need to determine how many pairs of packets are in the right order.

Ordering is determined by comparing same-index pairs within both packets,
abiding by the following rules:

1. If both values are integers, the lower integer should come first.
2. If both values are lists, recursively compare their elements. In addition, 
   the left list should be shorter or the same length as the right list.
3. If one value is a list and the other is an integer, recursively compare them
   as a list and a singleton list.
   
Return the sum of the indices (one-indexed) of pairs that are already in the 
right order. 
"""

"""
PART 2

...
"""

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d13", filename)


# This is a recursive parsing strategy to parse arbitrarily nested lists of
# integers. It assumes well-formedness, and works by traversing the given list
# string in windows of top-level elements one at a time, recursively parsing
# them. It traverses arbitrarily nested top-level elements using a stack to keep
# track of the current nesting level.
def parseList(string: str):
    if not string.startswith("["):
        return int(string)

    innerContents = string[1 : len(string) - 1]
    lst = []

    # Use a stack to match lists in order to traverse an entire 1-deep list at
    # a time or a single integer.
    stack = []

    # Inclusive bounds of the window containing the current element.
    start, end = 0, 0
    while end < len(innerContents):
        if innerContents[end] == "[":
            stack.append("[")
        elif innerContents[end] == "]":
            stack.pop()

        if len(stack) < 1:
            # Either a full list has been traversed or an integer has been
            # found. An integer may be multiple digits long so we need to ensure
            # that the end pointer of the window containing this element is
            # moved to fully contain the integer.
            nextComma = innerContents.find(",", end)

            # If there is no next comma, then this is the last element.
            if nextComma == -1:
                lst.append(parseList(innerContents[start : len(innerContents)]))
                break
            else:
                lst.append(parseList(innerContents[start:nextComma]))
                end = nextComma + 1
                start = end
        else:
            end += 1

    return lst


def readInput(filename: str):
    buffer = []
    pairs = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if line == "\n":
                continue

            buffer.append(line.strip())

            if len(buffer) >= 2:
                # Parse both packets.
                pairs.append(tuple([parseList(line) for line in buffer]))
                buffer.clear()

    return pairs


def sumIndicesOfCorrectlyOrderedPairs(pairs) -> int:
    return 0
