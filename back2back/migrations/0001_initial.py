# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('category', models.CharField(choices=[('gents-recurve', 'Gents Recurve'), ('ladies-recurve', 'Ladies Recurve'), ('gents-compound', 'Gents Compound'), ('ladies-compound', 'Ladies Compound')], max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('agb_number', models.CharField(default='', blank=True, max_length=20, verbose_name='AGB number')),
                ('seeding', models.PositiveIntegerField(null=True, blank=True)),
                ('first_group_number', models.PositiveIntegerField(null=True, blank=True)),
                ('first_group_index', models.PositiveIntegerField(help_text='indexed 0-5 to do the match layout', null=True, blank=True)),
                ('first_group_placing', models.PositiveIntegerField(null=True, blank=True)),
                ('first_group_points', models.PositiveIntegerField(default=0)),
                ('first_group_score', models.PositiveIntegerField(default=0)),
                ('second_group_number', models.PositiveIntegerField(null=True, blank=True)),
                ('second_group_index', models.PositiveIntegerField(help_text='indexed 0-5 to do the match layout', null=True, blank=True)),
                ('second_group_placing', models.PositiveIntegerField(null=True, blank=True)),
                ('second_group_points', models.PositiveIntegerField(default=0)),
                ('second_group_score', models.PositiveIntegerField(default=0)),
                ('final_round_seed', models.PositiveIntegerField(null=True, blank=True)),
                ('final_match_1_score', models.PositiveIntegerField(null=True, blank=True)),
                ('final_match_2_score', models.PositiveIntegerField(null=True, blank=True)),
                ('final_match_3_score', models.PositiveIntegerField(null=True, blank=True)),
                ('final_match_4_score', models.PositiveIntegerField(null=True, blank=True)),
                ('final_match_5_score', models.PositiveIntegerField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'entries',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('stage', models.CharField(choices=[('first-round', 'First Round'), ('second-round', 'Second Round')], max_length=255)),
                ('time', models.PositiveIntegerField()),
                ('score', models.PositiveIntegerField()),
                ('points', models.PositiveIntegerField()),
                ('entry', models.ForeignKey(to='back2back.Entry', on_delete=models.CASCADE)),
                ('opponent', models.ForeignKey(null=True, related_name='opponent_score_set', to='back2back.Entry', blank=True, on_delete=models.CASCADE)),
            ],
        ),
    ]
