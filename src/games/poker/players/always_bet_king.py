from random import choice

from games.poker.action import KuhnPokerAction
from games.poker.card import KuhnPokerCard
from games.poker.player import KuhnPokerPlayer
from games.poker.state import KuhnPokerState
from games.state import State


class AlwaysBetKingKuhnPokerPlayer(KuhnPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: KuhnPokerState):
        if self.get_current_card() == KuhnPokerCard.King:
            return KuhnPokerAction.BET
        else:
            return choice([KuhnPokerAction.BET, KuhnPokerAction.PASS])

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
