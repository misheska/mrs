# Generated by Django 2.1 on 2018-11-30 13:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mrsrequest', '0025_initial_data_distancevp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mrsrequest',
            old_name='mandate_date',
            new_name='mandate_datevp',
        ),
    ]