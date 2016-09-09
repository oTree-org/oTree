from otree.api import Currency as c, currency_range, SubmissionMustFail
from . import views
from ._builtin import Bot
from .models import Constants


class PlayerBot(Bot):

    def play_round(self):
        # must reject transcription that is too inaccurate
        yield SubmissionMustFail(views.Transcribe, {'transcribed_text': 'foo'})

        transcription = Constants.reference_texts[self.subsession.round_number - 1]
        add_char = Constants.allowed_error_rates[self.subsession.round_number - 1] > 0
        if add_char:
            # add a 1-char error, should still be fine
            transcription += 'a'

        yield (views.Transcribe, {'transcribed_text': transcription})


        for value in [
            self.player.levenshtein_distance,
            self.player.transcribed_text,
            self.player.payoff
        ]:
            assert value != None

        if add_char:
            assert self.player.levenshtein_distance == 1
        else:
            assert self.player.levenshtein_distance == 0

        if self.subsession.round_number == Constants.num_rounds:
            # final page should print lengths of all reference texts
            for ref_text in Constants.reference_texts:
                assert str(len(ref_text)) in self.html

            # because of add_char, there should be an error in at least 1 round
            assert any(p.levenshtein_distance > 0 for p in self.player.in_all_rounds())