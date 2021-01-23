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
In a common value auction game, players simultaneously bid on the item being
auctioned.<br/>
Prior to bidding, they are given an estimate of the actual value of the item.
This actual value is revealed after the bidding.<br/>
Bids are private. The player with the highest bid wins the auction, but
payoff depends on the bid amount and the actual value.<br/>
"""


class Constants(BaseConstants):
    name_in_url = 'common_value_auction'
    players_per_group = None
    num_rounds = 1
    instructions_template = 'common_value_auction/instructions.html'
    min_allowable_bid = c(0)
    max_allowable_bid = c(10)
    # Error margin for the value estimates shown to the players
    estimate_error_margin = c(1)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    item_value = models.CurrencyField(
        doc="""Common value of the item to be auctioned, random for treatment"""
    )
    highest_bid = models.CurrencyField()


class Player(BasePlayer):
    item_value_estimate = models.CurrencyField(
        doc="""Estimate of the common value, may be different for each player"""
    )
    bid_amount = models.CurrencyField(
        min=Constants.min_allowable_bid,
        max=Constants.max_allowable_bid,
        doc="""Amount bidded by the player""",
        label="Bid amount",
    )
    is_winner = models.BooleanField(
        initial=False, doc="""Indicates whether the player is the winner"""
    )


# FUNCTIONS
def creating_session(subsession: Subsession):
    for g in subsession.get_groups():
        import random

        item_value = random.uniform(
            Constants.min_allowable_bid, Constants.max_allowable_bid
        )
        g.item_value = round(item_value, 1)


def set_winner(group: Group):
    import random

    players = group.get_players()
    group.highest_bid = max([p.bid_amount for p in players])
    players_with_highest_bid = [p for p in players if p.bid_amount == group.highest_bid]
    winner = random.choice(
        players_with_highest_bid
    )  # if tie, winner is chosen at random
    winner.is_winner = True
    for p in players:
        set_payoff(p)


def generate_value_estimate(group: Group):
    import random

    minimum = group.item_value - Constants.estimate_error_margin
    maximum = group.item_value + Constants.estimate_error_margin
    estimate = random.uniform(minimum, maximum)
    estimate = round(estimate, 1)
    if estimate < Constants.min_allowable_bid:
        estimate = Constants.min_allowable_bid
    if estimate > Constants.max_allowable_bid:
        estimate = Constants.max_allowable_bid
    return estimate


def set_payoff(player: Player):
    group = player.group

    if player.is_winner:
        player.payoff = group.item_value - player.bid_amount
        if player.payoff < 0:
            player.payoff = 0
    else:
        player.payoff = 0


# PAGES
class Introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        group = player.group

        player.item_value_estimate = generate_value_estimate(group)


class Bid(Page):
    form_model = 'player'
    form_fields = ['bid_amount']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_winner'


class Results(Page):
    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(is_greedy=group.item_value - player.bid_amount < 0)


page_sequence = [Introduction, Bid, ResultsWaitPage, Results]
