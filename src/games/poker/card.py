from enum import Enum


class KuhnPokerCard(Enum):
    """
    kuhn poker is played with 3 cards with no suits
    """
    Jack = 0
    Queen = 1
    King = 2

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value

    def __str__(self):
        return {
            0: "J",
            1: "Q",
            2: "K"
        }[self.value]