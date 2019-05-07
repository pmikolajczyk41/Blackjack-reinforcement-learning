from model.actions import Action
from model.state import State


class Policy:
    def make_decision_in(self, state: State) -> Action:
        raise NotImplemented
