# PART 1

# A rucksack has two compartments. Items have types. An item of a given type can
# only go in exactly one compartment, and each compartment holds the exact same
# amount of items.

# There is an error violating this rule for a single item.

# We want to, for each rucksack, find the item type that violates that rule.
# Then, across all rucksacks, we want to sum the priorities of those violating
# types.

# PART 2

# Elves are grouped in threes, each with an identifying item type carried by all
# three elves, though they may carry other items in their rucksacks.

# At most two of the elves will be carrying any other item type.

# Split the given rucksack into its equal-length components.
def getRucksackComponents(rucksack: str) -> tuple[str, str]:
    size = len(rucksack)
    return (rucksack[0 : size // 2], rucksack[size // 2 :])


# Determine the priority number of a given item type.
def getItemPriority(itemType: str) -> int:
    if itemType.isupper():
        return ord(itemType) - ord("A") + 27

    return ord(itemType) - ord("a") + 1


# Find the common character across the given list of strings.
def findCommonItem(strings: list[str]) -> str:
    if len(strings) < 2:
        raise ValueError("Unable to find common item between less than 2 strings.")

    prevSet = set()
    currSet = prevSet

    for string in strings:
        for char in string:
            currSet.add(char)

        prevSet = prevSet.intersection(currSet)
        currSet = set()

    if len(prevSet) < 1:
        raise ValueError("No common item between all strings.")

    return prevSet.pop()


# Find the sum of the priorities of violating items for each given rucksack.
def sumViolatingItemPriorities(rucksacks: list[str]) -> int:
    return sum(
        [
            getItemPriority(findCommonItem(getRucksackComponents(rucksack)))
            for rucksack in rucksacks
        ]
    )


# Find the sum of the priorities of badge types for each given rucksack.
def sumBadgeTypes(rucksacks: list[str]) -> int:
    groupedRucksacks = [rucksacks[i : i + 3] for i in range(0, len(rucksacks), 3)]
    return sum([getItemPriority(findCommonItem(group)) for group in groupedRucksacks])
