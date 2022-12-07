import os
from collections import deque
from solution import findMarker

fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d06", filename)


def readInput(filename: str) -> str:
    with open(getAbsolutePath(filename)) as f:
        return f.read().strip()


input1 = readInput("input_1.txt")
input2 = readInput("input_2.txt")
input3 = readInput("input_3.txt")
input4 = readInput("input_4.txt")
input5 = readInput("input_5.txt")
mainInput = readInput("input_main.txt")


PACKET_HEADER_LENGTH = 4
MSG_HEADER_LENGTH = 14


def test_part_1_input_1():
    assert findMarker(input1, PACKET_HEADER_LENGTH) == 7


def test_part_1_input_2():
    assert findMarker(input2, PACKET_HEADER_LENGTH) == 5


def test_part_1_input_3():
    assert findMarker(input3, PACKET_HEADER_LENGTH) == 6


def test_part_1_input_4():
    assert findMarker(input4, PACKET_HEADER_LENGTH) == 10


def test_part_1_input_5():
    assert findMarker(input5, PACKET_HEADER_LENGTH) == 11


def test_part_1_solution():
    print(findMarker(mainInput, PACKET_HEADER_LENGTH))


def test_part_2_input_1():
    assert findMarker(input1, MSG_HEADER_LENGTH) == 19


def test_part_2_input_2():
    assert findMarker(input2, MSG_HEADER_LENGTH) == 23


def test_part_2_input_3():
    assert findMarker(input3, MSG_HEADER_LENGTH) == 23


def test_part_2_input_4():
    assert findMarker(input4, MSG_HEADER_LENGTH) == 29


def test_part_2_input_5():
    assert findMarker(input5, MSG_HEADER_LENGTH) == 26


def test_part_2_solution():
    print(findMarker(mainInput, MSG_HEADER_LENGTH))
