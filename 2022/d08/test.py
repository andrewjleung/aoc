from solution import (
    readInput,
    countVisibleTrees,
    getMaxScenicScore,
    getNextGTEElement,
    getRightIterator,
    getLeftIterator,
    getDownIterator,
    getUpIterator,
)

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    assert input1 == [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]


def test_part_1_input_1():
    assert countVisibleTrees(input1) == 21


def test_part_1_solution():
    print(countVisibleTrees(mainInput))


def test_getNextGTEElements():
    assert getNextGTEElement(getRightIterator(input1, 0)) == [2, 1, 1, 1, 0]
    assert getNextGTEElement(getLeftIterator(input1, 0)) == [1, 3, 2, 1, 0]
    assert getNextGTEElement(getDownIterator(input1, 0)) == [2, 1, 2, 1, 0]
    assert getNextGTEElement(getUpIterator(input1, 0)) == [1, 1, 2, 1, 0]


def test_part_2_input_1():
    assert getMaxScenicScore(input1) == 8


def test_part_2_solution():
    print(getMaxScenicScore(mainInput))
