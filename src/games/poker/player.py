from abc import ABC

from games.player import Player
from games.poker.card import KuhnPokerCard


class KuhnPokerPlayer(Player, ABC):

    def __init__(self, name):
        super().__init__(name)

        """
        score will store the money earned (or lost)
        """
        self.__score = 0

        """
        here we are storing the number of games
        """
        self.__num_games = 0

        """
        we also need to store the current card we are holding
        """
        self.__current_card = KuhnPokerCard.Jack

    """
    assigns a card to the player
    """
    def set_current_card(self, card: KuhnPokerCard):
        self.__current_card = card

    """
    gets the current player's card
    """
    def get_current_card(self):
        return self.__current_card

    """
    gets the score
    """
    def get_score(self):
        return self.__score

    """
    gets the score
    """
    def get_expected_value(self):
        return self.__score * 1.0 / self.__num_games

    def event_new_game(self):
        self.__num_games += 1

    def event_result(self, pos: int, result: int):
        if pos == self.get_current_pos():
            self.__score += result

    def print_stats(self):
        print(f"Player {self.get_name()} | Total profit: ${self.__score} | Profit per game: ${self.get_expected_value()}")
