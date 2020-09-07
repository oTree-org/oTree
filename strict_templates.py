from django.template.base import FilterExpression, Node
from django.template.smartif import TokenBase

'''
Make templates strict.
This has the potential to break existing templates, especially those in Django core.
But I tested by dropping Django's widget_tests folder into our test suite and 
running those tests, and did not get any regressions (same number of tests fail,
and don't get any InvalidVariableError's).
Other parts of Django with templates, such as admin, admindocs, postgres(?), GIS,
are not used by oTree. So we just need to consider users' templates,
which are unlikely to rely on silent failures.
'''

def patch_filter_expression():
    '''
    don't allow code like {{ bogus }} or {{ player.bogus }} to fail silently
    '''

    # can't fix this through inheritance because the class name
    # is hardcoded in django.template.base.Parser.compile_filter()

    original_resolve = FilterExpression.resolve
    # block {{ bogus }} but allow {{ bogus|default:1 }}, which seems to be
    # a common pattern for defaulting if a var is not found
    def resolve(self, context, ignore_failures=False):
        if self.filters:
            # allow {{ bogus|default:1 }}
            return original_resolve(self, context, ignore_failures=True)
        else:
            # this covers the following cases:
            # {{ bogus }}
            # {% if bogus %}
            # if-statements use ignore_failures=True,
            # because of TemplateLiteral.eval()
            # a bit risky to override, because
            # if-statements on nonexistent variables exist in django core,
            # such as in django/forms/templates/django/forms/widgets:
            # {% if widget.attrs.class %}
            return original_resolve(self, context, ignore_failures=False)
    FilterExpression.resolve = resolve

def patch_smartif():
    '''
    SmartIf is for if-statements with multiple tokens, like {% if bogus == 1 %}
    == is by far the most commonly used
    but we need to patch all operators, because now when FilterExpression.resolve()
    can raise, these functions will swallow the exception and return False,
    which can silently change the behavior of certain template expressions,
    which is unacceptable.
    For example, if we don't do this, then
    {% bogus != 'ok' %}
    will evaluate to False!
    '''

    def make_infix_eval(func):
        '''see infix()'s Operator.eval()'''
        def new_eval(self, context):
            return func(context, self.first, self.second)
        return new_eval

    def make_prefix_eval(func):
        '''see prefix()'s Operator.eval()'''
        def new_eval(self, context):
            return func(context, self.first)
        return new_eval

    infix_operators = {
        'or': lambda context, x, y: x.eval(context) or y.eval(context),
        'and': lambda context, x, y: x.eval(context) and y.eval(context),
        'in': lambda context, x, y: x.eval(context) in y.eval(context),
        'not in': lambda context, x, y: x.eval(context) not in y.eval(context),
        'is': lambda context, x, y: x.eval(context) is y.eval(context),
        'is not': lambda context, x, y: x.eval(context) is not y.eval(context),
        '==': lambda context, x, y: x.eval(context) == y.eval(context),
        '!=': lambda context, x, y: x.eval(context) != y.eval(context),
        '>': lambda context, x, y: x.eval(context) > y.eval(context),
        '>=': lambda context, x, y: x.eval(context) >= y.eval(context),
        '<': lambda context, x, y: x.eval(context) < y.eval(context),
        '<=': lambda context, x, y: x.eval(context) <= y.eval(context),
    }

    from django.template.smartif import OPERATORS
    for operator, func in infix_operators.items():
        OPERATORS[operator].eval = make_infix_eval(func)
    OPERATORS['not'].eval = make_prefix_eval(lambda context, x: not x.eval(context))


def patch_28935():
    # if we do the above patch, we also need a patch for the open issue:
    # https://code.djangoproject.com/ticket/28935
    # usually in oTree the problem will be in the user's (child) template
    def render_annotated(self, context):
        try:
            return self.render(context)
        except Exception as e:
            if context.template.engine.debug and not hasattr(e, 'template_debug'):
                e.template_debug = context.template.get_exception_info(e, self.token)
            raise
    Node.render_annotated = render_annotated


def patch_template_silent_failures():
    patch_filter_expression()
    patch_smartif()
    patch_28935()



