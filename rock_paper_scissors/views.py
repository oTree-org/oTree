# -*- coding: utf-8 -*-
from __future__ import division
import otree.views
import rock_paper_scissors.models as models
from rock_paper_scissors._builtin import Page, WaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
        return {'total_q': 1,
                'total_rounds': self.subsession.number_of_rounds,
                'round_number': self.subsession.round_number,
                'role': self.player.role()}


class Introduction(Page):

    template_name = 'rock_paper_scissors/Introduction.html'

    def participate_condition(self):
        return self.subsession.round_number == 1


class QuestionOne(Page):

    template_name = 'rock_paper_scissors/Question.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):

    template_name = 'rock_paper_scissors/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'num_q': 1,
                'question': 'Can you resume all the instructions in one line?',
                'answer': self.player.training_question_1,
                'correct': self.subsession.training_1_correct,
                'explanation': 'Scissors beats the paper, paper beats the rock and rock beat the scissors',
                'is_correct': self.player.is_training_question_1_correct()}


class Choice(Page):

    template_name = 'rock_paper_scissors/Choice.html'

    form_model = models.Player
    form_fields = ['rps_choice']


class ResultsWaitPage(WaitPage):

    scope = models.Group

    def after_all_players_arrive(self):
        self.group.set_points()

    def body_text(self):
        return "Waiting for your opponent."


class Results(Page):

    template_name = 'rock_paper_scissors/Results.html'

    def variables_for_template(self):
        self.player.set_payoff()

        return {'my_choice': self.player.rps_choice,
                'other_choice': self.player.other_player().rps_choice,
                'my_points': self.player.points_earned,
                'other_points': self.player.other_player().points_earned,
                'my_payoff': self.player.payoff,
                'other_payoff': self.player.other_player().payoff}


class ResultsSummary(Page):

    template_name = 'matching_pennies/ResultsSummary.html'

    def participate_condition(self):
        return self.subsession.round_number == self.subsession.number_of_rounds

    def variables_for_template(self):
        total_points_earned = sum(p.points_earned for p in self.player.me_in_all_rounds())
        base_points = 50

        return {'me_in_all_rounds': self.player.me_in_all_rounds(),
                'points_earned': self.player.points_earned,
                'is_winner': self.player.is_winner,
                'total_points_earned': total_points_earned,
                'base_points': base_points,
                'total_plus_base': total_points_earned + base_points}


def pages():

    return [Introduction,
            QuestionOne,
            FeedbackOne,
            Choice,
            ResultsWaitPage,
            Results,
            ResultsSummary]
