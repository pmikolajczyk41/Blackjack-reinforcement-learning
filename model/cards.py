from enum import IntEnum
from typing import List


class Card(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 10
    QUEEN = 10
    KING = 10
    ACE = 11

    @classmethod
    def get_values(cls) -> range:
        return range(2, 12)

    @classmethod
    def get_full_deck(cls) -> List:
        return list(Card.__members__.values())
