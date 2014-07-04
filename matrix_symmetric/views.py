# -*- coding: utf-8 -*-
import ptree.views
import ptree.views.concrete
import matrix_symmetric.forms as forms
from matrix_symmetric.utilities import ParticipantMixin, ExperimenterMixin
from django.utils.translation import ugettext as _
from django.conf import settings
from ptree.common import currency

class MyPage(ParticipantMixin, ptree.views.Page):

    def show_skip_wait(self):
        return self.PageActions.show

    template_name = 'matrix_symmetric/MyView.html'

    def get_form_class(self):
        return forms.MyForm

    def variables_for_template(self):
        return {
            'my_variable_here': 1,
        }

    def after_valid_form_submission(self):
        """If all you need to do is save the form to the database,
        this can be left blank or omitted."""

class ExperimenterPage(ExperimenterMixin, ptree.views.ExperimenterPage):
    pass

def pages():
    return [
        MyPage
    ]