from solution import readInput, shortestPathToSignal
import logging

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_part_1_input_1():
    assert shortestPathToSignal(input1) == 31


def test_part_1_solution():
    logging.info(shortestPathToSignal(mainInput))
