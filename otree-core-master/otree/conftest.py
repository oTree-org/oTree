#!/usr/bin/env python
# -*- coding: utf-8 -*-

# for py.test.
# this doesnt work if the module is under otree.bots, so i put it here
from otree.session import SESSION_CONFIGS_DICT


def pytest_addoption(parser):
    parser.addoption("--session_config_name")
    parser.addoption("--num_participants")
    parser.addoption("--preserve_data", action='store_true')


def pytest_generate_tests(metafunc):
    # if the test function has a parameter called session_config_name
    if 'session_config_name' in metafunc.fixturenames:
        option = metafunc.config.option
        session_config_name = option.session_config_name
        if session_config_name:
            session_config_names = [session_config_name]
        else:
            session_config_names = SESSION_CONFIGS_DICT.keys()
        num_participants = option.num_participants
        if num_participants:
            num_participants = int(num_participants)
        preserve_data = option.preserve_data

        params = [
            [name, num_participants, preserve_data]
            for name in session_config_names]
        metafunc.parametrize(
            "session_config_name,num_participants,preserve_data", params)
