# -*- coding: utf-8 -*-
"""Documentation at https://github.com/oTree-org/otree/wiki"""
from __future__ import division
from otree.db import models
import otree.models
from otree.common import Money


doc = """
<p>
    In Principal Agent Game, there are two players: One acts as the Agent and the other acts as the
    Principal. The Principal offers a contract to the Agent, which can be accepted or rejected.
</p>

<p>
    This game is described <a href="www.nottingham.ac.uk/cedex/documents/papers/2006-04.pdf">here</a>.
</p>

<p>
    Source code <a href="https://github.com/oTree-org/oTree/tree/master/principal_agent">here</a>.
</p>
"""


class Subsession(otree.models.BaseSubsession):

    name_in_url = 'principal_agent'


class Treatment(otree.models.BaseTreatment):

    # <built-in>
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    max_fixed_payment = models.MoneyField(
        default=7.00,
        doc="""
        Maxmimum absolute value for agent's fixed pay
        """
    )

    reject_principal_pay = models.MoneyField(
        default=0,
        doc='Amount the principal gets if the contract is rejected'
    )

    reject_agent_pay = models.MoneyField(
        default=1.00,
        doc='Amount the agent gets if the contract is rejected'
    )

    def cost_from_effort(self, effort):
        costs = {
            1: 0,
            2: .20,
            3: .40,
            4: .60,
            5: .90,
            6: 1.20,
            7: 1.60,
            8: 2.00,
            9: 2.50,
            10: 3.00
        }

        return Money(costs[effort])

    def return_from_effort(self, effort):
        return effort*Money(0.70)

class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_return = models.MoneyField(
        default=None,
        doc="""
        Total return from agent's effort = $0.70×(Agent Work effort)
        """
    )
    agent_fixed_pay = models.MoneyField(
        default=None,
        doc="""
        Amount offered as fixed pay to the agent.
        """
    )

    RETURN_SHARE_CHOICES = []
    for percent in range(10,100+1,10):
        RETURN_SHARE_CHOICES.append([percent/100, '{}%'.format(percent)])

    agent_return_share = models.FloatField(
        default=None,
        doc="""
        Share of the total return
        """,
        choices=RETURN_SHARE_CHOICES,
    )

    agent_work_effort = models.PositiveIntegerField(
        default=None,
        doc="""
        Agent's work effort, ranging from 1-10: 1-lowest 10-highest
        """,
        choices=range(1,10+1)
    )
    agent_work_cost = models.MoneyField(
        default=None,
        doc="""
        Costs of work effort for agent
        """
    )

    contract_accepted = models.NullBooleanField(
        default=None, verbose_name='Do you accept the contract?',
        doc="""Whether the agent accepts the proposal"""
    )

    players_per_match = 2

    def set_payoffs(self):
        principal = self.get_player_by_role('principal')
        agent = self.get_player_by_role('agent')

        if not self.contract_accepted:
            principal.payoff = self.treatment.reject_principal_pay
            agent.payoff = self.treatment.reject_agent_pay
        else:
            self.agent_work_cost = self.treatment.cost_from_effort(self.agent_work_effort)
            self.total_return = self.treatment.return_from_effort(self.agent_work_effort)

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