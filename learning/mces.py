from itertools import product

import numpy as np

from model.actions import Action
from model.cards import Card
from model.game import Game
from model.game_info import GameInfo
from model.policy import Policy
from model.state import State
from plotting import DeterministicPolicyPlotter


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


class MonteCarloExploringStates:
    def __init__(self):
        states = State.get_all_demanding_states()
        saps = list(product(states, list(Action)))

        self._pi = {state: np.random.choice(list(Action))
                    for state in states}
        self._Q = {StateActionPair(state, action): 0.
                   for state, action in saps}
        self._visits = {StateActionPair(state, action): 0
                        for state, action in saps}
        self._total_return = {StateActionPair(state, action): 0
                              for state, action in saps}

    @property
    def policy(self):
        return Policy.from_mapping(self._pi)

    def train(self, rounds=100000):
        for i in range(rounds):
            initial_state = self._choose_initial_state()
            game = Game(player_policy=Policy.from_mapping(self._pi))
            game_info = game.play_starting_in(initial_state)
            self._update_with(game_info)

    @staticmethod
    def _choose_initial_state():
        return State(current_sum=np.random.randint(12, 22),
                     opponent_points=np.random.choice(list(Card)),
                     holds_usable_ace=bool(np.random.randint(0, 2)))

    def _update_with(self, game_info: GameInfo) -> None:
        reward = game_info.winner
        for (state, action) in game_info.player_logs:
            sap = StateActionPair(state, action)

            self._visits[sap] += 1
            self._total_return[sap] += reward
            self._Q[sap] = self._total_return[sap] / self._visits[sap]

        for (state, _) in game_info.player_logs:
            stick_action_value = self._Q[StateActionPair(state, Action.STICK)]
            hit_action_value = self._Q[StateActionPair(state, Action.HIT)]
            if stick_action_value > hit_action_value:
                self._pi[state] = Action.STICK
            else:
                self._pi[state] = Action.HIT


if __name__ == '__main__':
    MCES = MonteCarloExploringStates()
    MCES.train(10000)
    DeterministicPolicyPlotter().plot(MCES.policy)
