#!/usr/bin/python3

from gameboard import *

gameboards = [BasicGameBoard, BitBoard7x6]

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
