# -*- coding: utf-8 -*-
import matching_pennies.models as models
from matching_pennies._builtin import Page, WaitPage
from otree.common import Money


def variables_for_all_templates(self):
    return {'total_q': 1,
            'total_rounds': self.subsession.number_of_rounds,
            'round_number': self.subsession.round_number,
            'role': self.player.role()}


class Introduction(Page):

    template_name = 'matching_pennies/Introduction.html'


class QuestionOne(Page):
    template_name = 'matching_pennies/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):
    template_name = 'matching_pennies/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'num_q': 1,
                'question': 'Suppose Player 1 picked "Heads" and Player 2 guessed "Tails". Which of the following will be the result of that round?',
                'answer': self.player.training_question_1,
                'correct': self.treatment.training_1_correct,
                'explanation': 'Player 1 gets 100 points, Player 2 gets 0 points',
                'is_correct': self.player.is_training_question_1_correct(),
                }


class Choice(Page):

    template_name = 'matching_pennies/Choice.html'

    form_model = models.Player
    form_fields = ['penny_side']

    def variables_for_template(self):
        return {'initial_amount': self.treatment.initial_amount,
                'winner_amount': self.treatment.initial_amount * 2,
                'loser_amount': Money(0)}


class ResultsWaitPage(WaitPage):

    group = models.Match

    def after_all_players_arrive(self):
        self.match.set_payoffs()

    def body_text(self):
        return "Waiting for the other player to select heads or tails."


class Results(Page):

    template_name = 'matching_pennies/Results.html'

    def variables_for_template(self):

        return {'my_choice': self.player.penny_side,
                'other_choice': self.player.other_player().penny_side,
                'is_winner': self.player.is_winner,
                'payoff': self.player.payoff,
                'me_in_previous_rounds': self.player.me_in_previous_rounds()}


def pages():

    return [Introduction,
            QuestionOne,
            FeedbackOne,
            Choice,
            ResultsWaitPage,
            Results]
