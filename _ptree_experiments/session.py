from ptree.session import SessionType


def session_types():

    return [
        SessionType(
            name="Prisoner Dilemma",
            base_pay=400,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['prisoner', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Trust',
            base_pay=10,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['trust', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Public Goods',
            base_pay=10,
            num_demo_participants=4,
            num_participants=12,
            subsession_apps=['public_goods', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Dictator',
            base_pay=100,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['dictator', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matching Pennies',
            base_pay=100,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['matching_pennies']*3 + ['lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Traveler Dilemma',
            base_pay=0,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['traveler_dilemma', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Survey',
            base_pay=0,
            num_demo_participants=1,
            num_participants=12,
            subsession_apps=['survey', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Bargaining',
            base_pay=0,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['bargaining', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Lying',
            base_pay=0,
            num_demo_participants=1,
            num_participants=12,
            subsession_apps=['lying', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Guessing',
            base_pay=0,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['guessing', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matrix Symmetric',
            base_pay=10,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['matrix_symmetric', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Matrix Asymmetric',
            base_pay=10,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['matrix_asymmetric', 'lab_results'],
            doc=""""""
        ),
        SessionType(
            name='Cournot Competition',
            base_pay=10,
            num_demo_participants=2,
            num_participants=12,
            subsession_apps=['cournot_competition', 'lab_results'],
            doc=""""""
        ),
    ]


def show_on_demo_page(session_type_name):

    return True

demo_page_intro_text = """
Click on one of the below links to learn more and play.
You can read the source code of these games <a href="https://github.com/wickens/ptree_library">here</a>.
"""
