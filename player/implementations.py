from player_base import *


class SimplePlayer(HashedPlayer):
    """ Simplest Player. Only relies on the basic heuristics every Alpha Beta Player has,
    which just liiks wether The player wins or not."""

    def score(self, gb, depth):
        return 0


class Count3Player(HashedPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""

    def score(self, gb, depth):
        return gb.count3(self.color) - gb.count3(gb.other_player(self.color))


class StrategyChangePlayer(HashedPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 30

    def __init__(self, color, params):
        self.simplePlayer = SimplePlayer(color, params)
        self.count3Player = Count3Player(color, params)
        super().__init__(color, params)

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return self.count3Player.score(gb, depth)
        else:
            return self.simplePlayer.score(gb, depth)


class HashedSimplePlayer(HashedPlayer):
    """ Simplest Player. Only relies on the basic heuristics every Alpha Beta Player has,
    which just liiks wether The player wins or not."""
    MIN_HASH_DEPTH = 3

    def score(self, gb, depth):
        return 0


class HashedCount3Player(HashedPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 3

    def score(self, gb, depth):
        return gb.count3(self.color) - gb.count3(gb.other_player(self.color))


class HashedStrategyChangePlayer(HashedPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 30
    MIN_HASH_DEPTH = 3

    def __init__(self, color, params):
        self.simplePlayer = SimplePlayer(color, params)
        self.count3Player = Count3Player(color, params)
        super().__init__(color, params)

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return self.count3Player.score(gb, depth)
        else:
            return self.simplePlayer.score(gb, depth)
