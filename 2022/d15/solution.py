import logging
import os
from dataclasses import dataclass
import re
from typing import Optional

"""
PART 1

You are given the positions of sensors along with the positions of the closest
beacon to each sensor. There are no ties when considering the closest beacon to
a sensor.

Because each sensor has a closest beacon, it follows that there cannot exist any
beacon closer to each sensor than the closest beacon. This forms a radius around
each beacon within which no beacon can possibly exist.

Using this logic, at row y=2000000, find the number of positions which cannot 
have any beacons.
"""

"""
PART 2

The distress beacon's `x` and `y` coordinates are >= 0 and <= 4000000. it is 
located in the only coordinate in this range which may hold a beacon. 

Find the distress beacon and calculate its tuning frequency, calculated as 
`x * 4000000 + y`.
"""

LINE_REGEX = r"Sensor at x=(?P<sensorX>-?[0-9]+), y=(?P<sensorY>-?[0-9]+): closest beacon is at x=(?P<beaconX>-?[0-9]+), y=(?P<beaconY>-?[0-9]+)"


@dataclass
class Position:
    x: int
    y: int


@dataclass
class Sensor:
    position: Position
    beacon: Position


fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d15", filename)


def readInput(filename: str) -> list[Sensor]:
    sensors = []
    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if line == "\n":
                continue

            matchGroups = re.match(LINE_REGEX, line.strip()).groupdict()
            sensors.append(
                Sensor(
                    Position(int(matchGroups["sensorX"]), int(matchGroups["sensorY"])),
                    Position(int(matchGroups["beaconX"]), int(matchGroups["beaconY"])),
                )
            )
    return sensors


def manhattanDist(position1: Position, position2: Position) -> int:
    x1, y1 = position1.x, position1.y
    x2, y2 = position2.x, position2.y
    return abs(x1 - x2) + abs(y1 - y2)


# Return an inclusive range of x values at which the given sensor overlaps
# the desired row. Return `None` if there is no overlap.
def getSensorRowOverlap(sensor: Sensor, row: int) -> Optional[tuple[int, int]]:
    radius = manhattanDist(sensor.position, sensor.beacon)

    # Normalize the desired row to be below the sensor (greater y). The
    # relative distance between the sensor and the row is preserved.
    if row < sensor.position.y:
        row = sensor.position.y + (sensor.position.y - row)

    if row > sensor.position.y + radius:
        return None

    # Compute the half-length of the overlap range.
    halfLength = sensor.position.y + radius - row

    # The overlap range is centered on the `x` coordinate of the sensor.
    # The amount that it extends out in both directions horizontally is
    # based upon how far the sensor is from the desired row.
    return [sensor.position.x - halfLength, sensor.position.x + halfLength]


def findPositionsWithoutBeacons(
    sensors: list[Sensor], row: int
) -> list[tuple[int, int]]:
    # How do we deduce that a beacon can't exist within a position?
    # A beacon can't exist within a position if for any sensor, it is as close
    # or closer to the sensor than that sensor's closest beacon. In other words,
    # any position which a sensor can reach on the desired row can't have a
    # beacon.

    # An approach to solve this is to initiate a search from each sensor with a
    # radius of the distance between it and its beacon to find cells on the
    # desired row. This approach can be further refined.

    # For any sensor, we can determine what range of cells it reaches on any
    # desired row in constant time based upon its radius (the Manhattan distance
    # between it and its closest beacon) and how far it is from the row.
    # After this, we can use an intervals algorithm to merge all overlapping
    # ranges. Finally, we can count the total length of all ranges.

    # The overall time complexity of this algorithm is then simply `O(n log n)`
    # where `n` is the the number of sensors. This is because intervals are
    # calculated in constant time for each sensor. Then, merging all intervals
    # can be done in `O(n log n)` time. Finally, a single linear pass across
    # `O(n)` intervals counts up the number of positions without beacons.

    # Get overlap `x` intervals for all sensors.
    # These intervals correspond to ranges of `x` values for each sensor which
    # overlap with the given row. These may overlap at this point.
    intervals = [getSensorRowOverlap(sensor, row) for sensor in sensors]
    intervals = [interval for interval in intervals if interval is not None]

    if len(intervals) < 1:
        return 0

    intervals.sort()
    mergedIntervals = []

    # Merge overlapping intervals to ensure only non-overlapping intervals remain.
    intervalStart, intervalEnd = intervals[0]

    for i in range(1, len(intervals)):
        b = intervals[i]

        if b[0] <= intervalEnd:
            intervalEnd = max(b[1], intervalEnd)
        else:
            mergedIntervals.append((intervalStart, intervalEnd))
            intervalStart, intervalEnd = b

    mergedIntervals.append((intervalStart, intervalEnd))
    return mergedIntervals


def countPositionsWithoutBeacons(sensors: list[Sensor], row: int) -> int:
    intervalsWithoutBeacons = findPositionsWithoutBeacons(sensors, row)

    # This is necessary since this approach won't already account for any
    # beacons which are already on the specified row. Therefore the number of
    # beacons which are on the row need to be subtracted from the number of
    # overlapping positions.
    numBeaconsOnRow = len(
        set([sensor.beacon.x for sensor in sensors if sensor.beacon.y == row])
    )

    # Count the number of positions without beacons by summing the lengths of
    # each interval.
    return (
        sum([end - start + 1 for start, end in intervalsWithoutBeacons])
        - numBeaconsOnRow
    )


def findDistressBeacon(
    sensors: list[Sensor], coordinateUpperBound: int
) -> Optional[tuple[int, int]]:
    for row in range(coordinateUpperBound):
        intervals = findPositionsWithoutBeacons(sensors, row)

        # Normalize the intervals by constraining them to the upper and lower
        # bound coordinates of the distress beacon.
        intervals = [
            (max(0, interval[0]), (min(coordinateUpperBound, interval[1])))
            for interval in intervals
            if interval[1] >= 0 and interval[0] <= coordinateUpperBound
        ]

        # If there is more than one interval, this means that there are two
        # non-overlapping, non-adjacent intervals meaning the distress beacon
        # must be between the two intervals.
        if len(intervals) > 1:
            return intervals[0][1] + 1, row

        # If there is one interval that spans the entire range, then the
        # distress beacon is not in this range.
        if intervals[0][0] == 0 and intervals[0][1] == coordinateUpperBound:
            continue

        # If there is one interval which doesn't start at 0, the distress beacon
        # is at `x == 0`.
        if intervals[0][0] != 0:
            return 0, row

        # If there is one interval which doesn't end at the upper bound, the
        # distress beacon is at the upper bound.
        return coordinateUpperBound, row

    return None


TUNING_FREQUENCY_X_COEFFICIENT = 4000000


def findTuningFrequency(sensors: list[Sensor], coordinateUpperBound: int) -> int:
    x, y = findDistressBeacon(sensors, coordinateUpperBound)

    return x * TUNING_FREQUENCY_X_COEFFICIENT + y
