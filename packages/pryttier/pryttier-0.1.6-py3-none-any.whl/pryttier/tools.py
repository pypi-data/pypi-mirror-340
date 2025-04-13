import time
from functools import partial
from typing import *


class Infix(object):
    def __init__(self, func: Callable) -> None:
        self.func = func

    def __or__(self, other: Self) -> Self:
        return self.func(other)

    def __ror__(self, other: Self) -> Self:
        return Infix(partial(self.func, other))

    def __call__(self, v1, v2):
        return self.func(v1, v2)


# ===Some Infix Operations===
percentOf = Infix(lambda x, y: x / 100 * y)  # x% of y
isDivisibleBy = Infix(lambda x, y: x % y == 0)  # checks if x is divisible by y


def apply(itr: Iterable, func: Callable) -> list:
    return [func(x) for x in itr]


def apply2D(iter1: Sequence, iter2: Sequence, func: Callable) -> list:
    return [func(item1, item2) for item1, item2 in zip(iter1, iter2)]


def chunks(lst: MutableSequence, n: int):
    result = []
    for i in range(0, len(lst), n):
        result.append(lst[i:i + n])
    return result


def findCommonItems(*lsts: list) -> list:
    return list(set(lsts[0]).intersection(*lsts[1:]))

def swap(array: list, index1: int, index2: int):
    temp: int = array[index1]
    array[index1] = array[index2]
    array[index2] = temp

def hex2Dec(hx: str):
    res = 0
    n = len(hx)
    for i in range(n):
        num = hx[i]
        if num in ["a", "A"]: num = "10"
        if num in ["b", "B"]: num = "11"
        if num in ["c", "C"]: num = "12"
        if num in ["d", "D"]: num = "13"
        if num in ["e", "E"]: num = "14"
        if num in ["f", "F"]: num = "15"

        res += int(num) * 16**(n - i - 1)
    return res

class Card:
    ACE = 1
    JACK = 11
    QUEEN = 12
    KING = 13

    HEARTS = 40
    DIAMONDS = 41
    SPADE = 42
    CLOVER = 43

    RED = 20
    BLACK = 21

    def __init__(self, number: str | Self, symbol: str | Self):
        self.n = number
        self.symbol = symbol
        self.color = self.RED if self.symbol in [self.HEARTS, self.DIAMONDS] else self.BLACK

    def __repr__(self):
        num = str(self.n)
        match self.n:
            case self.ACE:
                num = "Ace"
            case self.JACK:
                num = "Jack"
            case self.QUEEN:
                num = "Queen"
            case self.KING:
                num = "King"
        sym = ""
        match self.symbol:
            case self.HEARTS:
                sym = "Hearts"
            case self.DIAMONDS:
                sym = "Diamonds"
            case self.SPADE:
                sym = "Spade"
            case self.CLOVER:
                sym = "Clover"
        return f"{num} of {sym}"

