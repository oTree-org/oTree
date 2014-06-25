from ptree.session import SessionType


def session_types():
    return [
        SessionType(
            name="Prisoner Dilemma",
            base_pay=400,
            num_participants=2,
            subsession_apps=[
                'prisoner_minimal',
            ],
            doc="""
            Minimal prisoner's dilemma game. Single treatment. The players are asked separately whether they want to
            cooperate or compete.Their choices directly determine the payoffs.
            """
        ),
        SessionType(
            name='Trust Game',
            base_pay=10,
            num_participants=2,
            subsession_apps=[
                'trust',
            ],
            doc="""
            Trust game. Single treatment. Both players are given an initial sum.
            One player may give part of the sum to the other player, who actually receives triple the amount.
            The second player may then give part of the now-tripled amount back to the first player.
            """
        ),
        SessionType(
            name='Dictator',
            base_pay=100,
            num_participants=2,
            subsession_apps=[
                'dictator',
            ],
            doc="""
            The Dictator Game. Single treatment. Two players: Dictator and other participant. Dictator is given some
            amount of money, while the other participant is given nothing.
            The Dictator is told that he must offer some amount of that money to the other participant, even
            if that amount is zero. Whatever amount the dictator offers to the other participant must be accepted.
            """
        ),
    ]


def show_on_demo_page(session_type_name):
    return True

demo_page_intro_text = 'Click on one of the below sessions to play.'