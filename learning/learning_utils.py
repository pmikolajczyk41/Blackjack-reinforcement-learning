from itertools import product

from model.actions import Action
from model.policy import Policy
from model.state import State


class StateActionPair:
    def __init__(self, state: State, action: Action):
        self.state = state
        self.action = action

    def __eq__(self, other):
        if isinstance(other, StateActionPair):
            return self.state == other.state and self.action == other.action
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))


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
        self._visits = Algorithm._create_sap_unif_mapping(0)
        self._total_return = Algorithm._create_sap_unif_mapping(0)

    def train(self, rounds: int) -> None:
        raise NotImplemented
