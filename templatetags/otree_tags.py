from django import template

from otree.chat import chat_template_tag
from otree.common import safe_json
from otree.currency import Currency
from otree.templatetags.otree_internal import active_page, \
    ensure_superuser_exists
from .otree_forms import FormFieldNode
from otree.staticfiles import StaticNode

def c(val):
    return Currency(val)

def my_abs(val):
    '''
    it seems you can't use a builtin as a filter_func:
    File "C:\oTree\venv\lib\site-packages\django\template\base.py", line 1179, in filter
    filter_func._filter_name = name
    AttributeError: 'builtin_function_or_method' object has no attribute '_filter_name'
    '''
    return abs(val)

register = template.Library()
register.tag('formfield', FormFieldNode.parse)
register.filter(name='c', filter_func=c)
register.filter(name='abs', filter_func=my_abs)
register.filter('json', safe_json)

# this code is duplicated in otree.py
@register.inclusion_tag('otreechat_core/widget.html', takes_context=True)
def chat(context, *args, **kwargs):
    return chat_template_tag(context, *args, **kwargs)

@register.inclusion_tag('otree/tags/NextButton.html')
def next_button(*args, **kwargs):
    return {}

# this code is duplicated in otree.py
@register.inclusion_tag('otree/tags/formfields.html', takes_context=True)
def formfields(context, *args, **kwargs):
    return context

@register.tag('static')
def do_static(parser, token):
    '''this is copied from Django source'''
    return StaticNode.handle_token(parser, token)