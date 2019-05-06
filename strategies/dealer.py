from model.actions import Action
from model.state import State
from model.strategy import Strategy


class DealerStrategy(Strategy):
    def make_decision_in(self, state: State) -> Action:
        if state.current_sum <= 17:
            return Action.HIT
        else:
            return Action.STICK
