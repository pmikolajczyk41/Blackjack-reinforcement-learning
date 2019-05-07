from enum import Enum
from typing import List


class Winner(Enum):
    PLAYER = 0
    DEALER = 1
    DRAW = 2


class GameInfo:
    def __init__(self):
        self._winner = None
        self._player_logs = []
        self._dealer_logs = []

    @property
    def player_logs(self) -> List:
        return self._player_logs

    @property
    def dealer_logs(self) -> List:
        return self._dealer_logs

    @property
    def winner(self) -> Winner:
        return self._winner

    def log_player(self, state) -> None:
        self._player_logs.append(state)

    def log_dealer(self, state) -> None:
        self._dealer_logs.append(state)

    def set_winner(self, winner: Winner) -> None:
        self._winner = winner
