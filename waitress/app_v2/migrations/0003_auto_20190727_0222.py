# Generated by Django 2.2.2 on 2019-07-27 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("app_v2", "0002_auto_20190727_0221")]

    operations = [
        migrations.RemoveField(model_name="slackuser", name="id"),
        migrations.AlterField(
            model_name="slackuser",
            name="slack_id",
            field=models.CharField(
                blank=True,
                max_length=20,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
    ]
