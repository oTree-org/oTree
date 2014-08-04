import lying.forms as forms
from lying.utilities import Page, MatchWaitPage, SubsessionWaitPage
from ptree.common import currency


class Start(Page):
    template_name = 'lying/Start.html'


class FlipCoins(Page):

    template_name = 'lying/CoinFlip.html'

    def get_form_class(self):
        return forms.CoinFlipForm

    def variables_for_template(self):
        return {'number_of_flips': self.treatment.number_of_flips,
                'payoff_per_head': currency(self.treatment.payoff_per_head)}

    def after_valid_form_submission(self):
        self.participant.set_payoff()


class Results(Page):

    template_name = 'lying/Results.html'

    def variables_for_template(self):
        return {
            'test_amount': self.participant.test_amount,
            'payoff': currency(self.participant.payoff),
            'number_of_heads': self.participant.number_of_heads,
        }


def pages():
    return [Start, FlipCoins, Results]