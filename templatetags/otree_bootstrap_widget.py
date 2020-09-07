from django import template

register = template.Library()

@register.filter
def attrs_items(widget: dict):
    '''
    adds bootstrap class.

    the one thing missing is form-check on the div surrounding the option
    for radio buttons and checkbox (it's already added for radiohorizontal)

    maybe do this later. doesn't seem to improve the appearance
    (just indents it more which looks a bit weird)

    '''

    # for some reason 'type' is not always present
    # (seems to be the case for choice widgets)
    # that's why before we needed to use the |default filter
    input_type = widget.get('type')
    attrs = widget['attrs']
    if input_type in ['radio', 'checkbox']:
        bootstrap_class = 'form-check-input'
    else:
        bootstrap_class = 'form-control'
    if 'class' in attrs:
        attrs['class'] += (' ' + bootstrap_class)
    else:
        attrs['class'] = bootstrap_class
    return attrs.items()
