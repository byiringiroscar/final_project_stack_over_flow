# Generated by Django 4.0.6 on 2023-09-10 17:29

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0026_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 9, 10, 17, 29, 33, 711796, tzinfo=utc)),
        ),
    ]
