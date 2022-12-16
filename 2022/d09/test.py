from solution import readInput, countSimulatedTailPositions

input1 = readInput("input_1.txt")
input2 = readInput("input_2.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    assert input1 == [
        ("R", 4),
        ("U", 4),
        ("L", 3),
        ("D", 1),
        ("R", 4),
        ("D", 1),
        ("L", 5),
        ("R", 2),
    ]


def test_part_1_input_1():
    assert countSimulatedTailPositions(input1, 2) == 13


def test_part_1_main_input():
    print(countSimulatedTailPositions(mainInput, 2))


def test_part_2_input_1():
    assert countSimulatedTailPositions(input1, 10) == 1


def test_part_2_input_2():
    assert countSimulatedTailPositions(input2, 10) == 36


def test_part_2_solution():
    print(countSimulatedTailPositions(mainInput, 10))
