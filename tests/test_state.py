from unittest import TestCase

from model.cards import Card
from model.state import State, BUST

blank = Card.TWO


class TestState(TestCase):
    def check_sum_of_deal(self, expected_sum: int, first_card: Card, second_card: Card):
        state = State.from_deal(first_card, second_card, blank)
        self.assertEqual(expected_sum, state.current_sum)

    def test_from_deal(self):
        self.check_sum_of_deal(5, Card.TWO, Card.THREE)
        self.check_sum_of_deal(12, Card.ACE, Card.ACE)
        self.check_sum_of_deal(19, Card.EIGHT, Card.ACE)
        self.check_sum_of_deal(21, Card.ACE, Card.FACE_CARD)
        self.check_sum_of_deal(20, Card.FACE_CARD, Card.FACE_CARD)

    def check_sum(self, expected_sum: int, state: State):
        self.assertEqual(expected_sum, state.current_sum)

    def check_used_ace(self, state: State):
        self.assertFalse(state.holds_usable_ace)

    def test_moving_no_bust(self):
        state = State(17, blank, False)
        self.check_sum(20, state.move_with(Card.THREE))

    def test_moving_bust(self):
        state = State(17, blank, False)
        self.assertEqual(BUST, state.move_with(Card.FACE_CARD))

    def test_moving_with_ace_no_bust(self):
        state = State(4, blank, True)
        self.check_sum(15, state.move_with(Card.ACE))

    def test_moving_with_ace_bust(self):
        state = State(21, blank, False)
        self.assertEqual(BUST, state.move_with(Card.ACE))

    def test_moving_use_ace(self):
        state = State(17, blank, True)
        self.check_sum(17, state.move_with(Card.FACE_CARD))
        self.check_used_ace(state.move_with(Card.FACE_CARD))

    def test_blackjack_no_usable(self):
        state = State(21, blank, False)
        self.assertEqual(BUST, state.move_with(Card.TWO))

    def test_blackjack_use(self):
        state = State(21, blank, True)
        self.check_sum(13, state.move_with(Card.TWO))
        self.check_used_ace(state.move_with(Card.TWO))

    def test_blackjack_and_ace(self):
        state = State(21, blank, True)
        self.check_sum(12, state.move_with(Card.ACE))
        self.check_used_ace(state.move_with(Card.ACE))
