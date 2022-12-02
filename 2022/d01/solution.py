from heapq import heappush, heappop


def maxCaloriesPerElf(elves: list[list[int]]) -> int:
    if len(elves) < 1:
        raise ValueError("No elves.")

    return max([sum(elf) for elf in elves])


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
