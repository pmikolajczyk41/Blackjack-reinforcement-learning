from itertools import product
from typing import Union

from model.cards import Card


class State:
    def __init__(self,
                 current_sum: int,
                 opponent_points: int,
                 holds_usable_ace: bool):
        self.current_sum = current_sum
        self.opponent_points = opponent_points
        self.holds_usable_ace = holds_usable_ace

    @classmethod
    def from_deal(cls, first_card: Card, second_card: Card, opponent_hand: Union[Card, int]):
        current_sum = first_card + second_card
        if current_sum == 22:
            current_sum = 12

        return State(current_sum=current_sum,
                     opponent_points=opponent_hand,
                     holds_usable_ace=(first_card == Card.ACE or second_card == Card.ACE))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.current_sum == other.current_sum and \
                   self.opponent_points == other.opponent_points and \
                   self.holds_usable_ace == other.holds_usable_ace
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def move_with(self, card: Card):
        if card != Card.ACE:
            new_sum = self.current_sum + card
            if new_sum > 21 and self.holds_usable_ace:
                return State(new_sum - 10, self.opponent_points, False)
            elif new_sum > 21:
                return BUST
            return State(new_sum, self.opponent_points, self.holds_usable_ace)
        elif self.current_sum < 11:
            return State(self.current_sum + 11, self.opponent_points, True)
        elif self.current_sum >= 21 and not self.holds_usable_ace:
            return BUST
        elif self.current_sum >= 21 and self.holds_usable_ace:
            return State(self.current_sum - 9, self.opponent_points, False)
        else:
            return State(self.current_sum + 1, self.opponent_points, self.holds_usable_ace)

    @classmethod
    def get_all_demanding_states(cls):
        return [State(current_sum=current_sum,
                      opponent_points=opponent_points,
                      holds_usable_ace=holds_usable_ace)
                for current_sum, opponent_points, holds_usable_ace
                in product(range(12, 22), Card.get_values(), [True, False])]

    @classmethod
    def get_all_states(cls):
        return [State(current_sum=current_sum,
                      opponent_points=opponent_points,
                      holds_usable_ace=holds_usable_ace)
                for current_sum, opponent_points, holds_usable_ace
                in product(range(2, 22), Card.get_values(), [True, False])]

BUST = State(None, None, None)
