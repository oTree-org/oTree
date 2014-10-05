# -*- coding: utf-8 -*-
from __future__ import division
import otree.views
import otree.views.concrete
import quiz.models as models
from quiz._builtin import Page, WaitPage
from otree.common import Money, money_range

def variables_for_all_templates(self):
    return {
        # example:
        #'my_field': self.player.my_field,
    }

class Questions(Page):

    def participate_condition(self):
        return True

    template_name = 'quiz/Questions.html'

    def get_form_class(self):
        return forms.QuestionForm


class Results(Page):

    template_name = 'quiz/Results.html'

    def variables_for_template(self):
        self.player.payoff = 0
        quiz_questions = []
        for field_name in forms.QuestionForm.Meta.fields:
            quiz_questions.append(self.player.get_quiz_question(field_name))

        return {'quiz_questions': quiz_questions}

def pages():
    return [
        Questions,
        Results
    ]