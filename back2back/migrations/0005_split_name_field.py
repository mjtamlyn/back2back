# Generated by Django 3.2.9 on 2021-12-02 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('back2back', '0004_remove_seedings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entry',
            old_name='name',
            new_name='surname',
        ),
        migrations.AddField(
            model_name='entry',
            name='forename',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
