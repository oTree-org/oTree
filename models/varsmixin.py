from otree.db import models

class _SaveTheChangeWithCustomFieldSupport:
    '''
    2017-08-07: kept around because old migrations files reference it.
    after a few months when i squash migrations,
    the references to this will be deleted, so i can delete it.

    2017-09-05: I found a bug with NumPy + SaveTheChange;
    https://github.com/karanlyons/django-save-the-change/issues/27
    So I need to use this again. Implementing a simplified version of what
    Gregor made a while back.

    2019-08-30: trying to remove SaveTheChange. but still need this because
    migrations files reference it.
    '''



class ModelWithVars(models.Model):

    class Meta:
        abstract = True

    vars = models._PickleField(default=dict)  # type: dict
