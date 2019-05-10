from itertools import product

from model.actions import Action
from model.policy import Policy
from model.state import State, StateActionPair

ALL_STATES = State.get_all_states()
ALL_STATE_ACTION_PAIRS = [StateActionPair(s, a)
                          for s, a in product(ALL_STATES, list(Action))]


class Algorithm:
    @classmethod
    def _create_sap_unif_mapping(cls, value):
        return {sap: value for sap in ALL_STATE_ACTION_PAIRS}

    @property
    def policy(self) -> Policy:
        raise NotImplemented

    def __init__(self):
        self._Q = Algorithm._create_sap_unif_mapping(0.)

    def train(self, rounds: int) -> None:
        raise NotImplemented


class MonteCarloAlgorithm(Algorithm):
    def __init__(self):
        super().__init__()
        self._visits = Algorithm._create_sap_unif_mapping(0)
        self._total_return = Algorithm._create_sap_unif_mapping(0)

    def _update_counters_with(self, game_info):
        reward = game_info.winner
        for (state, action) in game_info.player_logs:
            sap = StateActionPair(state, action)

            self._visits[sap] += 1
            self._total_return[sap] += reward
            self._Q[sap] = self._total_return[sap] / self._visits[sap]
