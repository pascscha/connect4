#!/usr/bin/python3

from gameboard import *
import cProfile
import random

gameboards = [BasicGameBoard, BitBoard7x6]

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


print("\nBENCHMARKS:")


def available_moves(gb, player):
    out = []
    for row in range(gb.ROWS):
        if gb.is_legal(row):
            out.append(row)
    return out


def test_gameboard(GB):
    for i in range(1000):
        gb = GB()
        player = gb.RED
        while not gb.is_finished():
            moves = available_moves(gb, player)
            gb.place_stone(random.choice(moves), player)
            player = gb.other_player(player)


for GB in gameboards:
    print("Summary for {}:".format(GB.__name__))
    cProfile.run('test_gameboard({})'.format(GB.__name__))
