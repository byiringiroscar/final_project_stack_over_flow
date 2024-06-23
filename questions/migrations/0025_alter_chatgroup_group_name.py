# Generated by Django 4.0.6 on 2024-06-23 17:22

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0024_chatgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatgroup',
            name='group_name',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, max_length=100, unique=True),
        ),
    ]
