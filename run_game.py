#!/usr/bin/python3

import time
import logging
from concurrent.futures import ThreadPoolExecutor

from api import GameRunner, ConnectFourClient, RandomPlayerStrategy

from player.implementations import *
from arena import GameParameters

NUMBER_OF_GAMES = 1_000
SERVER_URL = "http://localhost:8080"


def main():
    logging.getLogger().setLevel(logging.INFO)
    executor = ThreadPoolExecutor(max_workers=2)

    client = ConnectFourClient(SERVER_URL)

    params = GameParameters()
    simple = SimplePlayerAlphaBeta(1, params)
    superduper = Count3BookPlayer(1, params)

    future1 = executor.submit(
        GameRunner(client=client, player_id='Alice', strategy=simple, number_of_games=NUMBER_OF_GAMES).run)
    future2 = executor.submit(
        GameRunner(client=client, player_id='Bob', strategy=superduper, number_of_games=NUMBER_OF_GAMES).run)

    while not future1.done() and not future2.done():
        time.sleep(1)

    logging.info('Done!')


if __name__ == '__main__':
    main()
