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

            if params.verbose:
                print("\nMove #{} - {}:\n{}".format(move, active_player.get_name(), gb))

            start_time = time.time()

            if not cls.make_move(active_player, gb):
                return Outcome(red_won=not redsTurn, illegal=True)

            elif params.timeout is not None and time.time() - start_time > params.timeout:
                return Outcome(red_won=not redsTurn, timeout=True)

            elif gb.has_won(active_player.color):
                return Outcome(red_won=redsTurn)

            redsTurn = not redsTurn
            move += 1
        return Outcome(red_won=False, tie=True)

    @classmethod
    def make_move(cls, player, gb):
        move = player.next_move(gb)
        if not gb.is_legal(move):
            print("{} made an illegal move.".format(player))
            return False
        else:
            gb.place_stone(move, player.color)
            return True


class Outcome:
    def __init__(self, red_won=True, illegal=False, timeout=False, tie=False):
        self.red_won = red_won
        self.illegal = illegal
        self.tie = tie
        self.timeout = timeout


class GameParameters:
    def __init__(self, timeout=None, verbose=True):
        self.timeout = timeout
        self.verbose = verbose
