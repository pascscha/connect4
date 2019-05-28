from player.base import *
import numpy as np
if machine_learning:
    from keras.models import load_model
    array_x = 0
    array_y = 0
    target = 0
    counter = 0
    model = 0


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
        return 0;
        # return score_simple(gb, self.color)


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


class StrategyChangePlayer5(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 5

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer10(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 10

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer15(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 15

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer20(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 20

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer25(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 25

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer30(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 30

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer35(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 35

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class StrategyChangePlayer40(AlphaBetaPlayer):
    """Combines SimplePlayer and Count3Player by changing to the Simple (and faster) player once the game has advanced enough"""
    STRATEGY_CHANGE = 40

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


class StrategyChangePlayerBook(BookPlayer):
    STRATEGY_CHANGE = 30

    def score(self, gb, depth):
        if depth < self.STRATEGY_CHANGE:
            return score_count3(gb, self.color)
        else:
            return score_simple(gb, self.color)


class CheaterPlayer(Cheater):
    def next_move(self, gb):
        if gb.moves_left() != gb.ROWS * gb.COLS:
            self.update_gamestate(gb)
        out = self.solve(self.move_string)
        self.move_string += str(out + 1)
        return out


class RandomPlayer(Player):
    def next_move(self, gb):
        possible = []
        for r in range(gb.ROWS):
            if(gb.is_legal(r)):
                possible.append(r)
        return random.choice(possible)


class CheaterRandom(Cheater):
    def next_move(self, gb):
        possible = []
        for r in range(gb.ROWS):
            if (gb.is_legal(r)):
                possible.append(r)
        out1 = random.choice(possible)

        if gb.moves_left() != gb.ROWS * gb.COLS:
            self.update_gamestate(gb)
        out2 = self.solve(self.move_string)
        out = random.choice([out1, out2, out2])
        self.move_string += str(out + 1)
        return out


class DataCollector(Cheater):
    """
    def __init__(self, color, params):
        global array_x, array_y, counter
        array_x = np.zeros((21, 6, 7))
        array_x.fill(4)
        array_y = np.zeros((21, 1))
        counter = 0
        super().__init__(color, params)
    """

    def next_move(self, gb):
        global array_x, array_y, counter
        for i in range(7):
            for j in range(6):
                array_x[counter][j][i] = gb.get_occupation(i, 5 - j)

        if gb.moves_left() != gb.ROWS * gb.COLS:
            self.update_gamestate(gb)
        out = self.solve(self.move_string)
        self.move_string += str(out + 1)

        # array_y[counter] = self.topscore

        counter += 1

        return out

    @staticmethod
    def get_x():
        global array_x
        return array_x

    @staticmethod
    def get_y():
        global array_y
        return array_y


class MachineLearning(AlphaBetaPlayer):
    IS_HUMAN = True

    def __init__(self, color, params):
        global array_x, model
        array_x = np.zeros((2, 6, 7, 2))
        model = load_model("keras/AnkerAI2")

        super().__init__(color, params)

    def score(self, gb, depth):
        global array_x, model

        for i in range(7):
            for j in range(6):
                current = gb.get_occupation(i, 5 - j)
                if current == 0:
                    array_x[0][j][i][0] = 1
                    array_x[1][j][6 - i][0] = 1
                elif current == 1:
                    array_x[0][j][i][1] = 1
                    array_x[1][j][6 - i][1] = 1

        prediction = model.predict(array_x)
        return 0.5 * (prediction[0] + prediction[1])


"""


1 Seconds per Move:
      0 1 2 3 4 5
    0 X ^ < < ^ T
    1 T X T ^ < ^
    2 T < X ^ < ^
    3 T ^ < X ^ ^
    4 T < ^ ^ X <
    5 T ^ < ^ ^ X

    Scoreboard:
    0:  16P StrategyChangePlayer
    1:  16P StrategyChangePlayer10
    2:  14P Count3Player
    3:  14P StrategyChangePlayer20
    4:  12P Count3BookPlayer
    5:  11P SimplePlayerAlphaBetaRandom



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



1 Seconds per Move:
      0 1 2 3 4 5 6 7
    0 X ^ < T < < ^ <
    1 < X < ^ < ^ < <
    2 < ^ X < ^ ^ < <
    3 ^ ^ < X ^ T ^ <
    4 T ^ < < X < ^ <
    5 < < ^ < T X T <
    6 ^ < ^ ^ ^ < X <
    7 ^ ^ ^ ^ < ^ ^ X

    Scoreboard:
    0:  30P Count3Player
    1:  24P StrategyChangePlayer
    2:  23P Count3BookPlayer
    3:  23P SimplePlayerAlphaBetaRandom
    4:  22P StrategyChangePlayerBook
    5:  21P Count3PlayerHash0
    6:  17P Count3PlayerRandom
    7:   3P StrategyChangePlayerHash

"""
