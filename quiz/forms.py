# -*- coding: utf-8 -*-
import quiz.models as models
from django import forms
from quiz._builtin import Form
from crispy_forms.layout import HTML
from otree.common import Money, money_range

class QuestionForm(Form):

    class Meta:
        model = models.Player
        fields = ['q_doctor', 'q_meal']