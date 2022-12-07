# PART 1

# Each elf is assigned a range of sections, denoted by a unique numeric ID.

# Each elf only has a single contiguous range. However, some fully contain
# others. Find those.

# PART 2

# Find the number of pairs which have any overlap at all.

# Determine if one given range fully overlaps the other.
def oneFullyContainsOther(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    merged = (min(range1[0], range2[0]), max(range1[1], range2[1]))
    return merged == range1 or merged == range2


# Determine if one given range overlaps the other.
def oneOverlapsAnother(range1: tuple[int, int], range2: tuple[int, int]) -> bool:
    # Ensure the range which starts earlier is `range1`.
    if range1[0] > range2[0]:
        range1, range2 = range2, range1

    return range1[1] >= range2[0]


# Count the number of assignment pairs which contain a full overlap between the
# two assignment ranges.
def countAssignmentsWithFullOverlap(
    assignmentPairs: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    count = 0

    for range1, range2 in assignmentPairs:
        if oneFullyContainsOther(range1, range2):
            count += 1

    return count


def countAssignmentsWithOverlap(
    assignmentPairs: tuple[tuple[int, int], tuple[int, int]]
) -> int:
    count = 0

    for range1, range2 in assignmentPairs:
        if oneOverlapsAnother(range1, range2):
            count += 1

    return count
