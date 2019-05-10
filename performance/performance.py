from collections import namedtuple
from itertools import product

from learning.mc_es import MonteCarloExploringStates
from learning.mc_on_policy_fv import MonteCarloOnPolicyFirstVisit
from learning.qlearning import QLearning
from learning.sarsa import Sarsa
from model.game import Game
from model.game_info import Winner
from model.policy import Policy
from policies.dealer import DealerPolicy
from policies.deterministic import DeterministicPolicy

GameStats = namedtuple('GameStats', ['wins', 'draws', 'losses'])

GAME_RUNS = 10000
EPOCHS = 50000
ALPHAS = [0.001, 0.01, 0.1, 0.2, 0.5]
GAMMAS = [0.5, 0.7, 0.9, 0.99]
EPSILONS = [0.2, 0.1, 0.05]


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


def profile_mces():
    mces = MonteCarloExploringStates()
    mces.train(EPOCHS)
    print(f'MonteCarloExploringStates:      {check_stats_of_policy(mces.policy)}')


def profile_mc_op_fv():
    for eps in EPSILONS:
        mcopfv = MonteCarloOnPolicyFirstVisit(epsilon=eps)
        mcopfv.train(EPOCHS)
        print(f'MonteCarloOnPolicyFirstVisit:   {check_stats_of_policy(mcopfv.policy)}\t\teps: {eps}')


def profile_sarsa():
    for alp, gam in product(ALPHAS, GAMMAS):
        sarsa = Sarsa(alpha=alp, gamma=gam)
        sarsa.train(EPOCHS)
        print(f'Sarsa:                          {check_stats_of_policy(sarsa.policy)}'
              f'\t\talpha: {alp}\t\tgamma: {gam}')


def profile_qlearning():
    for alp, gam in product(ALPHAS, GAMMAS):
        ql = QLearning(alpha=alp, gamma=gam)
        ql.train(EPOCHS)
        print(f'QLearning:                      {check_stats_of_policy(ql.policy)}'
              f'\t\talpha: {alp}\t\tgamma: {gam}')



if __name__ == '__main__':
    print(20 * '#')
    print(f'Deterministic policy:           {check_stats_of_policy(DeterministicPolicy())}')

    print(20 * '#')
    profile_mces()

    print(20 * '#')
    profile_mc_op_fv()

    print(20 * '#')
    profile_sarsa()

    print(20 * '#')
    profile_qlearning()
