# -*- coding: utf-8 -*-
import principal_agent.models as models
from principal_agent.utilities import Form
import ptree.forms


class ContractForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_fixed_pay', 'agent_return_share']

    def labels(self):
        return {
            'agent_fixed_pay': "Agent's Fixed Pay",
            'agent_return_share': "Agent's Return Share"
        }

    def agent_fixed_pay_error_message(self, value):
        if (value < -self.treatment.fixed_payment) or (value > self.treatment.fixed_payment):
            return 'Agent fixed pay should be between -{} and {}.'.format(self.treatment.fixed_payment, self.treatment.fixed_payment)

    def agent_return_share_error_message(self, value):
        if (value < 0) or (value > 100) or (value not in range(0, 101, 10)):
            return 'Agent return share should be in multiples of 10 .i.e 10%, 20%..,100%.'


class DecisionForm(Form):

    class Meta:
        model = models.Match
        fields = ['decision']

    def labels(self):
        return {
            'decision': "Accept or Reject?",
        }


class WorkEffortForm(Form):

    class Meta:
        model = models.Match
        fields = ['agent_work_effort']

    def labels(self):
        return {
            'agent_work_effort': 'Your work effort on the Contract?'
        }

    def agent_work_effort_error_message(self, value):
        if (value < 1) or (value > 10):
            return 'Work effort should be between 1-Lowest and 10 - highest.'