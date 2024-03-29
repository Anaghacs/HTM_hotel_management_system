# Generated by Django 5.0.2 on 2024-03-22 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0011_rename_chech_in_booking_check_in"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("customer", models.CharField(blank=True, max_length=40, null=True)),
                ("email_id", models.CharField(blank=True, max_length=150, null=True)),
                ("room_id", models.CharField(max_length=8)),
                ("finder", models.CharField(blank=True, max_length=150, null=True)),
                ("razorpay_order_id", models.CharField(max_length=60)),
                ("signature_id", models.CharField(max_length=128)),
                ("amount", models.CharField(blank=True, max_length=7, null=True)),
                ("paid_amount", models.BooleanField(default=False)),
                ("status", models.CharField(blank=True, max_length=20)),
                ("hotel", models.CharField(blank=True, max_length=50, null=True)),
                ("boock_date", models.DateTimeField(auto_now_add=True)),
                ("reason", models.CharField(blank=True, max_length=250, null=True)),
                ("code", models.CharField(blank=True, max_length=250, null=True)),
                ("source", models.CharField(blank=True, max_length=250, null=True)),
                ("step", models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
    ]
