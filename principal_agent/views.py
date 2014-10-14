# -*- coding: utf-8 -*-
from __future__ import division
from . import models
from ._builtin import Page, WaitPage
from otree.common import Money, money_range
from .models import Constants


def variables_for_all_templates(self):

    efforts_returns_costs = []
    for effort in range(1, 10+1):
        efforts_returns_costs.append(
            [effort,
             models.return_from_effort(effort),
             models.cost_from_effort(effort)]
        )

    return {'fixed_payment': Constants.max_fixed_payment,
            'reject_principal_pay': Constants.reject_principal_pay,
            'reject_agent_pay': Constants.reject_agent_pay,
            'efforts_returns_costs': efforts_returns_costs}


class Introduction(Page):

    template_name = 'principal_agent/Introduction.html'


class Offer(Page):

    def participate_condition(self):
        return self.player.role() == 'principal'

    template_name = 'principal_agent/Offer.html'

    form_model = models.Group
    form_fields = ['agent_fixed_pay', 'agent_return_share']


class OfferWaitPage(WaitPage):

    scope = models.Group

    def body_text(self):
        if self.player.role() == 'agent':
            return "Waiting for Player A to propose a contract."
        else:
            return "Waiting for Player B."


class Accept(Page):

    template_name = 'principal_agent/Accept.html'

    def participate_condition(self):
        return self.player.role() == 'agent'

    form_model = models.Group
    form_fields = ['contract_accepted']

    def variables_for_template(self):
        return {'fixed_pay': self.group.agent_fixed_pay,
                'return_share': int(self.group.agent_return_share * 100)}


class WorkEffort(Page):

    template_name = 'principal_agent/WorkEffort.html'

    form_model = models.Group
    form_fields = ['agent_work_effort']

    def participate_condition(self):
        return self.player.role() == 'agent' and self.group.contract_accepted

class ResultsWaitPage(WaitPage):
    scope = models.Group
    def body_text(self):
        if self.player.role() == 'principal':
            return "Waiting for Player B to respond."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):

    template_name = 'principal_agent/Results.html'

    def variables_for_template(self):
        return {'accepted': self.group.contract_accepted,
                'agent': self.player.role() == 'agent',
                'fixed_pay': self.group.agent_fixed_pay,
                'return_share': int(self.group.agent_return_share * 100),
                'effort_level': self.group.agent_work_effort,
                'payoff': self.player.payoff}


def pages():

    return [Introduction,
            Offer,
            OfferWaitPage,
            Accept,
            WorkEffort,
            ResultsWaitPage,
            Results]
