# -*- coding: utf-8 -*-
# <standard imports>
from __future__ import division
from otree.db import models
import otree.models
from otree import widgets
from otree.common import Money, money_range
import random
# </standard imports>


doc = """
In Principal Agent Game, there are two players: One acts as the Agent and the other acts as the
Principal. The Principal offers a contract to the Agent, which can be accepted or rejected.
The game is described <a href="http://www.nottingham.ac.uk/cedex/documents/papers/2006-04.pdf" target="_blank">here</a>.
Source code <a href="https://github.com/oTree-org/oTree/tree/master/principal_agent" target="_blank">here</a>.
"""


class Constants:
    max_fixed_payment = Money(7.00)
    #Maxmimum absolute value for agent's fixed pay"""

    # """Amount principal gets if contract is rejected"""
    reject_principal_pay = Money(0)

    reject_agent_pay = Money(1.00)

    # """Total return for single unit of agent's work effort"""
    agent_work_effort_base_return = Money(0.7)

    agent_return_share_choices = [[percent/100, '{}%'.format(percent)] for percent in range(10, 100+1, 10)]

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

def return_from_effort(effort):
    return effort*Constants.agent_work_effort_base_return

class Subsession(otree.models.BaseSubsession):

    name_in_url = 'principal_agent'


class Group(otree.models.BaseGroup):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    players_per_group = 2

    total_return = models.MoneyField(
        doc="""Total return from agent's effort = [Return for single unit of agent's work effort] * [Agent's work effort]"""
    )

    agent_fixed_pay = models.MoneyField(
        doc="""Amount offered as fixed pay to agent"""
    )

    agent_return_share = models.FloatField(
        doc="""Agent's share of total return""",
    )

    agent_work_effort = models.PositiveIntegerField(
        doc="""Agent's work effort, [1, 10]""",
    )


    agent_work_cost = models.MoneyField(
        doc="""Agent's cost of work effort"""
    )

    contract_accepted = models.NullBooleanField(
        doc="""Whether agent accepts proposal""",
        widget=widgets.RadioSelect(),
    )

    # choices
    def agent_fixed_pay_choices(self):
        return money_range(-Constants.max_fixed_payment, Constants.max_fixed_payment, 0.50)

    def agent_work_effort_choices(self):
        return range(1, 10+1)

    def agent_return_share_choices(self):
        return Constants.agent_return_share_choices

    def set_payoffs(self):
        principal = self.get_player_by_role('principal')
        agent = self.get_player_by_role('agent')

        if not self.contract_accepted:
            principal.payoff = Constants.reject_principal_pay
            agent.payoff = Constants.reject_agent_pay
        else:
            self.agent_work_cost = cost_from_effort(self.agent_work_effort)
            self.total_return = return_from_effort(self.agent_work_effort)

            money_to_agent = self.agent_return_share*self.total_return + self.agent_fixed_pay
            agent.payoff = money_to_agent - self.agent_work_cost
            principal.payoff = self.total_return - money_to_agent


class Player(otree.models.BasePlayer):

    # <built-in>
    group = models.ForeignKey(Group, null=True)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    def role(self):
        if self.id_in_group == 1:
            return 'principal'
        if self.id_in_group == 2:
            return 'agent'


