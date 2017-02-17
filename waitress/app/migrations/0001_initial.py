# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MealService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('breakfast', models.BooleanField(default=False)),
                ('lunch', models.BooleanField(default=False)),
                ('untapped', app.models.JSONField(default=app.models.untapped_default, verbose_name=b'Untapped', null=True, editable=False, blank=True)),
                ('date', models.DateField()),
                ('date_modified', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MealSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.BooleanField(default=False)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Passphrase',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('word', models.CharField(unique=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SlackUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('id', models.AutoField(unique=True, serialize=False, primary_key=True)),
                ('slack_id', models.CharField(unique=True, max_length=20, blank=True)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=60, blank=True)),
                ('user_type', models.CharField(default=b'employee', max_length=20, choices=[(b'chef', b'chef'), (b'cleaner', b'cleaner'), (b'guest', b'guest'), (b'security', b'security'), (b'staff', b'staff')])),
                ('photo', models.CharField(default=b'', max_length=512)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='passphrase',
            name='user',
            field=models.ForeignKey(to='app.SlackUser'),
        ),
        migrations.AddField(
            model_name='mealservice',
            name='user',
            field=models.ForeignKey(to='app.SlackUser'),
        ),
    ]
