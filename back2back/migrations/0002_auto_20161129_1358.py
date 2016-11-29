# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back2back', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='third_group_index',
            field=models.PositiveIntegerField(help_text='indexed 0-5 to do the match layout', blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='third_group_number',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='third_group_placing',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='third_group_points',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='entry',
            name='third_group_score',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='score',
            name='stage',
            field=models.CharField(choices=[('first-round', 'First Round'), ('second-round', 'Second Round'), ('third-round', 'Third Round')], max_length=255),
        ),
    ]
