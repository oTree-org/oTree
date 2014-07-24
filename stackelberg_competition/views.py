# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import stackelberg_competition.forms as forms
from stackelberg_competition.utilities import ParticipantMixIn, MatchMixIn, SubsessionMixIn
from ptree.common import currency


class Introduction(ParticipantMixIn, ptree.views.Page):

    template_name = 'stackelberg_competition/Introduction.html'

    def variables_for_template(self):
        return {
            'total_capacity': self.treatment.total_capacity
        }


class ChoiceOne(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 1

    template_name = 'stackelberg_competition/ChoiceOne.html'

    def get_form_class(self):
        return forms.QuantityForm

class SimpleCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):
    pass

class ChoiceTwo(ParticipantMixIn, ptree.views.Page):

    def participate_condition(self):
        return self.participant.index_among_participants_in_match == 2

    template_name = 'stackelberg_competition/ChoiceTwo.html'

    def get_form_class(self):
        return forms.QuantityForm

    def variables_for_template(self):
        return {
            'other_quantity': self.participant.other_participant().quantity
        }

class ResultsCheckpoint(MatchMixIn, ptree.views.MatchCheckpoint):

    def action(self):
        for p in self.match.participants():
            p.set_payoff()

class Results(ParticipantMixIn, ptree.views.Page):

    template_name = 'stackelberg_competition/Results.html'

    def variables_for_template(self):

        return {
            'payoff': currency(self.participant.payoff),
            'quantity': self.participant.quantity,
            'other_quantity': self.participant.other_participant().quantity,
            'price': currency(self.match.price)
        }


class ExperimenterPage(SubsessionMixIn, ptree.views.ExperimenterPage):
    pass


def pages():
    return [
        Introduction,
        ChoiceOne,
        SimpleCheckpoint,
        ChoiceTwo,
        ResultsCheckpoint,
        Results
    ]