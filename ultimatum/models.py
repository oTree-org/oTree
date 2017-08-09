from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
Ultimatum game with two treatments: direct response and strategy method.
In the former, one player makes an offer and the other either accepts or rejects.
It comes in two flavors, with and without hypothetical questions about the second player's response to offers other than the one that is made.
In the latter treatment, the second player is given a list of all possible offers, and is asked which ones to accept or reject.
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1

    instructions_template = 'ultimatum/Instructions.html'

    endowment = c(100)
    payoff_if_rejected = c(0)
    offer_increment = c(10)

    offer_choices = currency_range(0, endowment, offer_increment)
    offer_choices_count = len(offer_choices)

    keep_give_amounts = []
    for offer in offer_choices:
        keep_give_amounts.append((offer, endowment - offer))


class Subsession(BaseSubsession):
    def creating_session(self):
        # randomize to treatments
        for g in self.get_groups():
            if 'treatment' in self.session.config:
                g.use_strategy_method = self.session.config['use_strategy_method']
            else:
                g.use_strategy_method = random.choice([True, False])


def question(amount):
    return 'Would you accept an offer of {}?'.format(c(amount))


class Group(BaseGroup):
    use_strategy_method = models.BooleanField(
        doc="""Whether this group uses strategy method"""
    )

    amount_offered = models.CurrencyField(choices=Constants.offer_choices)

    offer_accepted = models.BooleanField(
        doc="if offered amount is accepted (direct response method)"
    )

    # for strategy method
    response_0 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(0))
    response_10 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(10))
    response_20 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(20))
    response_30 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(30))
    response_40 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(40))
    response_50 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(50))
    response_60 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(60))
    response_70 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(70))
    response_80 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(80))
    response_90 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(90))
    response_100 = models.BooleanField(
        widget=widgets.RadioSelectHorizontal(), verbose_name=question(100))


    def set_payoffs(self):
        p1, p2 = self.get_players()

        if self.use_strategy_method:
            self.offer_accepted = getattr(self, 'response_{}'.format(
                int(self.amount_offered)))

        if self.offer_accepted:
            p1.payoff = Constants.endowment - self.amount_offered
            p2.payoff = self.amount_offered
        else:
            p1.payoff = Constants.payoff_if_rejected
            p2.payoff = Constants.payoff_if_rejected


class Player(BasePlayer):
    pass
