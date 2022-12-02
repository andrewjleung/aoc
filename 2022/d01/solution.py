from heapq import heappush, heappop


def maxCaloriesPerElf(elves: list[list[int]]) -> int:
    maxCalories = 0

    for elf in elves:
        elfCalories = 0
        for calories in elf:
            elfCalories += calories
        maxCalories = max(maxCalories, elfCalories)

    return maxCalories


def caloriesOfTopThreeElves(elves: list[list[int]]) -> list[int]:
    minHeap = []

    for elf in elves:
        elfCalories = 0

        for calories in elf:
            elfCalories += calories

        if len(minHeap) < 3:
            heappush(minHeap, elfCalories)
        elif len(minHeap) >= 3 and minHeap[0] < elfCalories:
            heappop(minHeap)
            heappush(minHeap, elfCalories)

    return minHeap
