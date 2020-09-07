# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0006_auto_20160708_0657'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='browserbotsubmit',
            name='participant',
        ),
        migrations.RemoveField(
            model_name='browserbotsubmit',
            name='session',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='_is_auto_playing',
        ),
        migrations.RemoveField(
            model_name='session',
            name='special_category',
        ),
        migrations.AddField(
            model_name='participant',
            name='_is_bot',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='_bots_errored',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='_bots_finished',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='_cannot_restart_bots',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='has_bots',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='is_demo',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.AddField(
            model_name='session',
            name='ready',
            field=otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False),
        ),
        migrations.DeleteModel(
            name='BrowserBotSubmit',
        ),
    ]
