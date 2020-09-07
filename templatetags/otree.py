from otree.currency import Currency

from .otree_tags import (
    template, FormFieldNode,
)
from otree.chat import chat_template_tag
from otree.api import safe_json
from otree.staticfiles import StaticNode

# renaming otree_tags to otree and removing internal tags
# this code is duplicated in otree_tags. I duplicate it rather than importing
# register, because PyCharm's autocomplete doesn't detect the import and
# flags all the template tags in yellow.

register = template.Library()
register.tag('formfield', FormFieldNode.parse)

NEXT_BUTTON_TEMPLATE_PATH = 'otree/tags/NextButton.html'
@register.inclusion_tag(NEXT_BUTTON_TEMPLATE_PATH)
def next_button(*args, **kwargs):
    return {}


def my_abs(val):
    '''
    it seems you can't use a builtin as a filter_func:
    File "C:\oTree\venv\lib\site-packages\django\template\base.py", line 1179, in filter
    filter_func._filter_name = name
    AttributeError: 'builtin_function_or_method' object has no attribute '_filter_name'
    '''
    return abs(val)

# it seems that if you use positional args, PyCharm autocomplete doesn't work
# (highlights in yellow)
register.filter('abs', my_abs)

# use decorator because that way, PyCharm
# will autocomplete it correctly (no yellow highlight)
# i think that's safer than registering the Currency function directly,
# because it seems that Library.filter mutates the filter_func (see above)
@register.filter
def c(val):
    return Currency(val)

@register.filter
def json(val):
    return safe_json(val)

# this code is duplicated in otree_tags.py
@register.inclusion_tag('otreechat_core/widget.html', takes_context=True, name='chat')
def chat(context, *args, **kwargs):
    return chat_template_tag(context, *args, **kwargs)


# this code is duplicated in otree_tags.py
@register.inclusion_tag('otree/tags/formfields.html', takes_context=True)
def formfields(context, *args, **kwargs):
    return context


@register.tag('static')
def do_static(parser, token):
    '''this is copied from Django source'''
    return StaticNode.handle_token(parser, token)