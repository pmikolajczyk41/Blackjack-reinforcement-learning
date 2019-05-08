import numpy as np

from learning.learning_utils import *
from model.actions import Action
from model.cards import Card
from model.game import Game
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

    def _update_with(self, game_info):
        self._update_counters_with(game_info)
        self._update_policy_with(game_info)

    def _update_policy_with(self, game_info):
        for (state, _) in game_info.player_logs:
            stick_sap = StateActionPair(state, Action.STICK)
            hit_sap = StateActionPair(state, Action.HIT)

            stick_action_value = self._Q[stick_sap]
            hit_action_value = self._Q[hit_sap]
            if stick_action_value > hit_action_value:
                self._pi[state] = Action.STICK
            else:
                self._pi[state] = Action.HIT
