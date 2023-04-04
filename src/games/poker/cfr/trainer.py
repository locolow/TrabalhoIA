from random import shuffle

from games.poker.card import KuhnPokerCard


class KuhnPokerTrainer:
    """
    This code was converted and adapted from Java to Python
    Original source: http://modelai.gettysburg.edu/2013/cfr/
    This allows to train a Poker player to learn a nash-equilibrium strategy through the CFR algorithm
    """

    PASS = 0
    BET = 1
    NUM_ACTIONS = 2

    class Node:
        def __init__(self, info_set):
            self.__info_set = info_set
            self.__regret_sum = [0.0] * KuhnPokerTrainer.NUM_ACTIONS
            self.__strategy = [0.0] * KuhnPokerTrainer.NUM_ACTIONS
            self.__strategy_sum = [0.0] * KuhnPokerTrainer.NUM_ACTIONS

        def get_strategy(self, realization_weight):
            normalizing_sum = 0.0
            for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
                self.__strategy[a] = self.__regret_sum[a] if self.__regret_sum[a] > 0 else 0
                normalizing_sum += self.__strategy[a]

            for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
                if normalizing_sum > 0:
                    self.__strategy[a] /= normalizing_sum
                else:
                    self.__strategy[a] = 1.0 / KuhnPokerTrainer.NUM_ACTIONS
                self.__strategy_sum[a] += realization_weight * self.__strategy[a]
            return self.__strategy

        def get_average_strategy(self):
            avg_strategy = [0.0] * KuhnPokerTrainer.NUM_ACTIONS
            normalizing_sum = 0.0
            for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
                normalizing_sum += self.__strategy_sum[a]
            for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
                if normalizing_sum > 0:
                    avg_strategy[a] = self.__strategy_sum[a] / normalizing_sum
                else:
                    avg_strategy[a] = 1.0 / KuhnPokerTrainer.NUM_ACTIONS
            return avg_strategy

        def add_regret_sum(self, a, val):
            self.__regret_sum[a] += val

        def __str__(self):
            return f"{self.__info_set}: {str(self.get_average_strategy())}"

    def __init__(self):
        self.__node_map = {}

    def train(self, iterations):
        cards = [KuhnPokerCard.Jack, KuhnPokerCard.Queen, KuhnPokerCard.King]
        util = 0.0
        for i in range(0, iterations):
            shuffle(cards)
            util += self.cfr(cards, "", 1.0, 1.0)
        print(f"Average game value: {util/iterations}")
        for n in self.__node_map:
            print(self.__node_map[n])

    def cfr(self, cards, history, p0, p1):
        plays = len(history)
        player = plays % 2
        opponent = 1 - player
        if plays > 1:
            terminal_pass = history[plays - 1] == 'p'
            double_bet = history[plays-2:plays] == "bb"
            is_player_card_higher = cards[player] > cards[opponent]
            if terminal_pass:
                if history == "pp":
                    return 1 if is_player_card_higher else -1
                else:
                    return 1
            elif double_bet:
                return 2 if is_player_card_higher else -2

        info_set = f"{cards[player]}{history}"
        node = self.__node_map.get(info_set)
        if node is None:
            node = KuhnPokerTrainer.Node(info_set)
            self.__node_map[info_set] = node

        strategy = node.get_strategy(p0 if player == 0 else p1)
        util = [0.0] * KuhnPokerTrainer.NUM_ACTIONS
        node_util = 0.0

        for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
            next_history = f"{history}{'p' if a == 0 else 'b'}"
            util[a] = - self.cfr(cards, next_history, p0 * strategy[a], p1) if player == 0 else - self.cfr(cards, next_history, p0, p1 * strategy[a])
            node_util += strategy[a] * util[a]

        for a in range(0, KuhnPokerTrainer.NUM_ACTIONS):
            regret = util[a] - node_util
            node.add_regret_sum(a, (p1 if player == 0 else p0) * regret)

        return node_util

    def get_avg_strategy(self, info_set):
        node = self.__node_map.get(info_set)
        return node.get_average_strategy()
