import time
from collections import namedtuple
from itertools import product

from learning.learning_utils import Algorithm
from learning.mc_es import MonteCarloExploringStates
from learning.mc_on_policy_fv import MonteCarloOnPolicyFirstVisit
from learning.qlearning import QLearning
from learning.sarsa import Sarsa
from model.game import Game
from model.game_info import Winner
from model.policy import Policy
from plotting.plotting import ProbabilisticPolicyPlotter, DeterministicPolicyPlotter
from policies.dealer import DealerPolicy
from policies.deterministic import DeterministicPolicy

GameStats = namedtuple('GameStats', ['wins', 'draws', 'losses'])

GAME_RUNS = 10000
EPOCHS = 50000
EPOCHS_MORE = 2000000
ALPHAS = [0.01, 0.1, 0.5]
GAMMAS = [0.5, 0.9, 0.99]
EPSILONS = [0.2, 0.1, 0.05]

prob_policy_plotter = ProbabilisticPolicyPlotter()
det_policy_plotter = DeterministicPolicyPlotter()


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


def train(alg: Algorithm, rounds: int) -> float:
    start = time.time()
    alg.train(rounds)
    return time.time() - start


def profile_mces():
    def profile(epochs):
        mces = MonteCarloExploringStates()
        t = train(mces, epochs)

        print(f'MonteCarloExploringStates ({epochs} epochs, {t:4.2f}s): '
              f'{check_stats_of_policy(mces.policy)}')
        det_policy_plotter.plot(mces.policy)

    profile(EPOCHS)
    profile(EPOCHS_MORE)


def profile_mc_op_fv():
    def profile(epochs):
        for eps in EPSILONS:
            mcopfv = MonteCarloOnPolicyFirstVisit(epsilon=eps)
            t = train(mcopfv, epochs)

            print(f'MonteCarloOnPolicyFirstVisit ({epochs} epochs, {t:4.2f}s): '
                  f'{check_stats_of_policy(mcopfv.policy)}\t\teps: {eps}')

            prob_policy_plotter.plot(mcopfv.policy)

    profile(EPOCHS)
    profile(EPOCHS_MORE)


def profile_sarsa():
    def profile(epochs):
        for alp, gam in product(ALPHAS, GAMMAS):
            sarsa = Sarsa(alpha=alp, gamma=gam)
            t = train(sarsa, epochs)
            print(f'Sarsa ({epochs} epochs, {t:4.2f}s): '
                  f'{check_stats_of_policy(sarsa.policy)}'
                  f'\t\talpha: {alp}\t\tgamma: {gam}')

            prob_policy_plotter.plot(sarsa.policy)

    profile(EPOCHS)
    profile(EPOCHS_MORE)


def profile_qlearning():
    def profile(epochs):
        for alp, gam in product(ALPHAS, GAMMAS):
            ql = QLearning(alpha=alp, gamma=gam)
            t = train(ql, epochs)
            print(f'QLearning ({epochs} epochs, {t:4.2f}s): '
                  f'{check_stats_of_policy(ql.policy)}'
                  f'\t\talpha: {alp}\t\tgamma: {gam}')

            det_policy_plotter.plot(ql.policy)

    # profile(EPOCHS)
    profile(EPOCHS_MORE)


def profile_deterministic():
    print(f'Deterministic policy: {check_stats_of_policy(DeterministicPolicy())}')
    det_policy_plotter.plot(DeterministicPolicy())


if __name__ == '__main__':
    # print(20 * '#')
    # profile_deterministic()
    #
    # print(20 * '#')
    # profile_mces()
    #
    # print(20 * '#')
    # profile_mc_op_fv()

    # print(20 * '#')
    # profile_sarsa()

    print(20 * '#')
    profile_qlearning()
