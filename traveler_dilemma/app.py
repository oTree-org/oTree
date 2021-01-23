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
Kaushik Basu's famous traveler's dilemma (
<a href="http://www.jstor.org/stable/2117865" target="_blank">
    AER 1994
</a>).
It is a 2-player game. The game is framed as a traveler's dilemma and intended
for classroom/teaching use.
"""


class Constants(BaseConstants):
    name_in_url = 'traveler_dilemma'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'traveler_dilemma/instructions.html'
    # Player's reward for the lowest claim"""
    adjustment_abs = c(2)
    # Player's deduction for the higher claim
    # The maximum claim to be requested
    max_amount = c(100)
    # The minimum claim to be requested
    min_amount = c(2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    lower_claim = models.CurrencyField()


class Player(BasePlayer):
    claim = models.CurrencyField(
        min=Constants.min_amount,
        max=Constants.max_amount,
        label='How much will you claim for your antique?',
        doc="""
        Each player's claim
        """,
    )
    adjustment = models.CurrencyField()


# FUNCTIONS
def set_payoffs(group: Group):
    p1, p2 = group.get_players()
    if p1.claim == p2.claim:
        group.lower_claim = p1.claim
        for p in [p1, p2]:
            p.payoff = group.lower_claim
            p.adjustment = c(0)
    else:
        if p1.claim < p2.claim:
            winner = p1
            loser = p2
        else:
            winner = p2
            loser = p1
        group.lower_claim = winner.claim
        winner.adjustment = Constants.adjustment_abs
        loser.adjustment = -Constants.adjustment_abs
        winner.payoff = group.lower_claim + winner.adjustment
        loser.payoff = group.lower_claim + loser.adjustment


def other_player(player: Player):
    return player.get_others_in_group()[0]


# PAGES
class Introduction(Page):
    pass


class Claim(Page):
    form_model = 'player'
    form_fields = ['claim']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player_claim=other_player(player).claim)


page_sequence = [Introduction, Claim, ResultsWaitPage, Results]
