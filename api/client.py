import requests
import json
from urllib.parse import urljoin


class ConnectFourClient:
    ENDPOINT_JOIN = '/api/v1/players/join'
    ENDPOINT_GAMES = '/api/v1/players/games/%s'

    def __init__(self, url):
        self._url = url

    def join(self, player_id):
        headers = {'content-type': 'application/json'}
        payload = {'playerId': player_id}
        r = requests.post(urljoin(self._url, self.ENDPOINT_JOIN), data=json.dumps(payload), headers=headers)
        return r.json()

    def game_state(self, game_id):
        r = requests.get(urljoin(self._url, (self.ENDPOINT_GAMES % game_id)))
        return r.json()

    def drop_disc(self, game_id, player_id, column):
        headers = {'content-type': 'application/json'}
        payload = {'playerId': player_id,
                   'column': column}
        r = requests.post(urljoin(self._url, (self.ENDPOINT_GAMES % game_id)), data=json.dumps(payload),
                          headers=headers)
        return r.json()
