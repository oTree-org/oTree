from . import pages
from ._builtin import Bot


class PlayerBot(Bot):
    def play_round(self):
        # intro
        yield (pages.Introduction)

        if self.player.id_in_group == 1:
            # P1/A - propose contract
            yield (
                pages.Offer, {'agent_fixed_pay': 10, 'agent_return_share': 0.6}
            )
        else:
            # P2/B - accept or reject contract
            yield (
                pages.Accept,
                {'contract_accepted': True, 'agent_work_effort': 10}
            )
        # results

        yield (pages.Results)

        if self.player.id_in_group == 1:
            assert self.player.payoff == 46 + 30
        else:
            assert self.player.payoff == 34 + 30
