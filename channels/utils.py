from django.core.signing import Signer
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

_group_send = get_channel_layer().group_send
_sync_group_send = async_to_sync(_group_send)



def sync_group_send_wrapper(*, type: str, group: str, event: dict):
    '''make it a function that takes proper args that are intuitive.
    enforces correct use.
    '''
    return _sync_group_send(group, {'type': type, **event})


def wait_page_group_name(session_id, page_index,
                         group_id_in_subsession=''):

    return 'wait-page-{}-page{}-{}'.format(
        session_id, page_index, group_id_in_subsession)


def gbat_group_name(session_id, page_index):
    return 'group_by_arrival_time_session{}_page{}'.format(
        session_id, page_index)

def gbat_path(session_id, index_in_pages, app_name, player_id):
    return '/group_by_arrival_time/{},{},{},{}/'.format(
        session_id, index_in_pages, app_name, player_id
        )

def room_participants_group_name(room_name):
    return 'room-participants-{}'.format(room_name)


def room_participant_path(room_name, participant_label, tab_unique_id):
    return '/wait_for_session_in_room/{},{},{}/'.format(
            room_name, participant_label, tab_unique_id
    )

def room_admin_group_name(room_name):
    return f'room-admin-{room_name}'

def room_admin_path(room_name):
    return '/room_without_session/{}/'.format(room_name)

def create_session_path():
    return '/create_session/'

def create_demo_session_path():
    return '/create_demo_session/'

def wait_page_path(session_pk, index_in_pages, group_id_in_subsession=''):
    return '/wait_page/{},{},{}/'.format(
        session_pk, index_in_pages, group_id_in_subsession
    )

def browser_bots_launcher_group(session_code):
    return 'browser-bots-client-{}'.format(session_code)

def browser_bots_launcher_path(session_code):
    return '/browser_bots_client/{}/'.format(session_code)

def auto_advance_path(participant_code, page_index):
    return '/auto_advance/{},{}/'.format(participant_code, page_index)

def auto_advance_group(participant_code):
    return f'auto-advance-{participant_code}'

def chat_path(channel, participant_id):
    channel_and_id = '{}/{}'.format(channel, participant_id)
    channel_and_id_signed = Signer(sep='/').sign(channel_and_id)

    return '/otreechat_core/{}/'.format(channel_and_id_signed)


def get_chat_group(channel):
    return 'otreechat-{}'.format(channel)