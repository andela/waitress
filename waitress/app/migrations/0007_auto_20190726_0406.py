# Generated by Django 2.2.2 on 2019-07-26 04:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("app", "0006_auto_20190616_0954")]

    operations = [
        migrations.RenameField(
            model_name="slackuser", old_name="isActive", new_name="is_active"
        )
    ]
