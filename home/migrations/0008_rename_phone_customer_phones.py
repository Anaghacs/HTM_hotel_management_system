# Generated by Django 5.0.2 on 2024-03-09 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0007_hotel_hotel_number"),
    ]

    operations = [
        migrations.RenameField(
            model_name="customer",
            old_name="phone",
            new_name="phones",
        ),
    ]