import time


class Player:
    IS_HUMAN = False

    def __init__(self, color, params):
        self.color = color
        if params.timeout is not None:
            self.timeout = params.timeout
        else:
            self.timeout = 0xdeadbeef

    def next_move(self, gb):
        """Takes a game board and returns the next move"""
        raise NotImplementedError("Please Implement this method")

    def get_name(self):
        """Returns Name of this player"""
        return self.__class__.__name__


class HumanPlayer(Player):
    IS_HUMAN = True

    def next_move(self, gb):
        while True:
            move_raw = input("Player {}, were do you want to move next? ".format(gb.get_occupation_string(self.color)))
            if move_raw == "exit":
                exit(0)
            try:
                move = int(move_raw)
            except ValueError:
                print("Please enter an Integer.")
                continue
            if not gb.is_legal(move):
                print("You can't play there.")
            else:
                return move


class TimedPlayer(Player):
    SAFETY_TIME = .05

    def next_move(self, gb):
        timeout = time.time() + self.timeout - self.SAFETY_TIME
        move = 0
        try:
            for depth in range(gb.ROWS * gb.COLS):
                move = self.next_move_timeout(gb, depth, timeout)
        except TimeoutError:
            pass
        return move

    def next_move_timeout(self, gb, depth, timeout):
        """Tries to calculate best move within a certain timeout. If timeout is reached before,
        a timeout exception gets thrown."""
        raise NotImplementedError("Please Implement this method")


class AlphaBetaPlayer(TimedPlayer):
    POSITION_ORDER = [3, 2, 4, 5, 1, 0, 6]
    ALPHA_INIT = -100000
    BETA_INIT = -ALPHA_INIT
    WIN_SCORE = 1000

    def next_move_timeout(self, gb, depth, timeout):
        player = gb.other_player(self.color)
        alpha = self.ALPHA_INIT
        beta = self.BETA_INIT

        clone = gb.clone()
        bestMove = -1

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, player):
                if clone.has_won(player):
                    return pos
                score = -self.miniMax(clone, depth - 1, gb.other_player(player), -beta, -alpha, timeout)
                if score > alpha:
                    alpha = score
                    bestMove = pos
                clone = gb.clone()
        return bestMove

    def miniMax(self, gb, depth, player, alpha, beta, timeout):
        if gb.has_won(gb.other_player(player)):
            return -self.WIN_SCORE * depth
        elif gb.has_won(player):
            return self.WIN_SCORE * depth + 1
        elif alpha >= beta:
            return beta
        elif depth <= 0:
            return self.score(gb, depth)
        elif timeout < time.time():
            raise TimeoutError()

        clone = gb.clone()

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, player):
                if clone.has_won(player):
                    return pos
                score = -self.miniMax(clone, depth - 1, gb.other_player(player), -beta, -alpha, timeout)
                if score >= beta:
                    return score
                elif score > alpha:
                    alpha = score
                clone = gb.clone()
        return alpha

    def score(self, gb, depth):
        """Gives a score to a given position."""
        raise NotImplementedError("Please Implement this method")


class SimplePlayer(AlphaBetaPlayer):
    def score(self, gb, depth):
        if gb.has_won(self.color):
            return 100 * depth
        elif gb.has_won(gb.other_player(self.color)):
            return -1000 * depth
        else:
            return 0
