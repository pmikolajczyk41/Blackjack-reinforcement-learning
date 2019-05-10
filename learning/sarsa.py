from learning.learning_utils import Algorithm, StateActionPair
from model.game import Game
from model.policy import Policy


class Sarsa(Algorithm):
    default_epsilon = 0.1

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9):
        super().__init__()
        self._alpha = alpha
        self._gamma = gamma

    @property
    def policy(self, denominator: int = 0) -> Policy:
        if denominator == 0:
            return Policy.epsilon_greedy_from_values(self._Q, lambda: self.default_epsilon)
        else:
            return Policy.epsilon_greedy_from_values(self._Q, lambda: 1. / denominator)

    def train(self, rounds: int) -> None:
        for i in range(rounds):
            game_info = Game(player_policy=self.policy).play()
            # can do offline due to the acyclic game
            self._update_with(game_info)

    def _update_with(self, game_info):
        for (log, next_log) in zip(game_info.player_logs[:-1], game_info.player_logs[1:]):
            sap = StateActionPair(*log)
            next_sap = StateActionPair(*next_log)
            self._Q[sap] += self._alpha * (self._gamma * self._Q[next_sap] - self._Q[sap])

        last_sap = StateActionPair(*(game_info.player_logs[-1]))
        self._Q[last_sap] += self._alpha * (game_info.winner - self._Q[last_sap])
