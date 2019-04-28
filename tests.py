#!/usr/bin/python3
from gameboard.implementations import *
from player.implementations import *
from arena import GameParameters, Arena
import cProfile
import random
import operator
import sys
import inspect


def available_moves(gb, player):
    """Returns all legal moves for a game board"""
    out = []
    for row in range(gb.ROWS):
        if gb.is_legal(row):
            out.append(row)
    return out


def test_gameboard(GB, n):
    """Plays n random Games on a GameBoard class"""
    for i in range(n):
        gb = GB()
        player = gb.RED
        while not gb.is_finished():
            moves = available_moves(gb, player)
            gb.place_stone(random.choice(moves), player)
            player = gb.other_player(player)


def test_gameboards(gameboards):
    """Does some Functionality tests on a GameBoard"""
    for GB in gameboards:
        print("Testing {} ".format(GB.__name__), end="", flush=True)
        gb = GB()

        for r in range(gb.ROWS):
            for c in range(gb.COLS):
                assert(gb.get_occupation(r, c) == gb.EMPTY)

        assert(gb.place_stone(1, gb.RED))
        assert(gb.place_stone(1, gb.YELLOW))
        assert(gb.place_stone(1, gb.RED))
        assert(gb.place_stone(2, gb.YELLOW))
        assert(gb.place_stone(1, gb.RED))
        assert(gb.place_stone(2, gb.YELLOW))
        assert(gb.place_stone(1, gb.RED))
        assert(gb.place_stone(2, gb.YELLOW))
        assert(gb.place_stone(1, gb.RED))

        assert(gb.has_won(gb.RED))

        print("- Done!")

    print("All GameBoards seem to work correctly.")


def benchmark_gameboards(gameboards):
    """Benchmarks a GameBoard"""
    for GB in gameboards:
        print("Benchmark for {}:".format(GB.__name__))
        cProfile.run('test_gameboard({},1000)'.format(GB.__name__))

    gameboards = [BasicGameBoard, BitBoard7x6]


def test_player(Player):
    """Lets a player play a game against himself (used for benchmarking)"""
    params = GameParameters(timeout=1)
    gb = BitBoard7x6()
    p = Player(gb.RED, params)
    while not gb.is_finished():
        move = p.next_move(gb)
        gb.place_stone(move, p.color)
        p.color = gb.other_player(p.color)


def benchmark_players(players):
    """Benchmarks Player classes
    (time will be the same for all of them, but we can still see which functions they spend the most time on)"""
    print("Benchmarking players")

    for Player in players:
        print("Summary for {}:".format(Player.__name__))
        cProfile.run('test_player({})'.format(Player.__name__))


def tournament_players(players):
    """Lets every player play against every other player in order to determine their strength"""
    timeout = float(input("How much time per move? "))
    params = GameParameters(timeout=timeout, verbose=False)
    arena = Arena()

    scores = {}
    print("\nParticipating players:")
    for i in range(len(players)):
        print("{}: {}".format(i, players[i].__name__))
        scores[i] = 0

    print("\n ", end=" ")
    for i in range(len(players)):
        print(i, end=" ")
    print()

    errors = []
    for i in range(len(players)):
        print(i, end=" ", flush=True)
        for j in range(len(players)):
            if i != j:
                outcome = arena.play_game(players[i], players[j], BitBoard7x6, params)
                print(outcome.get_char(), end=" ", flush=True)

                if outcome.error is not None or outcome.timeout or outcome.illegal:
                    errors.append((players[i], players[j], outcome))

                if outcome.red_won:
                    scores[i] += 3
                elif outcome.tie:
                    scores[j] += 1
                    scores[i] += 1
                else:
                    scores[j] += 3
            else:
                print("X", end=" ", flush=True)
        print()

    if len(errors) > 0:
        print("\nErrors:")
        for error in errors:
            player1 = error[0].__name__
            player2 = error[1].__name__
            message = str(error[2])
            gameboard = error[2].gb
            print("{} (X) vs {} (O): {}\n{}\n".format(player1, player2, message, gameboard))

    print("\nScoreboard:")
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    for i in range(len(sorted_scores)):
        player_name = players[sorted_scores[i][0]].__name__
        score = sorted_scores[i][1]
        print("{}: {:>3}P {}".format(i, score, player_name))


def get_classes_from_module(module, blacklist=None, whitelist=None):
    out = []
    for name, obj in inspect.getmembers(sys.modules[module], inspect.isclass):
        if obj.__module__ == module:
            if blacklist is None or obj.__name__ not in blacklist:
                if whitelist is None or obj.__name__ in whitelist:
                    out.append(obj)
    return out


if __name__ == "__main__":

    # Gameboards (Class name as string) that we don't want to test
    gameboard_blacklist = ["BasicGameBoard"]
    gameboards = get_classes_from_module("gameboard.implementations", blacklist=gameboard_blacklist)

    # Players (Class name as string) that we don't want to test
    player_blacklist = [
        "SimplePlayerAlphaBeta",
        "SimplePlayerAlphaBetaHash",
        "SimplePlayerMinimax",
        "Count3PlayerHash0",
        "Count3PlayerHash1",
        "Count3PlayerHash2",
        "Count3PlayerHash3",
        "Count3PlayerHash4",
    ]

    # Players (Class name as string) that we want to test
    player_whitelist = [
        "Count3Player",
        "Count3PlayerMinimax",
        "Count3PlayerRandom",
        "SimpleBookPlayer",
        "Count3BookPlayer",
        #"Count3PlayerHash0",
        #"Count3PlayerHash1",
        #"Count3PlayerHash2",
        #"Count3PlayerHash3",
        #"Count3PlayerHash4",
    ]

    players = get_classes_from_module("player.implementations", whitelist=player_whitelist)

    # All available Tests
    tests = {test_gameboards: gameboards,
             benchmark_gameboards: gameboards,
             benchmark_players: players,
             tournament_players: players}

    print("Available tests:")
    for i in range(len(tests.items())):
        function = list(tests)[i]
        print("\t{}: {}".format(i, function.__name__))

    choice = int(input("\nPlease choose what test you want to perform: "))
    print()

    # Perfrom Test
    function = list(tests)[choice]
    param = list(tests.values())[choice]
    function(param)
