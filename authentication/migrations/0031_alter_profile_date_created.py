# Generated by Django 4.0.6 on 2024-06-20 09:59

import datetime
from django.db import migrations, models
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0030_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2024, 6, 20, 9, 59, 7, 886406, tzinfo=timezone.utc)),
        ),
    ]
