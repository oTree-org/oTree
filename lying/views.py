import lying.forms as forms
from lying.utilities import Page, MatchWaitPage, SubsessionWaitPage
from otree.common import Money, money_range


class FlipCoins(Page):

    template_name = 'lying/CoinFlip.html'

    def get_form_class(self):
        return forms.CoinFlipForm

    def variables_for_template(self):
        # participant is an instance of sessionlib.SessionUser
        #self.player.participant.vars['foo'] = 1

        # session is an instance of sessionlib.Session
        #self.subsession.session.vars['session_foo'] = 2
        return {'number_of_flips': self.treatment.number_of_flips,
                'payoff_per_head': self.treatment.payoff_per_head}

    def after_valid_form_submission(self):
        self.player.set_payoff()


class Results(Page):

    template_name = 'lying/Results.html'

    def variables_for_template(self):

        return {
            #'foo': self.player.participant.vars['foo'],
            #'session_foo': self.subsession.session.vars['session_foo'],
            'payoff': self.player.payoff,
            'number_of_heads': self.player.number_of_heads,
        }


def pages():
    return [FlipCoins, Results]