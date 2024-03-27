# Generated by Django 5.0.2 on 2024-03-27 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Storedotps',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.EmailField(max_length=254)),
                ('otp', models.CharField(max_length=6)),
                ('is_active', models.BooleanField(default=True)),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
