# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import demo_game.models as models
from demo_game._builtin import Page
from otree.common import currency


def variables_for_all_templates(self):
    return {
        'total_q': 4,  # total number of questions to help participants understand study
    }


class Introduction(Page):

    template_name = 'demo_game/Introduction.html'


class QuestionOne(Page):
    template_name = 'demo_game/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_1']

    def variables_for_template(self):
        return {'num_q': 1}


class FeedbackOne(Page):
    template_name = 'demo_game/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'num_q': 1,
                'question': "How many understanding questions are there? Please enter an odd negative integer, or a non-negative integer.",
                'answer': self.player.training_question_1,
                'correct': self.treatment.training_1_correct,
                'explanation': "There are 3 understanding questions.",
                'is_correct': self.player.is_training_question_1_correct(),
                }


class QuestionTwo(Page):
    template_name = 'demo_game/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_2']

    def variables_for_template(self):
        return {'num_q': 2}


class FeedbackTwo(Page):
    template_name = 'demo_game/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'num_q': 2,
                'question': "All the following are possible in oTree except one?",
                'answer': self.player.training_question_2,
                'correct': self.treatment.training_2_correct,
                'explanation': "Time travel (opens in pop up window)",
                'is_correct': self.player.is_training_question_2_correct(),
                }


class QuestionThree(Page):
    template_name = 'demo_game/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_3']

    def variables_for_template(self):
        return {'num_q': 3}


class FeedbackThree(Page):
    template_name = 'demo_game/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'num_q': 3,
                'question': "What operating system is required to use oTree?",
                'answer': self.player.training_question_3,
                'correct': self.treatment.training_3_correct,
                'explanation': "Any of the above operating system.",
                'is_correct': self.player.is_training_question_3_correct(),
                }


class QuestionFour(Page):
    template_name = 'demo_game/Question.html'

    def participate_condition(self):
        return True

    form_model = models.Player
    form_fields = ['training_question_4']

    def variables_for_template(self):
        return {'num_q': 4}


class FeedbackFour(Page):
    template_name = 'demo_game/Feedback.html'

    def participate_condition(self):
        return True

    def variables_for_template(self):
        return {'num_q': 4,
                'question': "What kind of data is included when you export a CSV from oTree?",
                'answer': self.player.training_question_4,
                'correct': self.treatment.training_4_correct,
                'explanation': "Any participants’ input/choice.",
                'is_correct': self.player.is_training_question_4_correct(),
                }



class FormsDemo(Page):

    template_name = 'demo_game/FormsDemo.html'

    form_model = models.Player
    form_fields = ['demo_field1', 'demo_field2']


class EmbedDemo(Page):

    template_name = 'demo_game/EmbedDemo.html'


class BootstrapWidgetDemo(Page):

    template_name = 'demo_game/BootstrapWidgetsDemo.html'


class AdminDemo(Page):

    template_name = 'demo_game/AdminDemo.html'


class Results(Page):

    def variables_for_template(self):
        if self.player.payoff is None:
            self.player.set_payoff()
        return {
            'payoff': currency(self.player.payoff)
        }

    template_name = 'demo_game/Results.html'

# TODO Replace this page with a lab results app..with a more detailed page..See DEMO GAME 3.docx By Shuya page 7
class Finish(Page):

    template_name = 'demo_game/Finish.html'


def pages():
    return [
        Introduction,
        QuestionOne,
        FeedbackOne,
        QuestionTwo,
        FeedbackTwo,
        QuestionThree,
        FeedbackThree,
        QuestionFour,
        FeedbackFour,
        FormsDemo,
        Results,
        Finish,
    ]