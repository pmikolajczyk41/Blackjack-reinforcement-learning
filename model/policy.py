from typing import Callable

import numpy as np

from model.actions import Action
from model.state import State, StateActionPair


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

    @classmethod
    def epsilon_greedy_from_values(cls, values: dict, exploring_prob: Callable):
        mapping = dict()
        for s in State.get_all_states():
            if values[StateActionPair(s, Action.STICK)] > values[StateActionPair(s, Action.HIT)]:
                mapping[s] = [1. - exploring_prob(), exploring_prob()]
            else:
                mapping[s] = [exploring_prob(), 1. - exploring_prob()]
        return Policy.from_probabilistic_mapping(mapping)

    @classmethod
    def from_values(cls, values: dict):
        mapping = dict()
        for s in State.get_all_states():
            if s.current_sum < 12: mapping[s] = Action.HIT
            elif values[StateActionPair(s, Action.STICK)] > values[StateActionPair(s, Action.HIT)]:
                mapping[s] = Action.STICK
            else: mapping[s] = Action.HIT
        return Policy.from_deterministic_mapping(mapping)
