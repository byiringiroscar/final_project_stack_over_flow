# Generated by Django 4.0.6 on 2023-09-13 22:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0028_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2023, 9, 13, 22, 11, 18, 704062, tzinfo=utc)),
        ),
    ]