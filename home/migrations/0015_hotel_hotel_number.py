# Generated by Django 5.0.2 on 2024-03-30 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_remove_hotel_hotel_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='hotel_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
