import lying.forms as forms
from lying.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {'round_number': self.subsession.round_number}

class FlipCoins(Page):

    template_name = 'lying/CoinFlip.html'

    def get_form_class(self):
        return forms.CoinFlipForm

    def variables_for_template(self):
        return {'number_of_flips': self.treatment.number_of_flips,
                'payoff_per_head': self.treatment.payoff_per_head,
                }

    def after_valid_form_submission(self):
        self.player.set_payoff()


class Results(Page):

    template_name = 'lying/Results.html'

    def variables_for_template(self):

        previous_players = self.player.previous_players()

        return {
            'payoff': self.player.payoff,
            'number_of_heads': self.player.number_of_heads,
            'previous_players': previous_players,
            'cumulative_payoff': sum(p.payoff for p in previous_players) + self.player.payoff,
            'cumulative_number_of_heads': sum(p.number_of_heads for p in previous_players) + self.player.number_of_heads,
        }

def pages():
    return [FlipCoins, Results]