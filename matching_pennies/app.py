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
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""


class Constants(BaseConstants):
    name_in_url = 'matching_pennies'
    players_per_group = 2
    num_rounds = 4
    stakes = c(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    penny_side = models.StringField(
        choices=[['Heads', 'Heads'], ['Tails', 'Tails']],
        widget=widgets.RadioSelect,
        label="I choose:",
    )
    is_winner = models.BooleanField()


# FUNCTIONS
def creating_session(subsession: Subsession):
    import random

    if subsession.round_number == 1:
        paying_round = random.randint(1, Constants.num_rounds)
        subsession.session.vars['paying_round'] = paying_round
    if subsession.round_number == 3:
        # reverse the roles
        matrix = subsession.get_group_matrix()
        for row in matrix:
            row.reverse()
        subsession.set_group_matrix(matrix)
    if subsession.round_number > 3:
        subsession.group_like_round(3)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    is_match = p1.penny_side == p2.penny_side
    for p in [p1, p2]:
        # a simpler way to write these 4 lines would be:
        # p.is_winner = (p.is_matcher() == is_match)
        if p.is_matcher() == is_match:
            p.is_winner = True
        else:
            p.is_winner = False
        if group.subsession.round_number == group.session.vars['paying_round'] and p.is_winner:
            p.payoff = Constants.stakes
        else:
            p.payoff = c(0)


def is_matcher(player: Player):
    return player.id_in_group == 1


# PAGES
class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'


class ResultsSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        player_in_all_rounds = player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=player.session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )


page_sequence = [Choice, ResultsWaitPage, ResultsSummary]
