# Generated by Django 4.0.5 on 2022-06-26 22:33

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0003_comment_alter_score_date_replaycomment_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 22, 33, 44, 850494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='replaycomment',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 22, 33, 44, 850494, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='score',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2022, 6, 26, 22, 33, 44, 849488, tzinfo=utc)),
        ),
    ]