#!/usr/bin/python3

if __name__ == "__main__":
    from arena import Arena, GameParameters
    from gameboard import BasicGameBoard, BitBoard7x6
    from player import *

    # Create Game Arena
    arena = Arena()

    # Game Parameters
    params = GameParameters(timeout=1)

    # Perform Game and store Outcome
    outcome = arena.play_game(StrategyChangePlayer, HumanPlayer, BitBoard7x6, params)

    # Print Outcome
    print("\nGAME FINISHED - {}:\n{}".format(outcome, outcome.gb))
