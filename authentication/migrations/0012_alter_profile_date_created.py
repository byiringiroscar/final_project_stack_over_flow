# Generated by Django 4.0.6 on 2022-07-21 19:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 7, 21, 19, 17, 57, 105199, tzinfo=utc)),
        ),
    ]
