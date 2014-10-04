# -*- coding: utf-8 -*-
from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import widgets
from otree import forms

doc = """
This is a one-period public goods game with 3 players. Assignment to groups is random.
<br />
The game is preceded by one understanding question (in a real experiment you would often have more).
<br />
Source code <a href="https://github.com/oTree-org/oTree/tree/master/public_goods" target="_blank">here</a>

"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'public_goods'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    endowment = models.PositiveIntegerField(
        default=100,
        doc="""Amount allocated to each player"""
    )

    efficiency_factor = models.FloatField(
        default=1.8,
        doc="""The multiplication factor in group contribution"""
    )

    question_correct = 92


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 3

    def set_payoffs(self):
        contributions = sum([p.contribution for p in self.players])
        individual_share = contributions * self.treatment.efficiency_factor / self.players_per_match
        for p in self.players:
            p.points = (self.treatment.endowment - p.contribution) + individual_share
            p.payoff = float(p.points) / 100


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    contribution = models.PositiveIntegerField(
        default=None,
        doc="""The amount contributed by the player""",
        widget=forms.TextInput()
    )

    points = models.PositiveIntegerField(null=True)

    question = models.PositiveIntegerField(null=True, verbose_name='', widget=forms.TextInput())
    feedbackq = models.CharField(null=True, verbose_name='How well do you think this sample game was implemented?', widget=forms.RadioSelectHorizontal())

    def feedbackq_choices(self):
        return ['Very well', 'Well', 'OK', 'Badly', 'Very badly']

    def question_correct(self):
        return self.question == self.treatment.question_correct

    def contribution_error_message(self, value):
        if not 0 <= value <= self.treatment.endowment:
            return 'Your entry is invalid.'

def treatments():
    return [Treatment.create()]
