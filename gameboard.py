
import numpy


class GameBoard:
    ROWS = 6
    COLS = 7

    EMPTY = 0
    YELLOW = 1
    RED = 2

    STRINGS = {
        EMPTY: " ",
        YELLOW: "O",
        RED: "X"
    }

    def __init__(self):
        for r in range(ROWS):
            for c in range(COLS):
                self.set_field(r, c, self.EMPTY)

    def set_field(self, row, col, value):
        """Sets The field at row, col to a specific value"""
        raise NotImplementedError("Please Implement this method")

    def get_field(self, row, col):
        """Gets the field value at row, col"""
        raise NotImplementedError("Please Implement this method")

    def has_won(self, player):
        """Determines if a given player has won or not"""
        raise NotImplementedError("Please Implement this method")

    def is_finished(self):
        """Checks if the game has finished"""
        raise NotImplementedError("Please Implement this method")

    def place_stone(self, col):
        """Place a stone into a column and let it drop to the bottom"""
        raise NotImplementedError("Please Implement this method")

    def __str__(self):
        """Returns a string representation of the game board"""
        lines = []
        for c in range(self.COLS):
            occupations = []
            for r in range(self.ROWS):
                occupation = self.get_field(r, c)
                if occupation in self.STRINGS:
                    occupations.append(self.STRINGS[occupation])
                else:
                    raise ValueError("Invalid Game Board occupation: {}".format(occupation))
            lines.append("|".join(occupations))
        lines.append("|".join(range(self.ROWS)))
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
                    if self.get_field(r, c) != other.get_field(r, c):
                        return False
            return True
