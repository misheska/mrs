# Generated by Django 2.1.6 on 2019-03-13 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mrsstat', '0008_conflicting_mrsrequest_counts'),
    ]

    operations = [
        migrations.AddField(
            model_name='stat',
            name='mrsrequest_count_resolved',
            field=models.IntegerField(default=0, editable=False, verbose_name='Nb. demandes en conflit resolu (non-soumise inclues)'),
        ),
    ]
