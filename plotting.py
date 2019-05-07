import matplotlib.pyplot as plt
from matplotlib import colors

from model.policy import Policy
from model.state import State


class DeterministicPolicyPlotter:
    @staticmethod
    def plot(policy: Policy) -> None:
        with_usable, without_usable = DeterministicPolicyPlotter._retrieve_choices(policy)

        cmap = colors.ListedColormap(['red', 'green'])

        fig, axs = plt.subplots(1, 2)
        axs[0].set_title('With usable ace')
        axs[1].set_title('Without usable ace')

        DeterministicPolicyPlotter._plot_one_ace_case(fig, axs[0], with_usable, cmap)
        DeterministicPolicyPlotter._plot_one_ace_case(fig, axs[1], without_usable, cmap)

        fig.tight_layout()
        plt.show()

    @staticmethod
    def _plot_one_ace_case(fig, ax, data, cmap):
        xs = range(2, 13)
        ys = range(12, 23)
        plot = ax.pcolormesh(xs, ys, data, cmap=cmap, edgecolors='k')

        cbar = fig.colorbar(plot, ax=ax, cmap=cmap, ticks=[.25, .75],
                            aspect=2, shrink=0.1)
        cbar.set_ticklabels(['Stick', 'Hit'])

        ax.set_aspect('equal', anchor='W')
        ax.set_xticks(xs[:-1])
        ax.set_yticks(ys[:-1])

    @staticmethod
    def _retrieve_choices(policy):
        choices_with_usable = [[policy.make_decision_in
                                (State(player_sum, opponent_sum, True)).value
                                for opponent_sum in range(2, 12)]
                               for player_sum in range(12, 22)]
        choices_without_usable = [[policy.make_decision_in
                                   (State(player_sum, opponent_sum, False)).value
                                   for opponent_sum in range(2, 12)]
                                  for player_sum in range(12, 22)]
        return choices_with_usable, choices_without_usable
