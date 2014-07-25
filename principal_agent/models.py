# -*- coding: utf-8 -*-
"""Documentation at https://github.com/wickens/django-ptree-docs/wiki"""

from ptree.db import models
import ptree.models


doc = """
<p>
    In Principal Agent Game, there are two participants: One acts as the Agent and the other acts as the
    Principal. The Principal offers a contract to the Agent, which can be accepted or rejected.
</p>
<p>
    Source code <a href="https://github.com/wickens/ptree_library/tree/master/principal_agent">here</a>
</p>
"""


class Subsession(ptree.models.BaseSubsession):

    name_in_url = 'principal_agent'


class Treatment(ptree.models.BaseTreatment):
    subsession = models.ForeignKey(Subsession)

    fixed_payment = models.IntegerField(
        null=True,
        doc="""
        Principal's fixed pay range: given as a range e.g -300 > x < 300
        """
    )


class Match(ptree.models.BaseMatch):

    treatment = models.ForeignKey(Treatment)
    subsession = models.ForeignKey(Subsession)

    total_return = models.PositiveIntegerField(
        null=True,
        doc="""
        Total return from agent's effort = 70×(Agent Work effort)
        """
    )
    agent_fixed_pay = models.IntegerField(
        null=True,
        doc="""
        Amount offered as fixed pay to the agent.
        """
    )
    agent_return_share = models.PositiveIntegerField(
        null=True,
        doc="""
        Share of the total return
        """
    )
    agent_work_effort = models.PositiveIntegerField(
        null=True,
        doc="""
        Agent's work effort, ranging from 1-10: 1-lowest 10-highest
        """
    )
    agent_work_costs = models.PositiveIntegerField(
        null=True,
        doc="""
        Costs of work effort for agent
        """
    )
    DECISION_CHOICES = (('Accept', 'I Accept the Contract'),
                        ('Reject', 'I Reject the Contract'))

    decision = models.CharField(
        max_length=10, null=True, verbose_name='What is your decision?',
        choices=DECISION_CHOICES,
        doc="""Agent's decision"""
    )

    def calculate_total_return(self):
        self.total_return = self.agent_work_effort * 70

    def calculate_agent_work_cost(self):
        if self.agent_work_effort == 1:
            self.agent_work_costs = 0
        elif self.agent_work_effort == 2:
            self.agent_work_costs = 20
        elif self.agent_work_effort == 3:
            self.agent_work_costs = 40
        elif self.agent_work_effort == 4:
            self.agent_work_costs = 60
        elif self.agent_work_effort == 5:
            self.agent_work_costs = 90
        elif self.agent_work_effort == 6:
            self.agent_work_costs = 120
        elif self.agent_work_effort == 7:
            self.agent_work_costs = 160
        elif self.agent_work_effort == 8:
            self.agent_work_costs = 200
        elif self.agent_work_effort == 9:
            self.agent_work_costs = 250
        elif self.agent_work_effort == 10:
            self.agent_work_costs = 300

    participants_per_match = 2


class Participant(ptree.models.BaseParticipant):

    match = models.ForeignKey(Match, null = True)
    treatment = models.ForeignKey(Treatment, null = True)
    subsession = models.ForeignKey(Subsession)

    def set_payoff(self):
        # TODO: re-structure payoff calculations to avoid negative payoffs
        if self.match.decision == 'Reject':
            if self.index_among_participants_in_match == 1:
                self.payoff = 0
            else:
                self.payoff = 100
        else:
            self.match.calculate_agent_work_cost()
            self.match.calculate_total_return()

            if self.index_among_participants_in_match == 1:  # principal
                # [100% – Agent's return share in %]×(total return) – fixed payment
                # if payoff < 0 ..then make it 0 - no negative payoffs
                calc_payoff = (0.01 * (100 - self.match.agent_return_share) * self.match.total_return) - self.match.agent_fixed_pay
                self.payoff = calc_payoff if calc_payoff > 0 else 0
            else:  # agent
                # [Agent's return share in %]×(total return) + fixed payment – cost of the Agent's work effort
                # if payoff < 0 ..then make it 0 - no negative payoffs
                calc_payoff = (0.01*self.match.agent_return_share * self.match.total_return) + (self.match.agent_fixed_pay - self.match.agent_work_costs)
                self.payoff = calc_payoff if calc_payoff > 0 else 0


def treatments():

    return [Treatment.create(fixed_payment=700)]
