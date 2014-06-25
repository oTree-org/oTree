# -*- coding: utf-8 -*-
"""Documentation at http://django-ptree.readthedocs.org/en/latest/app.html"""

from ptree.db import models
import ptree.models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxLengthValidator
from ptree.common import currency

doc="""
Trust game. Single treatment. Both players are given an initial sum.
One player may give part of the sum to the other player, who actually receives triple the amount.
The second player may then give part of the now-tripled amount back to the first player.
"""

class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'trust'

class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    amount_allocated = models.PositiveIntegerField(
        doc="""Initial amount allocated to each participant"""
    )

    increment_amount = models.PositiveIntegerField(
        doc="""The increment between send choices and send back choices, in cents"""
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    participants_per_match = 2

    # custom fields
    sent_amount = models.PositiveIntegerField(null=True,
                                              doc="""Amount sent by participant one""")
    sent_back_amount = models.PositiveIntegerField(null=True,
                                                   doc="""Amount sent back by participant two""")

    def send_choices(self):
        """Range of allowed values during send"""
        return range(0, self.treatment.amount_allocated+1, self.treatment.increment_amount)

    def send_back_choices(self):
        """Range of allowed values during send back"""
        return range(0, (self.sent_amount * 3 + 1), self.treatment.increment_amount)

    def get_send_field_choices(self):
        """Returns a tuple with the range of allowed values for participant one"""
        return tuple([(i, currency(i)) for i in self.send_choices()])

    def get_send_back_field_choices(self):
        """Returns a tuple with the range of allowed values for participant two"""
        return tuple([(i, currency(i)) for i in self.send_back_choices()])

    def get_payoff_participant_1(self):
        """Calculate participant one payoff"""
        if self.sent_amount is None:
            return None
        else:
            return self.treatment.amount_allocated - self.sent_amount + self.sent_back_amount

    def get_payoff_participant_2(self):
        """Calculate participant two payoff"""
        if self.sent_back_amount is None:
            return None
        else:
            return self.treatment.amount_allocated + self.sent_amount * 3 - self.sent_back_amount


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)

    # session feedback
    subsession_feedback = models.TextField(validators=[MaxLengthValidator(5000)], null=True, blank=True)

    def set_payoff(self):
        """ A method to calculate payoff for each participant"""
        if self.index_among_participants_in_match == 1:
            self.payoff = self.match.get_payoff_participant_1()
        elif self.index_among_participants_in_match == 2:
            self.payoff = self.match.get_payoff_participant_2()


def treatments():

    treatment_list = []

    treatment = Treatment(
        amount_allocated=100,
        increment_amount=5,
    )

    treatment_list.append(treatment)

    return treatment_list
