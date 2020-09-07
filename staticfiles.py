'''
call this file staticfiles instead of static because PyCharm is confused
with otree/static (even though that's not a module)
'''

from django.templatetags.static import StaticNode as DjStaticNode
from django.template.base import FilterExpression


class BackslashError(ValueError):
    pass


class StaticNode(DjStaticNode):
    def __init__(self, varname=None, path:FilterExpression=None):
        # path.token is the literal string, not the value of the variable
        # it resolves to,
        # so there should never be a \
        if path and ('\\' in path.token):
            msg = (
                r'{{% static {} %}} '
                r'contains a backslash ("\"); '
                r'you should change it to a forward slash ("/").'
            ).format(path.token)
            raise BackslashError(msg)
        # should we also handle cases where the \ was in a variable?
        # then have to consider about os.path.join which will use os.sep
        super().__init__(varname, path)
