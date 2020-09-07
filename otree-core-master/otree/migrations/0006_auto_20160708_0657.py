# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '0005_auto_20160707_1914'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalLockModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('locked', models.BooleanField(default=False)),
            ],
        ),
        migrations.DeleteModel(
            name='GlobalSingleton',
        ),
    ]
