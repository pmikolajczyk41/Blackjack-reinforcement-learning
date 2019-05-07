from model.actions import Action
from model.policy import Policy
from model.state import State


class DeterministicPolicy(Policy):
    def make_decision_in(self, state: State) -> Action:
        if state.current_sum <= 11:
            return Action.HIT
        elif state.current_sum >= 21:
            return Action.STICK

        elif state.holds_usable_ace:
            if state.current_sum <= 17:
                return Action.HIT
            if state.current_sum == 18 and state.opponent_points >= 9:
                return Action.HIT
            return Action.STICK

        else:
            if state.current_sum <= 16 and state.opponent_points >= 7:
                return Action.HIT
            if state.current_sum <= 12 and state.opponent_points <= 3:
                return Action.HIT
            if state.current_sum == 11 and state.opponent_points in [4, 5, 6]:
                return Action.HIT
            return Action.STICK
