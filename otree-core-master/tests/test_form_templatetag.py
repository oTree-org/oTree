#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.template import Context
from django.template import Template

import otree.db.models
import otree.forms

from .base import TestCase
from .models import SimplePlayer


class SimplePlayerForm(otree.forms.ModelForm):
    class Meta:
        model = SimplePlayer
        fields = ('name', 'age',)


class FormFieldTestMixin(TestCase):
    def setUp(self):
        self.simple_player = SimplePlayer.objects.create()

    def parse(self, fragment):
        return Template('{% load otree_tags %}' + fragment)

    def render(self, fragment, context=None):
        if context is None:
            context = Context()
        if not isinstance(context, Context):
            context = Context(context)
        return self.parse(fragment).render(context)


class CheckAllFieldsAreRenderedTests(FormFieldTestMixin, TestCase):
    def test_rendering_works(self):
        class OnlyNameForm(otree.forms.ModelForm):
            class Meta:
                model = SimplePlayer
                fields = ('name',)

        form = OnlyNameForm(instance=self.simple_player)
        templatename = 'otree/includes/_formfield_is_missing_error.html'
        with self.assertTemplateNotUsed(template_name=templatename):
            result = self.render(
                '''
                {% pageform form using %}
                    {% formfield player.name %}
                {% endpageform %}
                ''',
                context={'form': form, 'player': self.simple_player})

        self.assertTrue('<input' in result)
        self.assertTrue('name="name"' in result)

        form = SimplePlayerForm(instance=self.simple_player)
        with self.assertTemplateNotUsed(
                'otree/includes/_formfield_is_missing_error.html'):
            result = self.render(
                '''
                {% pageform form using %}
                    {% formfield player.name %}
                    {% formfield player.age %}
                {% endpageform %}
                ''',
                context={'form': form, 'player': self.simple_player})

    def test_rendering_complains_when_not_all_fields_are_rendered(self):
        form = SimplePlayerForm(
            # The missing field error only shows up if there are errors on the
            # form. So we construct one.
            data={'age': 'no number'},
            instance=self.simple_player)
        with self.assertTemplateUsed(
                'otree/includes/_formfield_is_missing_error.html'):
            tpl = (
                '{% pageform form using %}'
                '{% formfield player.name %}'
                '{% endpageform %}'
                '{% include "otree/includes/debug_info.html" %}'
            )
            self.render(
                tpl, context={'form': form, 'player': self.simple_player}
            )
