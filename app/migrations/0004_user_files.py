# Generated by Django 5.1.6 on 2025-02-12 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_temp_mod_msgs'),
    ]

    operations = [
        migrations.CreateModel(
            name='user_files',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('doc', models.TextField()),
            ],
        ),
    ]
