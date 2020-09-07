import re
from django.core.signing import Signer
from otree.channels import utils as channel_utils
from django.utils.translation import ugettext as _

class ChatTagError(Exception):
    pass

class UNDEFINED:
    pass


def chat_template_tag(context, *, channel=UNDEFINED, nickname=UNDEFINED):
    player = context['player']
    group = context['group']
    Constants = context['Constants']
    participant = context['participant']

    if channel == UNDEFINED:
        channel = group.id
    channel = str(channel)
    # channel name should not contain illegal chars,
    # so that it can be used in JS and URLs
    if not re.match(r'^[a-zA-Z0-9_-]+$', channel):
        raise ChatTagError(
            "'channel' can only contain ASCII letters, numbers, underscores, and hyphens. "
            "Value given was: {}".format(channel))
    # prefix the channel name with session code and app name
    prefixed_channel = '{}-{}-{}'.format(
        context['session'].id,
        Constants.name_in_url,
        # previously used a hash() here to ensure name_in_url is the same,
        # but hash() is non-reproducible across processes
        channel
    )
    context['channel'] = prefixed_channel

    if nickname == UNDEFINED:
        # Translators: A player's default chat nickname,
        # which is "Player" + their ID in group. For example:
        # "Player 2".
        nickname = _('Participant {id_in_group}').format(id_in_group=player.id_in_group)
    nickname = str(nickname)
    nickname_signed = Signer().sign(nickname)

    socket_path = channel_utils.chat_path(prefixed_channel, participant.id)

    chat_vars_for_js = {
        'socket_path': socket_path,
        'channel': prefixed_channel,
        'participant_id': participant.id,
        'nickname_signed': nickname_signed,
        # Translators: the name someone sees displayed for themselves in a chat.
        # It's their nickname followed by "(Me)". For example:
        # "Michael (Me)" or "Player 1 (Me)".
        'nickname_i_see_for_myself': _("{nickname} (Me)").format(nickname=nickname)
    }

    context['chat_vars_for_js'] = chat_vars_for_js

    return context