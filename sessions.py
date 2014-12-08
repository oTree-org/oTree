# -*- coding: utf-8 -*-
from __future__ import division

import otree.session


class SessionType(otree.session.SessionType):

    # defaults that can be overridden by an individual SessionType below
    money_per_point = 1.00
    demo_enabled = True
    fixed_pay = 10.00
    num_bots = 12
    doc = ""
    assign_to_groups_on_the_fly = False
    show_on_demo_page = True


def session_types():

    return [
        SessionType(
            name='demo_game',
            display_name="Demo Game",
            num_demo_participants=1,
            subsession_apps=['demo_game'],
        ),
        SessionType(
            name='public_goods',
            display_name="Public Goods",
            num_demo_participants=3,
            subsession_apps=['public_goods', 'payment_info'],
        ),
        SessionType(
            name='prisoner',
            display_name="Prisoner's Dilemma",
            num_demo_participants=2,
            subsession_apps=['prisoner', 'survey_sample', 'payment_info'],
        ),
        SessionType(
            name='cournot_competition',
            display_name="Cournot Competition",
            num_demo_participants=2,
            subsession_apps=[
                'cournot_competition', 'survey_sample', 'payment_info'
            ],
        ),
        SessionType(
            name='trust',
            display_name="Trust Game",
            num_demo_participants=2,
            subsession_apps=['trust', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='ultimatum',
            display_name="Ultimatum",
            num_demo_participants=2,
            subsession_apps=['ultimatum', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='dictator',
            display_name="Dictator Game",
            num_demo_participants=2,
            subsession_apps=['dictator', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='matching_pennies',
            display_name="Matching Pennies",
            num_demo_participants=2,
            subsession_apps=[
                'matching_pennies', 'survey_sample', 'payment_info'
            ],
        ),
        SessionType(
            name='traveler_dilemma',
            display_name="Traveler's Dilemma",
            num_demo_participants=2,
            subsession_apps=['traveler_dilemma', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='survey',
            display_name="Survey",
            num_demo_participants=1,
            subsession_apps=['survey'],
        ),
        SessionType(
            name='bargaining',
            display_name="Bargaining Game",
            num_demo_participants=2,
            subsession_apps=['bargaining', 'payment_info'],
        ),
        SessionType(
            name='beauty',
            display_name="Beauty Contest",
            num_demo_participants=5,
            num_bots=5,
            subsession_apps=['beauty', 'survey_sample', 'payment_info'],
        ),
        SessionType(
            name='common_value_auction',
            display_name="Common Value Auction",
            num_demo_participants=3,
            subsession_apps=['common_value_auction', 'payment_info'],
        ),
        SessionType(
            name='stackelberg_competition',
            display_name="Stackelberg Competition",
            money_per_point=0.01,
            num_demo_participants=2,
            subsession_apps=[
                'stackelberg_competition', 'survey_sample', 'payment_info'
            ],
        ),
        SessionType(
            name='vickrey_auction',
            display_name="Vickrey Auction",
            num_demo_participants=3,
            subsession_apps=['vickrey_auction', 'payment_info'],
        ),
        SessionType(
            name='volunteer_dilemma',
            display_name="Volunteer's Dilemma",
            num_demo_participants=3,
            subsession_apps=['volunteer_dilemma', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='bertrand_competition',
            display_name="Bertrand Competition",
            num_demo_participants=2,
            subsession_apps=[
                'bertrand_competition', 'feedback', 'payment_info'
            ],
        ),
        SessionType(
            name='principal_agent',
            display_name="Principal Agent",
            num_demo_participants=2,
            subsession_apps=['principal_agent', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='stag_hunt',
            display_name="Stag Hunt",
            num_demo_participants=2,
            subsession_apps=['stag_hunt', 'survey_sample', 'payment_info'],
        ),
        SessionType(
            name='battle_of_the_sexes',
            display_name="Battle of the Sexes",
            num_demo_participants=2,
            subsession_apps=[
                'battle_of_the_sexes', 'survey_sample', 'payment_info'
            ],
        ),
        SessionType(
            name='asset_market',
            display_name="Asset Market",
            num_demo_participants=2,
            subsession_apps=['asset_market', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='lemon_market',
            display_name="Lemon Market",
            num_demo_participants=3,
            subsession_apps=['lemon_market', 'feedback', 'payment_info'],
        ),
        SessionType(
            name='real_effort',
            display_name="Real-effort transcription task",
            num_demo_participants=1,
            subsession_apps=[
                'real_effort',
            ],
        ),
    ]


demo_page_intro_text = """
<ul>
    <li>
        <a href="https://github.com/oTree-org/otree" target="_blank">
            Source code
        </a> for the below games.
    </li>
    <li>
        <a href="http://www.otree.org/" target="_blank">
            oTree homepage
        </a>.
    </li>
</ul>
<p>
    Below are various games implemented with oTree. These games are all open
    source, and you can modify them as you wish to create your own variations.
    Click one to learn more and play.
</p>
"""
