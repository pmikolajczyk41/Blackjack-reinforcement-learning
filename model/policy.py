import numpy as np

from model.actions import Action
from model.state import State


class Policy:
    def make_decision_in(self, state: State) -> Action:
        raise NotImplemented

    @classmethod
    def from_deterministic_mapping(cls, mapping: dict):
        policy = Policy()
        setattr(policy, 'make_decision_in',
                lambda state: mapping[state])
        return policy

    @classmethod
    def from_probabilistic_mapping(cls, mapping: dict):
        policy = Policy()
        setattr(policy, 'make_decision_in',
                lambda state: np.random.choice(list(Action), p=mapping[state]))
        return policy
