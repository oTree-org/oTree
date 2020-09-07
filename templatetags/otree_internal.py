from django import template
from django.urls import reverse, Resolver404
import otree.common_internal


NO_USER_MSG = '''
You must set the
OTREE_ADMIN_PASSWORD environment variable
(or disable authentication by unsetting OTREE_AUTH_LEVEL).
'''


register = template.Library()


@register.filter
def id(bound_field):
    widget = bound_field.field.widget
    for_id = widget.attrs.get('id') or bound_field.auto_id
    if for_id:
        for_id = widget.id_for_label(for_id)
    return for_id


def active_page(request, view_name, *args, **kwargs):
    if not request:
        return ""
    try:
        url = reverse(view_name, args=args)
        return "active" if url == request.path_info else ""
    except Resolver404:
        return ""


def ensure_superuser_exists():
    '''
    Creates a superuser on the fly, so that the user doesn't have to migrate
    or resetdb to get a superuser.
    If eventually we use migrations instead of resetdb, then maybe won't
    need this anymore.
    '''
    return otree.common_internal.ensure_superuser_exists()


register.simple_tag(name='ensure_superuser_exists',
                    func=ensure_superuser_exists)
register.simple_tag(name='active_page', func=active_page)

