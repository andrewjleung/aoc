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
    op: str
    right: str

    def __substitute__(self, right: str, old: int) -> int:
        if right == "old":
            return old

        return int(right)

    def execute(self, old: int) -> int:
        right = self.__substitute__(self.right, old)
        op = self.op

        if op == "+":
            return old + right
        elif op == "*":
            return old * right
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

            _, op, opRight = buffer[2].split(" = ")[1].split(" ")
            operation = MonkeyOperation(op, opRight)

            testDivisor = int(buffer[3].split(" ")[-1])
            testTrueDestination = int(buffer[4].split(" ")[-1])
            testFalseDestination = int(buffer[5].split(" ")[-1])
            test = MonkeyTest(testDivisor, testTrueDestination, testFalseDestination)

            monkeys.append(Monkey(deque(startingItems), operation, test))
            buffer.clear()

    return monkeys


@dataclass
class GetMonkeyBusiness:
    monkeys: list[Monkey]
    managedWorry: bool

    def __post_init__(self):
        self.inspections = [0 for _ in range(len(self.monkeys))]
        self.allDivisorsProduct = 1

        for monkey in self.monkeys:
            self.allDivisorsProduct *= monkey.test.divisor

    def __inspect__(self, monkeyId: int) -> None:
        monkey = self.monkeys[monkeyId]
        monkey.items[0] = monkey.operation.execute(monkey.items[0])

        if self.managedWorry:
            monkey.items[0] //= 3
        else:
            # We want to make the number smaller while retaining whether or not
            # it is divisible by the divisor of any monkey that may test it in
            # the future.
            monkey.items[0] = monkey.items[0] % self.allDivisorsProduct

        self.inspections[monkeyId] += 1

    def __test__(self, monkeyId: int) -> int:
        monkey = self.monkeys[monkeyId]
        return monkey.test.run(monkey.items[0])

    def __throw__(self, thrower: int, receiver: int) -> None:
        thrower, receiver = self.monkeys[thrower], self.monkeys[receiver]
        item = thrower.items.popleft()
        receiver.items.append(item)

    def __doTurn__(self, monkeyId: int) -> None:
        monkey = self.monkeys[monkeyId]

        while len(monkey.items) > 0:
            self.__inspect__(monkeyId)
            self.__throw__(monkeyId, self.__test__(monkeyId))

    def runRounds(self, rounds: int) -> int:
        # Run x rounds.
        for _ in range(rounds):
            for i in range(len(self.monkeys)):
                self.__doTurn__(i)

        # Find the monkeys with the top two number of inspections and return the
        # product (the monkey business of rounds).
        firstMax = max(self.inspections)
        self.inspections.remove(firstMax)
        secondMax = max(self.inspections)

        return firstMax * secondMax
