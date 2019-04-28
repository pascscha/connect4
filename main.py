#!/usr/bin/python3

if __name__ == "__main__":
    from arena import Arena, GameParameters
    from gameboard import BasicGameBoard, BitBoard7x6
    from player import *

    arena = Arena()

    params = GameParameters(timeout=100)

    outcome = arena.play_game(SimplePlayer2, HumanPlayer, BitBoard7x6, params)

    print("\nGAME FINISHED - {}:\n{}".format(outcome, outcome.gb))
