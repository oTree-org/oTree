from otree.api import *



doc = """
In Cournot competition, firms simultaneously decide the units of products to
manufacture. The unit selling price depends on the total units produced. In
this implementation, there are 2 firms competing for 1 period.
"""


class C(BaseConstants):
    NAME_IN_URL = 'cournot'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'cournot/instructions.html'
    # Total production capacity of all players
    TOTAL_CAPACITY = 60
    MAX_UNITS_PER_PLAYER = int(TOTAL_CAPACITY / PLAYERS_PER_GROUP)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    unit_price = models.CurrencyField()
    total_units = models.IntegerField(doc="""Total units produced by all players""")


class Player(BasePlayer):
    units = models.IntegerField(
        min=0,
        max=C.MAX_UNITS_PER_PLAYER,
        doc="""Quantity of units to produce""",
        label="How many units will you produce (from 0 to 30)?",
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    group.total_units = sum([p.units for p in players])
    group.unit_price = C.TOTAL_CAPACITY - group.total_units
    for p in players:
        p.payoff = group.unit_price * p.units


def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES
class Introduction(Page):
    pass


class Decide(Page):
    form_model = 'player'
    form_fields = ['units']


class ResultsWaitPage(WaitPage):
    body_text = "Waiting for the other participant to decide."
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player_units=other_player(player).units)


page_sequence = [Introduction, Decide, ResultsWaitPage, Results]
