import lying.forms as forms
from lying.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class FlipCoins(Page):

    template_name = 'lying/CoinFlip.html'

    def get_form_class(self):
        return forms.CoinFlipForm

    def variables_for_template(self):
        return {'number_of_flips': self.treatment.number_of_flips,
                'payoff_per_head': self.treatment.payoff_per_head}

    def after_valid_form_submission(self):
        self.participant.set_payoff()


class Results(Page):

    template_name = 'lying/Results.html'

    def variables_for_template(self):
        return {
            'payoff': self.participant.payoff,
            'number_of_heads': self.participant.number_of_heads,
        }


def pages():
    return [FlipCoins, Results]