import time


class Arena:
    """ Arena Class. This is where the games are managed"""

    @classmethod
    def play_game(cls, playerClsRed, playerClsYellow, gameBoardCls, params):
        """ Plays a game between two Player Classes using a GameBoard Class."""

        # Initialize Classe
        gb = gameBoardCls()
        playerRed = playerClsRed(gb.RED, params)
        playerYellow = playerClsYellow(gb.YELLOW, params)

        if params.verbose:
            print("\nWelcome to the Epic battle of {} vs {}!".format(playerRed.get_name(), playerYellow.get_name()))
            print("Move #0 - {} ({}):".format(gb.get_occupation_string(playerRed.color),
                                              playerRed.get_name()))
            print(gb)

        # Red (1st Player) can start
        redsTurn = True
        move = 0

        while not gb.is_finished():

            # Coose active player class
            if redsTurn:
                active_player = playerRed
            else:
                active_player = playerYellow

            # Measure Time
            start_time = time.time()

            # Make Move
            try:
                legal, mv = cls.make_move(active_player, gb)
            except Exception as e:
                return Outcome(gb, red_won=not redsTurn, error=e)
            # Illegal Move
            if not legal:
                return Outcome(gb, red_won=not redsTurn, last_move=mv, illegal=True)

            # Timeout (Only for non-Human players)
            elif params.timeout is not None and not active_player.IS_HUMAN and time.time() - start_time > params.timeout:
                return Outcome(gb, red_won=not redsTurn, timeout=True)

            # Check if player won
            elif gb.has_won(active_player.color):
                return Outcome(gb, red_won=redsTurn)

            # Output
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

            # Switch players
            redsTurn = not redsTurn
            move += 1

        # Noone has won, it's a tie
        return Outcome(gb, red_won=False, tie=True)

    @classmethod
    def make_move(cls, player, gb):
        """Let a player make a move and check wether it's legal or not"""
        move = player.drop_disc(gb)
        if not gb.is_legal(move):
            return False, move
        else:
            gb.place_stone(move, player.color)
            return True, move


class Outcome:
    """Holds the outcome (result) of a game"""

    def __init__(self, gb, red_won=True, illegal=False, last_move=None, timeout=False, tie=False, error=None):
        self.gb = gb
        self.red_won = red_won
        self.illegal = illegal
        self.tie = tie
        self.timeout = timeout
        self.last_move = last_move
        self.error = error

    def __str__(self):
        """Verbose toString Method describing the outcome of the game"""
        if self.error is not None:
            if self.red_won:
                who = self.gb.YELLOW
            else:
                who = self.gb.RED
            return "{} had an Error: {}".format(self.gb.get_occupation_string(who), self.error)
        elif self.tie:
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
        """Get a single char describing the outcome.
        (Used for the tournament matrix)"""
        if self.tie:
            return "T"
        elif self.illegal or self.timeout:
            return "E"
        elif self.red_won:
            return "<"
        else:
            return "^"


class GameParameters:
    """Parameters for a connect 4 game"""

    def __init__(self, timeout=None, verbose=True):
        self.timeout = timeout
        self.verbose = verbose
