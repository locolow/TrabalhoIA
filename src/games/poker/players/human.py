from games.poker.action import KuhnPokerAction
from games.poker.player import KuhnPokerPlayer
from games.poker.state import KuhnPokerState
from games.state import State


class HumanKuhnPokerPlayer(KuhnPokerPlayer):

    def __init__(self, name):
        super().__init__(name)

    def get_action(self, state: KuhnPokerState):
        state.display()
        return {
            "b":    KuhnPokerAction.BET,
            "bet":  KuhnPokerAction.BET,
            "p":    KuhnPokerAction.PASS,
            "pass": KuhnPokerAction.PASS
        }.get(input("Choose an action (pass/p or bet/b): "))

    def event_action(self, pos: int, action, new_state: State):
        print(f"> player {pos} {action}")

    def event_end_game(self, final_state: State):
        pass

    def event_result(self, pos: int, result: int):
        print(f"> player {pos} got ${result}")

    def event_new_game(self):
        print("--- New game ---")
        print(f"> You are player {self.get_current_pos()} with card {self.get_current_card()}")
