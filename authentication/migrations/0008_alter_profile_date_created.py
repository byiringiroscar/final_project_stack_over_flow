# Generated by Django 4.0.6 on 2022-07-30 20:54

import datetime
from django.db import migrations, models
from datetime import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2022, 7, 30, 20, 54, 28, 585331, tzinfo=timezone.utc)),
        ),
    ]
