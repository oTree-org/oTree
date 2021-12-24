from otree.api import *



doc = """
Each player decides if to free ride or to volunteer from which all will
benefit.
See: Diekmann, A. (1985). Volunteer's dilemma. Journal of Conflict
Resolution, 605-610.
"""


class C(BaseConstants):
    NAME_IN_URL = 'volunteer_dilemma'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    INSTRUCTIONS_TEMPLATE = 'volunteer_dilemma/instructions.html'
    NUM_OTHER_PLAYERS = PLAYERS_PER_GROUP - 1
    # """Payoff for each player if at least one volunteers"""
    GENERAL_BENEFIT = cu(100)
    # """Cost incurred by volunteering player"""
    VOLUNTEER_COST = cu(40)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    num_volunteers = models.IntegerField()


class Player(BasePlayer):
    volunteer = models.BooleanField(
        label='Do you wish to volunteer?', doc="""Whether player volunteers"""
    )


# FUNCTIONS
def set_payoffs(group: Group):
    players = group.get_players()
    group.num_volunteers = sum([p.volunteer for p in players])
    if group.num_volunteers > 0:
        baseline_amount = C.GENERAL_BENEFIT
    else:
        baseline_amount = cu(0)
    for p in players:
        p.payoff = baseline_amount
        if p.volunteer:
            p.payoff -= C.VOLUNTEER_COST


# PAGES
class Introduction(Page):
    pass


class Decision(Page):
    form_model = 'player'
    form_fields = ['volunteer']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    pass


page_sequence = [Introduction, Decision, ResultsWaitPage, Results]
