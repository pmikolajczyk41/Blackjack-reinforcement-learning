import numpy as np

from learning.learning_utils import *
from model.actions import Action
from model.cards import Card
from model.game import Game
from model.game_info import GameInfo
from model.policy import Policy
from model.state import State


class MonteCarloExploringStates(Algorithm):
    def __init__(self):
        super().__init__()
        self._pi = {state: Action.HIT if state.current_sum < 20 else Action.STICK
                    for state in ALL_STATES}

    @property
    def policy(self) -> Policy:
        return Policy.from_deterministic_mapping(self._pi)

    def train(self, rounds: int) -> None:
        for i in range(rounds):
            initial_state = self._choose_initial_state()
            # safe, because of acyclic Markov Process
            self._pi[initial_state] = np.random.choice(list(Action))

            game = Game(player_policy=self.policy)
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
