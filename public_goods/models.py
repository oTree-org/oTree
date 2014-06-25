# -*- coding: utf-8 -*-
from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from ptree.common import currency

doc="""
Public goods game. Single treatment. Four players can contribute to a joint project.
The total contribution is multiplied by some factor, the resulting amount is then divided equally between the players.
"""

class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'public_goods'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)
    amount_allocated = models.PositiveIntegerField(null=True,
                                                   doc="""
                                                   Amount allocated to each participant
                                                   """)
    multiplication_factor = models.DecimalField(null=True,
                                                decimal_places=1,
                                                max_digits=2,
                                                doc="""
                                                The multiplication factor in group contribution
                                                """)


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    participants_per_match = 4
    contributions = models.PositiveIntegerField(null=True)
    individual_share = models.PositiveIntegerField(null=True)

    def set_contributions(self):
        self.contributions = sum(p.contributed_amount for p in self.participants())

    def set_individual_share(self):
        self.individual_share = int((self.contributions*self.treatment.multiplication_factor)/self.participants_per_match)


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    contributed_amount = models.PositiveIntegerField(null=True)

    def payoff_currency(self):
        return currency(self.payoff)

    def contributed_amount_currency(self):
        return currency(self.contributed_amount)

    def set_payoff(self):
        self.payoff = (self.treatment.amount_allocated - self.contributed_amount) + self.match.individual_share

    def contribute_choices(self):
        return range(0, self.treatment.amount_allocated+1, 10)

    def get_contribute_choices(self):
        return [(i, currency(i)) for i in self.contribute_choices()]


def treatments():

    treatment_list = []

    treatment = Treatment(
        amount_allocated=300,
        multiplication_factor=1.6,
    )

    treatment_list.append(treatment)

    return treatment_list
