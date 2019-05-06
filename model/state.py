from model.cards import Card


class State:
    def __init__(self,
                 current_sum: int,
                 dealers_card: Card,
                 holds_usable_ace: bool):
        self.current_sum = current_sum
        self.dealers_card = dealers_card
        self.holds_usable_ace = holds_usable_ace

    @classmethod
    def from_deal(cls, first_card: Card, second_card: Card, dealers_card: Card):
        current_sum = first_card + second_card
        if current_sum == 22:
            current_sum = 12

        return State(current_sum=current_sum,
                     dealers_card=dealers_card,
                     holds_usable_ace=(first_card == Card.ACE or second_card == Card.ACE))

    def __eq__(self, other):
        if isinstance(other, State):
            return self.current_sum == other.current_sum and \
                   self.dealers_card == other.dealers_card and \
                   self.holds_usable_ace == other.holds_usable_ace
        return False

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def move_with(self, card: Card):
        if card != Card.ACE:
            new_sum = self.current_sum + card
            if new_sum > 21 and self.holds_usable_ace:
                return State(new_sum - 10, self.dealers_card, False)
            elif new_sum > 21:
                return BUST
            return State(new_sum, self.dealers_card, self.holds_usable_ace)
        elif self.current_sum < 11:
            return State(self.current_sum + 11, self.dealers_card, True)
        elif self.current_sum >= 21 and not self.holds_usable_ace:
            return BUST
        elif self.current_sum >= 21 and self.holds_usable_ace:
            return State(self.current_sum - 9, self.dealers_card, False)
        else:
            return State(self.current_sum + 1, self.dealers_card, self.holds_usable_ace)

    def should_hit(self):
        return self != BUST and self.current_sum <= 11


BUST = State(None, None, None)
