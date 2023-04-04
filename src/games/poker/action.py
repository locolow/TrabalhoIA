from enum import Enum


class KuhnPokerAction(Enum):
    """
    a kuhn poker action is simple - pass or bet
    a pass is either a check (no money is in the table) or a fold (if there is a bet)
    a bet is either a regular bet (no money in the table) or a call (if there is a bet)
    """
    PASS = 0,
    BET = 1
