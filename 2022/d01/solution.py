def maxCaloriesPerElf(elves: list[list[int]]) -> int:
    maxCalories = 0

    for elf in elves:
        elfCalories = 0
        for calories in elf:
            elfCalories += calories
        maxCalories = max(maxCalories, elfCalories)

    return maxCalories
