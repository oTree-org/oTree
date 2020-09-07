#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Multiple algorithms for sorting oTree players

"""

# =============================================================================
# IMPORTS
# =============================================================================

import itertools
import random

from six.moves import range

# =============================================================================
# MATCH
# =============================================================================


def by_rank(ranked_list, players_per_group):
    ppg = players_per_group
    players = ranked_list
    group_matrix = []
    for i in range(0, len(players), ppg):
        group_matrix.append(players[i:i + ppg])
    return group_matrix


def randomly(group_matrix, fixed_id_in_group=False):
    """Random Uniform distribution of players in every group"""

    players = list(itertools.chain.from_iterable(group_matrix))
    sizes = [len(group) for group in group_matrix]
    if sizes and any(size != sizes[0] for size in sizes):
        raise ValueError(
            'This algorithm does not work with unevenly sized groups')
    players_per_group = sizes[0]

    if fixed_id_in_group:
        group_matrix = [list(col) for col in zip(*group_matrix)]
        for column in group_matrix:
            random.shuffle(column)
        return list(zip(*group_matrix))
    else:
        random.shuffle(players)
        return by_rank(players, players_per_group)
