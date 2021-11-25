from otree.api import *



doc = """
2 firms complete in a market by setting prices for homogenous goods.
See "Kruse, J. B., Rassenti, S., Reynolds, S. S., & Smith, V. L. (1994).
Bertrand-Edgeworth competition in experimental markets.
Econometrica: Journal of the Econometric Society, 343-371."
"""


class C(BaseConstants):
    PLAYERS_PER_GROUP = 2
    NAME_IN_URL = 'bertrand'
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'bertrand/instructions.html'
    MAXIMUM_PRICE = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    winning_price = models.CurrencyField()


class Player(BasePlayer):
    price = models.CurrencyField(
        min=0,
        max=C.MAXIMUM_PRICE,
        doc="""Price player offers to sell product for""",
        label="Please enter an amount from 0 to 100 as your price",
    )
    is_winner = models.BooleanField()


# FUNCTIONS
def set_payoffs(group: Group):
    import random

    players = group.get_players()
    group.winning_price = min([p.price for p in players])
    winners = [p for p in players if p.price == group.winning_price]
    winner = random.choice(winners)
    for p in players:
        if p == winner:
            p.is_winner = True
            p.payoff = p.price
        else:
            p.is_winner = False
            p.payoff = cu(0)


# PAGES
class Introduction(Page):
    pass


class Decide(Page):
    form_model = 'player'
    form_fields = ['price']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Introduction, Decide, ResultsWaitPage, Results]
