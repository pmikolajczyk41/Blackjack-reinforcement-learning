from collections import namedtuple

from model.game import Game
from model.game_info import Winner
from model.policy import Policy
from policies.dealer import DealerPolicy
from policies.deterministic import DeterministicPolicy

GameStats = namedtuple('GameStats', ['wins', 'draws', 'losses'])

GAME_RUNS = 10000
ALPHAS = [0.001, 0.01, 0.1, 0.2, 0.5]
GAMMAS = [0.5, 0.7, 0.9, 0.99]


def check_stats_of_policy(player_policy: Policy, dealer_policy: Policy = DealerPolicy()) -> GameStats:
    wins, losses = 0, 0
    game = Game(player_policy, dealer_policy)

    for run in range(GAME_RUNS):
        winner = game.play().winner
        if winner == Winner.PLAYER: wins += 1
        elif winner == Winner.DEALER: losses += 1

    return GameStats(wins=wins / GAME_RUNS,
                     losses=losses / GAME_RUNS,
                     draws=(GAME_RUNS - wins - losses) / GAME_RUNS)


if __name__ == '__main__':
    print(check_stats_of_policy(DeterministicPolicy()))
