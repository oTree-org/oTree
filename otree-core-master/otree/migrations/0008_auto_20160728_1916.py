# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0007_auto_20160726_1956'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='participant',
            options={},
        ),
        migrations.AlterModelOptions(
            name='session',
            options={},
        ),
        migrations.AlterIndexTogether(
            name='participant',
            index_together=set([]),
        ),
    ]
