# Generated by Django 5.0.2 on 2024-04-09 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_booking_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='cost',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]