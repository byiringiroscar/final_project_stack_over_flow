# Generated by Django 4.0.6 on 2022-09-06 23:34

import datetime
from django.db import migrations, models
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0023_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 9, 6, 23, 34, 24, 117512, tzinfo=timezone.utc)),
        ),
    ]
