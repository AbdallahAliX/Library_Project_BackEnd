# Generated by Django 5.0.6 on 2024-05-16 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_remove_borrowedbook_borrow_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='currentuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.user')),
            ],
        ),
    ]