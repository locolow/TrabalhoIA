from random import random

from games.poker.action import KuhnPokerAction
from games.poker.cfr.trainer import KuhnPokerTrainer
from games.poker.player import KuhnPokerPlayer
from games.poker.state import KuhnPokerState
from games.state import State


class CFRKuhnPokerPlayer(KuhnPokerPlayer):

    def __init__(self, name):
        super().__init__(name)
        self.__trainer = KuhnPokerTrainer()
        self.__trainer.train(100000)

    def get_action(self, state: KuhnPokerState):
        info_set = f"{self.get_current_card()}"
        for action in state.get_sequence():
            if action == KuhnPokerAction.PASS:
                info_set += 'p'
            else:
                info_set += 'b'
        prob = self.__trainer.get_avg_strategy(info_set)[0]

        return KuhnPokerAction.PASS if random() <= prob else KuhnPokerAction.BET

    def event_action(self, pos: int, action, new_state: State):
        # ignore
        pass

    def event_end_game(self, final_state: State):
        # ignore
        pass
