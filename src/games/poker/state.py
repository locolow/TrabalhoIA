from games.poker.action import KuhnPokerAction
from games.poker.card import KuhnPokerCard
from games.state import State


class KuhnPokerState(State):

    def __init__(self):
        super().__init__()
        """
        the sequence of plays
        """
        self.__sequence = []
        """
        the acting player index
        """
        self.__acting_player = 0
        """
        indicates if the game is finished
        """
        self.__is_finished = False
        """
        the cards that were seen so far
        """
        self.__cards = [None, None]
        """
        the best that were done so far
        in this version of Poker, each player bet $1 each before starting the game
        """
        self.__bets = [1, 1]
        """
        indicates if the game is in showdown (actions are finished and players are about to reveal the cards)
        """
        self.__is_showdown = False

    def get_num_players(self):
        return 2

    def validate_action(self, action) -> bool:
        return not self.__is_finished and action is not None

    def update(self, action):
        # only need to check the outcome of the action if none was added until now
        if len(self.__sequence) > 0:
            last_action = self.__sequence[-1]

            if last_action == KuhnPokerAction.BET:
                self.__is_finished = True
                if action == KuhnPokerAction.BET:
                    self.__is_showdown = True
            else:
                if action == KuhnPokerAction.PASS:
                    self.__is_finished = True
                    self.__is_showdown = True

        self.__sequence.append(action)

        # if someone is betting, we are going to increase its bet amount
        if action == KuhnPokerAction.BET:
            self.__bets[self.__acting_player] += 1

        # swap the player
        self.__acting_player = 1 if self.__acting_player == 0 else 0

    def display(self):
        for action in self.__sequence:
            print('b' if action == KuhnPokerAction.BET else 'p', end="")
        print(f": pot = {self.get_pot()}")

    """
    get the total amount that was put into bets so far
    """
    def get_pot(self):
        return sum(self.__bets)

    def is_finished(self) -> bool:
        return self.__is_finished

    def get_acting_player(self) -> int:
        return self.__acting_player

    def clone(self):
        cloned = KuhnPokerState()
        cloned.__bets = self.__bets.copy()
        cloned.__sequence = self.__sequence.copy()
        cloned.__is_finished = self.__is_finished
        cloned.__acting_player = self.__acting_player
        for i in range(0, len(self.__cards)):
            cloned.__cards[i] = self.__cards[i]
        cloned.__is_showdown = self.__is_showdown
        return cloned

    def get_result(self, pos):
        # no result if the game is not finished
        if not self.__is_finished:
            return None

        # if we are finished and we have a showdown, the cards must be available
        if self.__is_showdown:
            for card in self.__cards:
                if card is None:
                    return None

        pot = self.get_pot()
        opp_pos = 1 if pos == 0 else 0

        if self.__is_showdown:
            # noinspection PyTypeChecker
            # if there is a showdown, we will give 1 or 2 to the player with the best card and -1 or -2 to the looser
            return (1 if self.__cards[pos] > self.__cards[opp_pos] else -1) * (pot / 2)
        else:
            # this means that someone folded, so we will return the positive score to the player with the highest bet
            return 1 if self.__bets[pos] > self.__bets[opp_pos] else -1

    def before_results(self):
        pass

    """
    a player in position pos reveices a card 
    """
    def draw_card(self, pos, card: KuhnPokerCard):
        # noinspection PyTypeChecker
        self.__cards[pos] = card

    def is_showdown(self):
        return self.__is_showdown

    def get_sequence(self):
        return self.__sequence
