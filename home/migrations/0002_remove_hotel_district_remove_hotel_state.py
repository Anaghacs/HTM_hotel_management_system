# Generated by Django 5.0.1 on 2024-02-25 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="hotel",
            name="district",
        ),
        migrations.RemoveField(
            model_name="hotel",
            name="state",
        ),
    ]
