from otree.api import (
    Page,
    WaitPage,
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)


doc = """
This bargaining game involves 2 players. Each demands for a portion of some
available amount. If the sum of demands is no larger than the available
amount, both players get demanded portions. Otherwise, both get nothing.
"""


class Constants(BaseConstants):
    name_in_url = 'bargaining'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'bargaining/instructions.html'
    amount_shared = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_requests = models.CurrencyField()


class Player(BasePlayer):
    request = models.CurrencyField(
        doc="""
        Amount requested by this player.
        """,
        min=0,
        max=Constants.amount_shared,
        label="Please enter an amount from 0 to 100",
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    group.total_requests = sum([p.request for p in players])
    if group.total_requests <= Constants.amount_shared:
        for p in players:
            p.payoff = p.request
    else:
        for p in players:
            p.payoff = c(0)


def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES
class Introduction(Page):
    pass


class Request(Page):
    form_model = 'player'
    form_fields = ['request']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player_request=other_player(player).request)


page_sequence = [Introduction, Request, ResultsWaitPage, Results]
