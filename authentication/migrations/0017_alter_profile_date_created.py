# Generated by Django 4.0.6 on 2022-08-28 12:09

import datetime
from django.db import migrations, models
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0016_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 8, 28, 12, 9, 26, 966568, tzinfo=timezone.utc)),
        ),
    ]
