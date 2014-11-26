# -*- coding: utf-8 -*-
import otree.views
import otree.views.concrete
import ultimatum.forms as forms
from ultimatum.utilities import PlayerMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from otree.common import currency
from ultimatum import models


class Start(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Start.html'

    def show_skip_wait(self):
        if all(p.visited for p in self.subsession.players):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_body_text(self):
        return _('Please wait for the other players.')


class Introduction(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Introduction.html'

    def variables_for_template(self):
        return {'endowment': currency(self.treatment.endowment),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'fair_payoff': currency(self.treatment.endowment/2.0)}


class Offer(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Offer.html'

    def get_form_class(self):
        return forms.OfferForm

    def show_skip_wait(self):
        if self.player.index_among_players_in_match == 1:
            return self.PageActions.show
        else:
            return self.PageActions.skip

    def variables_for_template(self):
        return {'endowment': currency(self.treatment.endowment),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'fair_payoff': currency(self.treatment.endowment/2.0)}


class Accept(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Accept.html'

    def get_form_class(self):
        return forms.AcceptForm

    def show_skip_wait(self):
        if self.player.index_among_players_in_match == 2 and not self.treatment.strategy:
            if self.match.amount_offered is None:
                return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.skip

    def wait_page_body_text(self):
        return _("You have been randomly assigned to be the responder. Please wait while the proposer makes the offer.")

    def variables_for_template(self):
        return {'endowment': currency(self.treatment.endowment),
                'amount_offered': currency(self.match.amount_offered),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'fair_payoff': currency(self.treatment.endowment/2.0)}


class AcceptHypothetical(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/AcceptHypothetical.html'

    def get_form_class(self):
        return forms.AcceptHypotheticalForm

    def show_skip_wait(self):
        if self.player.index_among_players_in_match == 2 and not self.treatment.strategy and self.treatment.hypothetical:
            if self.match.amount_offered is None:
                return self.PageActions.wait
            else:
                return self.PageActions.show
        else:
            return self.PageActions.skip

    def variables_for_template(self):
        return {'endowment': currency(self.treatment.endowment),
                'amount_offered': currency(self.match.amount_offered),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'fair_payoff': currency(self.treatment.endowment/2.0)}


class AcceptStrategy(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/AcceptStrategy.html'

    def get_form_class(self):
        return forms.AcceptStrategyForm

    def show_skip_wait(self):
        if self.player.index_among_players_in_match == 2 and self.treatment.strategy:
            return self.PageActions.show
        else:
            return self.PageActions.skip

    def variables_for_template(self):
        return {'endowment': currency(self.treatment.endowment),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'fair_payoff': currency(self.treatment.endowment/2.0)}


class Results(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Results.html'

    def show_skip_wait(self):
        if self.match.amount_offered is None:
            return self.PageActions.wait
        else:
            if self.treatment.strategy:
                if any(offer is None for offer in self.match.get_all_offer_fields()):
                    return self.PageActions.wait
                else:
                    return self.PageActions.show
            else:
                if self.match.offer_accepted is None:
                    return self.PageActions.wait
                else:
                    return self.PageActions.show

    def wait_page_body_text(self):
        return _('Waiting for the other player to finish.')

    def variables_for_template(self):
        if self.treatment.strategy:
            for (counter, response) in enumerate(self.match.get_all_offer_fields()):
                if response and self.match.amount_offered == self.treatment.offer_choices()[counter]:
                    self.match.offer_accepted = True
            if self.match.offer_accepted is not True:
                self.match.offer_accepted = False

        if self.player.payoff is None:
            self.player.set_payoff()

        return {'endowment': currency(self.treatment.endowment),
                'offer_choices': self.treatment.offer_choices_tuples(),
                'offer_choices_count': len(self.treatment.offer_choices()),
                'reject_payoff': currency(self.treatment.payoff_if_rejected),
                'fair_offer': currency(self.treatment.offer_choices()[len(self.treatment.offer_choices())/2]),
                'strategy': self.treatment.strategy,
                'player_index': self.player.index_among_players_in_match,
                'amount_offered': currency(self.match.amount_offered),
                'offer_accepted': self.match.offer_accepted,
                'payoff': currency(self.player.payoff)}


class Feedback(PlayerMixin, otree.views.Page):

    template_name = 'ultimatum/Feedback.html'

    def get_form_class(self):
        return forms.FeedbackForm


class ExperimenterIntroduction(ExperimenterMixin, otree.views.ExperimenterPage):

    template_name = 'ultimatum/ExperimenterPage.html'

    def show_skip_wait(self):
        if all(p.payoff is not None for p in self.subsession.players):
            return self.PageActions.show
        else:
            return self.PageActions.wait

    def wait_page_title_text(self):
        return _('Ultimatum Game: Experimenter Page')

    def wait_page_body_text(self):
        player_count = len(self.subsession.players)
        player_string = "players" if player_count > 1 else "player"
        matches_count = len(self.subsession.matches)
        matches_string = "matches" if matches_count > 1 else "match"
        return """All {} {} in {} {} have started playing the game.
                  As the experimenter in this game, you have no particular role to play.
                  This page will change once all players have been given a
                  payoff.""".format(player_count, player_string, matches_count, matches_string)

    def variables_for_template(self):
        return {'player_count': len(self.subsession.players)}


def pages():

    return [Introduction,
            Offer,
            Accept,
            AcceptHypothetical,
            AcceptStrategy,
            Results]


def experimenter_pages():

    return [ExperimenterIntroduction]
