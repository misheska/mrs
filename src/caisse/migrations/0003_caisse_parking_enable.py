# Generated by Django 2.0.5 on 2018-06-19 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('caisse', '0002_caisse_meta_option_change'),
    ]

    operations = [
        migrations.AddField(
            model_name='caisse',
            name='parking_enable',
            field=models.BooleanField(default=True, verbose_name='active la saisie de frais de parking'),
        ),
    ]
