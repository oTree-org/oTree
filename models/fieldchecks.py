from django.core.exceptions import FieldDoesNotExist


def ensure_field(model, name, field):
    try:
        existing_field = model._meta.get_field(name)
    except FieldDoesNotExist:
        field.contribute_to_class(model, name)
    else:
        if not isinstance(existing_field, field.__class__):
            raise TypeError(
                '{model} requires a field with name {name} of type {type}.'
                .format(model=model, name=name, type=field.__class__.__name__))
    return field
