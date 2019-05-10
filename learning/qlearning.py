from learning.learning_utils import Algorithm, StateActionPair, ALL_STATES
from model.actions import Action
from model.game import Game
from model.policy import Policy


class QLearning(Algorithm):
    def __init__(self, alpha: float = 0.1, gamma: float = 0.9):
        super().__init__()
        self._alpha = alpha
        self._gamma = gamma
        behavioral_mapping = {state: [0., 1.] if state.current_sum < 12 else [.5, .5]
                              for state in ALL_STATES}
        self._beh_policy = Policy.from_probabilistic_mapping(behavioral_mapping)

    @property
    def policy(self) -> Policy:
        return Policy.from_values(self._Q)

    def train(self, rounds: int) -> None:
        for i in range(rounds):
            game_info = Game(player_policy=self._beh_policy).play()
            # can do offline due to the acyclic game
            self._update_with(game_info)

    def _update_with(self, game_info):
        for (log, next_log) in zip(game_info.player_logs[:-1], game_info.player_logs[1:]):
            sap = StateActionPair(*log)

            next_state = next_log[0]
            next_stick_sap = StateActionPair(next_state, Action.STICK)
            next_hit_sap = StateActionPair(next_state, Action.HIT)
            best_next_value = max(self._Q[next_stick_sap], self._Q[next_hit_sap])

            self._Q[sap] += self._alpha * (self._gamma * best_next_value - self._Q[sap])

        last_sap = StateActionPair(*(game_info.player_logs[-1]))
        self._Q[last_sap] += self._alpha * (game_info.winner - self._Q[last_sap])
