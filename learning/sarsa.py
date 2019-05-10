from learning.learning_utils import Algorithm, StateActionPair, ALL_STATES
from model.actions import Action
from model.game import Game
from model.policy import Policy
from plotting.plotting import ProbabilisticPolicyPlotter


class Sarsa(Algorithm):
    default_epsilon = 0.1

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9):
        super().__init__()
        self._alpha = alpha
        self._gamma = gamma
        self._pi = {state: [0., 1.] if state.current_sum < 12 else [.5, .5]
                    for state in ALL_STATES}

    @property
    def policy(self) -> Policy:
        return Policy.from_probabilistic_mapping(self._pi)

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

        self._update_policy_on_states([s for (s, _) in game_info.player_logs])

    def _update_policy_on_states(self, states, denominator: int = 0):
        if denominator: exploring_prob = 1. / denominator
        else: exploring_prob = self.default_epsilon

        for s in states:
            stick_sap = StateActionPair(s, Action.STICK)
            hit_sap = StateActionPair(s, Action.HIT)
            if self._Q[stick_sap] > self._Q[hit_sap]:
                self._pi[s] = [1. - exploring_prob, exploring_prob]
            else:
                self._pi[s] = [exploring_prob, 1. - exploring_prob]


if __name__ == '__main__':
    sarsa = Sarsa()
    sarsa.train(100000)
    ProbabilisticPolicyPlotter().plot(sarsa.policy)
