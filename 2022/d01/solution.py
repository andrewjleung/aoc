from heapq import heappush, heappop


def maxCaloriesPerElf(elves: list[list[int]]) -> int:
    maxCalories = 0

    for elf in elves:
        maxCalories = max(maxCalories, sum(elf))

    return maxCalories


def caloriesOfTopThreeElves(elves: list[list[int]]) -> list[int]:
    if len(elves) < 3:
        raise ValueError("Not enough elves to find the top three.")

    minHeap = []

    for i in range(3):
        heappush(minHeap, sum(elves[i]))

    for i in range(3, len(elves)):
        elfCalories = sum(elves[i])

        if len(minHeap) >= 3 and minHeap[0] < elfCalories:
            heappop(minHeap)
            heappush(minHeap, elfCalories)

    return minHeap
