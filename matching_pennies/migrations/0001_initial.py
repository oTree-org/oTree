# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('otree', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_is_missing_players', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], db_index=True, default=False)),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', otree.db.models.ForeignKey(to='otree.Session', related_name='matching_pennies_group')),
            ],
            options={
                'db_table': 'matching_pennies_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_index_in_game_pages', otree.db.models.PositiveIntegerField(null=True, default=0)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('payoff', otree.db.models.CurrencyField(max_digits=12, null=True)),
                ('training_question_1', otree.db.models.CharField(choices=[('Player 1 gets 0 points, Player 2 gets 0 points', 'Player 1 gets 0 points, Player 2 gets 0 points'), ('Player 1 gets 100 points, Player 2 gets 100 points', 'Player 1 gets 100 points, Player 2 gets 100 points'), ('Player 1 gets 100 points, Player 2 gets 0 points', 'Player 1 gets 100 points, Player 2 gets 0 points'), ('Player 1 gets 0 points, Player 2 gets 100 points', 'Player 1 gets 0 points, Player 2 gets 100 points')], max_length=100, null=True)),
                ('penny_side', otree.db.models.CharField(choices=[('Heads', 'Heads'), ('Tails', 'Tails')], max_length=500, null=True)),
                ('is_winner', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')])),
                ('group', otree.db.models.ForeignKey(to='matching_pennies.Group', null=True)),
                ('participant', otree.db.models.ForeignKey(to='otree.Participant', related_name='matching_pennies_player')),
                ('session', otree.db.models.ForeignKey(to='otree.Session', related_name='matching_pennies_player')),
            ],
            options={
                'db_table': 'matching_pennies_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', otree.db.models.ForeignKey(to='otree.Session', null=True, related_name='matching_pennies_subsession')),
            ],
            options={
                'db_table': 'matching_pennies_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=otree.db.models.ForeignKey(to='matching_pennies.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=otree.db.models.ForeignKey(to='matching_pennies.Subsession'),
        ),
    ]
