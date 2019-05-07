import random
from typing import Callable

from model.actions import Action
from model.cards import Card
from model.game_info import GameInfo, Winner
from model.policy import Policy
from model.state import State, BUST
from policies.dealer import DealerPolicy


class Deck:
    def __init__(self):
        self._deck = list(Card)

    def get_next_card(self) -> Card:
        return random.choice(self._deck)


class Game:
    def __init__(self, player_policy: Policy,
                 dealer_policy: Policy = DealerPolicy(),
                 deck: Deck = Deck()):
        self._player_policy = player_policy
        self._dealer_policy = dealer_policy
        self._deck = deck

    def _play_stage(self, initial_state: State, policy: Policy, log_action: Callable) -> State:
        taken_action = None
        state = initial_state
        log_action(state)

        while taken_action != Action.STICK and state != BUST:
            taken_action = policy.make_decision_in(state)
            if taken_action == Action.HIT:
                state = state.move_with(self._deck.get_next_card())
                log_action(state)
        return state

    def play(self) -> GameInfo:
        game_info = GameInfo()

        player_cards = (self._deck.get_next_card(), self._deck.get_next_card())
        dealer_cards = (self._deck.get_next_card(), self._deck.get_next_card())

        player_state = self._play_stage(initial_state=State.from_deal(*player_cards, dealer_cards[0]),
                                        policy=self._player_policy,
                                        log_action=game_info.log_player)

        if player_state == BUST:
            game_info.set_winner(Winner.DEALER)
            return game_info

        dealer_state = self._play_stage(initial_state=State.from_deal(*dealer_cards, player_state.current_sum),
                                        policy=self._dealer_policy,
                                        log_action=game_info.log_dealer)

        if dealer_state == BUST:
            game_info.set_winner(Winner.PLAYER)
            return game_info

        if player_state.current_sum > dealer_state.current_sum:
            game_info.set_winner(Winner.PLAYER)
        elif player_state.current_sum == dealer_state.current_sum:
            game_info.set_winner(Winner.DRAW)
        else:
            game_info.set_winner(Winner.DEALER)

        return game_info
