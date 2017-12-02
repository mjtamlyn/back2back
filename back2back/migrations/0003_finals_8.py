# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back2back', '0002_auto_20161129_1358'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='final_match_6_score',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='entry',
            name='final_match_7_score',
            field=models.PositiveIntegerField(null=True, blank=True),
        ),
    ]
