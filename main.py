#!/usr/bin/python3

if __name__ == "__main__":
    from arena import Arena, GameParameters
    from gameboard.implementations import *
    from player.implementations import *

    # Create Game Arena
    arena = Arena()

    # Game Parameters
    params = GameParameters(timeout=1)

    # Perform Game and store Outcome
    outcome = arena.play_game(SimplePlayerMinimax, HumanPlayer, BitBoard7x6, params)

    # Print Outcome
    print("\nGAME FINISHED - {}:\n{}".format(outcome, outcome.gb))
