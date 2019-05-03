from player.base import *


def score_simple(gb, color):
    return 0


def score_count3(gb, color):
    return gb.count3(color) - gb.count3(gb.other_player(color))


class SimplePlayerMinimax(MinimaxPlayer):
    """Simple Player using Minimax Algorithm"""

    def score(self, gb, depth):
        return score_simple(gb, self.color)


class SimplePlayerAlphaBeta(AlphaBetaPlayer):
    """Simple Player using Minimax Algorithm"""

    def score(self, gb, depth):
        return score_simple(gb, self.color)


class SimplePlayerAlphaBetaRandom(RandomizedAlphaBetaPlayer):
    """Simple Player using Minimax Algorithm"""

    def score(self, gb, depth):
        return score_simple(gb, self.color)


class SimplePlayerAlphaBetaHash(HashedPlayer):
    """ Simple Player using Alpha Beta and Hashing."""

    def score(self, gb, depth):
        return score_simple(gb, self.color)


class Count3PlayerMinimax(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3Player(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerRandom(RandomizedAlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerHash0(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 0

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerHash1(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 1

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerHash2(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 2

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerHash3(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 3

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class Count3PlayerHash4(AlphaBetaPlayer):
    """Tries to maximize 3 in a rows, with a preference of 3 in a rows that are lower on the field"""
    MIN_HASH_DEPTH = 4

    def score(self, gb, depth):
        return score_count3(gb, self.color)


class StrategyChangePlayer(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 30

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayerHash(HashedPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 30

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class SimpleBookPlayer(BookPlayer):
    def score(self, gb, depth):
        return score_simple(gb, self.color)


class Count3BookPlayer(BookPlayer):
    def score(self, gb, depth):
        return score_count3(gb, self.color)


class CheatPlayer(Cheater):
    def drop_disc(self, gb):
        self.update_gamestate(gb)
        out = self.solve(self.move_string)
        self.move_string += str(out + 1)
        return out


"""
.1 Seconds per Move:
    Scoreboard:
    0:  21P Count3PlayerHash
    1:  18P Count3Player
    2:  18P StrategyChangePlayer
    3:   9P SimplePlayerAlphaBeta
    4:   9P SimplePlayerAlphaBetaHash
    5:   0P SimplePlayerMinimax



.1 Seconds per Move:
    0: Count3Player
    1: Count3PlayerHash0
    2: Count3PlayerHash1
    3: Count3PlayerHash2
    4: Count3PlayerHash3
    5: Count3PlayerHash4
    6: StrategyChangePlayer
    7: StrategyChangePlayerHash

      0 1 2 3 4 5 6 7
    0 X < ^ ^ < T < T
    1 < X ^ ^ < < ^ <
    2 < < X ^ ^ < < ^
    3 < ^ ^ X ^ ^ ^ ^
    4 ^ < ^ ^ X ^ < <
    5 < < ^ < < X < <
    6 < < < < < < X <
    7 ^ T ^ ^ < ^ T X

    Scoreboard:
    0:  30P Count3PlayerHash1
    1:  28P Count3PlayerHash4
    2:  28P StrategyChangePlayer
    3:  18P Count3PlayerHash2
    4:  17P Count3Player
    5:  16P Count3PlayerHash0
    6:  15P Count3PlayerHash3
    7:  12P StrategyChangePlayerHash



.1 Seconds per Move:
    0 1 2 3 4
    0 X < < < T
    1 < X ^ ^ <
    2 < ^ X ^ <
    3 ^ ^ ^ X ^
    4 T < < < X

    Scoreboard:
    0:  14P Count3BookPlayer
    1:  14P SimpleBookPlayer
    2:  12P Count3Player
    3:  12P Count3PlayerMinimax
    4:   6P Count3PlayerRandom

"""
