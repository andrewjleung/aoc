import logging
import os
from dataclasses import dataclass
from functools import cmp_to_key

"""
PART 1

You are given pairs of packets, each pair separated by a blank line. 

Packets are lists of lists and integers. Lists are denoted with square bracket
notation and are comma-separated.

You need to determine how many pairs of packets are in the right order.

Ordering is determined by comparing same-index pairs within both packets,
abiding by the following rules:

1. If both values are integers, the lower integer should come first. If they are
   the same, you need to keep examining the input to break the tie. If the  
   higher integer comes first, then they are out of order.
2. If both values are lists, recursively compare their elements. As soon as any
   comparison yields an actual ordering, return that. Otherwise, if no ordering
   can be determined from their  elements, if the left value is shorter than the
   right, it is in order. If the right value is shorter than the left, it is out
   of order. otherwise, they are tied. 
3. If one value is a list and the other is an integer, recursively compare them
   as a list and a singleton list.
   
Return the sum of the indices (one-indexed) of pairs that are already in the 
right order. 
"""

"""
PART 2

From part 1, you ideally should have needed to encapsulate the logic behind
ordering packets into an unambiguous comparator.

After adding in a couple of "divider packets," sort all the packets then return
the decoder key which is defined as the product of the indices of the two 
divider packets after sorting.
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
    packets = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if line == "\n":
                continue

            packets.append(parseList(line.strip()))

    return packets


def compare(left, right) -> int:
    if isinstance(left, int) and isinstance(right, int):
        return left - right

    if isinstance(left, int):
        left = [left]
    elif isinstance(right, int):
        right = [right]

    for l, r in zip(left, right):
        comparison = compare(l, r)

        if comparison != 0:
            return comparison

    if len(left) < len(right):
        return -1

    if len(right) < len(left):
        return 1

    return 0


def sumIndicesOfCorrectlyOrderedPairs(packets) -> int:
    pairs = [(packets[i], packets[i + 1]) for i in range(0, len(packets), 2)]
    result = 0

    for i, (leftPacket, rightPacket) in enumerate(pairs):
        if compare(leftPacket, rightPacket) < 0:
            result += i + 1

    return result


DIVIDER_PACKETS = [[[2]], [[6]]]


def findDecoderKey(packets) -> int:
    packets.extend(DIVIDER_PACKETS)
    sortedPackets = sorted(packets, key=cmp_to_key(compare))

    decoderKey = 1

    for i, packet in enumerate(sortedPackets):
        if packet in DIVIDER_PACKETS:
            decoderKey *= i + 1

    return decoderKey
