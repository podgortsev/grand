# Generated by Django 5.1.6 on 2025-02-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mod_msgs',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
