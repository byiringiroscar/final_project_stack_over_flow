# Generated by Django 4.0.6 on 2022-07-27 10:20

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('full_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_two_f_enable', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', models.ImageField(blank=True, default='profile.png', null=True, upload_to='images/')),
                ('location', models.CharField(blank=True, max_length=100, null=True)),
                ('about_me', models.TextField(blank=True, null=True)),
                ('github_link', models.URLField(blank=True, default='https://github.com/', null=True)),
                ('website_link', models.URLField(blank=True, default='https://www.google.com/', null=True)),
                ('backend_development', models.PositiveIntegerField(blank=True, null=True)),
                ('frontend_development', models.PositiveIntegerField(blank=True, null=True)),
                ('hardware', models.PositiveIntegerField(blank=True, null=True)),
                ('uiandux', models.PositiveIntegerField(blank=True, null=True)),
                ('artificial_intelligence', models.PositiveIntegerField(blank=True, null=True)),
                ('date_created', models.DateField(default=datetime.datetime(2022, 7, 27, 10, 20, 10, 680989, tzinfo=utc))),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
