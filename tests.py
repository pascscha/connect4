#!/usr/bin/python3
from gameboard import *
from player import *
from arena import GameParameters, Arena
import cProfile
import random


def available_moves(gb, player):
    out = []
    for row in range(gb.ROWS):
        if gb.is_legal(row):
            out.append(row)
    return out


def test_gameboard(GB, n):
    for i in range(n):
        gb = GB()
        player = gb.RED
        while not gb.is_finished():
            moves = available_moves(gb, player)
            gb.place_stone(random.choice(moves), player)
            player = gb.other_player(player)


def test_gameboards(gameboards):
    print("FUNCTIONALITY:")

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
    for GB in gameboards:
        print("Benchmark for {}:".format(GB.__name__))
        cProfile.run('test_gameboard({},1000)'.format(GB.__name__))

    gameboards = [BasicGameBoard, BitBoard7x6]


def test_player(Player):
    params = GameParameters(timeout=1)
    gb = BitBoard7x6()
    p = Player(gb.RED, params)
    for i in range(10):
        move = p.next_move(gb)
        gb.place_stone(move, p.color)
        p.color = gb.other_player(p.color)


def benchmark_players(players):
    print("Benchmarking players")

    for Player in players:
        print("Summary for {}:".format(Player.__name__))
        cProfile.run('test_player({})'.format(Player.__name__))


def tournament_players(players):
    timeout = float(input("How much time per move? "))
    params = GameParameters(timeout=timeout, verbose=False)
    arena = Arena()

    print("\nParticipating players:")
    for i in range(len(players)):
        print("{}: {}".format(i, players[i].__name__))

    print("\n ", end=" ")
    for i in range(len(players)):
        print(i, end=" ")
    print()

    for i in range(len(players)):
        print(i, end=" ", flush=True)
        for j in range(len(players)):
            if i != j:
                outcome = arena.play_game(players[i], players[j], BitBoard7x6, params)
                print(outcome.get_char(), end=" ")
            else:
                print("X", end=" ")
        print()


if __name__ == "__main__":
    gameboards = [BasicGameBoard, BitBoard7x6]
    players = [SimplePlayer, SimplePlayer2, StrategyChanger]

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

    function = list(tests)[choice]
    param = list(tests.values())[choice]
    function(param)
