from model.game import Game, Deck
from model.game_info import Winner
from policies.dealer import DealerPolicy
from policies.deterministic import DeterministicPolicy


def play_sample(g):
    ginfo = g.play()
    print(f'winner: {ginfo.winner.name}')
    print(f'### Player states ###')
    for s in ginfo.player_logs:
        print(f'sum: {s[0].current_sum}\t\t'
              f'opponent pts: {s[0].opponent_points}\t'
              f'usable: {s[0].holds_usable_ace}\n'
              f'action: {s[1].name}')
    print(f'### Dealer states ###')
    for s in ginfo.dealer_logs:
        print(f'sum: {s[0].current_sum}\t\t'
              f'opponent pts: {s[0].opponent_points}\t'
              f'usable: {s[0].holds_usable_ace}\n'
              f'action: {s[1].name}')


if __name__ == '__main__':
    g = Game(player_policy=DeterministicPolicy(),
             dealer_policy=DealerPolicy(),
             deck=Deck())

    # play_sample(g)

    wins, draws, loses = 0, 0, 0
    rounds = 100000
    for i in range(rounds):
        winner = g.play().winner
        if winner == Winner.DEALER:
            loses += 1
        elif winner == Winner.PLAYER:
            wins += 1
        else:
            draws += 1

    print(f'wins: {100. * wins / rounds}%')
    print(f'draws: {100. * draws / rounds}%')
    print(f'loses: {100. * loses / rounds}%')
