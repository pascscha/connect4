#!/usr/bin/python3


def get_classes_from_module(module):
    out = []
    for name, obj in inspect.getmembers(sys.modules[module], inspect.isclass):
        if obj.__module__ == module:
            out.append(obj)
    return out


if __name__ == "__main__":
    from arena import Arena, GameParameters
    from gameboard.implementations import BitBoard7x6
    from player.implementations import *
    import sys
    import inspect

    available_players = [HumanPlayer] + get_classes_from_module("player.implementations")

    for i in range(len(available_players)):
        print("{}: {}".format(i, available_players[i].__name__))

    first_index = int(input("Please choose your first Player (X): "))
    first_player = available_players[first_index]

    second_index = int(input("Please choose your second Player (O): "))
    second_player = available_players[second_index]

    timeout = float(input("Please enter the timelimit (only for non-human players), 0 for no timeout: "))
    if timeout <= 0:
        timeout = None
    # Game Parameters
    params = GameParameters(timeout=timeout)

    # Create Game Arena
    arena = Arena()

    # Perform Game and store Outcome
    outcome = arena.play_game(first_player, second_player, BitBoard7x6, params)

    # Print Outcome
    print("\nGAME FINISHED - {}:\n{}".format(outcome, outcome.gb))
