# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0004_auto_20160704_1636'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StubModel',
            new_name='UndefinedFormModel',
        ),
    ]
