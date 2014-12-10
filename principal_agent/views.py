# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, cost_from_effort
from otree.common import safe_json


def variables_for_all_templates(self):

    efforts_returns_costs = []
    for effort in range(1, 10 + 1):
        efforts_returns_costs.append(
            [effort,
             models.return_from_effort(effort),
             models.cost_from_effort(effort)]
        )

    return {'instructions': 'principal_agent/Rules.html',
            'fixed_payment': Constants.max_fixed_payment,
            'reject_principal_pay': Constants.reject_principal_pay,
            'reject_agent_pay': Constants.reject_agent_pay,
            'efforts_returns_costs': efforts_returns_costs}


class Introduction(Page):

    template_name = 'global/Introduction.html'


class Question1(Page):
    template_name = 'global/Question.html'
    form_model = models.Player
    form_fields = ['training_my_payoff', 'training_other_payoff']

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        return {'question_template': 'principal_agent/Question.html'}


class Feedback1(Page):
    template_name = 'principal_agent/Feedback.html'

    def participate_condition(self):
        return self.subsession.round_number == 1

    def variables_for_template(self):
        p = self.player
        return {'answers': [
                ('yourself', [p.training_my_payoff, 46]),
                ('B', [p.training_other_payoff, 34])]}


class Offer(Page):

    def participate_condition(self):
        return self.player.role() == 'principal'

    template_name = 'principal_agent/Offer.html'

    form_model = models.Group
    form_fields = ['agent_fixed_pay', 'agent_return_share']


class OfferWaitPage(WaitPage):



    def body_text(self):
        if self.player.role() == 'agent':
            return "You are Participant B. Waiting for Participant A to propose a contract."
        else:
            return "Waiting for Participant B."


class Accept(Page):

    template_name = 'principal_agent/Accept.html'

    def participate_condition(self):
        return self.player.role() == 'agent'

    form_model = models.Group
    form_fields = ['contract_accepted', 'agent_work_effort']

    def variables_for_template(self):
        return {'fixed_pay': self.group.agent_fixed_pay,
                'EFFORT_TO_RETURN': safe_json(Constants.EFFORT_TO_RETURN),
                'EFFORT_TO_COST': safe_json(Constants.EFFORT_TO_COST),
                'return_share': int(self.group.agent_return_share * 100)}


class ResultsWaitPage(WaitPage):


    def body_text(self):
        if self.player.role() == 'principal':
            return "Waiting for Participant B to respond."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        return {'accepted': self.group.contract_accepted,
                'agent': self.player.role() == 'agent',
                'fixed_pay': self.group.agent_fixed_pay,
                'fixed_pay_int': int(self.group.agent_fixed_pay),
                'return_share': int(self.group.agent_return_share * 100),
                'effort_level': self.group.agent_work_effort,
                'effort_cost': cost_from_effort(self.group.agent_work_effort),
                'return': self.group.total_return,
                'received': self.player.payoff - Constants.bonus,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Question1,
            Feedback1,
            Offer,
            OfferWaitPage,
            Accept,
            ResultsWaitPage,
            Results]
