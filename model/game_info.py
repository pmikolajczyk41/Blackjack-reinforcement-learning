from enum import IntEnum
from typing import List, Tuple

from model.actions import Action
from model.state import State


class Winner(IntEnum):
    PLAYER = 1
    DEALER = -1
    DRAW = 0


class GameInfo:
    def __init__(self):
        self._winner = None
        self._player_logs = []
        self._dealer_logs = []

    @property
    def player_logs(self) -> List[Tuple[State, Action]]:
        return self._player_logs

    @property
    def dealer_logs(self) -> List[Tuple[State, Action]]:
        return self._dealer_logs

    @property
    def winner(self) -> Winner:
        return self._winner

    def log_player(self, state: State, action: Action) -> None:
        self._player_logs.append((state, action))

    def log_dealer(self, state: State, action: Action) -> None:
        self._dealer_logs.append((state, action))

    def set_winner(self, winner: Winner) -> None:
        self._winner = winner
