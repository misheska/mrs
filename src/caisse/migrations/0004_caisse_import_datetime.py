# Generated by Django 2.1 on 2019-01-02 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0003_caisse_parking_enable'),
    ]

    operations = [
        migrations.AddField(
            model_name='caisse',
            name='import_datetime',
            field=models.DateTimeField(null=True, verbose_name='Dernier import', blank=True),
        ),
    ]
