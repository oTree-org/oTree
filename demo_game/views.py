# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Currency as c, currency_range
from .models import Constants


def vars_for_all_templates(self):
    return {
        'total_q': 5,  # total number of questions to help participants understand study
    }


class Introduction(Page):
    pass

class Question1(Page):
    template_name = 'demo_game/Question.html'

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_1']


class Feedback1(Page):
    template_name = 'demo_game/Feedback.html'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {'num_q': 1,
                'question': "How many understanding questions are there? Please enter an odd negative integer, or a non-negative integer.",
                'answer': self.player.training_question_1,
                'correct': Constants.training_1_correct,
                'explanation': "There are 5 understanding questions.",
                'is_correct': self.player.is_training_question_1_correct(),
                }


class Question2(Page):
    template_name = 'demo_game/Question.html'

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_2']

    def vars_for_template(self):
        return {'num_q': 2}


class Feedback2(Page):
    template_name = 'demo_game/Feedback.html'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {'num_q': 2,
                'question': "All the following are possible in oTree except one?",
                'answer': self.player.training_question_2,
                'correct': Constants.training_2_correct,
                'explanation': "Time travel (opens in pop up window)",
                'is_correct': self.player.is_training_question_2_correct(),
                }


class Question3(Page):
    template_name = 'demo_game/Question.html'

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_3']

    def vars_for_template(self):
        return {'num_q': 3}


class Feedback3(Page):
    template_name = 'demo_game/Feedback.html'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {'num_q': 3,
                'question': "What operating system is required to use oTree?",
                'answer': self.player.training_question_3,
                'correct': Constants.training_3_correct,
                'explanation': "Any of the above operating system.",
                'is_correct': self.player.is_training_question_3_correct(),
                }


class Question4(Page):
    template_name = 'demo_game/Question.html'

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_4']

    def vars_for_template(self):
        return {'num_q': 4}


class Feedback4(Page):
    template_name = 'demo_game/Feedback.html'

    def is_displayed(self):
        return True

    def vars_for_template(self):
        return {'num_q': 4,
       'question': "What can be monitored during the experiment via the admin console?",
                'answer': self.player.training_question_4,
                'correct': Constants.training_4_correct,
                'explanation': "All of the above.",
                'is_correct': self.player.is_training_question_4_correct(),

                }


class Question5(Page):
    template_name = 'demo_game/Question.html'

    def is_displayed(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_5']

    def vars_for_template(self):
        return {'num_q': 5}


class Feedback5(Page):
    template_name = 'demo_game/Feedback.html'

    def is_displayed(self):
        return True


    def vars_for_template(self):
        return {'num_q': 5,
                'question': "What kind of data is included when you export a CSV from oTree?",
                'answer': self.player.training_question_5,
                'correct': Constants.training_5_correct,
                'explanation': "Any participants’ input/choice.",
                'is_correct': self.player.is_training_question_5_correct(),

                }


class FormsDemo(Page):

    form_model = models.Player
    form_fields = ['demo_field1', 'demo_field2']


class Results(Page):

    def vars_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()

        # return {
        #     'payoff': self.player.payoff
        # }


class Finish(Page):
    pass


page_sequence=[
        Introduction,
        Question1,
        Feedback1,
        Question2,
        Feedback2,
        Question3,
        Feedback3,
        Question4,
        Feedback4,
        Question5,
        Feedback5,
        FormsDemo,
        Results,
        Finish,
    ]
