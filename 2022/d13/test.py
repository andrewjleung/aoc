from solution import readInput, sumIndicesOfCorrectlyOrderedPairs, compare
import logging

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    assert input1 == [
        ([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]),
        ([[1], [2, 3, 4]], [[1], 4]),
        ([9], [[8, 7, 6]]),
        ([[4, 4], 4, 4], [[4, 4], 4, 4, 4]),
        ([7, 7, 7, 7], [7, 7, 7]),
        ([], [3]),
        ([[[]]], [[]]),
        ([1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]),
    ]


def test_compare():
    assert compare(1, 2) < 0
    assert compare(0, 0) == 0
    assert compare(2, 1) > 0

    assert compare([1, 1, 3, 1, 1], [1, 1, 5, 1, 1]) < 0
    assert compare([1, 1, 5, 1, 1], [1, 1, 3, 1, 1]) > 0
    assert compare([1, 1, 3, 1, 1], [1, 1, 3, 1, 1]) == 0

    assert compare([1, 1, 1], [1, 1]) > 0
    assert compare([1, 1], [1, 1, 1]) < 0

    assert compare([3, 4, 5], 2) > 0
    assert compare([3, 4, 5], 4) < 0

    assert compare(2, []) > 0
    assert compare(2, [3]) < 0


def test_part_1_input_1():
    assert sumIndicesOfCorrectlyOrderedPairs(input1) == 13


def test_part_1_solution():
    logging.info(sumIndicesOfCorrectlyOrderedPairs(mainInput))


# def test_part_2_input_1():
#     assert False


# def test_part_2_solution():
#     assert False
