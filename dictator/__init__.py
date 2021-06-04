from otree.api import *



doc = """
One player decides how to divide a certain amount between himself and the other
player.
See: Kahneman, Daniel, Jack L. Knetsch, and Richard H. Thaler. "Fairness
and the assumptions of economics." Journal of business (1986):
S285-S300.
"""


class Constants(BaseConstants):
    name_in_url = 'dictator'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'dictator/instructions.html'
    # Initial amount allocated to the dictator
    endowment = cu(100)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    kept = models.CurrencyField(
        doc="""Amount dictator decided to keep for himself""",
        min=0,
        max=Constants.endowment,
        label="I will keep",
    )


class Player(BasePlayer):
    pass


# FUNCTIONS
def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p1.payoff = group.kept
    p2.payoff = Constants.endowment - group.kept


# PAGES
class Introduction(Page):
    pass


class Offer(Page):
    form_model = 'group'
    form_fields = ['kept']

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(offer=Constants.endowment - group.kept)


page_sequence = [Introduction, Offer, ResultsWaitPage, Results]
