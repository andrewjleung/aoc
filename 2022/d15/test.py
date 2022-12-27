from solution import (
    readInput,
    countPositionsWithoutBeacons,
    Sensor,
    Position,
    getSensorRowOverlap,
    findTuningFrequency,
)
import logging


input1 = readInput("input_1.txt")
mainInput = readInput("input_main.txt")


def test_read_input():
    assert input1 == [
        Sensor(Position(2, 18), Position(-2, 15)),
        Sensor(Position(9, 16), Position(10, 16)),
        Sensor(Position(13, 2), Position(15, 3)),
        Sensor(Position(12, 14), Position(10, 16)),
        Sensor(Position(10, 20), Position(10, 16)),
        Sensor(Position(14, 17), Position(10, 16)),
        Sensor(Position(8, 7), Position(2, 10)),
        Sensor(Position(2, 0), Position(2, 10)),
        Sensor(Position(0, 11), Position(2, 10)),
        Sensor(Position(20, 14), Position(25, 17)),
        Sensor(Position(17, 20), Position(21, 22)),
        Sensor(Position(16, 7), Position(15, 3)),
        Sensor(Position(14, 3), Position(15, 3)),
        Sensor(Position(20, 1), Position(15, 3)),
    ]


def test_sensor_row_overlap():
    sensor = Sensor(Position(8, 7), Position(2, 10))
    assert getSensorRowOverlap(sensor, 17) is None
    assert getSensorRowOverlap(sensor, 16) == [8, 8]
    assert getSensorRowOverlap(sensor, 15) == [7, 9]
    assert getSensorRowOverlap(sensor, 11) == [3, 13]
    assert getSensorRowOverlap(sensor, -2) == [8, 8]
    assert getSensorRowOverlap(sensor, -1) == [7, 9]
    assert getSensorRowOverlap(sensor, 5) == [1, 15]


def test_part_1():
    assert countPositionsWithoutBeacons(input1, 10) == 26
    logging.info(countPositionsWithoutBeacons(mainInput, 2000000))


def test_part_2():
    assert findTuningFrequency(input1, 20) == 56000011
    assert findTuningFrequency(mainInput, 4000000) == 10884459367718
