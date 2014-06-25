from ptree.session import SessionType


def session_types():
    return [
        SessionType(
            name='Dictator',
            base_pay=0,
            num_participants=2,
            subsession_apps=[
                'dictator',
            ],
            doc="""
            Dictator Game. Two player game.
            """
        ),
    ]


def show_on_demo_page(session_type_name):
    return True

demo_page_intro_text = 'Click on one of the below sessions to play.'