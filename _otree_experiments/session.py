from otree.session import SessionType
import os

def session_types():

    return [
        SessionType(
            name='Public Goods',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=4,
            subsession_apps=['public_goods', 'lab_results'],
            doc=""""""
        ),

        SessionType(
            name="Prisoner Dilemma",
            base_pay=4.00,
            participants_per_demo_session=2,
            participants_per_session=2,
            subsession_apps=['prisoner', 'lab_results'],
            doc=""""""
        ),

        SessionType(
            name='Trust',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['trust', 'lab_results'],
            doc=""""""
        ),
                SessionType(
            name='Dictator',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['dictator', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matching Pennies',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['matching_pennies']*3 + ['lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Traveler Dilemma',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['traveler_dilemma', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Survey',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['survey', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Bargaining',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['bargaining', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Lying',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=1,
            subsession_apps=['lying']*5 + ['lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Guessing',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=10,
            subsession_apps=['guessing', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matrix Symmetric',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['matrix_symmetric', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matrix Asymmetric',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['matrix_asymmetric', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Cournot Competition',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['cournot_competition', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Stackelberg Competition',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['stackelberg_competition', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Private Value Auction',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=5,
            subsession_apps=['private_value_auction', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Volunteer Dilemma',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['volunteer_dilemma', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Bertrand Competition',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['bertrand_competition', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Principal Agent',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['principal_agent', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Coordination',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=2,
            subsession_apps=['coordination', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Stag Hunt',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['stag_hunt', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Battle of the sexes',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['battle_of_the_sexes', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Lemon Market',
            base_pay=10.00,
            participants_per_session=12,
            participants_per_demo_session=1,
            subsession_apps=['lemon_market', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Common Value Auction',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['common_value_auction', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Tragedy of the commons',
            base_pay=10.00,
            participants_per_session=2,
            participants_per_demo_session=2,
            subsession_apps=['tragedy_of_the_commons', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name="Showcase",
            base_pay=0,
            participants_per_demo_session=1,
            participants_per_session=1,
            subsession_apps=['showcase'],
            doc=""""""
        ),

    ]




def show_on_demo_page(session_type_name):
    return True

demo_page_intro_text = """
<p>
Click on one of the below links to learn more and play.
You can read the source code of these games <a href="https://github.com/oTree-org/otree">here</a>.
</p>

<p>For more information about oTree, go to <a href="http://www.otree.org/">oTree.org</a>.</p>
"""
