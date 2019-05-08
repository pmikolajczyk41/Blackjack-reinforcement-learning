from learning.learning_utils import *
from model.actions import Action
from model.game import Game
from model.policy import Policy


class MonteCarloOnPolicyFirstVisit(Algorithm):
    def __init__(self, epsilon: float = 0.1):
        super().__init__()
        self._eps = epsilon
        self._pi = {state: [0., 1.] if state.current_sum < 12 else [.5, .5]
                    for state in ALL_STATES}

    @property
    def policy(self) -> Policy:
        return Policy.from_probabilistic_mapping(self._pi)

    def train(self, rounds: int) -> None:
        for i in range(rounds):
            game_info = Game(player_policy=self.policy).play()
            self._update_with(game_info)

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
                self._pi[state] = [1. - self._eps / 2, self._eps / 2]
            else:
                self._pi[state] = [self._eps / 2, 1. - self._eps / 2]
