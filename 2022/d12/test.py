from solution import readInput, shortestPathToSignal, shortestPathFromAtoE
import logging

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_part_1_input_1():
    assert shortestPathToSignal(input1) == 31


def test_part_1_solution():
    logging.info(shortestPathToSignal(mainInput))


def test_part_2_input_1():
    assert shortestPathFromAtoE(input1) == 29


def test_part_2_solution():
    logging.info(shortestPathFromAtoE(mainInput))
