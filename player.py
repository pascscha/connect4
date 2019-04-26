class Player:
    def __init__(self, color, params):
        self.color = color
        self.timeout = params.timeout

    def next_move(self, gb):
        """Takes a game board and returns the next move"""
        raise NotImplementedError("Please Implement this method")

    def get_name(self):
        """Returns Name of this player"""
        return self.__class__.__name__


class HumanPlayer(Player):
    def next_move(self, gb):
        while True:
            move_raw = input("Player {}, were do you want to move next? ".format(gb.get_occupation_string(self.color)))
            try:
                move = int(move_raw)
            except:
                print("Please enter an Integer.")
                continue
            if not gb.is_legal(move):
                print("You can't play there.")
            else:
                return move
