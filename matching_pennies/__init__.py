from otree.api import *
c = Currency  # old name for currency; you can delete this.


doc = """
A demo of how rounds work in oTree, in the context of 'matching pennies'
"""


class Constants(BaseConstants):
    name_in_url = 'matching_pennies'
    players_per_group = 2
    num_rounds = 4
    stakes = cu(100)

    matcher_role = 'Matcher'
    mismatcher_role = 'Mismatcher'


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
    session = subsession.session
    import random

    if subsession.round_number == 1:
        paying_round = random.randint(1, Constants.num_rounds)
        session.vars['paying_round'] = paying_round
    if subsession.round_number == 3:
        # reverse the roles
        matrix = subsession.get_group_matrix()
        for row in matrix:
            row.reverse()
        subsession.set_group_matrix(matrix)
    if subsession.round_number > 3:
        subsession.group_like_round(3)


def set_payoffs(group: Group):
    subsession = group.subsession
    session = group.session

    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    for p in [p1, p2]:
        is_matcher = p.role == Constants.matcher_role
        p.is_winner = (p1.penny_side == p2.penny_side) == is_matcher
        if subsession.round_number == session.vars['paying_round'] and p.is_winner:
            p.payoff = Constants.stakes
        else:
            p.payoff = cu(0)


# PAGES
class Choice(Page):
    form_model = 'player'
    form_fields = ['penny_side']

    @staticmethod
    def vars_for_template(player: Player):
        return dict(player_in_previous_rounds=player.in_previous_rounds())


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class ResultsSummary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds

    @staticmethod
    def vars_for_template(player: Player):
        session = player.session

        player_in_all_rounds = player.in_all_rounds()
        return dict(
            total_payoff=sum([p.payoff for p in player_in_all_rounds]),
            paying_round=session.vars['paying_round'],
            player_in_all_rounds=player_in_all_rounds,
        )


page_sequence = [Choice, ResultsWaitPage, ResultsSummary]
