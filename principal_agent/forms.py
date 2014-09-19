# -*- coding: utf-8 -*-
import principal_agent.models as models
from principal_agent._builtin import Form
from otree.common import money_range, Money
from django import forms


class ContractForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_fixed_pay',
                  'agent_return_share']

    def labels(self):
        return {'agent_fixed_pay': "Fixed payment:",
                'agent_return_share': "Return share:"}

    def choices(self):
        return {'agent_fixed_pay': money_range(-self.treatment.max_fixed_payment, self.treatment.max_fixed_payment, 0.50)}


class DecisionForm(Form):

    class Meta:
        model = models.Match
        fields = ['contract_accepted']
        widgets = {'contract_accepted': forms.RadioSelect()}

    def labels(self):
        return {'contract_accepted': "Do you accept the contract?"}


class WorkEffortForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_work_effort']

    def labels(self):
        return {'agent_work_effort': 'Effort level:'}
