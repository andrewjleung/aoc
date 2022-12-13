from solution import (
    readInput,
    File,
    Directory,
    sumSmallDirectorySizes,
    getSmallestDirectorySizeToDelete,
)

input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    filesystem = Directory()
    dirA = Directory()
    dirD = Directory()
    dirE = Directory()
    fileB = File(14848514)
    fileC = File(8504156)
    fileF = File(29116)
    fileG = File(2557)
    fileH = File(62596)
    fileI = File(584)
    fileJ = File(4060174)
    fileD1 = File(8033020)
    fileD2 = File(5626152)
    fileK = File(7214296)

    filesystem.directories = {"a": dirA, "d": dirD}
    filesystem.files = {"b.txt": fileB, "c.dat": fileC}
    dirA.directories = {"e": dirE}
    dirA.files = {"f": fileF, "g": fileG, "h.lst": fileH}
    dirE.files = {"i": fileI}
    dirD.files = {"j": fileJ, "d.log": fileD1, "d.ext": fileD2, "k": fileK}

    assert input1 == filesystem


def test_part_1_input_1():
    assert sumSmallDirectorySizes(input1) == 95437


def test_part_1_solution():
    print(sumSmallDirectorySizes(mainInput))


def test_part_2_input_1():
    assert getSmallestDirectorySizeToDelete(input1) == 24933642


def test_part_2_solution():
    print(getSmallestDirectorySizeToDelete(mainInput))
