from learning.learning_utils import Algorithm
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
        super().train(rounds)
