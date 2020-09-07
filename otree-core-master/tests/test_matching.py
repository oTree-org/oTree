#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools

from mock import patch

import six
from django.core.management import call_command
from otree.models import Session

from .base import TestCase
from .multi_player_game import models as mpg_models

RANDOM_5_BY_3 = [
    [7, 12, 5],
    [13, 15, 1],
    [10, 9, 3],
    [2, 6, 8],
    [11, 14, 4],
]


class TestMatchPlayers(TestCase):

    def setUp(self):
        patcher = patch.object(mpg_models.Subsession, "before_session_starts")
        patcher.start()
        self.addCleanup(patcher.stop)

        call_command('create_session', 'multi_player_game', "15")
        self.session = Session.objects.get()
        self.subsession_1 = self.session.get_subsessions()[0]

    def assertCountEqual(self, *args, **kwargs):
        # In Python 2, this method is called ``assertItemsEqual``.
        if six.PY2:
            return self.assertItemsEqual(*args, **kwargs)
        return super(TestMatchPlayers, self).assertCountEqual(*args, **kwargs)

    def assert_groups_contains(self, groups, expected):
        actual = tuple(itertools.chain(*groups))
        self.assertCountEqual(actual, expected)

    def assert_groups_sizes(self, groups, expected):
        actual = [len(g) for g in groups]
        self.assertCountEqual(actual, expected)

    def assert_matchs(self, matching_function, validator):
        previous = []
        for subssn in self.session.get_subsessions():
            sizes = [
                len(g) for g in subssn.get_group_matrix()]
            new_group_matrix = matching_function(subssn)
            self.assert_groups_sizes(new_group_matrix, sizes)
            validator(
                new_group_matrix, subssn, subssn.get_players(),
                subssn.round_number, previous)
            previous.append(new_group_matrix)

    def assert_same_order_participants(self, actual, expected):
        actual = [p.participant for p in actual]
        expected = [p.participant for p in expected]
        self.assertListEqual(actual, expected)

    def test_set_group_matrix(self):

        desired_structure = RANDOM_5_BY_3
        subsession = self.subsession_1
        subsession.set_group_matrix(desired_structure)
        subsession.check_group_integrity()
        mat = subsession.get_group_matrix()
        for i, sublist in enumerate(mat):
            for j, player in enumerate(sublist):
                self.assertEqual(
                    player.id_in_subsession,
                    desired_structure[i][j]
                )

    def test_group_like_round(self):
        subsession_1 = self.subsession_1
        subsession_2 = subsession_1.in_round(2)
        desired_structure = RANDOM_5_BY_3
        subsession_1.set_group_matrix(desired_structure)
        subsession_2.group_like_round(1)
        mat = subsession_2.get_group_matrix()
        for i, sublist in enumerate(mat):
            for j, player in enumerate(sublist):
                self.assertEqual(
                    player.id_in_subsession,
                    desired_structure[i][j]
                )

    def test_group_randomly(self):
        subsession = self.subsession_1
        old_matrix = subsession.get_group_matrix()

        old_columns = {}
        old_rows = {}

        for i in range(len(old_matrix)):
            for j in range(len(old_matrix[i])):
                player = old_matrix[i][j]
                old_rows[player.id_in_subsession] = i
                old_columns[player.id_in_subsession] = j

        subsession.group_randomly()
        new_matrix = subsession.get_group_matrix()

        row_move_found = False
        col_move_found = False

        for i in range(len(new_matrix)):
            for j in range(len(new_matrix[i])):
                player = new_matrix[i][j]
                if old_rows[player.id_in_subsession] != i:
                    row_move_found = True
                if old_columns[player.id_in_subsession] != j:
                    col_move_found = True

        # we expect at least 1 player to have moved to a new row,
        # and 1 player to have moved to a new column

        self.assertTrue(row_move_found)
        self.assertTrue(col_move_found)

    def test_group_randomly_fixed(self):
        subsession_1 = self.subsession_1
        old_matrix = subsession_1.get_group_matrix()
        subsession_1.group_randomly(fixed_id_in_group=True)
        new_matrix = subsession_1.get_group_matrix()

        old_columns = list(zip(*old_matrix))
        new_columns = list(zip(*new_matrix))

        ordering_difference_found = False

        for col_index in range(len(new_columns)):
            old_col = old_columns[col_index]
            new_col = new_columns[col_index]
            self.assertEqual(set(old_col), set(new_col))
            if old_col != new_col:
                ordering_difference_found = True

        # in a matrix of 15 elements,
        # at least one reordering is basically guaranteed to occur
        # number of permutations: (5!)**3 = 1,728,000
        self.assertTrue(ordering_difference_found)
