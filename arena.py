import time


class Arena:

    @classmethod
    def play_game(cls, playerClsRed, playerClsYellow, gameBoardCls, params):
        gb = gameBoardCls()
        playerRed = playerClsRed(gb.RED, params)
        playerYellow = playerClsYellow(gb.YELLOW, params)

        redsTurn = False
        move = 0

        while not gb.is_finished():

            if redsTurn:
                active_player = playerRed
            else:
                active_player = playerYellow

            start_time = time.time()

            success, mv = cls.make_move(active_player, gb)
            if not success:
                return Outcome(gb, red_won=not redsTurn, last_move=mv, illegal=True)

            elif params.timeout is not None and not active_player.IS_HUMAN and time.time() - start_time > params.timeout:
                return Outcome(gb, red_won=not redsTurn, timeout=True)

            elif gb.has_won(active_player.color):
                return Outcome(gb, red_won=redsTurn)

            if params.verbose:
                print("\nMove #{} - {} ({}):".format(move,
                                                     gb.get_occupation_string(active_player.color),
                                                     active_player.get_name()))
            for r in range(gb.ROWS):
                if r == mv:
                    print("v", end=" ")
                else:
                    print(" ", end=" ")
            print()
            print(gb)

            redsTurn = not redsTurn
            move += 1
        return Outcome(gb, red_won=False, tie=True)

    @classmethod
    def make_move(cls, player, gb):
        move = player.next_move(gb)
        if not gb.is_legal(move):
            return False, move
        else:
            gb.place_stone(move, player.color)
            return True, move


class Outcome:
    def __init__(self, gb, red_won=True, illegal=False, last_move=None, timeout=False, tie=False):
        self.gb = gb
        self.red_won = red_won
        self.illegal = illegal
        self.tie = tie
        self.timeout = timeout
        self.last_move = last_move

    def __str__(self):
        if self.tie:
            return "Tie"
        elif self.illegal:
            if self.red_won:
                who = self.gb.YELLOW
            else:
                who = self.gb.RED
            return "{} made an Illegal move ({})".format(self.gb.get_occupation_string(who), self.last_move)
        elif self.timeout:
            if self.red_won:
                who = self.gb.YELLOW
            else:
                who = self.gb.RED
            return "{} timed out".format(self.gb.get_occupation_string(who))
        elif self.red_won:
            who = self.gb.RED
        else:
            who = self.gb.YELLOW
        return "{} Won".format(self.gb.get_occupation_string(who))

    def get_char(self):
        if self.tie:
            return "T"
        elif self.illegal:
            return "I"
        elif self.timeout:
            return "t"
        elif self.red_won:
            return "<"
        else:
            return "^"


class GameParameters:
    def __init__(self, timeout=None, verbose=True):
        self.timeout = timeout
        self.verbose = verbose
