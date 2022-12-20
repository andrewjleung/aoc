import os
from dataclasses import dataclass
from typing import Deque
from collections import deque
import logging

"""
PART 1

Monkeys take turns inspecting and throwing items.

On a single monkey's turn, it will inspect and throw all of the items it is 
holding one at a time in order. 

Each monkey has an operation that is applied to an item's worry level while 
inspecting that item. After inspection, the worry level of the item then is 
divided by three and rounded down. Lastly, the monkey tests the worry level and
throws to a specific monkey depending on the final value of the worry level.

The thrown item is appended to the end of the recipient monkey's list of items.

Turns are taken in order from monkey 0 to `n`. A set of turns from 0 to `n` 
constitutes one round.

An amount of monkey business is defined as the product of the number of item
inspections for the top two monkeys with the most item inspections.

return the monkey business after 20 rounds.
"""


@dataclass
class MonkeyOperation:
    left: str
    op: str
    right: str

    def __substitute__(self, operand: str, old: int) -> int:
        if operand == "old":
            return old

        return int(operand)

    def execute(self, old: int) -> int:
        left = self.__substitute__(self.left, old)
        right = self.__substitute__(self.right, old)
        op = self.op

        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        else:
            raise ValueError(f"Unrecognized operator: {op}")


@dataclass
class MonkeyTest:
    divisor: int
    trueDestination: int
    falseDestination: int

    def run(self, num: int) -> int:
        if num % self.divisor == 0:
            return self.trueDestination

        return self.falseDestination


@dataclass
class Monkey:
    items: Deque[int]
    operation: MonkeyOperation
    test: MonkeyTest
    inspections: int = 0

    def __inspect__(self) -> None:
        self.items[0] = self.operation.execute(self.items[0])
        self.items[0] //= 3
        self.inspections += 1

    def __test__(self) -> int:
        return self.test.run(self.items[0])

    def __throw_to__(self, monkeys: list["Monkey"], num: int) -> None:
        item = self.items.popleft()
        monkeys[num].items.append(item)

    def doTurn(self, monkeys: list["Monkey"]) -> None:
        while len(self.items) > 0:
            self.__inspect__()
            self.__throw_to__(monkeys, self.__test__())


fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d11", filename)


def readInput(filename: str) -> list[Monkey]:
    monkeys = []
    buffer = []

    with open(getAbsolutePath(filename)) as f:
        for line in f:
            if len(line.strip()) < 1:
                continue

            buffer.append(line.strip())

            if len(buffer) < 6:
                continue

            startingItems = [int(num) for num in buffer[1].split(": ")[1].split(", ")]

            opLeft, op, opRight = buffer[2].split(" = ")[1].split(" ")
            operation = MonkeyOperation(opLeft, op, opRight)

            testDivisor = int(buffer[3].split(" ")[-1])
            testTrueDestination = int(buffer[4].split(" ")[-1])
            testFalseDestination = int(buffer[5].split(" ")[-1])
            test = MonkeyTest(testDivisor, testTrueDestination, testFalseDestination)

            monkeys.append(Monkey(deque(startingItems), operation, test))
            buffer.clear()

    return monkeys


def getMonkeyBusinessAfterTwentyRounds(monkeys: list[Monkey]) -> int:
    # Run 20 rounds.
    for _ in range(20):
        for monkey in monkeys:
            monkey.doTurn(monkeys)

    # Find the monkeys with the top two number of inspections and return the
    # product (the monkey business of rounds).
    topMonkey = monkeys[0].inspections
    secondMonkey = None

    for i in range(1, len(monkeys)):
        monkey = monkeys[i]

        if monkey.inspections >= topMonkey:
            secondMonkey = topMonkey
            topMonkey = monkey.inspections

    return topMonkey * secondMonkey
