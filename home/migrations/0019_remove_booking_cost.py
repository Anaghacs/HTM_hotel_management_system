# Generated by Django 5.0.2 on 2024-04-08 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_booking_cost_alter_order_room_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='cost',
        ),
    ]
