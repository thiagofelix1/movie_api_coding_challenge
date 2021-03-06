# Generated by Django 4.0.5 on 2022-06-25 19:29

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_id', models.CharField(max_length=20)),
                ('movie_title', models.CharField(max_length=200)),
                ('note_value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('user_email', models.EmailField(max_length=254, verbose_name='email address')),
                ('user_nickname', models.CharField(max_length=20)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 6, 25, 19, 29, 46, 597081, tzinfo=utc))),
            ],
        ),
    ]
