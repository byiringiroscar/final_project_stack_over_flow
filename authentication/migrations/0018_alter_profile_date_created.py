# Generated by Django 4.0.6 on 2022-09-02 15:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 9, 2, 15, 6, 41, 605179, tzinfo=utc)),
        ),
    ]
