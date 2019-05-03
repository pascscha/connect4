#!/usr/bin/python3

import time
import random
import requests
import json
import os

"""
This file contains all Abstract Player classes but no actual finished Implementations.
The Finished Implementations can be cound in the file implementations.py
"""


class Player:
    """[Abstract] Base Class for a Connect4 Player"""
    IS_HUMAN = False

    def __init__(self, color, params):
        self.color = color
        self.params = params
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
    """Human Player that lets user choose where to play"""
    IS_HUMAN = True

    def __init__(self, color, params):
        self.name = input("Hi Human Player, what's your name? ")
        print("Nice to meet you, {}.".format(self.name))

        super().__init__(color, params)

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
                # gb = gb.clone()
                # gb.place_stone(move, self.color)
                # print(gb)
                # p = SimplePlayer(gb.other_player(self.color), self.params)
                # print("SCORE:", p.score(gb, 5))
                return move

    def get_name(self):
        return self.name


class TimedPlayer(Player):
    """[Abstract] Base Class for plaers with time limits"""
    SAFETY_FACTOR = .95

    def next_move(self, gb):
        timeout = time.time() + self.timeout * self.SAFETY_FACTOR
        move = 0
        try:
            moves_left = gb.moves_left()
            for depth in range(moves_left):
                move = self.next_move_timeout(gb, depth, timeout)
        except TimeoutError:
            pass
        return move

    def next_move_timeout(self, gb, depth, timeout):
        """Tries to calculate best move within a certain timeout. If timeout is reached before,
        a timeout exception gets thrown."""
        raise NotImplementedError("Please Implement this method")


class DepthPlayer(TimedPlayer):
    """[Abstract] Base Class for players that always have the same serach depth (useful for debugging)"""
    DEPTH = 6

    def next_move(self, gb):
        timeout = time.time() + 100
        move = self.next_move_timeout(gb, self.DEPTH, timeout)
        return move


class MinimaxPlayer(TimedPlayer):
    """[Abstract] Alpha Beta Player - Uses Alpha Beta Algorithm to evaluate Game Tree"""
    POSITION_ORDER = [3, 2, 4, 5, 1, 0, 6]
    WIN_SCORE = 1000

    MAX_SCORE = 0xfffffff0
    MIN_SCORE = -MAX_SCORE

    def next_move_timeout(self, gb, depth, timeout):
        player = self.color  # gb.other_player(self.color)

        clone = gb.clone()
        bestMove = -1
        bestScore = self.MIN_SCORE

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, player):
                score = self.min(clone, depth - 1, timeout)
                if score > bestScore:
                    bestScore = score
                    bestMove = pos
                clone = gb.clone()
        return bestMove

    def min(self, gb, depth, timeout):
        if gb.has_won(self.color):
            return self.WIN_SCORE * (depth + 1)
        elif timeout < time.time():
            raise TimeoutError()
        elif depth <= 0:
            return self.score(gb, depth)

        clone = gb.clone()

        bestScore = self.MAX_SCORE

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, gb.other_player(self.color)):
                score = self.max(clone, depth - 1, timeout)
                if score < bestScore:
                    bestScore = score
                clone = gb.clone()
        return bestScore

    def max(self, gb, depth, timeout):
        if gb.has_won(gb.other_player(self.color)):
            return - self.WIN_SCORE * (depth + 1)
        elif timeout < time.time():
            raise TimeoutError()
        elif depth <= 0:
            return self.score(gb, depth)

        clone = gb.clone()

        bestScore = self.MIN_SCORE

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, self.color):
                score = self.min(clone, depth - 1, timeout)
                if score > bestScore:
                    bestScore = score
                clone = gb.clone()
        return bestScore

    def score(self, gb, depth):
        """Gives a score to a given position."""
        raise NotImplementedError("Please Implement this method")


class AlphaBetaPlayer(TimedPlayer):
    """[Abstract] Alpha Beta Player - Uses Alpha Beta Algorithm to evaluate Game Tree"""
    POSITION_ORDER = [3, 2, 4, 5, 1, 0, 6]
    WIN_SCORE = 1000

    ALPHA_INIT = -0xfffffffffffffff0
    BETA_INIT = -ALPHA_INIT

    def next_move_timeout(self, gb, depth, timeout):
        player = self.color  # gb.other_player(self.color)
        alpha = self.ALPHA_INIT
        beta = self.BETA_INIT

        clone = gb.clone()
        bestMove = -1

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, player):
                score = self.min(clone, depth - 1, alpha, beta, timeout)
                if score > alpha:
                    alpha = score
                    bestMove = pos
                clone = gb.clone()
        return bestMove

    def min(self, gb, depth, alpha, beta, timeout):
        if gb.has_won(self.color):
            return self.WIN_SCORE * (depth + 1)
        elif timeout < time.time():
            raise TimeoutError()
        elif depth <= 0:
            return self.score(gb, depth)

        clone = gb.clone()

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, gb.other_player(self.color)):
                score = self.max(clone, depth - 1, alpha, beta, timeout)
                if score < beta:
                    beta = score
                if alpha >= beta:
                    return beta
                clone = gb.clone()
        return beta

    def max(self, gb, depth, alpha, beta, timeout):
        if gb.has_won(gb.other_player(self.color)):
            return - self.WIN_SCORE * (depth + 1)
        elif timeout < time.time():
            raise TimeoutError()
        elif depth <= 0:
            return self.score(gb, depth)

        clone = gb.clone()

        for pos in self.POSITION_ORDER:
            if clone.place_stone(pos, self.color):
                score = self.min(clone, depth - 1, alpha, beta, timeout)
                if score > alpha:
                    alpha = score
                if alpha >= beta:
                    return alpha
                clone = gb.clone()
        return alpha

    def score(self, gb, depth):
        """Gives a score to a given position."""
        raise NotImplementedError("Please Implement this method")


class RandomizedAlphaBetaPlayer(AlphaBetaPlayer):
    """[Abstract] Uses Alpha Beta Player but randomizes search order sligtly.
    Prevents Player from always playing in the center row."""
    POSITION_ORDER_BASE = [3, 2, 4, 5, 1, 0, 6]
    POSITION_ORDER = [3, 2, 4, 5, 1, 0, 6]
    RANDOMNESS = .3
    random.seed(0)

    def random_order(self):
        for i in range(len(self.POSITION_ORDER_BASE)):
            self.POSITION_ORDER[i] = self.POSITION_ORDER_BASE[i]

        for i in range(len(self.POSITION_ORDER_BASE) - 1):
            if random.random() < self.RANDOMNESS:
                temp = self.POSITION_ORDER[i]
                self.POSITION_ORDER[i] = self.POSITION_ORDER[i + 1]
                self.POSITION_ORDER[i + 1] = temp

    def next_move_timeout(self, gb, depth, timeout):
        self.random_order()  # Randomize order before every move
        return super().next_move_timeout(gb, depth, timeout)


class HashedPlayer(AlphaBetaPlayer):
    """[Abstract] Player that uses a hashmap in order to cut away transpositions."""
    MIN_HASH_DEPTH = 0

    def next_move_timeout(self, gb, depth, timeout):
        self.hash_map = []
        for i in range(depth + 1):
            self.hash_map.append({})
        return super().next_move_timeout(gb, depth, timeout)

    def min(self, gb, depth, alpha, beta, timeout):
        if depth >= self.MIN_HASH_DEPTH:
            if gb in self.hash_map[depth]:
                return self.hash_map[depth][gb]
            else:
                score = super().min(gb, depth, alpha, beta, timeout)
                self.hash_map[depth][gb] = score
                return score
        else:
            return super().min(gb, depth, alpha, beta, timeout)

    def max(self, gb, depth, alpha, beta, timeout):
        if depth >= self.MIN_HASH_DEPTH:
            if gb in self.hash_map[depth]:
                return self.hash_map[depth][gb]
            else:
                score = super().max(gb, depth, alpha, beta, timeout)
                self.hash_map[depth][gb] = score
                return score
        else:
            return super().max(gb, depth, alpha, beta, timeout)


class BookPlayer(AlphaBetaPlayer):
    """[Abstract] Player that uses an opening book for the first moves"""

    # The book file
    BOOK = os.path.dirname(os.path.realpath(__file__)) + "/7x6.book"

    # Lowest score
    MIN_SCORE = -0xfffffff0

    def __init__(self, color, params):
        print("Init")
        try:
            with open(self.BOOK, "rb") as f:
                self.WIDTH = self.bytes2int(f.read(1))
                self.HEIGHT = self.bytes2int(f.read(1))
                self.DEPTH = self.bytes2int(f.read(1))
                self.KEY_SIZE = self.bytes2int(f.read(1))
                self.VALUE_SIZE = self.bytes2int(f.read(1))
                self.LOG_SIZE = self.bytes2int(f.read(1))
                self.BOOK_SIZE = self.next_prime(1 << self.LOG_SIZE)
                self.KEYS = f.read(self.BOOK_SIZE)
                self.VALUES = f.read(self.BOOK_SIZE)
            self.book_open = True
        except Exception as e:
            print("Could not open book.", e)
            self.book_open = False

        super().__init__(color, params)

    @staticmethod
    def bytes2int(str):
        """Converts bytes to an integer"""
        return int.from_bytes(str, byteorder='big')

    @classmethod
    def med(cls, lower, upper):
        """Returns the average between upper and lower rounded down to the next integer"""
        return (upper + lower) // 2

    @classmethod
    def has_factor(cls, n, lower, upper):
        """checks if n has any factor inbetween lower and upper"""
        if lower ** 2 > n:
            return False
        elif lower + 1 >= upper:
            return n % lower == 0
        else:
            return cls.has_factor(n, lower, cls.med(lower, upper)) or \
                cls.has_factor(n, cls.med(lower, upper), upper)

    @classmethod
    def next_prime(cls, n):
        """Calculates the next biggest prime number of n."""
        if cls.has_factor(n, 2, n):
            return cls.next_prime(n + 1)
        else:
            return n

    def read_book(self, gb):
        """Returns best Score stored in its book for this position.
        If this position is not stored in the book it returns none."""
        if gb.ROWS * gb.COLS - gb.moves_left() <= self.DEPTH:
            i = gb.base3Rep(self.color)

            if i > len(self.KEYS):
                return None

            key = self.KEYS[i]

            if i % (1 << (self.KEY_SIZE * 8)) != key:
                return None
            else:
                return 19 - self.VALUES[i]
        else:
            return None

    def next_move(self, gb):
        if self.book_open:

            clone = gb.clone()
            bestMove = -1
            bestScore = self.MIN_SCORE
            has_none = False

            for pos in self.POSITION_ORDER:
                if clone.place_stone(pos, self.color):
                    score = self.read_book(clone)
                    clone = gb.clone()
                    if score is None:
                        has_none = True
                        continue
                    if score > bestScore:
                        bestScore = score
                        bestMove = pos

            if bestMove < 0 and has_none:
                self.book_open = False
                return super().next_move(gb)
            else:
                return bestMove
        else:
            return super().next_move(gb)


class Cheater(Player):
    """[Abstract] Cheating Player that looks for the best possible move online."""

    IS_HUMAN = True  # No timelimits for now

    def __init__(self, color, params):
        self.move_string = ""  # String containing all moves up to this position
        super().__init__(color, params)

    def solve(self, pos):
        """Call online solver in order to get best move"""
        raw_text = requests.get("https://connect4.gamesolver.org/solve?pos={}".format(pos)).text
        scores = json.loads(raw_text)["score"]

        for i in range(len(scores)):
            if scores[i] == 100:  # When a column is full the solver assings it score 100
                scores[i] = -100

        best = max(scores)  # Get the best score ...
        return scores.index(best)  # ... and return the index of it

    def update_gamestate(self, gb):
        """Updates gamesate (self.move_string) according to the game.the
        Only works if there is at most 1 new stone on the board"""
        my_gamestate = gb.__class__()
        my_gamestate.apply_move_string(self.move_string, offset=1)
        for r in range(gb.ROWS):
            for c in range(gb.COLS):
                if gb.get_occupation(r, c) != my_gamestate.get_occupation(r, c):
                    self.move_string += str(r + 1)
                    return
