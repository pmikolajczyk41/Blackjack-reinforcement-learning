from typing import List

import matplotlib.pyplot as plt
from matplotlib import colors

from model.policy import Policy
from model.state import State


class PolicyPlotter:
    def plot(self, policy: Policy) -> None:
        with_usable, without_usable = self._retrieve_choices(policy)

        fig, axs = plt.subplots(1, 2)
        axs[0].set_title('With usable ace')
        axs[1].set_title('Without usable ace')

        self._plot_one_ace_case(fig, axs[0], with_usable)
        self._plot_one_ace_case(fig, axs[1], without_usable)

        fig.tight_layout()
        plt.show()

    def _plot_one_ace_case(self, fig, param, data):
        raise NotImplemented

    def _retrieve_choices(self, policy) -> (List, List):
        raise NotImplemented


class DeterministicPolicyPlotter(PolicyPlotter):
    def _plot_one_ace_case(self, fig, ax, data):
        cmap = colors.ListedColormap(['red', 'green'])

        xs = range(2, 13)
        ys = range(12, 23)
        plot = ax.pcolormesh(xs, ys, data, cmap=cmap, edgecolors='k')

        cbar = fig.colorbar(plot, ax=ax, cmap=cmap, ticks=[.25, .75],
                            aspect=2, shrink=0.1)
        cbar.set_ticklabels(['Stick', 'Hit'])

        ax.set_aspect('equal', anchor='W')
        ax.set_xticks(xs[:-1])
        ax.set_yticks(ys[:-1])

    def _retrieve_choices(self, policy):
        choices_with_usable = [[policy.make_decision_in
                                (State(player_sum, opponent_sum, True)).value
                                for opponent_sum in range(2, 12)]
                               for player_sum in range(12, 22)]
        choices_without_usable = [[policy.make_decision_in
                                   (State(player_sum, opponent_sum, False)).value
                                   for opponent_sum in range(2, 12)]
                                  for player_sum in range(12, 22)]
        return choices_with_usable, choices_without_usable


class ProbabilisticPolicyPlotter(PolicyPlotter):

    def _plot_one_ace_case(self, fig, ax, data):
        xs = range(2, 13)
        ys = range(12, 23)
        plot = ax.pcolormesh(xs, ys, data, cmap='RdYlGn', edgecolors='k')

        cbar = fig.colorbar(plot, ax=ax, cmap='RdYlGn', ticks=[.1, .9],
                            aspect=12, shrink=0.3)
        cbar.set_ticklabels(['Stick', 'Hit'])

        ax.set_aspect('equal', anchor='W')
        ax.set_xticks(xs[:-1])
        ax.set_yticks(ys[:-1])

    def _retrieve_choices(self, policy):
        choices_with_usable = [[policy.hit_certainty_in
                                (State(player_sum, opponent_sum, True))
                                for opponent_sum in range(2, 12)]
                               for player_sum in range(12, 22)]
        choices_without_usable = [[policy.hit_certainty_in
                                   (State(player_sum, opponent_sum, False))
                                   for opponent_sum in range(2, 12)]
                                  for player_sum in range(12, 22)]
        return choices_with_usable, choices_without_usable
