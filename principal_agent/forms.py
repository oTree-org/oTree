# -*- coding: utf-8 -*-
import principal_agent.models as models
from principal_agent._builtin import Form
import otree.forms
from django import forms
from otree.common import money_range, Money

class ContractForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_fixed_pay', 'agent_return_share']

    def labels(self):
        return {
            'agent_fixed_pay': "Agent's Fixed Pay",
            'agent_return_share': "Agent's Return Share"
        }

    def choices(self):
        return {
            'agent_fixed_pay': money_range(-self.treatment.max_fixed_payment, self.treatment.max_fixed_payment, 0.50),
        }

class DecisionForm(Form):

    class Meta:
        model = models.Match
        fields = ['contract_accepted']

    def labels(self):
        return {
            'contract_accepted': "Do you accept or reject the contract?",
        }


class WorkEffortForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_work_effort']

    def labels(self):
        return {
            'agent_work_effort': 'Your work effort on the Contract?'
        }