from model.actions import Action
from model.policy import Policy
from model.state import State


class DealerPolicy(Policy):
    def make_decision_in(self, state: State) -> Action:
        if state.current_sum < 17:
            return Action.HIT
        else:
            return Action.STICK
