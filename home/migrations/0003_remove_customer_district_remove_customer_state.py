# Generated by Django 5.0.1 on 2024-02-25 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0002_remove_hotel_district_remove_hotel_state"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customer",
            name="district",
        ),
        migrations.RemoveField(
            model_name="customer",
            name="state",
        ),
    ]
