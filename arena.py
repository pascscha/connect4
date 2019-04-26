import time


class Arena:

    @classmethod
    def play_game(cls, playerClsRed, playerClsYellow, gameBoardCls, params):
        playerRed = playerCls1(params)
        playerYellow = playerCls2(params)
        gb = gameBoardCls()

        redsTurn = False
        move = 1
        while not gb.is_finished():
            if redsTurn:
                active_player = playerRed
            else:
                active_player = playerYellow

            start_time = time.time()
            if not cls.make_move(active_player, gb):
                return Outcome(red_won=not redsTurn, illegal=True)
            if time.time() - start_time > params.timeout:
                return Outcome(red_won=not redsTurn, timeout=True)
            if gb.has_won(active_player.color):
                return Outcome(red_won=redsTurn)
            if params.verbose:
                print("Move #{} - {}:\n{}".format(move, active_player.name, gb))
            redsTurn != redsTurn
        return Outcome(red_won=False, tie=True)

    @classmethod
    def make_move(cls, player, gb):
        move = player.next_move(gb)
        if not gb.is_legal(move):
            print("{} made an illegal move.".format(player))
            return False
        else:
            gb.make_move(move)
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
