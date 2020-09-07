#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import decimal
import string

from django.utils import html
from django.template import Context, Template
from django.contrib.staticfiles.storage import staticfiles_storage

import six

import mock

from otree.common import Currency as c

from .base import TestCase
from six.moves import range


class TestFilters(TestCase):

    def parse(self, fragment):
        return Template('{% load otree_tags %}' + fragment)

    def render(self, fragment, context=None):
        if context is None:
            context = Context()
        if not isinstance(context, Context):
            context = Context(context)
        return self.parse(fragment).render(context)

    def test_monkey_patch_staticfiles_tag(self):
        with mock.patch.object(staticfiles_storage, "url") as url:
            self.render("{% load staticfiles %}{% static 'foo.jpg' %}")
            url.assert_called_once_with("foo.jpg")
        with mock.patch.object(staticfiles_storage, "url") as url:
            url.side_effect = ValueError("boom")
            with self.assertRaises(ValueError):
                self.render("{% load staticfiles %}{% static 'foo.jpg' %}")

    def test_abs_value(self):
        for value in [0, 1, random.random(), c(1)]:
            actual = self.render("{{value|abs}}", context={'value': value})
            expected = six.text_type(value)
            self.assertEquals(actual, expected)

            nvalue = -value
            expected = self.render("{{value|abs}}", context={'value': nvalue})
            self.assertEquals(actual, expected)

        with self.assertRaises(TypeError):
            self.render("{{value|abs}}", context={'value': "foo"})
        with self.assertRaises(TypeError):
            self.render("{{value|abs}}", context={'value': None})

    def test_as_repr(self):
        for value in [0, 1, random.random(), None, "something"]:
            rendered = self.render("{{value|repr}}", context={'value': value})
            expected = repr(value)
            if isinstance(value, six.string_types):
                expected = html.escape(expected)
            self.assertEquals(rendered, expected)

    def test_strip(self):
        for value in [0, 1, random.random(), c(1), None, "something   "]:
            if isinstance(value, six.string_types):
                actual = self.render(
                    "{{value|strip}}", context={'value': value})
                expected = value.strip()
                self.assertEquals(actual, expected)
            else:
                with self.assertRaises(AttributeError):
                    self.render("{{value|strip}}", context={'value': value})

    def test_is_instance(self):
        for value in [0, 1, random.random(), "something", ()]:
            tpl = "{{value|is_instance:'int,int,float,str'}}"
            actual = self.render(tpl, context={'value': value})
            expected = not isinstance(value, tuple)
            self.assertEquals(actual, six.text_type(expected))

    def test_is_numeric(self):
        numeric_types = (int, float, complex, decimal.Decimal)
        for value in [0, 1, random.random(), c(1), None, "something"]:
            actual = self.render(
                "{{value|is_numeric}}", context={'value': value})
            expected = isinstance(value, c) or isinstance(value, numeric_types)
            self.assertEquals(actual, six.text_type(expected))

    def test_is_text(self):
        for value in [0, 1, random.random(), c(1), None, "something"]:
            actual = self.render(
                "{{value|is_text}}", context={'value': value})
            expected = isinstance(value, six.string_types)
            self.assertEquals(actual, six.text_type(expected))

    def test_br(self):

        def random_string(numbers, letters, spaces):
            numbers = [
                random.choice(string.digits) for _ in six.moves.range(numbers)]
            letters = [
                random.choice(string.ascii_uppercase)
                for _ in six.moves.range(letters)]
            spaces = [" "] * spaces
            rstring = numbers + letters + spaces
            random.shuffle(rstring)
            return " ".join("".join(rstring).strip().split())

        linenos = random.randint(100, 200)
        lines = [random_string(20, 20, 20) for _ in range(linenos)]
        actual = self.render(
            "{{value|br}}", context={'value': "\n".join(lines)})
        expected = "<br>".join(lines)
        self.assertEquals(actual, expected)
