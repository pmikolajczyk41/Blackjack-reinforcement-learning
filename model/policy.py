import numpy as np

from model.actions import Action
from model.state import State


class Policy:
    def make_decision_in(self, state: State) -> Action:
        raise NotImplemented

    def stick_certainty_in(self, state: State) -> float:
        raise NotImplemented

    def hit_certainty_in(self, state: State) -> float:
        return 1. - self.stick_certainty_in(state)

    @classmethod
    def from_deterministic_mapping(cls, mapping: dict):
        policy = Policy()
        setattr(policy, 'make_decision_in',
                lambda state: mapping[state])
        setattr(policy, 'stick_certainty_in',
                lambda state: 0. if mapping[state] == Action.HIT else 1.)
        return policy

    @classmethod
    def from_probabilistic_mapping(cls, mapping: dict):
        policy = Policy()
        setattr(policy, 'make_decision_in',
                lambda state: np.random.choice(list(Action), p=mapping[state]))
        setattr(policy, 'stick_certainty_in',
                lambda state: mapping[state][Action.STICK.value])
        return policy
