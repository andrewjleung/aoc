import os
from dataclasses import dataclass
from typing import Deque

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

    def run(self, num: int) -> bool:
        if num % self.divisor == 0:
            return self.trueDestination

        return self.falseDestination


@dataclass
class Monkey:
    items: Deque[int]
    operation: MonkeyOperation
    test: MonkeyTest

    def __inspect__(self) -> None:
        pass

    def __test__(self) -> int:
        pass

    def doTurn(self, monkeys: list["Monkey"]) -> None:
        pass


fileDir = os.path.dirname(os.path.realpath("__file__"))


def getAbsolutePath(filename: str):
    return os.path.join(fileDir, "2022/d11", filename)


def readInput(filename: str) -> list[Monkey]:
    with open(getAbsolutePath(filename)) as f:
        return f.readlines()


def getMonkeyBusinessAfterTwentyRounds(monkeys: list[Monkey]) -> int:
    pass
