# -*- coding: utf-8 -*-
import public_goods.models as models
from public_goods._builtin import Page, WaitPage


def variables_for_all_templates(self):
    return {'endowment': self.treatment.endowment}


class Introduction(Page):

    """Description of the game: How to play and returns expected"""

    template_name = 'public_goods/Introduction.html'

    def variables_for_template(self):
        return {'no_of_players': self.match.players_per_match,
                'efficiency_factor': self.treatment.efficiency_factor}


class Question(Page):
    template_name = 'public_goods/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['question']


class Feedback(Page):
    template_name = 'public_goods/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'answer': self.player.question,
                'is_correct': self.player.question_correct(),
                }


class Contribute(Page):

    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']

    template_name = 'public_goods/Contribute.html'


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for other participants to contribute."


class Results(Page):

    """Players payoff: How much each has earned"""

    template_name = 'public_goods/Results.html'

    def variables_for_template(self):
        # calculations here
        my_contribution = self.player.contribution
        other_contribution = sum([c.contribution for c in self.match.players])
        total_contribution = other_contribution + my_contribution
        total_earnings = float(total_contribution) * 1.8
        share_earnings = float(total_earnings) / 3
        individual_earnings = (self.treatment.endowment - my_contribution) + share_earnings

        return {
            'my_contribution': my_contribution,
            'other_contribution': other_contribution,
            'total_contribution': total_contribution,
            'total_earnings': total_earnings,
            'share_earnings': share_earnings,
            'payoff': self.player.payoff,
            'base_pay': self.player.participant.session.base_pay,
            'total_pay': self.player.participant.total_pay()
        }

class FeedbackQ(Page):
    template_name = 'public_goods/FeedbackQ.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['feedbackq']



def pages():

    return [Introduction,
            Question,
            Feedback,
            Contribute,
            ResultsWaitPage,
            Results,
            FeedbackQ]
