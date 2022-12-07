"""
PART 1

You are given a starting configuration of stacks of crates and a set of
instructions for the movements of the crates in the format:
"move x from y to z." When multiple quantities of crates are moved, they are
moved one at a time meaning that the first crate moved ends up below the next
ones and so on.

Crates are denoted by letters and stacks are denoted in 1-indexed order.

Return which crate will end up on the top of each stack in a single string.
"""

# Mutate the given arrangement by applying the given move. This assumes that the
# move is valid.
def applyMove(
    arrangement: list[list[str]], move: list[tuple[int, int, int]]
) -> list[list[str]]:
    quantity, fromStack, toStack = move

    for _ in range(quantity):
        element = arrangement[fromStack - 1].pop()
        arrangement[toStack - 1].append(element)

    return arrangement


# Return the top crates of each given stack after applying the given procedure.
def rearrangeAndGetTopOfStacks(
    arrangement: list[list[str]], moves: list[tuple[int, int, int]]
) -> str:
    for move in moves:
        arrangement = applyMove(arrangement, move)

    topOfStacks = []
    for stack in arrangement:
        topOfStacks.append(stack[-1])

    return "".join(topOfStacks)
