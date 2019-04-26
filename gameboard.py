#!/usr/bin/python3

import numpy as np


class GameBoard:
    ROWS = 7
    COLS = 6

    EMPTY = 0
    YELLOW = 1
    RED = 2

    STRINGS = {
        EMPTY: " ",
        YELLOW: "O",
        RED: "X"
    }

    def __init__(self):
        for r in range(self.ROWS):
            for c in range(self.COLS):
                self.set_occupation(r, c, self.EMPTY)

    def set_occupation(self, row, col, value):
        """Sets The field at row, col to a specific value"""
        raise NotImplementedError("Please Implement this method")

    def get_occupation(self, row, col):
        """Gets the field value at row, col"""
        raise NotImplementedError("Please Implement this method")

    def has_won(self, player):
        """Determines if a given player has won or not"""
        raise NotImplementedError("Please Implement this method")

    def is_finished(self):
        """Checks if the game has finished"""
        raise NotImplementedError("Please Implement this method")

    def is_full(self):
        """Checks wether the game board is full"""
        raise NotImplementedError("Please Implement this method")

    def is_legal(self, row):
        """Checks wether any player can play in this row"""
        raise NotImplementedError("Please Implement this method")

    def place_stone(self, row):
        """Place a stone into a column and let it drop to the bottom.
        Returns True iff Action was successfull"""
        raise NotImplementedError("Please Implement this method")

    @classmethod
    def get_occupation_string(cls, occupation):
        if occupation in cls.STRINGS:
            return cls.STRINGS[occupation]
        else:
            raise ValueError("Invalid Game Board occupation: {}".format(occupation))

    def __str__(self):
        """Returns a string representation of the game board"""
        lines = []
        for c in range(self.COLS - 1, -1, -1):
            occupations = []
            for r in range(self.ROWS):
                occupation = self.get_occupation(r, c)
                occupation_string = self.get_occupation_string(occupation)
                occupations.append(occupation_string)
            lines.append("|".join(occupations))
        lines.append("-" * (2 * self.ROWS - 1))
        numbers = []
        for n in range(self.ROWS):
            numbers.append(str(n))
        lines.append("|".join(numbers))
        return "\n".join(lines)

    def __eq__(self, other):
        if not isinstance(self, other):  # Check if both of them are Gameboards
            raise ValueError("Can't compare {} and {}.".format(type(self), type(other)))
        else:
            if self.ROWS != other.ROWS or self.COLS != other.COLS:  # Check if dimensions match
                return False

            # Check if all other fields are equal
            for r in range(self.ROWS):
                for c in range(other.ROWS):
                    if self.get_occupation(r, c) != other.get_occupation(r, c):
                        return False
            return True


class BasicGameBoard(GameBoard):
    DIRECTIONS = [
        (0, 1),
        (1, 0),
        (1, 1),
        (-1, 1),
    ]

    def __init__(self):
        self.field = np.ndarray(shape=(self.ROWS, self.COLS), dtype=np.byte)
        self.field.fill(self.EMPTY)

    def set_occupation(self, row, col, value):
        self.field[row][col] = value

    def get_occupation(self, row, col):
        return self.field[row][col]

    def has_won(self, player):
        for direction in self.DIRECTIONS:
            if direction[0] > 0:
                start_r = 0
                end_r = self.ROWS - direction[0] * 4
            else:
                start_r = direction[0] * -4
                end_r = self.ROWS

            if direction[1] > 0:
                start_c = 0
                end_c = self.COLS - direction[1] * 4
            else:
                start_c = direction[1] * -4
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

    def is_finished(self):
        return self.is_full() or self.has_won(self.RED) or self.has_won(self.YELLOW)

    def is_full(self):
        for r in range(self.ROWS):
            if self.field[r][-1] == self.EMPTY:
                return False
        return True

    def place_stone(self, r, value):
        for c in range(self.COLS):
            if self.get_occupation(r, c) == self.EMPTY:
                self.set_occupation(r, c, value)
                return True
        return False

    def is_legal(self, row):
        return 0 <= row < self.ROWS and self.field[row][-1] == self.EMPTY
