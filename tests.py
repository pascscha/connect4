#!/usr/bin/python3

import gameboard

print("Testing BasicGameBoard ", end="", flush=True)
gb = gameboard.BasicGameBoard()

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
