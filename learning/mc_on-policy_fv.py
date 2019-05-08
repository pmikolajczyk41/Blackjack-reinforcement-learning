from learning.learning_utils import Algorithm
from model.policy import Policy


class MonteCarloOnPolicyFirstVisit(Algorithm):
    def __init__(self):
        super().__init__()
        self._pi = Algorithm._create_sap_unif_mapping(.5)

    @property
    def policy(self) -> Policy:
        return Policy.from_probabilistic_mapping(self._pi)

    def train(self, rounds: int) -> None:
        pass
