# -*- coding: utf-8 -*-

import random

from django.template import Template, Context

import six

from otree.common import Currency as c

from .base import TestCase


class CurrencyTests(TestCase):

    def test_currency_non_ascii_character(self):
        # https://github.com/oTree-org/otree-core/issues/387

        class TestC(c):
            CODE = 'EUR'

        money = TestC(23)
        template = Template('''{{money}}''')
        ctx = Context({"money": money})
        rendered = template.render(ctx)
        self.assertEquals(rendered, six.text_type(money))

    def test_string_format(self):

        class TestC(c):
            CODE = 'USD'

        money = TestC(23)
        self.assertEqual('{}'.format(money), '$23.00')

    def test_currency_unary_operator(self):
        #  https://github.com/oTree-org/otree-core/issues/391
        msg = "Currency operator '{}' fail"
        for money in [c(-random.random()), c(random.random()), c(0)]:
            self.assertIsInstance(abs(money), c, msg.format("abs()"))
            self.assertIsInstance(-money, c, msg.format("-VALUE"))
            self.assertIsInstance(+money, c, msg.format("+VALUE"))

    def test_currency_operator(self):
        msg = "Currency operator '{}' fail"
        for money in [c(-random.random()), c(random.random()), c(0)]:
            money = money + 1
            self.assertIsInstance(money, c, msg.format("+"))
            money = money - 1
            self.assertIsInstance(money, c, msg.format("-"))
            money = money / 1
            self.assertIsInstance(money, c, msg.format("/"))
            money = money * 1
            self.assertIsInstance(money, c, msg.format("*"))
            money = money ** 1
            self.assertIsInstance(money, c, msg.format("**"))
            money = money // 1
            self.assertIsInstance(money, c, msg.format("//"))

    def test_currency_inplace_operator(self):
        msg = "Currency operator '{}' fail"
        for money in [c(-random.random()), c(random.random()), c(0)]:
            money += 1
            self.assertIsInstance(money, c, msg.format("+="))
            money -= 1
            self.assertIsInstance(money, c, msg.format("-="))
            money /= 1
            self.assertIsInstance(money, c, msg.format("/="))
            money *= 1
            self.assertIsInstance(money, c, msg.format("*="))
            money **= 1
            self.assertIsInstance(money, c, msg.format("**="))
            money //= 1
            self.assertIsInstance(money, c, msg.format("//="))
