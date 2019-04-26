
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

    def is_full(self):
        """Checks wether the game board is full"""
        raise NotImplementedError("Please Implement this method")

    def place_stone(self, col):
        """Place a stone into a column and let it drop to the bottom.
        Returns True iff Action was successfull"""
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


class BasicGameBoard(GameBoard):
    DIRECTIONS = [
        (0, 1),
        (1, 0),
        (1, 1),
        (-1, 1),
    ]

    def __init__(self):
        self.field = np.array((self.ROWS, self.COLS), self.EMPTY)

    def set_field(self, row, col, value):
        self.field[row][col] = value

    def get_field(self, row, col):
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
            if self.get_field(row + i * direction[0], col + i * direction[1]) != player:
                return False
        return True

    def is_finished(self):
        return self.is_full() or self.has_won(self.RED) or self.has_won(self.YELLOW)

    def is_full(self):
        for r in range(self.ROWS):
            if self.field[r][-1] == self.EMPTY:
                return False
        return True

    def place_stone(self, c, value):
        for r in range(self.ROWS - 1, -1, -1):
            if self.field[r][c] == self.EMPTY:
                self.field[r][c] == value
                return True
        return False
