from . import views
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        # intro
        yield (views.Introduction)

        if self.player.id_in_group == 1:
            # P1/A - propose contract
            yield (
                views.Offer, {'agent_fixed_pay': 10, 'agent_return_share': 0.6}
            )
        else:
            # P2/B - accept or reject contract
            yield (
                views.Accept,
                {'contract_accepted': True, 'agent_work_effort': 10}
            )
        # results

        yield (views.Results)

        if self.player.id_in_group == 1:
            assert self.player.payoff == 46 + 30
        else:
            assert self.player.payoff == 34 + 30
