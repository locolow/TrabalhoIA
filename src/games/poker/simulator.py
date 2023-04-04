from random import shuffle

from games.game_simulator import GameSimulator
from games.poker.card import KuhnPokerCard
from games.poker.player import KuhnPokerPlayer
from games.poker.state import KuhnPokerState


class KuhnPokerSimulator(GameSimulator):

    def __init__(self, player1: KuhnPokerPlayer, player2: KuhnPokerPlayer):
        super().__init__([player1, player2])
        """
        deck of cards
        """
        self.__deck = [KuhnPokerCard.Jack, KuhnPokerCard.Queen, KuhnPokerCard.King]

    def init_game(self):
        # shuffle the deck
        shuffle(self.__deck)

        # assign a card to each player
        positions = self.get_player_positions()
        for pos in range(0, len(positions)):
            positions[pos].set_current_card(self.__deck[pos])
        return KuhnPokerState()

    def before_end_game(self, state: KuhnPokerState):
        # if we reached the show down, we are going to reveal the cards to all players
        if state.is_showdown():
            for pos in range(0, self.num_players()):
                state.draw_card(pos, self.__deck[pos])

    def end_game(self, state: KuhnPokerState):
        # ignored for this simulator
        pass
