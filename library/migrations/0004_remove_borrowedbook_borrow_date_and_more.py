# Generated by Django 5.0.6 on 2024-05-13 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0003_user_borrowedbook'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='borrowedbook',
            name='borrow_date',
        ),
        migrations.RemoveField(
            model_name='borrowedbook',
            name='return_date',
        ),
    ]
