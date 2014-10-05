# -*- coding: utf-8 -*-
from __future__ import division
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from __future__ import division
from otree.db import models
import otree.models
from otree.common import Money, money_range
from otree import widgets


doc = """
In Principal Agent Game, there are two players: One acts as the Agent and the other acts as the
Principal. The Principal offers a contract to the Agent, which can be accepted or rejected.
The game is described <a href="http://www.nottingham.ac.uk/cedex/documents/papers/2006-04.pdf" target="_blank">here</a>.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/principal_agent" target="_blank">here</a>.
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'principal_agent'

    max_fixed_payment = models.MoneyField(
        default=7.00,
        doc="""Maxmimum absolute value for agent's fixed pay"""
    )

    reject_principal_pay = models.MoneyField(
        default=0,
        doc="""Amount principal gets if contract is rejected"""
    )

    reject_agent_pay = models.MoneyField(
        default=1.00,
        doc="""Amount agent gets if contract is rejected"""
    )

    agent_work_effort_base_return = models.MoneyField(
        default=0.7,
        doc="""Total return for single unit of agent's work effort"""
    )

    @staticmethod
    def cost_from_effort(effort):
        costs = {1: 0,
                 2: .20,
                 3: .40,
                 4: .60,
                 5: .90,
                 6: 1.20,
                 7: 1.60,
                 8: 2.00,
                 9: 2.50,
                 10: 3.00}
        return Money(costs[effort])

    def return_from_effort(self, effort):
        return effort*Money(self.agent_work_effort_base_return)



class Treatment(otree.models.BaseTreatment):
    """Leave this class empty"""

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_match = 2

    total_return = models.MoneyField(
        default=None,
        doc="""Total return from agent's effort = [Return for single unit of agent's work effort] * [Agent's work effort]"""
    )

    agent_fixed_pay = models.MoneyField(
        default=None,
        doc="""Amount offered as fixed pay to agent"""
    )

    agent_return_share = models.FloatField(
        default=None,
        doc="""Agent's share of total return""",
    )

    agent_work_effort = models.PositiveIntegerField(
        default=None,
        doc="""Agent's work effort, [1, 10]""",
    )


    agent_work_cost = models.MoneyField(
        default=None,
        doc="""Agent's cost of work effort"""
    )

    contract_accepted = models.NullBooleanField(
        default=None,
        doc="""Whether agent accepts proposal""",
        widget=widgets.RadioSelect(),
    )

    # choices
    def agent_fixed_pay_choices(self):
        return money_range(-self.subsession.max_fixed_payment, self.subsession.max_fixed_payment, 0.50)

    def agent_work_effort_choices(self):
        return range(1, 10+1)

    def agent_return_share_choices(self):
        RETURN_SHARE_CHOICES = []
        for percent in range(10, 100+1, 10):
            RETURN_SHARE_CHOICES.append([percent/100, '{}%'.format(percent)])

        return RETURN_SHARE_CHOICES


    def set_payoffs(self):
        principal = self.get_player_by_role('principal')
        agent = self.get_player_by_role('agent')

        if not self.contract_accepted:
            principal.payoff = self.subsession.reject_principal_pay
            agent.payoff = self.subsession.reject_agent_pay
        else:
            self.agent_work_cost = self.subsession.cost_from_effort(self.agent_work_effort)
            self.total_return = self.subsession.return_from_effort(self.agent_work_effort)

            money_to_agent = self.agent_return_share*self.total_return + self.agent_fixed_pay
            agent.payoff = money_to_agent - self.agent_work_cost
            principal.payoff = self.total_return - money_to_agent


class Player(otree.models.BasePlayer):

    # <built-in>
    match = models.ForeignKey(Match, null=True)
    treatment = models.ForeignKey(Treatment, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def role(self):
        if self.index_among_players_in_match == 1:
            return 'principal'
        if self.index_among_players_in_match == 2:
            return 'agent'


def treatments():

    return [Treatment.create()]
