# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-otree-docs/wiki"""

from otree.db import models
import otree.models


doc = """
<p>
    In Principal Agent Game, there are two players: One acts as the Agent and the other acts as the
    Principal. The Principal offers a contract to the Agent, which can be accepted or rejected.
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

    fixed_payment = models.MoneyField(
        default=7.00,
        doc="""
        Principal's fixed pay range: given as a range e.g -300 > x < 300
        """
    )


class Match(otree.models.BaseMatch):

    # <built-in>
    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)
    # </built-in>

    total_return = models.MoneyField(
        default=None,
        doc="""
        Total return from agent's effort = 70×(Agent Work effort)
        """
    )
    agent_fixed_pay = models.MoneyField(
        default=None,
        doc="""
        Amount offered as fixed pay to the agent.
        """
    )
    agent_return_share = models.PositiveIntegerField(
        default=None,
        doc="""
        Share of the total return
        """
    )
    agent_work_effort = models.PositiveIntegerField(
        default=None,
        doc="""
        Agent's work effort, ranging from 1-10: 1-lowest 10-highest
        """
    )
    agent_work_costs = models.MoneyField(
        default=None,
        doc="""
        Costs of work effort for agent
        """
    )

    decision = models.CharField(
        default=None, verbose_name='What is your decision?',
        choices=['Accept', 'Reject'],
        doc="""Agent's decision"""
    )

    def calculate_total_return(self):
        self.total_return = self.agent_work_effort * 70

    def calculate_agent_work_cost(self):
        efforts_to_costs = {
            1: 0,
            2: 20,
            3: 40,
            4: 60,
            5: 90,
            6: 120,
            7: 160,
            8: 200,
            9: 250,
            10: 300
        }

        self.agent_work_costs = efforts_to_costs[self.agent_work_effort]

    players_per_match = 2

    def set_payoffs(self):
        '''FIXME: need to review if this is correct'''
        # TODO: re-structure payoff calculations to avoid negative payoffs
        principal = self.get_player_by_role('principal')
        agent = self.get_player_by_role('agent')

        if self.decision == 'Reject':
            principal.payoff = 0
            agent.payoff = 100
        else:
            self.calculate_agent_work_cost()
            self.calculate_total_return()

            # [100% – Agent's return share in %]×(total return) – fixed payment
            principal.payoff = max(0, (0.01 * (100 - self.match.agent_return_share) * self.match.total_return) - self.match.agent_fixed_pay)
            # [Agent's return share in %]×(total return) + fixed payment – cost of the Agent's work effort
            # if payoff < 0 ..then make it 0 - no negative payoffs
            agent.payoff = max(0, 0.01*self.agent_return_share * self.total_return + self.agent_fixed_pay - self.agent_work_costs)


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