"""
Conftest module to be used with bots, not the tests themselves.
"""


def pytest_addoption(parser):
    parser.addoption("--session_config_name")
    parser.addoption("--num_participants", type=int)
    parser.addoption("--export_path")


def pytest_generate_tests(metafunc):
    '''pass command line args to the test function'''
    option = metafunc.config.option

    metafunc.parametrize(
        "session_config_name,num_participants,export_path",
        [[option.session_config_name, option.num_participants, option.export_path]]
    )
