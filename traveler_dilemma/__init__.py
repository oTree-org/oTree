from otree.api import *


doc = """
Kaushik Basu's famous traveler's dilemma (
<a href="http://www.jstor.org/stable/2117865" target="_blank">
    AER 1994
</a>).
It is a 2-player game. The game is framed as a traveler's dilemma and intended
for classroom/teaching use.
"""


class C(BaseConstants):
    NAME_IN_URL = 'traveler_dilemma'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'traveler_dilemma/instructions.html'
    # Player's reward for the lowest claim"""
    ADJUSTMENT_ABS = cu(2)
    # Player's deduction for the higher claim
    # The maximum claim to be requested
    MAX_AMOUNT = cu(100)
    # The minimum claim to be requested
    MIN_AMOUNT = cu(2)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    lower_claim = models.CurrencyField()


class Player(BasePlayer):
    claim = models.CurrencyField(
        min=C.MIN_AMOUNT,
        max=C.MAX_AMOUNT,
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
            p.adjustment = cu(0)
    else:
        if p1.claim < p2.claim:
            winner = p1
            loser = p2
        else:
            winner = p2
            loser = p1
        group.lower_claim = winner.claim
        winner.adjustment = C.ADJUSTMENT_ABS
        loser.adjustment = -C.ADJUSTMENT_ABS
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
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        return dict(other_player_claim=other_player(player).claim)


page_sequence = [Introduction, Claim, ResultsWaitPage, Results]
