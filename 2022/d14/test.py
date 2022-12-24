from solution import (
    readInput,
    numUnitsOfSandWhichComeToRest,
    getRockCells,
    numUnitsOfSandWhichComeToRestAfterBlocked,
)
import logging

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    assert input1 == [
        [(498, 4), (498, 6), (496, 6)],
        [(503, 4), (502, 4), (502, 9), (494, 9)],
    ]


def test_get_rock_cells():
    assert set(getRockCells(input1)) == set(
        [
            (498, 4),
            (498, 5),
            (498, 6),
            (497, 6),
            (496, 6),
            (503, 4),
            (502, 4),
            (502, 5),
            (502, 6),
            (502, 7),
            (502, 8),
            (502, 9),
            (501, 9),
            (500, 9),
            (499, 9),
            (498, 9),
            (497, 9),
            (496, 9),
            (495, 9),
            (494, 9),
        ]
    )


def test_part_1():
    assert numUnitsOfSandWhichComeToRest(input1) == 24
    logging.info(numUnitsOfSandWhichComeToRest(mainInput))


def test_part_2():
    assert numUnitsOfSandWhichComeToRestAfterBlocked(input1) == 93
    logging.info(numUnitsOfSandWhichComeToRestAfterBlocked(mainInput))
