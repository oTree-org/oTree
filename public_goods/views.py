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
        current_player = self.player
        other_players = self.player.other_players_in_match
        total_contribution = sum([c.contribution for c in self.match.players])
        total_earnings = float(total_contribution) * 1.8
        share_earnings = float(total_earnings) / 3
        individual_earnings = (self.treatment.endowment - current_player.contribution) + share_earnings
        base_points = 10
        total_points = individual_earnings + base_points

        return {
            'current_player': current_player,
            'other_players': other_players,
            'total_contribution': total_contribution,
            'total_earnings': total_earnings,
            'share_earnings': share_earnings,
            'individual_earnings': individual_earnings,
            'payoff': self.player.payoff,
            'base_points': base_points,
            'total_points': total_points
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
