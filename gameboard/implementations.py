#!/usr/bin/python3
from gameboard.base import *


class BasicGameBoard(GameBoard):
    """Basic Gameboard using an array as the game field. Flexible in size"""

    # All directions 4 in a row could appear
    DIRECTIONS = [
        (0, 1),  # Vertical |
        (1, 0),  # Horizontal -
        (1, 1),  # Diagonal /
        (-1, 1),  # Diagonal \
    ]

    def __init__(self):
        self.field = np.ndarray(shape=(self.ROWS, self.COLS), dtype=np.byte)
        self.field.fill(self.EMPTY)

    def set_occupation(self, row, col, player):
        self.field[row][col] = player

    def get_occupation(self, row, col):
        return self.field[row][col]

    def has_won(self, player):
        for direction in self.DIRECTIONS:
            if direction[0] > 0:
                start_r = 0
                end_r = self.ROWS - direction[0] * 3
            else:
                start_r = direction[0] * -3
                end_r = self.ROWS

            if direction[1] > 0:
                start_c = 0
                end_c = self.COLS - direction[1] * 3
            else:
                start_c = direction[1] * -3
                end_c = self.COLS

            for r in range(start_r, end_r):
                for c in range(start_c, end_c):
                    if self.has_won_dir(r, c, direction, player):
                        return True
        return False

    def has_won_dir(self, row, col, direction, player):
        """Checks wether a player has 4 in a row starting from a given row, col and with a given direction"""
        for i in range(4):
            if self.get_occupation(row + i * direction[0], col + i * direction[1]) != player:
                return False
        return True

    def is_full(self):
        for r in range(self.ROWS):
            if self.field[r][-1] == self.EMPTY:
                return False
        return True

    def place_stone(self, r, player):
        for c in range(self.COLS):
            if self.get_occupation(r, c) == self.EMPTY:
                self.set_occupation(r, c, player)
                return True
        return False

    def is_legal(self, row):
        return 0 <= row < self.ROWS and self.field[row][-1] == self.EMPTY


class BitBoard7x6(GameBoard):
    """BitBoard Class

      | .  .  .  .  .  .  .  TOP
    6 | 6 14 22 30 38 46 54
    5 | 5 13 21 29 37 45 53
    4 | 4 12 20 28 36 44 52
    3 | 3 11 19 27 35 43 51
    2 | 2 10 18 26 34 42 50
    1 | 1  9 17 25 33 41 49
    0 | 0  8 16 24 32 40 48  BOTTOM
      | TTTTTTTTTTTTTTTTTTT
      | 0  1  2  3  4  5  6

    """

    # WARNING: THESE CONSTANTS CANNOT BE CHANGED
    # WITHOUT BRAKING IMPORTANT FUNCTIONS
    RED = 0
    YELLOW = 1
    EMPTY = 2

    ROWS = 7
    COLS = 6

    # Constants used for bit count
    M1 = np.int64(0x5555555555555555)
    M2 = np.int64(0x3333333333333333)
    M4 = np.int64(0x0f0f0f0f0f0f0f0f)
    H01 = np.int64(0x0101010101010101)

    # Masks for each row (vertical)
    ROW_MASKS = np.array([0x0000000000003f,
                          0x00000000003f00,
                          0x000000003f0000,
                          0x0000003f000000,
                          0x00003f00000000,
                          0x003f0000000000,
                          0x3f000000000000], dtype=np.int64)

    def __init__(self):
        self.disks = np.zeros(shape=(2), dtype=np.int64)
        self.top_empty = np.int64(0x01010101010101)

    def copy_gamestate(self, other):
        if isinstance(other, self.__class__):
            self.disks[0] = other.disks[0]
            self.disks[1] = other.disks[1]
            self.top_empty = other.top_empty
        else:
            super().copy_gamestate(other)

    def update_top_empty(self):
        self.top_empty = np.int64(0)
        for r in range(self.ROWS):
            for c in range(self.COLS + 1):
                position = 1 << (c + 8 * r)
                if c == self.COLS or self.get_occupation(r, c) == self.EMPTY:
                    print("top empty at ", r, c)
                    self.top_empty |= position
                    break

    @classmethod
    def other_player(cls, player):
        return 1 - player

    @classmethod
    def count_bits(self, x):
        x -= (x >> 1) & self.M1
        x = (x & self.M2) + ((x >> 2) & self.M2)
        x = (x + (x >> 4)) & self.M4
        return (x * self.H01) >> 56

    def place_stone(self, r, player):
        position = self.ROW_MASKS[r] & self.top_empty
        if position != 0:
            self.disks[player] |= position
            self.top_empty = self.top_empty ^ position | position << 1
            return True
        else:
            return False

    def is_top(self, row, col):
        position = 1 << (col + 8 * row)
        return (self.top_empty & position) != 0

    def get_occupation(self, row, col):
        position = 1 << (col + 8 * row)
        if (self.disks[0] & position) != 0:
            return self.RED
        elif (self.disks[1] & position) != 0:
            return self.YELLOW
        else:
            return self.EMPTY

    def set_occupation(self, row, col, player):
        position = 1 << (col + 8 * row)
        self.disks[player] |= position
        self.disks[1 - player] &= ~position

    def has_won(self, player):
        board = self.disks[player]

        # Diagonal \
        y = board & board >> 7
        if y & (y >> 14):
            return True

        # Horizontal -
        y = board & board >> 8
        if y & (y >> 16):
            return True

        # Diagonal /
        y = board & board >> 9
        if y & (y >> 18):
            return True

        # Vertical |
        y = board & board >> 1
        if y & (y >> 2):
            return True

        return False

    def is_full(self):
        return (self.top_empty & 0x3f3f3f3f3f3f3f) == 0

    def is_legal(self, row):
        return 0 <= row < self.ROWS and self.top_empty & self.ROW_MASKS[row] != 0

    def count3(self, player):
        board = self.disks[player]

        # vertical
        possible = (board << 1) & (board << 2) & (board << 3)  # straight up

        # horizontal
        intermed = (board << 8) & (board << 16)  # two on left
        possible |= intermed & (board << 24)  # XXX.
        possible |= intermed & (board >> 8)  # XX.X

        intermed = (board >> 8) & (board >> 16)  # two on right
        possible |= intermed & (board >> 24)  # .XXX
        possible |= intermed & (board << 8)  # X.XX

        # diagonal 1
        intermed = (board << 7) & (board << 16)
        possible |= intermed & (board << 21)
        possible |= intermed & (board >> 7)
        intermed = (board >> 7) & (board >> 16)
        possible |= intermed & (board >> 21)
        possible |= intermed & (board << 7)

        # diagonal 2
        intermed = (board << 9) & (board << 18)
        possible |= intermed & (board << 27)
        possible |= intermed & (board >> 9)
        intermed = (board >> 9) & (board >> 18)
        possible |= intermed & (board >> 27)
        possible |= intermed & (board << 9)

        possible &= ~self.disks[1 - player]

        # Weighted
        return 7 * self.count_bits(possible & 0x01010101010101) + \
            6 * self.count_bits(possible & 0x02020202020202) +\
            5 * self.count_bits(possible & 0x04040404040404) +\
            4 * self.count_bits(possible & 0x08080808080808) +\
            3 * self.count_bits(possible & 0x10101010101010) +\
            2 * self.count_bits(possible & 0x20202020202020) +\
            1 * self.count_bits(possible & 0x40404040404040)

    def __eq__(self, other):
        if not isinstance(other, BitBoard7x6):
            return super().__eq__(other)
        else:
            return self.disks[0] == other.disks[0] and self.disks[1] == other.disks[1]

    def __lt__(self, other):
        if not isinstance(other, BitBoard7x6):
            return super().__lt__(other)
        else:
            return self.disks[0] < other.disks[0] or self.disks[1] < other.disks[1]

    def __hash__(self):
        """ Custom Hash function, really simple but fast."""
        return int(self.disks[0] - self.disks[1])
