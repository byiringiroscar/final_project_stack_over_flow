# Generated by Django 4.0.6 on 2024-06-21 07:52

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from datetime import timezone

class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0031_alter_profile_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='date_created',
            field=models.DateField(default=datetime.datetime(2024, 6, 21, 7, 52, 5, 369480, tzinfo=timezone.utc)),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
