from enum import Enum


class Winner(Enum):
    PLAYER = 0
    DEALER = 1
    DRAW = 2


class GameInfo:
    def __init__(self):
        self.winner = None
        self._player_logs = []
        self._dealer_logs = []

    @property
    def player_logs(self):
        return self._player_logs

    @property
    def dealer_logs(self):
        return self._dealer_logs

    def log_player(self, state):
        self._player_logs.append(state)

    def log_dealer(self, state):
        self._dealer_logs.append(state)

    def set_winner(self, winner: Winner):
        self.winner = winner
