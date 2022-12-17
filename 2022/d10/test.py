from solution import readInput, simulateInstructionsAndSumSignalStrengths, renderScreen

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_part_1_input_1():
    assert simulateInstructionsAndSumSignalStrengths(input1) == 13140


def test_part_1_solution():
    print(simulateInstructionsAndSumSignalStrengths(mainInput))


def test_part_2_input_1():
    expectedScreen = [
        "##..##..##..##..##..##..##..##..##..##..",
        "###...###...###...###...###...###...###.",
        "####....####....####....####....####....",
        "#####.....#####.....#####.....#####.....",
        "######......######......######......####",
        "#######.......#######.......#######.....",
    ]

    assert renderScreen(input1) == expectedScreen


def test_part_2_solution():
    for row in renderScreen(mainInput):
        print(row)
